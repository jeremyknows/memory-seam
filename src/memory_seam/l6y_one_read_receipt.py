from __future__ import annotations

from collections.abc import Mapping
from typing import Any

L6Y_ONE_READ_RECEIPT_SCHEMA_VERSION = "l6y-one-read-receipt-v1"
L6Y_ONE_READ_OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ"
L6Y_ONE_READ_HOLD_STATUS = "HOLD_DENIED_BEFORE_READ_APPROVAL_MISMATCH_NO_LIVE"
L6Y_ONE_READ_APPROVAL_RESULT = "DENIED_BEFORE_CALLBACK"

L6Y_ONE_READ_SAFE_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "receipt_status",
        "approval_result",
        "live_read_invoked",
        "allowed",
        "allowed_result_count",
        "operation_class",
        "operation_count_attempted",
        "descriptor_ref",
        "source_card_ref",
        "read_usefulness_label",
        "redaction_status",
        "rollback_status",
        "guarded_counters",
        "report_safe",
        "metadata_only",
        "unsafe_raw_fields_rejected_before_report",
    }
)

L6Y_ONE_READ_GUARDED_COUNTERS = (
    "approval_comments_examined",
    "valid_owner_approval_comments",
    "provider_callbacks",
    "backend_callbacks",
    "source_stat_callbacks",
    "source_read_callbacks",
    "credential_reads",
    "runtime_registry_reads",
    "persistence_writes",
    "mutation_callbacks",
    "rollback_callbacks",
    "cache_purge_callbacks",
)

L6Y_ONE_READ_UNSAFE_KEY_MARKERS = (
    "raw",
    "private",
    "secret",
    "token",
    "credential",
    "password",
    "auth",
    "oauth",
    "keychain",
    "env",
    "path",
    "uri",
    "platform_id",
    "prompt",
    "query",
    "payload",
    "backend_response",
    "correlation",
    "source_text",
    "approval_text",
)

L6Y_ONE_READ_UNSAFE_ECHO_MARKERS = (
    "raw private source text",
    "private path",
    "source://",
    "platform-raw-id",
    "raw platform id",
    "raw prompt",
    "raw query",
    "query payload",
    "raw payload",
    "raw backend response",
    "credential",
    "auth material",
    "oauth material",
    "keychain material",
    "auth-file material",
    "private-correlation-ref",
    "raw approval text",
)


def build_l6y02_approval_mismatch_hold_receipt() -> dict[str, Any]:
    """Return the report-safe #222 deny-before-read HOLD receipt fixture.

    The fixture is a committed metadata object only. It performs no live/private
    read, source discovery, callback, credential/auth lookup, Runtime Registry
    consumption, persistence, mutation, activation, publication, production/canary
    movement, Gate movement, rollback execution, or cache purge.
    """

    return {
        "schema_version": L6Y_ONE_READ_RECEIPT_SCHEMA_VERSION,
        "receipt_status": L6Y_ONE_READ_HOLD_STATUS,
        "approval_result": L6Y_ONE_READ_APPROVAL_RESULT,
        "live_read_invoked": False,
        "allowed": False,
        "allowed_result_count": 0,
        "operation_class": L6Y_ONE_READ_OPERATION_CLASS,
        "operation_count_attempted": 0,
        "descriptor_ref": "MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ",
        "source_card_ref": "MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ",
        "read_usefulness_label": "NOT_EVALUATED_NO_READ",
        "redaction_status": "REPORT_SAFE_METADATA_ONLY",
        "rollback_status": "NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED",
        "guarded_counters": {
            counter: 0 for counter in L6Y_ONE_READ_GUARDED_COUNTERS
        }
        | {"approval_comments_examined": 1},
        "report_safe": True,
        "metadata_only": True,
        "unsafe_raw_fields_rejected_before_report": True,
    }


def _contains_unsafe_echo(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker.lower() in lowered for marker in L6Y_ONE_READ_UNSAFE_ECHO_MARKERS)
    if isinstance(value, Mapping):
        return any(_contains_unsafe_echo(item) for item in value.values())
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_unsafe_echo(item) for item in value)
    return False


def _contains_unsafe_key(key: str) -> bool:
    lowered = key.lower().replace("-", "_")
    return any(marker in lowered for marker in L6Y_ONE_READ_UNSAFE_KEY_MARKERS)


def validate_l6y_one_read_receipt(receipt: Mapping[str, Any]) -> list[str]:
    """Return report-safe validation errors for the L6Y.02 receipt.

    The verifier inspects an already supplied receipt mapping only. It is not a
    read path and does not call providers, backends, sources, credentials,
    Runtime Registry, persistence, services, production/canary controls, Atlas
    Gate controls, rollback, mutation, or cache-purge surfaces.
    """

    errors: list[str] = []
    unknown_fields = set(receipt) - L6Y_ONE_READ_SAFE_RECEIPT_FIELDS
    if unknown_fields:
        errors.append("unsafe_receipt_field_present")
    if any(_contains_unsafe_key(str(field)) for field in unknown_fields):
        errors.append("unsafe_receipt_key_present")
    if receipt.get("schema_version") != L6Y_ONE_READ_RECEIPT_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if receipt.get("receipt_status") != L6Y_ONE_READ_HOLD_STATUS:
        errors.append("unexpected_receipt_status")
    if receipt.get("approval_result") != L6Y_ONE_READ_APPROVAL_RESULT:
        errors.append("unexpected_approval_result")
    if receipt.get("operation_class") != L6Y_ONE_READ_OPERATION_CLASS:
        errors.append("unexpected_operation_class")
    if receipt.get("operation_count_attempted") != 0:
        errors.append("operation_count_not_zero_for_hold")
    if receipt.get("live_read_invoked") is not False:
        errors.append("live_read_invoked_not_false_for_hold")
    if receipt.get("allowed") is not False:
        errors.append("allowed_not_false")
    if receipt.get("allowed_result_count") != 0:
        errors.append("allowed_result_count_not_zero")
    if receipt.get("read_usefulness_label") != "NOT_EVALUATED_NO_READ":
        errors.append("unexpected_read_usefulness_label")
    if receipt.get("redaction_status") != "REPORT_SAFE_METADATA_ONLY":
        errors.append("unexpected_redaction_status")
    if receipt.get("rollback_status") != "NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED":
        errors.append("unexpected_rollback_status")
    for field in ("report_safe", "metadata_only", "unsafe_raw_fields_rejected_before_report"):
        if receipt.get(field) is not True:
            errors.append(f"{field}_not_true")
    for ref_field in ("descriptor_ref", "source_card_ref"):
        ref = receipt.get(ref_field)
        if ref != "MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ":
            errors.append(f"unexpected_{ref_field}")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping):
        errors.append("missing_guarded_counters")
    else:
        if counters.get("approval_comments_examined") != 1:
            errors.append("unexpected_counter_approval_comments_examined")
        for counter in L6Y_ONE_READ_GUARDED_COUNTERS:
            expected = 1 if counter == "approval_comments_examined" else 0
            if counters.get(counter) != expected:
                errors.append(f"nonzero_counter_{counter}")
        unknown_counters = set(counters) - set(L6Y_ONE_READ_GUARDED_COUNTERS)
        if unknown_counters:
            errors.append("unsafe_guarded_counter_present")
        if any(_contains_unsafe_key(str(counter)) for counter in unknown_counters):
            errors.append("unsafe_guarded_counter_key_present")
    if _contains_unsafe_echo(receipt):
        errors.append("unsafe_echo_marker_present")
    return errors


__all__ = [
    "L6Y_ONE_READ_APPROVAL_RESULT",
    "L6Y_ONE_READ_GUARDED_COUNTERS",
    "L6Y_ONE_READ_HOLD_STATUS",
    "L6Y_ONE_READ_OPERATION_CLASS",
    "L6Y_ONE_READ_RECEIPT_SCHEMA_VERSION",
    "L6Y_ONE_READ_SAFE_RECEIPT_FIELDS",
    "L6Y_ONE_READ_UNSAFE_ECHO_MARKERS",
    "L6Y_ONE_READ_UNSAFE_KEY_MARKERS",
    "build_l6y02_approval_mismatch_hold_receipt",
    "validate_l6y_one_read_receipt",
]
