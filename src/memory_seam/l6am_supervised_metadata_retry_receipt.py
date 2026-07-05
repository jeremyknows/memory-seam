from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from memory_seam.l6al_service_auth_contract import zero_l6al03_guarded_counters
from memory_seam.l6am_supervised_metadata_retry_packet import (
    L6AM01_ENDPOINT,
    L6AM01_EVIDENCE_CLASS,
    L6AM01_FORBIDDEN_OUTPUT_FIELDS,
    L6AM01_N,
    L6AM01_PARENT_ISSUE,
    L6AM01_QUERY_LABEL,
    L6AM01_QUERY_TEXT,
    L6AM01_RAIL_STARTING_SOURCE_FLOOR,
    L6AM01_REPOSITORY,
    L6AM01_SCOPE,
    L6AM01_AGENT,
)

L6AM02_SCHEMA_VERSION = "l6am02-supervised-metadata-retry-receipt-v1"
L6AM02_RAIL_ISSUE = 358
L6AM02_STATUS = "PASS_SUPERVISED_METADATA_RETRY_SAFE_DENIAL_CAPTURED"
L6AM02_BLOCKER_CLASSIFICATION = "SERVICE_ROUTE_AUDIENCE_AUTH_BINDING_BLOCKED_DENIAL_BEFORE_READ"
L6AM02_OPERATION_CLASS = "L6AM_EXACT_SUPERVISED_METADATA_RETRY_EXECUTION"
L6AM02_ENDPOINT = "memory_seam_recall"
L6AM02_AUTH_STATUS = "denied_before_read"
L6AM02_AUTH_STATUS_CODE = 403
L6AM02_DEGRADED_REASONS = ("wrong_route_audience",)
L6AM02_ITEM_COUNT = 0
L6AM02_SAFE_ITEM_LABELS: tuple[str, ...] = ()
L6AM02_DENIED_MISMATCH_STATUS = "NOT_EXECUTED_LIVE_MISMATCH_WOULD_BE_SECOND_SOURCE_BEARING_RECALL"

L6AM02_REPORT_SAFE_OUTPUT_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "operation_class",
        "evidence_class",
        "status",
        "blocker_classification",
        "endpoint",
        "packet_endpoint",
        "agent",
        "scope_requested",
        "scope_effective",
        "n",
        "query_label",
        "auth_status",
        "auth_status_code",
        "degraded",
        "degraded_reasons",
        "partial",
        "item_count",
        "safe_item_labels",
        "denial_before_read_mismatch_check",
        "guarded_counters",
    }
)


def build_l6am02_safe_denial_receipt() -> dict[str, Any]:
    """Return the report-safe receipt from the one exact supervised MCP retry."""

    return {
        "schema_version": L6AM02_SCHEMA_VERSION,
        "repo": L6AM01_REPOSITORY,
        "parent_issue": L6AM01_PARENT_ISSUE,
        "rail_issue": L6AM02_RAIL_ISSUE,
        "rail_starting_source_floor": L6AM01_RAIL_STARTING_SOURCE_FLOOR,
        "operation_class": L6AM02_OPERATION_CLASS,
        "evidence_class": L6AM01_EVIDENCE_CLASS,
        "status": L6AM02_STATUS,
        "blocker_classification": L6AM02_BLOCKER_CLASSIFICATION,
        "endpoint": L6AM02_ENDPOINT,
        "packet_endpoint": L6AM01_ENDPOINT,
        "agent": L6AM01_AGENT,
        "scope_requested": L6AM01_SCOPE,
        "scope_effective": [],
        "n": L6AM01_N,
        "query_label": L6AM01_QUERY_LABEL,
        "auth_status": L6AM02_AUTH_STATUS,
        "auth_status_code": L6AM02_AUTH_STATUS_CODE,
        "degraded": True,
        "degraded_reasons": list(L6AM02_DEGRADED_REASONS),
        "partial": True,
        "item_count": L6AM02_ITEM_COUNT,
        "safe_item_labels": list(L6AM02_SAFE_ITEM_LABELS),
        "denial_before_read_mismatch_check": L6AM02_DENIED_MISMATCH_STATUS,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6am02_receipt_report_safe(receipt: Mapping[str, Any]) -> None:
    forbidden = L6AM01_FORBIDDEN_OUTPUT_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"unsafe report fields present: {sorted(forbidden)}")

    unexpected = set(receipt.keys()).difference(L6AM02_REPORT_SAFE_OUTPUT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected report fields present: {sorted(unexpected)}")

    if receipt.get("endpoint") != L6AM02_ENDPOINT:
        raise AssertionError("receipt must name only the supervised MCP endpoint metadata")
    if receipt.get("auth_status_code") != L6AM02_AUTH_STATUS_CODE:
        raise AssertionError("receipt must preserve the safe 403 auth status")
    if receipt.get("item_count") != 0:
        raise AssertionError("safe denial receipt must have zero returned items")
    if receipt.get("safe_item_labels") != []:
        raise AssertionError("safe denial receipt must not contain item labels")

    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero after denial-before-read")

    reasons = receipt.get("degraded_reasons")
    if not isinstance(reasons, Sequence) or "wrong_route_audience" not in reasons:
        raise AssertionError("receipt must classify the wrong-route-audience blocker")

    mismatch_status = receipt.get("denial_before_read_mismatch_check")
    if mismatch_status != L6AM02_DENIED_MISMATCH_STATUS:
        raise AssertionError("live mismatch check must remain unexecuted when it would require a second recall")


def exact_l6am02_retry_binding() -> dict[str, Any]:
    return {
        "tool": L6AM02_ENDPOINT,
        "agent": L6AM01_AGENT,
        "scope": L6AM01_SCOPE,
        "n": L6AM01_N,
        "query": L6AM01_QUERY_TEXT,
    }
