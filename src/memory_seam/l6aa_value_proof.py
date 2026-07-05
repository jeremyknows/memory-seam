from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from typing import Any

L6AA_VALUE_PROOF_SCHEMA_VERSION = "l6aa-value-proof-receipt-v1"
L6AA_OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ"
L6AA_PASS_STATUS = "PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ"
L6AA_HOLD_STATUS = "HOLD_DENIED_BEFORE_READ"
L6AA03_VERIFIER_STATUS = "RECEIPT_REPORTABLE_HYGIENE_VERIFIER_NO_ADDITIONAL_READS"
L6AA_APPROVED = "APPROVED_EXACT_OWNER_ISSUE_BOUND_FRESH_TARGET_REF_MATCH"
L6AA_DENIED = "DENY_BEFORE_READ"
L6AA_DESCRIPTOR_REF = "descriptor:l6aa/report-safe-operator-preference-card"
L6AA_SOURCE_CARD_REF = "source-card:l6aa/report-safe-operator-preference-card"
L6AA_APPROVAL_COMMENT_ID = "4650520977"

L6AA_GUARDED_COUNTERS = (
    "approval_comments_examined",
    "valid_owner_approval_comments",
    "live_read_invocations",
    "operation_count_attempted",
    "allowed_result_count",
    "provider_callbacks",
    "backend_callbacks",
    "source_stat_callbacks",
    "source_read_callbacks",
    "credential_reads",
    "auth_env_keychain_oauth_auth_file_reads",
    "runtime_registry_reads",
    "source_discovery_queries",
    "workspace_scans",
    "family_scans",
    "broad_recall_queries",
    "index_queries",
    "persistence_writes",
    "mutation_callbacks",
    "rollback_callbacks",
    "cache_purge_callbacks",
    "service_listener_startup_activations",
    "publication_or_visibility_changes",
    "provider_prod_canary_or_gate_moves",
)

L6AA_SAFE_RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "receipt_status",
        "approval_result",
        "stop_condition",
        "rollback_status",
        "approval_comment_id_examined",
        "approval_comment_author",
        "owner_actor_association",
        "approval_comment_created_at",
        "approval_evaluated_at",
        "freshness_result",
        "packet_issue_id",
        "read_issue_id",
        "parent_issue_id",
        "source_floor_requirement",
        "source_floor_verified_commit",
        "operation_class",
        "max_operation_count",
        "descriptor_ref",
        "source_card_ref",
        "live_read_invoked",
        "allowed",
        "allowed_result_count",
        "operation_count_attempted",
        "read_usefulness_label",
        "value_proof_summary",
        "source_card_report_safe_fields_seen",
        "redaction_status",
        "guarded_counters",
        "report_safe",
        "metadata_only",
        "unsafe_raw_fields_rejected_before_report",
    }
)

L6AA_SAFE_SOURCE_CARD_METADATA_FIELDS = frozenset(
    {
        "card_id",
        "source_tier",
        "private_class",
        "canonicality",
        "retrieval_backend",
        "title",
        "safe_summary",
        "reportable",
        "redaction_applied",
        "redaction_labels",
    }
)

L6AA_UNSAFE_KEY_MARKERS = (
    "raw",
    "private",
    "secret",
    "token",
    "credential_value",
    "password",
    "auth_material",
    "oauth_token",
    "keychain",
    "env_value",
    "absolute_path",
    "source_uri",
    "platform_id",
    "prompt_payload",
    "query_payload",
    "payload_content",
    "backend_response",
    "correlation_ref",
    "source_text",
    "approval_text",
)

L6AA_UNSAFE_ECHO_MARKERS = (
    "raw private source text",
    "private absolute path",
    "source://",
    "platform-raw-id",
    "raw platform id",
    "raw prompt",
    "raw query",
    "query payload",
    "raw payload",
    "raw backend response",
    "credential value",
    "auth material",
    "oauth token",
    "keychain material",
    "auth-file material",
    "private-correlation-ref",
    "raw approval text",
    "i approve exactly one supervised",
)


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _fresh_within_12h(created_at: str, evaluated_at: str) -> bool:
    age = _parse_utc(evaluated_at) - _parse_utc(created_at)
    return 0 <= age.total_seconds() <= 12 * 60 * 60


def _contains_unsafe_key(key: str) -> bool:
    lowered = key.lower().replace("-", "_")
    return any(marker in lowered for marker in L6AA_UNSAFE_KEY_MARKERS)


def _contains_unsafe_echo(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in L6AA_UNSAFE_ECHO_MARKERS)
    if isinstance(value, Mapping):
        return any(_contains_unsafe_echo(item) for item in value.values())
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_unsafe_echo(item) for item in value)
    return False


def _zero_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6AA_GUARDED_COUNTERS}


def approval_matches_l6aa_packet(approval: Mapping[str, Any], *, evaluated_at: str) -> bool:
    """Recognize only the exact issue-bound #242 owner approval shape.

    The caller supplies already-fetched public issue-comment metadata. This helper
    never reads source cards, credentials, Runtime Registry state, private files,
    workspaces, indexes, providers, backends, or raw approval text.
    """

    expected = {
        "approval_comment_id": L6AA_APPROVAL_COMMENT_ID,
        "approval_comment_author": "jeremyknows",
        "owner_actor_association": "OWNER",
        "packet_issue_id": "#241",
        "read_issue_id": "#242",
        "parent_issue_id": "#6",
        "subject": "jeremyknows/memory-seam",
        "audience": "L6AA owner-approved target-ref live-read value proof",
        "scope": "one report-safe source-card read",
        "operation_class": L6AA_OPERATION_CLASS,
        "max_operation_count": 1,
        "descriptor_ref": L6AA_DESCRIPTOR_REF,
        "source_card_ref": L6AA_SOURCE_CARD_REF,
        "source_floor_requirement": "b141f7be878a5b0d136cced3beb12ef38f0a25c9 or later",
        "preauth_anchor_refs_present": True,
        "report_safe_output_only": True,
        "deny_before_read_on_mismatch": True,
    }
    for key, value in expected.items():
        if approval.get(key) != value:
            return False
    created_at = approval.get("approval_comment_created_at")
    return isinstance(created_at, str) and _fresh_within_12h(created_at, evaluated_at)


def build_l6aa02_hold_receipt(approval: Mapping[str, Any], *, evaluated_at: str) -> dict[str, Any]:
    counters = _zero_counters()
    if approval:
        counters["approval_comments_examined"] = 1
    return {
        "schema_version": L6AA_VALUE_PROOF_SCHEMA_VERSION,
        "receipt_status": L6AA_HOLD_STATUS,
        "approval_result": L6AA_DENIED,
        "stop_condition": "DENIED_BEFORE_CALLBACK",
        "rollback_status": "NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED",
        "approval_comment_id_examined": str(approval.get("approval_comment_id", "NONE")),
        "approval_comment_author": str(approval.get("approval_comment_author", "NONE")),
        "owner_actor_association": str(approval.get("owner_actor_association", "NONE")),
        "approval_comment_created_at": str(approval.get("approval_comment_created_at", "NONE")),
        "approval_evaluated_at": evaluated_at,
        "freshness_result": "NOT_RECOGNIZED_OR_NOT_FRESH",
        "packet_issue_id": "#241",
        "read_issue_id": "#242",
        "parent_issue_id": "#6",
        "source_floor_requirement": "b141f7be878a5b0d136cced3beb12ef38f0a25c9 or later",
        "source_floor_verified_commit": "169bcaf040277441f5f4b2a2e90f3f894817046d",
        "operation_class": L6AA_OPERATION_CLASS,
        "max_operation_count": 1,
        "descriptor_ref": L6AA_DESCRIPTOR_REF,
        "source_card_ref": L6AA_SOURCE_CARD_REF,
        "live_read_invoked": False,
        "allowed": False,
        "allowed_result_count": 0,
        "operation_count_attempted": 0,
        "read_usefulness_label": "NOT_APPLICABLE_NO_READ_EXECUTED",
        "value_proof_summary": "Denied before read; no value proof from source-card evidence.",
        "source_card_report_safe_fields_seen": [],
        "redaction_status": "REPORT_SAFE_METADATA_ONLY_RAW_APPROVAL_TEXT_OMITTED",
        "guarded_counters": counters,
        "report_safe": True,
        "metadata_only": True,
        "unsafe_raw_fields_rejected_before_report": True,
    }


def execute_l6aa02_value_proof(
    approval: Mapping[str, Any],
    *,
    evaluated_at: str,
    read_report_safe_source_card: Callable[[str, str], Mapping[str, Any]],
    source_floor_verified_commit: str = "169bcaf040277441f5f4b2a2e90f3f894817046d",
) -> dict[str, Any]:
    """Execute exactly one report-safe source-card read if #242 approval matches.

    The read callback receives only the exact descriptor/source-card refs and must
    return metadata-only card fields. Unsafe keys or unsafe echoed values are
    rejected before receipt output.
    """

    if not approval_matches_l6aa_packet(approval, evaluated_at=evaluated_at):
        return build_l6aa02_hold_receipt(approval, evaluated_at=evaluated_at)

    card = dict(read_report_safe_source_card(L6AA_DESCRIPTOR_REF, L6AA_SOURCE_CARD_REF))
    unknown_card_fields = set(card) - L6AA_SAFE_SOURCE_CARD_METADATA_FIELDS
    if (
        unknown_card_fields
        or any(_contains_unsafe_key(str(key)) for key in unknown_card_fields)
        or _contains_unsafe_echo(card)
    ):
        return build_l6aa02_hold_receipt(approval, evaluated_at=evaluated_at) | {
            "freshness_result": "FRESH_WITHIN_12H",
            "value_proof_summary": "Denied after report-safety check; unsafe source-card metadata omitted.",
        }
    safe_fields = sorted(str(key) for key in card)
    counters = _zero_counters() | {
        "approval_comments_examined": 1,
        "valid_owner_approval_comments": 1,
        "live_read_invocations": 1,
        "operation_count_attempted": 1,
        "allowed_result_count": 1,
        "source_read_callbacks": 1,
    }
    return {
        "schema_version": L6AA_VALUE_PROOF_SCHEMA_VERSION,
        "receipt_status": L6AA_PASS_STATUS,
        "approval_result": L6AA_APPROVED,
        "stop_condition": "COMPLETED_ONE_REPORT_SAFE_READ_NO_ADDITIONAL_READS",
        "rollback_status": "NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED",
        "approval_comment_id_examined": L6AA_APPROVAL_COMMENT_ID,
        "approval_comment_author": "jeremyknows",
        "owner_actor_association": "OWNER",
        "approval_comment_created_at": str(approval["approval_comment_created_at"]),
        "approval_evaluated_at": evaluated_at,
        "freshness_result": "FRESH_WITHIN_12H",
        "packet_issue_id": "#241",
        "read_issue_id": "#242",
        "parent_issue_id": "#6",
        "source_floor_requirement": "b141f7be878a5b0d136cced3beb12ef38f0a25c9 or later",
        "source_floor_verified_commit": source_floor_verified_commit,
        "operation_class": L6AA_OPERATION_CLASS,
        "max_operation_count": 1,
        "descriptor_ref": L6AA_DESCRIPTOR_REF,
        "source_card_ref": L6AA_SOURCE_CARD_REF,
        "live_read_invoked": True,
        "allowed": "EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY",
        "allowed_result_count": 1,
        "operation_count_attempted": 1,
        "read_usefulness_label": "USEFUL_REPORT_SAFE_OPERATOR_PREFERENCE_METADATA_SEEN",
        "value_proof_summary": "One exact issue-bound supervised report-safe source-card read returned metadata sufficient to prove the target card exists, is reportable, and has redaction labels without exposing raw private content.",
        "source_card_report_safe_fields_seen": safe_fields,
        "redaction_status": "REPORT_SAFE_METADATA_ONLY_RAW_SOURCE_CONTENT_OMITTED",
        "guarded_counters": counters,
        "report_safe": True,
        "metadata_only": True,
        "unsafe_raw_fields_rejected_before_report": True,
    }


def validate_l6aa_value_proof_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    unknown_fields = set(receipt) - L6AA_SAFE_RECEIPT_FIELDS
    if unknown_fields:
        errors.append("unsafe_receipt_field_present")
    if any(_contains_unsafe_key(str(field)) for field in unknown_fields):
        errors.append("unsafe_receipt_key_present")
    if _contains_unsafe_echo(receipt):
        errors.append("unsafe_echo_marker_present")
    if receipt.get("schema_version") != L6AA_VALUE_PROOF_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if receipt.get("packet_issue_id") != "#241" or receipt.get("read_issue_id") != "#242":
        errors.append("unexpected_issue_binding")
    if receipt.get("operation_class") != L6AA_OPERATION_CLASS:
        errors.append("unexpected_operation_class")
    if receipt.get("descriptor_ref") != L6AA_DESCRIPTOR_REF or receipt.get("source_card_ref") != L6AA_SOURCE_CARD_REF:
        errors.append("unexpected_target_ref")
    if receipt.get("max_operation_count") != 1:
        errors.append("unexpected_max_operation_count")
    for field in ("report_safe", "metadata_only", "unsafe_raw_fields_rejected_before_report"):
        if receipt.get(field) is not True:
            errors.append(f"{field}_not_true")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping):
        errors.append("missing_guarded_counters")
    else:
        unknown_counters = set(counters) - set(L6AA_GUARDED_COUNTERS)
        if unknown_counters:
            errors.append("unsafe_guarded_counter_present")
        if any(_contains_unsafe_key(str(counter)) for counter in unknown_counters):
            errors.append("unsafe_guarded_counter_key_present")
    if receipt.get("receipt_status") == L6AA_PASS_STATUS:
        expected_ones = {
            "approval_comments_examined",
            "valid_owner_approval_comments",
            "live_read_invocations",
            "operation_count_attempted",
            "allowed_result_count",
            "source_read_callbacks",
        }
        if receipt.get("approval_result") != L6AA_APPROVED:
            errors.append("unexpected_approval_result")
        if receipt.get("live_read_invoked") is not True:
            errors.append("live_read_invoked_not_true_for_pass")
        if receipt.get("allowed") != "EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY":
            errors.append("allowed_broadened_or_missing")
        for counter in L6AA_GUARDED_COUNTERS:
            expected = 1 if counter in expected_ones else 0
            if isinstance(counters, Mapping) and counters.get(counter) != expected:
                errors.append(f"unexpected_counter_{counter}")
    elif receipt.get("receipt_status") == L6AA_HOLD_STATUS:
        if receipt.get("approval_result") != L6AA_DENIED:
            errors.append("unexpected_approval_result")
        if receipt.get("live_read_invoked") is not False:
            errors.append("live_read_invoked_not_false_for_hold")
        if receipt.get("allowed") is not False:
            errors.append("allowed_not_false_for_hold")
        for counter in L6AA_GUARDED_COUNTERS:
            expected = 1 if counter == "approval_comments_examined" else 0
            if isinstance(counters, Mapping) and counters.get(counter) != expected:
                errors.append(f"unexpected_counter_{counter}")
    else:
        errors.append("unexpected_receipt_status")
    return errors


def verify_l6aa03_receipt_reportable_hygiene(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Verify an already-supplied #242 receipt without performing any read.

    L6AA.03 is verifier/review-only. This helper consumes only a receipt mapping
    supplied by the caller, delegates report-safety checks to the L6AA.02 receipt
    validator, and returns metadata-only verifier status. It has no callbacks and
    no path to source-card, credential, Runtime Registry, discovery, persistence,
    activation, provider, production, canary, or Gate surfaces.
    """

    errors = validate_l6aa_value_proof_receipt(receipt)
    status = receipt.get("receipt_status")

    if receipt.get("read_issue_id") != "#242" or receipt.get("packet_issue_id") != "#241":
        errors.append("unexpected_l6aa03_receipt_binding")

    if status == L6AA_PASS_STATUS:
        if receipt.get("allowed") != "EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY":
            errors.append("l6aa03_pass_allowed_scope_not_exact")
        if receipt.get("operation_count_attempted") != 1:
            errors.append("l6aa03_pass_operation_count_not_one")
        if receipt.get("allowed_result_count") != 1:
            errors.append("l6aa03_pass_allowed_result_count_not_one")
        if receipt.get("live_read_invoked") is not True:
            errors.append("l6aa03_pass_live_read_not_recorded")
    elif status == L6AA_HOLD_STATUS:
        if receipt.get("allowed") is not False:
            errors.append("l6aa03_hold_allowed_not_false")
        if receipt.get("operation_count_attempted") != 0:
            errors.append("l6aa03_hold_operation_count_not_zero")
        if receipt.get("allowed_result_count") != 0:
            errors.append("l6aa03_hold_allowed_result_count_not_zero")
        if receipt.get("live_read_invoked") is not False:
            errors.append("l6aa03_hold_live_read_not_false")

    counters = receipt.get("guarded_counters")
    if isinstance(counters, Mapping):
        pass_one_counters = {
            "approval_comments_examined",
            "valid_owner_approval_comments",
            "live_read_invocations",
            "operation_count_attempted",
            "allowed_result_count",
            "source_read_callbacks",
        }
        for counter, value in counters.items():
            if status != L6AA_PASS_STATUS and value != 0:
                errors.append(f"l6aa03_unapproved_nonzero_counter_{counter}")
            if status == L6AA_PASS_STATUS and counter not in pass_one_counters and value != 0:
                errors.append(f"l6aa03_pass_forbidden_nonzero_counter_{counter}")

    unique_errors = sorted(set(errors))
    return {
        "schema_version": "l6aa03-receipt-hygiene-verifier-v1",
        "verifier_status": L6AA03_VERIFIER_STATUS,
        "accepted": not unique_errors,
        "errors": unique_errors,
        "receipt_status_examined": str(status),
        "packet_issue_id": "#241",
        "read_issue_id": "#242",
        "verifier_issue_id": "#243",
        "parent_issue_id": "#6",
        "additional_live_read_invoked": False,
        "callbacks_invoked": False,
        "metadata_only": True,
        "report_safe": True,
        "broad_allowed_true_accepted": False,
    }


__all__ = [
    "L6AA_APPROVED",
    "L6AA_DENIED",
    "L6AA_DESCRIPTOR_REF",
    "L6AA_GUARDED_COUNTERS",
    "L6AA_HOLD_STATUS",
    "L6AA_OPERATION_CLASS",
    "L6AA03_VERIFIER_STATUS",
    "L6AA_PASS_STATUS",
    "L6AA_SAFE_RECEIPT_FIELDS",
    "L6AA_SAFE_SOURCE_CARD_METADATA_FIELDS",
    "L6AA_SOURCE_CARD_REF",
    "L6AA_VALUE_PROOF_SCHEMA_VERSION",
    "approval_matches_l6aa_packet",
    "build_l6aa02_hold_receipt",
    "execute_l6aa02_value_proof",
    "validate_l6aa_value_proof_receipt",
    "verify_l6aa03_receipt_reportable_hygiene",
]
