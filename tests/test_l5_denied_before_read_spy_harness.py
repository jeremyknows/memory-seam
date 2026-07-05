from __future__ import annotations

import os
from dataclasses import dataclass

import pytest

from memory_seam.contracts import ContextReadKillSwitch, context_source_descriptor_id
from memory_seam.descriptors import ContextSourceDescriptorRegistry, ContextSourceGrant, ContextSourceGrantMatrix
from memory_seam.providers import NullMemorySeamProvider
from memory_seam.runtime import LocalReadOnlyRuntime, ReadOnlyRuntimeConfig, RuntimeRequest, StaticIdentityVerifier


@dataclass
class PreReadBoundarySpy:
    """Counters for surfaces that must stay cold for L5 denied requests."""

    provider_calls: int = 0
    source_read_calls: int = 0
    file_stat_calls: int = 0
    read_backend_calls: int = 0
    runtime_registry_calls: int = 0

    def snapshot(self) -> dict[str, int]:
        return {
            "provider_calls": self.provider_calls,
            "source_read_calls": self.source_read_calls,
            "file_stat_calls": self.file_stat_calls,
            "read_backend_calls": self.read_backend_calls,
            "runtime_registry_calls": self.runtime_registry_calls,
        }


class ExplodingLiveAdapterSpyProvider(NullMemorySeamProvider):
    """Provider spy that fails closed if a denied request reaches live-read territory."""

    def __init__(self, spy: PreReadBoundarySpy) -> None:
        self.spy = spy

    def context(self, **kwargs):  # pragma: no cover - denied requests must not enter provider code
        self.spy.provider_calls += 1
        self.spy.read_backend_calls += 1
        raise AssertionError("pre-read boundary failed: context provider reached after denial")

    def recall(self, query, **kwargs):  # pragma: no cover - denied requests must not enter provider code
        self.spy.provider_calls += 1
        self.spy.read_backend_calls += 1
        raise AssertionError("pre-read boundary failed: recall provider reached after denial")


def _runtime(spy: PreReadBoundarySpy, *, kill_switch: ContextReadKillSwitch | None = None) -> LocalReadOnlyRuntime:
    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, kill_switch=kill_switch),
        provider=ExplodingLiveAdapterSpyProvider(spy),
        identity_verifier=StaticIdentityVerifier(
            subject="agent:example",
            allowed_scopes=frozenset({"context", "context:project", "wiki"}),
        ),
    )


def _assert_denied_before_read(spy: PreReadBoundarySpy, response: dict, expected_error: str) -> None:
    assert response["status_code"] in {403, 404, 405, 503}, expected_error
    assert response["body"]["error"] == expected_error
    assert spy.snapshot() == {
        "provider_calls": 0,
        "source_read_calls": 0,
        "file_stat_calls": 0,
        "read_backend_calls": 0,
        "runtime_registry_calls": 0,
    }, f"pre-read boundary failed for {expected_error}: {spy.snapshot()}"
    runtime_receipt = response["body"]["runtime"]
    assert runtime_receipt["service_started"] is False
    assert runtime_receipt["runtime_registry_consumed"] is False
    assert runtime_receipt["write_custody_or_reindex"] is False


@pytest.mark.parametrize(
    ("case_name", "runtime_request", "expected_error", "kill_switch"),
    [
        (
            "unsupported_include_scope",
            RuntimeRequest("GET", "/context?include=unsupported_family"),
            "unsupported_context_include",
            None,
        ),
        (
            "unsupported_recall_scope",
            RuntimeRequest("GET", "/recall?scope=unsupported_family&query=boundary"),
            "unsupported_recall_scope",
            None,
        ),
        (
            "subject_mismatch",
            RuntimeRequest("GET", "/context?include=project&agent=watson"),
            "subject_agent_mismatch",
            None,
        ),
        (
            "disabled_family",
            RuntimeRequest("GET", "/context?include=project"),
            "source_family_disabled",
            ContextReadKillSwitch(disabled_families=frozenset({"project"}), reason="operator_hold"),
        ),
        (
            "revoked_generation",
            RuntimeRequest("GET", "/context?include=project"),
            "cache_generation_revoked",
            ContextReadKillSwitch(cache_generation="approved_generation", reason="operator_hold"),
        ),
        (
            "descriptor_removed",
            RuntimeRequest("GET", "/context?include=project"),
            "descriptor_disabled",
            ContextReadKillSwitch(
                disabled_descriptors=frozenset({context_source_descriptor_id("agent:example", "project")}),
                reason="operator_hold",
            ),
        ),
        (
            "write_like_route",
            RuntimeRequest("POST", "/diary/append"),
            "write_like_route_unavailable",
            None,
        ),
    ],
)
def test_l5_denied_requests_stop_before_live_adapter_sources_stats_backends_or_registry(
    monkeypatch, case_name, runtime_request, expected_error, kill_switch
):
    spy = PreReadBoundarySpy()

    def fail_if_stat(*args, **kwargs):  # pragma: no cover - denied requests must not stat sources
        spy.file_stat_calls += 1
        raise AssertionError(f"pre-read boundary failed for {case_name}: file/stat touched")

    monkeypatch.setattr(os, "stat", fail_if_stat)

    response = _runtime(spy, kill_switch=kill_switch).handle(runtime_request)

    _assert_denied_before_read(spy, response, expected_error)


def test_l5_removed_descriptor_grant_denies_before_source_stat_or_backend(monkeypatch, tmp_path):
    spy = PreReadBoundarySpy()

    def fail_if_stat(*args, **kwargs):  # pragma: no cover - removed descriptor must not stat paths
        spy.file_stat_calls += 1
        raise AssertionError("pre-read boundary failed: removed descriptor touched file/stat")

    monkeypatch.setattr(os, "stat", fail_if_stat)
    registry = ContextSourceDescriptorRegistry.from_descriptors(roots={"fixture_root": tmp_path}, descriptors=[])
    grants = ContextSourceGrantMatrix.from_grants([ContextSourceGrant("agent:example", "project", reason="fixture")])

    with pytest.raises(ValueError, match="grant references unknown descriptor: agent:example/project"):
        registry.to_allowlist(grants=grants)

    assert spy.snapshot() == {
        "provider_calls": 0,
        "source_read_calls": 0,
        "file_stat_calls": 0,
        "read_backend_calls": 0,
        "runtime_registry_calls": 0,
    }
