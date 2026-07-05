from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from memory_seam.l6al_service_auth_contract import zero_l6al03_guarded_counters

L6AP_PARENT_ISSUE = 6
L6AP_REPOSITORY = "jeremyknows/memory-seam"
L6AP_RAIL_STARTING_SOURCE_FLOOR = "35046efe4880145d929bbe0ddb00196b83c9cc04"
L6AP_FRESH_APPROVAL_SOURCE = "fresh-discord-source-deck-message-report-safe-anchor"
L6AP_PARENT_RAIL_CREATED_RECEIPT = "issue-6-comment-4659797054"

L6AP01_SCHEMA_VERSION = "l6ap01-fresh-binding-approval-max-one-preflight-v1"
L6AP02_SCHEMA_VERSION = "l6ap02-supervised-metadata-retry-safe-denial-receipt-v1"
L6AP03_SCHEMA_VERSION = "l6ap03-post-retry-step3-state-usefulness-decision-v1"
L6AP04_SCHEMA_VERSION = "l6ap04-trust-boundary-review-v1"
L6AP01_RAIL_ISSUE = 390
L6AP02_RAIL_ISSUE = 391
L6AP03_RAIL_ISSUE = 392
L6AP04_RAIL_ISSUE = 393
L6AP01_STATUS = "FRESH_BINDING_APPROVAL_RECEIPT_MAX_ONE_PREFLIGHT_READY_RETRY_HELD"
L6AP01_REFUSED_STATUS = "MAX_ONE_METADATA_RETRY_PREFLIGHT_REFUSED_BEFORE_READ"
L6AP02_STATUS = "SUPERVISED_METADATA_RETRY_SAFE_DENIAL_CAPTURED"
L6AP02_BLOCKER_CLASSIFICATION = "SERVICE_ROUTE_AUDIENCE_AUTH_BINDING_BLOCKED_DENIAL_BEFORE_READ"
L6AP03_STATUS = "STEP3_USEFULNESS_READINESS_HELD_AFTER_DENIED_EMPTY_METADATA_RETRY"
L6AP03_DECISION = "KEEP_STEP3_HELD_NO_SUCCESSOR_EXECUTION_RAIL"
L6AP03_STEP3_STATE = "HELD_DENIAL_BEFORE_READ_EMPTY_METADATA"
L6AP03_NEXT_BOUNDED_PROOF_LANE = "L6AP_TRUST_BOUNDARY_REVIEW_THEN_SOURCE_FLOOR_RECONCILIATION"
L6AP04_STATUS = "TRUST_BOUNDARY_REVIEW_PASS_MAX_ONE_METADATA_RETRY_RAIL"
L6AP04_DECISION = "PASS_TO_SOURCE_FLOOR_PARENT_TRACKER_RECONCILIATION"
L6AP01_APPROVAL_RECEIPT_COMMENT = "issue-390-comment-4659796366"
L6AP02_APPROVAL_RECEIPT_COMMENT = "issue-391-comment-4659796502"
L6AP01_OPERATION_CLASS = "L6AP_EXACT_MAX_ONE_SUPERVISED_METADATA_RETRY"
L6AP02_OPERATION_CLASS = "L6AP_EXACT_MAX_ONE_SUPERVISED_METADATA_RETRY_EXECUTION"
L6AP03_OPERATION_CLASS = "L6AP_POST_RETRY_STEP3_STATE_DECISION"
L6AP04_OPERATION_CLASS = "L6AP_TRUST_BOUNDARY_REVIEW"
L6AP01_QUERY_TEXT = (
    "Memory Seam supervised metadata read retry source-floor readiness held surfaces denial-before-read"
)
L6AP01_QUERY_LABEL = "supervised_metadata_readiness"
L6AP01_EVIDENCE_CLASS = "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
L6AP01_TARGET = {
    "endpoint": "memory_seam_recall",
    "route_audience": "memory-seam:read:recall",
    "acting_for": "sax",
    "agent": "sax",
    "scope": "wiki",
    "n": 3,
    "query_label": L6AP01_QUERY_LABEL,
    "query_text": L6AP01_QUERY_TEXT,
    "evidence_class": L6AP01_EVIDENCE_CLASS,
    "max_operation_count": 1,
    "report_safe_metadata_only": True,
    "denial_before_read_required": True,
    "custody": "one-run only",
}
L6AP01_REPORT_SAFE_RETRY_METADATA_FIELDS = (
    "status",
    "endpoint",
    "route_audience",
    "agent",
    "scope",
    "n",
    "query_label",
    "evidence_class",
    "items_count",
    "safe_item_labels",
    "denial_reason",
    "auth_status_code",
    "guarded_counters",
)
L6AP02_DENIAL_REASON = "wrong_route_audience"
L6AP02_AUTH_STATUS_CODE = 403
L6AP02_ITEMS_COUNT = 0
L6AP02_SAFE_ITEM_LABELS: tuple[str, ...] = ()
L6AP02_REPORT_SAFE_OUTPUT_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "operation_class",
        "status",
        "blocker_classification",
        "endpoint",
        "route_audience",
        "agent",
        "scope",
        "n",
        "query_label",
        "evidence_class",
        "items_count",
        "safe_item_labels",
        "denial_reason",
        "auth_status_code",
        "partial",
        "degraded",
        "guarded_counters",
        "max_operation_count",
        "retry_operation_count",
        "second_retry_performed",
        "report_safe_metadata_only",
        "denial_before_read_required",
    }
)

L6AP03_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "operation_class",
        "status",
        "decision",
        "step3_state",
        "next_bounded_proof_lane",
        "retry_result_metadata",
        "precise_blocker",
        "usefulness_readiness_receipt_created",
        "successor_execution_rail_created",
        "source_consumption_scope",
        "residual_holds",
        "guarded_counters",
    }
)

L6AP04_TRUST_REVIEW_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "operation_class",
        "status",
        "decision",
        "reviewed_artifacts",
        "source_consumption_scope",
        "retry_receipt_metadata",
        "trust_boundary_findings",
        "rollback_stop_conditions",
        "residual_holds",
        "retry_operation_count",
        "second_retry_performed",
        "runtime_registry_or_service_activation_performed",
        "provider_prod_canary_gate_or_write_movement_performed",
        "successor_execution_rail_created",
        "guarded_counters",
    }
)

L6AP04_ROLLBACK_STOP_CONDITIONS = (
    "raw_private_source_content_or_source_path_uri_requested",
    "auth_provider_payload_secret_env_keychain_oauth_auth_file_or_credential_requested",
    "runtime_registry_provider_callback_or_service_activation_requested",
    "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested",
    "retry_operation_count_greater_than_one_or_second_retry_requested",
    "safe_denial_or_empty_retry_result_without_source_floor_reconciliation",
    "any_nonzero_guarded_counter",
)

L6AP02_FORBIDDEN_OUTPUT_FIELDS = frozenset(
    {
        "text",
        "content",
        "raw_text",
        "raw_content",
        "raw_item_text",
        "raw_source_text",
        "source_uri",
        "source_path",
        "private_path",
        "platform_raw_id",
        "auth_payload",
        "auth_value",
        "credential_value",
        "token",
        "provider_payload",
        "callback_payload",
        "runtime_registry_payload",
        "query",
        "query_text",
        "items",
        "source_labels",
    }
)
L6AP01_STOP_CONDITIONS = (
    "stale_copied_or_broadened_approval",
    "missing_issue_bound_authorization",
    "raw_private_source_or_auth_output_requested",
    "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "runtime_registry_provider_callback_or_service_activation_requested",
    "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "provider_prod_canary_atlas_gate_write_or_mutation_requested",
    "max_operation_count_not_one",
    "report_safe_metadata_only_not_true",
    "denial_before_read_not_required",
)
L6AP01_FORBIDDEN_TRUE_FLAGS = {
    "raw_output_requested": "raw_private_source_or_auth_output_requested",
    "raw_private_output_requested": "raw_private_source_or_auth_output_requested",
    "raw_source_output_requested": "raw_private_source_or_auth_output_requested",
    "source_uri_requested": "raw_private_source_or_auth_output_requested",
    "provider_payload_requested": "raw_private_source_or_auth_output_requested",
    "auth_payload_requested": "raw_private_source_or_auth_output_requested",
    "secret_read_requested": "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "env_read_requested": "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "keychain_read_requested": "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "oauth_read_requested": "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "auth_file_read_requested": "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "credential_read_requested": "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "runtime_registry_requested": "runtime_registry_provider_callback_or_service_activation_requested",
    "provider_callback_requested": "runtime_registry_provider_callback_or_service_activation_requested",
    "service_activation_requested": "runtime_registry_provider_callback_or_service_activation_requested",
    "source_discovery_requested": "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "broad_recall_requested": "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "allowed": "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "broad_allowed": "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "provider_prod_requested": "provider_prod_canary_atlas_gate_write_or_mutation_requested",
    "canary_requested": "provider_prod_canary_atlas_gate_write_or_mutation_requested",
    "gate_requested": "provider_prod_canary_atlas_gate_write_or_mutation_requested",
    "atlas_gate_requested": "provider_prod_canary_atlas_gate_write_or_mutation_requested",
    "write_requested": "provider_prod_canary_atlas_gate_write_or_mutation_requested",
    "mutation_requested": "provider_prod_canary_atlas_gate_write_or_mutation_requested",
}
L6AP01_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "status",
        "operation_class",
        "fresh_approval_source",
        "approval_receipt_comment",
        "parent_rail_created_receipt",
        "target",
        "accepted_authority",
        "approval_not_inferred_from",
        "report_safe_retry_metadata_fields",
        "denial_before_read_stop_conditions",
        "preflight_ready",
        "retry_authorized_for_l6ap02_only",
        "retry_executed",
        "guarded_counters",
    }
)
L6AP01_PREFLIGHT_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "status",
        "reasons",
        "target_metadata",
        "preflight_ready",
        "retry_executed",
        "guarded_counters",
    }
)


def build_l6ap01_fresh_binding_preflight_receipt() -> dict[str, Any]:
    """Bind the fresh approval and exact retry target without performing the retry."""

    return {
        "schema_version": L6AP01_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AP_PARENT_ISSUE,
        "rail_issue": L6AP01_RAIL_ISSUE,
        "rail_starting_source_floor": L6AP_RAIL_STARTING_SOURCE_FLOOR,
        "status": L6AP01_STATUS,
        "operation_class": L6AP01_OPERATION_CLASS,
        "fresh_approval_source": L6AP_FRESH_APPROVAL_SOURCE,
        "approval_receipt_comment": L6AP01_APPROVAL_RECEIPT_COMMENT,
        "parent_rail_created_receipt": L6AP_PARENT_RAIL_CREATED_RECEIPT,
        "target": dict(L6AP01_TARGET),
        "accepted_authority": {
            "fresh_exact_non_secret_binding_approval": True,
            "explicit_issue_bound_max_one_retry_authorization": True,
            "source_floor_bound": L6AP_RAIL_STARTING_SOURCE_FLOOR,
            "custody": "one-run only",
            "max_operation_count": 1,
            "next_execution_issue_only": 391,
        },
        "approval_not_inferred_from": [
            "stale copied approval text",
            "broadened approval language",
            "parent rail-created receipt alone",
            "issue closure",
            "PR merge",
            "broad allowed=true language",
        ],
        "report_safe_retry_metadata_fields": list(L6AP01_REPORT_SAFE_RETRY_METADATA_FIELDS),
        "denial_before_read_stop_conditions": list(L6AP01_STOP_CONDITIONS),
        "preflight_ready": True,
        "retry_authorized_for_l6ap02_only": True,
        "retry_executed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def evaluate_l6ap01_max_one_retry_preflight(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Evaluate a proposed L6AP retry request and refuse unsafe shapes before read."""

    if not isinstance(candidate, Mapping):
        candidate = {}

    reasons: list[str] = []
    target = dict(L6AP01_TARGET)

    if candidate.get("fresh_approval_source") != L6AP_FRESH_APPROVAL_SOURCE:
        reasons.append("stale_copied_or_broadened_approval")
    if candidate.get("approval_fresh") is False or candidate.get("approval_state") in {"stale", "copied", "broadened", "expired", "revoked"}:
        reasons.append("stale_copied_or_broadened_approval")
    if candidate.get("issue_bound_authorization") is not True:
        reasons.append("missing_issue_bound_authorization")
    if candidate.get("authorization_issue") not in {L6AP01_RAIL_ISSUE, 391}:
        reasons.append("missing_issue_bound_authorization")

    for field, expected in target.items():
        if field in candidate and candidate.get(field) != expected:
            reasons.append(f"wrong_{field}")
    if candidate.get("query") not in {None, target["query_text"]}:
        reasons.append("wrong_query")
    if candidate.get("max_operation_count", target["max_operation_count"]) != 1:
        reasons.append("max_operation_count_not_one")
    if candidate.get("operation_count", 0) > 1:
        reasons.append("max_operation_count_not_one")
    if candidate.get("report_safe_metadata_only", target["report_safe_metadata_only"]) is not True:
        reasons.append("report_safe_metadata_only_not_true")
    if candidate.get("denial_before_read_required", target["denial_before_read_required"]) is not True:
        reasons.append("denial_before_read_not_required")

    for flag, reason in L6AP01_FORBIDDEN_TRUE_FLAGS.items():
        if candidate.get(flag) is True:
            reasons.append(reason)

    ready = not reasons
    return {
        "schema_version": L6AP01_SCHEMA_VERSION,
        "rail_issue": L6AP01_RAIL_ISSUE,
        "status": L6AP01_STATUS if ready else L6AP01_REFUSED_STATUS,
        "reasons": sorted(set(reasons or ["exact_fresh_issue_bound_max_one_preflight_ready"])),
        "target_metadata": {
            key: target[key]
            for key in (
                "endpoint",
                "route_audience",
                "agent",
                "scope",
                "n",
                "query_label",
                "evidence_class",
                "max_operation_count",
                "report_safe_metadata_only",
                "denial_before_read_required",
            )
        },
        "preflight_ready": ready,
        "retry_executed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ap01_receipt_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AP01_RECEIPT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AP.01 receipt fields present: {sorted(unexpected)}")
    if receipt.get("status") != L6AP01_STATUS:
        raise AssertionError("L6AP.01 receipt must mark preflight ready")
    target = receipt.get("target")
    if not isinstance(target, Mapping) or target != L6AP01_TARGET:
        raise AssertionError("L6AP.01 target must bind the exact approved retry metadata")
    if receipt.get("retry_executed") is not False:
        raise AssertionError("L6AP.01 must not execute the retry")
    fields = receipt.get("report_safe_retry_metadata_fields")
    if not isinstance(fields, list):
        raise AssertionError("report-safe retry metadata fields must be listed")
    forbidden = {"raw", "private", "source_uri", "auth_payload", "provider_payload", "secret", "credential"}
    if any(any(token in field for token in forbidden) for field in fields):
        raise AssertionError("L6AP.01 retry metadata fields must exclude raw/private/source/auth/secret content")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AP.01")


def assert_l6ap01_preflight_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AP01_PREFLIGHT_RECEIPT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AP.01 preflight fields present: {sorted(unexpected)}")
    if receipt.get("retry_executed") is not False:
        raise AssertionError("L6AP.01 preflight evaluation cannot execute retry")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AP.01 preflight")


def build_l6ap02_safe_denial_receipt() -> dict[str, Any]:
    """Return report-safe metadata from the one authorized L6AP.02 recall attempt."""

    return {
        "schema_version": L6AP02_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AP_PARENT_ISSUE,
        "rail_issue": L6AP02_RAIL_ISSUE,
        "rail_starting_source_floor": L6AP_RAIL_STARTING_SOURCE_FLOOR,
        "operation_class": L6AP02_OPERATION_CLASS,
        "status": L6AP02_STATUS,
        "blocker_classification": L6AP02_BLOCKER_CLASSIFICATION,
        "endpoint": L6AP01_TARGET["endpoint"],
        "route_audience": L6AP01_TARGET["route_audience"],
        "agent": L6AP01_TARGET["agent"],
        "scope": L6AP01_TARGET["scope"],
        "n": L6AP01_TARGET["n"],
        "query_label": L6AP01_QUERY_LABEL,
        "evidence_class": L6AP01_EVIDENCE_CLASS,
        "items_count": L6AP02_ITEMS_COUNT,
        "safe_item_labels": list(L6AP02_SAFE_ITEM_LABELS),
        "denial_reason": L6AP02_DENIAL_REASON,
        "auth_status_code": L6AP02_AUTH_STATUS_CODE,
        "partial": True,
        "degraded": True,
        "guarded_counters": zero_l6al03_guarded_counters(),
        "max_operation_count": 1,
        "retry_operation_count": 1,
        "second_retry_performed": False,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
    }


def assert_l6ap02_receipt_report_safe(receipt: Mapping[str, Any]) -> None:
    forbidden = L6AP02_FORBIDDEN_OUTPUT_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AP.02 report fields present: {sorted(forbidden)}")

    unexpected = set(receipt.keys()).difference(L6AP02_REPORT_SAFE_OUTPUT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AP.02 report fields present: {sorted(unexpected)}")

    if receipt.get("status") != L6AP02_STATUS:
        raise AssertionError("L6AP.02 receipt must capture the safe-denial retry result")
    if receipt.get("endpoint") != L6AP01_TARGET["endpoint"]:
        raise AssertionError("L6AP.02 receipt must name only the approved endpoint metadata")
    if receipt.get("route_audience") != L6AP01_TARGET["route_audience"]:
        raise AssertionError("L6AP.02 receipt must preserve the approved route audience label")
    if receipt.get("auth_status_code") != L6AP02_AUTH_STATUS_CODE:
        raise AssertionError("L6AP.02 receipt must preserve the safe auth status code")
    if receipt.get("denial_reason") != L6AP02_DENIAL_REASON:
        raise AssertionError("L6AP.02 receipt must classify the denial before read")
    if receipt.get("items_count") != 0:
        raise AssertionError("L6AP.02 safe-denial receipt must have zero items")
    if receipt.get("safe_item_labels") != []:
        raise AssertionError("L6AP.02 safe-denial receipt must not contain item labels")
    if receipt.get("retry_operation_count") != 1 or receipt.get("second_retry_performed") is not False:
        raise AssertionError("L6AP.02 receipt must prove exactly one retry and no second retry")
    if receipt.get("report_safe_metadata_only") is not True:
        raise AssertionError("L6AP.02 receipt must remain metadata-only")
    if receipt.get("denial_before_read_required") is not True:
        raise AssertionError("L6AP.02 receipt must keep denial-before-read required")

    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero after L6AP.02 denial-before-read")


def exact_l6ap02_retry_binding() -> dict[str, Any]:
    """Expose the exact report-safe retry binding without source-bearing payload fields."""

    return {
        "tool": L6AP01_TARGET["endpoint"],
        "route_audience": L6AP01_TARGET["route_audience"],
        "agent": L6AP01_TARGET["agent"],
        "scope": L6AP01_TARGET["scope"],
        "n": L6AP01_TARGET["n"],
        "query_label": L6AP01_QUERY_LABEL,
        "evidence_class": L6AP01_EVIDENCE_CLASS,
        "max_operation_count": 1,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
    }

def build_l6ap03_post_retry_step3_decision() -> dict[str, Any]:
    """Decide Step 3 from the committed L6AP.02 report-safe retry metadata only."""

    retry = build_l6ap02_safe_denial_receipt()
    retry_metadata = {
        "status": retry["status"],
        "endpoint": retry["endpoint"],
        "route_audience": retry["route_audience"],
        "agent": retry["agent"],
        "scope": retry["scope"],
        "n": retry["n"],
        "query_label": retry["query_label"],
        "evidence_class": retry["evidence_class"],
        "items_count": retry["items_count"],
        "safe_item_labels": retry["safe_item_labels"],
        "denial_reason": retry["denial_reason"],
        "auth_status_code": retry["auth_status_code"],
        "retry_operation_count": retry["retry_operation_count"],
        "second_retry_performed": retry["second_retry_performed"],
        "guarded_counters": retry["guarded_counters"],
    }
    return {
        "schema_version": L6AP03_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AP_PARENT_ISSUE,
        "rail_issue": L6AP03_RAIL_ISSUE,
        "rail_starting_source_floor": L6AP_RAIL_STARTING_SOURCE_FLOOR,
        "operation_class": L6AP03_OPERATION_CLASS,
        "status": L6AP03_STATUS,
        "decision": L6AP03_DECISION,
        "step3_state": L6AP03_STEP3_STATE,
        "next_bounded_proof_lane": L6AP03_NEXT_BOUNDED_PROOF_LANE,
        "retry_result_metadata": retry_metadata,
        "precise_blocker": L6AP02_BLOCKER_CLASSIFICATION,
        "usefulness_readiness_receipt_created": False,
        "successor_execution_rail_created": False,
        "source_consumption_scope": [
            "committed L6AP docs/tests/module metadata",
            "public issue and PR metadata only",
            "L6AP.02 report-safe retry receipt metadata only",
        ],
        "residual_holds": [
            "Step 3 current-session usefulness remains held until safe metadata items or labels return",
            "no successor execution rail from denied or empty retry momentum",
            "no second retry",
            "no raw/private/source/auth/provider/callback output",
            "no source discovery or broad recall",
            "no provider/prod/canary/Gate/write movement",
            "no Runtime Registry/provider callback/service activation",
            "no broad allowed=true behavior",
        ],
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ap03_decision_report_safe(decision: Mapping[str, Any]) -> None:
    forbidden = L6AP02_FORBIDDEN_OUTPUT_FIELDS.intersection(decision.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AP.03 report fields present: {sorted(forbidden)}")

    unexpected = set(decision.keys()).difference(L6AP03_REPORT_SAFE_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AP.03 report fields present: {sorted(unexpected)}")

    if decision.get("status") != L6AP03_STATUS:
        raise AssertionError("L6AP.03 must keep Step 3 held after denied/empty metadata")
    if decision.get("decision") != L6AP03_DECISION:
        raise AssertionError("L6AP.03 must not create a successor execution rail from momentum")
    if decision.get("usefulness_readiness_receipt_created") is not False:
        raise AssertionError("L6AP.03 cannot claim usefulness readiness without safe metadata items/labels")
    if decision.get("successor_execution_rail_created") is not False:
        raise AssertionError("L6AP.03 cannot create successor execution rails")

    retry_metadata = decision.get("retry_result_metadata")
    if not isinstance(retry_metadata, Mapping):
        raise AssertionError("retry metadata must be a report-safe mapping")
    if retry_metadata.get("items_count") != 0 or retry_metadata.get("safe_item_labels") != []:
        raise AssertionError("L6AP.03 denied/empty branch requires zero items and no safe labels")
    if retry_metadata.get("denial_reason") != L6AP02_DENIAL_REASON:
        raise AssertionError("L6AP.03 must name the precise denial blocker")
    if retry_metadata.get("auth_status_code") != L6AP02_AUTH_STATUS_CODE:
        raise AssertionError("L6AP.03 must preserve the safe denial status code")
    if retry_metadata.get("retry_operation_count") != 1 or retry_metadata.get("second_retry_performed") is not False:
        raise AssertionError("L6AP.03 must consume exactly one retry and prove no second retry")

    counters = decision.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("L6AP.03 decision must keep guarded counters zero")
    retry_counters = retry_metadata.get("guarded_counters")
    if not isinstance(retry_counters, Mapping) or any(value != 0 for value in retry_counters.values()):
        raise AssertionError("L6AP.03 retry metadata must carry zero guarded counters")


def build_l6ap04_trust_boundary_review() -> dict[str, Any]:
    """Review the L6AP max-one retry rail using report-safe committed/public metadata only."""

    retry = build_l6ap02_safe_denial_receipt()
    retry_metadata = {
        "status": retry["status"],
        "endpoint": retry["endpoint"],
        "route_audience": retry["route_audience"],
        "agent": retry["agent"],
        "scope": retry["scope"],
        "n": retry["n"],
        "query_label": retry["query_label"],
        "evidence_class": retry["evidence_class"],
        "items_count": retry["items_count"],
        "safe_item_labels": retry["safe_item_labels"],
        "denial_reason": retry["denial_reason"],
        "auth_status_code": retry["auth_status_code"],
        "retry_operation_count": retry["retry_operation_count"],
        "second_retry_performed": retry["second_retry_performed"],
        "guarded_counters": retry["guarded_counters"],
    }
    return {
        "schema_version": L6AP04_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AP_PARENT_ISSUE,
        "rail_issue": L6AP04_RAIL_ISSUE,
        "rail_starting_source_floor": L6AP_RAIL_STARTING_SOURCE_FLOOR,
        "operation_class": L6AP04_OPERATION_CLASS,
        "status": L6AP04_STATUS,
        "decision": L6AP04_DECISION,
        "reviewed_artifacts": [
            "#390 L6AP.01 fresh binding approval and max-one retry preflight",
            "#391 L6AP.02 supervised metadata retry safe-denial receipt",
            "#392 L6AP.03 post-retry Step 3 usefulness decision",
        ],
        "source_consumption_scope": [
            "committed L6AP docs/tests/module metadata",
            "public issue and PR metadata only",
            "L6AP.02 report-safe retry receipt metadata only",
        ],
        "retry_receipt_metadata": retry_metadata,
        "trust_boundary_findings": {
            "raw_private_source_content_or_source_path_uri_present": False,
            "auth_provider_payload_secret_env_keychain_oauth_auth_file_or_credential_present": False,
            "runtime_registry_provider_callback_or_service_activation_present": False,
            "source_discovery_broad_recall_or_broad_allowed_true_present": False,
            "provider_prod_canary_gate_atlas_gate_write_or_mutation_present": False,
            "exactly_one_retry_performed": True,
            "denied_before_read_with_zero_items": True,
            "step3_usefulness_remains_held": True,
            "next_lane_limited_to_source_floor_reconciliation": True,
        },
        "rollback_stop_conditions": list(L6AP04_ROLLBACK_STOP_CONDITIONS),
        "residual_holds": [
            "Step 3 current-session usefulness remains held until safe metadata items or labels return",
            "no successor execution rail from denied or empty retry momentum",
            "no second retry",
            "no raw/private/source/auth/provider/callback output",
            "no source paths or URIs",
            "no secret/env/keychain/OAuth/auth-file/credential reads",
            "no source discovery or broad recall",
            "no Runtime Registry/provider callback/service activation",
            "no provider/prod/canary/Gate/write movement",
            "no broad allowed=true behavior",
        ],
        "retry_operation_count": 1,
        "second_retry_performed": False,
        "runtime_registry_or_service_activation_performed": False,
        "provider_prod_canary_gate_or_write_movement_performed": False,
        "successor_execution_rail_created": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ap04_trust_review_report_safe(review: Mapping[str, Any]) -> None:
    forbidden = L6AP02_FORBIDDEN_OUTPUT_FIELDS.intersection(review.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AP.04 report fields present: {sorted(forbidden)}")

    unexpected = set(review.keys()).difference(L6AP04_TRUST_REVIEW_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AP.04 report fields present: {sorted(unexpected)}")
    if review.get("status") != L6AP04_STATUS:
        raise AssertionError("L6AP.04 must pass only the bounded trust-boundary review")
    if review.get("retry_operation_count") != 1 or review.get("second_retry_performed") is not False:
        raise AssertionError("L6AP.04 must prove exactly one retry and no second retry")
    if review.get("successor_execution_rail_created") is not False:
        raise AssertionError("L6AP.04 cannot create successor execution rails")
    if review.get("runtime_registry_or_service_activation_performed") is not False:
        raise AssertionError("L6AP.04 cannot activate Runtime Registry or services")
    if review.get("provider_prod_canary_gate_or_write_movement_performed") is not False:
        raise AssertionError("L6AP.04 cannot move provider/prod/canary/Gate/write surfaces")

    findings = review.get("trust_boundary_findings")
    if not isinstance(findings, Mapping):
        raise AssertionError("trust-boundary findings must be a mapping")
    false_required = {
        "raw_private_source_content_or_source_path_uri_present",
        "auth_provider_payload_secret_env_keychain_oauth_auth_file_or_credential_present",
        "runtime_registry_provider_callback_or_service_activation_present",
        "source_discovery_broad_recall_or_broad_allowed_true_present",
        "provider_prod_canary_gate_atlas_gate_write_or_mutation_present",
    }
    unsafe_true = [key for key in false_required if findings.get(key) is not False]
    if unsafe_true:
        raise AssertionError(f"L6AP.04 unsafe boundary findings present: {unsafe_true}")
    true_required = {
        "exactly_one_retry_performed",
        "denied_before_read_with_zero_items",
        "step3_usefulness_remains_held",
        "next_lane_limited_to_source_floor_reconciliation",
    }
    missing_true = [key for key in true_required if findings.get(key) is not True]
    if missing_true:
        raise AssertionError(f"L6AP.04 required safe findings missing: {missing_true}")

    retry_metadata = review.get("retry_receipt_metadata")
    if not isinstance(retry_metadata, Mapping):
        raise AssertionError("retry receipt metadata must be a report-safe mapping")
    if retry_metadata.get("items_count") != 0 or retry_metadata.get("safe_item_labels") != []:
        raise AssertionError("L6AP.04 denied-before-read review requires zero items and no safe labels")
    if retry_metadata.get("denial_reason") != L6AP02_DENIAL_REASON:
        raise AssertionError("L6AP.04 must name the precise denial blocker")
    if retry_metadata.get("auth_status_code") != L6AP02_AUTH_STATUS_CODE:
        raise AssertionError("L6AP.04 must preserve the safe denial status code")
    if retry_metadata.get("retry_operation_count") != 1 or retry_metadata.get("second_retry_performed") is not False:
        raise AssertionError("L6AP.04 retry metadata must prove exactly one retry")

    counters = review.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("L6AP.04 review must keep guarded counters zero")
    retry_counters = retry_metadata.get("guarded_counters")
    if not isinstance(retry_counters, Mapping) or any(value != 0 for value in retry_counters.values()):
        raise AssertionError("L6AP.04 retry metadata must carry zero guarded counters")


L6AP05_SCHEMA_VERSION = "l6ap05-source-floor-parent-tracker-reconciliation-v1"
L6AP05_RAIL_ISSUE = 394
L6AP05_STATUS = "SOURCE_FLOOR_PARENT_TRACKER_RECONCILED_METADATA_RETRY_RAIL_COMPLETE_STEP3_HELD"
L6AP05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR = "87c1f917eb48b77e19257dd4f8e6dd3740f13be4"
L6AP05_RAIL_ANCHORS = (
    {
        "issue": 390,
        "pr": 395,
        "merge_commit": "55ee79090eea1ac62bdc6dc3760e6f8c28fb55bf",
        "artifact": "L6AP.01 fresh binding approval and max-one retry preflight",
    },
    {
        "issue": 391,
        "pr": 396,
        "merge_commit": "e5efaa1a61cca0573c5ce5c6a325f15de14e9ca7",
        "artifact": "L6AP.02 supervised metadata retry safe-denial receipt",
    },
    {
        "issue": 392,
        "pr": 397,
        "merge_commit": "e19be48cd1e2085f4af9deff9bfd0912dd043f2a",
        "artifact": "L6AP.03 post-retry Step 3 usefulness decision",
    },
    {
        "issue": 393,
        "pr": 398,
        "merge_commit": L6AP05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR,
        "artifact": "L6AP.04 trust-boundary review",
    },
)
L6AP05_PARENT_RECEIPT_TEXT = (
    "Parent #6 receipt: L6AP max-one metadata retry rail complete through source-floor "
    "reconciliation. Issues #390-#394 and PRs #395-#399 record fresh binding preflight, "
    "one report-safe supervised metadata retry, denied-before-read safe metadata, Step 3 "
    "usefulness held, trust-boundary PASS, and final reconciliation. Retry summary: "
    "memory_seam_recall / memory-seam:read:recall / sax / wiki / n=3 / "
    "supervised_metadata_readiness / SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE returned "
    "auth_status_code=403, denial_reason=wrong_route_audience, items_count=0, "
    "safe_item_labels=[], retry_operation_count=1, second_retry_performed=false, no second "
    "retry, guarded counters zero. Step 3 remains held; no successor execution rail, no external tracker "
    "write, no cron mutation, no provider/prod/canary/Gate/write movement, and no broad "
    "allowed=true behavior occurred."
)
L6AP05_TRACKER_UPDATE_TEXT = (
    "Atlas tracker update text: mark Memory Seam roadmap Step 3 as METADATA RETRY "
    "ATTEMPTED / DENIED-BEFORE-READ / USEFULNESS HELD at source floor "
    "87c1f917eb48b77e19257dd4f8e6dd3740f13be4; record #390-#394 and PR #395-#399 "
    "as the L6AP max-one metadata retry rail. Record retry metadata only: endpoint "
    "memory_seam_recall, route audience memory-seam:read:recall, agent sax, scope wiki, "
    "n=3, query_label supervised_metadata_readiness, evidence_class "
    "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE, denial_reason wrong_route_audience, "
    "auth_status_code 403, items_count 0, safe_item_labels empty, retry count 1, no "
    "second retry, guarded counters zero. Next frontier is service route-audience auth "
    "binding repair or operator/service configuration proof before any newly authorized "
    "retry; writer performed no external tracker write and no cron mutation."
)
L6AP05_RESIDUAL_HOLDS = (
    "step3_current_session_usefulness",
    "successor_execution_rail",
    "second_retry",
    "raw_private_source_content_or_source_path_uri",
    "auth_provider_payload_secret_env_keychain_oauth_auth_file_or_credential_reads",
    "runtime_registry_provider_callback_or_service_activation",
    "source_discovery_broad_recall_or_broad_allowed_true",
    "external_tracker_write_or_cron_mutation_from_writer",
    "provider_prod_canary_gate_atlas_gate_write_or_mutation",
)
L6AP05_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "status",
        "rail_starting_source_floor",
        "final_pre_reconciliation_source_floor",
        "rail_anchors",
        "retry_metadata_summary",
        "step3_state",
        "final_result",
        "next_frontier",
        "parent_receipt_text",
        "tracker_update_text",
        "external_tracker_written",
        "cron_mutated",
        "successor_execution_rail_created",
        "provider_prod_canary_gate_or_write_movement_performed",
        "residual_holds",
        "guarded_counters",
    }
)


def build_l6ap05_source_floor_parent_tracker_reconciliation() -> dict[str, Any]:
    """Reconcile the completed L6AP retry rail using report-safe metadata only."""

    retry = build_l6ap02_safe_denial_receipt()
    retry_metadata = {
        "status": retry["status"],
        "endpoint": retry["endpoint"],
        "route_audience": retry["route_audience"],
        "agent": retry["agent"],
        "scope": retry["scope"],
        "n": retry["n"],
        "query_label": retry["query_label"],
        "evidence_class": retry["evidence_class"],
        "items_count": retry["items_count"],
        "safe_item_labels": retry["safe_item_labels"],
        "denial_reason": retry["denial_reason"],
        "auth_status_code": retry["auth_status_code"],
        "retry_operation_count": retry["retry_operation_count"],
        "second_retry_performed": retry["second_retry_performed"],
        "guarded_counters": retry["guarded_counters"],
    }
    return {
        "schema_version": L6AP05_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AP_PARENT_ISSUE,
        "rail_issue": L6AP05_RAIL_ISSUE,
        "status": L6AP05_STATUS,
        "rail_starting_source_floor": L6AP_RAIL_STARTING_SOURCE_FLOOR,
        "final_pre_reconciliation_source_floor": L6AP05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR,
        "rail_anchors": [dict(anchor) for anchor in L6AP05_RAIL_ANCHORS],
        "retry_metadata_summary": retry_metadata,
        "step3_state": L6AP03_STEP3_STATE,
        "final_result": "metadata retry rail reconciled; Step 3 usefulness remains held",
        "next_frontier": (
            "service route-audience auth binding repair or operator/service configuration proof "
            "before any newly authorized max-one metadata retry"
        ),
        "parent_receipt_text": L6AP05_PARENT_RECEIPT_TEXT,
        "tracker_update_text": L6AP05_TRACKER_UPDATE_TEXT,
        "external_tracker_written": False,
        "cron_mutated": False,
        "successor_execution_rail_created": False,
        "provider_prod_canary_gate_or_write_movement_performed": False,
        "residual_holds": list(L6AP05_RESIDUAL_HOLDS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ap05_reconciliation_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AP05_RECEIPT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AP.05 reconciliation fields present: {sorted(unexpected)}")
    if receipt.get("status") != L6AP05_STATUS:
        raise AssertionError("L6AP.05 status must record final source-floor reconciliation")
    if receipt.get("rail_issue") != L6AP05_RAIL_ISSUE or receipt.get("parent_issue") != L6AP_PARENT_ISSUE:
        raise AssertionError("L6AP.05 must bind the final rail issue and parent issue")
    if receipt.get("rail_starting_source_floor") != L6AP_RAIL_STARTING_SOURCE_FLOOR:
        raise AssertionError("L6AP.05 must preserve the starting source floor")
    if receipt.get("final_pre_reconciliation_source_floor") != L6AP05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR:
        raise AssertionError("L6AP.05 must anchor the final pre-reconciliation source floor")
    anchors = receipt.get("rail_anchors")
    if not isinstance(anchors, list) or [anchor.get("issue") for anchor in anchors] != [390, 391, 392, 393]:
        raise AssertionError("L6AP.05 must reconcile #390-#393 in order")
    if [anchor.get("pr") for anchor in anchors] != [395, 396, 397, 398]:
        raise AssertionError("L6AP.05 must anchor PR #395-#398")

    retry_metadata = receipt.get("retry_metadata_summary")
    if not isinstance(retry_metadata, Mapping):
        raise AssertionError("L6AP.05 retry metadata summary must be a mapping")
    if retry_metadata.get("items_count") != 0 or retry_metadata.get("safe_item_labels") != []:
        raise AssertionError("L6AP.05 must preserve denied/empty retry metadata")
    if retry_metadata.get("denial_reason") != L6AP02_DENIAL_REASON:
        raise AssertionError("L6AP.05 must preserve the route-audience denial reason")
    if retry_metadata.get("auth_status_code") != L6AP02_AUTH_STATUS_CODE:
        raise AssertionError("L6AP.05 must preserve the safe auth status code")
    if retry_metadata.get("retry_operation_count") != 1 or retry_metadata.get("second_retry_performed") is not False:
        raise AssertionError("L6AP.05 must prove exactly one retry and no second retry")

    for field in (
        "external_tracker_written",
        "cron_mutated",
        "successor_execution_rail_created",
        "provider_prod_canary_gate_or_write_movement_performed",
    ):
        if receipt.get(field) is not False:
            raise AssertionError(f"L6AP.05 must keep {field}=false")
    if receipt.get("step3_state") != L6AP03_STEP3_STATE:
        raise AssertionError("L6AP.05 must keep Step 3 held after denied/empty metadata")

    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("L6AP.05 guarded counters must remain zero")
    retry_counters = retry_metadata.get("guarded_counters")
    if not isinstance(retry_counters, Mapping) or any(value != 0 for value in retry_counters.values()):
        raise AssertionError("L6AP.05 retry metadata counters must remain zero")

    forbidden = L6AP02_FORBIDDEN_OUTPUT_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AP.05 report fields present: {sorted(forbidden)}")
