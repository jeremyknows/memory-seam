"""Portable Memory Seam no-live testing helpers."""

from __future__ import annotations

from pathlib import Path

from .descriptors import ContextSourceDescriptor, ContextSourceGrant, ContextSourceDescriptorRegistry

PROJECT_DOC_SAFE_SUMMARY = (
    "Sax can use the no-live Memory Seam project-doc fixture through a "
    "local MCP authority. The fixture proves an allowed "
    "agent:example/project grant, metadata-only retrieval, read-receipt "
    "propagation, and disabled-grant denial before source reads."
)


def synthetic_project_doc_fixture_allowlist(case: str):
    if case not in {"sax_project_doc_granted", "sax_project_doc_missing_grant", "sax_project_doc_disabled_grant"}:
        raise ValueError(f"unknown local context fixture case: {case}")
    descriptor = ContextSourceDescriptor(
        subject="agent:example",
        include_family="project",
        root_ref="synthetic-project-doc-root",
        relative_path="project/AGENTS.md",
        source_tier="project_doc",
        private_class="atlas_private",
        canonicality="canonical_source",
        retrieval_backend="metadata_only",
        max_bytes=1,
        stale_after_seconds=None,
        reportable=True,
        title="Sax project descriptor fixture",
        safe_summary=PROJECT_DOC_SAFE_SUMMARY,
    )
    registry = ContextSourceDescriptorRegistry.from_descriptors(
        roots={"synthetic-project-doc-root": Path("/tmp/synthetic-memory-seam-project-doc-root")},
        descriptors=[descriptor],
    )
    if case == "sax_project_doc_granted":
        grants = [ContextSourceGrant(subject="agent:example", include_family="project", reason="reviewed_static")]
    elif case == "sax_project_doc_disabled_grant":
        grants = [ContextSourceGrant(subject="agent:example", include_family="project", enabled=False, reason="reviewed_static")]
    else:
        grants = []
    return registry.to_allowlist(grants=grants)
