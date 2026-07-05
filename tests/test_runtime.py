from __future__ import annotations

from memory_seam.contracts import ContextReadKillSwitch, context_source_descriptor_id
from memory_seam.providers import NullMemorySeamProvider
from memory_seam.receipts import RUNTIME_AUDIT_RECEIPT_VERSION, build_runtime_audit_receipt
from memory_seam.runtime import (
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
    runtime_health,
    runtime_idle_tick,
)


class CountingProvider(NullMemorySeamProvider):
    """Provider probe that records any read callback invocation."""

    def __init__(self):
        self.context_calls = 0
        self.recall_calls = 0

    def context(self, **kwargs):
        self.context_calls += 1
        return super().context(**kwargs)

    def recall(self, query, **kwargs):
        self.recall_calls += 1
        return super().recall(query, **kwargs)

    @property
    def read_calls(self):
        return self.context_calls + self.recall_calls


def test_runtime_health_is_default_off_and_no_service_started():
    health = runtime_health()
    assert health["runtime_status"] == "default_off_read_only_runtime_skeleton"
    assert health["default_off"] is True
    assert health["service_started"] is False
    assert health["runtime_registry_consumed"] is False
    assert health["audit_persisted"] is False
    assert health["write_custody_or_reindex"] is False
    assert "listener_activation" in health["held_surfaces"]


def test_idle_tick_is_metadata_only_and_touches_no_source_surfaces(monkeypatch):
    counters = {
        "provider_health": 0,
        "provider_context": 0,
        "provider_recall": 0,
        "route_request": 0,
        "open": 0,
        "os_stat": 0,
    }

    class ExplodingProvider(NullMemorySeamProvider):
        def health(self):  # pragma: no cover - must not be reached
            counters["provider_health"] += 1
            raise AssertionError("idle tick must not call provider health")

        def context(self, **kwargs):  # pragma: no cover - must not be reached
            counters["provider_context"] += 1
            raise AssertionError("idle tick must not call provider context")

        def recall(self, query, **kwargs):  # pragma: no cover - must not be reached
            counters["provider_recall"] += 1
            raise AssertionError("idle tick must not call provider recall")

    def fail_route_request(*args, **kwargs):  # pragma: no cover - must not be reached
        counters["route_request"] += 1
        raise AssertionError("idle tick must not route a read request")

    def fail_open(*args, **kwargs):  # pragma: no cover - must not be reached
        counters["open"] += 1
        raise AssertionError("idle tick must not read files")

    def fail_os_stat(*args, **kwargs):  # pragma: no cover - must not be reached
        counters["os_stat"] += 1
        raise AssertionError("idle tick must not stat files")

    monkeypatch.setattr("memory_seam.runtime.route_request", fail_route_request)
    monkeypatch.setattr("builtins.open", fail_open)
    monkeypatch.setattr("os.stat", fail_os_stat)

    runtime = LocalReadOnlyRuntime(provider=ExplodingProvider())
    tick = runtime.idle_tick()

    assert tick["tick"] == "idle"
    assert tick["metadata_only"] is True
    assert tick["read_backend_called"] is False
    assert tick["source_read_called"] is False
    assert tick["file_stat_called"] is False
    assert tick["service_started"] is False
    assert tick["runtime_registry_consumed"] is False
    assert tick["global_config_mutation"] is False
    assert tick["write_custody_or_reindex"] is False
    assert tick["unsupervised_read_unheld"] is False
    assert tick["write_custody_unheld"] is False
    assert counters == {
        "provider_health": 0,
        "provider_context": 0,
        "provider_recall": 0,
        "route_request": 0,
        "open": 0,
        "os_stat": 0,
    }
    assert runtime_idle_tick()["read_backend_called"] is False


def test_runtime_denies_reads_when_disabled_before_provider_call():
    class ExplodingProvider(NullMemorySeamProvider):
        def context(self, **kwargs):  # pragma: no cover - must not be reached
            raise AssertionError("provider should not be called while runtime is disabled")

    runtime = LocalReadOnlyRuntime(provider=ExplodingProvider())
    response = runtime.handle(RuntimeRequest("GET", "/context?include=project"))
    assert response["status_code"] == 503
    body = response["body"]
    assert body["error"] == "runtime_disabled"
    assert body["runtime"]["default_off"] is True
    assert body["runtime"]["service_started"] is False


def test_enabled_runtime_still_requires_identity_verifier():
    runtime = LocalReadOnlyRuntime(config=ReadOnlyRuntimeConfig(enabled=True))
    response = runtime.handle(RuntimeRequest("GET", "/context?include=project"))
    assert response["status_code"] == 403
    assert response["body"]["error"] == "identity_verifier_unconfigured"
    assert response["body"]["runtime"]["audit_persisted"] is False


def test_enabled_runtime_routes_null_provider_and_attaches_metadata_receipt():
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        identity_verifier=StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context"})),
    )
    response = runtime.handle(
        RuntimeRequest("GET", "/context?include=project&timeout_ms=250&read_receipt=metadata_only")
    )
    assert response["status_code"] == 200
    body = response["body"]
    assert body["endpoint"] == "context"
    assert body["identity_subject"] == "agent:example"
    assert body["read_backend_called"] is False
    assert body["service_started"] is False
    assert body["runtime_registry_consumed"] is False
    assert body["write_custody_or_reindex"] is False
    assert body["read_receipt"]["audit_shape"]["persisted"] is False
    assert body["runtime"]["audit_receipt"]["schema"] == RUNTIME_AUDIT_RECEIPT_VERSION
    assert body["runtime"]["audit_receipt"]["persisted"] is False
    assert body["runtime"]["audit_receipt"]["raw_content_persisted"] is False
    assert body["read_receipt"]["rollback_shape"]["cache_purge_required"] is False
    assert body["runtime"]["rollback"]["disable_runtime"] is True


def test_runtime_audit_receipt_is_stable_metadata_only():
    raw_path = "/private/source.md"
    raw_content = "secret source body that must not be retained"
    credential_ref = "credential:keychain:item"

    receipt = build_runtime_audit_receipt(
        decision="allowed",
        runtime_status="default_off_read_only_runtime_skeleton",
        endpoint="context",
        subject="agent:example",
        source_family="project",
        reason="operator_demo",
    )

    rendered = repr(receipt)
    assert receipt["schema"] == "memory_seam_runtime_audit_receipt_v0"
    assert receipt["schema_version"] == 0
    assert receipt["sink"] == "metadata_only_return_value"
    assert receipt["persisted"] is False
    assert receipt["raw_content_persisted"] is False
    assert receipt["raw_source_path_persisted"] is False
    assert receipt["credential_refs_persisted"] is False
    assert receipt["raw_subject_persisted"] is False
    assert receipt["privacy_pass"] is True
    assert raw_path not in rendered
    assert raw_content not in rendered
    assert credential_ref not in rendered
    assert "agent:example" not in rendered


def test_kill_switch_denies_before_identity_or_provider():
    class ExplodingIdentityVerifier:
        def verify(self, request):  # pragma: no cover - must not be reached
            raise AssertionError("identity verifier should not be called after global kill switch")

    provider = CountingProvider()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(
            enabled=True,
            kill_switch=ContextReadKillSwitch(disable_all=True, reason="operator_hold"),
        ),
        provider=provider,
        identity_verifier=ExplodingIdentityVerifier(),
    )
    response = runtime.handle(RuntimeRequest("GET", "/recall?query=roadmap"))
    assert response["status_code"] == 503
    assert response["body"]["error"] == "memory_seam_disabled"
    runtime_receipt = response["body"]["runtime"]
    assert runtime_receipt["write_custody_or_reindex"] is False
    assert runtime_receipt["rollback"] == {
        "disable_runtime": True,
        "disable_family": None,
        "disable_descriptor": None,
        "cache_generation": None,
        "cache_purge_required": False,
        "provider_restart_required": False,
        "write_custody_or_reindex_required": False,
    }
    assert provider.read_calls == 0


def test_kill_switch_family_denial_returns_safe_rollback_hint_before_read():
    provider = CountingProvider()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(
            enabled=True,
            kill_switch=ContextReadKillSwitch(disabled_families=frozenset({"project"}), reason="operator_hold"),
        ),
        provider=provider,
        identity_verifier=StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context"})),
    )

    response = runtime.handle(RuntimeRequest("GET", "/context?include=project"))

    assert response["status_code"] == 503
    assert response["body"]["error"] == "source_family_disabled"
    rollback = response["body"]["runtime"]["rollback"]
    assert rollback["disable_runtime"] is True
    assert rollback["disable_family"] == "project"
    assert rollback["disable_descriptor"] is None
    assert rollback["provider_restart_required"] is False
    assert rollback["write_custody_or_reindex_required"] is False
    assert provider.read_calls == 0


def test_kill_switch_descriptor_denial_returns_hashed_descriptor_only():
    subject = "agent:example"
    descriptor_id = context_source_descriptor_id(subject, "project")
    provider = CountingProvider()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(
            enabled=True,
            kill_switch=ContextReadKillSwitch(disabled_descriptors=frozenset({descriptor_id})),
        ),
        provider=provider,
        identity_verifier=StaticIdentityVerifier(subject=subject, allowed_scopes=frozenset({"context"})),
    )

    response = runtime.handle(RuntimeRequest("GET", "/context?include=project"))

    assert response["status_code"] == 503
    assert response["body"]["error"] == "descriptor_disabled"
    rollback = response["body"]["runtime"]["rollback"]
    assert rollback["disable_descriptor"] == descriptor_id
    assert rollback["disable_family"] is None
    assert "agent:example" not in repr(rollback)
    assert provider.read_calls == 0


def test_denial_before_read_regression_matrix():
    cases = [
        (
            "wrong_subject",
            RuntimeRequest("GET", "/context?include=project&agent=watson"),
            StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context"})),
            ReadOnlyRuntimeConfig(enabled=True),
            403,
            "subject_agent_mismatch",
        ),
        (
            "missing_context_scope",
            RuntimeRequest("GET", "/context?include=project"),
            StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"wiki"})),
            ReadOnlyRuntimeConfig(enabled=True),
            403,
            "scope_not_allowed",
        ),
        (
            "unsupported_include",
            RuntimeRequest("GET", "/context?include=keychain"),
            StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context"})),
            ReadOnlyRuntimeConfig(enabled=True),
            403,
            "unsupported_context_include",
        ),
        (
            "protected_write_route",
            RuntimeRequest("POST", "/diary/append"),
            StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context", "diary"})),
            ReadOnlyRuntimeConfig(enabled=True),
            405,
            "write_like_route_unavailable",
        ),
        (
            "disabled_source_family",
            RuntimeRequest("GET", "/context?include=project"),
            StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context"})),
            ReadOnlyRuntimeConfig(
                enabled=True,
                kill_switch=ContextReadKillSwitch(disabled_families=frozenset({"project"})),
            ),
            503,
            "source_family_disabled",
        ),
    ]

    for name, request, verifier, config, status_code, error_code in cases:
        provider = CountingProvider()
        runtime = LocalReadOnlyRuntime(config=config, provider=provider, identity_verifier=verifier)

        response = runtime.handle(request)

        assert response["status_code"] == status_code, name
        assert response["body"]["error"] == error_code, name
        assert provider.read_calls == 0, name
