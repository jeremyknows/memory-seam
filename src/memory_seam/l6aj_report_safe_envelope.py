from __future__ import annotations

from collections.abc import Mapping
from typing import Any

L6AJ03_SCHEMA_VERSION = "l6aj03-report-safe-source-query-output-envelope-v1"
L6AJ03_REPOSITORY = "jeremyknows/memory-seam"
L6AJ03_PARENT_ISSUE = 6
L6AJ03_RAIL_ISSUE = 333
L6AJ03_RAIL_STARTING_SOURCE_FLOOR = "e7b3e67c438891be00f4001d9cfff72026ebe4d3"
L6AJ03_SOURCE_FLOOR_ENTERING_SLICE = "435c352b03a8ac41d109ec1105b86e1626a65af1"
L6AJ03_PARENT_SUCCESSOR_PREP_COMMENT_ID = "4654676210"
L6AJ03_SCAFFOLD_AUTHORIZATION_COMMENT_ID = "4654676115"
L6AJ03_DENIAL_HARNESS_PREAUTH_COMMENT_ID = "4654676162"
L6AJ03_STATUS = "PASS_REPORT_SAFE_SOURCE_QUERY_OUTPUT_ENVELOPE_READY_NO_EXECUTION"
L6AJ03_OPERATION_CLASS = "L6AJ_SUPERVISED_REAL_READ_REPORT_SAFE_ENVELOPE_PREP"
L6AJ03_EVIDENCE_CLASS = "SUPERVISED_REAL_READ_REPORT_SAFE_ENVELOPE_FIXTURE_ONLY"
L6AJ03_NEXT_FRONTIER = "TRUST_BOUNDARY_AND_STOP_CONDITION_REVIEW_FOR_ISSUE_334"

L6AJ03_SAFE_SOURCE_FIELDS = frozenset(
    {
        "source_binding_ref",
        "source_binding_kind",
        "source_owner_class",
        "source_family_label",
        "source_descriptor_ref",
        "source_card_ref",
        "source_floor",
        "source_access_mode",
        "fixture_only",
    }
)

L6AJ03_SAFE_QUERY_FIELDS = frozenset(
    {
        "query_binding_ref",
        "query_intent_label",
        "query_scope_label",
        "query_output_purpose",
        "max_query_count",
        "denied_out_of_scope_request_count",
        "fixture_only",
    }
)

L6AJ03_SAFE_OUTPUT_FIELDS = frozenset(
    {
        "schema_version",
        "status",
        "repo",
        "parent_issue",
        "rail_issue",
        "operation_class",
        "evidence_class",
        "rail_starting_source_floor",
        "source_floor_entering_slice",
        "parent_successor_prep_comment",
        "scaffold_authorization_comment",
        "denial_harness_preauthorization_comment",
        "allowed",
        "supervised_real_read_execution_authorized",
        "supervised_real_read_count",
        "denied_out_of_scope_request_count",
        "denial_before_read_required",
        "source_binding",
        "query_binding",
        "output_contract",
        "guarded_counters",
        "held_surface_flags",
        "artifact_paths",
        "next_frontier",
    }
)

L6AJ03_OUTPUT_CONTRACT_FIELDS = frozenset(
    {
        "allowed_output_fields",
        "forbidden_output_fields",
        "required_redaction_posture",
        "safe_value_classes",
        "unsafe_echo_rejected",
        "report_safe_only",
        "fixture_only",
    }
)

L6AJ03_GUARDED_COUNTERS = (
    "live_private_read_count",
    "source_card_read_count",
    "raw_private_content_count",
    "raw_source_text_count",
    "raw_approval_prose_count",
    "credential_auth_read_count",
    "source_discovery_count",
    "workspace_scan_count",
    "family_scan_count",
    "broad_recall_count",
    "index_query_count",
    "runtime_registry_read_count",
    "provider_route_invocation_count",
    "callback_invocation_count",
    "persistence_or_mutation_attempt_count",
    "write_attempt_count",
    "activation_attempt_count",
    "cron_change_attempt_count",
    "publication_or_gate_movement_attempt_count",
    "broad_allowed_attempt_count",
)

L6AJ03_FORBIDDEN_OUTPUT_FIELDS = frozenset(
    {
        "raw_private_content",
        "raw_source_text",
        "raw_approval_prose",
        "credential_value",
        "auth_value",
        "env_value",
        "keychain_value",
        "oauth_value",
        "auth_file_material",
        "private_path",
        "source_uri",
        "platform_raw_id",
        "raw_query",
        "query_payload",
        "backend_response",
        "private_correlation_ref",
        "runtime_registry_payload",
        "callback_payload",
        "provider_route_payload",
        "allowed_true_broad_result",
    }
)

L6AJ03_UNSAFE_ECHO_MARKERS = (
    "credential value",
    "oauth token",
    "keychain material",
    "auth-file material",
    "raw private source text",
    "private absolute path",
    "source://",
    "platform-raw-id",
    "raw prompt",
    "raw query",
    "query payload",
    "backend response",
    "private-correlation-ref",
)


def zero_l6aj03_guarded_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6AJ03_GUARDED_COUNTERS}


def held_l6aj03_surface_flags() -> dict[str, bool]:
    return {
        "supervised_real_read_execution": False,
        "live_private_reads": False,
        "source_card_reads": False,
        "raw_private_content": False,
        "raw_source_text": False,
        "raw_approval_prose": False,
        "credentials_auth_env_keychain_oauth_auth_file_reads": False,
        "discovery_workspace_family_scans_broad_recall_index_query": False,
        "runtime_registry_consumption": False,
        "callbacks_provider_routes": False,
        "persistence_runtime_mutation_write_delete_reindex_cache_purge_rollback_execution": False,
        "service_global_activation": False,
        "cron_changes": False,
        "publication_provider_prod_canary_gate_atlas_gate_movement": False,
        "broad_allowed_true_behavior": False,
    }


def build_l6aj03_synthetic_source_binding() -> dict[str, Any]:
    return {
        "source_binding_ref": "synthetic-public-metadata-source-binding:l6aj03",
        "source_binding_kind": "synthetic_fixture_reference",
        "source_owner_class": "owner_approval_required_future_only",
        "source_family_label": "supervised-real-read-step-3-fixture-family",
        "source_descriptor_ref": "descriptor:l6aj03/report-safe-future-source-placeholder",
        "source_card_ref": "source-card:l6aj03/report-safe-future-source-placeholder",
        "source_floor": L6AJ03_SOURCE_FLOOR_ENTERING_SLICE,
        "source_access_mode": "no_live_no_source_card_no_discovery",
        "fixture_only": True,
    }


def build_l6aj03_synthetic_query_binding() -> dict[str, Any]:
    return {
        "query_binding_ref": "synthetic-public-metadata-query-binding:l6aj03",
        "query_intent_label": "future_supervised_real_read_report_safe_value_check",
        "query_scope_label": "single_exact_owner_approved_query_future_only",
        "query_output_purpose": "report_safe_receipt_and_usefulness_metadata_only",
        "max_query_count": 1,
        "denied_out_of_scope_request_count": 1,
        "fixture_only": True,
    }


def build_l6aj03_output_contract() -> dict[str, Any]:
    return {
        "allowed_output_fields": sorted(L6AJ03_SAFE_OUTPUT_FIELDS),
        "forbidden_output_fields": sorted(L6AJ03_FORBIDDEN_OUTPUT_FIELDS),
        "required_redaction_posture": "metadata_labels_booleans_counts_refs_only_no_raw_values",
        "safe_value_classes": [
            "status_label",
            "issue_or_comment_reference",
            "source_floor_hash",
            "synthetic_descriptor_or_source_card_ref",
            "boolean_held_surface_flag_false",
            "zero_guarded_counter",
            "bounded_count",
            "usefulness_label_without_raw_content",
        ],
        "unsafe_echo_rejected": True,
        "report_safe_only": True,
        "fixture_only": True,
    }


def build_l6aj03_report_safe_envelope_fixture() -> dict[str, Any]:
    return {
        "schema_version": L6AJ03_SCHEMA_VERSION,
        "status": L6AJ03_STATUS,
        "repo": L6AJ03_REPOSITORY,
        "parent_issue": L6AJ03_PARENT_ISSUE,
        "rail_issue": L6AJ03_RAIL_ISSUE,
        "operation_class": L6AJ03_OPERATION_CLASS,
        "evidence_class": L6AJ03_EVIDENCE_CLASS,
        "rail_starting_source_floor": L6AJ03_RAIL_STARTING_SOURCE_FLOOR,
        "source_floor_entering_slice": L6AJ03_SOURCE_FLOOR_ENTERING_SLICE,
        "parent_successor_prep_comment": L6AJ03_PARENT_SUCCESSOR_PREP_COMMENT_ID,
        "scaffold_authorization_comment": L6AJ03_SCAFFOLD_AUTHORIZATION_COMMENT_ID,
        "denial_harness_preauthorization_comment": L6AJ03_DENIAL_HARNESS_PREAUTH_COMMENT_ID,
        "allowed": False,
        "supervised_real_read_execution_authorized": False,
        "supervised_real_read_count": 0,
        "denied_out_of_scope_request_count": 0,
        "denial_before_read_required": True,
        "source_binding": build_l6aj03_synthetic_source_binding(),
        "query_binding": build_l6aj03_synthetic_query_binding(),
        "output_contract": build_l6aj03_output_contract(),
        "guarded_counters": zero_l6aj03_guarded_counters(),
        "held_surface_flags": held_l6aj03_surface_flags(),
        "artifact_paths": [
            "src/memory_seam/l6aj_report_safe_envelope.py",
            "docs/l6aj03-report-safe-source-query-output-envelope.md",
            "tests/test_l6aj03_report_safe_source_query_output_envelope.py",
        ],
        "next_frontier": L6AJ03_NEXT_FRONTIER,
    }


def validate_l6aj03_source_query_output_envelope(envelope: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    extra_fields = set(envelope) - L6AJ03_SAFE_OUTPUT_FIELDS
    if extra_fields:
        errors.append(f"UNSAFE_EXTRA_FIELDS:{sorted(extra_fields)}")
    source_binding = envelope.get("source_binding")
    if not isinstance(source_binding, Mapping) or set(source_binding) != L6AJ03_SAFE_SOURCE_FIELDS:
        errors.append("SOURCE_BINDING_FIELD_SET_MISMATCH")
    query_binding = envelope.get("query_binding")
    if not isinstance(query_binding, Mapping) or set(query_binding) != L6AJ03_SAFE_QUERY_FIELDS:
        errors.append("QUERY_BINDING_FIELD_SET_MISMATCH")
    output_contract = envelope.get("output_contract")
    if not isinstance(output_contract, Mapping) or set(output_contract) != L6AJ03_OUTPUT_CONTRACT_FIELDS:
        errors.append("OUTPUT_CONTRACT_FIELD_SET_MISMATCH")
    elif set(output_contract.get("forbidden_output_fields", ())) != L6AJ03_FORBIDDEN_OUTPUT_FIELDS:
        errors.append("FORBIDDEN_OUTPUT_FIELD_SET_MISMATCH")
    counters = envelope.get("guarded_counters")
    if not isinstance(counters, Mapping) or set(counters) != set(L6AJ03_GUARDED_COUNTERS):
        errors.append("GUARDED_COUNTER_SET_MISMATCH")
    elif any(value != 0 for value in counters.values()):
        errors.append("NON_ZERO_GUARDED_COUNTER")
    if any(value is not False for value in envelope.get("held_surface_flags", {}).values()):
        errors.append("HELD_SURFACE_FLAG_TRUE")
    if envelope.get("allowed") is True:
        errors.append("BROAD_ALLOWED_TRUE")
    if envelope.get("supervised_real_read_execution_authorized") is True:
        errors.append("EXECUTION_AUTHORIZED_IN_PREP_ENVELOPE")
    if envelope.get("supervised_real_read_count") != 0:
        errors.append("NONZERO_SUPERVISED_REAL_READ_COUNT")
    if _contains_l6aj03_unsafe_echo(envelope):
        errors.append("UNSAFE_ECHO_MARKER")
    return errors


def _contains_l6aj03_unsafe_echo(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in L6AJ03_UNSAFE_ECHO_MARKERS)
    if isinstance(value, Mapping):
        return any(_contains_l6aj03_unsafe_echo(item) for item in value.values())
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_l6aj03_unsafe_echo(item) for item in value)
    return False
