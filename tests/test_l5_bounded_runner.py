from __future__ import annotations

import pytest

from memory_seam import (
    BoundedReadGrant,
    BoundedRunnerConfig,
    L5_BOUNDED_RUNNER_SCHEMA,
    LocalReadOnlyRuntime,
    NullMemorySeamProvider,
    ReadOnlyRuntimeConfig,
    StaticIdentityVerifier,
    run_bounded_read_ticks,
    validate_bounded_runner_config,
)
from memory_seam.runtime import RuntimeRequest


class SpyRuntime:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests: list[RuntimeRequest] = []
        self.provider_calls = 0
        self.backend_calls = 0
        self.source_reads = 0
        self.file_stat_calls = 0
        self.write_custody_or_reindex = False

    def handle(self, request: RuntimeRequest):
        self.requests.append(request)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


@pytest.fixture
def grant() -> BoundedReadGrant:
    return BoundedReadGrant(
        subject="agent:example",
        source_family="project",
        include_scope="project",
        approval_label="future_one_tick_canary_packet",
    )


def approved_config(grant: BoundedReadGrant, **overrides) -> BoundedRunnerConfig:
    values = {
        "enabled": True,
        "execution_approved": True,
        "grant": grant,
        "max_ticks": 2,
        "expires_after_tick": 10,
    }
    values.update(overrides)
    return BoundedRunnerConfig(**values)


def assert_zero_runner_side_effects(receipt):
    posture = receipt["posture"]
    assert posture["service_started"] is False
    assert posture["cron_or_startup_created"] is False
    assert posture["runtime_registry_consumed"] is False
    assert posture["global_config_mutation"] is False
    assert posture["source_discovery_called"] is False
    assert posture["credential_auth_env_keychain_authfile_reads"] is False
    assert posture["file_stat_calls"] == 0
    assert posture["provider_prod_canary_authority"] is False
    assert posture["write_custody_or_reindex"] is False
    assert posture["atlas_gate_movement"] is False


def test_default_off_runner_cannot_run_without_touching_runtime(grant):
    runtime = SpyRuntime([{"status_code": 200, "body": {}}])

    receipt = run_bounded_read_ticks(
        runtime,
        BoundedRunnerConfig(grant=grant),
        current_tick=1,
    )

    assert receipt["schema"] == L5_BOUNDED_RUNNER_SCHEMA
    assert receipt["decision"] == "DENY_BEFORE_READ"
    assert receipt["reason"] == "runner_default_off"
    assert receipt["ticks_attempted"] == 0
    assert runtime.requests == []
    assert_zero_runner_side_effects(receipt)
    assert receipt["authority_note"] == "readiness_only_not_unsupervised_or_recurring_unhold"


@pytest.mark.parametrize(
    ("config", "reason"),
    [
        (BoundedRunnerConfig(enabled=True, execution_approved=False), "execution_approval_missing"),
        (BoundedRunnerConfig(enabled=True, execution_approved=True), "explicit_source_grant_missing"),
        (
            BoundedRunnerConfig(
                enabled=True,
                execution_approved=True,
                grant=BoundedReadGrant(
                    subject="agent:example",
                    source_family="project",
                    include_scope="project",
                    approval_label="future_one_tick_canary_packet",
                    metadata_only=False,
                ),
                expires_after_tick=10,
            ),
            "metadata_only_required",
        ),
    ],
)
def test_runner_requires_approval_grant_and_metadata_only_before_read(config, reason):
    runtime = SpyRuntime([{"status_code": 200, "body": {}}])

    receipt = run_bounded_read_ticks(runtime, config, current_tick=1)

    assert receipt["decision"] == "DENY_BEFORE_READ"
    assert receipt["reason"] == reason
    assert receipt["ticks_attempted"] == 0
    assert runtime.requests == []
    assert_zero_runner_side_effects(receipt)


def test_runner_proves_finite_repeat_count_with_synthetic_runtime(grant):
    runtime = SpyRuntime(
        [
            {"status_code": 200, "body": {"endpoint": "context"}},
            {"status_code": 200, "body": {"endpoint": "context"}},
        ]
    )

    receipt = run_bounded_read_ticks(runtime, approved_config(grant, max_ticks=2), current_tick=1)

    assert receipt["decision"] == "COMPLETE"
    assert receipt["reason"] == "finite_repeat_count_reached"
    assert receipt["ticks_attempted"] == 2
    assert [tick["ordinal"] for tick in receipt["ticks"]] == [1, 2]
    assert all(tick["decision"] == "ALLOWED" for tick in receipt["ticks"])
    assert len(runtime.requests) == 2
    assert {request.method for request in runtime.requests} == {"GET"}
    assert all(request.target.startswith("/context?include=project&agent=agent:example") for request in runtime.requests)
    assert_zero_runner_side_effects(receipt)
    assert runtime.provider_calls == 0
    assert runtime.backend_calls == 0
    assert runtime.source_reads == 0
    assert runtime.file_stat_calls == 0
    assert runtime.write_custody_or_reindex is False


def test_runner_expiry_blocks_before_and_during_loop(grant):
    expired_runtime = SpyRuntime([{"status_code": 200, "body": {}}])
    expired = run_bounded_read_ticks(
        expired_runtime,
        approved_config(grant, expires_after_tick=2),
        current_tick=3,
    )
    assert expired["decision"] == "DENY_BEFORE_READ"
    assert expired["reason"] == "runner_expired"
    assert expired_runtime.requests == []

    mid_runtime = SpyRuntime(
        [
            {"status_code": 200, "body": {}},
            {"status_code": 200, "body": {}},
        ]
    )
    mid = run_bounded_read_ticks(
        mid_runtime,
        approved_config(grant, max_ticks=3, expires_after_tick=1),
        current_tick=1,
    )
    assert mid["decision"] == "STOPPED"
    assert mid["reason"] == "runner_expired_mid_loop"
    assert mid["ticks_attempted"] == 1
    assert len(mid_runtime.requests) == 1
    assert_zero_runner_side_effects(mid)


def test_runner_anti_recursion_guard_denies_before_read(grant):
    runtime = SpyRuntime([{"status_code": 200, "body": {}}])
    config = approved_config(grant, recursion_guard_token="same-token")

    receipt = run_bounded_read_ticks(
        runtime,
        config,
        current_tick=1,
        active_recursion_token="same-token",
    )

    assert receipt["decision"] == "DENY_BEFORE_READ"
    assert receipt["reason"] == "anti_recursion_guard_active"
    assert receipt["ticks_attempted"] == 0
    assert runtime.requests == []
    assert_zero_runner_side_effects(receipt)


def test_runner_stops_on_denial_and_error_without_retrying_broadly(grant):
    denied_runtime = SpyRuntime(
        [
            {"status_code": 403, "body": {"error": "scope_not_allowed"}},
            {"status_code": 200, "body": {}},
        ]
    )
    denied = run_bounded_read_ticks(denied_runtime, approved_config(grant, max_ticks=2), current_tick=1)
    assert denied["decision"] == "STOPPED"
    assert denied["reason"] == "scope_not_allowed"
    assert denied["ticks"] == [
        {"ordinal": 1, "decision": "DENIED", "status_code": 403, "reason": "scope_not_allowed", "metadata_only": True}
    ]
    assert len(denied_runtime.requests) == 1

    error_runtime = SpyRuntime([RuntimeError("backend unavailable"), {"status_code": 200, "body": {}}])
    errored = run_bounded_read_ticks(error_runtime, approved_config(grant, max_ticks=2), current_tick=1)
    assert errored["decision"] == "STOPPED"
    assert errored["reason"] == "runtime_error"
    assert errored["ticks"] == [{"ordinal": 1, "decision": "ERROR", "reason": "RuntimeError", "metadata_only": True}]
    assert len(error_runtime.requests) == 1
    assert_zero_runner_side_effects(errored)


def test_runner_refuses_write_like_custody_and_reindex_paths_before_runtime():
    runtime = SpyRuntime([{"status_code": 200, "body": {}}])
    for term in ("write", "delete", "reindex", "custody", "purge"):
        grant = BoundedReadGrant(
            subject="agent:example",
            source_family="project",
            include_scope=f"{term}_project",
            approval_label="future_one_tick_canary_packet",
        )
        receipt = run_bounded_read_ticks(runtime, approved_config(grant), current_tick=1)
        assert receipt["decision"] == "DENY_BEFORE_READ"
        assert receipt["reason"] == "write_like_or_custody_path_denied"
        assert receipt["ticks_attempted"] == 0
        assert_zero_runner_side_effects(receipt)
    assert runtime.requests == []


def test_runner_config_validation_limits_repeat_count_and_labels(grant):
    assert validate_bounded_runner_config(approved_config(grant, max_ticks=0), current_tick=1) == "finite_repeat_count_invalid"
    assert validate_bounded_runner_config(approved_config(grant, max_ticks=6), current_tick=1) == "finite_repeat_count_invalid"
    unsafe = BoundedReadGrant(
        subject="agent:example",
        source_family="project",
        include_scope="project",
        approval_label="contains/private/path",
    )
    assert validate_bounded_runner_config(approved_config(unsafe), current_tick=1) == "unsafe_grant_label"


def test_runner_can_use_local_runtime_without_activation(grant):
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        provider=NullMemorySeamProvider(),
        identity_verifier=StaticIdentityVerifier(subject="agent:example"),
    )

    receipt = run_bounded_read_ticks(runtime, approved_config(grant, max_ticks=1), current_tick=1)

    assert receipt["decision"] == "COMPLETE"
    assert receipt["ticks_attempted"] == 1
    assert receipt["ticks"][0]["status_code"] == 200
    assert_zero_runner_side_effects(receipt)
    health = runtime.health()
    assert health["service_started"] is False
    assert health["runtime_registry_consumed"] is False
    assert health["write_custody_or_reindex"] is False
