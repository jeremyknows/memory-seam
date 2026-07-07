from __future__ import annotations

from collections.abc import Mapping
from typing import Any

L6X_ONE_READ_RECEIPT_SCHEMA_VERSION = "l6x-one-read-receipt-v1"
L6X_ONE_READ_OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ"

L6X_ONE_READ_SAFE_RECEIPT_FIELDS = frozenset(
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
        "stop_status",
        "rollback_status",
        "guarded_counters",
        "report_safe",
        "metadata_only",
        "unsafe_raw_fields_rejected_before_report",
    }
)

L6X_ONE_READ_GUARDED_COUNTERS = (
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

L6X_ONE_READ_UNSAFE_ECHO_MARKERS = (
    "raw private source text",
    "private path",
    "source://",
    "platform-raw-id",
    "raw prompt",
    "raw query",
    "raw backend response",
    "credential",
    "auth material",
    "private-correlation-ref",
    "raw approval text",
)


def build_l6x02_absent_approval_hold_receipt() -> dict[str, Any]:
    """Return the report-safe #212 absent-approval HOLD receipt fixture."""

    return {
        "schema_version": L6X_ONE_READ_RECEIPT_SCHEMA_VERSION,
        "receipt_status": "HOLD",
        "approval_result": "DENIED_BEFORE_CALLBACK",
        "live_read_invoked": False,
        "allowed": False,
        "allowed_result_count": 0,
        "operation_class": L6X_ONE_READ_OPERATION_CLASS,
        "operation_count_attempted": 0,
        "descriptor_ref": "ABSENT_DENIED_BEFORE_READ",
        "source_card_ref": "ABSENT_DENIED_BEFORE_READ",
        "stop_status": "APPROVAL_ABSENT_DENIED_BEFORE_READ",
        "rollback_status": "NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED",
        "guarded_counters": {counter: 0 for counter in L6X_ONE_READ_GUARDED_COUNTERS},
        "report_safe": True,
        "metadata_only": True,
        "unsafe_raw_fields_rejected_before_report": True,
    }


def _contains_unsafe_echo(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker.lower() in lowered for marker in L6X_ONE_READ_UNSAFE_ECHO_MARKERS)
    if isinstance(value, Mapping):
        return any(_contains_unsafe_echo(item) for item in value.values())
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_unsafe_echo(item) for item in value)
    return False


def validate_l6x_one_read_receipt(receipt: Mapping[str, Any]) -> list[str]:
    """Return report-safe validation errors for one-read attempt receipts.

    The verifier is metadata-only: it inspects an already supplied receipt mapping and
    never performs source discovery, live reads, callbacks, persistence, activation, or
    credential/auth reads.
    """

    errors: list[str] = []
    unknown_fields = set(receipt) - L6X_ONE_READ_SAFE_RECEIPT_FIELDS
    if unknown_fields:
        errors.append("unsafe_receipt_field_present")
    if receipt.get("schema_version") != L6X_ONE_READ_RECEIPT_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if receipt.get("operation_class") != L6X_ONE_READ_OPERATION_CLASS:
        errors.append("unexpected_operation_class")
    if receipt.get("operation_count_attempted") not in (0, 1):
        errors.append("operation_count_not_zero_or_one")
    if receipt.get("live_read_invoked") is True and receipt.get("operation_count_attempted") != 1:
        errors.append("live_read_without_single_operation")
    if receipt.get("allowed") is not False:
        errors.append("allowed_not_false")
    if receipt.get("allowed_result_count") != 0:
        errors.append("allowed_result_count_not_zero")
    for field in ("report_safe", "metadata_only", "unsafe_raw_fields_rejected_before_report"):
        if receipt.get(field) is not True:
            errors.append(f"{field}_not_true")
    for ref_field in ("descriptor_ref", "source_card_ref"):
        ref = receipt.get(ref_field)
        if not isinstance(ref, str) or not ref:
            errors.append(f"missing_{ref_field}")
        elif _contains_unsafe_echo(ref):
            errors.append(f"unsafe_{ref_field}_echo")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping):
        errors.append("missing_guarded_counters")
    else:
        for counter in L6X_ONE_READ_GUARDED_COUNTERS:
            if counters.get(counter) != 0:
                errors.append(f"nonzero_counter_{counter}")
    if _contains_unsafe_echo(receipt):
        errors.append("unsafe_echo_marker_present")
    return errors


__all__ = [
    "L6X_ONE_READ_GUARDED_COUNTERS",
    "L6X_ONE_READ_OPERATION_CLASS",
    "L6X_ONE_READ_RECEIPT_SCHEMA_VERSION",
    "L6X_ONE_READ_SAFE_RECEIPT_FIELDS",
    "L6X_ONE_READ_UNSAFE_ECHO_MARKERS",
    "build_l6x02_absent_approval_hold_receipt",
    "validate_l6x_one_read_receipt",
]
