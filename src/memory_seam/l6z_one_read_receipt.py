from __future__ import annotations

from collections.abc import Mapping
from typing import Any

L6Z_ONE_READ_RECEIPT_SCHEMA_VERSION = "l6z-one-read-receipt-v1"
L6Z_ONE_READ_OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ"
L6Z_ONE_READ_HOLD_STATUS = "HOLD_DENIED_BEFORE_READ_APPROVAL_TARGET_REF_MISMATCH_NO_LIVE"
L6Z_ONE_READ_APPROVAL_RESULT = "DENY_BEFORE_READ"
L6Z_ONE_READ_STOP_CONDITION = "DENIED_BEFORE_CALLBACK"
L6Z_ONE_READ_EXPECTED_DESCRIPTOR_REF = "descriptor:l6z/report-safe-operator-preference-card"
L6Z_ONE_READ_EXPECTED_SOURCE_CARD_REF = "source-card:l6z/report-safe-operator-preference-card"
L6Z_ONE_READ_PRESENTED_DESCRIPTOR_REF = "descriptor:l6z/operator-proof"
L6Z_ONE_READ_PRESENTED_SOURCE_CARD_REF = "source-card:l6z/operator-proof"

L6Z_ONE_READ_SAFE_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "receipt_status",
        "approval_result",
        "stop_condition",
        "rollback_status",
        "approval_comment_id_examined",
        "approval_comment_author",
        "owner_actor_association",
        "approval_comment_created_at",
        "approval_evaluated_at",
        "freshness_result",
        "packet_issue_id",
        "read_issue_id",
        "parent_issue_id",
        "operation_class",
        "max_operation_count",
        "descriptor_ref_expected",
        "source_card_ref_expected",
        "descriptor_ref_presented",
        "source_card_ref_presented",
        "mismatch_reason",
        "live_read_invoked",
        "allowed",
        "allowed_result_count",
        "operation_count_attempted",
        "read_usefulness_label",
        "redaction_status",
        "guarded_counters",
        "report_safe",
        "metadata_only",
        "unsafe_raw_fields_rejected_before_report",
    }
)

L6Z_ONE_READ_GUARDED_COUNTERS = (
    "approval_comments_examined",
    "valid_owner_approval_comments",
    "live_read_invocations",
    "operation_count_attempted",
    "allowed_result_count",
    "provider_callbacks",
    "backend_callbacks",
    "source_stat_callbacks",
    "source_read_callbacks",
    "credential_reads",
    "auth_env_keychain_oauth_auth_file_reads",
    "runtime_registry_reads",
    "source_discovery_queries",
    "workspace_scans",
    "family_scans",
    "broad_recall_queries",
    "index_queries",
    "persistence_writes",
    "mutation_callbacks",
    "rollback_callbacks",
    "cache_purge_callbacks",
    "service_listener_startup_activations",
    "publication_or_visibility_changes",
    "provider_prod_canary_or_gate_moves",
)

L6Z_ONE_READ_UNSAFE_KEY_MARKERS = (
    "raw",
    "private",
    "secret",
    "token",
    "credential_value",
    "password",
    "auth_material",
    "oauth_token",
    "keychain",
    "env_value",
    "absolute_path",
    "source_uri",
    "platform_id",
    "prompt_payload",
    "query_payload",
    "payload_content",
    "backend_response",
    "correlation_ref",
    "source_text",
    "approval_text",
)

L6Z_ONE_READ_UNSAFE_ECHO_MARKERS = (
    "raw private source text",
    "private absolute path",
    "source://",
    "platform-raw-id",
    "raw platform id",
    "raw prompt",
    "raw query",
    "query payload",
    "raw payload",
    "raw backend response",
    "credential value",
    "auth material",
    "oauth token",
    "keychain material",
    "auth-file material",
    "private-correlation-ref",
    "raw approval text",
    "i approve exactly one supervised",
)


def build_l6z02_target_ref_mismatch_hold_receipt() -> dict[str, Any]:
    """Return the report-safe #232 deny-before-read HOLD receipt fixture.

    The fixture is committed metadata only. It does not perform a live/private
    read, callback, discovery query, Runtime Registry lookup, credential/auth
    lookup, persistence, mutation, activation, publication, production/canary
    movement, Gate movement, rollback execution, or cache purge.
    """

    return {
        "schema_version": L6Z_ONE_READ_RECEIPT_SCHEMA_VERSION,
        "receipt_status": L6Z_ONE_READ_HOLD_STATUS,
        "approval_result": L6Z_ONE_READ_APPROVAL_RESULT,
        "stop_condition": L6Z_ONE_READ_STOP_CONDITION,
        "rollback_status": "NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED",
        "approval_comment_id_examined": "4649997717",
        "approval_comment_author": "jeremyknows",
        "owner_actor_association": "OWNER",
        "approval_comment_created_at": "2026-06-08T14:25:56Z",
        "approval_evaluated_at": "2026-06-08T14:39:48Z",
        "freshness_result": "FRESH_WITHIN_12H",
        "packet_issue_id": "#231",
        "read_issue_id": "#232",
        "parent_issue_id": "#6",
        "operation_class": L6Z_ONE_READ_OPERATION_CLASS,
        "max_operation_count": 1,
        "descriptor_ref_expected": L6Z_ONE_READ_EXPECTED_DESCRIPTOR_REF,
        "source_card_ref_expected": L6Z_ONE_READ_EXPECTED_SOURCE_CARD_REF,
        "descriptor_ref_presented": L6Z_ONE_READ_PRESENTED_DESCRIPTOR_REF,
        "source_card_ref_presented": L6Z_ONE_READ_PRESENTED_SOURCE_CARD_REF,
        "mismatch_reason": "EXECUTABLE_TARGET_REFS_DO_NOT_MATCH_L6Z01_PACKET",
        "live_read_invoked": False,
        "allowed": False,
        "allowed_result_count": 0,
        "operation_count_attempted": 0,
        "read_usefulness_label": "NOT_APPLICABLE_NO_READ_EXECUTED",
        "redaction_status": "REPORT_SAFE_METADATA_ONLY_RAW_APPROVAL_TEXT_OMITTED",
        "guarded_counters": {
            counter: 0 for counter in L6Z_ONE_READ_GUARDED_COUNTERS
        }
        | {"approval_comments_examined": 1},
        "report_safe": True,
        "metadata_only": True,
        "unsafe_raw_fields_rejected_before_report": True,
    }


def _contains_unsafe_echo(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker.lower() in lowered for marker in L6Z_ONE_READ_UNSAFE_ECHO_MARKERS)
    if isinstance(value, Mapping):
        return any(_contains_unsafe_echo(item) for item in value.values())
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_unsafe_echo(item) for item in value)
    return False


def _contains_unsafe_key(key: str) -> bool:
    lowered = key.lower().replace("-", "_")
    return any(marker in lowered for marker in L6Z_ONE_READ_UNSAFE_KEY_MARKERS)


def validate_l6z_one_read_receipt(receipt: Mapping[str, Any]) -> list[str]:
    """Return report-safe validation errors for the #232 receipt.

    The verifier inspects an already supplied receipt mapping only. It is not a
    read path and does not call providers, backends, source-stat/source-read,
    credentials, Runtime Registry, persistence, services, production/canary
    controls, Atlas Gate controls, rollback, mutation, or cache-purge surfaces.
    """

    errors: list[str] = []
    unknown_fields = set(receipt) - L6Z_ONE_READ_SAFE_RECEIPT_FIELDS
    if unknown_fields:
        errors.append("unsafe_receipt_field_present")
    if any(_contains_unsafe_key(str(field)) for field in unknown_fields):
        errors.append("unsafe_receipt_key_present")
    expected_values = {
        "schema_version": L6Z_ONE_READ_RECEIPT_SCHEMA_VERSION,
        "receipt_status": L6Z_ONE_READ_HOLD_STATUS,
        "approval_result": L6Z_ONE_READ_APPROVAL_RESULT,
        "stop_condition": L6Z_ONE_READ_STOP_CONDITION,
        "rollback_status": "NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED",
        "approval_comment_author": "jeremyknows",
        "owner_actor_association": "OWNER",
        "freshness_result": "FRESH_WITHIN_12H",
        "packet_issue_id": "#231",
        "read_issue_id": "#232",
        "parent_issue_id": "#6",
        "operation_class": L6Z_ONE_READ_OPERATION_CLASS,
        "descriptor_ref_expected": L6Z_ONE_READ_EXPECTED_DESCRIPTOR_REF,
        "source_card_ref_expected": L6Z_ONE_READ_EXPECTED_SOURCE_CARD_REF,
        "descriptor_ref_presented": L6Z_ONE_READ_PRESENTED_DESCRIPTOR_REF,
        "source_card_ref_presented": L6Z_ONE_READ_PRESENTED_SOURCE_CARD_REF,
        "mismatch_reason": "EXECUTABLE_TARGET_REFS_DO_NOT_MATCH_L6Z01_PACKET",
        "read_usefulness_label": "NOT_APPLICABLE_NO_READ_EXECUTED",
        "redaction_status": "REPORT_SAFE_METADATA_ONLY_RAW_APPROVAL_TEXT_OMITTED",
    }
    for field, expected in expected_values.items():
        if receipt.get(field) != expected:
            errors.append(f"unexpected_{field}")
    if receipt.get("max_operation_count") != 1:
        errors.append("unexpected_max_operation_count")
    if receipt.get("approval_comment_id_examined") != "4649997717":
        errors.append("unexpected_approval_comment_id_examined")
    for field in ("live_read_invoked", "allowed"):
        if receipt.get(field) is not False:
            errors.append(f"{field}_not_false_for_hold")
    for field in ("allowed_result_count", "operation_count_attempted"):
        if receipt.get(field) != 0:
            errors.append(f"{field}_not_zero")
    for field in ("report_safe", "metadata_only", "unsafe_raw_fields_rejected_before_report"):
        if receipt.get(field) is not True:
            errors.append(f"{field}_not_true")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping):
        errors.append("missing_guarded_counters")
    else:
        for counter in L6Z_ONE_READ_GUARDED_COUNTERS:
            expected = 1 if counter == "approval_comments_examined" else 0
            if counters.get(counter) != expected:
                errors.append(f"unexpected_counter_{counter}")
        unknown_counters = set(counters) - set(L6Z_ONE_READ_GUARDED_COUNTERS)
        if unknown_counters:
            errors.append("unsafe_guarded_counter_present")
        if any(_contains_unsafe_key(str(counter)) for counter in unknown_counters):
            errors.append("unsafe_guarded_counter_key_present")
    if receipt.get("allowed") is True:
        errors.append("broad_allowed_true_rejected")
    if _contains_unsafe_echo(receipt):
        errors.append("unsafe_echo_marker_present")
    return errors


__all__ = [
    "L6Z_ONE_READ_APPROVAL_RESULT",
    "L6Z_ONE_READ_EXPECTED_DESCRIPTOR_REF",
    "L6Z_ONE_READ_EXPECTED_SOURCE_CARD_REF",
    "L6Z_ONE_READ_GUARDED_COUNTERS",
    "L6Z_ONE_READ_HOLD_STATUS",
    "L6Z_ONE_READ_OPERATION_CLASS",
    "L6Z_ONE_READ_PRESENTED_DESCRIPTOR_REF",
    "L6Z_ONE_READ_PRESENTED_SOURCE_CARD_REF",
    "L6Z_ONE_READ_RECEIPT_SCHEMA_VERSION",
    "L6Z_ONE_READ_SAFE_RECEIPT_FIELDS",
    "L6Z_ONE_READ_STOP_CONDITION",
    "L6Z_ONE_READ_UNSAFE_ECHO_MARKERS",
    "L6Z_ONE_READ_UNSAFE_KEY_MARKERS",
    "build_l6z02_target_ref_mismatch_hold_receipt",
    "validate_l6z_one_read_receipt",
]
