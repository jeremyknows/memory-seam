from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from memory_seam.l6aa_value_proof import (
    L6AA_APPROVED,
    L6AA_OPERATION_CLASS,
    L6AA_PASS_STATUS,
)

L6AB01_SCHEMA_VERSION = "l6ab01-source-card-value-comparison-v1"
L6AB01_STATUS = "REPORT_SAFE_VALUE_COMPARISON_MATRIX_NO_LIVE_READS"
L6AB03_SCHEMA_VERSION = "l6ab03-report-safe-value-evidence-ux-v1"
L6AB03_STATUS = "REPORT_SAFE_VALUE_EVIDENCE_UX_PACKET_NO_LIVE_READS"
L6AB03_FUTURE_APPROVAL_TEMPLATE = (
    "I authorize exactly one future report-safe source-card read for issue <ISSUE>, "
    "in repo jeremyknows/memory-seam, performed by Sax, using descriptor ref "
    "<DESCRIPTOR_REF> and source-card ref <SOURCE_CARD_REF>, for operation class "
    "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ, max_operation_count=1, "
    "report-safe output only, deny-before-read on any mismatch/stale/copy/broadened "
    "variant, with no source discovery, no credentials/auth/env/keychain/OAuth/auth-file "
    "reads, no Runtime Registry consumption, no persistence/mutation, no activation, "
    "no publication/visibility/provider/prod/canary/Gate movement, and no broad allowed=true route."
)

L6AB01_SAFE_MATRIX_FIELDS = frozenset(
    {
        "case_id",
        "source_rail",
        "issue_anchor",
        "approval_state",
        "target_ref_state",
        "receipt_status",
        "comparison_outcome",
        "live_read_invoked",
        "allowed",
        "allowed_result_count",
        "operation_count_attempted",
        "value_signal",
        "report_safe_evidence",
        "descriptor_ref_match",
        "source_card_ref_match",
        "cannot_authorize_another_read",
    }
)

L6AB01_SAFE_PACKET_FIELDS = frozenset(
    {
        "schema_version",
        "status",
        "parent_issue_id",
        "rail_issue_id",
        "source_floor_requirement",
        "source_floor_verified_commit",
        "operation_class_compared",
        "matrix",
        "additional_live_read_invoked",
        "callbacks_invoked",
        "metadata_only",
        "report_safe",
        "cannot_authorize_another_read",
        "preserved_holds",
    }
)

L6AB01_PRESERVED_HOLDS = (
    "no_live_or_private_reads",
    "no_raw_private_content",
    "no_credentials_auth_env_keychain_oauth_or_auth_file_reads",
    "no_source_discovery_workspace_family_broad_recall_or_index_queries",
    "no_runtime_registry_consumption",
    "no_persistence_mutation_reindex_cache_purge_or_rollback_execution",
    "no_service_listener_startup_or_global_runtime_config_activation",
    "no_publication_visibility_provider_prod_canary_or_gate_movement",
    "no_broad_allowed_true_route",
)


def _safe_case(
    *,
    case_id: str,
    source_rail: str,
    issue_anchor: str,
    approval_state: str,
    target_ref_state: str,
    receipt_status: str,
    comparison_outcome: str,
    live_read_invoked: bool,
    allowed: bool | str,
    allowed_result_count: int,
    operation_count_attempted: int,
    value_signal: str,
    report_safe_evidence: str,
    descriptor_ref_match: bool,
    source_card_ref_match: bool,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "source_rail": source_rail,
        "issue_anchor": issue_anchor,
        "approval_state": approval_state,
        "target_ref_state": target_ref_state,
        "receipt_status": receipt_status,
        "comparison_outcome": comparison_outcome,
        "live_read_invoked": live_read_invoked,
        "allowed": allowed,
        "allowed_result_count": allowed_result_count,
        "operation_count_attempted": operation_count_attempted,
        "value_signal": value_signal,
        "report_safe_evidence": report_safe_evidence,
        "descriptor_ref_match": descriptor_ref_match,
        "source_card_ref_match": source_card_ref_match,
        "cannot_authorize_another_read": True,
    }


def build_l6ab01_value_comparison_matrix(
    *, source_floor_verified_commit: str = "91761ed55889f4c5432b55c445e396e727a6be93",
) -> dict[str, Any]:
    """Compare existing report-safe L6X-L6AA outcomes without any read path.

    The packet is assembled from committed public/report-safe rail artifacts and
    contains no callback, no provider handle, no Runtime Registry handle, and no
    approval text. It cannot authorize a live/private read; the only PASS row is
    historical metadata for the already-consumed #242 exact-owner-approved read.
    """

    return {
        "schema_version": L6AB01_SCHEMA_VERSION,
        "status": L6AB01_STATUS,
        "parent_issue_id": "#6",
        "rail_issue_id": "#251",
        "source_floor_requirement": "91761ed55889f4c5432b55c445e396e727a6be93 or later",
        "source_floor_verified_commit": source_floor_verified_commit,
        "operation_class_compared": L6AA_OPERATION_CLASS,
        "matrix": [
            _safe_case(
                case_id="absent-approval",
                source_rail="L6X",
                issue_anchor="#212/#214/#215",
                approval_state="ABSENT_OWNER_APPROVAL",
                target_ref_state="NOT_REACHED_NO_APPROVAL",
                receipt_status="HOLD_DENIED_BEFORE_READ_NO_APPROVAL_NO_LIVE",
                comparison_outcome="DENIED_BEFORE_READ",
                live_read_invoked=False,
                allowed=False,
                allowed_result_count=0,
                operation_count_attempted=0,
                value_signal="No source-card value proof; approval absence proved denial posture.",
                report_safe_evidence="L6X HOLD receipt and reconciliation metadata only.",
                descriptor_ref_match=False,
                source_card_ref_match=False,
            ),
            _safe_case(
                case_id="missing-target-refs",
                source_rail="L6Y",
                issue_anchor="#222/#225",
                approval_state="OWNER_APPROVAL_PRESENT_FRESH",
                target_ref_state="MISSING_EXECUTABLE_DESCRIPTOR_AND_SOURCE_CARD_REFS",
                receipt_status="HOLD_DENIED_BEFORE_READ_APPROVAL_MISMATCH_NO_LIVE",
                comparison_outcome="DENIED_BEFORE_READ",
                live_read_invoked=False,
                allowed=False,
                allowed_result_count=0,
                operation_count_attempted=0,
                value_signal="Control-plane value only; fresh approval still could not identify executable refs.",
                report_safe_evidence="L6Y HOLD receipt, usefulness review, and reconciliation metadata only.",
                descriptor_ref_match=False,
                source_card_ref_match=False,
            ),
            _safe_case(
                case_id="mismatched-target-refs",
                source_rail="L6Z",
                issue_anchor="#232/#235",
                approval_state="OWNER_APPROVAL_PRESENT_FRESH",
                target_ref_state="MISMATCHED_EXECUTABLE_DESCRIPTOR_OR_SOURCE_CARD_REFS",
                receipt_status="HOLD_DENIED_BEFORE_READ_APPROVAL_TARGET_REF_MISMATCH_NO_LIVE",
                comparison_outcome="DENIED_BEFORE_READ",
                live_read_invoked=False,
                allowed=False,
                allowed_result_count=0,
                operation_count_attempted=0,
                value_signal="Useful denial evidence; exact refs matter before any source-card callback.",
                report_safe_evidence="L6Z HOLD receipt, redaction verifier, usefulness review, and reconciliation metadata only.",
                descriptor_ref_match=False,
                source_card_ref_match=False,
            ),
            _safe_case(
                case_id="exact-owner-approved-target-refs",
                source_rail="L6AA",
                issue_anchor="#242/#245",
                approval_state=L6AA_APPROVED,
                target_ref_state="EXACT_DESCRIPTOR_AND_SOURCE_CARD_REF_MATCH",
                receipt_status=L6AA_PASS_STATUS,
                comparison_outcome="PASS_ONE_HISTORICAL_REPORT_SAFE_SOURCE_CARD_READ_CONSUMED",
                live_read_invoked=True,
                allowed="EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY",
                allowed_result_count=1,
                operation_count_attempted=1,
                value_signal="Report-safe metadata proved the target card existed, was reportable, and carried redaction labels.",
                report_safe_evidence="L6AA #242 PASS receipt metadata and #243-#245 verifier/review/reconciliation metadata only.",
                descriptor_ref_match=True,
                source_card_ref_match=True,
            ),
        ],
        "additional_live_read_invoked": False,
        "callbacks_invoked": False,
        "metadata_only": True,
        "report_safe": True,
        "cannot_authorize_another_read": True,
        "preserved_holds": list(L6AB01_PRESERVED_HOLDS),
    }


L6AB03_SAFE_PACKET_FIELDS = frozenset(
    {
        "schema_version",
        "status",
        "parent_issue_id",
        "rail_issue_id",
        "depends_on",
        "evidence_headline",
        "consumed_approval_read_statement",
        "what_the_evidence_proves",
        "what_the_evidence_does_not_prove",
        "future_approval_template_text_only",
        "template_is_active_authorization",
        "raw_private_content_included",
        "raw_approval_text_included",
        "source_uri_included",
        "private_path_included",
        "prompt_or_query_payload_included",
        "backend_response_included",
        "credential_or_auth_material_included",
        "live_read_invoked",
        "callbacks_invoked",
        "report_safe",
        "residual_holds",
    }
)

L6AB03_REQUIRED_PROVES = (
    "Exact owner-approved target refs produced one historical report-safe source-card metadata receipt.",
    "The #242 evidence carried reportability and redaction-label metadata without raw source content.",
    "Denied rails show approval, target-ref, stale, copied, broadened, expired, non-owner, and allowed-true variants stop before read.",
)

L6AB03_REQUIRED_NOT_PROVES = (
    "It does not prove ongoing permission to read source cards.",
    "It does not expose raw private content, raw approval text, source URIs, private paths, prompts, queries, backend responses, credentials, or auth material.",
    "It does not authorize live/private reads, callbacks, discovery, Runtime Registry use, persistence, activation, publication, provider movement, Gate movement, or broad allowed=true routing.",
)


def validate_l6ab01_value_comparison_packet(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    unknown_packet_fields = set(packet) - L6AB01_SAFE_PACKET_FIELDS
    if unknown_packet_fields:
        errors.append("unsafe_packet_field_present")
    if packet.get("schema_version") != L6AB01_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if packet.get("status") != L6AB01_STATUS:
        errors.append("unexpected_status")
    if packet.get("parent_issue_id") != "#6" or packet.get("rail_issue_id") != "#251":
        errors.append("unexpected_issue_binding")
    if packet.get("operation_class_compared") != L6AA_OPERATION_CLASS:
        errors.append("unexpected_operation_class")
    for field in (
        "additional_live_read_invoked",
        "callbacks_invoked",
        "cannot_authorize_another_read",
        "metadata_only",
        "report_safe",
    ):
        expected = False if field in {"additional_live_read_invoked", "callbacks_invoked"} else True
        if packet.get(field) is not expected:
            errors.append(f"unexpected_{field}")

    matrix = packet.get("matrix")
    if not isinstance(matrix, list) or len(matrix) != 4:
        errors.append("unexpected_matrix_shape")
        return sorted(set(errors))

    case_ids = [row.get("case_id") for row in matrix if isinstance(row, Mapping)]
    if case_ids != [
        "absent-approval",
        "missing-target-refs",
        "mismatched-target-refs",
        "exact-owner-approved-target-refs",
    ]:
        errors.append("unexpected_matrix_order")

    pass_rows = 0
    for row in matrix:
        if not isinstance(row, Mapping):
            errors.append("matrix_row_not_mapping")
            continue
        if set(row) - L6AB01_SAFE_MATRIX_FIELDS:
            errors.append("unsafe_matrix_field_present")
        if row.get("cannot_authorize_another_read") is not True:
            errors.append("matrix_row_can_authorize_read")
        if row.get("allowed") is True:
            errors.append("broad_allowed_true_present")
        if row.get("comparison_outcome") == "PASS_ONE_HISTORICAL_REPORT_SAFE_SOURCE_CARD_READ_CONSUMED":
            pass_rows += 1
            if row.get("live_read_invoked") is not True:
                errors.append("pass_row_missing_historical_read_flag")
            if row.get("allowed") != "EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY":
                errors.append("pass_row_allowed_scope_not_exact")
            if row.get("allowed_result_count") != 1 or row.get("operation_count_attempted") != 1:
                errors.append("pass_row_count_not_one")
            if row.get("descriptor_ref_match") is not True or row.get("source_card_ref_match") is not True:
                errors.append("pass_row_target_refs_not_matched")
        else:
            if row.get("live_read_invoked") is not False:
                errors.append("hold_row_live_read_invoked")
            if row.get("allowed") is not False:
                errors.append("hold_row_allowed_not_false")
            if row.get("allowed_result_count") != 0 or row.get("operation_count_attempted") != 0:
                errors.append("hold_row_count_not_zero")
    if pass_rows != 1:
        errors.append("unexpected_pass_row_count")
    return sorted(set(errors))


def build_l6ab03_value_evidence_ux_packet() -> dict[str, Any]:
    """Build the operator-facing L6AB.03 packet without any read path."""

    matrix = build_l6ab01_value_comparison_matrix()
    pass_row = matrix["matrix"][-1]
    return {
        "schema_version": L6AB03_SCHEMA_VERSION,
        "status": L6AB03_STATUS,
        "parent_issue_id": "#6",
        "rail_issue_id": "#253",
        "depends_on": "#252 closed/PASS",
        "evidence_headline": (
            "Useful report-safe value was proven once: exact #242 owner approval plus exact target refs "
            "returned one metadata-only source-card evidence receipt, now consumed."
        ),
        "consumed_approval_read_statement": (
            f"The L6AA PASS evidence is historical only: {pass_row['issue_anchor']} consumed "
            "exactly one report-safe source-card read; it is not reusable approval."
        ),
        "what_the_evidence_proves": list(L6AB03_REQUIRED_PROVES),
        "what_the_evidence_does_not_prove": list(L6AB03_REQUIRED_NOT_PROVES),
        "future_approval_template_text_only": L6AB03_FUTURE_APPROVAL_TEMPLATE,
        "template_is_active_authorization": False,
        "raw_private_content_included": False,
        "raw_approval_text_included": False,
        "source_uri_included": False,
        "private_path_included": False,
        "prompt_or_query_payload_included": False,
        "backend_response_included": False,
        "credential_or_auth_material_included": False,
        "live_read_invoked": False,
        "callbacks_invoked": False,
        "report_safe": True,
        "residual_holds": list(L6AB01_PRESERVED_HOLDS),
    }


def validate_l6ab03_value_evidence_ux_packet(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(packet) != L6AB03_SAFE_PACKET_FIELDS:
        errors.append("unexpected_packet_fields")
    if packet.get("schema_version") != L6AB03_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if packet.get("status") != L6AB03_STATUS:
        errors.append("unexpected_status")
    if packet.get("parent_issue_id") != "#6" or packet.get("rail_issue_id") != "#253":
        errors.append("unexpected_issue_binding")
    if packet.get("depends_on") != "#252 closed/PASS":
        errors.append("unexpected_dependency")
    if not str(packet.get("evidence_headline", "")).startswith("Useful report-safe value was proven once"):
        errors.append("missing_value_headline")
    if "consumed" not in str(packet.get("consumed_approval_read_statement", "")):
        errors.append("missing_consumed_read_statement")
    if packet.get("what_the_evidence_proves") != list(L6AB03_REQUIRED_PROVES):
        errors.append("unexpected_proves_list")
    if packet.get("what_the_evidence_does_not_prove") != list(L6AB03_REQUIRED_NOT_PROVES):
        errors.append("unexpected_not_proves_list")
    template = packet.get("future_approval_template_text_only")
    if template != L6AB03_FUTURE_APPROVAL_TEMPLATE:
        errors.append("unexpected_future_template")
    if packet.get("template_is_active_authorization") is not False:
        errors.append("template_treated_as_active_authorization")
    for false_field in (
        "raw_private_content_included",
        "raw_approval_text_included",
        "source_uri_included",
        "private_path_included",
        "prompt_or_query_payload_included",
        "backend_response_included",
        "credential_or_auth_material_included",
        "live_read_invoked",
        "callbacks_invoked",
    ):
        if packet.get(false_field) is not False:
            errors.append(f"unsafe_{false_field}")
    if packet.get("report_safe") is not True:
        errors.append("not_report_safe")
    if "no_broad_allowed_true_route" not in packet.get("residual_holds", []):
        errors.append("missing_allowed_true_hold")
    return sorted(set(errors))


__all__ = [
    "L6AB01_PRESERVED_HOLDS",
    "L6AB01_SAFE_MATRIX_FIELDS",
    "L6AB01_SAFE_PACKET_FIELDS",
    "L6AB01_SCHEMA_VERSION",
    "L6AB01_STATUS",
    "L6AB03_FUTURE_APPROVAL_TEMPLATE",
    "L6AB03_REQUIRED_NOT_PROVES",
    "L6AB03_REQUIRED_PROVES",
    "L6AB03_SAFE_PACKET_FIELDS",
    "L6AB03_SCHEMA_VERSION",
    "L6AB03_STATUS",
    "build_l6ab01_value_comparison_matrix",
    "build_l6ab03_value_evidence_ux_packet",
    "validate_l6ab01_value_comparison_packet",
    "validate_l6ab03_value_evidence_ux_packet",
]
