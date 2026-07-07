from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from memory_seam.l6al_service_auth_contract import zero_l6al03_guarded_counters
from memory_seam.l6an_service_operator_auth_binding_packet import (
    L6AN01_BINDING_PROOF_SHAPE,
    L6AN01_NO_GO_SURFACES,
    build_l6an01_exact_retry_binding,
)
from memory_seam.l6am_supervised_metadata_retry_packet import (
    L6AM01_PARENT_ISSUE,
    L6AM01_REPOSITORY,
)

L6AO01_SCHEMA_VERSION = "l6ao01-auth-held-default-off-binding-intake-v1"
L6AO01_RAIL_ISSUE = 380
L6AO01_PARENT_ISSUE = L6AM01_PARENT_ISSUE
L6AO01_RAIL_STARTING_SOURCE_FLOOR = "57e8bd4612824ada20718e41b1eea33210fe2974"
L6AO01_PREAUTH_COMMENT = "4656625129"
L6AO01_PARENT_RAIL_CREATED_COMMENT = "4656626203"
L6AO01_STATUS = "AUTH_HELD_BLOCKER_RECEIPT_DEFAULT_OFF_BINDING_INTAKE_READY"
L6AO01_RETRY_STATE = "HELD_NO_LIVE_RETRY_DEFAULT_OFF_UNTIL_EXACT_FRESH_BINDING_AND_MAX_ONE_EXECUTION_PACKET"
L6AO01_INTAKE_STATE = "DEFAULT_OFF_REPORT_SAFE_NON_SECRET_BINDING_INTAKE_ONLY"
L6AO01_OPERATION_CLASS = "L6AO_EXACT_MAX_ONE_METADATA_RETRY_AUTH_HELD_DEFAULT_OFF"
L6AO01_REQUIRED_INTAKE_FIELDS = frozenset(
    {
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
        "issue_bound_authorization_ref",
    }
)
L6AO01_DEFAULT_OFF_FLAGS = {
    "retry_authorized": False,
    "retry_executed": False,
    "live_retry_enabled": False,
    "runtime_registry_enabled": False,
    "provider_callback_enabled": False,
    "service_activation_enabled": False,
    "source_discovery_enabled": False,
    "external_write_enabled": False,
    "provider_prod_canary_gate_enabled": False,
    "broad_allowed": False,
}
L6AO01_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "status",
        "preauth_comment",
        "parent_rail_created_comment",
        "source_blocker_receipt",
        "operation_class",
        "retry_state",
        "intake_state",
        "default_off_flags",
        "binding_intake_packet",
        "approval_not_inferred_from",
        "no_go_surfaces",
        "guarded_counters",
    }
)

L6AO02_SCHEMA_VERSION = "l6ao02-binding-intake-readiness-fixtures-v1"
L6AO02_RAIL_ISSUE = 381
L6AO02_READY_STATUS = "BINDING_INTAKE_READY_RETRY_HELD"
L6AO02_HELD_STATUS = "BINDING_INTAKE_HELD_BEFORE_READ"
L6AO02_DENIED_STATUS = "BINDING_INTAKE_DENIED_BEFORE_READ"
L6AO02_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "status",
        "reasons",
        "target_metadata",
        "retry_executed",
        "guarded_counters",
    }
)
L6AO02_TARGET_FIELDS = (
    "endpoint",
    "route_audience",
    "agent",
    "scope",
    "n",
    "query_label",
    "query_text",
    "evidence_class",
    "max_operation_count",
    "report_safe_metadata_only",
)
L6AO02_FORBIDDEN_TRUE_FLAGS = {
    "raw_output_requested": "raw_output_requested",
    "raw_private_output_requested": "raw_output_requested",
    "raw_source_output_requested": "raw_output_requested",
    "allowed": "broad_allowed_true",
    "broad_allowed": "broad_allowed_true",
}

L6AO03_SCHEMA_VERSION = "l6ao03-max-one-metadata-retry-execution-packet-v1"
L6AO03_RAIL_ISSUE = 382
L6AO03_PACKET_STATUS = "MAX_ONE_METADATA_RETRY_EXECUTION_PACKET_READY_RETRY_HELD"
L6AO03_REFUSED_STATUS = "MAX_ONE_METADATA_RETRY_EXECUTION_REFUSED_BEFORE_READ"
L6AO03_OPERATION_CLASS = "L6AO_EXACT_MAX_ONE_METADATA_RETRY_EXECUTION_PACKET"
L6AO03_REPORT_SAFE_OUTPUT_FIELDS = (
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
    "guarded_counters",
)
L6AO03_STOP_CONDITIONS = (
    "missing_fresh_exact_non_secret_binding_approval",
    "missing_explicit_retry_issue_authorization",
    "stale_or_mismatched_binding_approval",
    "max_operation_count_not_one",
    "report_safe_metadata_only_not_true",
    "denial_before_read_not_required",
    "raw_private_source_or_auth_content_requested",
    "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "runtime_registry_provider_callback_or_service_activation_requested",
    "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested",
)
L6AO03_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "parent_issue",
        "status",
        "operation_class",
        "target",
        "approval_requirements",
        "report_safe_output_fields",
        "denial_before_read_stop_conditions",
        "rollback_stop_conditions",
        "retry_authorized",
        "retry_executed",
        "refusal_reasons",
        "guarded_counters",
    }
)
L6AO03_FORBIDDEN_TRUE_FLAGS = {
    "raw_output_requested": "raw_private_source_or_auth_content_requested",
    "raw_private_output_requested": "raw_private_source_or_auth_content_requested",
    "raw_source_output_requested": "raw_private_source_or_auth_content_requested",
    "credential_read_requested": "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "secret_read_requested": "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "auth_file_read_requested": "secret_env_keychain_oauth_auth_file_or_credential_read_requested",
    "runtime_registry_requested": "runtime_registry_provider_callback_or_service_activation_requested",
    "provider_callback_requested": "runtime_registry_provider_callback_or_service_activation_requested",
    "service_activation_requested": "runtime_registry_provider_callback_or_service_activation_requested",
    "source_discovery_requested": "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "broad_recall_requested": "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "allowed": "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "broad_allowed": "source_discovery_broad_recall_or_broad_allowed_true_requested",
    "write_requested": "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested",
    "mutation_requested": "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested",
    "provider_prod_canary_gate_requested": "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested",
    "atlas_gate_requested": "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested",
}

L6AO04_SCHEMA_VERSION = "l6ao04-trust-boundary-review-v1"
L6AO04_RAIL_ISSUE = 383
L6AO04_STATUS = "TRUST_BOUNDARY_REVIEW_PASS_AUTH_HELD_RETRY_DEFAULT_OFF"
L6AO04_REVIEWED_ARTIFACTS = (
    "#380 L6AO.01 auth-held blocker receipt and default-off binding intake",
    "#381 L6AO.02 binding-intake readiness fixtures and denial-before-read states",
    "#382 L6AO.03 max-one metadata retry execution packet scaffold",
)
L6AO04_BLOCKER_OWNER = "service-owner-or-operator"
L6AO04_FUTURE_UNBLOCK_CONDITION = (
    "fresh exact non-secret operator/service binding approval plus explicit issue-bound "
    "max-one metadata retry authorization"
)
L6AO04_TRUST_BOUNDARY_FINDINGS = {
    "secret_private_source_or_raw_content_present": False,
    "secret_env_keychain_oauth_auth_file_or_credential_read_present": False,
    "runtime_registry_provider_callback_or_service_activation_present": False,
    "source_discovery_broad_recall_or_broad_allowed_true_present": False,
    "provider_prod_canary_gate_atlas_gate_write_or_mutation_present": False,
    "auth_blocker_owner_named": True,
    "future_unblock_condition_exact": True,
    "retry_remains_auth_held_default_off": True,
}
L6AO04_ROLLBACK_STOP_CONDITIONS = (
    "missing_fresh_exact_non_secret_operator_service_binding_approval",
    "missing_explicit_issue_bound_max_one_metadata_retry_authorization",
    "stale_copied_mismatched_expired_or_broadened_approval",
    "any_raw_private_source_or_auth_content_request",
    "any_secret_env_keychain_oauth_auth_file_or_credential_read_request",
    "any_source_discovery_broad_recall_or_broad_allowed_true_request",
    "any_runtime_registry_provider_callback_or_service_activation_request",
    "any_provider_prod_canary_gate_atlas_gate_write_or_mutation_request",
    "any_nonzero_guarded_counter_or_retry_execution_attempt",
)
L6AO04_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "parent_issue",
        "status",
        "source_floor",
        "reviewed_artifacts",
        "trust_boundary_findings",
        "blocker_owner",
        "future_unblock_condition",
        "rollback_stop_conditions",
        "retry_authorized",
        "retry_executed",
        "guarded_counters",
    }
)

L6AO05_SCHEMA_VERSION = "l6ao05-source-floor-parent-tracker-reconciliation-v1"
L6AO05_RAIL_ISSUE = 384
L6AO05_STATUS = "AUTH_HELD_UNBLOCK_RAIL_COMPLETE_RETRY_HELD"
L6AO05_FINAL_SOURCE_FLOOR = "93481ca84ca2e1f3535acbb68d22199e09ed41be"
L6AO05_RAIL_ANCHORS = (
    {
        "issue": 380,
        "pr": 385,
        "merge_commit": "e012328ec4156b778b797d48b6a16c8363398cac",
        "artifact": "L6AO.01 auth-held blocker receipt and default-off binding intake packet",
    },
    {
        "issue": 381,
        "pr": 386,
        "merge_commit": "d7bbb00f955522baf8a62c3c3b5daa8604e39424",
        "artifact": "L6AO.02 binding-intake readiness fixtures and denial-before-read states",
    },
    {
        "issue": 382,
        "pr": 387,
        "merge_commit": "2ca36d07ba02bda0f33de9db7955ae6ffd0b1b54",
        "artifact": "L6AO.03 max-one metadata retry execution packet scaffold",
    },
    {
        "issue": 383,
        "pr": 388,
        "merge_commit": L6AO05_FINAL_SOURCE_FLOOR,
        "artifact": "L6AO.04 trust-boundary review",
    },
)
L6AO05_PARENT_RECEIPT_TEXT = (
    "Parent #6 receipt: L6AO auth-held/default-off unblock rail complete. "
    "Issues #380-#384 and PRs #385-#389 record the blocker receipt, binding intake readiness, "
    "max-one metadata retry execution packet scaffold, trust-boundary review, and source-floor reconciliation. "
    "Final result: auth-held unblock rail complete; retry remains held unless fresh exact non-secret "
    "binding approval plus explicit max-one retry issue authorization exists. No live retry, raw/private/source "
    "content, credential/auth reads, Runtime Registry/provider callback/service activation, source discovery, "
    "external tracker writes, cron mutation, Gate movement, or broad allowed=true behavior occurred."
)
L6AO05_TRACKER_UPDATE_TEXT = (
    "Atlas tracker update text: mark L6AO auth-held/default-off unblock rail complete / RETRY HELD at "
    "source floor 93481ca84ca2e1f3535acbb68d22199e09ed41be; record #380-#384 and PR #385-#389 as "
    "repo-side evidence; carry next retry as HELD until fresh exact non-secret binding approval plus explicit "
    "max-one retry issue exists; writer performed no external tracker write and no cron mutation."
)
L6AO05_RESIDUAL_HOLDS = (
    "live_retry",
    "raw_private_source_or_auth_content",
    "secret_env_keychain_oauth_auth_file_or_credential_reads",
    "runtime_registry_provider_callback_or_service_activation",
    "source_discovery_broad_recall_or_broad_allowed_true",
    "external_tracker_write_or_cron_mutation_from_writer",
    "provider_prod_canary_gate_atlas_gate_write_or_mutation",
)
L6AO05_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "parent_issue",
        "status",
        "rail_starting_source_floor",
        "final_source_floor",
        "rail_anchors",
        "final_result",
        "retry_state",
        "parent_receipt_text",
        "tracker_update_text",
        "external_tracker_written",
        "cron_mutated",
        "retry_authorized",
        "retry_executed",
        "residual_holds",
        "guarded_counters",
    }
)


def build_l6ao01_source_blocker_receipt() -> dict[str, Any]:
    """Record the report-safe auth-held blocker without reading credentials or sources."""

    return {
        "blocker": "auth_held_missing_fresh_operator_service_binding",
        "prior_denial_summary": "L6AM/L6AN safe denial: auth_status_code=403 wrong_route_audience items=0",
        "prior_request_class": "memory_seam_recall_report_safe_metadata_only_max_one",
        "default_decision": "deny_before_read_and_hold_retry",
        "source_floor": L6AO01_RAIL_STARTING_SOURCE_FLOOR,
        "raw_or_private_content_included": False,
        "credential_or_auth_material_included": False,
        "live_retry_executed": False,
    }


def build_l6ao01_binding_intake_packet() -> dict[str, Any]:
    """Return the non-secret binding intake shape while keeping execution default-off."""

    exact = build_l6an01_exact_retry_binding()
    return {
        "required_fields": sorted(L6AO01_REQUIRED_INTAKE_FIELDS),
        "must_match": {
            "route_audience": exact["route_audience"],
            "acting_for": exact["acting_for"],
            "agent": exact["agent"],
            "scope": exact["scope"],
            "query_label": exact["query_label"],
            "evidence_class": exact["evidence_class"],
            "max_operation_count": exact["max_operation_count"],
            "report_safe_metadata_only": exact["report_safe_metadata_only"],
            "denial_before_read_required": exact["denial_before_read_required"],
        },
        "proof_shape_source": list(L6AN01_BINDING_PROOF_SHAPE),
        "may_contain_secret_material": False,
        "may_contain_raw_private_or_source_content": False,
        "runtime_or_provider_lookup_allowed": False,
        "default_off_until_later_packet": True,
        "retry_authorized_by_intake": False,
    }


def build_l6ao01_auth_held_default_off_intake_receipt() -> dict[str, Any]:
    """Build the L6AO.01 receipt/intake packet as report-safe metadata only."""

    return {
        "schema_version": L6AO01_SCHEMA_VERSION,
        "repo": L6AM01_REPOSITORY,
        "parent_issue": L6AO01_PARENT_ISSUE,
        "rail_issue": L6AO01_RAIL_ISSUE,
        "rail_starting_source_floor": L6AO01_RAIL_STARTING_SOURCE_FLOOR,
        "status": L6AO01_STATUS,
        "preauth_comment": L6AO01_PREAUTH_COMMENT,
        "parent_rail_created_comment": L6AO01_PARENT_RAIL_CREATED_COMMENT,
        "source_blocker_receipt": build_l6ao01_source_blocker_receipt(),
        "operation_class": L6AO01_OPERATION_CLASS,
        "retry_state": L6AO01_RETRY_STATE,
        "intake_state": L6AO01_INTAKE_STATE,
        "default_off_flags": dict(L6AO01_DEFAULT_OFF_FLAGS),
        "binding_intake_packet": build_l6ao01_binding_intake_packet(),
        "approval_not_inferred_from": [
            "parent issue #6 rail-created receipt comment 4656626203",
            "issue-bound preauth comment #380 4656625129",
            "L6AN completion packet merge",
            "PR merge",
            "issue closure",
            "stale copied or broadened approval text",
            "broad allowed=true language",
        ],
        "no_go_surfaces": list(L6AN01_NO_GO_SURFACES),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ao01_receipt_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AO01_REPORT_SAFE_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AO.01 receipt fields present: {sorted(unexpected)}")
    if receipt.get("status") != L6AO01_STATUS:
        raise AssertionError("L6AO.01 status must mark auth-held default-off intake ready")
    if receipt.get("retry_state") != L6AO01_RETRY_STATE:
        raise AssertionError("L6AO.01 retry state must remain held/default-off")
    flags = receipt.get("default_off_flags")
    if not isinstance(flags, Mapping) or any(value is not False for value in flags.values()):
        raise AssertionError("all L6AO.01 default-off flags must remain false")
    intake = receipt.get("binding_intake_packet")
    if not isinstance(intake, Mapping):
        raise AssertionError("binding intake packet must be report-safe metadata")
    for key in (
        "may_contain_secret_material",
        "may_contain_raw_private_or_source_content",
        "runtime_or_provider_lookup_allowed",
        "retry_authorized_by_intake",
    ):
        if intake.get(key) is not False:
            raise AssertionError(f"binding intake packet must keep {key}=false")
    if intake.get("default_off_until_later_packet") is not True:
        raise AssertionError("binding intake must remain default-off until a later execution packet")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AO.01 intake")


def build_l6ao02_ready_binding_intake_fixture() -> dict[str, Any]:
    """Return the exact report-safe binding intake fixture; no runtime state is inspected."""

    exact = build_l6an01_exact_retry_binding()
    return {
        "operator_service_binding_ref": "operator-service-binding:l6ao02:report-safe-metadata-recall:max-one",
        "binding_owner": "service-owner-or-operator",
        "identity_subject": "supervised service caller bound to sax",
        "endpoint": exact["endpoint"],
        "route_audience": exact["route_audience"],
        "acting_for": exact["acting_for"],
        "agent": exact["agent"],
        "scope": exact["scope"],
        "n": exact["n"],
        "query_label": exact["query_label"],
        "query_text": exact["query_text"],
        "evidence_class": exact["evidence_class"],
        "max_operation_count": exact["max_operation_count"],
        "report_safe_metadata_only": exact["report_safe_metadata_only"],
        "denial_before_read_required": exact["denial_before_read_required"],
        "expires_at_or_one_run_custody": "one-run-custody:l6ao02:max-one-retry-held",
        "issue_bound_authorization_ref": "issue-381-preauth-comment-4656625391",
    }


def evaluate_l6ao02_binding_intake_readiness(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Evaluate committed intake metadata only, denying before any read or retry."""

    if not isinstance(candidate, Mapping):
        candidate = {}

    reasons: list[str] = []
    status = L6AO02_READY_STATUS

    for field in (
        "operator_service_binding_ref",
        "binding_owner",
        "identity_subject",
        "expires_at_or_one_run_custody",
        "issue_bound_authorization_ref",
    ):
        if not candidate.get(field):
            reasons.append("missing_binding_intake_reference")
            status = L6AO02_HELD_STATUS

    if candidate.get("expires_at_or_one_run_custody") in {"expired", "stale", "revoked"}:
        reasons.append("stale_binding_intake_reference")
        status = L6AO02_HELD_STATUS
    if candidate.get("binding_fresh") is False:
        reasons.append("stale_binding_intake_reference")
        status = L6AO02_HELD_STATUS

    exact = build_l6an01_exact_retry_binding()
    for field in L6AO02_TARGET_FIELDS:
        if field in candidate and candidate.get(field) != exact[field]:
            reasons.append(f"wrong_{field}")
            status = L6AO02_DENIED_STATUS
    if "query" in candidate and candidate.get("query") != exact["query_text"]:
        reasons.append("wrong_query")
        status = L6AO02_DENIED_STATUS

    for flag, reason in L6AO02_FORBIDDEN_TRUE_FLAGS.items():
        if candidate.get(flag) is True:
            reasons.append(reason)
            status = L6AO02_DENIED_STATUS

    if not reasons:
        reasons.append("exact_default_off_binding_intake_ready_retry_still_held")

    return {
        "schema_version": L6AO02_SCHEMA_VERSION,
        "rail_issue": L6AO02_RAIL_ISSUE,
        "status": status,
        "reasons": sorted(set(reasons)),
        "target_metadata": {field: candidate.get(field) for field in L6AO02_TARGET_FIELDS},
        "retry_executed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ao02_readiness_receipt_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AO02_RECEIPT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AO.02 receipt fields present: {sorted(unexpected)}")
    if receipt.get("retry_executed") is not False:
        raise AssertionError("L6AO.02 readiness fixtures cannot execute retry")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AO.02 readiness")


def build_l6ao03_max_one_metadata_retry_execution_packet() -> dict[str, Any]:
    """Build the future execution handoff packet without authorizing or running it."""

    exact = build_l6an01_exact_retry_binding()
    return {
        "schema_version": L6AO03_SCHEMA_VERSION,
        "rail_issue": L6AO03_RAIL_ISSUE,
        "parent_issue": L6AO01_PARENT_ISSUE,
        "status": L6AO03_PACKET_STATUS,
        "operation_class": L6AO03_OPERATION_CLASS,
        "target": {
            "endpoint": exact["endpoint"],
            "route_audience": exact["route_audience"],
            "agent": exact["agent"],
            "scope": exact["scope"],
            "n": exact["n"],
            "query_label": exact["query_label"],
            "query_text": exact["query_text"],
            "evidence_class": exact["evidence_class"],
            "max_operation_count": exact["max_operation_count"],
            "report_safe_metadata_only": exact["report_safe_metadata_only"],
            "denial_before_read_required": exact["denial_before_read_required"],
        },
        "approval_requirements": {
            "fresh_exact_non_secret_binding_approval_required": True,
            "explicit_retry_issue_authorization_required": True,
            "accepted_binding_approval_kind": "issue-bound-fresh-non-secret-operator-service-binding",
            "accepted_retry_authorization_kind": "explicit-issue-bound-max-one-metadata-retry-authorization",
            "approval_not_inferred_from": [
                "preauth comments",
                "parent rail-created receipt",
                "binding-intake readiness fixture",
                "PR merge",
                "issue closure",
                "stale copied approval text",
                "broad allowed=true language",
            ],
        },
        "report_safe_output_fields": list(L6AO03_REPORT_SAFE_OUTPUT_FIELDS),
        "denial_before_read_stop_conditions": list(L6AO03_STOP_CONDITIONS),
        "rollback_stop_conditions": [
            "stop_before_read_and_emit_receipt_only",
            "keep_guarded_counters_zero_on_refusal",
            "do_not_retry_more_than_once",
            "do_not_persist_or_mutate_external_state",
        ],
        "retry_authorized": False,
        "retry_executed": False,
        "refusal_reasons": [
            "missing_fresh_exact_non_secret_binding_approval",
            "missing_explicit_retry_issue_authorization",
        ],
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def evaluate_l6ao03_execution_authorization(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Refuse the future retry unless both fresh exact approvals are present."""

    if not isinstance(candidate, Mapping):
        candidate = {}

    packet = build_l6ao03_max_one_metadata_retry_execution_packet()
    reasons: list[str] = []
    if candidate.get("fresh_exact_non_secret_binding_approval") is not True:
        reasons.append("missing_fresh_exact_non_secret_binding_approval")
    if candidate.get("explicit_retry_issue_authorization") is not True:
        reasons.append("missing_explicit_retry_issue_authorization")
    if candidate.get("binding_approval_fresh") is False or candidate.get("binding_approval_state") in {"stale", "expired", "revoked"}:
        reasons.append("stale_or_mismatched_binding_approval")

    target = packet["target"]
    for field in ("endpoint", "route_audience", "agent", "scope", "n", "query_label", "query_text", "evidence_class"):
        if field in candidate and candidate.get(field) != target[field]:
            reasons.append(f"wrong_{field}")
    if candidate.get("max_operation_count", target["max_operation_count"]) != 1:
        reasons.append("max_operation_count_not_one")
    if candidate.get("report_safe_metadata_only", target["report_safe_metadata_only"]) is not True:
        reasons.append("report_safe_metadata_only_not_true")
    if candidate.get("denial_before_read_required", target["denial_before_read_required"]) is not True:
        reasons.append("denial_before_read_not_required")
    for flag, reason in L6AO03_FORBIDDEN_TRUE_FLAGS.items():
        if candidate.get(flag) is True:
            reasons.append(reason)

    packet["status"] = L6AO03_REFUSED_STATUS
    packet["retry_authorized"] = False
    packet["retry_executed"] = False
    packet["refusal_reasons"] = sorted(set(reasons or ["execution_authority_absent_default_off_hold"]))
    packet["guarded_counters"] = zero_l6al03_guarded_counters()
    return packet


def assert_l6ao03_execution_packet_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AO03_RECEIPT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AO.03 receipt fields present: {sorted(unexpected)}")
    if receipt.get("retry_authorized") is not False or receipt.get("retry_executed") is not False:
        raise AssertionError("L6AO.03 scaffold must not authorize or execute retry")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AO.03 execution packet")
    fields = receipt.get("report_safe_output_fields")
    if not isinstance(fields, list) or "raw_private_source" in fields or "credential" in fields:
        raise AssertionError("L6AO.03 output fields must remain receipt-safe")


def build_l6ao04_trust_boundary_review() -> dict[str, Any]:
    """Review L6AO.01-L6AO.03 report-safe artifacts while keeping retry held."""

    return {
        "schema_version": L6AO04_SCHEMA_VERSION,
        "rail_issue": L6AO04_RAIL_ISSUE,
        "parent_issue": L6AO01_PARENT_ISSUE,
        "status": L6AO04_STATUS,
        "source_floor": L6AO01_RAIL_STARTING_SOURCE_FLOOR,
        "reviewed_artifacts": list(L6AO04_REVIEWED_ARTIFACTS),
        "trust_boundary_findings": dict(L6AO04_TRUST_BOUNDARY_FINDINGS),
        "blocker_owner": L6AO04_BLOCKER_OWNER,
        "future_unblock_condition": L6AO04_FUTURE_UNBLOCK_CONDITION,
        "rollback_stop_conditions": list(L6AO04_ROLLBACK_STOP_CONDITIONS),
        "retry_authorized": False,
        "retry_executed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ao04_review_report_safe(review: Mapping[str, Any]) -> None:
    unexpected = set(review.keys()).difference(L6AO04_RECEIPT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AO.04 review fields present: {sorted(unexpected)}")
    if review.get("status") != L6AO04_STATUS:
        raise AssertionError("L6AO.04 review must record trust-boundary pass with auth-held retry")
    if review.get("retry_authorized") is not False or review.get("retry_executed") is not False:
        raise AssertionError("L6AO.04 review must not authorize or execute retry")
    counters = review.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AO.04 review")
    findings = review.get("trust_boundary_findings")
    if not isinstance(findings, Mapping):
        raise AssertionError("L6AO.04 findings must be report-safe metadata")
    for key in (
        "secret_private_source_or_raw_content_present",
        "secret_env_keychain_oauth_auth_file_or_credential_read_present",
        "runtime_registry_provider_callback_or_service_activation_present",
        "source_discovery_broad_recall_or_broad_allowed_true_present",
        "provider_prod_canary_gate_atlas_gate_write_or_mutation_present",
    ):
        if findings.get(key) is not False:
            raise AssertionError(f"L6AO.04 finding {key} must remain false")
    for key in (
        "auth_blocker_owner_named",
        "future_unblock_condition_exact",
        "retry_remains_auth_held_default_off",
    ):
        if findings.get(key) is not True:
            raise AssertionError(f"L6AO.04 finding {key} must remain true")


def build_l6ao05_source_floor_parent_tracker_reconciliation() -> dict[str, Any]:
    """Reconcile the L6AO rail using report-safe repo metadata only."""

    return {
        "schema_version": L6AO05_SCHEMA_VERSION,
        "rail_issue": L6AO05_RAIL_ISSUE,
        "parent_issue": L6AO01_PARENT_ISSUE,
        "status": L6AO05_STATUS,
        "rail_starting_source_floor": L6AO01_RAIL_STARTING_SOURCE_FLOOR,
        "final_source_floor": L6AO05_FINAL_SOURCE_FLOOR,
        "rail_anchors": [dict(anchor) for anchor in L6AO05_RAIL_ANCHORS],
        "final_result": "auth-held unblock rail complete",
        "retry_state": (
            "retry remains held unless fresh exact non-secret binding approval plus explicit "
            "max-one retry issue exists"
        ),
        "parent_receipt_text": L6AO05_PARENT_RECEIPT_TEXT,
        "tracker_update_text": L6AO05_TRACKER_UPDATE_TEXT,
        "external_tracker_written": False,
        "cron_mutated": False,
        "retry_authorized": False,
        "retry_executed": False,
        "residual_holds": list(L6AO05_RESIDUAL_HOLDS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ao05_reconciliation_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AO05_RECEIPT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AO.05 reconciliation fields present: {sorted(unexpected)}")
    if receipt.get("status") != L6AO05_STATUS:
        raise AssertionError("L6AO.05 status must record complete auth-held rail with retry held")
    if receipt.get("final_result") != "auth-held unblock rail complete":
        raise AssertionError("L6AO.05 final result must mark the auth-held unblock rail complete")
    retry_state = receipt.get("retry_state")
    if not isinstance(retry_state, str) or "fresh exact non-secret binding approval" not in retry_state:
        raise AssertionError("L6AO.05 retry state must keep exact approval and max-one issue blockers")
    if "explicit max-one retry issue" not in retry_state:
        raise AssertionError("L6AO.05 retry state must require explicit max-one retry issue authorization")
    if receipt.get("external_tracker_written") is not False or receipt.get("cron_mutated") is not False:
        raise AssertionError("L6AO.05 writer must not mutate external tracker state or crons")
    if receipt.get("retry_authorized") is not False or receipt.get("retry_executed") is not False:
        raise AssertionError("L6AO.05 reconciliation must not authorize or execute retry")
    anchors = receipt.get("rail_anchors")
    if not isinstance(anchors, list) or [anchor.get("issue") for anchor in anchors] != [380, 381, 382, 383]:
        raise AssertionError("L6AO.05 must preserve #380-#383 rail anchors in order")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AO.05 reconciliation")
    holds = receipt.get("residual_holds")
    if not isinstance(holds, list) or "live_retry" not in holds:
        raise AssertionError("L6AO.05 residual holds must preserve live retry hold")
