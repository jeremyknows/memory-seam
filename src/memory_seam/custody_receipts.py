"""No-op custody receipt fixtures for future write/custody decisions.

This module is metadata-only. It defines the review shape for future custody
receipts without implementing writes, custody handoff, rollback, or reindexing.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

L6_CUSTODY_RECEIPT_STATUS = "noop_fixture_implementation_held"
L6_CUSTODY_RECEIPT_SCHEMA_VERSION = "l6-custody-receipt-noop-v1"
L6_CUSTODY_RECEIPT_HELD_SURFACES = (
    "write_execution",
    "custody_transfer",
    "delete_execution",
    "reindex_execution",
    "rollback_execution",
    "provider_backend_calls",
    "source_discovery_or_reads",
)
L6_CUSTODY_RECEIPT_REQUIRED_FIELDS = (
    "schema_version",
    "status",
    "receipt_id",
    "shape",
    "decision",
    "requested_operation",
    "safe_subject_ref",
    "safe_scope",
    "safe_payload_class",
    "approval_state",
    "rollback_state",
    "side_effects",
    "held_surfaces",
    "report_safety",
)
L6_CUSTODY_RECEIPT_ALLOWED_SHAPES = (
    "requested",
    "denied_before_write",
    "held_for_approval",
    "rollback_required",
)
_SAFE_SIDE_EFFECTS = {
    "write_custody_or_reindex": False,
    "write_callbacks": 0,
    "custody_callbacks": 0,
    "reindex_callbacks": 0,
    "rollback_callbacks": 0,
    "provider_calls": 0,
    "backend_calls": 0,
    "source_stat_calls": 0,
    "source_read_calls": 0,
}
_REPORT_SAFETY = {
    "raw_private_text": False,
    "credentials_or_auth_material": False,
    "private_paths": False,
    "platform_ids": False,
    "raw_query_or_payload": False,
    "private_correlation_refs": False,
}


def _fixture(
    *,
    receipt_id: str,
    shape: str,
    decision: str,
    requested_operation: str,
    approval_state: str,
    rollback_state: str,
    safe_payload_class: str,
) -> dict[str, Any]:
    return {
        "schema_version": L6_CUSTODY_RECEIPT_SCHEMA_VERSION,
        "status": L6_CUSTODY_RECEIPT_STATUS,
        "receipt_id": receipt_id,
        "shape": shape,
        "decision": decision,
        "requested_operation": requested_operation,
        "safe_subject_ref": "synthetic-agent-subject",
        "safe_scope": "synthetic-memory-scope",
        "safe_payload_class": safe_payload_class,
        "approval_state": approval_state,
        "rollback_state": rollback_state,
        "side_effects": deepcopy(_SAFE_SIDE_EFFECTS),
        "held_surfaces": L6_CUSTODY_RECEIPT_HELD_SURFACES,
        "report_safety": deepcopy(_REPORT_SAFETY),
    }


L6_CUSTODY_RECEIPT_NOOP_FIXTURES: tuple[dict[str, Any], ...] = (
    _fixture(
        receipt_id="receipt-fixture-requested",
        shape="requested",
        decision="record_request_only_no_write",
        requested_operation="write_intent",
        approval_state="not_approved",
        rollback_state="not_applicable_no_write_occurred",
        safe_payload_class="metadata_summary_only",
    ),
    _fixture(
        receipt_id="receipt-fixture-denied-before-write",
        shape="denied_before_write",
        decision="deny_before_write_callbacks",
        requested_operation="delete_intent",
        approval_state="denied",
        rollback_state="not_applicable_no_write_occurred",
        safe_payload_class="unsafe_or_unapproved_write_like_shape",
    ),
    _fixture(
        receipt_id="receipt-fixture-held-for-approval",
        shape="held_for_approval",
        decision="hold_pending_explicit_human_approval",
        requested_operation="custody_transfer_intent",
        approval_state="held_for_jeremy_approval",
        rollback_state="not_applicable_no_write_occurred",
        safe_payload_class="bounded_custody_metadata_only",
    ),
    _fixture(
        receipt_id="receipt-fixture-rollback-required",
        shape="rollback_required",
        decision="record_rollback_need_only_no_rollback_execution",
        requested_operation="rollback_intent",
        approval_state="implementation_held",
        rollback_state="rollback_required_but_not_executed",
        safe_payload_class="safe_failure_metadata_only",
    ),
)


def build_l6_custody_receipt_noop_fixtures() -> tuple[dict[str, Any], ...]:
    """Return deep-copied no-op custody receipt fixtures.

    Returning copies keeps tests and downstream examples from mutating the module
    constants while preserving a pure metadata-only contract.
    """

    return deepcopy(L6_CUSTODY_RECEIPT_NOOP_FIXTURES)


def validate_l6_custody_receipt_noop_fixture(receipt: dict[str, Any]) -> list[str]:
    """Return report-safe validation errors for a no-op custody receipt fixture."""

    errors: list[str] = []
    for field in L6_CUSTODY_RECEIPT_REQUIRED_FIELDS:
        if field not in receipt:
            errors.append(f"missing_{field}")
    if receipt.get("schema_version") != L6_CUSTODY_RECEIPT_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if receipt.get("status") != L6_CUSTODY_RECEIPT_STATUS:
        errors.append("unexpected_status")
    if receipt.get("shape") not in L6_CUSTODY_RECEIPT_ALLOWED_SHAPES:
        errors.append("unexpected_shape")
    side_effects = receipt.get("side_effects")
    if not isinstance(side_effects, dict):
        errors.append("missing_side_effect_counters")
    elif side_effects != _SAFE_SIDE_EFFECTS:
        errors.append("nonzero_side_effect_counter")
    report_safety = receipt.get("report_safety")
    if not isinstance(report_safety, dict):
        errors.append("missing_report_safety_flags")
    elif report_safety != _REPORT_SAFETY:
        errors.append("unsafe_report_safety_flag")
    held_surfaces = tuple(receipt.get("held_surfaces", ()))
    for surface in L6_CUSTODY_RECEIPT_HELD_SURFACES:
        if surface not in held_surfaces:
            errors.append(f"missing_held_surface_{surface}")
    return errors
