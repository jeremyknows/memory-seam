"""Metadata-only rollback/audit fixtures for future L6 write/custody slices.

This module defines public-safe schema fixtures only. It does not implement,
authorize, simulate, activate, schedule, or execute writes, custody transfer,
delete, reindex, rollback, cache purge, provider/backend calls, source
discovery, live/private reads, recurring runners, services, listeners,
cron/startup activation, Runtime Registry consumption, global configuration
mutation, publication, visibility changes, Atlas Gate movement, or production
authoritative behavior.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

L6_WRITE_CUSTODY_ROLLBACK_AUDIT_STATUS = "schema_fixture_implementation_held"
L6_WRITE_CUSTODY_ROLLBACK_AUDIT_SCHEMA_VERSION = "l6-write-custody-rollback-audit-v1"
L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FIELDS = (
    "schema_version",
    "status",
    "plan_ref",
    "approval_model_ref",
    "future_slice_scope",
    "operation_classes",
    "rollback_plan",
    "audit_event_fields",
    "stop_conditions",
    "timeout",
    "failure_modes",
    "runtime_mutation",
    "side_effects",
    "held_surfaces",
    "report_safety",
)
L6_WRITE_CUSTODY_ROLLBACK_AUDIT_OPERATION_CLASSES = (
    "write_intent",
    "custody_receipt_persistence",
    "delete_intent",
    "reindex_intent",
    "rollback_intent",
    "cache_purge_intent",
)
L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_AUDIT_FIELDS = (
    "schema_version",
    "event_ref",
    "approval_ref",
    "operation_class",
    "actor_binding_ref",
    "custody_owner_role",
    "approver_role",
    "pre_mutation_guard_result",
    "mutation_supported",
    "mutation_attempted",
    "rollback_required",
    "rollback_plan_ref",
    "stop_condition_ref",
    "timeout_ref",
    "failure_mode_ref",
    "side_effect_counters",
    "report_safe_reference",
)
L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_STOP_CONDITIONS = (
    "approval_missing_or_mismatched",
    "actor_binding_mismatch",
    "approval_expired",
    "max_operation_count_exhausted",
    "pre_mutation_guard_denied",
    "unsupported_runtime_mutation_surface",
    "audit_field_missing",
    "rollback_plan_missing",
    "timeout_elapsed",
    "report_safety_violation",
)
L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FAILURE_MODES = (
    "deny_before_mutation",
    "emit_report_safe_audit_receipt_only",
    "require_human_triage_for_any_future_mutation_attempt",
    "do_not_retry_automatically",
    "do_not_execute_rollback_without_separate_approval",
)
L6_WRITE_CUSTODY_ROLLBACK_AUDIT_HELD_SURFACES = (
    "write_execution",
    "custody_transfer",
    "delete_execution",
    "reindex_execution",
    "rollback_execution",
    "cache_purge_execution",
    "provider_backend_calls",
    "source_discovery",
    "live_private_source_reads",
    "unsupervised_reads",
    "recurring_runner_or_activation",
    "runtime_registry_consumption",
    "global_config_mutation",
    "credential_auth_env_keychain_oauth_authfile_reads",
    "provider_prod_canary_authority",
    "publication_or_visibility_change",
    "atlas_gate_movement",
)
_SAFE_SIDE_EFFECTS = {
    "write_callbacks": 0,
    "custody_callbacks": 0,
    "delete_callbacks": 0,
    "reindex_callbacks": 0,
    "rollback_callbacks": 0,
    "cache_purge_callbacks": 0,
    "provider_calls": 0,
    "backend_calls": 0,
    "source_discovery_calls": 0,
    "source_stat_calls": 0,
    "source_read_calls": 0,
    "runtime_registry_reads": 0,
    "activation_callbacks": 0,
    "audit_persistence_callbacks": 0,
}
_REPORT_SAFETY = {
    "raw_private_text": False,
    "credentials_or_auth_material": False,
    "private_paths": False,
    "raw_platform_ids": False,
    "raw_query_payloads": False,
    "raw_payload_content": False,
    "private_correlation_refs": False,
}


def _rollback_plan() -> dict[str, Any]:
    return {
        "plan_ref": "rollback-plan-public-safe-fixture",
        "scope": "one_future_exactly_approved_bounded_slice",
        "preconditions": (
            "approval_model_fields_validated",
            "pre_mutation_guard_passed_in_future_slice",
            "report_safe_audit_fields_ready",
            "separate_future_rollback_approval_required_before_execution",
        ),
        "steps": (
            "capture_pre_mutation_report_safe_audit_receipt",
            "deny_current_schema_fixture_before_mutation",
            "if_future_mutation_is_approved_then_record_reversible_operation_ref_only",
            "stop_and_require_human_triage_on_any_uncertain_or_unsafe_state",
        ),
        "postconditions": (
            "no_current_runtime_mutation_supported",
            "rollback_execution_remains_held",
            "public_artifacts_remain_report_safe",
        ),
    }


def _fixture() -> dict[str, Any]:
    return {
        "schema_version": L6_WRITE_CUSTODY_ROLLBACK_AUDIT_SCHEMA_VERSION,
        "status": L6_WRITE_CUSTODY_ROLLBACK_AUDIT_STATUS,
        "plan_ref": "l6s-02-rollback-audit-plan-public-safe-fixture",
        "approval_model_ref": "l6-write-custody-approval-model-v1-required",
        "future_slice_scope": "one_future_exactly_approved_bounded_implementation_issue",
        "operation_classes": L6_WRITE_CUSTODY_ROLLBACK_AUDIT_OPERATION_CLASSES,
        "rollback_plan": _rollback_plan(),
        "audit_event_fields": L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_AUDIT_FIELDS,
        "stop_conditions": L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_STOP_CONDITIONS,
        "timeout": {
            "max_duration_ref": "future_slice_timeout_required_before_execution",
            "on_timeout": "stop_before_mutation_or_stop_after_bounded_future_operation_and_require_human_triage",
            "recurring_retry": False,
            "activation_allowed": False,
        },
        "failure_modes": L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FAILURE_MODES,
        "runtime_mutation": {
            "supported": False,
            "attempted": False,
            "approval_from_this_fixture": False,
            "rollback_execution_supported": False,
        },
        "side_effects": deepcopy(_SAFE_SIDE_EFFECTS),
        "held_surfaces": L6_WRITE_CUSTODY_ROLLBACK_AUDIT_HELD_SURFACES,
        "report_safety": deepcopy(_REPORT_SAFETY),
    }


L6_WRITE_CUSTODY_ROLLBACK_AUDIT_FIXTURE: dict[str, Any] = _fixture()


def build_l6_write_custody_rollback_audit_fixture() -> dict[str, Any]:
    """Return a deep-copied rollback/audit plan fixture without mutation authority."""

    return deepcopy(L6_WRITE_CUSTODY_ROLLBACK_AUDIT_FIXTURE)


def validate_l6_write_custody_rollback_audit_fixture(fixture: dict[str, Any]) -> list[str]:
    """Return report-safe validation errors for an L6 rollback/audit fixture."""

    errors: list[str] = []
    for field in L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FIELDS:
        if field not in fixture:
            errors.append(f"missing_{field}")
    if fixture.get("schema_version") != L6_WRITE_CUSTODY_ROLLBACK_AUDIT_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if fixture.get("status") != L6_WRITE_CUSTODY_ROLLBACK_AUDIT_STATUS:
        errors.append("unexpected_status")
    if tuple(fixture.get("operation_classes", ())) != L6_WRITE_CUSTODY_ROLLBACK_AUDIT_OPERATION_CLASSES:
        errors.append("unexpected_operation_classes")
    rollback_plan = fixture.get("rollback_plan")
    if not isinstance(rollback_plan, dict) or not rollback_plan.get("plan_ref"):
        errors.append("missing_rollback_plan")
    audit_fields = tuple(fixture.get("audit_event_fields", ()))
    for field in L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_AUDIT_FIELDS:
        if field not in audit_fields:
            errors.append(f"missing_audit_field_{field}")
    stop_conditions = tuple(fixture.get("stop_conditions", ()))
    for stop_condition in L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_STOP_CONDITIONS:
        if stop_condition not in stop_conditions:
            errors.append(f"missing_stop_condition_{stop_condition}")
    failure_modes = tuple(fixture.get("failure_modes", ()))
    for failure_mode in L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FAILURE_MODES:
        if failure_mode not in failure_modes:
            errors.append(f"missing_failure_mode_{failure_mode}")
    timeout = fixture.get("timeout")
    if not isinstance(timeout, dict) or timeout.get("activation_allowed") is not False:
        errors.append("invalid_timeout_plan")
    runtime_mutation = fixture.get("runtime_mutation")
    if not isinstance(runtime_mutation, dict):
        errors.append("missing_runtime_mutation_plan")
    elif any(runtime_mutation.get(key) for key in ("supported", "attempted", "approval_from_this_fixture", "rollback_execution_supported")):
        errors.append("runtime_mutation_not_held")
    side_effects = fixture.get("side_effects")
    if not isinstance(side_effects, dict):
        errors.append("missing_side_effect_counters")
    elif side_effects != _SAFE_SIDE_EFFECTS:
        errors.append("nonzero_side_effect_counter")
    report_safety = fixture.get("report_safety")
    if not isinstance(report_safety, dict):
        errors.append("missing_report_safety_flags")
    elif report_safety != _REPORT_SAFETY:
        errors.append("unsafe_report_safety_flag")
    held_surfaces = tuple(fixture.get("held_surfaces", ()))
    for surface in L6_WRITE_CUSTODY_ROLLBACK_AUDIT_HELD_SURFACES:
        if surface not in held_surfaces:
            errors.append(f"missing_held_surface_{surface}")
    return errors
