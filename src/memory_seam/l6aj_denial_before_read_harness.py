from __future__ import annotations

from collections.abc import Mapping
from typing import Any

L6AJ_SCHEMA_VERSION = "l6aj02-denial-before-read-fixture-harness-v1"
L6AJ_REPOSITORY = "jeremyknows/memory-seam"
L6AJ_PARENT_ISSUE = 6
L6AJ_RAIL_ISSUE = 332
L6AJ_RAIL_STARTING_SOURCE_FLOOR = "e7b3e67c438891be00f4001d9cfff72026ebe4d3"
L6AJ_SOURCE_FLOOR_ENTERING_SLICE = "55c3fec203ba0398347cdc441dbb2be36cf290ca"
L6AJ_PARENT_SUCCESSOR_PREP_COMMENT_ID = "4654676210"
L6AJ_SCAFFOLD_AUTHORIZATION_COMMENT_ID = "4654676115"
L6AJ_DENIAL_HARNESS_PREAUTH_COMMENT_ID = "4654676162"
L6AJ_OPERATION_CLASS = "L6AJ_SUPERVISED_REAL_READ_DENIAL_BEFORE_READ_FIXTURE_HARNESS"
L6AJ_STATUS = "PASS_DENIAL_BEFORE_READ_FIXTURE_HARNESS_READY_NO_LIVE_READ"
L6AJ_DENIED_STATUS = "DENIED_BEFORE_READ_OUT_OF_SCOPE_SUPERVISED_REAL_READ_REQUEST"
L6AJ_DENIED_EVIDENCE_CLASS = "SUPERVISED_REAL_READ_DENIAL_BEFORE_READ_FIXTURE_ONLY"
L6AJ_ALLOWED_EXECUTION_STATUS = "HELD_SUPERVISED_REAL_READ_EXECUTION_NOT_AUTHORIZED"
L6AJ_OWNER_ASSOCIATION = "OWNER"

L6AJ_GUARDED_COUNTERS = (
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
    "delete_reindex_cache_purge_rollback_attempt_count",
    "activation_attempt_count",
    "cron_change_attempt_count",
    "publication_or_gate_movement_attempt_count",
    "broad_allowed_attempt_count",
)

L6AJ_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "status",
        "repo",
        "parent_issue",
        "rail_issue",
        "source_floor",
        "rail_starting_source_floor",
        "parent_successor_prep_comment",
        "scaffold_authorization_comment",
        "denial_harness_preauthorization_comment",
        "operation_class",
        "evidence_class",
        "allowed",
        "supervised_real_read_count",
        "denied_out_of_scope_request_count",
        "denial_before_read",
        "source_access_attempted",
        "source_card_access_attempted",
        "live_adapter_invoked",
        "runtime_registry_consumed",
        "provider_route_invoked",
        "callback_invoked",
        "persistence_or_mutation_attempted",
        "activation_attempted",
        "write_attempted",
        "publication_or_gate_movement_attempted",
        "broad_allowed_attempted",
        "guarded_counters",
        "held_surface_flags",
        "inert_spy_summary",
        "non_sensitive_value_metadata",
        "artifact_paths",
    }
)

L6AJ_REQUIRED_HARNESS_PREAUTH_FIELDS = frozenset(
    {
        "repo",
        "rail_issue",
        "parent_issue",
        "rail_starting_source_floor",
        "source_floor",
        "parent_successor_prep_comment",
        "scaffold_authorization_comment",
        "denial_harness_preauthorization_comment",
        "operation_class",
        "actor_association",
        "max_denied_out_of_scope_requests",
        "supervised_real_read_execution_authorized",
        "live_private_reads_authorized",
        "source_card_reads_authorized",
        "raw_private_or_source_or_approval_prose_authorized",
        "credentials_or_auth_reads_authorized",
        "discovery_or_scan_authorized",
        "runtime_registry_authorized",
        "callbacks_or_provider_routes_authorized",
        "persistence_or_mutation_authorized",
        "service_or_global_activation_authorized",
        "cron_changes_authorized",
        "publication_or_gate_movement_authorized",
        "writes_authorized",
        "broad_allowed_true_authorized",
    }
)

L6AJ_UNSAFE_REQUEST_KEYS = (
    "raw",
    "private",
    "source_text",
    "approval_prose",
    "credential",
    "auth",
    "env",
    "keychain",
    "oauth",
    "auth_file",
    "discovery",
    "workspace_scan",
    "family_scan",
    "broad_recall",
    "index_query",
    "live_read",
    "source_card",
    "source_access",
    "runtime_registry",
    "callback",
    "provider_route",
    "persist",
    "mutation",
    "write",
    "delete",
    "reindex",
    "cache_purge",
    "rollback",
    "activation",
    "cron",
    "publication",
    "visibility",
    "gate_movement",
    "atlas_gate",
    "allowed_true",
)

L6AJ_UNSAFE_ECHO_MARKERS = (
    "credential value",
    "oauth token",
    "keychain material",
    "auth-file material",
    "source://",
    "platform-raw-id",
    "private absolute path",
    "raw prompt",
    "raw query",
    "query payload",
    "backend response",
    "private-correlation-ref",
    "raw private source text",
)


def zero_l6aj_guarded_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6AJ_GUARDED_COUNTERS}


def held_l6aj_surface_flags() -> dict[str, bool]:
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


def build_l6aj02_harness_preauthorization_fixture() -> dict[str, Any]:
    return {
        "repo": L6AJ_REPOSITORY,
        "rail_issue": L6AJ_RAIL_ISSUE,
        "parent_issue": L6AJ_PARENT_ISSUE,
        "rail_starting_source_floor": L6AJ_RAIL_STARTING_SOURCE_FLOOR,
        "source_floor": L6AJ_SOURCE_FLOOR_ENTERING_SLICE,
        "parent_successor_prep_comment": L6AJ_PARENT_SUCCESSOR_PREP_COMMENT_ID,
        "scaffold_authorization_comment": L6AJ_SCAFFOLD_AUTHORIZATION_COMMENT_ID,
        "denial_harness_preauthorization_comment": L6AJ_DENIAL_HARNESS_PREAUTH_COMMENT_ID,
        "operation_class": L6AJ_OPERATION_CLASS,
        "actor_association": L6AJ_OWNER_ASSOCIATION,
        "max_denied_out_of_scope_requests": 1,
        "supervised_real_read_execution_authorized": False,
        "live_private_reads_authorized": False,
        "source_card_reads_authorized": False,
        "raw_private_or_source_or_approval_prose_authorized": False,
        "credentials_or_auth_reads_authorized": False,
        "discovery_or_scan_authorized": False,
        "runtime_registry_authorized": False,
        "callbacks_or_provider_routes_authorized": False,
        "persistence_or_mutation_authorized": False,
        "service_or_global_activation_authorized": False,
        "cron_changes_authorized": False,
        "publication_or_gate_movement_authorized": False,
        "writes_authorized": False,
        "broad_allowed_true_authorized": False,
    }


def preauthorization_allows_l6aj02_denial_harness(preauthorization: Mapping[str, Any] | None) -> bool:
    if preauthorization is None:
        return False
    if not L6AJ_REQUIRED_HARNESS_PREAUTH_FIELDS.issubset(preauthorization.keys()):
        return False
    expected = build_l6aj02_harness_preauthorization_fixture()
    return all(preauthorization.get(key) == value for key, value in expected.items())


def _base_receipt() -> dict[str, Any]:
    return {
        "schema_version": L6AJ_SCHEMA_VERSION,
        "repo": L6AJ_REPOSITORY,
        "parent_issue": L6AJ_PARENT_ISSUE,
        "rail_issue": L6AJ_RAIL_ISSUE,
        "source_floor": L6AJ_SOURCE_FLOOR_ENTERING_SLICE,
        "rail_starting_source_floor": L6AJ_RAIL_STARTING_SOURCE_FLOOR,
        "parent_successor_prep_comment": L6AJ_PARENT_SUCCESSOR_PREP_COMMENT_ID,
        "scaffold_authorization_comment": L6AJ_SCAFFOLD_AUTHORIZATION_COMMENT_ID,
        "denial_harness_preauthorization_comment": L6AJ_DENIAL_HARNESS_PREAUTH_COMMENT_ID,
        "operation_class": L6AJ_OPERATION_CLASS,
        "artifact_paths": [
            "src/memory_seam/l6aj_denial_before_read_harness.py",
            "docs/l6aj02-denial-before-read-fixture-harness.md",
            "tests/test_l6aj02_denial_before_read_fixture_harness.py",
        ],
        "guarded_counters": zero_l6aj_guarded_counters(),
        "held_surface_flags": held_l6aj_surface_flags(),
        "source_access_attempted": False,
        "source_card_access_attempted": False,
        "live_adapter_invoked": False,
        "runtime_registry_consumed": False,
        "provider_route_invoked": False,
        "callback_invoked": False,
        "persistence_or_mutation_attempted": False,
        "activation_attempted": False,
        "write_attempted": False,
        "publication_or_gate_movement_attempted": False,
        "broad_allowed_attempted": False,
        "inert_spy_summary": {
            "spy_class": "inert_fixture_counters_only",
            "source_access_spy_count": 0,
            "provider_callback_spy_count": 0,
            "runtime_registry_spy_count": 0,
            "mutation_spy_count": 0,
        },
        "non_sensitive_value_metadata": {
            "value_class": "denial_label_only",
            "fixture_only": True,
            "request_values_echoed": False,
        },
    }


def deny_l6aj02_out_of_scope_supervised_real_read_request(
    request_metadata: Mapping[str, Any] | None = None,
    preauthorization: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a report-safe denied-before-read receipt for #332.

    Only request key names are inspected. No request values are echoed, no source
    references are dereferenced, and every guarded callback/provider/Registry/mutation
    counter remains zero.
    """

    keys = set(request_metadata or {})
    out_of_scope_requested = bool(keys) and any(
        marker in key.lower().replace("-", "_")
        for key in keys
        for marker in L6AJ_UNSAFE_REQUEST_KEYS
    )
    receipt = _base_receipt()
    receipt.update(
        {
            "status": L6AJ_DENIED_STATUS,
            "evidence_class": L6AJ_DENIED_EVIDENCE_CLASS,
            "allowed": False,
            "supervised_real_read_count": 0,
            "denied_out_of_scope_request_count": 1,
            "denial_before_read": True,
            "non_sensitive_value_metadata": {
                "value_class": "denial_label_only",
                "fixture_only": True,
                "request_values_echoed": False,
                "out_of_scope_request_detected": out_of_scope_requested,
                "preauthorization_fixture_matched": preauthorization_allows_l6aj02_denial_harness(
                    preauthorization
                ),
            },
        }
    )
    return receipt


def attempt_l6aj02_allowed_supervised_real_read(
    preauthorization: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Fail closed: #332 has no authority to perform an allowed real read."""

    receipt = _base_receipt()
    receipt.update(
        {
            "status": L6AJ_ALLOWED_EXECUTION_STATUS,
            "evidence_class": L6AJ_DENIED_EVIDENCE_CLASS,
            "allowed": False,
            "supervised_real_read_count": 0,
            "denied_out_of_scope_request_count": 0,
            "denial_before_read": True,
            "non_sensitive_value_metadata": {
                "value_class": "execution_hold_label_only",
                "fixture_only": True,
                "preauthorization_fixture_matched": preauthorization_allows_l6aj02_denial_harness(
                    preauthorization
                ),
                "execution_approval_present": False,
            },
        }
    )
    return receipt


def validate_l6aj02_report_safe_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    extra_fields = set(receipt) - L6AJ_REPORT_SAFE_FIELDS
    if extra_fields:
        errors.append(f"UNSAFE_EXTRA_FIELDS:{sorted(extra_fields)}")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping):
        errors.append("GUARDED_COUNTER_SET_MISMATCH")
    elif set(counters) != set(L6AJ_GUARDED_COUNTERS):
        errors.append("GUARDED_COUNTER_SET_MISMATCH")
    elif any(value != 0 for value in counters.values()):
        errors.append("NON_ZERO_GUARDED_COUNTER")
    if receipt.get("allowed") is True:
        errors.append("BROAD_ALLOWED_TRUE")
    for field in (
        "source_access_attempted",
        "source_card_access_attempted",
        "live_adapter_invoked",
        "runtime_registry_consumed",
        "provider_route_invoked",
        "callback_invoked",
        "persistence_or_mutation_attempted",
        "activation_attempted",
        "write_attempted",
        "publication_or_gate_movement_attempted",
        "broad_allowed_attempted",
    ):
        if receipt.get(field) is not False:
            errors.append("HELD_SURFACE_FLAG_TRUE")
            break
    if any(value is not False for value in receipt.get("held_surface_flags", {}).values()):
        errors.append("HELD_SURFACE_FLAG_TRUE")
    if _contains_unsafe_echo(receipt):
        errors.append("UNSAFE_ECHO_MARKER")
    return errors


def _contains_unsafe_echo(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in L6AJ_UNSAFE_ECHO_MARKERS)
    if isinstance(value, Mapping):
        return any(_contains_unsafe_echo(item) for item in value.values())
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_unsafe_echo(item) for item in value)
    return False
