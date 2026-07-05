"""Provider protocols and null provider for Memory Seam core.

The provider layer is an API contract only. It defines the shape that Atlas or
other downstream adapters can implement without importing Atlas backends here.
The bundled ``NullMemorySeamProvider`` is deliberately no-live: it performs no
source reads, starts no services, and returns deterministic envelopes suitable
for route/schema tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Protocol, runtime_checkable

from .contracts import CONTRACT_STATUS


@runtime_checkable
class HealthProvider(Protocol):
    """Provider surface for the read-only health endpoint."""

    def health(self) -> dict[str, Any]:
        """Return metadata-only provider health."""
        ...


@runtime_checkable
class ContextProvider(Protocol):
    """Provider surface for the read-only context endpoint."""

    def context(
        self,
        *,
        include: list[str],
        mode: str,
        agent: str | None,
        token_subject: str | None,
        allowed_scopes: Iterable[str] | None,
        acting_for: str | None,
        timeout_ms: int,
        context_sources: Any = None,
        context_source_allowlist: Any = None,
        include_read_receipt: bool = False,
    ) -> dict[str, Any]:
        """Return a Memory Seam context envelope."""
        ...


@runtime_checkable
class RecallProvider(Protocol):
    """Provider surface for the read-only recall endpoint."""

    def recall(
        self,
        query: str,
        *,
        scope: str,
        agent: str | None,
        token_subject: str | None,
        allowed_scopes: Iterable[str] | None,
        acting_for: str | None,
        n: int,
        timeout_ms: int,
        context_sources: Any = None,
        context_source_allowlist: Any = None,
        include_read_receipt: bool = False,
    ) -> dict[str, Any]:
        """Return a Memory Seam recall envelope."""
        ...


@runtime_checkable
class MemorySeamProvider(HealthProvider, ContextProvider, RecallProvider, Protocol):
    """Complete read-only Memory Seam provider protocol."""


@dataclass(frozen=True)
class NullMemorySeamProvider:
    """Deterministic no-live provider used as the default contract stub.

    It is safe for package consumers and tests because it never discovers paths,
    reads private sources, contacts backends, starts listeners, consumes runtime
    registry state, or writes custody/reindex artifacts.
    """

    provider_name: str = "null"

    def health(self) -> dict[str, Any]:
        return {
            "ok": True,
            "provider": self.provider_name,
            "contract_status": CONTRACT_STATUS,
            "read_backend_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "write_custody_or_reindex": False,
        }

    def context(
        self,
        *,
        include: list[str],
        mode: str,
        agent: str | None,
        token_subject: str | None,
        allowed_scopes: Iterable[str] | None,
        acting_for: str | None,
        timeout_ms: int,
        context_sources: Any = None,
        context_source_allowlist: Any = None,
        include_read_receipt: bool = False,
    ) -> dict[str, Any]:
        return {
            "endpoint": "context",
            "provider": self.provider_name,
            "contract_status": CONTRACT_STATUS,
            "include_requested": list(include),
            "include_effective": [],
            "mode": mode,
            "agent": agent,
            "identity_subject": token_subject,
            "acting_for": acting_for,
            "allowed_scopes": sorted(set(allowed_scopes or [])),
            "timeout_ms": timeout_ms,
            "items": [],
            "partial": False,
            "degraded_reasons": ["provider_unconfigured"],
            "read_receipt_requested": include_read_receipt,
            "read_backend_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "write_custody_or_reindex": False,
        }

    def recall(
        self,
        query: str,
        *,
        scope: str,
        agent: str | None,
        token_subject: str | None,
        allowed_scopes: Iterable[str] | None,
        acting_for: str | None,
        n: int,
        timeout_ms: int,
        context_sources: Any = None,
        context_source_allowlist: Any = None,
        include_read_receipt: bool = False,
    ) -> dict[str, Any]:
        return {
            "endpoint": "recall",
            "provider": self.provider_name,
            "contract_status": CONTRACT_STATUS,
            "query": query,
            "scope_requested": scope,
            "scope_effective": [],
            "agent": agent,
            "identity_subject": token_subject,
            "acting_for": acting_for,
            "allowed_scopes": sorted(set(allowed_scopes or [])),
            "n": n,
            "timeout_ms": timeout_ms,
            "items": [],
            "partial": False,
            "degraded_reasons": ["provider_unconfigured"],
            "read_receipt_requested": include_read_receipt,
            "read_backend_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "write_custody_or_reindex": False,
        }


def provider_handlers(provider: MemorySeamProvider) -> dict[str, Any]:
    """Return ``route_request`` handler callables for a provider instance."""

    return {
        "health_handler": provider.health,
        "context_handler": provider.context,
        "recall_handler": provider.recall,
    }


__all__ = [
    "ContextProvider",
    "HealthProvider",
    "MemorySeamProvider",
    "NullMemorySeamProvider",
    "RecallProvider",
    "provider_handlers",
]
