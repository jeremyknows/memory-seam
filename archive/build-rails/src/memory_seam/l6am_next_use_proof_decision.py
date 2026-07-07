from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from memory_seam.l6al_service_auth_contract import ENDPOINT_AUDIENCES, zero_l6al03_guarded_counters
from memory_seam.l6am_supervised_metadata_retry_packet import (
    L6AM01_AGENT,
    L6AM01_EVIDENCE_CLASS,
    L6AM01_N,
    L6AM01_PARENT_ISSUE,
    L6AM01_QUERY_LABEL,
    L6AM01_QUERY_TEXT,
    L6AM01_RAIL_STARTING_SOURCE_FLOOR,
    L6AM01_REPOSITORY,
    L6AM01_SCOPE,
)
from memory_seam.l6am_supervised_metadata_retry_receipt import (
    L6AM02_BLOCKER_CLASSIFICATION,
    L6AM02_STATUS,
    build_l6am02_safe_denial_receipt,
)

L6AM03_SCHEMA_VERSION = "l6am03-next-use-proof-decision-v1"
L6AM03_RAIL_ISSUE = 359
L6AM03_STATUS = "PASS_NEXT_USE_PROOF_DECISION_AUTH_UNBLOCK_PACKET_PREPARED"
L6AM03_DECISION = "PREPARE_SERVICE_OPERATOR_AUTH_UNBLOCK_PACKET_BEFORE_USER_VISIBLE_USE_PROOF"
L6AM03_NEXT_FRONTIER = "SERVICE_OPERATOR_AUTH_BINDING_UNBLOCK_FOR_EXACT_METADATA_RECALL"
L6AM03_USER_VISIBLE_PROOF_STATE = "HELD_UNTIL_AUTH_BINDING_RETURNS_METADATA"

L6AM03_MISSING_BINDING_FIELDS = (
    "route_audience=memory-seam:read:recall (recall endpoint)",
    "identity_subject bound to the supervised service caller",
    "acting_for=sax",
    "agent=sax",
    "scope=wiki",
    "query_label=supervised_metadata_readiness",
    "evidence_class=SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
    "max_operation_count=1",
    "report_safe_metadata_only=true",
    "denial_before_read_required=true",
    "operator/service binding reference with expiry or one-run custody",
)

L6AM03_STOP_CONDITIONS = (
    "auth_status_code_403",
    "wrong_route_audience",
    "unauthorized_narrowing",
    "missing_identity_subject",
    "missing_acting_for",
    "missing_or_stale_operator_service_binding_ref",
    "empty_items",
    "raw_output_request",
    "source_discovery_or_broad_recall_request",
    "runtime_registry_or_provider_callback_request",
    "service_activation_or_prod_canary_gate_request",
    "write_mutation_or_persistence_request",
    "broad_allowed_true_request",
)

L6AM03_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "status",
        "decision",
        "next_frontier",
        "user_visible_proof_state",
        "l6am02_status",
        "l6am02_blocker_classification",
        "retry_result_metadata",
        "missing_binding_fields",
        "unblock_packet",
        "stop_conditions",
        "guarded_counters",
    }
)


def build_l6am03_auth_unblock_packet() -> dict[str, Any]:
    """Prepare the exact service/operator auth unblock packet after the L6AM.02 safe denial."""

    return {
        "operation_class": L6AM03_NEXT_FRONTIER,
        "endpoint": "memory_seam_recall",
        "route_audience_required": ENDPOINT_AUDIENCES["recall"],
        "acting_for_required": L6AM01_AGENT,
        "agent_required": L6AM01_AGENT,
        "scope_required": L6AM01_SCOPE,
        "n_required": L6AM01_N,
        "query_label_required": L6AM01_QUERY_LABEL,
        "query_text_required": L6AM01_QUERY_TEXT,
        "evidence_class_required": L6AM01_EVIDENCE_CLASS,
        "max_operation_count": 1,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
        "requires_fresh_operator_service_binding": True,
        "approval_not_inferred_from": [
            "L6AM.01 packet merge",
            "L6AM.02 safe-denial receipt",
            "issue closure",
            "labels",
            "stale parent comments",
            "broad keep-going language",
        ],
    }


def build_l6am03_next_use_proof_decision() -> dict[str, Any]:
    retry = build_l6am02_safe_denial_receipt()
    retry_metadata = {
        "endpoint": retry["endpoint"],
        "auth_status": retry["auth_status"],
        "auth_status_code": retry["auth_status_code"],
        "degraded": retry["degraded"],
        "degraded_reasons": retry["degraded_reasons"],
        "item_count": retry["item_count"],
        "safe_item_labels": retry["safe_item_labels"],
    }
    return {
        "schema_version": L6AM03_SCHEMA_VERSION,
        "repo": L6AM01_REPOSITORY,
        "parent_issue": L6AM01_PARENT_ISSUE,
        "rail_issue": L6AM03_RAIL_ISSUE,
        "rail_starting_source_floor": L6AM01_RAIL_STARTING_SOURCE_FLOOR,
        "status": L6AM03_STATUS,
        "decision": L6AM03_DECISION,
        "next_frontier": L6AM03_NEXT_FRONTIER,
        "user_visible_proof_state": L6AM03_USER_VISIBLE_PROOF_STATE,
        "l6am02_status": L6AM02_STATUS,
        "l6am02_blocker_classification": L6AM02_BLOCKER_CLASSIFICATION,
        "retry_result_metadata": retry_metadata,
        "missing_binding_fields": list(L6AM03_MISSING_BINDING_FIELDS),
        "unblock_packet": build_l6am03_auth_unblock_packet(),
        "stop_conditions": list(L6AM03_STOP_CONDITIONS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6am03_decision_report_safe(decision: Mapping[str, Any]) -> None:
    unexpected = set(decision.keys()).difference(L6AM03_REPORT_SAFE_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected report fields present: {sorted(unexpected)}")
    if decision.get("decision") != L6AM03_DECISION:
        raise AssertionError("L6AM.03 must choose the auth unblock packet after denied/empty retry")
    retry_metadata = decision.get("retry_result_metadata")
    if not isinstance(retry_metadata, Mapping):
        raise AssertionError("retry result metadata must be report-safe mapping")
    if retry_metadata.get("item_count") != 0:
        raise AssertionError("metadata-returned proof is not available when item_count is zero")
    if retry_metadata.get("auth_status_code") != 403:
        raise AssertionError("auth unblock packet must be based on the 403 safe denial")
    if "wrong_route_audience" not in retry_metadata.get("degraded_reasons", []):
        raise AssertionError("wrong_route_audience must remain the concrete blocker")
    counters = decision.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("decision packet must keep guarded counters zero")
    if decision.get("user_visible_proof_state") != L6AM03_USER_VISIBLE_PROOF_STATE:
        raise AssertionError("user-visible use proof must stay held until auth returns metadata")
