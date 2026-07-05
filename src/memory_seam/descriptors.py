"""No-live descriptor schema/verifier for Memory Seam context sources.

This module deliberately describes synthetic, exact registrations only. It does
not discover host paths, read profile/session/credential material, start a
service, or consume runtime registry state.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .contracts import (
    ContextSource,
    ContextSourceAllowlist,
    DEFAULT_CONTEXT_SOURCE_HARD_MAX_BYTES,
    DEFAULT_CONTEXT_SOURCE_MAX_BYTES,
    PROTECTED_CONTEXT_PATH_FRAGMENTS,
    PROTECTED_CONTEXT_PATH_NAMES,
    VALID_CONTEXT_INCLUDES,
)

VALID_CONTEXT_GRANT_REASONS = {
    "fixture",
    "legacy_test_only",
    "operator_approved",
    "reviewed_static",
    "supervised_real_read",
}
VALID_CONTEXT_RETRIEVAL_BACKENDS = {"filesystem", "metadata_only"}


@dataclass(frozen=True)
class ContextSourceDescriptor:
    """No-live real-source descriptor keyed by subject + include family.

    Descriptors are policy records, not discovery. They keep reportable output on
    opaque root labels plus relative paths; only the verifier materializes a
    ContextSource for later exact-path validation/read.
    """

    subject: str
    include_family: str
    root_ref: str
    relative_path: str
    source_tier: str
    private_class: str
    canonicality: str
    retrieval_backend: str = "filesystem"
    max_bytes: int = DEFAULT_CONTEXT_SOURCE_MAX_BYTES
    stale_after_seconds: int | None = 604_800
    reportable: bool = False
    enabled: bool = True
    title: str | None = None
    safe_summary: str | None = None

    def __post_init__(self) -> None:
        if self.include_family not in VALID_CONTEXT_INCLUDES:
            raise ValueError(f"unknown include_family: {self.include_family}")
        if not self.subject or not self.subject.strip():
            raise ValueError("subject must be non-empty")
        if not self.root_ref or not self.root_ref.strip():
            raise ValueError("root_ref must be non-empty")
        _validate_relative_descriptor_path(self.relative_path)
        if self.retrieval_backend not in VALID_CONTEXT_RETRIEVAL_BACKENDS:
            raise ValueError("retrieval_backend must be filesystem or metadata_only")
        if int(self.max_bytes) < 1 or int(self.max_bytes) > DEFAULT_CONTEXT_SOURCE_MAX_BYTES:
            raise ValueError(f"max_bytes must be 1..{DEFAULT_CONTEXT_SOURCE_MAX_BYTES}")
        if self.stale_after_seconds is not None and int(self.stale_after_seconds) < 0:
            raise ValueError("stale_after_seconds must be non-negative or null")


@dataclass(frozen=True)
class ContextSourceGrant:
    """Per-agent grant row for a registered context source family.

    Grant rows are intentionally tiny: they can only reference an exact
    ``(subject, include_family)`` descriptor key and can only disable/narrow that
    source. They do not carry paths, roots, token material, or discovery rules.
    """

    subject: str
    include_family: str
    enabled: bool = True
    reason: str | None = None

    def __post_init__(self) -> None:
        if not self.subject or not self.subject.strip():
            raise ValueError("grant subject must be non-empty")
        if self.include_family not in VALID_CONTEXT_INCLUDES:
            raise ValueError(f"unknown grant include_family: {self.include_family}")
        if self.reason is not None and self.reason not in VALID_CONTEXT_GRANT_REASONS:
            raise ValueError("grant reason must be a safe label")


@dataclass(frozen=True)
class ContextSourceGrantMatrix:
    """Canonical no-live grant matrix keyed by subject + include family."""

    grants: dict[tuple[str, str], ContextSourceGrant]

    @classmethod
    def from_grants(cls, grants: Iterable[ContextSourceGrant]) -> "ContextSourceGrantMatrix":
        keyed: dict[tuple[str, str], ContextSourceGrant] = {}
        for grant in grants:
            key = (grant.subject, grant.include_family)
            if key in keyed:
                raise ValueError(f"duplicate grant key: {grant.subject}/{grant.include_family}")
            keyed[key] = grant
        return cls(grants=keyed)

    def assert_descriptors_exist(self, descriptor_keys: set[tuple[str, str]]) -> None:
        missing = sorted(key for key in self.grants if key not in descriptor_keys)
        if missing:
            subject, include_family = missing[0]
            raise ValueError(f"grant references unknown descriptor: {subject}/{include_family}")

    def is_enabled(self, subject: str, include_family: str) -> bool:
        grant = self.grants.get((subject, include_family))
        return bool(grant and grant.enabled)

    def grant_for(self, subject: str, include_family: str) -> ContextSourceGrant | None:
        return self.grants.get((subject, include_family))


@dataclass(frozen=True)
class ContextSourceDescriptorRegistry:
    """Verifier/materializer for no-live descriptor registrations.

    Roots are injected by tests/operators as opaque labels. The registry never
    scans a root, expands globs, or substitutes a different subject/family.
    """

    roots: Mapping[str, Path]
    descriptors: dict[tuple[str, str], ContextSourceDescriptor]

    @classmethod
    def from_descriptors(
        cls,
        *,
        roots: Mapping[str, str | Path],
        descriptors: Iterable[ContextSourceDescriptor],
    ) -> "ContextSourceDescriptorRegistry":
        normalized_roots = {ref: Path(root) for ref, root in roots.items()}
        keyed: dict[tuple[str, str], ContextSourceDescriptor] = {}
        for descriptor in descriptors:
            if descriptor.root_ref not in normalized_roots:
                raise ValueError(f"unknown root_ref: {descriptor.root_ref}")
            key = (descriptor.subject, descriptor.include_family)
            if key in keyed:
                raise ValueError(f"duplicate descriptor key: {descriptor.subject}/{descriptor.include_family}")
            keyed[key] = descriptor
        return cls(roots=normalized_roots, descriptors=keyed)

    def to_allowlist(
        self,
        grants: ContextSourceGrantMatrix | Iterable[ContextSourceGrant] | None = None,
        *,
        allow_legacy_test_only_without_grants: bool = False,
    ):
        if grants is None:
            if not allow_legacy_test_only_without_grants:
                raise ValueError("grants are required for descriptor allowlist materialization")
            return ContextSourceAllowlist(
                registrations={key: self._to_context_source(descriptor) for key, descriptor in self.descriptors.items()}
            )

        grant_matrix = grants if isinstance(grants, ContextSourceGrantMatrix) else ContextSourceGrantMatrix.from_grants(grants)
        grant_matrix.assert_descriptors_exist(set(self.descriptors))
        registrations = {}
        policy_denials = {}
        for key, descriptor in self.descriptors.items():
            if not descriptor.enabled:
                policy_denials[key] = "descriptor_disabled"
                continue
            grant = grant_matrix.grant_for(*key)
            if grant is None:
                policy_denials[key] = "source_grant_missing"
            elif not grant.enabled:
                policy_denials[key] = "source_grant_disabled"
            else:
                registrations[key] = self._to_context_source(descriptor)
        return ContextSourceAllowlist(
            registrations=registrations,
            policy_denials=policy_denials,
        )

    def _to_context_source(self, descriptor: ContextSourceDescriptor):
        root = self.roots[descriptor.root_ref]
        path = root / descriptor.relative_path
        return ContextSource(
            include=descriptor.include_family,
            subject=descriptor.subject,
            path=str(path),
            root=str(root),
            source_tier=descriptor.source_tier,
            private_class=descriptor.private_class,
            max_bytes=descriptor.max_bytes,
            max_bytes_hard=DEFAULT_CONTEXT_SOURCE_HARD_MAX_BYTES,
            stale_after_seconds=descriptor.stale_after_seconds,
            enabled=descriptor.enabled,
            reportable=descriptor.reportable,
            title=descriptor.title,
            retrieval_backend=descriptor.retrieval_backend,
            canonicality=descriptor.canonicality,
            safe_summary=descriptor.safe_summary,
        )


def describe_context_source_descriptors(
    *,
    roots: Mapping[str, str | Path],
    descriptors: Iterable[ContextSourceDescriptor],
    grants: Iterable[ContextSourceGrant] | ContextSourceGrantMatrix | None = None,
) -> dict[str, Any]:
    """Return a reportable descriptor inventory without local root paths."""

    registry = ContextSourceDescriptorRegistry.from_descriptors(roots=roots, descriptors=descriptors)
    grant_matrix: ContextSourceGrantMatrix | None = None
    if grants is not None:
        grant_matrix = grants if isinstance(grants, ContextSourceGrantMatrix) else ContextSourceGrantMatrix.from_grants(grants)
        grant_matrix.assert_descriptors_exist(set(registry.descriptors))
    descriptor_rows = []
    for subject, include_family in sorted(registry.descriptors):
        descriptor = registry.descriptors[(subject, include_family)]
        descriptor_rows.append(
            {
                "key": [subject, include_family],
                "subject": subject,
                "include_family": include_family,
                "root_ref": descriptor.root_ref,
                "relative_path": descriptor.relative_path,
                "source_tier": descriptor.source_tier,
                "private_class": descriptor.private_class,
                "canonicality": descriptor.canonicality,
                "retrieval_backend": descriptor.retrieval_backend,
                "max_bytes": descriptor.max_bytes,
                "stale_after_seconds": descriptor.stale_after_seconds,
                "reportable": descriptor.reportable,
                "enabled": descriptor.enabled,
                "safe_summary_present": bool(descriptor.safe_summary),
                "grant_enabled": None if grant_matrix is None else grant_matrix.is_enabled(subject, include_family),
            }
        )
    grant_rows = []
    if grant_matrix is not None:
        for subject, include_family in sorted(grant_matrix.grants):
            grant = grant_matrix.grants[(subject, include_family)]
            grant_rows.append(
                {
                    "key": [subject, include_family],
                    "subject": subject,
                    "include_family": include_family,
                    "enabled": grant.enabled,
                    "reason_label": grant.reason,
                }
            )
    return {
        "descriptor_count": len(descriptor_rows),
        "grant_count": len(grant_rows),
        "root_refs": sorted(registry.roots),
        "descriptors": descriptor_rows,
        "grants": grant_rows,
        "no_live": {
            "reads_real_sources": False,
            "discovers_paths": False,
            "starts_service": False,
            "reads_credentials": False,
            "consumes_runtime_registry": False,
        },
    }


def _validate_relative_descriptor_path(relative_path: str) -> None:
    if not relative_path or not relative_path.strip():
        raise ValueError("relative_path must be non-empty")
    path = Path(relative_path)
    path_text = str(path)
    if path.is_absolute():
        raise ValueError("relative_path must be relative")
    raw_parts = relative_path.replace("\\", "/").split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise ValueError("relative_path must not contain empty/current/parent components")
    if any(char in path_text for char in "*?["):
        raise ValueError("relative_path must not contain wildcards")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("relative_path must not contain empty/current/parent components")
    if path.name in PROTECTED_CONTEXT_PATH_NAMES or path.name.startswith("state.db"):
        raise ValueError("relative_path must not target protected source names")
    normalized = "/" + path_text.replace("\\", "/")
    if any(fragment in normalized for fragment in PROTECTED_CONTEXT_PATH_FRAGMENTS):
        raise ValueError("relative_path must not target protected source fragments")
