from __future__ import annotations

import os

import pytest

from memory_seam.descriptors import (
    ContextSourceDescriptor,
    ContextSourceDescriptorRegistry,
    ContextSourceGrant,
    ContextSourceGrantMatrix,
    describe_context_source_descriptors,
)
from memory_seam.runtime import (
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
)
from memory_seam.providers import NullMemorySeamProvider


class SpyProvider(NullMemorySeamProvider):
    def __init__(self):
        self.context_calls = 0
        self.recall_calls = 0

    def context(self, **kwargs):  # pragma: no cover - denial tests must not reach this
        self.context_calls += 1
        raise AssertionError("context provider must not be called before contract denial")

    def recall(self, query, **kwargs):  # pragma: no cover - denial tests must not reach this
        self.recall_calls += 1
        raise AssertionError("recall provider must not be called before contract denial")

    @property
    def read_calls(self) -> int:
        return self.context_calls + self.recall_calls


def _descriptor(**overrides) -> ContextSourceDescriptor:
    values = {
        "subject": "agent:example",
        "include_family": "project",
        "root_ref": "fixture_root",
        "relative_path": "docs/project.md",
        "source_tier": "synthetic_fixture",
        "private_class": "reportable_synthetic",
        "canonicality": "safe_fixture",
        "retrieval_backend": "filesystem",
        "max_bytes": 100,
    }
    values.update(overrides)
    return ContextSourceDescriptor(**values)


def test_schema_contract_inventory_names_required_surfaces_without_private_source_text(tmp_path):
    root = tmp_path / "fixture_root"
    target = root / "docs" / "project.md"
    target.parent.mkdir(parents=True)
    target.write_text("private fixture text must not appear in report", encoding="utf-8")

    descriptor = _descriptor(safe_summary="safe descriptor summary")
    grant = ContextSourceGrant(subject="agent:example", include_family="project", reason="fixture")

    report = describe_context_source_descriptors(
        roots={"fixture_root": root},
        descriptors=[descriptor],
        grants=[grant],
    )

    descriptor_row = report["descriptors"][0]
    assert descriptor_row["source_tier"] == "synthetic_fixture"
    assert descriptor_row["private_class"] == "reportable_synthetic"
    assert descriptor_row["canonicality"] == "safe_fixture"
    assert descriptor_row["retrieval_backend"] == "filesystem"
    assert descriptor_row["grant_enabled"] is True
    assert report["no_live"] == {
        "reads_real_sources": False,
        "discovers_paths": False,
        "starts_service": False,
        "reads_credentials": False,
        "consumes_runtime_registry": False,
    }
    rendered = repr(report)
    assert str(root) not in rendered
    assert "private fixture text" not in rendered


def test_missing_or_blank_grant_denies_by_default_before_stat_or_materialized_read(tmp_path, monkeypatch):
    root = tmp_path / "fixture_root"
    target = root / "docs" / "project.md"
    target.parent.mkdir(parents=True)
    target.write_text("source text must not be read", encoding="utf-8")
    registry = ContextSourceDescriptorRegistry.from_descriptors(
        roots={"fixture_root": root},
        descriptors=[_descriptor()],
    )

    def fail_if_stat(*args, **kwargs):  # pragma: no cover - should never be called
        pytest.fail("missing/blank grant denial attempted to stat a source")

    monkeypatch.setattr(os, "stat", fail_if_stat)

    allowlist = registry.to_allowlist(grants=[])

    assert allowlist.get("agent:example", "project") is None
    assert allowlist.denial_reason("agent:example", "project") == "source_grant_missing"
    assert allowlist.includes_for_subject("agent:example") == ["project"]


def test_disabled_descriptor_and_disabled_grant_contract_denials_materialize_no_sources(tmp_path, monkeypatch):
    root = tmp_path / "fixture_root"
    (root / "docs").mkdir(parents=True)

    def fail_if_stat(*args, **kwargs):  # pragma: no cover - should never be called
        pytest.fail("disabled descriptor/grant denial attempted to stat a source")

    monkeypatch.setattr(os, "stat", fail_if_stat)

    disabled_descriptor_registry = ContextSourceDescriptorRegistry.from_descriptors(
        roots={"fixture_root": root},
        descriptors=[_descriptor(enabled=False)],
    )
    descriptor_allowlist = disabled_descriptor_registry.to_allowlist(
        grants=[ContextSourceGrant(subject="agent:example", include_family="project", reason="fixture")]
    )
    assert descriptor_allowlist.get("agent:example", "project") is None
    assert descriptor_allowlist.denial_reason("agent:example", "project") == "descriptor_disabled"

    disabled_grant_registry = ContextSourceDescriptorRegistry.from_descriptors(
        roots={"fixture_root": root},
        descriptors=[_descriptor()],
    )
    grant_allowlist = disabled_grant_registry.to_allowlist(
        grants=[ContextSourceGrant(subject="agent:example", include_family="project", enabled=False, reason="fixture")]
    )
    assert grant_allowlist.get("agent:example", "project") is None
    assert grant_allowlist.denial_reason("agent:example", "project") == "source_grant_disabled"


def test_grant_cannot_create_unknown_descriptor_authority(tmp_path):
    registry = ContextSourceDescriptorRegistry.from_descriptors(
        roots={"fixture_root": tmp_path / "fixture_root"},
        descriptors=[_descriptor(include_family="project")],
    )
    grants = ContextSourceGrantMatrix.from_grants(
        [ContextSourceGrant(subject="agent:example", include_family="memory", reason="fixture")]
    )

    with pytest.raises(ValueError, match="grant references unknown descriptor: agent:example/memory"):
        registry.to_allowlist(grants=grants)


def test_unknown_family_runtime_denies_before_provider_backend_call():
    provider = SpyProvider()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        provider=provider,
        identity_verifier=StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context", "wiki"})),
    )

    context_response = runtime.handle(RuntimeRequest("GET", "/context?include=unknown_family"))
    recall_response = runtime.handle(RuntimeRequest("GET", "/recall?scope=unknown_family&query=boundary"))

    assert context_response["status_code"] == 403
    assert context_response["body"]["error"] == "unsupported_context_include"
    assert recall_response["status_code"] == 403
    assert recall_response["body"]["error"] == "unsupported_recall_scope"
    assert provider.read_calls == 0
