from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from memory_seam.l6al_service_auth_contract import ENDPOINT_AUDIENCES, zero_l6al03_guarded_counters
from memory_seam.l6am_next_use_proof_decision import L6AM03_NEXT_FRONTIER
from memory_seam.l6am_supervised_metadata_retry_packet import (
    L6AM01_AGENT,
    L6AM01_EVIDENCE_CLASS,
    L6AM01_N,
    L6AM01_PARENT_ISSUE,
    L6AM01_QUERY_LABEL,
    L6AM01_QUERY_TEXT,
    L6AM01_REPOSITORY,
    L6AM01_SCOPE,
)
from memory_seam.l6am_supervised_metadata_retry_receipt import build_l6am02_safe_denial_receipt

L6AN01_SCHEMA_VERSION = "l6an01-service-operator-auth-binding-packet-v1"
L6AN01_RAIL_ISSUE = 370
L6AN01_RAIL_STARTING_SOURCE_FLOOR = "c7574563ac1be1bf4c9c135586338ab760c0eb28"
L6AN01_STATUS = "PASS_SERVICE_OPERATOR_AUTH_BINDING_UNBLOCK_PACKET_READY_RETRY_HELD"
L6AN01_RETRY_STATE = "HELD_MISSING_FRESH_OPERATOR_SERVICE_BINDING"
L6AN01_BINDING_PROOF_SHAPE = (
    "operator_service_binding_ref",
    "binding_owner",
    "identity_subject",
    "route_audience",
    "acting_for",
    "agent",
    "scope",
    "query_label",
    "evidence_class",
    "max_operation_count",
    "report_safe_metadata_only",
    "denial_before_read_required",
    "expires_at_or_one_run_custody",
)
L6AN01_NO_GO_SURFACES = (
    "live_retry",
    "raw_private_source_or_auth_content",
    "secret_env_keychain_oauth_auth_file_credential_read",
    "runtime_registry_consumption",
    "provider_callback_or_service_activation",
    "source_discovery_or_broad_recall",
    "write_mutation_or_persistence",
    "provider_prod_canary_gate_movement",
    "broad_allowed_true",
)
L6AN01_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "status",
        "source_blocker",
        "retry_state",
        "operation_class",
        "exact_retry_binding",
        "binding_proof_request",
        "approval_not_inferred_from",
        "safe_denial_metadata",
        "no_go_surfaces",
        "guarded_counters",
    }
)

L6AN02_SCHEMA_VERSION = "l6an02-non-secret-binding-reference-validator-v1"
L6AN02_RAIL_ISSUE = 371
L6AN02_READY_STATUS = "AUTH_BINDING_READY_RETRY_HELD"
L6AN02_HELD_STATUS = "AUTH_BINDING_HELD_BEFORE_READ"
L6AN02_DENIED_STATUS = "AUTH_BINDING_DENIED_BEFORE_READ"
L6AN02_REQUIRED_REFERENCE_FIELDS = frozenset(L6AN01_BINDING_PROOF_SHAPE)
L6AN02_REPORT_SAFE_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "status",
        "reasons",
        "ready_metadata",
        "retry_executed",
        "guarded_counters",
    }
)
L6AN02_FORBIDDEN_TRUE_FLAGS = {
    "raw_output_requested": "raw_output_requested",
    "raw_private_output_requested": "raw_output_requested",
    "broad_allowed": "broad_allowed_true",
    "provider_callback_requested": "provider_callback_requested",
    "callback_route_requested": "provider_callback_requested",
    "runtime_registry_requested": "runtime_registry_requested",
    "runtime_registry_consumption_requested": "runtime_registry_requested",
    "service_activation_requested": "service_activation_requested",
    "provider_route_activation_requested": "service_activation_requested",
}

L6AN03_SCHEMA_VERSION = "l6an03-service-owner-handoff-retry-gate-v1"
L6AN03_RAIL_ISSUE = 372
L6AN03_STATUS = "SERVICE_OWNER_HANDOFF_READY_RETRY_GATE_HELD"
L6AN03_RETRY_GATE_DECISION = "RETRY_HELD_PENDING_FRESH_EXACT_BINDING_AND_NEW_MAX_ONE_RETRY_ISSUE"
L6AN03_REQUIRED_FUTURE_EVIDENCE = (
    "fresh_issue_comment_or_service_owner_reference",
    "operator_service_binding_ref",
    "identity_subject_bound_to_sax_service_caller",
    "route_audience_memory_seam_read_recall",
    "acting_for_sax",
    "agent_sax",
    "scope_wiki",
    "query_label_supervised_metadata_readiness",
    "evidence_class_supervised_metadata_read_retry_report_safe",
    "max_operation_count_one",
    "report_safe_metadata_only_true",
    "denial_before_read_required_true",
    "expiry_or_one_run_custody",
    "explicit_new_max_one_retry_issue_authorization",
)
L6AN03_REPORT_SAFE_HANDOFF_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "parent_issue",
        "status",
        "retry_gate_decision",
        "service_owner_request",
        "required_future_evidence",
        "current_ready_receipt",
        "actual_retry_executed",
        "guarded_counters",
        "held_surfaces",
    }
)

L6AN04_SCHEMA_VERSION = "l6an04-trust-boundary-review-v1"
L6AN04_RAIL_ISSUE = 373
L6AN04_STATUS = "TRUST_BOUNDARY_REVIEW_PASS_RETRY_HELD"
L6AN04_REVIEWED_ARTIFACTS = (
    "#370 L6AN.01 service/operator auth-binding unblock packet",
    "#371 L6AN.02 non-secret binding-reference validator",
    "#372 L6AN.03 service-owner handoff retry-gate decision",
)
L6AN04_STOP_CONDITIONS = (
    "missing_fresh_exact_operator_service_binding_reference",
    "missing_explicit_new_max_one_retry_issue_authorization",
    "any_request_for_secret_env_keychain_oauth_auth_file_or_credential_material",
    "any_runtime_registry_provider_callback_or_service_activation_request",
    "any_raw_private_source_uri_payload_or_broad_allowed_true_behavior",
    "any_provider_prod_canary_gate_write_or_mutation_surface",
)
L6AN04_REPORT_SAFE_REVIEW_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "parent_issue",
        "status",
        "reviewed_artifacts",
        "boundary_findings",
        "rollback_stop_conditions",
        "retry_executed",
        "guarded_counters",
    }
)

L6AN05_SCHEMA_VERSION = "l6an05-source-floor-parent-tracker-reconciliation-v1"
L6AN05_RAIL_ISSUE = 374
L6AN05_STATUS = "SERVICE_OPERATOR_AUTH_BINDING_REQUEST_READY_RETRY_HELD"
L6AN05_TRACKER_REF = "atlas/sax/data/memory-seam-8-step-roadmap-tracker"
L6AN05_TRACKER_UPDATE_STATE = "AUTH BINDING UNBLOCK REQUEST READY / RETRY HELD"
L6AN05_FINAL_SOURCE_FLOOR_BEFORE_RECONCILIATION = "cb26336b2db1848a4bf972d97153c648158719e4"
L6AN05_NEXT_FRONTIER = (
    "L6AO exact max-one metadata retry only after fresh non-secret operator/service "
    "binding reference approval plus explicit new max-one retry issue authorization"
)
L6AN05_RAIL_EVIDENCE = (
    {"issue": 370, "pr": 375, "source_floor": "0003c66f2b45c2b5c27bc8e674bad8445893b00c", "status": L6AN01_STATUS},
    {"issue": 371, "pr": 376, "source_floor": "8972bf7a6a035d53a263f95338105d05a186cfa0", "status": L6AN02_READY_STATUS},
    {"issue": 372, "pr": 377, "source_floor": "d263ceeae15063aad83238e0d15dc51109b91e24", "status": L6AN03_STATUS},
    {"issue": 373, "pr": 378, "source_floor": L6AN05_FINAL_SOURCE_FLOOR_BEFORE_RECONCILIATION, "status": L6AN04_STATUS},
)
L6AN05_VERIFICATION = (
    "python -m pytest -q tests/test_l6an05_source_floor_parent_tracker_reconciliation.py",
    "python -m pytest -q",
    "python scripts/public_hygiene_scan.py",
    "git diff --check",
    "python -m compileall -q src tests examples",
)
L6AN05_RESIDUAL_HOLDS = (
    "no_live_private_retry",
    "no_secret_env_keychain_oauth_auth_file_credential_reads",
    "no_runtime_registry_consumption",
    "no_provider_callback_or_service_activation",
    "no_source_discovery_or_broad_recall",
    "no_write_mutation_external_systems",
    "no_provider_prod_canary_gate_or_atlas_gate_movement",
    "no_successor_issue_created_by_reconciliation",
    "no_cron_job_created_modified_removed_resumed_or_paused",
    "no_broad_allowed_true_behavior",
)
L6AN05_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "final_source_floor_before_reconciliation",
        "status",
        "service_operator_auth_binding_request_ready",
        "retry_state",
        "rail_evidence",
        "parent_completion_receipt",
        "tracker_ref",
        "tracker_update_state",
        "tracker_update_summary",
        "next_frontier",
        "verification_commands",
        "residual_holds",
        "guarded_counters",
    }
)



def build_l6an01_exact_retry_binding() -> dict[str, Any]:
    """Return the exact non-secret labels that a future binding proof must match."""

    return {
        "endpoint": "memory_seam_recall",
        "route_audience": ENDPOINT_AUDIENCES["recall"],
        "acting_for": L6AM01_AGENT,
        "agent": L6AM01_AGENT,
        "scope": L6AM01_SCOPE,
        "n": L6AM01_N,
        "query_label": L6AM01_QUERY_LABEL,
        "query_text": L6AM01_QUERY_TEXT,
        "evidence_class": L6AM01_EVIDENCE_CLASS,
        "max_operation_count": 1,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
    }


def build_l6an01_binding_proof_request() -> dict[str, Any]:
    """Name the report-safe operator/service proof required before retry can run."""

    return {
        "required_shape": list(L6AN01_BINDING_PROOF_SHAPE),
        "operator_service_binding_ref_required": True,
        "expiry_or_one_run_custody_required": True,
        "identity_subject_required": "supervised service caller bound to sax",
        "must_match": build_l6an01_exact_retry_binding(),
        "fresh_issue_bound_owner_or_service_owner_approval_required": True,
        "may_contain_secret_material": False,
        "retry_authorized_by_packet": False,
    }


def build_l6an02_exact_binding_reference_fixture() -> dict[str, Any]:
    """Return a non-secret fixture that satisfies the L6AN.01 proof shape."""

    exact = build_l6an01_exact_retry_binding()
    return {
        "operator_service_binding_ref": "operator-service-binding:l6an02:report-safe-metadata-recall:max-one",
        "binding_owner": "service-owner-or-operator",
        "identity_subject": "supervised service caller bound to sax",
        "route_audience": exact["route_audience"],
        "acting_for": exact["acting_for"],
        "agent": exact["agent"],
        "scope": exact["scope"],
        "query_label": exact["query_label"],
        "evidence_class": exact["evidence_class"],
        "max_operation_count": exact["max_operation_count"],
        "report_safe_metadata_only": exact["report_safe_metadata_only"],
        "denial_before_read_required": exact["denial_before_read_required"],
        "expires_at_or_one_run_custody": "one-run-custody:l6an02:max-one-retry-held",
    }


def validate_l6an02_binding_reference(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Validate report-safe binding metadata without runtime or credential access."""

    reasons: list[str] = []
    status = L6AN02_READY_STATUS
    if not isinstance(candidate, Mapping):
        candidate = {}

    missing = sorted(field for field in L6AN02_REQUIRED_REFERENCE_FIELDS if not candidate.get(field))
    if missing:
        reasons.append("missing_or_stale_operator_service_binding_ref")
        status = L6AN02_HELD_STATUS

    expiry = candidate.get("expires_at_or_one_run_custody")
    if expiry in {"expired", "stale", "revoked"} or candidate.get("binding_fresh") is False:
        reasons.append("missing_or_stale_operator_service_binding_ref")
        status = L6AN02_HELD_STATUS

    exact = build_l6an01_exact_retry_binding()
    for field in (
        "route_audience",
        "acting_for",
        "agent",
        "scope",
        "query_label",
        "evidence_class",
        "max_operation_count",
        "report_safe_metadata_only",
        "denial_before_read_required",
    ):
        if field in candidate and candidate.get(field) != exact[field]:
            reasons.append(f"wrong_{field}")
            status = L6AN02_DENIED_STATUS

    for flag, reason in L6AN02_FORBIDDEN_TRUE_FLAGS.items():
        if candidate.get(flag) is True:
            reasons.append(reason)
            status = L6AN02_DENIED_STATUS

    if candidate.get("allowed") is True:
        reasons.append("broad_allowed_true")
        status = L6AN02_DENIED_STATUS

    if not reasons:
        reasons.append("exact_non_secret_binding_reference_present_retry_still_held")

    ready_metadata = {
        "operator_service_binding_ref_present": bool(candidate.get("operator_service_binding_ref")),
        "route_audience": candidate.get("route_audience"),
        "acting_for": candidate.get("acting_for"),
        "agent": candidate.get("agent"),
        "scope": candidate.get("scope"),
        "query_label": candidate.get("query_label"),
        "evidence_class": candidate.get("evidence_class"),
        "max_operation_count": candidate.get("max_operation_count"),
        "report_safe_metadata_only": candidate.get("report_safe_metadata_only"),
        "denial_before_read_required": candidate.get("denial_before_read_required"),
        "expiry_or_one_run_custody_present": bool(candidate.get("expires_at_or_one_run_custody")),
    }
    return {
        "schema_version": L6AN02_SCHEMA_VERSION,
        "rail_issue": L6AN02_RAIL_ISSUE,
        "status": status,
        "reasons": sorted(set(reasons)),
        "ready_metadata": ready_metadata,
        "retry_executed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6an02_receipt_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AN02_REPORT_SAFE_RECEIPT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AN.02 receipt fields present: {sorted(unexpected)}")
    if receipt.get("retry_executed") is not False:
        raise AssertionError("L6AN.02 validator cannot execute or authorize retry")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for pure binding validation")


def build_l6an03_service_owner_handoff_receipt(
    binding_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a report-safe service-owner handoff and retry-gate decision."""

    candidate = binding_reference if binding_reference is not None else build_l6an02_exact_binding_reference_fixture()
    current_ready_receipt = validate_l6an02_binding_reference(candidate)
    return {
        "schema_version": L6AN03_SCHEMA_VERSION,
        "rail_issue": L6AN03_RAIL_ISSUE,
        "parent_issue": L6AM01_PARENT_ISSUE,
        "status": L6AN03_STATUS,
        "retry_gate_decision": L6AN03_RETRY_GATE_DECISION,
        "service_owner_request": {
            "request_class": "exact_non_secret_service_operator_binding_for_future_l6ao_retry",
            "may_include_secret_material": False,
            "runtime_or_provider_inspection_requested": False,
            "live_retry_requested": False,
            "new_successor_issue_requested": False,
            "must_match": build_l6an01_exact_retry_binding(),
        },
        "required_future_evidence": list(L6AN03_REQUIRED_FUTURE_EVIDENCE),
        "current_ready_receipt": current_ready_receipt,
        "actual_retry_executed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
        "held_surfaces": list(L6AN01_NO_GO_SURFACES),
    }


def assert_l6an03_handoff_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AN03_REPORT_SAFE_HANDOFF_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AN.03 handoff fields present: {sorted(unexpected)}")
    if receipt.get("actual_retry_executed") is not False:
        raise AssertionError("L6AN.03 handoff cannot execute or authorize retry")
    if receipt.get("retry_gate_decision") != L6AN03_RETRY_GATE_DECISION:
        raise AssertionError("L6AN.03 retry gate must remain held")
    request = receipt.get("service_owner_request")
    if not isinstance(request, Mapping):
        raise AssertionError("service-owner request must be report-safe metadata")
    if request.get("may_include_secret_material") is not False:
        raise AssertionError("service-owner handoff may ask only for non-secret references")
    if request.get("runtime_or_provider_inspection_requested") is not False:
        raise AssertionError("service-owner handoff must not inspect runtime or provider state")
    assert_l6an02_receipt_report_safe(receipt.get("current_ready_receipt", {}))
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AN.03 handoff")


def build_l6an04_trust_boundary_review() -> dict[str, Any]:
    """Review L6AN.01-L6AN.03 as report-safe artifacts without external access."""

    packet = build_l6an01_service_operator_auth_binding_packet()
    validator_receipt = validate_l6an02_binding_reference(build_l6an02_exact_binding_reference_fixture())
    handoff = build_l6an03_service_owner_handoff_receipt()
    assert_l6an01_packet_report_safe(packet)
    assert_l6an02_receipt_report_safe(validator_receipt)
    assert_l6an03_handoff_report_safe(handoff)

    return {
        "schema_version": L6AN04_SCHEMA_VERSION,
        "rail_issue": L6AN04_RAIL_ISSUE,
        "parent_issue": L6AM01_PARENT_ISSUE,
        "status": L6AN04_STATUS,
        "reviewed_artifacts": list(L6AN04_REVIEWED_ARTIFACTS),
        "boundary_findings": {
            "secret_like_material_present": False,
            "raw_private_data_present": False,
            "source_uri_or_provider_payload_present": False,
            "runtime_registry_payload_present": False,
            "auth_file_material_present": False,
            "broad_allowed_true_behavior_present": False,
            "usable_service_operator_handoff_present": True,
            "retry_remains_held": True,
        },
        "rollback_stop_conditions": list(L6AN04_STOP_CONDITIONS),
        "retry_executed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6an04_review_report_safe(review: Mapping[str, Any]) -> None:
    unexpected = set(review.keys()).difference(L6AN04_REPORT_SAFE_REVIEW_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AN.04 review fields present: {sorted(unexpected)}")
    if review.get("retry_executed") is not False:
        raise AssertionError("L6AN.04 review cannot execute retry")
    findings = review.get("boundary_findings")
    if not isinstance(findings, Mapping):
        raise AssertionError("L6AN.04 findings must be report-safe metadata")
    for forbidden in (
        "secret_like_material_present",
        "raw_private_data_present",
        "source_uri_or_provider_payload_present",
        "runtime_registry_payload_present",
        "auth_file_material_present",
        "broad_allowed_true_behavior_present",
    ):
        if findings.get(forbidden) is not False:
            raise AssertionError(f"L6AN.04 forbidden finding must remain false: {forbidden}")
    if findings.get("retry_remains_held") is not True:
        raise AssertionError("L6AN.04 review must keep retry held")
    counters = review.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AN.04 review")


def build_l6an05_source_floor_parent_tracker_reconciliation() -> dict[str, Any]:
    """Reconcile the L6AN auth-binding unblock rail without executing a retry."""

    trust_review = build_l6an04_trust_boundary_review()
    assert_l6an04_review_report_safe(trust_review)
    return {
        "schema_version": L6AN05_SCHEMA_VERSION,
        "repo": L6AM01_REPOSITORY,
        "parent_issue": L6AM01_PARENT_ISSUE,
        "rail_issue": L6AN05_RAIL_ISSUE,
        "rail_starting_source_floor": L6AN01_RAIL_STARTING_SOURCE_FLOOR,
        "final_source_floor_before_reconciliation": L6AN05_FINAL_SOURCE_FLOOR_BEFORE_RECONCILIATION,
        "status": L6AN05_STATUS,
        "service_operator_auth_binding_request_ready": True,
        "retry_state": "HELD_UNLESS_FRESH_EXACT_BINDING_APPROVAL_AND_NEW_MAX_ONE_RETRY_ISSUE_EXIST",
        "rail_evidence": [dict(item) for item in L6AN05_RAIL_EVIDENCE],
        "parent_completion_receipt": (
            "L6AN complete: #370-#374 produced a report-safe service/operator auth-binding "
            "request for exact metadata recall. Service/operator auth-binding request is ready; "
            "retry remains held unless exact fresh binding approval exists and explicitly authorizes "
            "a new max-one retry issue."
        ),
        "tracker_ref": L6AN05_TRACKER_REF,
        "tracker_update_state": L6AN05_TRACKER_UPDATE_STATE,
        "tracker_update_summary": (
            "Step 3 becomes AUTH BINDING UNBLOCK REQUEST READY / RETRY HELD after L6AN #370-#374; "
            "current-session usefulness and fresh-agent proof remain held until exact metadata labels/items return."
        ),
        "next_frontier": L6AN05_NEXT_FRONTIER,
        "verification_commands": list(L6AN05_VERIFICATION),
        "residual_holds": list(L6AN05_RESIDUAL_HOLDS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6an05_reconciliation_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AN05_REPORT_SAFE_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AN.05 reconciliation fields present: {sorted(unexpected)}")
    if receipt.get("status") != L6AN05_STATUS:
        raise AssertionError("L6AN.05 status must mark auth-binding request ready and retry held")
    if receipt.get("service_operator_auth_binding_request_ready") is not True:
        raise AssertionError("service/operator auth-binding request must be marked ready")
    if "HELD" not in str(receipt.get("retry_state")):
        raise AssertionError("retry must remain held after reconciliation")
    if receipt.get("tracker_update_state") != L6AN05_TRACKER_UPDATE_STATE:
        raise AssertionError("tracker update state must be pinned to auth-binding unblock ready / retry held")
    if receipt.get("next_frontier") != L6AN05_NEXT_FRONTIER:
        raise AssertionError("next frontier must be exact L6AO max-one retry after fresh binding approval")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AN.05 reconciliation")


def build_l6an01_service_operator_auth_binding_packet() -> dict[str, Any]:
    safe_denial = build_l6am02_safe_denial_receipt()
    safe_denial_metadata = {
        "endpoint": safe_denial["endpoint"],
        "auth_status": safe_denial["auth_status"],
        "auth_status_code": safe_denial["auth_status_code"],
        "degraded_reasons": safe_denial["degraded_reasons"],
        "item_count": safe_denial["item_count"],
        "safe_item_labels": safe_denial["safe_item_labels"],
    }
    return {
        "schema_version": L6AN01_SCHEMA_VERSION,
        "repo": L6AM01_REPOSITORY,
        "parent_issue": L6AM01_PARENT_ISSUE,
        "rail_issue": L6AN01_RAIL_ISSUE,
        "rail_starting_source_floor": L6AN01_RAIL_STARTING_SOURCE_FLOOR,
        "status": L6AN01_STATUS,
        "source_blocker": "L6AM safe denial: auth_status_code=403 wrong_route_audience items=0",
        "retry_state": L6AN01_RETRY_STATE,
        "operation_class": L6AM03_NEXT_FRONTIER,
        "exact_retry_binding": build_l6an01_exact_retry_binding(),
        "binding_proof_request": build_l6an01_binding_proof_request(),
        "approval_not_inferred_from": [
            "parent successor receipt #6 comment 4656321058",
            "issue-bound preauth comment #370 4656320851",
            "packet merge",
            "PR merge",
            "issue closure",
            "stale or copied comments",
            "broad keep-going language",
        ],
        "safe_denial_metadata": safe_denial_metadata,
        "no_go_surfaces": list(L6AN01_NO_GO_SURFACES),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6an01_packet_report_safe(packet: Mapping[str, Any]) -> None:
    unexpected = set(packet.keys()).difference(L6AN01_REPORT_SAFE_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected report fields present: {sorted(unexpected)}")
    if packet.get("retry_state") != L6AN01_RETRY_STATE:
        raise AssertionError("retry must remain held until a fresh exact binding proof appears")
    proof = packet.get("binding_proof_request")
    if not isinstance(proof, Mapping):
        raise AssertionError("binding proof request must be report-safe metadata")
    if proof.get("retry_authorized_by_packet") is not False:
        raise AssertionError("L6AN.01 packet cannot authorize or execute a retry")
    if proof.get("may_contain_secret_material") is not False:
        raise AssertionError("binding proof request must ask for non-secret references only")
    counters = packet.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for docs/tests-only auth-binding packet")
