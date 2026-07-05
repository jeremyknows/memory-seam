"""Portable no-live Memory Seam core contracts.

These types/constants intentionally avoid Atlas Query backend imports so they can
be packaged as the pure boundary while Atlas-specific adapters stay downstream.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from pathlib import Path
from typing import Any, Iterable
import os

CONTRACT_STATUS = "contract_authoritative_implementation_held"
READ_ENDPOINTS = ("context", "recall", "health")
WRITE_LIKE_ROUTES = (
    "POST /write",
    "POST /diary/append",
    "POST /draft/create",
    "POST /wiki/publish",
    "POST /confirm",
    "POST /thread/retire",
    "POST /curate",
    "POST /archive",
    "POST /delete",
    "POST /reindex",
)
WRITE_LIKE_PAYLOAD_KEYS = frozenset(
    {
        "write",
        "write_intent",
        "write_request",
        "delete",
        "delete_request",
        "reindex",
        "reindex_request",
        "custody",
        "custody_receipt",
        "custody_owner",
        "cache_purge",
    }
)
WRITE_LIKE_ACTION_VALUES = frozenset({"write", "delete", "reindex", "custody", "cache_purge", "purge"})
VALID_SCOPES = {"wiki", "diary", "session", "context", "all"}
VALID_CONTEXT_INCLUDES = {"user", "memory", "soul", "project", "last_session"}
CONTEXT_SCOPE_PREFIX = "context:"
MAX_RECALL_N = 20
MAX_QUERY_CHARS = 500
MAX_CONTEXT_INCLUDES = 10
MIN_TIMEOUT_MS = 1
MAX_TIMEOUT_MS = 10_000
DEFAULT_CONTEXT_SOURCE_MAX_BYTES = 12_000
DEFAULT_CONTEXT_SOURCE_HARD_MAX_BYTES = 24_000
PROTECTED_CONTEXT_PATH_NAMES = {".env", "auth.json", "state.db", "state.db-shm", "state.db-wal"}
PROTECTED_CONTEXT_PATH_FRAGMENTS = (
    "/sessions/",
    "/session/",
    "/logs/",
    "/gateway/",
    "/keychain/",
    "/oauth/",
    "/runtime-" + "registry.yaml",
)
SAFE_KILL_SWITCH_REASON_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
# ADR 0001 W2b: diary read ceiling sentinels (parity with adapter PR #191).
# Fail-closed: missing/unknown values normalize to SELF; FLEET widens only
# when the verifier explicitly grants it (never from query params or anonymous
# subjects).
DIARY_READ_CEILING_SELF = "self"
DIARY_READ_CEILING_FLEET = "fleet"
VALID_DIARY_READ_CEILINGS: frozenset[str] = frozenset({DIARY_READ_CEILING_SELF, DIARY_READ_CEILING_FLEET})


def payload_has_write_like_shape(payload: dict[str, Any] | None) -> bool:
    """Return true for write/custody/reindex-shaped request metadata.

    The helper intentionally reports only a boolean so denial responses never echo
    raw payload values, private paths, platform ids, credentials, or custody refs.
    """

    if not payload:
        return False
    for raw_key, value in payload.items():
        key = str(raw_key).strip().lower().replace("-", "_")
        if key in WRITE_LIKE_PAYLOAD_KEYS:
            return True
        if key in {"action", "operation", "intent", "route"}:
            values = value if isinstance(value, (list, tuple, set)) else (value,)
            for raw_value in values:
                normalized = str(raw_value).strip().lower().replace("-", "_")
                if normalized in WRITE_LIKE_ACTION_VALUES:
                    return True
    return False


@dataclass(frozen=True)
class SubjectPolicy:
    token_subject: str | None = None
    allowed_scopes: frozenset[str] = frozenset({"wiki", "diary", "context"})
    acting_for: str | None = None
    # Verifier-derived diary read ceiling (never from query params). "self"
    # keeps today's subject ceiling; "fleet" permits cross-agent diary recall
    # behind the enforced private-class wall. Fail-closed default.
    diary_read_ceiling: str = DIARY_READ_CEILING_SELF


@dataclass(frozen=True)
class ContextSource:
    include: str
    subject: str
    path: str
    source_tier: str
    private_class: str
    root: str | None = None
    max_bytes: int = DEFAULT_CONTEXT_SOURCE_MAX_BYTES
    max_bytes_hard: int = DEFAULT_CONTEXT_SOURCE_HARD_MAX_BYTES
    stale_after_seconds: int | None = 604_800
    enabled: bool = True
    reportable: bool = False
    title: str | None = None
    retrieval_backend: str = "filesystem"
    canonicality: str = "runtime_context"
    freshness_ts: str | None = None
    safe_summary: str | None = None
    source_card_count: int | None = None
    source_card_ids: tuple[str, ...] = ()
    source_card_safe_details: tuple[dict[str, Any], ...] = ()
    accepted_now: tuple[str, ...] = ()
    held_now: tuple[str, ...] = ()
    next_safe_action: str | None = None
    evidence_floor: str | None = None
    contributing_card_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ContextSourceAllowlist:
    registrations: dict[tuple[str, str], ContextSource]
    policy_denials: dict[tuple[str, str], str] | None = None

    @classmethod
    def from_sources(cls, sources: Iterable[ContextSource]) -> "ContextSourceAllowlist":
        registrations: dict[tuple[str, str], ContextSource] = {}
        for source in sources:
            registrations[(source.subject, source.include)] = source
        return cls(registrations=registrations)

    def get(self, token_subject: str, include_family: str) -> ContextSource | None:
        source = self.registrations.get((token_subject, include_family))
        if source is None:
            return None
        if source.subject != token_subject or source.include != include_family:
            return None
        return source

    def denial_reason(self, token_subject: str, include_family: str) -> str | None:
        if not self.policy_denials:
            return None
        return self.policy_denials.get((token_subject, include_family))

    def includes_for_subject(self, token_subject: str) -> list[str]:
        includes = [include for subject, include in self.registrations if subject == token_subject]
        if self.policy_denials:
            includes.extend(include for subject, include in self.policy_denials if subject == token_subject)
        return [include for include in dict.fromkeys(includes) if include in VALID_CONTEXT_INCLUDES]


@dataclass(frozen=True)
class ContextReadKillSwitch:
    disable_all: bool = False
    disabled_families: frozenset[str] = frozenset()
    disabled_descriptors: frozenset[str] = frozenset()
    cache_generation: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class SourceReadPlan:
    source: ContextSource
    resolved_path: Path
    resolved_root: Path
    max_bytes: int
    max_bytes_hard: int
    stat_result: os.stat_result


@dataclass(frozen=True)
class ContextSourceReadResult:
    text: str
    truncated: bool
    max_bytes_applied: bool
    freshness_ts: str | None
    source_age_seconds: int | None
    freshness_label: str


def context_source_descriptor_id(subject: str, include_family: str) -> str:
    digest = hashlib.sha256(f"{subject}\0{include_family}".encode("utf-8")).hexdigest()[:16]
    return f"descriptor-{digest}"


def kill_switch_snapshot(kill_switch: ContextReadKillSwitch | None) -> dict[str, Any] | None:
    if kill_switch is None:
        return None
    reason_code = None
    if kill_switch.reason:
        reason_code = kill_switch.reason if SAFE_KILL_SWITCH_REASON_RE.fullmatch(kill_switch.reason) else "operator_supplied"
    return {
        "effective": bool(
            kill_switch.disable_all
            or kill_switch.disabled_families
            or kill_switch.disabled_descriptors
            or kill_switch.cache_generation is not None
        ),
        "disable_all": kill_switch.disable_all,
        "disabled_families": sorted(kill_switch.disabled_families),
        "disabled_descriptors": sorted(kill_switch.disabled_descriptors),
        "cache_generation": kill_switch.cache_generation,
        "reason_code": reason_code,
        "deny_before_read_required": True,
    }


def kill_switch_denial_for(
    *,
    kill_switch: ContextReadKillSwitch | None,
    token_subject: str | None,
    include_family: str,
    cache_generation: str | None,
) -> str | None:
    if kill_switch is None:
        return None
    if kill_switch.disable_all:
        return "memory_seam_disabled"
    if include_family in kill_switch.disabled_families:
        return "source_family_disabled"
    if token_subject is not None:
        descriptor_id = context_source_descriptor_id(token_subject, include_family)
        if descriptor_id in kill_switch.disabled_descriptors:
            return "descriptor_disabled"
    if kill_switch.cache_generation is not None and cache_generation != kill_switch.cache_generation:
        return "cache_generation_revoked"
    return None
