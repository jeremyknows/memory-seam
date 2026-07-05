from __future__ import annotations

from collections.abc import Mapping
from typing import Any

L6AH_RUNTIME_INTEGRATION_SCHEMA_VERSION = "l6ah01-default-off-runtime-integration-v1"
L6AH_OPERATION_CLASS = "L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE"
L6AH_REPOSITORY = "jeremyknows/memory-seam"
L6AH_ISSUE_NUMBER = 311
L6AH_PARENT_ISSUE = 6
L6AH_APPROVAL_COMMENT_ID = "4654131093"
L6AH_PARENT_SUCCESSOR_COMMENT_ID = "4654131206"
L6AH_SOURCE_FLOOR = "df8e034cd0d53c675212b6f7aa594abd4bd272d3"
L6AH_OWNER_ASSOCIATION = "OWNER"
L6AH_MAX_INTEGRATION_SLICES = 1
L6AH_MAX_RUNTIME_USE_SMOKES = 0
L6AH_PASS_STATUS = "PASS_DEFAULT_OFF_RUNTIME_INTEGRATION_FIXTURE_ONLY"
L6AH_DENIED_STATUS = "DENIED_DEFAULT_OFF"
L6AH_HOLD_STATUS = "HOLD_FOR_OWNER_DECISION"
L6AH_DESCRIPTOR_REF = "descriptor:l6ah/default-off-runtime-integration-fixture"
L6AH_ADAPTER_VALUE_REF = "adapter-value:l6ah/report-safe-source-card-value-fixture"

L6AH_ALLOWED_FILE_ENVELOPE = (
    "src/memory_seam/l6ag_default_off_runtime_integration.py",
    "tests/test_l6ag_default_off_runtime_integration.py",
    "docs/l6ah01-default-off-runtime-integration-receipt.md",
    "docs/README.md",
    "docs/contract-test-inventory.md",
)

L6AH_HELD_SURFACES = (
    "service_global_activation",
    "live_private_reads",
    "source_card_reads",
    "raw_private_content_source_text_approval_prose",
    "credentials_auth_env_keychain_oauth_auth_file_reads",
    "discovery_workspace_family_scans_broad_recall_index_query",
    "runtime_registry_consumption",
    "callbacks_provider_routes",
    "runtime_persistence_mutation_write_delete_reindex_cache_purge_rollback_execution",
    "cron_changes",
    "publication_visibility_provider_prod_canary_gate_movement",
    "atlas_gate_movement",
    "broad_allowed_true_behavior",
)

L6AH_GUARDED_COUNTERS = (
    "live_read_invocations",
    "source_card_reads",
    "raw_private_content_reads",
    "raw_source_text_reads",
    "raw_approval_prose_reads",
    "credential_reads",
    "auth_env_keychain_oauth_auth_file_reads",
    "source_discovery_queries",
    "workspace_scans",
    "family_scans",
    "broad_recall_queries",
    "index_queries",
    "runtime_registry_reads",
    "provider_route_invocations",
    "provider_callbacks",
    "backend_callbacks",
    "source_stat_callbacks",
    "source_read_callbacks",
    "persistence_writes",
    "mutation_callbacks",
    "write_callbacks",
    "delete_callbacks",
    "reindex_callbacks",
    "cache_purge_callbacks",
    "rollback_callbacks",
    "service_listener_startup_activations",
    "cron_changes",
    "publication_or_visibility_changes",
    "provider_prod_canary_or_gate_moves",
    "atlas_gate_moves",
    "allowed_true_results",
)

L6AH_REQUIRED_APPROVAL_FIELDS = frozenset(
    {
        "repository",
        "issue_number",
        "actor_association",
        "operation_class",
        "source_floor",
        "approval_comment_id",
        "parent_successor_comment_id",
        "approved_file_envelope",
        "max_integration_slices",
        "max_runtime_use_smokes",
        "service_global_activation_authorized",
        "live_private_reads_authorized",
        "source_card_reads_authorized",
        "raw_private_or_source_or_approval_prose_authorized",
        "credentials_or_auth_reads_authorized",
        "discovery_or_scan_authorized",
        "runtime_registry_authorized",
        "callbacks_or_provider_routes_authorized",
        "runtime_persistence_or_mutation_authorized",
        "cron_changes_authorized",
        "publication_or_visibility_authorized",
        "provider_prod_canary_or_gate_movement_authorized",
        "atlas_gate_movement_authorized",
        "broad_allowed_true_authorized",
    }
)

L6AH_ADAPTER_VALUE_SAFE_FIELDS = frozenset(
    {
        "descriptor_ref",
        "adapter_value_ref",
        "source_card_ref",
        "usefulness_label",
        "adapter_status",
        "fixture_only",
        "default_off",
        "report_safe",
        "metadata_only",
        "live_read_invoked",
        "guarded_counters",
    }
)

L6AH_REPORT_SAFE_OUTPUT_FIELDS = frozenset(
    {
        "schema_version",
        "status",
        "approval_result",
        "denial_reasons",
        "repository",
        "issue_number",
        "parent_issue",
        "operation_class",
        "source_floor",
        "approval_comment_id",
        "parent_successor_comment_id",
        "descriptor_ref",
        "adapter_value_ref",
        "source_card_ref",
        "usefulness_label",
        "runtime_integration_scope",
        "fixture_only",
        "default_off",
        "report_safe",
        "metadata_only",
        "approval_matched",
        "default_off_denied",
        "allowed",
        "integration_slice_count",
        "runtime_use_smoke_count",
        "max_integration_slices",
        "max_runtime_use_smokes",
        "live_adapter_invoked",
        "callback_invoked",
        "registry_consumed",
        "persistence_attempted",
        "activation_attempted",
        "broad_allowed_attempted",
        "guarded_counters",
        "residual_holds",
    }
)

L6AH_UNSAFE_KEY_MARKERS = (
    "raw",
    "secret",
    "token",
    "credential",
    "password",
    "auth",
    "oauth",
    "keychain",
    "env_value",
    "absolute_path",
    "source_uri",
    "platform_id",
    "prompt",
    "query",
    "payload",
    "backend_response",
    "correlation",
    "source_text",
    "approval_text",
)

L6AH_UNSAFE_ECHO_MARKERS = (
    "private absolute path",
    "source://",
    "platform-raw-id",
    "raw prompt",
    "raw query",
    "query payload",
    "raw payload",
    "backend response",
    "credential value",
    "auth material",
    "oauth token",
    "keychain material",
    "auth-file material",
    "private-correlation-ref",
)


def _zero_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6AH_GUARDED_COUNTERS}


def _contains_unsafe_key(key: str) -> bool:
    lowered = key.lower().replace("-", "_")
    return any(marker in lowered for marker in L6AH_UNSAFE_KEY_MARKERS)


def _contains_unsafe_echo(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in L6AH_UNSAFE_ECHO_MARKERS)
    if isinstance(value, Mapping):
        return any(_contains_unsafe_echo(item) for item in value.values())
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_unsafe_echo(item) for item in value)
    return False


def build_l6ah01_exact_approval_fixture() -> dict[str, Any]:
    """Return report-safe approval metadata for the exact issue-bound #311 slice."""

    return {
        "repository": L6AH_REPOSITORY,
        "issue_number": L6AH_ISSUE_NUMBER,
        "actor_association": L6AH_OWNER_ASSOCIATION,
        "operation_class": L6AH_OPERATION_CLASS,
        "source_floor": L6AH_SOURCE_FLOOR,
        "approval_comment_id": L6AH_APPROVAL_COMMENT_ID,
        "parent_successor_comment_id": L6AH_PARENT_SUCCESSOR_COMMENT_ID,
        "approved_file_envelope": list(L6AH_ALLOWED_FILE_ENVELOPE),
        "max_integration_slices": L6AH_MAX_INTEGRATION_SLICES,
        "max_runtime_use_smokes": L6AH_MAX_RUNTIME_USE_SMOKES,
        "service_global_activation_authorized": False,
        "live_private_reads_authorized": False,
        "source_card_reads_authorized": False,
        "raw_private_or_source_or_approval_prose_authorized": False,
        "credentials_or_auth_reads_authorized": False,
        "discovery_or_scan_authorized": False,
        "runtime_registry_authorized": False,
        "callbacks_or_provider_routes_authorized": False,
        "runtime_persistence_or_mutation_authorized": False,
        "cron_changes_authorized": False,
        "publication_or_visibility_authorized": False,
        "provider_prod_canary_or_gate_movement_authorized": False,
        "atlas_gate_movement_authorized": False,
        "broad_allowed_true_authorized": False,
    }


def build_l6ah01_report_safe_adapter_value_fixture() -> dict[str, Any]:
    """Return committed report-safe adapter-value metadata; no adapter is invoked."""

    return {
        "descriptor_ref": L6AH_DESCRIPTOR_REF,
        "adapter_value_ref": L6AH_ADAPTER_VALUE_REF,
        "source_card_ref": "source-card:l6ah/report-safe-source-card-value-fixture",
        "usefulness_label": "USEFUL_REPORT_SAFE_ADAPTER_VALUE_READY_FOR_DEFAULT_OFF_INTEGRATION",
        "adapter_status": "COMMITTED_FIXTURE_ONLY_REPORT_SAFE_ADAPTER_VALUE",
        "fixture_only": True,
        "default_off": True,
        "report_safe": True,
        "metadata_only": True,
        "live_read_invoked": False,
        "guarded_counters": _zero_counters(),
    }


def approval_denial_reasons_l6ah01(approval: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    missing = sorted(L6AH_REQUIRED_APPROVAL_FIELDS - set(approval))
    if missing:
        reasons.append("MISSING_REQUIRED_APPROVAL_FIELDS")
    if approval.get("repository") != L6AH_REPOSITORY:
        reasons.append("REPOSITORY_MISMATCH")
    if approval.get("issue_number") != L6AH_ISSUE_NUMBER:
        reasons.append("ISSUE_MISMATCH_OR_COPIED_APPROVAL")
    if approval.get("actor_association") != L6AH_OWNER_ASSOCIATION:
        reasons.append("NON_OWNER_APPROVAL")
    if approval.get("operation_class") != L6AH_OPERATION_CLASS:
        reasons.append("OPERATION_CLASS_MISMATCH")
    if approval.get("source_floor") != L6AH_SOURCE_FLOOR:
        reasons.append("SOURCE_FLOOR_MISMATCH")
    if approval.get("approval_comment_id") != L6AH_APPROVAL_COMMENT_ID:
        reasons.append("APPROVAL_COMMENT_MISMATCH")
    if approval.get("parent_successor_comment_id") != L6AH_PARENT_SUCCESSOR_COMMENT_ID:
        reasons.append("PARENT_SUCCESSOR_COMMENT_MISMATCH")
    if tuple(approval.get("approved_file_envelope", ())) != L6AH_ALLOWED_FILE_ENVELOPE:
        reasons.append("FILE_ENVELOPE_MISMATCH_OR_BROADENED")
    if approval.get("max_integration_slices") != L6AH_MAX_INTEGRATION_SLICES:
        reasons.append("MAX_INTEGRATION_SLICES_NOT_EXACTLY_ONE")
    if approval.get("max_runtime_use_smokes") != L6AH_MAX_RUNTIME_USE_SMOKES:
        reasons.append("RUNTIME_USE_SMOKE_NOT_AUTHORIZED")
    forbidden_true_fields = (
        "service_global_activation_authorized",
        "live_private_reads_authorized",
        "source_card_reads_authorized",
        "raw_private_or_source_or_approval_prose_authorized",
        "credentials_or_auth_reads_authorized",
        "discovery_or_scan_authorized",
        "runtime_registry_authorized",
        "callbacks_or_provider_routes_authorized",
        "runtime_persistence_or_mutation_authorized",
        "cron_changes_authorized",
        "publication_or_visibility_authorized",
        "provider_prod_canary_or_gate_movement_authorized",
        "atlas_gate_movement_authorized",
        "broad_allowed_true_authorized",
    )
    if any(approval.get(field) is not False for field in forbidden_true_fields):
        reasons.append("HELD_SURFACE_AUTHORIZATION_REQUESTED")
    return reasons


def approval_matches_l6ah01(approval: Mapping[str, Any]) -> bool:
    return not approval_denial_reasons_l6ah01(approval)


def adapter_value_denial_reasons_l6ah01(adapter_value: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    if set(adapter_value) - L6AH_ADAPTER_VALUE_SAFE_FIELDS:
        reasons.append("UNEXPECTED_ADAPTER_VALUE_FIELD")
    if any(_contains_unsafe_key(str(key)) for key in adapter_value):
        reasons.append("UNSAFE_ADAPTER_VALUE_KEY")
    if _contains_unsafe_echo(adapter_value):
        reasons.append("UNSAFE_ADAPTER_VALUE_ECHO")
    for field in ("fixture_only", "default_off", "report_safe", "metadata_only"):
        if adapter_value.get(field) is not True:
            reasons.append(f"ADAPTER_VALUE_{field.upper()}_NOT_TRUE")
    if adapter_value.get("live_read_invoked") is not False:
        reasons.append("ADAPTER_VALUE_LIVE_READ_INVOKED")
    counters = adapter_value.get("guarded_counters")
    if not isinstance(counters, Mapping):
        reasons.append("ADAPTER_VALUE_MISSING_GUARDED_COUNTERS")
    elif any(counters.get(counter) != 0 for counter in L6AH_GUARDED_COUNTERS):
        reasons.append("ADAPTER_VALUE_GUARDED_COUNTER_NONZERO")
    return reasons


def integrate_l6ah01_report_safe_adapter_value(
    approval: Mapping[str, Any] | None,
    adapter_value: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Integrate a committed report-safe adapter-value fixture under exact approval.

    The seam is default-off and accepts metadata mappings only. It does not call
    an adapter, provider route, callback, Runtime Registry, persistence layer,
    service startup hook, credential/config/env source, or live/private reader.
    """

    approval_mapping: Mapping[str, Any] = approval or {}
    adapter_value_mapping: Mapping[str, Any] = (
        adapter_value or build_l6ah01_report_safe_adapter_value_fixture()
    )
    reasons = approval_denial_reasons_l6ah01(approval_mapping)
    reasons.extend(adapter_value_denial_reasons_l6ah01(adapter_value_mapping))
    passed = not reasons

    descriptor_ref = str(adapter_value_mapping.get("descriptor_ref", L6AH_DESCRIPTOR_REF))
    adapter_value_ref = str(adapter_value_mapping.get("adapter_value_ref", L6AH_ADAPTER_VALUE_REF))
    source_card_ref = str(
        adapter_value_mapping.get(
            "source_card_ref", "source-card:l6ah/report-safe-source-card-value-fixture"
        )
    )
    usefulness_label = str(
        adapter_value_mapping.get(
            "usefulness_label", "NOT_APPLICABLE_DENIED_DEFAULT_OFF"
        )
    )
    if not passed:
        descriptor_ref = L6AH_DESCRIPTOR_REF
        adapter_value_ref = L6AH_ADAPTER_VALUE_REF
        source_card_ref = "source-card:l6ah/report-safe-source-card-value-fixture"
        usefulness_label = "NOT_APPLICABLE_DENIED_DEFAULT_OFF"

    return {
        "schema_version": L6AH_RUNTIME_INTEGRATION_SCHEMA_VERSION,
        "status": L6AH_PASS_STATUS if passed else L6AH_DENIED_STATUS,
        "approval_result": (
            "EXACT_ISSUE_BOUND_OWNER_APPROVAL_MATCH_RUNTIME_INTEGRATION_FIXTURE_ONLY"
            if passed
            else "DENY_BEFORE_RUNTIME_INTEGRATION"
        ),
        "denial_reasons": [] if passed else sorted(set(reasons)),
        "repository": L6AH_REPOSITORY,
        "issue_number": L6AH_ISSUE_NUMBER,
        "parent_issue": L6AH_PARENT_ISSUE,
        "operation_class": L6AH_OPERATION_CLASS,
        "source_floor": L6AH_SOURCE_FLOOR,
        "approval_comment_id": L6AH_APPROVAL_COMMENT_ID,
        "parent_successor_comment_id": L6AH_PARENT_SUCCESSOR_COMMENT_ID,
        "descriptor_ref": descriptor_ref,
        "adapter_value_ref": adapter_value_ref,
        "source_card_ref": source_card_ref,
        "usefulness_label": usefulness_label,
        "runtime_integration_scope": "FIXTURE_ONLY_REPORT_SAFE_METADATA_NO_SERVICE_OR_PROVIDER_WIRING",
        "fixture_only": True,
        "default_off": True,
        "report_safe": True,
        "metadata_only": True,
        "approval_matched": passed,
        "default_off_denied": not passed,
        "allowed": "EXACT_FIXTURE_ONLY_RUNTIME_INTEGRATION_SLICE" if passed else False,
        "integration_slice_count": 1 if passed else 0,
        "runtime_use_smoke_count": 0,
        "max_integration_slices": L6AH_MAX_INTEGRATION_SLICES,
        "max_runtime_use_smokes": L6AH_MAX_RUNTIME_USE_SMOKES,
        "live_adapter_invoked": False,
        "callback_invoked": False,
        "registry_consumed": False,
        "persistence_attempted": False,
        "activation_attempted": False,
        "broad_allowed_attempted": False,
        "guarded_counters": _zero_counters(),
        "residual_holds": list(L6AH_HELD_SURFACES),
    }


def validate_l6ah01_runtime_integration_output(output: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(output) - L6AH_REPORT_SAFE_OUTPUT_FIELDS:
        errors.append("unexpected_output_field")
    if any(_contains_unsafe_key(str(key)) for key in (set(output) - L6AH_REPORT_SAFE_OUTPUT_FIELDS)):
        errors.append("unsafe_output_key")
    if _contains_unsafe_echo(output):
        errors.append("unsafe_output_echo")
    if output.get("schema_version") != L6AH_RUNTIME_INTEGRATION_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if output.get("repository") != L6AH_REPOSITORY or output.get("issue_number") != L6AH_ISSUE_NUMBER:
        errors.append("unexpected_issue_binding")
    if output.get("operation_class") != L6AH_OPERATION_CLASS:
        errors.append("unexpected_operation_class")
    for field in ("fixture_only", "default_off", "report_safe", "metadata_only"):
        if output.get(field) is not True:
            errors.append(f"{field}_not_true")
    for field in (
        "live_adapter_invoked",
        "callback_invoked",
        "registry_consumed",
        "persistence_attempted",
        "activation_attempted",
        "broad_allowed_attempted",
    ):
        if output.get(field) is not False:
            errors.append(f"{field}_not_false")
    counters = output.get("guarded_counters")
    if not isinstance(counters, Mapping):
        errors.append("missing_guarded_counters")
    elif any(counters.get(counter) != 0 for counter in L6AH_GUARDED_COUNTERS):
        errors.append("guarded_counter_nonzero")
    if output.get("runtime_use_smoke_count") != 0:
        errors.append("runtime_use_smoke_count_nonzero")
    if output.get("allowed") is True:
        errors.append("broad_allowed_true")
    if output.get("status") == L6AH_PASS_STATUS:
        if output.get("approval_matched") is not True:
            errors.append("pass_approval_not_matched")
        if output.get("default_off_denied") is not False:
            errors.append("pass_default_off_denied")
        if output.get("allowed") != "EXACT_FIXTURE_ONLY_RUNTIME_INTEGRATION_SLICE":
            errors.append("pass_allowed_label_missing")
        if output.get("integration_slice_count") != 1:
            errors.append("pass_integration_slice_count_not_one")
    elif output.get("status") == L6AH_DENIED_STATUS:
        if output.get("approval_matched") is not False:
            errors.append("denied_approval_matched")
        if output.get("default_off_denied") is not True:
            errors.append("denied_default_off_not_true")
        if output.get("allowed") is not False:
            errors.append("denied_allowed_not_false")
        if output.get("integration_slice_count") != 0:
            errors.append("denied_integration_slice_count_nonzero")
        if not output.get("denial_reasons"):
            errors.append("denied_reasons_missing")
    else:
        errors.append("unexpected_status")
    return errors


__all__ = [
    "L6AH_ADAPTER_VALUE_REF",
    "L6AH_ALLOWED_FILE_ENVELOPE",
    "L6AH_APPROVAL_COMMENT_ID",
    "L6AH_DENIED_STATUS",
    "L6AH_GUARDED_COUNTERS",
    "L6AH_HELD_SURFACES",
    "L6AH_ISSUE_NUMBER",
    "L6AH_OPERATION_CLASS",
    "L6AH_PASS_STATUS",
    "L6AH_REPOSITORY",
    "L6AH_RUNTIME_INTEGRATION_SCHEMA_VERSION",
    "L6AH_SOURCE_FLOOR",
    "adapter_value_denial_reasons_l6ah01",
    "approval_denial_reasons_l6ah01",
    "approval_matches_l6ah01",
    "build_l6ah01_exact_approval_fixture",
    "build_l6ah01_report_safe_adapter_value_fixture",
    "integrate_l6ah01_report_safe_adapter_value",
    "validate_l6ah01_runtime_integration_output",
]
