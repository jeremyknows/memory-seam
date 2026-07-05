from __future__ import annotations

import os

import pytest

from memory_seam.descriptors import (
    ContextSourceDescriptor,
    ContextSourceDescriptorRegistry,
    ContextSourceGrant,
    ContextSourceGrantMatrix,
)
from memory_seam.providers import NullMemorySeamProvider
from memory_seam.runtime import (
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
)


class ReadSpyProvider(NullMemorySeamProvider):
    """Provider spy that proves contract denials happen before backend reads."""

    def __init__(self) -> None:
        self.context_calls = 0
        self.recall_calls = 0

    def context(self, **kwargs):  # pragma: no cover - denial cases must not reach this
        self.context_calls += 1
        raise AssertionError("context provider was called after a denial case")

    def recall(self, query, **kwargs):  # pragma: no cover - denial cases must not reach this
        self.recall_calls += 1
        raise AssertionError("recall provider was called after a denial case")

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


def _registry(tmp_path, descriptors):
    return ContextSourceDescriptorRegistry.from_descriptors(
        roots={"fixture_root": tmp_path / "fixture_root"},
        descriptors=descriptors,
    )


@pytest.mark.parametrize(
    ("name", "descriptors", "grants", "expected_reason"),
    [
        (
            "blank_grant_matrix",
            [_descriptor()],
            [],
            "source_grant_missing",
        ),
        (
            "disabled_grant",
            [_descriptor()],
            [ContextSourceGrant("agent:example", "project", enabled=False, reason="fixture")],
            "source_grant_disabled",
        ),
    ],
)
def test_descriptor_denial_fixture_matrix_denies_before_stat_or_materialized_read(
    tmp_path, monkeypatch, name, descriptors, grants, expected_reason
):
    stat_calls = 0

    def fail_if_stat(*args, **kwargs):  # pragma: no cover - should never be called
        nonlocal stat_calls
        stat_calls += 1
        raise AssertionError(f"{name} attempted to stat a source before denial")

    monkeypatch.setattr(os, "stat", fail_if_stat)

    allowlist = _registry(tmp_path, descriptors).to_allowlist(grants=grants)

    assert allowlist.get("agent:example", "project") is None, name
    assert allowlist.denial_reason("agent:example", "project") == expected_reason, name
    assert stat_calls == 0, name


def test_missing_descriptor_fixture_matrix_denies_before_stat_or_source_materialization(tmp_path, monkeypatch):
    stat_calls = 0

    def fail_if_stat(*args, **kwargs):  # pragma: no cover - should never be called
        nonlocal stat_calls
        stat_calls += 1
        raise AssertionError("missing descriptor grant attempted to stat a source")

    monkeypatch.setattr(os, "stat", fail_if_stat)
    registry = _registry(tmp_path, descriptors=[_descriptor(include_family="project")])
    grants = ContextSourceGrantMatrix.from_grants(
        [ContextSourceGrant("agent:example", "memory", reason="fixture")]
    )

    with pytest.raises(ValueError, match="grant references unknown descriptor: agent:example/memory"):
        registry.to_allowlist(grants=grants)

    assert stat_calls == 0


def test_unknown_family_fixture_matrix_denies_before_stat_provider_or_backend(monkeypatch):
    stat_calls = 0

    def fail_if_stat(*args, **kwargs):  # pragma: no cover - should never be called
        nonlocal stat_calls
        stat_calls += 1
        raise AssertionError("unknown family denial attempted to stat a source")

    monkeypatch.setattr(os, "stat", fail_if_stat)
    provider = ReadSpyProvider()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        provider=provider,
        identity_verifier=StaticIdentityVerifier(
            subject="agent:example",
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )

    context_response = runtime.handle(RuntimeRequest("GET", "/context?include=unknown_family"))
    recall_response = runtime.handle(RuntimeRequest("GET", "/recall?scope=unknown_family&query=boundary"))

    assert context_response["status_code"] == 403
    assert context_response["body"]["error"] == "unsupported_context_include"
    assert recall_response["status_code"] == 403
    assert recall_response["body"]["error"] == "unsupported_recall_scope"
    assert provider.read_calls == 0
    assert stat_calls == 0


@pytest.mark.parametrize(
    ("name", "runtime_request", "verifier", "expected_error"),
    [
        (
            "subject_mismatch",
            RuntimeRequest("GET", "/context?include=project&agent=watson"),
            StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context"})),
            "subject_agent_mismatch",
        ),
        (
            "audience_scope_mismatch",
            RuntimeRequest("GET", "/recall?scope=wiki&query=boundary"),
            StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context"})),
            "scope_not_allowed",
        ),
    ],
)
def test_subject_and_audience_mismatch_fixture_matrix_denies_before_provider_backend(
    name, runtime_request, verifier, expected_error
):
    provider = ReadSpyProvider()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        provider=provider,
        identity_verifier=verifier,
    )

    response = runtime.handle(runtime_request)

    assert response["status_code"] == 403, name
    assert response["body"]["error"] == expected_error, name
    assert provider.read_calls == 0, name
