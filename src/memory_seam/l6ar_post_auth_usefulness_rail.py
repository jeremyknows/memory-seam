from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from memory_seam.l6al_service_auth_contract import zero_l6al03_guarded_counters

L6AR_REPOSITORY = "memory-seam/reference-release"
L6AR_PARENT_ISSUE = 6
L6AR_RAIL_STARTING_SOURCE_FLOOR = "67b5bcc1019899ed3075c8bc44dcfdb9221d9c33"
L6AR_SYSTEM_PIPES_REPAIR_FLOOR = "a709b14a33b7d22ec980dba97ce20bf56a6c2d86"
L6AR_PARENT_CREATION_RECEIPT = "4663160613"

L6AR01_RAIL_ISSUE = 410
L6AR01_SCHEMA_VERSION = "l6ar01-reference-adapter-recall-authority-intake-v1"
L6AR01_STATUS = "REFERENCE_ADAPTER_RECALL_AUTHORITY_INTAKE_RELOAD_BOUNDARY_ANCHORED"
L6AR01_HELD_STATUS = "REFERENCE_ADAPTER_RECALL_AUTHORITY_INTAKE_HELD_BEFORE_READ"
L6AR01_ENDPOINT = "memory_seam_recall"
L6AR01_ROUTE_AUDIENCE = "memory-seam:read:recall"
L6AR01_AGENT = "reference-agent"
L6AR01_ACTING_FOR = "reference-operator"
L6AR01_SCOPE = "wiki"
L6AR01_N = 3
L6AR01_QUERY_LABEL = "supervised_metadata_readiness"
L6AR01_EVIDENCE_CLASS = "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
L6AR01_FRESH_STDIO_AUTH_STATE = "AUTH_UNBLOCKED_IN_FRESH_ADAPTER_PROCESS_AFTER_REFERENCE_REPAIR"
L6AR01_STALE_CACHE_STATE = "STALE_CLIENT_CACHE_NOT_RELIED_ON_FOR_RETRY_AUTHORITY"
L6AR01_RELOAD_BOUNDARY = "fresh adapter process boundary required before any #412 max-one attempt"
L6AR01_NEXT_ISSUE = 411
L6AR01_ATTEMPT_COUNT = 0

L6AR02_RAIL_ISSUE = 411
L6AR02_SCHEMA_VERSION = "l6ar02-report-safe-usefulness-candidate-packet-v1"
L6AR02_STATUS = "REPORT_SAFE_USEFULNESS_QUERY_SOURCE_CARD_CANDIDATE_PACKET_READY"
L6AR02_HELD_STATUS = "REPORT_SAFE_USEFULNESS_CANDIDATE_PACKET_HELD_BEFORE_READ"
L6AR02_QUERY_LABEL = "supervised_metadata_readiness"
L6AR02_SOURCE_CARD_CANDIDATE_LABEL = "report_safe_metadata_usefulness_candidate"
L6AR02_DESCRIPTOR_CANDIDATE_LABEL = "report_safe_metadata_descriptor_candidate"
L6AR02_USEFULNESS_GOAL_LABEL = "post_auth_metadata_usefulness_signal"
L6AR02_EXPECTED_EVIDENCE_LABELS = (
    "endpoint_route_audience_alignment",
    "auth_status_label",
    "item_count_scalar",
    "safe_item_label_set",
    "degraded_flag_set",
)
L6AR02_NEXT_ISSUE = 412

L6AR03_RAIL_ISSUE = 412
L6AR03_SCHEMA_VERSION = "l6ar03-fresh-process-metadata-usefulness-attempt-v1"
L6AR03_STATUS = "FRESH_PROCESS_METADATA_USEFULNESS_ZERO_ITEM_DEGRADED_RECEIPT_CAPTURED"
L6AR03_HELD_STATUS = "FRESH_PROCESS_METADATA_USEFULNESS_ATTEMPT_HELD_OR_UNSAFE"
L6AR03_OPERATION_CLASS = "memory_seam_recall_report_safe_metadata_usefulness_attempt"
L6AR03_AUTH_STATUS = "tool_success"
L6AR03_DENIAL_REASON_LABEL = "unauthorized_narrowing"
L6AR03_DEGRADED = True
L6AR03_DEGRADED_FLAGS = ("unauthorized_narrowing",)
L6AR03_ITEM_COUNT = 0
L6AR03_SAFE_ITEM_LABELS: tuple[str, ...] = ()
L6AR03_ATTEMPT_COUNT = 1
L6AR03_NEXT_ISSUE = 413

L6AR04_RAIL_ISSUE = 413
L6AR04_SCHEMA_VERSION = "l6ar04-post-auth-usefulness-trust-boundary-review-v1"
L6AR04_STATUS = "TRUST_BOUNDARY_REVIEW_PASS_POST_AUTH_USEFULNESS_ZERO_ITEM_HELD"
L6AR04_HELD_STATUS = "TRUST_BOUNDARY_REVIEW_HOLD_POST_AUTH_USEFULNESS_BOUNDARY"
L6AR04_REVIEW_VERDICT = "PASS"
L6AR04_NEXT_ISSUE = 414

L6AR05_RAIL_ISSUE = 414
L6AR05_SCHEMA_VERSION = "l6ar05-source-floor-parent-tracker-reconciliation-v1"
L6AR05_STATUS = "SOURCE_FLOOR_PARENT_TRACKER_RECONCILIATION_COMPLETE"
L6AR05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR = "0fb18605f2a1150c2f683f1f69b05d5a10f48447"
L6AR05_NEXT_FRONTIER = "post-auth usefulness remains held after zero-item degraded metadata receipt; external tracker updates remain maintainer-owned"
L6AR05_PARENT_RECEIPT_TEXT = (
    "Parent #6 receipt: L6AR post-auth usefulness rail complete through source-floor "
    "reconciliation. #410 anchored fresh adapter recall authority after the reference repair; "
    "#411 prepared a report-safe usefulness candidate packet; #412 consumed exactly one "
    "fresh-process metadata attempt and stopped on zero-item degraded output; #413 recorded "
    "PASS for the trust-boundary review; #414 reconciles source floor, parent receipt text, "
    "tracker update text, and next frontier. No raw/private/source item content, source paths/URIs, "
    "auth/provider/callback payloads, provider/prod/canary/write movement, second attempt, "
    "successor issue, or scheduler mutation was introduced."
)
L6AR05_TRACKER_UPDATE_TEXT = (
    "Reference tracker update text: mark Memory Seam post-auth usefulness successor rail L6AR as "
    "RECONCILED / ZERO-ITEM DEGRADED METADATA RECEIPT / TRUST-BOUNDARY PASS. Record source floor "
    "0fb18605f2a1150c2f683f1f69b05d5a10f48447 before #414, note #412 attempt_count=1, "
    "second_attempt_performed=false, item_count=0, safe_item_labels=[], degraded_flags=[unauthorized_narrowing], "
    "guarded_counters=zero, and do not create or run another usefulness attempt from this rail. "
    "External tracker edits remain owned by the release maintainer, not this writer."
)
L6AR05_RAIL_ANCHORS = (
    {"issue": 410, "pr": 415, "source_floor": "8e1d22cadc8830c00f4cb1578e1cede97b9f4199", "status": L6AR01_STATUS},
    {"issue": 411, "pr": 416, "source_floor": "6b24532d3f3083bb336466ce7b939aa4d0a60b23", "status": L6AR02_STATUS},
    {"issue": 412, "pr": 417, "source_floor": "0b460e1127b5cd479cc378dd9059409fde05c270", "status": L6AR03_STATUS},
    {"issue": 413, "pr": 418, "source_floor": "0fb18605f2a1150c2f683f1f69b05d5a10f48447", "status": L6AR04_STATUS},
)

L6AR01_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "system_pipes_repair_floor",
        "parent_creation_receipt",
        "status",
        "recall_target",
        "fresh_stdio_auth_state",
        "stale_cache_state",
        "reload_boundary",
        "authority_scope",
        "retry_executed",
        "attempt_count",
        "second_attempt_performed",
        "next_issue",
        "residual_holds",
        "guarded_counters",
    }
)

L6AR02_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "system_pipes_repair_floor",
        "parent_creation_receipt",
        "status",
        "usefulness_candidate",
        "source_card_candidate",
        "retry_executed",
        "live_private_read_executed",
        "attempt_count",
        "second_attempt_performed",
        "next_issue",
        "residual_holds",
        "guarded_counters",
    }
)

L6AR03_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "system_pipes_repair_floor",
        "parent_creation_receipt",
        "status",
        "preflight",
        "operation_class",
        "endpoint",
        "route_audience",
        "agent",
        "acting_for",
        "scope",
        "n",
        "query_label",
        "evidence_class",
        "auth_status",
        "denial_reason_label",
        "degraded",
        "degraded_flags",
        "item_count",
        "safe_item_labels",
        "attempt_count",
        "second_attempt_performed",
        "fresh_process_boundary",
        "report_safe_metadata_only",
        "max_operation_count",
        "next_issue",
        "residual_holds",
        "guarded_counters",
    }
)

L6AR04_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "system_pipes_repair_floor",
        "parent_creation_receipt",
        "status",
        "review_verdict",
        "reviewed_rail_issues",
        "reviewed_statuses",
        "attempt_custody",
        "trust_boundary_findings",
        "residual_holds",
        "next_issue",
        "guarded_counters",
    }
)

L6AR05_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "system_pipes_repair_floor",
        "parent_creation_receipt",
        "final_pre_reconciliation_source_floor",
        "status",
        "rail_anchors",
        "attempt_metadata_summary",
        "trust_boundary_review",
        "parent_receipt_text",
        "tracker_update_text",
        "next_frontier",
        "external_tracker_written",
        "cron_mutated",
        "successor_issues_created",
        "second_attempt_performed",
        "provider_prod_canary_gate_or_write_movement_performed",
        "residual_holds",
        "guarded_counters",
    }
)

L6AR01_FORBIDDEN_FIELDS = frozenset(
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
        "provider_payload",
        "callback_payload",
        "credential_value",
        "token",
        "secret",
        "env",
        "keychain",
        "oauth",
        "auth_file",
        "query",
        "query_text",
        "items",
        "source_labels",
        "allowed",
        "broad_allowed",
    }
)

L6AR01_RESIDUAL_HOLDS = (
    "no raw/private/source item content",
    "no source paths or URIs",
    "no auth/provider/callback payloads",
    "no secrets/env/keychain/OAuth/auth-file/credential reads",
    "no broad recall/source discovery",
    "no provider/prod/canary/write/mutation movement",
    "no broad allowed=true",
    "no #412 usefulness attempt before #410 and #411 are merged",
    "no second attempt outside issue #412",
    "no successor issues or scheduler mutations",
)
L6AR02_RESIDUAL_HOLDS = L6AR01_RESIDUAL_HOLDS
L6AR03_RESIDUAL_HOLDS = tuple(
    hold
    for hold in L6AR01_RESIDUAL_HOLDS
    if hold != "no #412 usefulness attempt before #410 and #411 are merged"
) + (
    "#412 max-one usefulness attempt completed; no second attempt",
    "#413 trust-boundary review required before reconciliation",
)
L6AR04_RESIDUAL_HOLDS = tuple(
    hold
    for hold in L6AR03_RESIDUAL_HOLDS
    if hold != "#413 trust-boundary review required before reconciliation"
) + (
    "#412 max-one usefulness attempt is consumed and not reusable",
    "#414 source-floor parent/tracker reconciliation required before closing the rail",
)
L6AR05_RESIDUAL_HOLDS = tuple(
    hold
    for hold in L6AR04_RESIDUAL_HOLDS
    if hold != "#414 source-floor parent/tracker reconciliation required before closing the rail"
) + (
    "external tracker edits remain owned by the release maintainer",
    "L6AR rail closed without successor issue creation or scheduler mutation",
)


def build_l6ar01_recall_authority_intake() -> dict[str, Any]:
    """Record the reference-adapter reload boundary without executing recall."""

    return {
        "schema_version": L6AR01_SCHEMA_VERSION,
        "repo": L6AR_REPOSITORY,
        "parent_issue": L6AR_PARENT_ISSUE,
        "rail_issue": L6AR01_RAIL_ISSUE,
        "rail_starting_source_floor": L6AR_RAIL_STARTING_SOURCE_FLOOR,
        "system_pipes_repair_floor": L6AR_SYSTEM_PIPES_REPAIR_FLOOR,
        "parent_creation_receipt": L6AR_PARENT_CREATION_RECEIPT,
        "status": L6AR01_STATUS,
        "recall_target": {
            "endpoint": L6AR01_ENDPOINT,
            "route_audience": L6AR01_ROUTE_AUDIENCE,
            "agent": L6AR01_AGENT,
            "acting_for": L6AR01_ACTING_FOR,
            "scope": L6AR01_SCOPE,
            "n": L6AR01_N,
            "query_label": L6AR01_QUERY_LABEL,
            "evidence_class": L6AR01_EVIDENCE_CLASS,
            "report_safe_metadata_only": True,
            "max_operation_count": 1,
        },
        "fresh_stdio_auth_state": L6AR01_FRESH_STDIO_AUTH_STATE,
        "stale_cache_state": L6AR01_STALE_CACHE_STATE,
        "reload_boundary": L6AR01_RELOAD_BOUNDARY,
        "authority_scope": "docs/tests intake only; #412 owns the single fresh-process metadata attempt after #410/#411 pass",
        "retry_executed": False,
        "attempt_count": L6AR01_ATTEMPT_COUNT,
        "second_attempt_performed": False,
        "next_issue": L6AR01_NEXT_ISSUE,
        "residual_holds": list(L6AR01_RESIDUAL_HOLDS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def evaluate_l6ar01_reload_boundary(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Accept only a report-safe no-attempt reload-boundary acknowledgement."""

    if not isinstance(candidate, Mapping):
        candidate = {}

    reasons: list[str] = []
    for field in L6AR01_FORBIDDEN_FIELDS.intersection(candidate.keys()):
        reasons.append(f"forbidden_field_{field}")

    expected_values = {
        "endpoint": L6AR01_ENDPOINT,
        "route_audience": L6AR01_ROUTE_AUDIENCE,
        "agent": L6AR01_AGENT,
        "acting_for": L6AR01_ACTING_FOR,
        "scope": L6AR01_SCOPE,
        "n": L6AR01_N,
        "query_label": L6AR01_QUERY_LABEL,
        "evidence_class": L6AR01_EVIDENCE_CLASS,
        "fresh_stdio_auth_state": L6AR01_FRESH_STDIO_AUTH_STATE,
        "stale_cache_state": L6AR01_STALE_CACHE_STATE,
        "retry_executed": False,
        "attempt_count": 0,
        "second_attempt_performed": False,
    }
    for field, expected in expected_values.items():
        if candidate.get(field) != expected:
            reasons.append(f"wrong_{field}")

    if candidate.get("source_discovery_requested") is True:
        reasons.append("source_discovery_requested")
    if candidate.get("broad_recall_requested") is True:
        reasons.append("broad_recall_requested")
    if candidate.get("provider_prod_requested") is True:
        reasons.append("provider_prod_requested")
    if candidate.get("write_requested") is True or candidate.get("mutation_requested") is True:
        reasons.append("write_or_mutation_requested")

    return {
        "schema_version": L6AR01_SCHEMA_VERSION,
        "rail_issue": L6AR01_RAIL_ISSUE,
        "status": L6AR01_HELD_STATUS if reasons else L6AR01_STATUS,
        "reasons": reasons or ["reload_boundary_anchored_no_attempt"],
        "retry_executed": False,
        "attempt_count": 0,
        "second_attempt_performed": False,
        "next_issue": L6AR01_NEXT_ISSUE if not reasons else L6AR01_RAIL_ISSUE,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ar01_report_safe(receipt: Mapping[str, Any]) -> None:
    unsafe = set(receipt) - L6AR01_REPORT_SAFE_FIELDS
    if unsafe:
        raise AssertionError(f"unsafe L6AR.01 report fields: {sorted(unsafe)}")

    recall_target = receipt.get("recall_target")
    if not isinstance(recall_target, Mapping):
        raise AssertionError("L6AR.01 recall_target must be metadata mapping")
    target_unsafe = L6AR01_FORBIDDEN_FIELDS.intersection(recall_target.keys())
    if target_unsafe:
        raise AssertionError(f"unsafe L6AR.01 recall target fields: {sorted(target_unsafe)}")

    if receipt.get("retry_executed") is not False:
        raise AssertionError("L6AR.01 must not execute retry")
    if receipt.get("attempt_count") != 0:
        raise AssertionError("L6AR.01 attempt count must stay zero")
    if receipt.get("second_attempt_performed") is not False:
        raise AssertionError("L6AR.01 must not perform a second attempt")
    guarded = receipt.get("guarded_counters")
    if not isinstance(guarded, Mapping) or any(value != 0 for value in guarded.values()):
        raise AssertionError("L6AR.01 guarded counters must stay zero")


def build_l6ar02_usefulness_candidate_packet() -> dict[str, Any]:
    """Build the #411 report-safe candidate packet without live/private reads."""

    return {
        "schema_version": L6AR02_SCHEMA_VERSION,
        "repo": L6AR_REPOSITORY,
        "parent_issue": L6AR_PARENT_ISSUE,
        "rail_issue": L6AR02_RAIL_ISSUE,
        "rail_starting_source_floor": L6AR_RAIL_STARTING_SOURCE_FLOOR,
        "system_pipes_repair_floor": L6AR_SYSTEM_PIPES_REPAIR_FLOOR,
        "parent_creation_receipt": L6AR_PARENT_CREATION_RECEIPT,
        "status": L6AR02_STATUS,
        "usefulness_candidate": {
            "endpoint": L6AR01_ENDPOINT,
            "route_audience": L6AR01_ROUTE_AUDIENCE,
            "agent": L6AR01_AGENT,
            "acting_for": L6AR01_ACTING_FOR,
            "scope": L6AR01_SCOPE,
            "n": L6AR01_N,
            "query_label": L6AR02_QUERY_LABEL,
            "evidence_class": L6AR01_EVIDENCE_CLASS,
            "usefulness_goal_label": L6AR02_USEFULNESS_GOAL_LABEL,
            "report_safe_metadata_only": True,
            "max_operation_count": 1,
            "fresh_process_required": True,
        },
        "source_card_candidate": {
            "descriptor_candidate_label": L6AR02_DESCRIPTOR_CANDIDATE_LABEL,
            "source_card_candidate_label": L6AR02_SOURCE_CARD_CANDIDATE_LABEL,
            "expected_evidence_labels": list(L6AR02_EXPECTED_EVIDENCE_LABELS),
            "raw_content_required": False,
            "source_path_or_uri_required": False,
            "private_identifier_required": False,
        },
        "retry_executed": False,
        "live_private_read_executed": False,
        "attempt_count": 0,
        "second_attempt_performed": False,
        "next_issue": L6AR02_NEXT_ISSUE,
        "residual_holds": list(L6AR02_RESIDUAL_HOLDS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def evaluate_l6ar02_usefulness_candidate(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Accept only the #411 report-safe no-read usefulness/source-card candidate."""

    if not isinstance(candidate, Mapping):
        candidate = {}

    reasons: list[str] = []
    for field in L6AR01_FORBIDDEN_FIELDS.intersection(candidate.keys()):
        reasons.append(f"forbidden_field_{field}")

    expected_values = {
        "endpoint": L6AR01_ENDPOINT,
        "route_audience": L6AR01_ROUTE_AUDIENCE,
        "agent": L6AR01_AGENT,
        "acting_for": L6AR01_ACTING_FOR,
        "scope": L6AR01_SCOPE,
        "n": L6AR01_N,
        "query_label": L6AR02_QUERY_LABEL,
        "evidence_class": L6AR01_EVIDENCE_CLASS,
        "source_card_candidate_label": L6AR02_SOURCE_CARD_CANDIDATE_LABEL,
        "descriptor_candidate_label": L6AR02_DESCRIPTOR_CANDIDATE_LABEL,
        "retry_executed": False,
        "live_private_read_executed": False,
        "attempt_count": 0,
        "second_attempt_performed": False,
    }
    for field, expected in expected_values.items():
        if candidate.get(field) != expected:
            reasons.append(f"wrong_{field}")

    if candidate.get("raw_content_required") is True:
        reasons.append("raw_content_required")
    if candidate.get("source_path_or_uri_required") is True:
        reasons.append("source_path_or_uri_required")
    if candidate.get("private_identifier_required") is True:
        reasons.append("private_identifier_required")
    if candidate.get("source_discovery_requested") is True:
        reasons.append("source_discovery_requested")
    if candidate.get("broad_recall_requested") is True:
        reasons.append("broad_recall_requested")
    if candidate.get("provider_prod_requested") is True:
        reasons.append("provider_prod_requested")
    if candidate.get("write_requested") is True or candidate.get("mutation_requested") is True:
        reasons.append("write_or_mutation_requested")

    return {
        "schema_version": L6AR02_SCHEMA_VERSION,
        "rail_issue": L6AR02_RAIL_ISSUE,
        "status": L6AR02_HELD_STATUS if reasons else L6AR02_STATUS,
        "reasons": reasons or ["report_safe_candidate_ready_no_read"],
        "retry_executed": False,
        "live_private_read_executed": False,
        "attempt_count": 0,
        "second_attempt_performed": False,
        "next_issue": L6AR02_NEXT_ISSUE if not reasons else L6AR02_RAIL_ISSUE,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ar02_report_safe(receipt: Mapping[str, Any]) -> None:
    unsafe = set(receipt) - L6AR02_REPORT_SAFE_FIELDS
    if unsafe:
        raise AssertionError(f"unsafe L6AR.02 report fields: {sorted(unsafe)}")

    for section_name in ("usefulness_candidate", "source_card_candidate"):
        section = receipt.get(section_name)
        if not isinstance(section, Mapping):
            raise AssertionError(f"L6AR.02 {section_name} must be metadata mapping")
        section_unsafe = L6AR01_FORBIDDEN_FIELDS.intersection(section.keys())
        if section_unsafe:
            raise AssertionError(f"unsafe L6AR.02 {section_name} fields: {sorted(section_unsafe)}")

    if receipt.get("retry_executed") is not False:
        raise AssertionError("L6AR.02 must not execute retry")
    if receipt.get("live_private_read_executed") is not False:
        raise AssertionError("L6AR.02 must not execute live/private read")
    if receipt.get("attempt_count") != 0:
        raise AssertionError("L6AR.02 attempt count must stay zero")
    if receipt.get("second_attempt_performed") is not False:
        raise AssertionError("L6AR.02 must not perform a second attempt")
    guarded = receipt.get("guarded_counters")
    if not isinstance(guarded, Mapping) or any(value != 0 for value in guarded.values()):
        raise AssertionError("L6AR.02 guarded counters must stay zero")


def build_l6ar03_fresh_process_usefulness_attempt_receipt() -> dict[str, Any]:
    """Return report-safe metadata from the single #412 fresh-process attempt."""

    l6ar01 = build_l6ar01_recall_authority_intake()
    l6ar02 = build_l6ar02_usefulness_candidate_packet()
    return {
        "schema_version": L6AR03_SCHEMA_VERSION,
        "repo": L6AR_REPOSITORY,
        "parent_issue": L6AR_PARENT_ISSUE,
        "rail_issue": L6AR03_RAIL_ISSUE,
        "rail_starting_source_floor": L6AR_RAIL_STARTING_SOURCE_FLOOR,
        "system_pipes_repair_floor": L6AR_SYSTEM_PIPES_REPAIR_FLOOR,
        "parent_creation_receipt": L6AR_PARENT_CREATION_RECEIPT,
        "status": L6AR03_STATUS,
        "preflight": {
            "l6ar01_status": l6ar01["status"],
            "l6ar02_status": l6ar02["status"],
            "l6ar01_rail_issue": L6AR01_RAIL_ISSUE,
            "l6ar02_rail_issue": L6AR02_RAIL_ISSUE,
            "preflight_passed": l6ar01["status"] == L6AR01_STATUS and l6ar02["status"] == L6AR02_STATUS,
        },
        "operation_class": L6AR03_OPERATION_CLASS,
        "endpoint": L6AR01_ENDPOINT,
        "route_audience": L6AR01_ROUTE_AUDIENCE,
        "agent": L6AR01_AGENT,
        "acting_for": L6AR01_ACTING_FOR,
        "scope": L6AR01_SCOPE,
        "n": L6AR01_N,
        "query_label": L6AR02_QUERY_LABEL,
        "evidence_class": L6AR01_EVIDENCE_CLASS,
        "auth_status": L6AR03_AUTH_STATUS,
        "denial_reason_label": L6AR03_DENIAL_REASON_LABEL,
        "degraded": L6AR03_DEGRADED,
        "degraded_flags": list(L6AR03_DEGRADED_FLAGS),
        "item_count": L6AR03_ITEM_COUNT,
        "safe_item_labels": list(L6AR03_SAFE_ITEM_LABELS),
        "attempt_count": L6AR03_ATTEMPT_COUNT,
        "second_attempt_performed": False,
        "fresh_process_boundary": "reference-agent fresh adapter process via Atlas Query",
        "report_safe_metadata_only": True,
        "max_operation_count": 1,
        "next_issue": L6AR03_NEXT_ISSUE,
        "residual_holds": list(L6AR03_RESIDUAL_HOLDS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def evaluate_l6ar03_usefulness_attempt_receipt(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Accept only the safe scalar/label shape from the one #412 attempt."""

    if not isinstance(candidate, Mapping):
        candidate = {}

    reasons: list[str] = []
    for field in L6AR01_FORBIDDEN_FIELDS.intersection(candidate.keys()):
        reasons.append(f"forbidden_field_{field}")

    expected_values = {
        "endpoint": L6AR01_ENDPOINT,
        "route_audience": L6AR01_ROUTE_AUDIENCE,
        "agent": L6AR01_AGENT,
        "acting_for": L6AR01_ACTING_FOR,
        "scope": L6AR01_SCOPE,
        "n": L6AR01_N,
        "query_label": L6AR02_QUERY_LABEL,
        "evidence_class": L6AR01_EVIDENCE_CLASS,
        "auth_status": L6AR03_AUTH_STATUS,
        "denial_reason_label": L6AR03_DENIAL_REASON_LABEL,
        "degraded": L6AR03_DEGRADED,
        "degraded_flags": list(L6AR03_DEGRADED_FLAGS),
        "item_count": L6AR03_ITEM_COUNT,
        "safe_item_labels": list(L6AR03_SAFE_ITEM_LABELS),
        "attempt_count": L6AR03_ATTEMPT_COUNT,
        "second_attempt_performed": False,
        "report_safe_metadata_only": True,
        "max_operation_count": 1,
    }
    for field, expected in expected_values.items():
        if candidate.get(field) != expected:
            reasons.append(f"wrong_{field}")

    forbidden_true_flags = {
        "raw_output_requested": "raw_output_requested",
        "raw_private_output_requested": "raw_output_requested",
        "source_discovery_requested": "source_discovery_requested",
        "broad_recall_requested": "broad_recall_requested",
        "provider_prod_requested": "provider_prod_requested",
        "canary_requested": "provider_prod_requested",
        "gate_requested": "gate_requested",
        "write_requested": "write_or_mutation_requested",
        "mutation_requested": "write_or_mutation_requested",
    }
    for flag, reason in forbidden_true_flags.items():
        if candidate.get(flag) is True:
            reasons.append(reason)

    return {
        "schema_version": L6AR03_SCHEMA_VERSION,
        "rail_issue": L6AR03_RAIL_ISSUE,
        "status": L6AR03_HELD_STATUS if reasons else L6AR03_STATUS,
        "reasons": sorted(set(reasons or ["fresh_process_metadata_usefulness_zero_item_degraded_receipt_captured"])),
        "attempt_count": L6AR03_ATTEMPT_COUNT,
        "second_attempt_performed": False,
        "next_issue": L6AR03_NEXT_ISSUE if not reasons else L6AR03_RAIL_ISSUE,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ar03_report_safe(receipt: Mapping[str, Any]) -> None:
    unsafe = set(receipt) - L6AR03_REPORT_SAFE_FIELDS
    if unsafe:
        raise AssertionError(f"unsafe L6AR.03 report fields: {sorted(unsafe)}")
    forbidden = L6AR01_FORBIDDEN_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"forbidden L6AR.03 report fields: {sorted(forbidden)}")

    preflight = receipt.get("preflight")
    if not isinstance(preflight, Mapping) or preflight.get("preflight_passed") is not True:
        raise AssertionError("L6AR.03 must prove #410/#411 preflight passed before attempt")
    if receipt.get("status") != L6AR03_STATUS:
        raise AssertionError("L6AR.03 receipt must capture the fresh-process attempt result")
    if receipt.get("attempt_count") != 1 or receipt.get("second_attempt_performed") is not False:
        raise AssertionError("L6AR.03 must record exactly one attempt and no second attempt")
    if receipt.get("item_count") != 0 or receipt.get("safe_item_labels") != []:
        raise AssertionError("L6AR.03 receipt must preserve zero-item safe labels")
    if receipt.get("degraded_flags") != list(L6AR03_DEGRADED_FLAGS):
        raise AssertionError("L6AR.03 receipt must preserve degraded flags")
    if receipt.get("report_safe_metadata_only") is not True or receipt.get("max_operation_count") != 1:
        raise AssertionError("L6AR.03 receipt must remain report-safe max-one metadata only")
    guarded = receipt.get("guarded_counters")
    if not isinstance(guarded, Mapping) or any(value != 0 for value in guarded.values()):
        raise AssertionError("L6AR.03 guarded counters must stay zero")


def build_l6ar04_trust_boundary_review() -> dict[str, Any]:
    """Review #410-#412 evidence without adding reads or authority."""

    l6ar01 = build_l6ar01_recall_authority_intake()
    l6ar02 = build_l6ar02_usefulness_candidate_packet()
    l6ar03 = build_l6ar03_fresh_process_usefulness_attempt_receipt()
    return {
        "schema_version": L6AR04_SCHEMA_VERSION,
        "repo": L6AR_REPOSITORY,
        "parent_issue": L6AR_PARENT_ISSUE,
        "rail_issue": L6AR04_RAIL_ISSUE,
        "rail_starting_source_floor": L6AR_RAIL_STARTING_SOURCE_FLOOR,
        "system_pipes_repair_floor": L6AR_SYSTEM_PIPES_REPAIR_FLOOR,
        "parent_creation_receipt": L6AR_PARENT_CREATION_RECEIPT,
        "status": L6AR04_STATUS,
        "review_verdict": L6AR04_REVIEW_VERDICT,
        "reviewed_rail_issues": [L6AR01_RAIL_ISSUE, L6AR02_RAIL_ISSUE, L6AR03_RAIL_ISSUE],
        "reviewed_statuses": {
            "l6ar01": l6ar01["status"],
            "l6ar02": l6ar02["status"],
            "l6ar03": l6ar03["status"],
        },
        "attempt_custody": {
            "endpoint": L6AR01_ENDPOINT,
            "route_audience": L6AR01_ROUTE_AUDIENCE,
            "agent": L6AR01_AGENT,
            "acting_for": L6AR01_ACTING_FOR,
            "scope": L6AR01_SCOPE,
            "n": L6AR01_N,
            "query_label": L6AR02_QUERY_LABEL,
            "auth_status": L6AR03_AUTH_STATUS,
            "degraded": L6AR03_DEGRADED,
            "degraded_flags": list(L6AR03_DEGRADED_FLAGS),
            "item_count": L6AR03_ITEM_COUNT,
            "safe_item_labels": list(L6AR03_SAFE_ITEM_LABELS),
            "attempt_count": L6AR03_ATTEMPT_COUNT,
            "second_attempt_performed": False,
            "max_operation_count": 1,
        },
        "trust_boundary_findings": [
            "fresh_stdio_boundary_used_for_the_only_attempt",
            "stale_in_chat_mcp_cache_not_treated_as_authority",
            "report_safe_scalar_label_metadata_only",
            "zero_item_degraded_result_stops_without_second_attempt",
            "no_source_discovery_or_raw_private_content_persisted",
            "no_provider_prod_canary_gate_write_or_mutation_movement",
            "guarded_counters_remain_zero",
        ],
        "residual_holds": list(L6AR04_RESIDUAL_HOLDS),
        "next_issue": L6AR04_NEXT_ISSUE,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def evaluate_l6ar04_trust_boundary_review(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Return PASS only for the exact report-safe #410-#412 trust-boundary shape."""

    if not isinstance(candidate, Mapping):
        candidate = {}

    reasons: list[str] = []
    for field in L6AR01_FORBIDDEN_FIELDS.intersection(candidate.keys()):
        reasons.append(f"forbidden_field_{field}")

    expected_values = {
        "review_verdict": L6AR04_REVIEW_VERDICT,
        "reviewed_rail_issues": [L6AR01_RAIL_ISSUE, L6AR02_RAIL_ISSUE, L6AR03_RAIL_ISSUE],
        "l6ar01_status": L6AR01_STATUS,
        "l6ar02_status": L6AR02_STATUS,
        "l6ar03_status": L6AR03_STATUS,
        "attempt_count": L6AR03_ATTEMPT_COUNT,
        "second_attempt_performed": False,
        "item_count": L6AR03_ITEM_COUNT,
        "safe_item_labels": list(L6AR03_SAFE_ITEM_LABELS),
    }
    for field, expected in expected_values.items():
        if candidate.get(field) != expected:
            reasons.append(f"wrong_{field}")

    forbidden_true_flags = {
        "retry_requested": "retry_requested",
        "second_attempt_requested": "second_attempt_requested",
        "raw_output_requested": "raw_output_requested",
        "source_discovery_requested": "source_discovery_requested",
        "broad_recall_requested": "broad_recall_requested",
        "provider_prod_requested": "provider_prod_requested",
        "canary_requested": "provider_prod_requested",
        "gate_requested": "gate_requested",
        "write_requested": "write_or_mutation_requested",
        "mutation_requested": "write_or_mutation_requested",
    }
    for flag, reason in forbidden_true_flags.items():
        if candidate.get(flag) is True:
            reasons.append(reason)

    return {
        "schema_version": L6AR04_SCHEMA_VERSION,
        "rail_issue": L6AR04_RAIL_ISSUE,
        "status": L6AR04_HELD_STATUS if reasons else L6AR04_STATUS,
        "review_verdict": "HOLD" if reasons else L6AR04_REVIEW_VERDICT,
        "reasons": sorted(set(reasons or ["post_auth_usefulness_trust_boundary_passed"])),
        "next_issue": L6AR04_NEXT_ISSUE if not reasons else L6AR04_RAIL_ISSUE,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ar04_report_safe(receipt: Mapping[str, Any]) -> None:
    unsafe = set(receipt) - L6AR04_REPORT_SAFE_FIELDS
    if unsafe:
        raise AssertionError(f"unsafe L6AR.04 report fields: {sorted(unsafe)}")
    forbidden = L6AR01_FORBIDDEN_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"forbidden L6AR.04 report fields: {sorted(forbidden)}")

    if receipt.get("status") != L6AR04_STATUS or receipt.get("review_verdict") != L6AR04_REVIEW_VERDICT:
        raise AssertionError("L6AR.04 trust-boundary review must record PASS")
    if receipt.get("reviewed_rail_issues") != [L6AR01_RAIL_ISSUE, L6AR02_RAIL_ISSUE, L6AR03_RAIL_ISSUE]:
        raise AssertionError("L6AR.04 must review only #410-#412")
    custody = receipt.get("attempt_custody")
    if not isinstance(custody, Mapping):
        raise AssertionError("L6AR.04 attempt custody must be metadata mapping")
    custody_forbidden = L6AR01_FORBIDDEN_FIELDS.intersection(custody.keys())
    if custody_forbidden:
        raise AssertionError(f"unsafe L6AR.04 custody fields: {sorted(custody_forbidden)}")
    if custody.get("attempt_count") != 1 or custody.get("second_attempt_performed") is not False:
        raise AssertionError("L6AR.04 must preserve the consumed max-one attempt boundary")
    if custody.get("item_count") != 0 or custody.get("safe_item_labels") != []:
        raise AssertionError("L6AR.04 must preserve the zero-item result")
    guarded = receipt.get("guarded_counters")
    if not isinstance(guarded, Mapping) or any(value != 0 for value in guarded.values()):
        raise AssertionError("L6AR.04 guarded counters must stay zero")


def build_l6ar05_source_floor_parent_tracker_reconciliation() -> dict[str, Any]:
    """Reconcile L6AR source floor, parent receipt, tracker text, and next frontier."""

    attempt = build_l6ar03_fresh_process_usefulness_attempt_receipt()
    review = build_l6ar04_trust_boundary_review()
    return {
        "schema_version": L6AR05_SCHEMA_VERSION,
        "repo": L6AR_REPOSITORY,
        "parent_issue": L6AR_PARENT_ISSUE,
        "rail_issue": L6AR05_RAIL_ISSUE,
        "rail_starting_source_floor": L6AR_RAIL_STARTING_SOURCE_FLOOR,
        "system_pipes_repair_floor": L6AR_SYSTEM_PIPES_REPAIR_FLOOR,
        "parent_creation_receipt": L6AR_PARENT_CREATION_RECEIPT,
        "final_pre_reconciliation_source_floor": L6AR05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR,
        "status": L6AR05_STATUS,
        "rail_anchors": [dict(anchor) for anchor in L6AR05_RAIL_ANCHORS],
        "attempt_metadata_summary": {
            "status": attempt["status"],
            "endpoint": attempt["endpoint"],
            "route_audience": attempt["route_audience"],
            "agent": attempt["agent"],
            "acting_for": attempt["acting_for"],
            "scope": attempt["scope"],
            "n": attempt["n"],
            "query_label": attempt["query_label"],
            "evidence_class": attempt["evidence_class"],
            "auth_status": attempt["auth_status"],
            "denial_reason_label": attempt["denial_reason_label"],
            "degraded": attempt["degraded"],
            "degraded_flags": attempt["degraded_flags"],
            "item_count": attempt["item_count"],
            "safe_item_labels": attempt["safe_item_labels"],
            "attempt_count": attempt["attempt_count"],
            "second_attempt_performed": attempt["second_attempt_performed"],
            "guarded_counters": attempt["guarded_counters"],
        },
        "trust_boundary_review": {
            "status": review["status"],
            "review_verdict": review["review_verdict"],
            "reviewed_rail_issues": review["reviewed_rail_issues"],
            "guarded_counters": review["guarded_counters"],
        },
        "parent_receipt_text": L6AR05_PARENT_RECEIPT_TEXT,
        "tracker_update_text": L6AR05_TRACKER_UPDATE_TEXT,
        "next_frontier": L6AR05_NEXT_FRONTIER,
        "external_tracker_written": False,
        "cron_mutated": False,
        "successor_issues_created": False,
        "second_attempt_performed": False,
        "provider_prod_canary_gate_or_write_movement_performed": False,
        "residual_holds": list(L6AR05_RESIDUAL_HOLDS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6ar05_report_safe(receipt: Mapping[str, Any]) -> None:
    unsafe = set(receipt) - L6AR05_REPORT_SAFE_FIELDS
    if unsafe:
        raise AssertionError(f"unsafe L6AR.05 report fields: {sorted(unsafe)}")
    forbidden = L6AR01_FORBIDDEN_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"forbidden L6AR.05 report fields: {sorted(forbidden)}")

    if receipt.get("status") != L6AR05_STATUS:
        raise AssertionError("L6AR.05 must record source-floor reconciliation complete")
    if receipt.get("rail_issue") != L6AR05_RAIL_ISSUE or receipt.get("parent_issue") != L6AR_PARENT_ISSUE:
        raise AssertionError("L6AR.05 must bind #414 and parent #6")
    if receipt.get("final_pre_reconciliation_source_floor") != L6AR05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR:
        raise AssertionError("L6AR.05 must preserve the final pre-reconciliation source floor")

    anchors = receipt.get("rail_anchors")
    if not isinstance(anchors, list) or [anchor.get("issue") for anchor in anchors] != [410, 411, 412, 413]:
        raise AssertionError("L6AR.05 must reconcile #410-#413 in order")
    if [anchor.get("pr") for anchor in anchors] != [415, 416, 417, 418]:
        raise AssertionError("L6AR.05 must anchor PR #415-#418")

    attempt = receipt.get("attempt_metadata_summary")
    if not isinstance(attempt, Mapping):
        raise AssertionError("L6AR.05 attempt summary must be report-safe metadata")
    attempt_forbidden = L6AR01_FORBIDDEN_FIELDS.intersection(attempt.keys())
    if attempt_forbidden:
        raise AssertionError(f"unsafe L6AR.05 attempt fields: {sorted(attempt_forbidden)}")
    if attempt.get("attempt_count") != 1 or attempt.get("second_attempt_performed") is not False:
        raise AssertionError("L6AR.05 must preserve exactly one consumed attempt and no second attempt")
    if attempt.get("item_count") != 0 or attempt.get("safe_item_labels") != []:
        raise AssertionError("L6AR.05 must preserve zero-item metadata")
    if attempt.get("degraded_flags") != list(L6AR03_DEGRADED_FLAGS):
        raise AssertionError("L6AR.05 must preserve degraded flags")

    review = receipt.get("trust_boundary_review")
    if not isinstance(review, Mapping) or review.get("review_verdict") != L6AR04_REVIEW_VERDICT:
        raise AssertionError("L6AR.05 must carry forward the #413 PASS review")

    for field in (
        "external_tracker_written",
        "cron_mutated",
        "successor_issues_created",
        "second_attempt_performed",
        "provider_prod_canary_gate_or_write_movement_performed",
    ):
        if receipt.get(field) is not False:
            raise AssertionError(f"L6AR.05 must keep {field}=false")

    for counters in (receipt.get("guarded_counters"), attempt.get("guarded_counters"), review.get("guarded_counters")):
        if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
            raise AssertionError("L6AR.05 guarded counters must remain zero")
