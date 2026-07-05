from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from memory_seam.l6al_service_auth_contract import zero_l6al03_guarded_counters
from memory_seam.l6ap_metadata_retry_rail import (
    L6AP02_AUTH_STATUS_CODE,
    L6AP02_BLOCKER_CLASSIFICATION,
    L6AP02_DENIAL_REASON,
    L6AP02_ITEMS_COUNT,
    L6AP02_SAFE_ITEM_LABELS,
    L6AP_REPOSITORY,
    build_l6ap02_safe_denial_receipt,
)

L6AQ_PARENT_ISSUE = 6
L6AQ_RAIL_STARTING_SOURCE_FLOOR = "755ab24e4ac5a283081f134cbc18c95c59d1c60e"
L6AQ01_RAIL_ISSUE = 400
L6AQ01_SCHEMA_VERSION = "l6aq01-route-audience-auth-denial-localization-v1"
L6AQ01_STATUS = "ROUTE_AUDIENCE_AUTH_DENIAL_LOCALIZED_REPAIR_TARGET_READY"
L6AQ01_REFUSED_STATUS = "ROUTE_AUDIENCE_AUTH_DENIAL_LOCALIZATION_REFUSED_BEFORE_READ"
L6AQ01_BLOCKER_CLASSIFICATION = "SERVICE_ROUTE_AUDIENCE_AUTH_BINDING_MISMATCH_LOCALIZED"
L6AQ01_REPAIR_TARGET = "memory_seam_recall_service_operator_route_audience_binding"
L6AQ01_EXPECTED_ROUTE_AUDIENCE = "memory-seam:read:recall"
L6AQ01_EXPECTED_ENDPOINT = "memory_seam_recall"
L6AQ01_EXPECTED_AGENT = "sax"
L6AQ01_EXPECTED_SCOPE = "wiki"
L6AQ01_EXPECTED_N = 3
L6AQ01_EXPECTED_QUERY_LABEL = "supervised_metadata_readiness"
L6AQ01_EXPECTED_EVIDENCE_CLASS = "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
L6AQ01_SOURCE_CONSUMPTION_SCOPE = (
    "committed L6AP report-safe retry metadata",
    "existing repo route-audience/auth contracts",
    "public issue and PR metadata only",
)
L6AQ01_PRESERVED_HOLDS = (
    "no raw/private/source content",
    "no source paths or URIs",
    "no auth payloads, provider payloads, secrets, env, keychain, OAuth, auth-file, or credential reads",
    "no source discovery or broad recall",
    "no Runtime Registry, provider callback, or service activation",
    "no provider/prod/canary/Gate/write/mutation movement",
    "no broad allowed=true",
    "no live retry and no second retry",
)
L6AQ01_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "status",
        "source_consumption_scope",
        "prior_retry_metadata",
        "expected_binding",
        "observed_denial",
        "blocker_classification",
        "repair_target",
        "repair_target_requirements",
        "preserved_holds",
        "retry_executed",
        "second_retry_performed",
        "guarded_counters",
    }
)

L6AQ02_RAIL_ISSUE = 401
L6AQ02_SCHEMA_VERSION = "l6aq02-repaired-route-audience-binding-contract-v1"
L6AQ02_STATUS = "REPAIRED_ROUTE_AUDIENCE_BINDING_CONTRACT_READY_DEFAULT_OFF"
L6AQ02_READY_STATUS = "REPAIRED_ROUTE_AUDIENCE_BINDING_READY_RETRY_STILL_DEFAULT_OFF"
L6AQ02_HELD_STATUS = "REPAIRED_ROUTE_AUDIENCE_BINDING_HELD_BEFORE_READ"
L6AQ02_DENIED_STATUS = "REPAIRED_ROUTE_AUDIENCE_BINDING_DENIED_BEFORE_READ"
L6AQ02_BINDING_REF = "operator-service-binding:l6aq02:memory-seam-recall-route-audience:max-one"
L6AQ02_ONE_RUN_CUSTODY = "one-run-custody:l6aq02:#403-preflight-only"
L6AQ02_OPERATION_CLASS = "memory_seam_recall_report_safe_metadata_retry"
L6AQ02_DEFAULT_OFF_UNTIL = "issue_403_preflight_and_max_one_retry_authority_pass"
L6AQ02_ALLOWED_CONTRACT_FIELDS = frozenset(
    {
        "operator_service_binding_ref",
        "binding_owner",
        "identity_subject",
        "endpoint",
        "route_audience",
        "acting_for",
        "agent",
        "scope",
        "n",
        "query_label",
        "evidence_class",
        "operation_class",
        "max_operation_count",
        "report_safe_metadata_only",
        "denial_before_read_required",
        "expires_at_or_one_run_custody",
        "binding_fresh",
        "default_off_until_issue_403_preflight",
        "retry_authorized_by_contract",
    }
)
L6AQ02_REQUIRED_CONTRACT_FIELDS = frozenset(
    {
        "operator_service_binding_ref",
        "binding_owner",
        "identity_subject",
        "endpoint",
        "route_audience",
        "acting_for",
        "agent",
        "scope",
        "n",
        "query_label",
        "evidence_class",
        "operation_class",
        "max_operation_count",
        "report_safe_metadata_only",
        "denial_before_read_required",
        "expires_at_or_one_run_custody",
        "binding_fresh",
        "default_off_until_issue_403_preflight",
        "retry_authorized_by_contract",
    }
)
L6AQ02_FORBIDDEN_TRUE_FLAGS = {
    "raw_output_requested": "raw_output_requested",
    "raw_private_output_requested": "raw_output_requested",
    "provider_payload_requested": "provider_payload_requested",
    "auth_payload_requested": "auth_payload_requested",
    "credential_read_requested": "credential_read_requested",
    "secret_env_keychain_oauth_auth_file_requested": "credential_read_requested",
    "source_discovery_requested": "source_discovery_requested",
    "broad_recall_requested": "source_discovery_requested",
    "runtime_registry_requested": "runtime_registry_requested",
    "provider_callback_requested": "provider_callback_requested",
    "service_activation_requested": "service_activation_requested",
    "provider_prod_requested": "provider_prod_requested",
    "canary_requested": "provider_prod_requested",
    "gate_requested": "gate_requested",
    "write_requested": "write_requested",
    "mutation_requested": "write_requested",
    "allowed": "broad_allowed_true",
    "broad_allowed": "broad_allowed_true",
}
L6AQ02_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "status",
        "repair_target",
        "operation_class",
        "binding_contract",
        "preflight_requirement",
        "default_off_until",
        "mismatch_cases_covered",
        "preserved_holds",
        "retry_executed",
        "second_retry_performed",
        "guarded_counters",
    }
)
L6AQ02_VALIDATION_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "status",
        "reasons",
        "ready_metadata",
        "retry_executed",
        "second_retry_performed",
        "guarded_counters",
    }
)

L6AQ03_RAIL_ISSUE = 402
L6AQ03_SCHEMA_VERSION = "l6aq03-operator-service-configuration-proof-v1"
L6AQ03_STATUS = "OPERATOR_SERVICE_CONFIGURATION_PROOF_READY_RETRY_STILL_DEFAULT_OFF"
L6AQ03_READY_STATUS = "OPERATOR_SERVICE_CONFIGURATION_PREFLIGHT_READY_RETRY_STILL_DEFAULT_OFF"
L6AQ03_HELD_STATUS = "OPERATOR_SERVICE_CONFIGURATION_HELD_BEFORE_READ"
L6AQ03_DENIED_STATUS = "OPERATOR_SERVICE_CONFIGURATION_DENIED_BEFORE_READ"
L6AQ03_ISSUE_BOUND_AUTHORITY = "issue-bound:#402-only-proof:#403-max-one-preflight"
L6AQ03_ONE_RUN_BINDING = "one-run:max-one:#403-only-after-l6aq03-pass"
L6AQ03_ALLOWED_PROOF_FIELDS = L6AQ02_ALLOWED_CONTRACT_FIELDS | frozenset(
    {
        "configuration_proof_issue",
        "issue_bound_authority",
        "one_run_binding",
        "metadata_only_output_contract",
        "denial_before_read_stop",
        "retry_authorized_by_configuration_proof",
    }
)
L6AQ03_REQUIRED_PROOF_FIELDS = L6AQ03_ALLOWED_PROOF_FIELDS
L6AQ03_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "status",
        "operation_class",
        "configuration_proof",
        "preflight_result",
        "narrowness_proof",
        "refusal_cases_covered",
        "preserved_holds",
        "retry_executed",
        "second_retry_performed",
        "guarded_counters",
    }
)
L6AQ03_VALIDATION_FIELDS = frozenset(
    {
        "schema_version",
        "rail_issue",
        "status",
        "reasons",
        "preflight_metadata",
        "retry_executed",
        "second_retry_performed",
        "guarded_counters",
    }
)

L6AQ04_RAIL_ISSUE = 403
L6AQ04_SCHEMA_VERSION = "l6aq04-post-repair-metadata-retry-denial-receipt-v1"
L6AQ04_STATUS = "POST_REPAIR_METADATA_RETRY_DENIED_BEFORE_READ_NO_ITEMS"
L6AQ04_BLOCKER_CLASSIFICATION = "SERVICE_ROUTE_AUDIENCE_AUTH_BINDING_STILL_DENIED_AFTER_REPAIR_PROOF"
L6AQ04_RETRY_OPERATION_COUNT = 1
L6AQ04_AUTH_STATUS_CODE = 403
L6AQ04_DENIAL_REASON = "wrong_route_audience"
L6AQ04_ITEMS_COUNT = 0
L6AQ04_SAFE_ITEM_LABELS: tuple[str, ...] = ()
L6AQ04_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "status",
        "blocker_classification",
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
        "residual_holds",
    }
)

L6AQ05_RAIL_ISSUE = 404
L6AQ05_SCHEMA_VERSION = "l6aq05-post-repair-source-floor-parent-tracker-reconciliation-v1"
L6AQ05_STATUS = "POST_REPAIR_RETRY_RECONCILED_STEP3_HELD_WRONG_ROUTE_AUDIENCE"
L6AQ05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR = "d3ee131fbe566066da60b4b61a7e11957fb65352"
L6AQ05_RAIL_ANCHORS = (
    {
        "issue": 400,
        "pr": 405,
        "merge_commit": "2975e5cbe301fab1333306f860993c8b5948b51c",
        "artifact": "L6AQ.01 route-audience auth denial localization",
    },
    {
        "issue": 401,
        "pr": 406,
        "merge_commit": "8a82c149455540c134e080735f947dba24c12034",
        "artifact": "L6AQ.02 repaired route-audience binding contract",
    },
    {
        "issue": 402,
        "pr": 407,
        "merge_commit": "09428d5c4078bc2b9793916aed05b33958fc66f6",
        "artifact": "L6AQ.03 operator/service configuration proof",
    },
    {
        "issue": 403,
        "pr": 408,
        "merge_commit": L6AQ05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR,
        "artifact": "L6AQ.04 post-repair metadata retry denial receipt",
    },
)
L6AQ05_PARENT_RECEIPT_TEXT = (
    "Parent #6 receipt: L6AQ route-audience repair rail complete through source-floor "
    "reconciliation. Issues #400-#404 and PRs #405-#409 record denial localization, "
    "repaired binding contract, operator/service configuration proof, one post-repair "
    "report-safe metadata retry, denied-before-read safe metadata, and final reconciliation. "
    "Retry summary: memory_seam_recall / memory-seam:read:recall / sax / wiki / n=3 / "
    "supervised_metadata_readiness / SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE returned "
    "auth_status_code=403, denial_reason=wrong_route_audience, items_count=0, "
    "safe_item_labels=[], retry_operation_count=1, second_retry_performed=false, no second "
    "retry, guarded counters zero. Step 3 remains held on the service route-audience auth "
    "binding blocker; no successor issues, external tracker write, cron mutation, service "
    "activation, provider/prod/canary/Gate/write movement, or broad allowed=true behavior "
    "occurred."
)
L6AQ05_TRACKER_UPDATE_TEXT = (
    "Atlas tracker update text: mark Memory Seam roadmap Step 3 as POST-REPAIR METADATA "
    "RETRY ATTEMPTED / DENIED-BEFORE-READ / USEFULNESS HELD at source floor "
    "d3ee131fbe566066da60b4b61a7e11957fb65352; record #400-#404 and PR #405-#409 as "
    "the L6AQ route-audience repair and post-repair retry reconciliation rail. Record retry "
    "metadata only: endpoint memory_seam_recall, route audience memory-seam:read:recall, "
    "agent sax, scope wiki, n=3, query_label supervised_metadata_readiness, evidence_class "
    "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE, denial_reason wrong_route_audience, "
    "auth_status_code 403, items_count 0, safe_item_labels empty, retry count 1, no second "
    "retry, guarded counters zero. Exact blocker remains service route-audience auth binding; "
    "do not create or run another retry from this rail; writer performed no external tracker "
    "write and no cron mutation."
)
L6AQ05_RESIDUAL_HOLDS = (
    "step3_current_session_usefulness",
    "service_route_audience_auth_binding_blocker",
    "successor_issue_creation_from_this_writer",
    "second_retry",
    "raw_private_source_content_or_source_path_uri",
    "auth_provider_payload_secret_env_keychain_oauth_auth_file_or_credential_reads",
    "runtime_registry_provider_callback_or_service_activation",
    "source_discovery_broad_recall_or_broad_allowed_true",
    "external_tracker_write_or_cron_mutation_from_writer",
    "provider_prod_canary_gate_atlas_gate_write_or_mutation",
)
L6AQ05_RECEIPT_FIELDS = frozenset(
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
        "exact_blocker",
        "parent_receipt_text",
        "tracker_update_text",
        "external_tracker_written",
        "cron_mutated",
        "successor_issues_created",
        "second_retry_performed",
        "provider_prod_canary_gate_or_write_movement_performed",
        "residual_holds",
        "guarded_counters",
    }
)

L6AQ01_PRIOR_RETRY_FIELDS = frozenset(
    {
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
        "retry_operation_count",
        "second_retry_performed",
        "report_safe_metadata_only",
        "denial_before_read_required",
    }
)
L6AQ01_FORBIDDEN_FIELDS = frozenset(
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
        "allowed",
        "broad_allowed",
    }
)


def _prior_retry_metadata() -> dict[str, Any]:
    receipt = build_l6ap02_safe_denial_receipt()
    return {field: receipt[field] for field in L6AQ01_PRIOR_RETRY_FIELDS}


def build_l6aq01_route_audience_denial_localization() -> dict[str, Any]:
    """Localize the prior report-safe recall denial without reading source or auth payloads."""

    retry = _prior_retry_metadata()
    return {
        "schema_version": L6AQ01_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AQ_PARENT_ISSUE,
        "rail_issue": L6AQ01_RAIL_ISSUE,
        "rail_starting_source_floor": L6AQ_RAIL_STARTING_SOURCE_FLOOR,
        "status": L6AQ01_STATUS,
        "source_consumption_scope": list(L6AQ01_SOURCE_CONSUMPTION_SCOPE),
        "prior_retry_metadata": retry,
        "expected_binding": {
            "endpoint": L6AQ01_EXPECTED_ENDPOINT,
            "route_audience": L6AQ01_EXPECTED_ROUTE_AUDIENCE,
            "agent": L6AQ01_EXPECTED_AGENT,
            "scope": L6AQ01_EXPECTED_SCOPE,
            "n": L6AQ01_EXPECTED_N,
            "query_label": L6AQ01_EXPECTED_QUERY_LABEL,
            "evidence_class": L6AQ01_EXPECTED_EVIDENCE_CLASS,
            "report_safe_metadata_only": True,
            "denial_before_read_required": True,
            "max_operation_count": 1,
        },
        "observed_denial": {
            "denial_reason": L6AP02_DENIAL_REASON,
            "auth_status_code": L6AP02_AUTH_STATUS_CODE,
            "items_count": L6AP02_ITEMS_COUNT,
            "safe_item_labels": list(L6AP02_SAFE_ITEM_LABELS),
            "denied_before_read": True,
        },
        "blocker_classification": L6AQ01_BLOCKER_CLASSIFICATION,
        "repair_target": L6AQ01_REPAIR_TARGET,
        "repair_target_requirements": [
            "bind memory_seam_recall to route audience memory-seam:read:recall for agent sax and scope wiki",
            "preserve metadata-only output and denial-before-read behavior",
            "keep the repair default-off until later preflight and exact max-one retry authorization pass",
            "refuse broad allowed=true or route-audience broadening",
        ],
        "preserved_holds": list(L6AQ01_PRESERVED_HOLDS),
        "retry_executed": False,
        "second_retry_performed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def evaluate_l6aq01_route_audience_localization_input(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Fail closed unless candidate metadata matches the report-safe L6AP denial shape."""

    if not isinstance(candidate, Mapping):
        candidate = {}

    reasons: list[str] = []
    for field in L6AQ01_FORBIDDEN_FIELDS.intersection(candidate.keys()):
        reasons.append(f"forbidden_field_{field}")

    expected_values = {
        "endpoint": L6AQ01_EXPECTED_ENDPOINT,
        "route_audience": L6AQ01_EXPECTED_ROUTE_AUDIENCE,
        "agent": L6AQ01_EXPECTED_AGENT,
        "scope": L6AQ01_EXPECTED_SCOPE,
        "n": L6AQ01_EXPECTED_N,
        "query_label": L6AQ01_EXPECTED_QUERY_LABEL,
        "evidence_class": L6AQ01_EXPECTED_EVIDENCE_CLASS,
        "denial_reason": L6AP02_DENIAL_REASON,
        "auth_status_code": L6AP02_AUTH_STATUS_CODE,
        "items_count": L6AP02_ITEMS_COUNT,
        "safe_item_labels": list(L6AP02_SAFE_ITEM_LABELS),
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
        "retry_operation_count": 1,
        "second_retry_performed": False,
    }
    for field, expected in expected_values.items():
        if candidate.get(field) != expected:
            reasons.append(f"wrong_{field}")

    forbidden_true_flags = {
        "raw_output_requested": "raw_output_requested",
        "raw_private_output_requested": "raw_output_requested",
        "source_discovery_requested": "source_discovery_requested",
        "broad_recall_requested": "source_discovery_requested",
        "runtime_registry_requested": "runtime_registry_requested",
        "provider_callback_requested": "provider_callback_requested",
        "service_activation_requested": "service_activation_requested",
        "provider_prod_requested": "provider_prod_requested",
        "canary_requested": "provider_prod_requested",
        "gate_requested": "gate_requested",
        "write_requested": "write_requested",
        "mutation_requested": "write_requested",
    }
    for flag, reason in forbidden_true_flags.items():
        if candidate.get(flag) is True:
            reasons.append(reason)

    localized = not reasons
    return {
        "schema_version": L6AQ01_SCHEMA_VERSION,
        "rail_issue": L6AQ01_RAIL_ISSUE,
        "status": L6AQ01_STATUS if localized else L6AQ01_REFUSED_STATUS,
        "reasons": sorted(set(reasons or ["report_safe_wrong_route_audience_denial_localized"])),
        "blocker_classification": L6AQ01_BLOCKER_CLASSIFICATION if localized else L6AP02_BLOCKER_CLASSIFICATION,
        "repair_target": L6AQ01_REPAIR_TARGET if localized else None,
        "retry_executed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def build_l6aq02_repaired_binding_contract_fixture() -> dict[str, Any]:
    """Return the report-safe repaired route-audience binding contract fixture."""

    return {
        "operator_service_binding_ref": L6AQ02_BINDING_REF,
        "binding_owner": "service-owner-or-operator",
        "identity_subject": "supervised service caller bound to sax",
        "endpoint": L6AQ01_EXPECTED_ENDPOINT,
        "route_audience": L6AQ01_EXPECTED_ROUTE_AUDIENCE,
        "acting_for": L6AQ01_EXPECTED_AGENT,
        "agent": L6AQ01_EXPECTED_AGENT,
        "scope": L6AQ01_EXPECTED_SCOPE,
        "n": L6AQ01_EXPECTED_N,
        "query_label": L6AQ01_EXPECTED_QUERY_LABEL,
        "evidence_class": L6AQ01_EXPECTED_EVIDENCE_CLASS,
        "operation_class": L6AQ02_OPERATION_CLASS,
        "max_operation_count": 1,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
        "expires_at_or_one_run_custody": L6AQ02_ONE_RUN_CUSTODY,
        "binding_fresh": True,
        "default_off_until_issue_403_preflight": True,
        "retry_authorized_by_contract": False,
    }


def build_l6aq02_repaired_route_audience_binding_contract() -> dict[str, Any]:
    """Define the default-off repaired binding contract without executing recall."""

    return {
        "schema_version": L6AQ02_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AQ_PARENT_ISSUE,
        "rail_issue": L6AQ02_RAIL_ISSUE,
        "rail_starting_source_floor": L6AQ_RAIL_STARTING_SOURCE_FLOOR,
        "status": L6AQ02_STATUS,
        "repair_target": L6AQ01_REPAIR_TARGET,
        "operation_class": L6AQ02_OPERATION_CLASS,
        "binding_contract": build_l6aq02_repaired_binding_contract_fixture(),
        "preflight_requirement": {
            "issue": 403,
            "endpoint": L6AQ01_EXPECTED_ENDPOINT,
            "agent": L6AQ01_EXPECTED_AGENT,
            "scope": L6AQ01_EXPECTED_SCOPE,
            "n": L6AQ01_EXPECTED_N,
            "query_label": L6AQ01_EXPECTED_QUERY_LABEL,
            "evidence_class": L6AQ01_EXPECTED_EVIDENCE_CLASS,
            "max_operation_count": 1,
            "report_safe_metadata_only": True,
            "denial_before_read_required": True,
        },
        "default_off_until": L6AQ02_DEFAULT_OFF_UNTIL,
        "mismatch_cases_covered": [
            "wrong_route_audience",
            "missing_binding",
            "stale_binding",
            "broadened_audience",
            "broad_allowed_true",
            "raw_output",
            "provider_prod_canary_gate_write_movement",
            "runtime_registry_provider_callback_service_activation",
        ],
        "preserved_holds": list(L6AQ01_PRESERVED_HOLDS),
        "retry_executed": False,
        "second_retry_performed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def validate_l6aq02_repaired_binding_contract(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Validate repaired binding metadata, denying before read on mismatches or broadening."""

    reasons: list[str] = []
    status = L6AQ02_READY_STATUS
    if not isinstance(candidate, Mapping):
        candidate = {}

    unsafe_keys = L6AQ01_FORBIDDEN_FIELDS.intersection(candidate.keys())
    for field in unsafe_keys:
        reasons.append(f"forbidden_field_{field}")
        status = L6AQ02_DENIED_STATUS

    unexpected = set(candidate.keys()).difference(L6AQ02_ALLOWED_CONTRACT_FIELDS | set(L6AQ02_FORBIDDEN_TRUE_FLAGS))
    if unexpected:
        for field in sorted(unexpected):
            reasons.append(f"unexpected_field_{field}")
        status = L6AQ02_DENIED_STATUS

    missing = sorted(
        field
        for field in L6AQ02_REQUIRED_CONTRACT_FIELDS
        if field not in candidate or candidate.get(field) in {None, ""}
    )
    if missing:
        reasons.append("missing_binding")
        status = L6AQ02_HELD_STATUS if status != L6AQ02_DENIED_STATUS else status

    if candidate.get("expires_at_or_one_run_custody") in {"expired", "stale", "revoked"}:
        reasons.append("stale_binding")
        status = L6AQ02_HELD_STATUS if status != L6AQ02_DENIED_STATUS else status
    if candidate.get("binding_fresh") is False:
        reasons.append("stale_binding")
        status = L6AQ02_HELD_STATUS if status != L6AQ02_DENIED_STATUS else status

    expected = build_l6aq02_repaired_binding_contract_fixture()
    for field in (
        "endpoint",
        "route_audience",
        "acting_for",
        "agent",
        "scope",
        "n",
        "query_label",
        "evidence_class",
        "operation_class",
        "max_operation_count",
        "report_safe_metadata_only",
        "denial_before_read_required",
        "default_off_until_issue_403_preflight",
        "retry_authorized_by_contract",
    ):
        if field in candidate and candidate.get(field) != expected[field]:
            if field == "route_audience" and str(candidate.get(field, "")).endswith("*"):
                reasons.append("broadened_audience")
            else:
                reasons.append(f"wrong_{field}")
            status = L6AQ02_DENIED_STATUS

    for flag, reason in L6AQ02_FORBIDDEN_TRUE_FLAGS.items():
        if candidate.get(flag) is True:
            reasons.append(reason)
            status = L6AQ02_DENIED_STATUS

    if candidate.get("retry_authorized_by_contract") is True:
        reasons.append("contract_attempted_to_authorize_retry")
        status = L6AQ02_DENIED_STATUS
    if candidate.get("default_off_until_issue_403_preflight") is False:
        reasons.append("default_off_bypassed")
        status = L6AQ02_DENIED_STATUS

    if not reasons:
        reasons.append("repaired_route_audience_binding_ready_retry_still_default_off")

    return {
        "schema_version": L6AQ02_SCHEMA_VERSION,
        "rail_issue": L6AQ02_RAIL_ISSUE,
        "status": status,
        "reasons": sorted(set(reasons)),
        "ready_metadata": {
            "operator_service_binding_ref_present": bool(candidate.get("operator_service_binding_ref")),
            "endpoint": candidate.get("endpoint"),
            "route_audience": candidate.get("route_audience"),
            "agent": candidate.get("agent"),
            "scope": candidate.get("scope"),
            "n": candidate.get("n"),
            "query_label": candidate.get("query_label"),
            "evidence_class": candidate.get("evidence_class"),
            "max_operation_count": candidate.get("max_operation_count"),
            "report_safe_metadata_only": candidate.get("report_safe_metadata_only"),
            "denial_before_read_required": candidate.get("denial_before_read_required"),
            "default_off_until_issue_403_preflight": candidate.get("default_off_until_issue_403_preflight"),
            "retry_authorized_by_contract": candidate.get("retry_authorized_by_contract"),
        },
        "retry_executed": False,
        "second_retry_performed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }



def build_l6aq03_operator_service_configuration_proof_fixture() -> dict[str, Any]:
    """Return the report-safe operator/service configuration proof fixture."""

    contract = build_l6aq02_repaired_binding_contract_fixture()
    return contract | {
        "configuration_proof_issue": L6AQ03_RAIL_ISSUE,
        "issue_bound_authority": L6AQ03_ISSUE_BOUND_AUTHORITY,
        "one_run_binding": L6AQ03_ONE_RUN_BINDING,
        "metadata_only_output_contract": True,
        "denial_before_read_stop": True,
        "retry_authorized_by_configuration_proof": False,
    }


def validate_l6aq03_operator_service_configuration_proof(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Validate the #402 operator/service config proof without executing recall."""

    reasons: list[str] = []
    status = L6AQ03_READY_STATUS
    if not isinstance(candidate, Mapping):
        candidate = {}

    unexpected = set(candidate.keys()).difference(L6AQ03_ALLOWED_PROOF_FIELDS | set(L6AQ02_FORBIDDEN_TRUE_FLAGS) | L6AQ01_FORBIDDEN_FIELDS)
    for field in sorted(unexpected):
        reasons.append(f"unexpected_field_{field}")
        status = L6AQ03_DENIED_STATUS

    forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(candidate.keys())
    for field in sorted(forbidden):
        reasons.append(f"forbidden_field_{field}")
        status = L6AQ03_DENIED_STATUS

    missing = sorted(
        field
        for field in L6AQ03_REQUIRED_PROOF_FIELDS
        if field not in candidate or candidate.get(field) in {None, ""}
    )
    if missing:
        reasons.append("missing_configuration_proof")
        status = L6AQ03_HELD_STATUS if status != L6AQ03_DENIED_STATUS else status

    contract_candidate = {field: candidate[field] for field in L6AQ02_ALLOWED_CONTRACT_FIELDS if field in candidate}
    contract_validation = validate_l6aq02_repaired_binding_contract(contract_candidate)
    if contract_validation["status"] == L6AQ02_HELD_STATUS:
        reasons.extend(contract_validation["reasons"])
        reasons.append("underlying_binding_held")
        status = L6AQ03_HELD_STATUS if status != L6AQ03_DENIED_STATUS else status
    elif contract_validation["status"] == L6AQ02_DENIED_STATUS:
        reasons.extend(contract_validation["reasons"])
        status = L6AQ03_DENIED_STATUS

    expected = build_l6aq03_operator_service_configuration_proof_fixture()
    for field in (
        "configuration_proof_issue",
        "issue_bound_authority",
        "one_run_binding",
        "metadata_only_output_contract",
        "denial_before_read_stop",
        "retry_authorized_by_configuration_proof",
    ):
        if field in candidate and candidate.get(field) != expected[field]:
            reasons.append(f"wrong_{field}")
            status = L6AQ03_DENIED_STATUS

    if candidate.get("retry_authorized_by_configuration_proof") is True:
        reasons.append("configuration_proof_attempted_to_authorize_retry")
        status = L6AQ03_DENIED_STATUS
    if candidate.get("max_operation_count", 1) != 1:
        reasons.append("multi_operation_requested")
        status = L6AQ03_DENIED_STATUS

    for flag, reason in L6AQ02_FORBIDDEN_TRUE_FLAGS.items():
        if candidate.get(flag) is True:
            reasons.append(reason)
            status = L6AQ03_DENIED_STATUS

    if not reasons:
        reasons.append("operator_service_configuration_ready_retry_still_default_off")

    return {
        "schema_version": L6AQ03_SCHEMA_VERSION,
        "rail_issue": L6AQ03_RAIL_ISSUE,
        "status": status,
        "reasons": sorted(set(reasons)),
        "preflight_metadata": {
            "endpoint": candidate.get("endpoint"),
            "route_audience": candidate.get("route_audience"),
            "agent": candidate.get("agent"),
            "scope": candidate.get("scope"),
            "n": candidate.get("n"),
            "query_label": candidate.get("query_label"),
            "evidence_class": candidate.get("evidence_class"),
            "max_operation_count": candidate.get("max_operation_count"),
            "report_safe_metadata_only": candidate.get("report_safe_metadata_only"),
            "denial_before_read_required": candidate.get("denial_before_read_required"),
            "configuration_proof_issue": candidate.get("configuration_proof_issue"),
            "issue_bound_authority": candidate.get("issue_bound_authority"),
            "one_run_binding": candidate.get("one_run_binding"),
            "retry_authorized_by_configuration_proof": candidate.get("retry_authorized_by_configuration_proof"),
        },
        "retry_executed": False,
        "second_retry_performed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def build_l6aq03_operator_service_configuration_proof() -> dict[str, Any]:
    """Bind the #402 operator/service config proof without executing recall."""

    proof = build_l6aq03_operator_service_configuration_proof_fixture()
    return {
        "schema_version": L6AQ03_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AQ_PARENT_ISSUE,
        "rail_issue": L6AQ03_RAIL_ISSUE,
        "rail_starting_source_floor": L6AQ_RAIL_STARTING_SOURCE_FLOOR,
        "status": L6AQ03_STATUS,
        "operation_class": L6AQ02_OPERATION_CLASS,
        "configuration_proof": proof,
        "preflight_result": validate_l6aq03_operator_service_configuration_proof(proof),
        "narrowness_proof": {
            "endpoint": L6AQ01_EXPECTED_ENDPOINT,
            "route_audience": L6AQ01_EXPECTED_ROUTE_AUDIENCE,
            "agent": L6AQ01_EXPECTED_AGENT,
            "scope": L6AQ01_EXPECTED_SCOPE,
            "n": L6AQ01_EXPECTED_N,
            "query_label": L6AQ01_EXPECTED_QUERY_LABEL,
            "evidence_class": L6AQ01_EXPECTED_EVIDENCE_CLASS,
            "max_operation_count": 1,
            "report_safe_metadata_only": True,
            "denial_before_read_required": True,
            "issue_bound": True,
            "retry_authorized": False,
        },
        "refusal_cases_covered": [
            "stale_binding",
            "broadened_audience",
            "copied_or_wrong_issue_authority",
            "missing_configuration_proof",
            "multi_operation_requested",
            "raw_output_requested",
            "secret_or_credential_read_requested",
            "source_discovery_or_broad_recall_requested",
            "runtime_registry_provider_callback_service_activation",
            "provider_prod_canary_gate_write_movement",
            "broad_allowed_true",
        ],
        "preserved_holds": list(L6AQ01_PRESERVED_HOLDS),
        "retry_executed": False,
        "second_retry_performed": False,
        "guarded_counters": zero_l6al03_guarded_counters(),
    }



def build_l6aq04_post_repair_metadata_retry_receipt() -> dict[str, Any]:
    """Return report-safe metadata from the one authorized L6AQ.04 retry attempt."""

    config_proof = build_l6aq03_operator_service_configuration_proof_fixture()
    preflight = validate_l6aq03_operator_service_configuration_proof(config_proof)
    return {
        "schema_version": L6AQ04_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AQ_PARENT_ISSUE,
        "rail_issue": L6AQ04_RAIL_ISSUE,
        "rail_starting_source_floor": L6AQ_RAIL_STARTING_SOURCE_FLOOR,
        "status": L6AQ04_STATUS,
        "blocker_classification": L6AQ04_BLOCKER_CLASSIFICATION,
        "preflight": {
            "binding_contract_status": validate_l6aq02_repaired_binding_contract(
                build_l6aq02_repaired_binding_contract_fixture()
            )["status"],
            "configuration_proof_status": preflight["status"],
            "preflight_passed": preflight["status"] == L6AQ03_READY_STATUS,
            "retry_authorized_only_by_issue_403": True,
        },
        "operation_class": L6AQ02_OPERATION_CLASS,
        "endpoint": L6AQ01_EXPECTED_ENDPOINT,
        "route_audience": L6AQ01_EXPECTED_ROUTE_AUDIENCE,
        "agent": L6AQ01_EXPECTED_AGENT,
        "acting_for": L6AQ01_EXPECTED_AGENT,
        "scope": L6AQ01_EXPECTED_SCOPE,
        "n": L6AQ01_EXPECTED_N,
        "query_label": L6AQ01_EXPECTED_QUERY_LABEL,
        "evidence_class": L6AQ01_EXPECTED_EVIDENCE_CLASS,
        "items_count": L6AQ04_ITEMS_COUNT,
        "safe_item_labels": list(L6AQ04_SAFE_ITEM_LABELS),
        "denial_reason": L6AQ04_DENIAL_REASON,
        "auth_status_code": L6AQ04_AUTH_STATUS_CODE,
        "partial": True,
        "degraded": True,
        "guarded_counters": zero_l6al03_guarded_counters(),
        "max_operation_count": 1,
        "retry_operation_count": L6AQ04_RETRY_OPERATION_COUNT,
        "second_retry_performed": False,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
        "residual_holds": list(L6AQ01_PRESERVED_HOLDS),
    }


def assert_l6aq04_retry_receipt_report_safe(receipt: Mapping[str, Any]) -> None:
    forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AQ.04 report fields present: {sorted(forbidden)}")
    unexpected = set(receipt.keys()).difference(L6AQ04_REPORT_SAFE_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AQ.04 report fields present: {sorted(unexpected)}")
    if receipt.get("status") != L6AQ04_STATUS:
        raise AssertionError("L6AQ.04 receipt must capture the post-repair denial result")
    preflight = receipt.get("preflight")
    if not isinstance(preflight, Mapping) or preflight.get("preflight_passed") is not True:
        raise AssertionError("L6AQ.04 must prove #401/#402 preflight passed before retry")
    if preflight.get("binding_contract_status") != L6AQ02_READY_STATUS:
        raise AssertionError("L6AQ.04 binding preflight must validate as ready/default-off")
    if preflight.get("configuration_proof_status") != L6AQ03_READY_STATUS:
        raise AssertionError("L6AQ.04 configuration preflight must validate as ready/default-off")
    if receipt.get("endpoint") != L6AQ01_EXPECTED_ENDPOINT:
        raise AssertionError("L6AQ.04 receipt must name the approved endpoint metadata")
    if receipt.get("route_audience") != L6AQ01_EXPECTED_ROUTE_AUDIENCE:
        raise AssertionError("L6AQ.04 receipt must preserve the repaired route audience label")
    if receipt.get("auth_status_code") != L6AQ04_AUTH_STATUS_CODE:
        raise AssertionError("L6AQ.04 receipt must preserve the safe auth status code")
    if receipt.get("denial_reason") != L6AQ04_DENIAL_REASON:
        raise AssertionError("L6AQ.04 receipt must classify the denial before read")
    if receipt.get("items_count") != 0 or receipt.get("safe_item_labels") != []:
        raise AssertionError("L6AQ.04 denied retry must have zero items and no safe labels")
    if receipt.get("retry_operation_count") != 1 or receipt.get("second_retry_performed") is not False:
        raise AssertionError("L6AQ.04 receipt must prove exactly one retry and no second retry")
    if receipt.get("report_safe_metadata_only") is not True or receipt.get("denial_before_read_required") is not True:
        raise AssertionError("L6AQ.04 receipt must remain metadata-only with denial-before-read required")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero after L6AQ.04 denial-before-read")


def build_l6aq05_post_repair_reconciliation() -> dict[str, Any]:
    """Reconcile L6AQ using only report-safe retry metadata and public rail anchors."""

    retry = build_l6aq04_post_repair_metadata_retry_receipt()
    retry_metadata = {
        "status": retry["status"],
        "endpoint": retry["endpoint"],
        "route_audience": retry["route_audience"],
        "agent": retry["agent"],
        "acting_for": retry["acting_for"],
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
        "schema_version": L6AQ05_SCHEMA_VERSION,
        "repo": L6AP_REPOSITORY,
        "parent_issue": L6AQ_PARENT_ISSUE,
        "rail_issue": L6AQ05_RAIL_ISSUE,
        "status": L6AQ05_STATUS,
        "rail_starting_source_floor": L6AQ_RAIL_STARTING_SOURCE_FLOOR,
        "final_pre_reconciliation_source_floor": L6AQ05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR,
        "rail_anchors": [dict(anchor) for anchor in L6AQ05_RAIL_ANCHORS],
        "retry_metadata_summary": retry_metadata,
        "step3_state": "USEFULNESS_HELD_DENIED_EMPTY_METADATA",
        "final_result": "post-repair retry reconciled; Step 3 usefulness remains held",
        "exact_blocker": L6AQ04_BLOCKER_CLASSIFICATION,
        "parent_receipt_text": L6AQ05_PARENT_RECEIPT_TEXT,
        "tracker_update_text": L6AQ05_TRACKER_UPDATE_TEXT,
        "external_tracker_written": False,
        "cron_mutated": False,
        "successor_issues_created": False,
        "second_retry_performed": False,
        "provider_prod_canary_gate_or_write_movement_performed": False,
        "residual_holds": list(L6AQ05_RESIDUAL_HOLDS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6aq05_reconciliation_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AQ05_RECEIPT_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AQ.05 reconciliation fields present: {sorted(unexpected)}")
    forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AQ.05 report fields present: {sorted(forbidden)}")
    if receipt.get("status") != L6AQ05_STATUS:
        raise AssertionError("L6AQ.05 status must record final post-repair retry reconciliation")
    if receipt.get("rail_issue") != L6AQ05_RAIL_ISSUE or receipt.get("parent_issue") != L6AQ_PARENT_ISSUE:
        raise AssertionError("L6AQ.05 must bind the final rail issue and parent issue")
    if receipt.get("rail_starting_source_floor") != L6AQ_RAIL_STARTING_SOURCE_FLOOR:
        raise AssertionError("L6AQ.05 must preserve the rail starting source floor")
    if receipt.get("final_pre_reconciliation_source_floor") != L6AQ05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR:
        raise AssertionError("L6AQ.05 must anchor the final pre-reconciliation source floor")

    anchors = receipt.get("rail_anchors")
    if not isinstance(anchors, list) or [anchor.get("issue") for anchor in anchors] != [400, 401, 402, 403]:
        raise AssertionError("L6AQ.05 must reconcile #400-#403 in order")
    if [anchor.get("pr") for anchor in anchors] != [405, 406, 407, 408]:
        raise AssertionError("L6AQ.05 must anchor PR #405-#408")

    retry_metadata = receipt.get("retry_metadata_summary")
    if not isinstance(retry_metadata, Mapping):
        raise AssertionError("L6AQ.05 retry metadata summary must be report-safe metadata")
    retry_forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(retry_metadata.keys())
    if retry_forbidden:
        raise AssertionError(f"unsafe L6AQ.05 retry metadata fields present: {sorted(retry_forbidden)}")
    if retry_metadata.get("items_count") != 0 or retry_metadata.get("safe_item_labels") != []:
        raise AssertionError("L6AQ.05 must preserve denied/empty retry metadata")
    if retry_metadata.get("denial_reason") != L6AQ04_DENIAL_REASON:
        raise AssertionError("L6AQ.05 must preserve the route-audience denial reason")
    if retry_metadata.get("auth_status_code") != L6AQ04_AUTH_STATUS_CODE:
        raise AssertionError("L6AQ.05 must preserve the safe auth status code")
    if retry_metadata.get("retry_operation_count") != 1 or retry_metadata.get("second_retry_performed") is not False:
        raise AssertionError("L6AQ.05 must prove exactly one retry and no second retry")

    for field in (
        "external_tracker_written",
        "cron_mutated",
        "successor_issues_created",
        "second_retry_performed",
        "provider_prod_canary_gate_or_write_movement_performed",
    ):
        if receipt.get(field) is not False:
            raise AssertionError(f"L6AQ.05 must keep {field}=false")

    if receipt.get("step3_state") != "USEFULNESS_HELD_DENIED_EMPTY_METADATA":
        raise AssertionError("L6AQ.05 must keep Step 3 held after denied/empty metadata")
    if receipt.get("exact_blocker") != L6AQ04_BLOCKER_CLASSIFICATION:
        raise AssertionError("L6AQ.05 must name the exact remaining blocker")

    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("L6AQ.05 guarded counters must remain zero")
    retry_counters = retry_metadata.get("guarded_counters")
    if not isinstance(retry_counters, Mapping) or any(value != 0 for value in retry_counters.values()):
        raise AssertionError("L6AQ.05 retry metadata counters must remain zero")


def assert_l6aq03_configuration_proof_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AQ03_REPORT_SAFE_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AQ.03 proof fields present: {sorted(unexpected)}")
    if receipt.get("status") != L6AQ03_STATUS:
        raise AssertionError("L6AQ.03 must define the operator/service configuration proof")
    if receipt.get("retry_executed") is not False or receipt.get("second_retry_performed") is not False:
        raise AssertionError("L6AQ.03 cannot execute or authorize retry")
    proof = receipt.get("configuration_proof")
    if not isinstance(proof, Mapping):
        raise AssertionError("configuration proof must be report-safe metadata")
    forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(proof.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AQ.03 proof fields present: {sorted(forbidden)}")
    validation = validate_l6aq03_operator_service_configuration_proof(proof)
    if validation.get("status") != L6AQ03_READY_STATUS:
        raise AssertionError("configuration proof fixture must validate as ready/default-off")
    if proof.get("retry_authorized_by_configuration_proof") is not False:
        raise AssertionError("configuration proof cannot authorize retry")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AQ.03")


def assert_l6aq03_validation_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AQ03_VALIDATION_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AQ.03 validation fields present: {sorted(unexpected)}")
    if receipt.get("retry_executed") is not False or receipt.get("second_retry_performed") is not False:
        raise AssertionError("L6AQ.03 validation cannot execute retry")
    metadata = receipt.get("preflight_metadata")
    if not isinstance(metadata, Mapping):
        raise AssertionError("preflight metadata must be report-safe mapping")
    forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(metadata.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AQ.03 validation fields present: {sorted(forbidden)}")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AQ.03 validation")

def assert_l6aq02_contract_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AQ02_REPORT_SAFE_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AQ.02 contract fields present: {sorted(unexpected)}")
    forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AQ.02 report fields present: {sorted(forbidden)}")
    if receipt.get("status") != L6AQ02_STATUS:
        raise AssertionError("L6AQ.02 must define the repaired binding contract")
    if receipt.get("retry_executed") is not False or receipt.get("second_retry_performed") is not False:
        raise AssertionError("L6AQ.02 cannot execute or authorize retry")
    contract = receipt.get("binding_contract")
    if not isinstance(contract, Mapping):
        raise AssertionError("binding contract must be report-safe metadata")
    contract_forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(contract.keys())
    if contract_forbidden:
        raise AssertionError(f"unsafe binding contract fields present: {sorted(contract_forbidden)}")
    if set(contract.keys()) != L6AQ02_ALLOWED_CONTRACT_FIELDS:
        raise AssertionError("binding contract field set drifted")
    validation = validate_l6aq02_repaired_binding_contract(contract)
    if validation.get("status") != L6AQ02_READY_STATUS:
        raise AssertionError("binding contract fixture must validate as ready/default-off")
    if contract.get("retry_authorized_by_contract") is not False:
        raise AssertionError("binding contract cannot authorize retry")
    if contract.get("default_off_until_issue_403_preflight") is not True:
        raise AssertionError("binding contract must remain default-off until #403 preflight")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AQ.02")


def assert_l6aq02_validation_report_safe(receipt: Mapping[str, Any]) -> None:
    unexpected = set(receipt.keys()).difference(L6AQ02_VALIDATION_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AQ.02 validation fields present: {sorted(unexpected)}")
    if receipt.get("retry_executed") is not False or receipt.get("second_retry_performed") is not False:
        raise AssertionError("L6AQ.02 validation cannot execute retry")
    ready = receipt.get("ready_metadata")
    if not isinstance(ready, Mapping):
        raise AssertionError("ready metadata must be report-safe mapping")
    forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(ready.keys())
    if forbidden:
        raise AssertionError(f"unsafe ready metadata fields present: {sorted(forbidden)}")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AQ.02 validation")



def assert_l6aq01_localization_report_safe(receipt: Mapping[str, Any]) -> None:
    forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"unsafe L6AQ.01 report fields present: {sorted(forbidden)}")
    unexpected = set(receipt.keys()).difference(L6AQ01_REPORT_SAFE_FIELDS)
    if unexpected:
        raise AssertionError(f"unexpected L6AQ.01 report fields present: {sorted(unexpected)}")
    if receipt.get("status") != L6AQ01_STATUS:
        raise AssertionError("L6AQ.01 must localize the route-audience denial")
    if receipt.get("repair_target") != L6AQ01_REPAIR_TARGET:
        raise AssertionError("L6AQ.01 must name the recall route-audience binding repair target")
    if receipt.get("retry_executed") is not False or receipt.get("second_retry_performed") is not False:
        raise AssertionError("L6AQ.01 cannot execute a retry")

    prior = receipt.get("prior_retry_metadata")
    if not isinstance(prior, Mapping):
        raise AssertionError("L6AQ.01 prior retry metadata must be report-safe mapping")
    prior_forbidden = L6AQ01_FORBIDDEN_FIELDS.intersection(prior.keys())
    if prior_forbidden:
        raise AssertionError(f"unsafe prior retry metadata fields present: {sorted(prior_forbidden)}")
    if prior.get("denial_reason") != L6AP02_DENIAL_REASON or prior.get("auth_status_code") != L6AP02_AUTH_STATUS_CODE:
        raise AssertionError("L6AQ.01 must consume the prior wrong-route-audience safe denial")
    if prior.get("items_count") != 0 or prior.get("safe_item_labels") != []:
        raise AssertionError("L6AQ.01 must consume the denied/empty prior retry metadata")

    expected = receipt.get("expected_binding")
    if not isinstance(expected, Mapping) or expected.get("route_audience") != L6AQ01_EXPECTED_ROUTE_AUDIENCE:
        raise AssertionError("L6AQ.01 must bind the expected recall route audience label")
    observed = receipt.get("observed_denial")
    if not isinstance(observed, Mapping) or observed.get("denial_reason") != L6AP02_DENIAL_REASON:
        raise AssertionError("L6AQ.01 must name the observed denial label")

    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero for L6AQ.01")
