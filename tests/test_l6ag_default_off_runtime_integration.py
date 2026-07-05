from __future__ import annotations

from memory_seam.l6ag_default_off_runtime_integration import (
    L6AH_ADAPTER_VALUE_REF,
    L6AH_ALLOWED_FILE_ENVELOPE,
    L6AH_DENIED_STATUS,
    L6AH_GUARDED_COUNTERS,
    L6AH_HELD_SURFACES,
    L6AH_ISSUE_NUMBER,
    L6AH_OPERATION_CLASS,
    L6AH_PASS_STATUS,
    L6AH_REPOSITORY,
    L6AH_SOURCE_FLOOR,
    adapter_value_denial_reasons_l6ah01,
    approval_denial_reasons_l6ah01,
    approval_matches_l6ah01,
    build_l6ah01_exact_approval_fixture,
    build_l6ah01_report_safe_adapter_value_fixture,
    integrate_l6ah01_report_safe_adapter_value,
    validate_l6ah01_runtime_integration_output,
)


def test_missing_approval_denies_default_off_before_runtime_integration() -> None:
    output = integrate_l6ah01_report_safe_adapter_value(None)

    assert output["status"] == L6AH_DENIED_STATUS
    assert output["approval_result"] == "DENY_BEFORE_RUNTIME_INTEGRATION"
    assert output["approval_matched"] is False
    assert output["default_off_denied"] is True
    assert output["allowed"] is False
    assert output["integration_slice_count"] == 0
    assert output["runtime_use_smoke_count"] == 0
    assert output["live_adapter_invoked"] is False
    assert output["callback_invoked"] is False
    assert output["registry_consumed"] is False
    assert output["persistence_attempted"] is False
    assert output["activation_attempted"] is False
    assert output["broad_allowed_attempted"] is False
    assert all(value == 0 for value in output["guarded_counters"].values())
    assert "MISSING_REQUIRED_APPROVAL_FIELDS" in output["denial_reasons"]
    assert validate_l6ah01_runtime_integration_output(output) == []


def test_exact_issue_bound_approval_accepts_fixture_only_report_safe_value() -> None:
    approval = build_l6ah01_exact_approval_fixture()
    adapter_value = build_l6ah01_report_safe_adapter_value_fixture()

    output = integrate_l6ah01_report_safe_adapter_value(approval, adapter_value)

    assert output["status"] == L6AH_PASS_STATUS
    assert output["approval_result"] == (
        "EXACT_ISSUE_BOUND_OWNER_APPROVAL_MATCH_RUNTIME_INTEGRATION_FIXTURE_ONLY"
    )
    assert output["repository"] == L6AH_REPOSITORY
    assert output["issue_number"] == L6AH_ISSUE_NUMBER
    assert output["operation_class"] == L6AH_OPERATION_CLASS
    assert output["source_floor"] == L6AH_SOURCE_FLOOR
    assert output["adapter_value_ref"] == L6AH_ADAPTER_VALUE_REF
    assert output["approval_matched"] is True
    assert output["default_off_denied"] is False
    assert output["allowed"] == "EXACT_FIXTURE_ONLY_RUNTIME_INTEGRATION_SLICE"
    assert output["integration_slice_count"] == 1
    assert output["runtime_use_smoke_count"] == 0
    assert output["fixture_only"] is True
    assert output["report_safe"] is True
    assert output["metadata_only"] is True
    assert output["live_adapter_invoked"] is False
    assert output["callback_invoked"] is False
    assert output["registry_consumed"] is False
    assert output["persistence_attempted"] is False
    assert output["activation_attempted"] is False
    assert output["broad_allowed_attempted"] is False
    assert all(value == 0 for value in output["guarded_counters"].values())
    assert set(output["residual_holds"]) == set(L6AH_HELD_SURFACES)
    assert validate_l6ah01_runtime_integration_output(output) == []


def test_copied_stale_or_mismatched_approval_denies_before_slice_count() -> None:
    approval = build_l6ah01_exact_approval_fixture()
    approval.update(
        {
            "issue_number": 303,
            "source_floor": "1ff55c0056248162b7726f966f7a5a31e9a8241f",
            "operation_class": "L6AG_DESIGN_ONLY_NOT_IMPLEMENTATION",
        }
    )

    reasons = approval_denial_reasons_l6ah01(approval)
    output = integrate_l6ah01_report_safe_adapter_value(approval)

    assert "ISSUE_MISMATCH_OR_COPIED_APPROVAL" in reasons
    assert "SOURCE_FLOOR_MISMATCH" in reasons
    assert "OPERATION_CLASS_MISMATCH" in reasons
    assert output["status"] == L6AH_DENIED_STATUS
    assert output["integration_slice_count"] == 0
    assert output["runtime_use_smoke_count"] == 0
    assert output["live_adapter_invoked"] is False
    assert validate_l6ah01_runtime_integration_output(output) == []


def test_broadened_files_extra_smoke_non_owner_and_held_surfaces_deny() -> None:
    approval = build_l6ah01_exact_approval_fixture()
    approval["approved_file_envelope"] = list(L6AH_ALLOWED_FILE_ENVELOPE) + [
        "src/memory_seam/runtime.py"
    ]
    approval["actor_association"] = "MEMBER"
    approval["max_integration_slices"] = 2
    approval["max_runtime_use_smokes"] = 1
    approval["runtime_registry_authorized"] = True
    approval["callbacks_or_provider_routes_authorized"] = True
    approval["runtime_persistence_or_mutation_authorized"] = True
    approval["service_global_activation_authorized"] = True
    approval["broad_allowed_true_authorized"] = True

    output = integrate_l6ah01_report_safe_adapter_value(approval)

    assert output["status"] == L6AH_DENIED_STATUS
    assert set(output["denial_reasons"]) >= {
        "FILE_ENVELOPE_MISMATCH_OR_BROADENED",
        "NON_OWNER_APPROVAL",
        "MAX_INTEGRATION_SLICES_NOT_EXACTLY_ONE",
        "RUNTIME_USE_SMOKE_NOT_AUTHORIZED",
        "HELD_SURFACE_AUTHORIZATION_REQUESTED",
    }
    assert output["allowed"] is False
    assert output["integration_slice_count"] == 0
    assert output["runtime_use_smoke_count"] == 0
    assert output["registry_consumed"] is False
    assert output["callback_invoked"] is False
    assert output["persistence_attempted"] is False
    assert output["activation_attempted"] is False
    assert output["broad_allowed_attempted"] is False
    assert validate_l6ah01_runtime_integration_output(output) == []


def test_unsafe_or_non_fixture_adapter_value_rejected_without_held_surface_use() -> None:
    approval = build_l6ah01_exact_approval_fixture()
    adapter_value = build_l6ah01_report_safe_adapter_value_fixture()
    adapter_value.update(
        {
            "fixture_only": False,
            "raw_payload": "fixture attempts unsafe echo",
            "live_read_invoked": True,
        }
    )

    reasons = adapter_value_denial_reasons_l6ah01(adapter_value)
    output = integrate_l6ah01_report_safe_adapter_value(approval, adapter_value)

    assert "UNEXPECTED_ADAPTER_VALUE_FIELD" in reasons
    assert "UNSAFE_ADAPTER_VALUE_KEY" in reasons
    assert "ADAPTER_VALUE_FIXTURE_ONLY_NOT_TRUE" in reasons
    assert "ADAPTER_VALUE_LIVE_READ_INVOKED" in reasons
    assert output["status"] == L6AH_DENIED_STATUS
    assert output["integration_slice_count"] == 0
    assert output["live_adapter_invoked"] is False
    assert output["callback_invoked"] is False
    assert output["registry_consumed"] is False
    assert output["persistence_attempted"] is False
    assert output["activation_attempted"] is False
    assert validate_l6ah01_runtime_integration_output(output) == []


def test_all_guarded_counter_families_remain_zero_and_report_safe() -> None:
    output = integrate_l6ah01_report_safe_adapter_value(
        build_l6ah01_exact_approval_fixture(),
        build_l6ah01_report_safe_adapter_value_fixture(),
    )

    assert set(output["guarded_counters"]) == set(L6AH_GUARDED_COUNTERS)
    assert output["guarded_counters"]["provider_route_invocations"] == 0
    assert output["guarded_counters"]["runtime_registry_reads"] == 0
    assert output["guarded_counters"]["persistence_writes"] == 0
    assert output["guarded_counters"]["service_listener_startup_activations"] == 0
    assert output["guarded_counters"]["cron_changes"] == 0
    assert output["guarded_counters"]["provider_prod_canary_or_gate_moves"] == 0
    assert output["guarded_counters"]["atlas_gate_moves"] == 0
    assert output["allowed"] is not True
    assert validate_l6ah01_runtime_integration_output(output) == []


def test_approval_match_helper_is_exact_only() -> None:
    approval = build_l6ah01_exact_approval_fixture()

    assert approval_matches_l6ah01(approval) is True

    approval["repository"] = "example/other"
    assert approval_matches_l6ah01(approval) is False
