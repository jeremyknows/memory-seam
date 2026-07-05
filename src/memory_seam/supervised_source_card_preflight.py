"""Default-off supervised source-card proof preflight skeleton.

This bounded L6V.01 slice recognizes only the issue #187 approved
``SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`` preflight shape and emits
report-safe metadata-only receipts. It never performs live/private reads, source
discovery, Runtime Registry consumption, credential reads, provider/backend or
source callbacks, persistence, mutation, service activation, publication,
production authority, or Atlas Gate movement. There is no ``allowed=true`` path.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_STATUS = "supervised_source_card_preflight_default_off"
L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_SCHEMA_VERSION = "l6v-supervised-source-card-preflight-v1"
L6V_SUPERVISED_SOURCE_CARD_RECEIPT_SCHEMA_VERSION = "l6v-supervised-source-card-receipt-v1"
L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_SLICE = "L6V.01_SUPERVISED_SOURCE_CARD_PROOF_PREFLIGHT_SKELETON"
L6V_SUPERVISED_SOURCE_CARD_DENIAL_MATRIX_SLICE = "L6V.02_SUPERVISED_SOURCE_CARD_PROOF_DENIAL_MATRIX"
L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_PROOF_SLICE = "L6V.03_REPORT_SAFE_SOURCE_CARD_DESCRIPTOR_FIXTURE_PROOF"
L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF"
L6V_SUPERVISED_SOURCE_CARD_APPROVAL_REF = "issue-187-comment-4645178496"
L6V_SUPERVISED_SOURCE_CARD_APPROVAL_SOURCE_URL = (
    "fixture:l6v-supervised-source-card-approval-source:internal-review-2026"
)
L6V_SUPERVISED_SOURCE_CARD_APPROVAL_ISSUE = 187
L6V_SUPERVISED_SOURCE_CARD_APPROVAL_AUTHOR_ASSOCIATION = "OWNER"
L6V_SUPERVISED_SOURCE_CARD_APPROVAL_CREATED_AT = "2026-06-08T03:28:46Z"
L6V_SUPERVISED_SOURCE_CARD_APPROVAL_EXPIRES_AT = "2026-06-08T15:28:46Z"
L6V_SUPERVISED_SOURCE_CARD_SOURCE_FLOOR = "876375b"
L6V_SUPERVISED_SOURCE_CARD_UPSTREAM_PACKET = "docs/l6u05-supervised-live-use-trust-boundary-review.md"
L6V_SUPERVISED_SOURCE_CARD_MAX_OPERATION_COUNT = 1

L6V_SUPERVISED_SOURCE_CARD_REQUIRED_APPROVAL_FIELDS = (
    "issue_ref",
    "operation_class",
    "max_operation_count",
    "actor_ref",
    "subject_ref",
    "owner_ref",
    "audience",
    "scope",
    "approval_ref",
    "approval_source_url",
    "author_association",
    "approval_created_at",
    "approval_expires_at",
    "evaluation_time",
    "descriptor_ref",
    "source_card_ref",
    "stop_condition_refs",
)

L6V_SUPERVISED_SOURCE_CARD_DENIAL_AUTHORITY_FIELDS = (
    "requested_callback_family",
    "requested_live_private_read",
    "requested_source_discovery",
    "requested_runtime_registry",
    "requested_service_activation",
    "requested_publication",
    "requested_visibility_change",
    "requested_provider_prod_canary",
    "requested_atlas_gate_movement",
    "requested_write_family",
)

L6V_SUPERVISED_SOURCE_CARD_ALLOWED_STOP_CONDITION_REFS = frozenset(
    (
        "deny-before-callback",
        "no-live-private-read",
        "no-allowed-true-route",
        "max-one-operation",
    )
)

L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS = (
    "provider_callbacks",
    "backend_callbacks",
    "source_stat_callbacks",
    "source_read_callbacks",
    "write_callbacks",
    "custody_callbacks",
    "delete_callbacks",
    "reindex_callbacks",
    "rollback_callbacks",
    "cache_purge_callbacks",
    "credential_reads",
    "auth_reads",
    "env_reads",
    "keychain_reads",
    "oauth_reads",
    "auth_file_reads",
    "runtime_registry_consumptions",
    "source_discoveries",
    "workspace_scans",
    "family_scans",
    "broad_recall_queries",
    "index_queries",
    "live_private_reads",
    "persistence_writes",
    "audit_record_writes",
    "custody_record_writes",
    "cache_mutations",
    "service_activations",
    "publication_actions",
    "visibility_changes",
    "atlas_gate_movements",
)

L6V_SUPERVISED_SOURCE_CARD_HELD_SURFACES = (
    "live_private_reads",
    "raw_source_content",
    "source_discovery_or_workspace_scan",
    "broad_recall_or_index_query",
    "source_stat_or_source_read_callbacks",
    "provider_backend_callbacks",
    "write_custody_delete_reindex_rollback_cache_purge_callbacks",
    "credential_auth_env_keychain_oauth_authfile_reads",
    "runtime_registry_consumption",
    "persistence_audit_custody_or_cache_mutation",
    "service_listener_startup_cron_activation",
    "global_config_mutation",
    "publication_or_visibility_change",
    "provider_prod_canary_or_production_authority",
    "atlas_gate_movement",
    "allowed_true_route",
)

L6V_SUPERVISED_SOURCE_CARD_REPORT_SAFETY = {
    "raw_source_content_included": False,
    "private_raw_content_included": False,
    "credentials_or_auth_material_included": False,
    "private_paths_included": False,
    "source_uris_included": False,
    "raw_platform_ids_included": False,
    "raw_prompts_or_queries_included": False,
    "raw_payload_content_included": False,
    "raw_backend_responses_included": False,
    "private_correlation_refs_included": False,
}


def _zero_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS}


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class SupervisedSourceCardPreflightCallbackHarness:
    """Synthetic callback bundle that fails if preflight calls guarded surfaces."""

    callbacks: Mapping[str, Callable[[], None]]
    counters: dict[str, int]

    @classmethod
    def build(cls) -> "SupervisedSourceCardPreflightCallbackHarness":
        counters = _zero_counters()

        def make_callback(name: str) -> Callable[[], None]:
            def callback() -> None:
                counters[name] += 1
                raise AssertionError(f"unexpected_supervised_source_card_callback:{name}")

            return callback

        return cls(callbacks={name: make_callback(name) for name in counters}, counters=counters)


L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE: dict[str, Any] = {
    "descriptor_ref": "synthetic_descriptor:l6v-report-safe-project-doc-v1",
    "source_card_ref": "synthetic_source_card:l6v-report-safe-project-doc-v1",
    "descriptor_kind": "committed_synthetic_report_safe_descriptor",
    "source_card_kind": "committed_synthetic_report_safe_source_card",
    "fixture_ref": "committed_synthetic_fixture:l6v-report-safe-project-doc-v1",
    "subject_ref": "memory-seam:l6v-supervised-proof-subject",
    "audience": "memory-seam-supervised-proof",
    "scope": "report-safe-source-card-preflight-only",
    "metadata_only": True,
    "committed_synthetic": True,
    "report_safe": True,
    "raw_source_content_included": False,
    "source_uri_included": False,
    "private_path_included": False,
    "raw_platform_id_included": False,
    "raw_query_or_payload_included": False,
    "private_correlation_ref_included": False,
    "credentials_or_auth_material_included": False,
}

L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_REQUIRED_FIELDS = (
    "descriptor_ref",
    "source_card_ref",
    "descriptor_kind",
    "source_card_kind",
    "fixture_ref",
    "subject_ref",
    "audience",
    "scope",
    "metadata_only",
    "committed_synthetic",
    "report_safe",
)

L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_UNSAFE_FIELDS = (
    "raw_source_content",
    "private_path",
    "source_uri",
    "credential_material",
    "auth_material",
    "token",
    "raw_query_text",
    "raw_prompt_text",
    "raw_payload_content",
    "raw_backend_response",
    "raw_platform_id",
    "private_correlation_ref",
)

L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FALSE_FLAGS = (
    "raw_source_content_included",
    "source_uri_included",
    "private_path_included",
    "raw_platform_id_included",
    "raw_query_or_payload_included",
    "private_correlation_ref_included",
    "credentials_or_auth_material_included",
)


def parse_supervised_source_card_operation_class(operation_class: str) -> str | None:
    """Return the exact supervised proof operation class, rejecting variants."""

    if operation_class == L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS:
        return L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS
    return None


def build_l6v_supervised_source_card_approval_context_fixture() -> dict[str, Any]:
    """Return the report-safe approval shape required for issue #187 only."""

    return {
        "issue_ref": "#187",
        "operation_class": L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS,
        "max_operation_count": L6V_SUPERVISED_SOURCE_CARD_MAX_OPERATION_COUNT,
        "actor_ref": "github-author-association:OWNER",
        "subject_ref": "memory-seam:l6v-supervised-proof-subject",
        "owner_ref": "repo-owner:jeremyknows",
        "audience": "memory-seam-supervised-proof",
        "scope": "report-safe-source-card-preflight-only",
        "approval_ref": L6V_SUPERVISED_SOURCE_CARD_APPROVAL_REF,
        "approval_source_url": L6V_SUPERVISED_SOURCE_CARD_APPROVAL_SOURCE_URL,
        "author_association": L6V_SUPERVISED_SOURCE_CARD_APPROVAL_AUTHOR_ASSOCIATION,
        "approval_created_at": L6V_SUPERVISED_SOURCE_CARD_APPROVAL_CREATED_AT,
        "approval_expires_at": L6V_SUPERVISED_SOURCE_CARD_APPROVAL_EXPIRES_AT,
        "evaluation_time": L6V_SUPERVISED_SOURCE_CARD_APPROVAL_CREATED_AT,
        "descriptor_ref": L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["descriptor_ref"],
        "source_card_ref": L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["source_card_ref"],
        "stop_condition_refs": (
            "deny-before-callback",
            "no-live-private-read",
            "no-allowed-true-route",
            "max-one-operation",
        ),
        "raw_approval_text_included": False,
        "raw_actor_id_included": False,
        "raw_source_content_included": False,
    }


def validate_l6v_supervised_source_card_approval_context(approval_context: Mapping[str, Any]) -> tuple[str, ...]:
    """Return report-safe denial/HOLD codes for missing, stale, or variant approvals."""

    errors: list[str] = []
    for field in L6V_SUPERVISED_SOURCE_CARD_REQUIRED_APPROVAL_FIELDS:
        if field not in approval_context:
            errors.append(f"missing_{field}")
    if approval_context.get("issue_ref") != "#187":
        errors.append("mismatched_issue_ref")
    if approval_context.get("actor_ref") != "github-author-association:OWNER":
        errors.append("mismatched_actor_ref")
    if approval_context.get("subject_ref") != "memory-seam:l6v-supervised-proof-subject":
        errors.append("mismatched_subject_ref")
    if approval_context.get("owner_ref") != "repo-owner:jeremyknows":
        errors.append("mismatched_owner_ref")
    if approval_context.get("audience") != "memory-seam-supervised-proof":
        errors.append("mismatched_audience")
    if approval_context.get("scope") != "report-safe-source-card-preflight-only":
        errors.append("broadened_scope")
    if parse_supervised_source_card_operation_class(str(approval_context.get("operation_class", ""))) is None:
        errors.append("variant_or_mismatched_operation_class")
    max_count = approval_context.get("max_operation_count")
    if not isinstance(max_count, int) or max_count != L6V_SUPERVISED_SOURCE_CARD_MAX_OPERATION_COUNT:
        errors.append("max_operation_count_not_exactly_one")
    if approval_context.get("approval_ref") != L6V_SUPERVISED_SOURCE_CARD_APPROVAL_REF:
        errors.append("mismatched_approval_ref")
    if approval_context.get("approval_source_url") != L6V_SUPERVISED_SOURCE_CARD_APPROVAL_SOURCE_URL:
        errors.append("mismatched_approval_source_url")
    if approval_context.get("author_association") != L6V_SUPERVISED_SOURCE_CARD_APPROVAL_AUTHOR_ASSOCIATION:
        errors.append("mismatched_author_association")
    if approval_context.get("descriptor_ref") != L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["descriptor_ref"]:
        errors.append("mismatched_descriptor_ref")
    if approval_context.get("source_card_ref") != L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["source_card_ref"]:
        errors.append("mismatched_source_card_ref")
    stop_refs = approval_context.get("stop_condition_refs")
    if not isinstance(stop_refs, tuple | list) or "deny-before-callback" not in stop_refs:
        errors.append("missing_stop_condition_refs")
    elif any(ref not in L6V_SUPERVISED_SOURCE_CARD_ALLOWED_STOP_CONDITION_REFS for ref in stop_refs):
        errors.append("broadened_stop_condition_refs")
    created_at = _parse_timestamp(approval_context.get("approval_created_at"))
    expires_at = _parse_timestamp(approval_context.get("approval_expires_at"))
    evaluation_time = _parse_timestamp(approval_context.get("evaluation_time"))
    if created_at is None:
        errors.append("invalid_approval_created_at")
    if expires_at is None:
        errors.append("invalid_approval_expires_at")
    if evaluation_time is None:
        errors.append("invalid_evaluation_time")
    if created_at is not None and expires_at is not None:
        if expires_at <= created_at or expires_at - created_at > timedelta(hours=12):
            errors.append("stale_or_broadened_approval_window")
    if evaluation_time is not None and expires_at is not None and evaluation_time >= expires_at:
        errors.append("approval_expired")
    for unsafe_flag in (
        "raw_approval_text_included",
        "raw_actor_id_included",
        "raw_source_content_included",
    ):
        if approval_context.get(unsafe_flag) is not False:
            errors.append(f"unsafe_{unsafe_flag}")
    for authority_field in L6V_SUPERVISED_SOURCE_CARD_DENIAL_AUTHORITY_FIELDS:
        requested_value = approval_context.get(authority_field)
        if requested_value not in (None, False, "", (), []):
            errors.append(f"held_authority_requested_{authority_field}")
    return tuple(errors)


def build_l6v_supervised_source_card_denial_matrix_cases() -> tuple[dict[str, Any], ...]:
    """Return report-safe stale/variant/held-authority denial matrix descriptors."""

    return (
        {"case_id": "stale_expired_approval", "expected_code": "approval_expired"},
        {"case_id": "variant_operation_class", "expected_code": "variant_or_mismatched_operation_class"},
        {"case_id": "copied_wrong_issue", "expected_code": "mismatched_issue_ref"},
        {"case_id": "unrelated_actor", "expected_code": "mismatched_actor_ref"},
        {"case_id": "mismatched_subject", "expected_code": "mismatched_subject_ref"},
        {"case_id": "broadened_scope", "expected_code": "broadened_scope"},
        {"case_id": "broadened_stop_conditions", "expected_code": "broadened_stop_condition_refs"},
        {"case_id": "callback_request", "expected_code": "held_authority_requested_requested_callback_family"},
        {"case_id": "activation_request", "expected_code": "held_authority_requested_requested_service_activation"},
        {"case_id": "publication_request", "expected_code": "held_authority_requested_requested_publication"},
        {"case_id": "provider_prod_canary_request", "expected_code": "held_authority_requested_requested_provider_prod_canary"},
        {"case_id": "atlas_gate_request", "expected_code": "held_authority_requested_requested_atlas_gate_movement"},
    )


def build_l6v_supervised_source_card_preflight_fixture() -> dict[str, Any]:
    """Return a copied default-off fixture with no live/source/callback authority."""

    return {
        "schema_version": L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_SCHEMA_VERSION,
        "status": L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_STATUS,
        "slice": L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_SLICE,
        "hardening_slice": L6V_SUPERVISED_SOURCE_CARD_DENIAL_MATRIX_SLICE,
        "descriptor_proof_slice": L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_PROOF_SLICE,
        "source_floor": L6V_SUPERVISED_SOURCE_CARD_SOURCE_FLOOR,
        "upstream_packet": L6V_SUPERVISED_SOURCE_CARD_UPSTREAM_PACKET,
        "operation_class": L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS,
        "max_operation_count": L6V_SUPERVISED_SOURCE_CARD_MAX_OPERATION_COUNT,
        "default_off": True,
        "synthetic_no_live_only": True,
        "report_safe_only": True,
        "allowed": False,
        "allowed_result_count": 0,
        "live_adapter_invoked": False,
        "guarded_counters": L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS,
        "denial_matrix_cases": build_l6v_supervised_source_card_denial_matrix_cases(),
        "held_surfaces": L6V_SUPERVISED_SOURCE_CARD_HELD_SURFACES,
        "descriptor_fixture": deepcopy(L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE),
        "report_safety": deepcopy(L6V_SUPERVISED_SOURCE_CARD_REPORT_SAFETY),
    }


def build_l6v_report_safe_source_card_descriptor_fixture() -> dict[str, Any]:
    """Return the committed synthetic metadata-only descriptor/source-card fixture."""

    return deepcopy(L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE)


def validate_l6v_report_safe_source_card_descriptor_fixture(descriptor_fixture: Mapping[str, Any]) -> tuple[str, ...]:
    """Fail closed on raw/private descriptor fields before report output is built."""

    errors: list[str] = []
    for field in L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_REQUIRED_FIELDS:
        if field not in descriptor_fixture:
            errors.append(f"missing_{field}")
    for field in L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_UNSAFE_FIELDS:
        value = descriptor_fixture.get(field)
        if value not in (None, False, "", (), []):
            errors.append(f"unsafe_{field}_present")
    for flag in L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FALSE_FLAGS:
        if descriptor_fixture.get(flag) is not False:
            errors.append(f"unsafe_{flag}")
    for true_flag in ("metadata_only", "committed_synthetic", "report_safe"):
        if descriptor_fixture.get(true_flag) is not True:
            errors.append(f"{true_flag}_not_true")
    if descriptor_fixture.get("descriptor_ref") != L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["descriptor_ref"]:
        errors.append("mismatched_descriptor_ref")
    if descriptor_fixture.get("source_card_ref") != L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["source_card_ref"]:
        errors.append("mismatched_source_card_ref")
    if descriptor_fixture.get("subject_ref") != "memory-seam:l6v-supervised-proof-subject":
        errors.append("mismatched_subject_ref")
    if descriptor_fixture.get("audience") != "memory-seam-supervised-proof":
        errors.append("mismatched_audience")
    if descriptor_fixture.get("scope") != "report-safe-source-card-preflight-only":
        errors.append("broadened_scope")
    return tuple(errors)


def build_l6v_report_safe_source_card_descriptor_proof(
    descriptor_fixture: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a report-safe descriptor proof without echoing submitted raw values."""

    fixture = descriptor_fixture or build_l6v_report_safe_source_card_descriptor_fixture()
    denial_codes = validate_l6v_report_safe_source_card_descriptor_fixture(fixture)
    descriptor_valid = not denial_codes
    return {
        "schema_version": "l6v-report-safe-source-card-descriptor-proof-v1",
        "slice": L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_PROOF_SLICE,
        "issue_ref": "#189",
        "source_floor": L6V_SUPERVISED_SOURCE_CARD_SOURCE_FLOOR,
        "upstream_packet": L6V_SUPERVISED_SOURCE_CARD_UPSTREAM_PACKET,
        "operation_class": L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS,
        "status_detail": "descriptor_fixture_report_safe" if descriptor_valid else "descriptor_fixture_rejected_before_report",
        "descriptor_valid": descriptor_valid,
        "metadata_only": descriptor_valid,
        "report_safe_only": True,
        "synthetic_no_live_only": True,
        "allowed": False,
        "allowed_result_count": 0,
        "allowed_true_route_present": False,
        "denied_or_held_before_callback": True,
        "callbacks_invoked": False,
        "live_adapter_invoked": False,
        "mutation_attempted": False,
        "persistence_attempted": False,
        "descriptor_ref": L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["descriptor_ref"],
        "source_card_ref": L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["source_card_ref"],
        "fixture_ref": L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["fixture_ref"],
        "descriptor_denial_codes": denial_codes,
        "unsafe_fixture_value_echoed": False,
        "counters": _zero_counters(),
        "report_safety": deepcopy(L6V_SUPERVISED_SOURCE_CARD_REPORT_SAFETY),
    }


def run_l6v_supervised_source_card_preflight(
    approval_context: Mapping[str, Any] | None,
    operation_class: str = L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS,
    harness: SupervisedSourceCardPreflightCallbackHarness | None = None,
) -> dict[str, Any]:
    """Evaluate the issue-bound preflight without invoking any guarded callback."""

    harness = harness or SupervisedSourceCardPreflightCallbackHarness.build()
    parsed_operation_class = parse_supervised_source_card_operation_class(operation_class)
    recognized = parsed_operation_class == L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS
    approval_denial_codes = (
        validate_l6v_supervised_source_card_approval_context(approval_context) if approval_context is not None else ("missing_approval_context",)
    )
    preflight_ready = recognized and not approval_denial_codes
    status_detail = "ready_metadata_only_preflight" if preflight_ready else "held_or_denied_before_callback"
    result = {
        "schema_version": L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_SCHEMA_VERSION,
        "receipt_schema_version": L6V_SUPERVISED_SOURCE_CARD_RECEIPT_SCHEMA_VERSION,
        "status": L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_STATUS,
        "status_detail": status_detail,
        "slice": L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_SLICE,
        "hardening_slice": L6V_SUPERVISED_SOURCE_CARD_DENIAL_MATRIX_SLICE,
        "issue_ref": "#187",
        "source_floor": L6V_SUPERVISED_SOURCE_CARD_SOURCE_FLOOR,
        "upstream_packet": L6V_SUPERVISED_SOURCE_CARD_UPSTREAM_PACKET,
        "approval_ref": L6V_SUPERVISED_SOURCE_CARD_APPROVAL_REF,
        "operation_class": parsed_operation_class or "unsupported_operation_class",
        "operation_count": 1 if recognized else 0,
        "max_operation_count": L6V_SUPERVISED_SOURCE_CARD_MAX_OPERATION_COUNT,
        "recognized_operation": recognized,
        "preflight_ready": preflight_ready,
        "default_off": True,
        "synthetic_no_live_only": True,
        "report_safe_only": True,
        "allowed": False,
        "allowed_result_count": 0,
        "allowed_true_route_present": False,
        "denied_or_held_before_callback": True,
        "callbacks_invoked": False,
        "live_adapter_invoked": False,
        "mutation_attempted": False,
        "persistence_attempted": False,
        "approval_denial_codes": approval_denial_codes,
        "denial_matrix_cases": build_l6v_supervised_source_card_denial_matrix_cases(),
        "descriptor_ref": L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["descriptor_ref"],
        "source_card_ref": L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE["source_card_ref"],
        "descriptor_fixture": deepcopy(L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE),
        "counters": deepcopy(harness.counters),
        "held_surfaces": L6V_SUPERVISED_SOURCE_CARD_HELD_SURFACES,
        "report_safety": deepcopy(L6V_SUPERVISED_SOURCE_CARD_REPORT_SAFETY),
    }
    result["receipt"] = build_l6v_supervised_source_card_receipt(result)
    return result


def build_l6v_supervised_source_card_receipt(result: Mapping[str, Any]) -> dict[str, Any]:
    """Build a non-persistent, report-safe held/ready receipt from preflight metadata."""

    counters = result.get("counters")
    zero_counters = isinstance(counters, Mapping) and all(
        counters.get(counter) == 0 for counter in L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS
    )
    return {
        "schema_version": L6V_SUPERVISED_SOURCE_CARD_RECEIPT_SCHEMA_VERSION,
        "emitted_for": "supervised_source_card_preflight_metadata_only",
        "status_detail": result.get("status_detail"),
        "issue_ref": result.get("issue_ref"),
        "approval_ref": result.get("approval_ref"),
        "operation_class": result.get("operation_class"),
        "preflight_ready": result.get("preflight_ready") is True,
        "allowed": False,
        "allowed_result_count": 0,
        "allowed_true_route_present": False,
        "live_adapter_invoked": False,
        "callbacks_invoked": False,
        "guarded_counters_zero": zero_counters,
        "descriptor_ref": result.get("descriptor_ref"),
        "source_card_ref": result.get("source_card_ref"),
        "approval_denial_codes": tuple(result.get("approval_denial_codes", ())),
        "held_surfaces": L6V_SUPERVISED_SOURCE_CARD_HELD_SURFACES,
        "report_safety": deepcopy(L6V_SUPERVISED_SOURCE_CARD_REPORT_SAFETY),
        "non_persistent": True,
        "metadata_only": True,
    }


def validate_l6v_supervised_source_card_preflight_result(result: Mapping[str, Any]) -> list[str]:
    """Return report-safe validation codes for the preflight result."""

    errors: list[str] = []
    if result.get("schema_version") != L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if result.get("receipt_schema_version") != L6V_SUPERVISED_SOURCE_CARD_RECEIPT_SCHEMA_VERSION:
        errors.append("unexpected_receipt_schema_version")
    if result.get("issue_ref") != "#187":
        errors.append("unexpected_issue_ref")
    if result.get("operation_count", 0) > L6V_SUPERVISED_SOURCE_CARD_MAX_OPERATION_COUNT:
        errors.append("operation_count_exceeded_one")
    for field in ("default_off", "synthetic_no_live_only", "report_safe_only", "denied_or_held_before_callback"):
        if result.get(field) is not True:
            errors.append(f"{field}_not_true")
    for field in (
        "allowed",
        "allowed_true_route_present",
        "callbacks_invoked",
        "live_adapter_invoked",
        "mutation_attempted",
        "persistence_attempted",
    ):
        if result.get(field) is not False:
            errors.append(f"{field}_not_false")
    if result.get("allowed_result_count") != 0:
        errors.append("allowed_result_count_not_zero")
    counters = result.get("counters")
    if not isinstance(counters, Mapping):
        errors.append("missing_counters")
    else:
        for counter in L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS:
            if counters.get(counter) != 0:
                errors.append(f"nonzero_counter_{counter}")
    if result.get("report_safety") != L6V_SUPERVISED_SOURCE_CARD_REPORT_SAFETY:
        errors.append("unsafe_report_safety")
    receipt = result.get("receipt")
    if not isinstance(receipt, Mapping):
        errors.append("missing_receipt")
    else:
        if receipt.get("schema_version") != L6V_SUPERVISED_SOURCE_CARD_RECEIPT_SCHEMA_VERSION:
            errors.append("unexpected_receipt_schema")
        for field in ("allowed", "allowed_true_route_present", "live_adapter_invoked", "callbacks_invoked"):
            if receipt.get(field) is not False:
                errors.append(f"receipt_{field}_not_false")
        if receipt.get("allowed_result_count") != 0:
            errors.append("receipt_allowed_result_count_not_zero")
        if receipt.get("guarded_counters_zero") is not True:
            errors.append("receipt_guarded_counters_not_zero")
        if receipt.get("report_safety") != L6V_SUPERVISED_SOURCE_CARD_REPORT_SAFETY:
            errors.append("unsafe_receipt_report_safety")
    held_surfaces = tuple(result.get("held_surfaces", ()))
    for surface in L6V_SUPERVISED_SOURCE_CARD_HELD_SURFACES:
        if surface not in held_surfaces:
            errors.append(f"missing_held_surface_{surface}")
    return errors


__all__ = [
    "L6V_SUPERVISED_SOURCE_CARD_APPROVAL_REF",
    "L6V_SUPERVISED_SOURCE_CARD_APPROVAL_SOURCE_URL",
    "L6V_SUPERVISED_SOURCE_CARD_ALLOWED_STOP_CONDITION_REFS",
    "L6V_SUPERVISED_SOURCE_CARD_DENIAL_AUTHORITY_FIELDS",
    "L6V_SUPERVISED_SOURCE_CARD_DENIAL_MATRIX_SLICE",
    "L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FALSE_FLAGS",
    "L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_PROOF_SLICE",
    "L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_REQUIRED_FIELDS",
    "L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_UNSAFE_FIELDS",
    "L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS",
    "L6V_SUPERVISED_SOURCE_CARD_HELD_SURFACES",
    "L6V_SUPERVISED_SOURCE_CARD_MAX_OPERATION_COUNT",
    "L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS",
    "L6V_SUPERVISED_SOURCE_CARD_REPORT_SAFETY",
    "L6V_SUPERVISED_SOURCE_CARD_REQUIRED_APPROVAL_FIELDS",
    "L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FIXTURE",
    "SupervisedSourceCardPreflightCallbackHarness",
    "build_l6v_report_safe_source_card_descriptor_fixture",
    "build_l6v_report_safe_source_card_descriptor_proof",
    "build_l6v_supervised_source_card_approval_context_fixture",
    "build_l6v_supervised_source_card_denial_matrix_cases",
    "build_l6v_supervised_source_card_preflight_fixture",
    "build_l6v_supervised_source_card_receipt",
    "parse_supervised_source_card_operation_class",
    "run_l6v_supervised_source_card_preflight",
    "validate_l6v_report_safe_source_card_descriptor_fixture",
    "validate_l6v_supervised_source_card_approval_context",
    "validate_l6v_supervised_source_card_preflight_result",
]
