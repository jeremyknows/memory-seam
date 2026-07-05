from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

L6AE_ADAPTER_SCHEMA_VERSION = "l6ae01-report-safe-source-card-value-adapter-v1"
L6AE_OPERATION_CLASS = "L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON"
L6AE_REPOSITORY = "jeremyknows/memory-seam"
L6AE_ISSUE_NUMBER = 281
L6AE_PARENT_ISSUE = 6
L6AE_APPROVAL_COMMENT_ID = "4652448584"
L6AE_SOURCE_FLOOR = "972cc3026cd1a2629679778143de0eafe7b3b921"
L6AE_APPROVAL_EXPIRES_AT = "2026-06-09T07:01:56Z"
L6AE_OWNER_ASSOCIATION = "OWNER"
L6AE_MAX_SLICES = 1
L6AE_PASS_STATUS = "PASS_REPORT_SAFE_VALUE_ADAPTER_FIXTURE_ONLY"
L6AE_DENIED_STATUS = "DENIED_DEFAULT_OFF"
L6AE_HOLD_STATUS = "HOLD_FOR_OWNER_DECISION"
L6AE_DESCRIPTOR_REF = "descriptor:l6ae/report-safe-source-card-value-adapter-fixture"
L6AE_SOURCE_CARD_REF = "source-card:l6ae/report-safe-source-card-value-adapter-fixture"

L6AE_ALLOWED_FILE_ENVELOPE = (
    "src/memory_seam/l6ad_report_safe_source_card_value_adapter.py",
    "src/memory_seam/__init__.py",
    "tests/test_l6ad_report_safe_source_card_value_adapter.py",
    "docs/l6ae-default-off-adapter-implementation-receipt.md",
    "docs/README.md",
    "docs/contract-test-inventory.md",
)

L6AE_HELD_SURFACES = (
    "live_private_reads",
    "raw_private_content",
    "raw_source_text",
    "raw_approval_prose",
    "additional_source_card_reads",
    "credentials_auth_env_keychain_oauth_auth_file_reads",
    "source_discovery_workspace_family_scans_broad_recall_index_query",
    "runtime_registry_consumption",
    "provider_backend_source_stat_source_read_callbacks",
    "persistence_mutation_write_delete_reindex_cache_purge_rollback_execution",
    "service_listener_startup_global_activation",
    "cron_changes",
    "publication_visibility_change",
    "provider_prod_canary_gate_movement",
    "atlas_gate_movement",
    "broad_allowed_true_behavior",
)

L6AE_GUARDED_COUNTERS = (
    "live_read_invocations",
    "additional_source_card_reads",
    "raw_private_content_reads",
    "raw_source_text_reads",
    "credential_reads",
    "auth_env_keychain_oauth_auth_file_reads",
    "source_discovery_queries",
    "workspace_scans",
    "family_scans",
    "broad_recall_queries",
    "index_queries",
    "runtime_registry_reads",
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

L6AE_REQUIRED_APPROVAL_FIELDS = frozenset(
    {
        "repository",
        "issue_number",
        "actor_association",
        "operation_class",
        "source_floor",
        "approval_comment_id",
        "approved_file_envelope",
        "expires_at",
        "max_slices",
        "live_private_reads_authorized",
        "raw_private_content_authorized",
        "additional_source_card_reads_authorized",
        "credentials_or_auth_reads_authorized",
        "source_discovery_authorized",
        "runtime_registry_authorized",
        "callbacks_authorized",
        "persistence_or_mutation_authorized",
        "activation_authorized",
        "cron_changes_authorized",
        "publication_or_visibility_authorized",
        "provider_prod_canary_or_gate_movement_authorized",
        "atlas_gate_movement_authorized",
        "broad_allowed_true_authorized",
    }
)

L6AE_REPORT_SAFE_OUTPUT_FIELDS = frozenset(
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
        "approval_expires_at",
        "evaluated_at",
        "descriptor_ref",
        "source_card_ref",
        "usefulness_label",
        "adapter_scope",
        "fixture_only",
        "default_off",
        "report_safe",
        "metadata_only",
        "allowed",
        "allowed_result_count",
        "live_read_invoked",
        "unsafe_raw_fields_rejected_before_report",
        "guarded_counters",
        "residual_holds",
    }
)

L6AE_FIXTURE_SAFE_FIELDS = frozenset(
    {
        "descriptor_ref",
        "source_card_ref",
        "usefulness_label",
        "status_label",
        "fixture_only",
        "default_off",
        "report_safe",
        "metadata_only",
        "guarded_counters",
    }
)

L6AE_UNSAFE_KEY_MARKERS = (
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

L6AE_UNSAFE_ECHO_MARKERS = (
    "raw private",
    "raw source",
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
    "raw approval",
)


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _zero_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6AE_GUARDED_COUNTERS}


def _contains_unsafe_key(key: str) -> bool:
    lowered = key.lower().replace("-", "_")
    return any(marker in lowered for marker in L6AE_UNSAFE_KEY_MARKERS)


def _contains_unsafe_echo(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in L6AE_UNSAFE_ECHO_MARKERS)
    if isinstance(value, Mapping):
        return any(_contains_unsafe_echo(item) for item in value.values())
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_unsafe_echo(item) for item in value)
    return False


def build_l6ae01_exact_approval_fixture() -> dict[str, Any]:
    """Return report-safe approval metadata for the exact issue-bound #281 slice.

    The fixture intentionally stores metadata only. It does not fetch GitHub,
    read environment/config/credential material, store raw approval prose, or
    authorize any live/private source-card read.
    """

    return {
        "repository": L6AE_REPOSITORY,
        "issue_number": L6AE_ISSUE_NUMBER,
        "actor_association": L6AE_OWNER_ASSOCIATION,
        "operation_class": L6AE_OPERATION_CLASS,
        "source_floor": L6AE_SOURCE_FLOOR,
        "approval_comment_id": L6AE_APPROVAL_COMMENT_ID,
        "approved_file_envelope": list(L6AE_ALLOWED_FILE_ENVELOPE),
        "expires_at": L6AE_APPROVAL_EXPIRES_AT,
        "max_slices": L6AE_MAX_SLICES,
        "live_private_reads_authorized": False,
        "raw_private_content_authorized": False,
        "additional_source_card_reads_authorized": False,
        "credentials_or_auth_reads_authorized": False,
        "source_discovery_authorized": False,
        "runtime_registry_authorized": False,
        "callbacks_authorized": False,
        "persistence_or_mutation_authorized": False,
        "activation_authorized": False,
        "cron_changes_authorized": False,
        "publication_or_visibility_authorized": False,
        "provider_prod_canary_or_gate_movement_authorized": False,
        "atlas_gate_movement_authorized": False,
        "broad_allowed_true_authorized": False,
    }


def build_l6ae01_report_safe_fixture() -> dict[str, Any]:
    return {
        "descriptor_ref": L6AE_DESCRIPTOR_REF,
        "source_card_ref": L6AE_SOURCE_CARD_REF,
        "usefulness_label": "USEFUL_REPORT_SAFE_VALUE_METADATA_ADAPTER_READY",
        "status_label": "COMMITTED_FIXTURE_ONLY_NO_LIVE_READ",
        "fixture_only": True,
        "default_off": True,
        "report_safe": True,
        "metadata_only": True,
        "guarded_counters": _zero_counters(),
    }


def approval_denial_reasons(approval: Mapping[str, Any], *, evaluated_at: str) -> list[str]:
    reasons: list[str] = []
    missing = sorted(L6AE_REQUIRED_APPROVAL_FIELDS - set(approval))
    if missing:
        reasons.append("MISSING_REQUIRED_APPROVAL_FIELDS")
    if approval.get("repository") != L6AE_REPOSITORY:
        reasons.append("REPOSITORY_MISMATCH")
    if approval.get("issue_number") != L6AE_ISSUE_NUMBER:
        reasons.append("ISSUE_MISMATCH_OR_COPIED_APPROVAL")
    if approval.get("actor_association") != L6AE_OWNER_ASSOCIATION:
        reasons.append("NON_OWNER_APPROVAL")
    if approval.get("operation_class") != L6AE_OPERATION_CLASS:
        reasons.append("OPERATION_CLASS_MISMATCH")
    if approval.get("source_floor") != L6AE_SOURCE_FLOOR:
        reasons.append("SOURCE_FLOOR_MISMATCH")
    if approval.get("approval_comment_id") != L6AE_APPROVAL_COMMENT_ID:
        reasons.append("APPROVAL_COMMENT_MISMATCH")
    if tuple(approval.get("approved_file_envelope", ())) != L6AE_ALLOWED_FILE_ENVELOPE:
        reasons.append("FILE_ENVELOPE_MISMATCH_OR_BROADENED")
    if approval.get("max_slices") != L6AE_MAX_SLICES:
        reasons.append("MAX_SLICES_NOT_EXACTLY_ONE")
    try:
        if _parse_utc(str(evaluated_at)) > _parse_utc(str(approval.get("expires_at", ""))):
            reasons.append("APPROVAL_EXPIRED")
    except ValueError:
        reasons.append("APPROVAL_EXPIRY_INVALID")
    forbidden_true_fields = [
        "live_private_reads_authorized",
        "raw_private_content_authorized",
        "additional_source_card_reads_authorized",
        "credentials_or_auth_reads_authorized",
        "source_discovery_authorized",
        "runtime_registry_authorized",
        "callbacks_authorized",
        "persistence_or_mutation_authorized",
        "activation_authorized",
        "cron_changes_authorized",
        "publication_or_visibility_authorized",
        "provider_prod_canary_or_gate_movement_authorized",
        "atlas_gate_movement_authorized",
        "broad_allowed_true_authorized",
    ]
    if any(approval.get(field) is not False for field in forbidden_true_fields):
        reasons.append("HELD_SURFACE_AUTHORIZATION_REQUESTED")
    return reasons


def approval_matches_l6ae01(approval: Mapping[str, Any], *, evaluated_at: str) -> bool:
    return not approval_denial_reasons(approval, evaluated_at=evaluated_at)


def adapt_l6ae01_report_safe_source_card_value(
    approval: Mapping[str, Any] | None,
    fixture: Mapping[str, Any] | None = None,
    *,
    evaluated_at: str,
) -> dict[str, Any]:
    """Return report-safe fixture metadata when the exact #281 approval matches.

    This adapter is deliberately default-off and fixture-only. It never calls a
    provider/backend/source reader, never discovers sources, never reads
    credentials/config/environment material, never persists data, never starts a
    service, and never emits a broad boolean ``allowed=True`` result.
    """

    approval_mapping: Mapping[str, Any] = approval or {}
    fixture_mapping: Mapping[str, Any] = fixture or build_l6ae01_report_safe_fixture()
    reasons = approval_denial_reasons(approval_mapping, evaluated_at=evaluated_at)
    unsafe_fixture = (
        set(fixture_mapping) - L6AE_FIXTURE_SAFE_FIELDS
        or any(_contains_unsafe_key(str(key)) for key in fixture_mapping)
        or _contains_unsafe_echo(fixture_mapping)
        or fixture_mapping.get("fixture_only") is not True
        or fixture_mapping.get("report_safe") is not True
        or fixture_mapping.get("metadata_only") is not True
    )
    if unsafe_fixture:
        reasons.append("UNSAFE_OR_NON_FIXTURE_INPUT_REJECTED")

    passed = not reasons
    descriptor_ref = str(fixture_mapping.get("descriptor_ref", L6AE_DESCRIPTOR_REF))
    source_card_ref = str(fixture_mapping.get("source_card_ref", L6AE_SOURCE_CARD_REF))
    usefulness_label = str(
        fixture_mapping.get("usefulness_label", "NOT_APPLICABLE_DENIED_DEFAULT_OFF")
    )
    if not passed:
        descriptor_ref = L6AE_DESCRIPTOR_REF
        source_card_ref = L6AE_SOURCE_CARD_REF
        usefulness_label = "NOT_APPLICABLE_DENIED_DEFAULT_OFF"

    return {
        "schema_version": L6AE_ADAPTER_SCHEMA_VERSION,
        "status": L6AE_PASS_STATUS if passed else L6AE_DENIED_STATUS,
        "approval_result": (
            "EXACT_ISSUE_BOUND_OWNER_APPROVAL_MATCH_FIXTURE_ONLY"
            if passed
            else "DENY_BEFORE_ADAPTER_ACTION"
        ),
        "denial_reasons": [] if passed else sorted(set(reasons)),
        "repository": L6AE_REPOSITORY,
        "issue_number": L6AE_ISSUE_NUMBER,
        "parent_issue": L6AE_PARENT_ISSUE,
        "operation_class": L6AE_OPERATION_CLASS,
        "source_floor": L6AE_SOURCE_FLOOR,
        "approval_comment_id": L6AE_APPROVAL_COMMENT_ID,
        "approval_expires_at": L6AE_APPROVAL_EXPIRES_AT,
        "evaluated_at": evaluated_at,
        "descriptor_ref": descriptor_ref,
        "source_card_ref": source_card_ref,
        "usefulness_label": usefulness_label,
        "adapter_scope": "FIXTURE_ONLY_REPORT_SAFE_METADATA_NO_RUNTIME_WIRING",
        "fixture_only": True,
        "default_off": True,
        "report_safe": True,
        "metadata_only": True,
        "allowed": "EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER" if passed else False,
        "allowed_result_count": 1 if passed else 0,
        "live_read_invoked": False,
        "unsafe_raw_fields_rejected_before_report": True,
        "guarded_counters": _zero_counters(),
        "residual_holds": list(L6AE_HELD_SURFACES),
    }


def validate_l6ae01_adapter_output(output: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(output) - L6AE_REPORT_SAFE_OUTPUT_FIELDS:
        errors.append("unexpected_output_field")
    unsafe_unknown_fields = (set(output) - L6AE_REPORT_SAFE_OUTPUT_FIELDS)
    if any(_contains_unsafe_key(str(key)) for key in unsafe_unknown_fields):
        errors.append("unsafe_output_key")
    if _contains_unsafe_echo(output):
        errors.append("unsafe_output_echo")
    if output.get("schema_version") != L6AE_ADAPTER_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if output.get("repository") != L6AE_REPOSITORY or output.get("issue_number") != L6AE_ISSUE_NUMBER:
        errors.append("unexpected_issue_binding")
    if output.get("operation_class") != L6AE_OPERATION_CLASS:
        errors.append("unexpected_operation_class")
    for field in ("fixture_only", "default_off", "report_safe", "metadata_only"):
        if output.get(field) is not True:
            errors.append(f"{field}_not_true")
    if output.get("live_read_invoked") is not False:
        errors.append("live_read_invoked_not_false")
    counters = output.get("guarded_counters")
    if not isinstance(counters, Mapping):
        errors.append("missing_guarded_counters")
    elif any(counters.get(counter) != 0 for counter in L6AE_GUARDED_COUNTERS):
        errors.append("guarded_counter_nonzero")
    if output.get("allowed") is True:
        errors.append("broad_allowed_true")
    if output.get("status") == L6AE_PASS_STATUS:
        if output.get("allowed") != "EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER":
            errors.append("pass_allowed_label_missing")
        if output.get("allowed_result_count") != 1:
            errors.append("pass_allowed_count_not_one_fixture_result")
    elif output.get("status") == L6AE_DENIED_STATUS:
        if output.get("allowed") is not False:
            errors.append("denied_allowed_not_false")
        if output.get("allowed_result_count") != 0:
            errors.append("denied_allowed_count_nonzero")
        if not output.get("denial_reasons"):
            errors.append("denied_reasons_missing")
    else:
        errors.append("unexpected_status")
    return errors


__all__ = [
    "L6AE_ADAPTER_SCHEMA_VERSION",
    "L6AE_ALLOWED_FILE_ENVELOPE",
    "L6AE_APPROVAL_COMMENT_ID",
    "L6AE_APPROVAL_EXPIRES_AT",
    "L6AE_DENIED_STATUS",
    "L6AE_GUARDED_COUNTERS",
    "L6AE_HELD_SURFACES",
    "L6AE_HOLD_STATUS",
    "L6AE_ISSUE_NUMBER",
    "L6AE_OPERATION_CLASS",
    "L6AE_PASS_STATUS",
    "L6AE_REPOSITORY",
    "L6AE_SOURCE_FLOOR",
    "adapt_l6ae01_report_safe_source_card_value",
    "approval_denial_reasons",
    "approval_matches_l6ae01",
    "build_l6ae01_exact_approval_fixture",
    "build_l6ae01_report_safe_fixture",
    "validate_l6ae01_adapter_output",
]
