"""Default-off local read-only Memory Seam runtime skeleton.

This module is intentionally boring: it starts no listener, discovers no live
sources, consumes no Runtime Registry, and persists no audit data. It is a small
in-process wrapper around the existing router/provider contracts so downstream
adapters can prove L3 runtime posture before any service activation decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol, runtime_checkable

from urllib.parse import parse_qs, urlsplit

from .contracts import (
    CONTRACT_STATUS,
    VALID_CONTEXT_INCLUDES,
    VALID_SCOPES,
    WRITE_LIKE_ROUTES,
    ContextReadKillSwitch,
    context_source_descriptor_id,
    kill_switch_denial_for,
    kill_switch_snapshot,
    payload_has_write_like_shape,
)
from .policy import context_scope_allowed, policy, scope_allowed, subject_can_act_for_agent
from .providers import MemorySeamProvider, NullMemorySeamProvider, provider_handlers
from .receipts import build_read_receipt, build_runtime_audit_receipt, read_receipt_enabled
from .router import route_request

RUNTIME_STATUS = "default_off_read_only_runtime_skeleton"
RUNTIME_HELD_SURFACES = (
    "service_start",
    "listener_activation",
    "runtime_registry_consumption",
    "persistent_audit_sink",
    "global_config_mutation",
    "write_custody_reindex",
)


@dataclass(frozen=True)
class IdentityDecision:
    """Metadata-only result from a runtime identity verifier."""

    allowed: bool
    subject: str | None = None
    allowed_scopes: frozenset[str] = frozenset()
    acting_for: str | None = None
    reason: str | None = None


@runtime_checkable
class IdentityVerifier(Protocol):
    """Protocol for runtime identity verification.

    Implementations must not widen authority from request content alone. The
    default verifier below denies everything so the runtime remains default-off.
    """

    def verify(self, request: "RuntimeRequest") -> IdentityDecision:
        """Return the subject/scopes authorized for this in-process request."""
        ...


@dataclass(frozen=True)
class DenyAllIdentityVerifier:
    """Default verifier: no configured identity means no runtime reads."""

    reason: str = "identity_verifier_unconfigured"

    def verify(self, request: "RuntimeRequest") -> IdentityDecision:
        return IdentityDecision(allowed=False, reason=self.reason)


@dataclass(frozen=True)
class StaticIdentityVerifier:
    """Test/demo verifier for explicit subjects; it performs no external lookup."""

    subject: str
    allowed_scopes: frozenset[str] = frozenset({"context", "wiki", "diary"})
    acting_for: str | None = None

    def verify(self, request: "RuntimeRequest") -> IdentityDecision:
        return IdentityDecision(
            allowed=True,
            subject=self.subject,
            allowed_scopes=self.allowed_scopes,
            acting_for=self.acting_for,
        )


@dataclass(frozen=True)
class ReadOnlyRuntimeConfig:
    """Configuration for the local runtime wrapper.

    ``enabled`` defaults to False by design. Enabling still does not start a
    service; callers invoke ``handle`` directly and supply any provider/identity
    verifier explicitly.
    """

    enabled: bool = False
    provider_name: str = "null"
    kill_switch: ContextReadKillSwitch | None = None
    audit_sink: str = "metadata_only_return_value"
    persist_audit: bool = False
    service_start_allowed: bool = False
    consume_runtime_registry: bool = False
    held_surfaces: tuple[str, ...] = RUNTIME_HELD_SURFACES


@dataclass(frozen=True)
class RuntimeRequest:
    """In-process request shape for the default-off runtime skeleton."""

    method: str
    target: str
    headers: dict[str, str] = field(default_factory=dict)
    body: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LocalReadOnlyRuntime:
    """In-process runtime wrapper around Memory Seam router/provider contracts."""

    config: ReadOnlyRuntimeConfig = field(default_factory=ReadOnlyRuntimeConfig)
    provider: MemorySeamProvider = field(default_factory=NullMemorySeamProvider)
    identity_verifier: IdentityVerifier = field(default_factory=DenyAllIdentityVerifier)

    def health(self) -> dict[str, Any]:
        provider_health = self.provider.health()
        return {
            "ok": bool(self.config.enabled),
            "runtime_status": RUNTIME_STATUS,
            "contract_status": CONTRACT_STATUS,
            "provider": self.config.provider_name,
            "provider_health": provider_health,
            "default_off": not self.config.enabled,
            "read_only": True,
            "service_started": False,
            "service_start_allowed": self.config.service_start_allowed,
            "runtime_registry_consumed": self.config.consume_runtime_registry,
            "audit_sink": self.config.audit_sink,
            "audit_persisted": self.config.persist_audit,
            "write_custody_or_reindex": False,
            "held_surfaces": list(self.config.held_surfaces),
            "kill_switch": kill_switch_snapshot(self.config.kill_switch),
        }

    def idle_tick(self) -> dict[str, Any]:
        """Return a metadata-only idle tick without touching provider/source surfaces.

        This is narrower than ``health``: it deliberately does not call provider
        health, route parsing, source discovery, file stat/read helpers, Runtime
        Registry, service startup, global configuration, or write/custody/reindex
        paths. It is the safe in-process wake/check contract for L5 idle ticks.
        """

        return {
            "ok": True,
            "tick": "idle",
            "runtime_status": RUNTIME_STATUS,
            "contract_status": CONTRACT_STATUS,
            "default_off": not self.config.enabled,
            "read_only": True,
            "metadata_only": True,
            "read_backend_called": False,
            "source_read_called": False,
            "file_stat_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "global_config_mutation": False,
            "write_custody_or_reindex": False,
            "unsupervised_read_unheld": False,
            "write_custody_unheld": False,
            "held_surfaces": list(self.config.held_surfaces),
        }

    def handle(self, request: RuntimeRequest) -> dict[str, Any]:
        """Handle a request without starting listeners or discovering live sources."""

        if not self.config.enabled:
            return self._runtime_denial(503, "runtime_disabled")
        if self.config.kill_switch and self.config.kill_switch.disable_all:
            return self._runtime_denial(503, "memory_seam_disabled")

        identity = self.identity_verifier.verify(request)
        if not identity.allowed:
            return self._runtime_denial(403, identity.reason or "identity_denied")

        preflight_denial = self._preflight_read_denial(request, identity)
        if preflight_denial is not None:
            return preflight_denial

        routed = route_request(
            request.method,
            request.target,
            **provider_handlers(self.provider),
            read_receipt_enabled=read_receipt_enabled,
            token_subject=identity.subject,
            allowed_scopes=identity.allowed_scopes,
            acting_for=identity.acting_for,
            request_body=request.body,
        )
        body = dict(routed.get("body") or {})
        endpoint = body.get("endpoint")
        if endpoint in {"context", "recall"} and body.get("read_receipt_requested"):
            body["read_receipt"] = build_read_receipt(
                endpoint=str(endpoint),
                token_subject=identity.subject,
                timeout_ms=int(body.get("timeout_ms", 0) or 0),
                envelope=body,
            )
        body["runtime"] = self._runtime_receipt(
            "allowed",
            endpoint=str(endpoint or "runtime"),
            subject=identity.subject,
            source_family=self._runtime_source_family(str(endpoint or "runtime"), body),
        )
        return {**routed, "body": body}

    def _runtime_denial(
        self,
        status_code: int,
        reason: str,
        *,
        source_family: str | None = None,
        descriptor_id: str | None = None,
        cache_generation: str | None = None,
    ) -> dict[str, Any]:
        return {
            "status_code": status_code,
            "headers": {"content-type": "application/json"},
            "body": {
                "error": reason,
                "contract_status": CONTRACT_STATUS,
                "runtime_status": RUNTIME_STATUS,
                "runtime": self._runtime_receipt(
                    reason,
                    source_family=source_family,
                    reason=reason,
                    descriptor_id=descriptor_id,
                    cache_generation=cache_generation,
                ),
            },
        }

    def _preflight_read_denial(
        self, request: RuntimeRequest, identity: IdentityDecision
    ) -> dict[str, Any] | None:
        """Deny unauthorized read requests before provider callbacks are built.

        This duplicates only the small amount of route/query inspection needed to
        keep read authorization ahead of any provider source-card or backend
        access. The router still owns final request parsing for allowed traffic.
        """

        normalized_method = request.method.upper()
        parsed = urlsplit(request.target)
        path = parsed.path or "/"
        params = parse_qs(parsed.query, keep_blank_values=True)
        route = f"{normalized_method} {path}"

        if route in WRITE_LIKE_ROUTES:
            return self._runtime_denial(405, "write_like_route_unavailable")
        if path not in {"/health", "/context", "/recall"}:
            return self._runtime_denial(404, "route_not_found")
        if normalized_method != "GET":
            return self._runtime_denial(405, "method_not_allowed")
        if payload_has_write_like_shape({key: values for key, values in params.items()}) or payload_has_write_like_shape(
            request.body
        ):
            return self._runtime_denial(405, "write_like_payload_unavailable")
        if path == "/health":
            return None

        subject_policy = policy(identity.subject, identity.allowed_scopes, acting_for=identity.acting_for)
        agent = self._first(params, "agent")
        if self._body_mismatch(request.body, "agent", agent):
            return self._runtime_denial(403, "query_body_identity_mismatch")
        if not subject_can_act_for_agent(agent, subject_policy):
            return self._runtime_denial(403, "subject_agent_mismatch")

        if path == "/context":
            includes = self._csv_list(self._first(params, "include")) or ["project"]
            body_includes = self._body_list(request.body, "include")
            if body_includes and body_includes != includes:
                return self._runtime_denial(403, "query_body_identity_mismatch")
            for include_family in includes:
                if include_family not in VALID_CONTEXT_INCLUDES:
                    return self._runtime_denial(403, "unsupported_context_include")
                if not context_scope_allowed(subject_policy, include_family):
                    return self._runtime_denial(403, "scope_not_allowed")
                kill_switch_denial = kill_switch_denial_for(
                    kill_switch=self.config.kill_switch,
                    token_subject=identity.subject,
                    include_family=include_family,
                    cache_generation=None,
                )
                if kill_switch_denial is not None:
                    descriptor_id = None
                    if identity.subject is not None:
                        descriptor_id = context_source_descriptor_id(identity.subject, include_family)
                    return self._runtime_denial(
                        503,
                        kill_switch_denial,
                        source_family=include_family,
                        descriptor_id=descriptor_id,
                        cache_generation=self.config.kill_switch.cache_generation if self.config.kill_switch else None,
                    )
            return None

        scope = self._first(params, "scope", "wiki") or "wiki"
        if self._body_mismatch(request.body, "scope", scope):
            return self._runtime_denial(403, "query_body_identity_mismatch")
        if scope not in VALID_SCOPES:
            return self._runtime_denial(403, "unsupported_recall_scope")
        if not scope_allowed(subject_policy, scope):
            return self._runtime_denial(403, "scope_not_allowed")
        return None

    @staticmethod
    def _first(params: dict[str, list[str]], key: str, default: str | None = None) -> str | None:
        values = params.get(key)
        if not values:
            return default
        return values[0]

    @staticmethod
    def _csv_list(value: str | None) -> list[str]:
        if not value:
            return []
        return [part.strip() for part in value.split(",") if part.strip()]

    @classmethod
    def _body_list(cls, body: dict[str, Any], key: str) -> list[str]:
        value = body.get(key)
        if value is None:
            return []
        if isinstance(value, str):
            return cls._csv_list(value) or [value]
        if isinstance(value, Iterable):
            return [str(part).strip() for part in value if str(part).strip()]
        return [str(value)]

    @classmethod
    def _body_mismatch(cls, body: dict[str, Any], key: str, query_value: str | None) -> bool:
        values = cls._body_list(body, key)
        if not values:
            return False
        return values != ([query_value] if query_value is not None else [])

    @staticmethod
    def _runtime_source_family(endpoint: str, body: dict[str, Any]) -> str:
        if endpoint == "context":
            includes = body.get("include_effective") or body.get("include_requested") or []
            return str(includes[0]) if len(includes) == 1 else "multi_context"
        if endpoint == "recall":
            scope = str(body.get("scope_requested") or "wiki")
            return scope if scope != "all" else "multi_scope"
        return "runtime"

    def _runtime_receipt(
        self,
        decision: str,
        *,
        endpoint: str | None = None,
        subject: str | None = None,
        source_family: str | None = None,
        reason: str | None = None,
        descriptor_id: str | None = None,
        cache_generation: str | None = None,
    ) -> dict[str, Any]:
        return {
            "schema": "memory_seam_runtime_receipt_v0",
            "decision": decision,
            "default_off": not self.config.enabled,
            "read_only": True,
            "audit_sink": self.config.audit_sink,
            "audit_persisted": self.config.persist_audit,
            "audit_receipt": build_runtime_audit_receipt(
                decision=decision,
                runtime_status=RUNTIME_STATUS,
                endpoint=endpoint,
                subject=subject,
                source_family=source_family,
                reason=reason,
                sink=self.config.audit_sink,
                persist=self.config.persist_audit,
            ),
            "service_started": False,
            "runtime_registry_consumed": self.config.consume_runtime_registry,
            "write_custody_or_reindex": False,
            "rollback": self._rollback_hint(
                reason or decision,
                source_family=source_family,
                descriptor_id=descriptor_id,
                cache_generation=cache_generation,
            ),
            "held_surfaces": list(self.config.held_surfaces),
        }

    @staticmethod
    def _rollback_hint(
        reason: str,
        *,
        source_family: str | None = None,
        descriptor_id: str | None = None,
        cache_generation: str | None = None,
    ) -> dict[str, Any]:
        """Return safe operator rollback hints without source reads or raw subjects."""

        hint: dict[str, Any] = {
            "disable_runtime": True,
            "disable_family": None,
            "disable_descriptor": None,
            "cache_generation": None,
            "cache_purge_required": False,
            "provider_restart_required": False,
            "write_custody_or_reindex_required": False,
        }
        if reason == "source_family_disabled":
            hint["disable_family"] = source_family
        elif reason == "descriptor_disabled":
            hint["disable_descriptor"] = descriptor_id
        elif reason == "cache_generation_revoked":
            hint["cache_generation"] = cache_generation
            hint["cache_purge_required"] = True
        return hint


def runtime_health(config: ReadOnlyRuntimeConfig | None = None) -> dict[str, Any]:
    """Return default-off runtime health without constructing a service."""

    return LocalReadOnlyRuntime(config=config or ReadOnlyRuntimeConfig()).health()


def runtime_idle_tick(config: ReadOnlyRuntimeConfig | None = None) -> dict[str, Any]:
    """Return the L5 metadata-only idle tick without provider/source access."""

    return LocalReadOnlyRuntime(config=config or ReadOnlyRuntimeConfig()).idle_tick()


__all__ = [
    "DenyAllIdentityVerifier",
    "IdentityDecision",
    "IdentityVerifier",
    "LocalReadOnlyRuntime",
    "RUNTIME_HELD_SURFACES",
    "RUNTIME_STATUS",
    "ReadOnlyRuntimeConfig",
    "RuntimeRequest",
    "StaticIdentityVerifier",
    "runtime_health",
    "runtime_idle_tick",
]
