from __future__ import annotations

from collections.abc import Mapping
from typing import Any

L6AI_SCHEMA_VERSION = "l6ai02-current-session-tool-proof-v1"
L6AI_REPOSITORY = "jeremyknows/memory-seam"
L6AI_PARENT_ISSUE = 6
L6AI_RAIL_ISSUE = 322
L6AI_SOURCE_FLOOR = "9c706d0b430f64e0b3ea9fd85b220f6abcb0c497"
L6AI_PARENT_SUCCESSOR_COMMENT_ID = "4654450317"
L6AI_CONTRACT_AUTHORIZATION_COMMENT_ID = "4654450209"
L6AI_PROOF_APPROVAL_COMMENT_ID = "4654450262"
L6AI_OPERATION_CLASS = "L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"
L6AI_ALLOWED_STATUS = "PASS_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"
L6AI_DENIED_STATUS = "DENIED_BEFORE_SOURCE_ACCESS_OUT_OF_SCOPE_CURRENT_SESSION_REQUEST"
L6AI_ALLOWED_LABEL = "EXACT_NO_LIVE_CURRENT_SESSION_TOOL_PROOF"
L6AI_ALLOWED_EVIDENCE_CLASS = "CURRENT_SESSION_TOOL_SHIM_NO_LIVE_REPORT_SAFE"
L6AI_DENIED_EVIDENCE_CLASS = "CURRENT_SESSION_DENIAL_BEFORE_SOURCE_ACCESS"
L6AI_OWNER_ASSOCIATION = "OWNER"

L6AI_GUARDED_COUNTERS = (
    "live_private_read_count",
    "source_card_read_count",
    "raw_private_content_count",
    "raw_source_text_count",
    "raw_approval_prose_count",
    "credential_auth_read_count",
    "discovery_query_count",
    "runtime_registry_read_count",
    "callback_invocation_count",
    "persistence_or_mutation_attempt_count",
    "activation_attempt_count",
    "write_attempt_count",
    "publication_or_gate_movement_attempt_count",
    "broad_allowed_attempt_count",
)

L6AI_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "status",
        "repo",
        "parent_issue",
        "rail_issue",
        "source_floor",
        "parent_successor_comment",
        "contract_authorization_comment",
        "proof_approval_comment",
        "operation_class",
        "evidence_class",
        "allowed",
        "current_session_tool_proof_count",
        "denied_out_of_scope_request_count",
        "denial_before_source_access",
        "artifact_paths",
        "guarded_counters",
        "runtime_registry_consumed",
        "callback_invoked",
        "persistence_or_mutation_attempted",
        "activation_attempted",
        "write_attempted",
        "publication_or_gate_movement_attempted",
        "broad_allowed_attempted",
        "held_surface_flags",
        "non_sensitive_value_metadata",
    }
)

L6AI_REQUIRED_APPROVAL_FIELDS = frozenset(
    {
        "repo",
        "rail_issue",
        "parent_issue",
        "source_floor",
        "parent_successor_comment",
        "contract_authorization_comment",
        "proof_approval_comment",
        "operation_class",
        "actor_association",
        "max_allowed_current_session_tool_proofs",
        "max_denied_out_of_scope_requests",
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

L6AI_UNSAFE_REQUEST_KEYS = (
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
    "source_card_read",
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

L6AI_UNSAFE_ECHO_MARKERS = (
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


def _zero_guarded_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6AI_GUARDED_COUNTERS}


def _held_surface_flags() -> dict[str, bool]:
    return {
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


def _base_receipt() -> dict[str, Any]:
    return {
        "schema_version": L6AI_SCHEMA_VERSION,
        "repo": L6AI_REPOSITORY,
        "parent_issue": L6AI_PARENT_ISSUE,
        "rail_issue": L6AI_RAIL_ISSUE,
        "source_floor": L6AI_SOURCE_FLOOR,
        "parent_successor_comment": L6AI_PARENT_SUCCESSOR_COMMENT_ID,
        "contract_authorization_comment": L6AI_CONTRACT_AUTHORIZATION_COMMENT_ID,
        "proof_approval_comment": L6AI_PROOF_APPROVAL_COMMENT_ID,
        "operation_class": L6AI_OPERATION_CLASS,
        "artifact_paths": [
            "src/memory_seam/l6ai_current_session_tool_proof.py",
            "docs/l6ai02-current-session-allowed-denied-no-live-tool-proof.md",
            "tests/test_l6ai02_current_session_allowed_denied_no_live_tool_proof.py",
        ],
        "guarded_counters": _zero_guarded_counters(),
        "runtime_registry_consumed": False,
        "callback_invoked": False,
        "persistence_or_mutation_attempted": False,
        "activation_attempted": False,
        "write_attempted": False,
        "publication_or_gate_movement_attempted": False,
        "broad_allowed_attempted": False,
        "held_surface_flags": _held_surface_flags(),
        "non_sensitive_value_metadata": {
            "value_class": "public_metadata_only",
            "tool_path": "current_session_memory_seam_shim",
            "no_live": True,
            "report_safe": True,
        },
    }


def build_l6ai02_exact_approval_fixture() -> dict[str, Any]:
    return {
        "repo": L6AI_REPOSITORY,
        "rail_issue": L6AI_RAIL_ISSUE,
        "parent_issue": L6AI_PARENT_ISSUE,
        "source_floor": L6AI_SOURCE_FLOOR,
        "parent_successor_comment": L6AI_PARENT_SUCCESSOR_COMMENT_ID,
        "contract_authorization_comment": L6AI_CONTRACT_AUTHORIZATION_COMMENT_ID,
        "proof_approval_comment": L6AI_PROOF_APPROVAL_COMMENT_ID,
        "operation_class": L6AI_OPERATION_CLASS,
        "actor_association": L6AI_OWNER_ASSOCIATION,
        "max_allowed_current_session_tool_proofs": 1,
        "max_denied_out_of_scope_requests": 1,
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


def approval_allows_l6ai02_current_session_proof(approval: Mapping[str, Any] | None) -> bool:
    if approval is None:
        return False
    if not L6AI_REQUIRED_APPROVAL_FIELDS.issubset(approval.keys()):
        return False
    expected = build_l6ai02_exact_approval_fixture()
    return all(approval.get(key) == value for key, value in expected.items())


def execute_l6ai02_allowed_current_session_no_live_tool_proof(
    approval: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Return the exact report-safe #322 allowed proof receipt.

    The function is a current-session shim over committed public metadata only. It never
    reads live/private data, source cards, credentials, Runtime Registry state, callbacks,
    provider routes, or any mutable runtime surface.
    """

    receipt = _base_receipt()
    if not approval_allows_l6ai02_current_session_proof(approval):
        receipt.update(
            {
                "status": L6AI_DENIED_STATUS,
                "evidence_class": L6AI_DENIED_EVIDENCE_CLASS,
                "allowed": False,
                "current_session_tool_proof_count": 0,
                "denied_out_of_scope_request_count": 0,
                "denial_before_source_access": True,
            }
        )
        return receipt

    receipt.update(
        {
            "status": L6AI_ALLOWED_STATUS,
            "evidence_class": L6AI_ALLOWED_EVIDENCE_CLASS,
            "allowed": L6AI_ALLOWED_LABEL,
            "current_session_tool_proof_count": 1,
            "denied_out_of_scope_request_count": 0,
            "denial_before_source_access": False,
        }
    )
    return receipt


def deny_l6ai02_out_of_scope_current_session_request(
    request_metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Deny the one #322 out-of-scope request before source access.

    The request metadata is only inspected by key name to prove the denial path; no
    request values are echoed into the receipt.
    """

    keys = set(request_metadata or {})
    out_of_scope_requested = bool(keys) and any(
        marker in key.lower().replace("-", "_")
        for key in keys
        for marker in L6AI_UNSAFE_REQUEST_KEYS
    )
    receipt = _base_receipt()
    receipt.update(
        {
            "status": L6AI_DENIED_STATUS,
            "evidence_class": L6AI_DENIED_EVIDENCE_CLASS,
            "allowed": False,
            "current_session_tool_proof_count": 0,
            "denied_out_of_scope_request_count": 1,
            "denial_before_source_access": True,
            "non_sensitive_value_metadata": {
                "value_class": "denial_label_only",
                "out_of_scope_request_detected": out_of_scope_requested,
                "request_values_echoed": False,
            },
        }
    )
    return receipt


def validate_l6ai02_report_safe_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    extra_fields = set(receipt) - L6AI_REPORT_SAFE_FIELDS
    if extra_fields:
        errors.append(f"UNSAFE_EXTRA_FIELDS:{sorted(extra_fields)}")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping):
        errors.append("GUARDED_COUNTER_SET_MISMATCH")
    elif set(counters) != set(L6AI_GUARDED_COUNTERS):
        errors.append("GUARDED_COUNTER_SET_MISMATCH")
    elif any(value != 0 for value in counters.values()):
        errors.append("NON_ZERO_GUARDED_COUNTER")
    if receipt.get("allowed") is True:
        errors.append("BROAD_ALLOWED_TRUE")
    if any(
        receipt.get(field) is not False
        for field in (
            "runtime_registry_consumed",
            "callback_invoked",
            "persistence_or_mutation_attempted",
            "activation_attempted",
            "write_attempted",
            "publication_or_gate_movement_attempted",
            "broad_allowed_attempted",
        )
    ):
        errors.append("HELD_SURFACE_FLAG_TRUE")
    if any(value is not False for value in receipt.get("held_surface_flags", {}).values()):
        errors.append("HELD_SURFACE_FLAG_TRUE")
    if _contains_unsafe_echo(receipt):
        errors.append("UNSAFE_ECHO_MARKER")
    return errors


def _contains_unsafe_echo(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in L6AI_UNSAFE_ECHO_MARKERS)
    if isinstance(value, Mapping):
        return any(_contains_unsafe_echo(item) for item in value.values())
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_unsafe_echo(item) for item in value)
    return False
