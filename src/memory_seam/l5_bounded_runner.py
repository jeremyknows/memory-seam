"""Default-off bounded runner shape for future repeated Memory Seam reads.

The runner is deliberately in-process and inert unless a caller supplies explicit
synthetic grant data and an execution approval marker. It does not schedule
itself, start services/listeners, consume Runtime Registry, mutate global config,
or touch write/custody/reindex surfaces.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .runtime import RuntimeRequest

L5_BOUNDED_RUNNER_SCHEMA = "memory_seam_l5_bounded_runner_v0"
L5_BOUNDED_RUNNER_STATUS = "default_off_bounded_runner_readiness_only"
L5_BOUNDED_RUNNER_MAX_TICKS = 5
L5_BOUNDED_RUNNER_HELD_SURFACES = (
    "cron_activation",
    "startup_activation",
    "service_listener_activation",
    "runtime_registry_consumption",
    "global_config_mutation",
    "unsupervised_recurring_reads",
    "write_custody_reindex",
    "provider_prod_canary_authority",
    "atlas_gate_movement",
)

_ALLOWED_SOURCE_FAMILIES = {"project"}
_ALLOWED_INCLUDE_SCOPES = {"project"}
_WRITE_LIKE_TERMS = ("write", "delete", "reindex", "custody", "purge")


class RunnerRuntime(Protocol):
    """Minimal runtime protocol consumed by the bounded runner."""

    def handle(self, request: RuntimeRequest) -> dict[str, Any]:
        """Handle one in-process request without runner-owned service activation."""
        ...


@dataclass(frozen=True)
class BoundedReadGrant:
    """Explicit metadata-only grant shape required before any tick can run."""

    subject: str
    source_family: str
    include_scope: str
    approval_label: str
    metadata_only: bool = True


@dataclass(frozen=True)
class BoundedRunnerConfig:
    """Default-off finite runner config for a future supervised canary.

    ``enabled`` and ``execution_approved`` both default to ``False`` so merely
    constructing the config cannot perform reads. ``expires_after_tick`` is an
    abstract counter supplied by tests/operators; the module does not inspect the
    clock, environment, Runtime Registry, or global configuration.
    """

    enabled: bool = False
    execution_approved: bool = False
    grant: BoundedReadGrant | None = None
    max_ticks: int = 1
    expires_after_tick: int = 0
    stop_on_denial: bool = True
    stop_on_error: bool = True
    recursion_guard_token: str = "memory_seam_l5_bounded_runner"
    receipt_target: str = "metadata_only_return_value"
    held_surfaces: tuple[str, ...] = L5_BOUNDED_RUNNER_HELD_SURFACES


@dataclass(frozen=True)
class BoundedRunnerPosture:
    """Side-effect counters asserted by tests and public receipts."""

    service_started: bool = False
    cron_or_startup_created: bool = False
    runtime_registry_consumed: bool = False
    global_config_mutation: bool = False
    source_discovery_called: bool = False
    credential_auth_env_keychain_authfile_reads: bool = False
    file_stat_calls: int = 0
    provider_prod_canary_authority: bool = False
    write_custody_or_reindex: bool = False
    atlas_gate_movement: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "service_started": self.service_started,
            "cron_or_startup_created": self.cron_or_startup_created,
            "runtime_registry_consumed": self.runtime_registry_consumed,
            "global_config_mutation": self.global_config_mutation,
            "source_discovery_called": self.source_discovery_called,
            "credential_auth_env_keychain_authfile_reads": self.credential_auth_env_keychain_authfile_reads,
            "file_stat_calls": self.file_stat_calls,
            "provider_prod_canary_authority": self.provider_prod_canary_authority,
            "write_custody_or_reindex": self.write_custody_or_reindex,
            "atlas_gate_movement": self.atlas_gate_movement,
        }


@dataclass
class BoundedRunnerReceiptBuilder:
    """Collects report-safe tick receipts for one bounded in-process run."""

    config: BoundedRunnerConfig
    current_tick: int
    ticks: list[dict[str, Any]] = field(default_factory=list)
    posture: BoundedRunnerPosture = field(default_factory=BoundedRunnerPosture)

    def build(self, decision: str, reason: str, *, stopped: bool = True) -> dict[str, Any]:
        return {
            "schema": L5_BOUNDED_RUNNER_SCHEMA,
            "status": L5_BOUNDED_RUNNER_STATUS,
            "decision": decision,
            "reason": reason,
            "default_off": not self.config.enabled,
            "execution_approved": self.config.execution_approved,
            "finite_repeat_count": self.config.max_ticks,
            "expires_after_tick": self.config.expires_after_tick,
            "current_tick": self.current_tick,
            "ticks_attempted": len(self.ticks),
            "stopped": stopped,
            "metadata_only": True,
            "receipt_target": self.config.receipt_target,
            "posture": self.posture.as_dict(),
            "ticks": self.ticks,
            "held_surfaces": list(self.config.held_surfaces),
            "authority_note": "readiness_only_not_unsupervised_or_recurring_unhold",
        }


class BoundedRunnerConfigError(ValueError):
    """Raised only by explicit validation helpers, never by background activation."""


def validate_bounded_runner_config(config: BoundedRunnerConfig, *, current_tick: int) -> str | None:
    """Return a safe denial reason when the runner must not execute."""

    if not config.enabled:
        return "runner_default_off"
    if not config.execution_approved:
        return "execution_approval_missing"
    if config.grant is None:
        return "explicit_source_grant_missing"
    if config.max_ticks < 1 or config.max_ticks > L5_BOUNDED_RUNNER_MAX_TICKS:
        return "finite_repeat_count_invalid"
    if current_tick > config.expires_after_tick:
        return "runner_expired"
    grant = config.grant
    if not grant.metadata_only:
        return "metadata_only_required"
    if _has_write_like_term(grant.source_family) or _has_write_like_term(grant.include_scope):
        return "write_like_or_custody_path_denied"
    if grant.source_family not in _ALLOWED_SOURCE_FAMILIES:
        return "unsupported_source_family"
    if grant.include_scope not in _ALLOWED_INCLUDE_SCOPES:
        return "unsupported_include_scope"
    if not _safe_label(grant.subject) or not _safe_label(grant.approval_label):
        return "unsafe_grant_label"
    return None


def run_bounded_read_ticks(
    runtime: RunnerRuntime,
    config: BoundedRunnerConfig,
    *,
    current_tick: int,
    active_recursion_token: str | None = None,
) -> dict[str, Any]:
    """Run a finite in-process tick loop only when explicitly enabled/approved.

    The function performs no scheduling and owns no provider/source discovery. It
    delegates a metadata-only request to the supplied runtime and stops on denial
    or error, returning a report-safe receipt.
    """

    builder = BoundedRunnerReceiptBuilder(config=config, current_tick=current_tick)
    if active_recursion_token == config.recursion_guard_token:
        return builder.build("DENY_BEFORE_READ", "anti_recursion_guard_active")

    denial_reason = validate_bounded_runner_config(config, current_tick=current_tick)
    if denial_reason is not None:
        return builder.build("DENY_BEFORE_READ", denial_reason)

    assert config.grant is not None  # narrowed by validation
    for ordinal in range(1, config.max_ticks + 1):
        if current_tick + ordinal - 1 > config.expires_after_tick:
            return builder.build("STOPPED", "runner_expired_mid_loop")
        request = RuntimeRequest(
            method="GET",
            target=(
                f"/context?include={config.grant.include_scope}"
                f"&agent={config.grant.subject}&read_receipt=metadata_only"
            ),
            body={
                "agent": config.grant.subject,
                "include": [config.grant.include_scope],
                "runner": "l5_bounded_metadata_only",
            },
        )
        try:
            response = runtime.handle(request)
        except Exception as exc:  # pragma: no cover - exact exception covered by tests via reason
            builder.ticks.append(
                {
                    "ordinal": ordinal,
                    "decision": "ERROR",
                    "reason": exc.__class__.__name__,
                    "metadata_only": True,
                }
            )
            if config.stop_on_error:
                return builder.build("STOPPED", "runtime_error")
            continue
        status_code = int(response.get("status_code", 0) or 0)
        decision = "ALLOWED" if 200 <= status_code < 300 else "DENIED"
        safe_reason = _safe_response_reason(response) if decision == "DENIED" else "metadata_only_tick_complete"
        builder.ticks.append(
            {
                "ordinal": ordinal,
                "decision": decision,
                "status_code": status_code,
                "reason": safe_reason,
                "metadata_only": True,
            }
        )
        if decision == "DENIED" and config.stop_on_denial:
            return builder.build("STOPPED", safe_reason)
    return builder.build("COMPLETE", "finite_repeat_count_reached", stopped=True)


def _safe_response_reason(response: dict[str, Any]) -> str:
    body = response.get("body")
    if isinstance(body, dict):
        reason = body.get("error") or body.get("reason")
        if isinstance(reason, str) and _safe_label(reason):
            return reason
    return "runtime_denied"


def _has_write_like_term(value: str) -> bool:
    lowered = value.lower()
    return any(term in lowered for term in _WRITE_LIKE_TERMS)


def _safe_label(value: str) -> bool:
    if not value or len(value) > 96:
        return False
    return all(char.isalnum() or char in {"_", "-", ":"} for char in value)


__all__ = [
    "BoundedReadGrant",
    "BoundedRunnerConfig",
    "BoundedRunnerConfigError",
    "BoundedRunnerPosture",
    "L5_BOUNDED_RUNNER_HELD_SURFACES",
    "L5_BOUNDED_RUNNER_MAX_TICKS",
    "L5_BOUNDED_RUNNER_SCHEMA",
    "L5_BOUNDED_RUNNER_STATUS",
    "RunnerRuntime",
    "run_bounded_read_ticks",
    "validate_bounded_runner_config",
]
