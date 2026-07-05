from __future__ import annotations

from collections.abc import Mapping
from typing import Any

L6AK03_SCHEMA_VERSION = "l6ak03-route-audience-auth-contract-v1"
L6AK03_REPOSITORY = "jeremyknows/memory-seam"
L6AK03_PARENT_ISSUE = 6
L6AK03_RAIL_ISSUE = 343
L6AK03_RAIL_STARTING_SOURCE_FLOOR = "95e7a7979ae092703da8f77c4d897f703348a308"
L6AK03_SOURCE_FLOOR_ENTERING_SLICE = "5346907"
L6AK03_PRIOR_RECEIPT_PR = 345
L6AK03_PRIOR_DESIGN_PR = 346
L6AK03_OPERATION_CLASS = "L6AK_NON_SECRET_ROUTE_AUDIENCE_AUTH_CONTRACT_SHIM"
L6AK03_EVIDENCE_CLASS = "SUPERVISED_METADATA_READ_AUTH_CONTRACT_TYPED_RECEIPT"
L6AK03_READY_STATUS = "READY_FOR_EXACT_RETRY_AUTH_BINDING_VERIFIED_RETRY_NOT_EXECUTED"
L6AK03_DENIED_STATUS = "DENIED_BEFORE_READ_AUTH_BINDING_MISMATCH"

EXPECTED_IDENTITY_SUBJECT = "atlas-query-supervised-metadata-reader"
EXPECTED_ACTING_FOR = "sax"
EXPECTED_AGENT = "sax"
EXPECTED_AUDIENCE = "memory-seam:supervised-metadata-read:atlas-query-mcp"
EXPECTED_RECALL_SCOPE = "wiki"
EXPECTED_CONTEXT_INCLUDE = "health"
EXPECTED_OUTPUT_MODE = "metadata_only_report_safe"
EXPECTED_APPROVAL_FRESHNESS = "fresh_issue_bound_l6ak"
EXPECTED_MAX_OPERATION_COUNT = 1

L6AK03_GUARDED_COUNTERS = (
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

L6AK03_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "status",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "source_floor_entering_slice",
        "prior_receipt_pr",
        "prior_design_pr",
        "operation_class",
        "evidence_class",
        "ready_for_exact_retry",
        "retry_executed",
        "read_authorized",
        "denial_before_read",
        "denial_reason",
        "source_access_attempted",
        "source_discovery_attempted",
        "runtime_registry_consumed",
        "provider_route_invoked",
        "callback_invoked",
        "persistence_or_mutation_attempted",
        "activation_attempted",
        "publication_or_gate_movement_attempted",
        "broad_allowed_attempted",
        "guarded_counters",
        "binding_summary",
        "artifact_paths",
    }
)

UNSAFE_REQUEST_KEYS = frozenset(
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
        "provider_payload",
        "allowed_true",
    }
)


def zero_l6ak03_guarded_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6AK03_GUARDED_COUNTERS}


def build_l6ak03_exact_binding_fixture() -> dict[str, Any]:
    return {
        "identity_subject": EXPECTED_IDENTITY_SUBJECT,
        "acting_for": EXPECTED_ACTING_FOR,
        "agent": EXPECTED_AGENT,
        "audience": EXPECTED_AUDIENCE,
        "scope": EXPECTED_RECALL_SCOPE,
        "context_include": EXPECTED_CONTEXT_INCLUDE,
        "output_mode": EXPECTED_OUTPUT_MODE,
        "approval_freshness": EXPECTED_APPROVAL_FRESHNESS,
        "max_operation_count": EXPECTED_MAX_OPERATION_COUNT,
        "metadata_only": True,
        "report_safe": True,
        "raw_output_requested": False,
        "broader_scope_requested": False,
        "service_activation_requested": False,
        "provider_route_requested": False,
        "runtime_registry_requested": False,
        "persistence_or_mutation_requested": False,
        "publication_or_gate_movement_requested": False,
    }


def _binding_summary(request: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "identity_subject_present": bool(request.get("identity_subject")),
        "acting_for": request.get("acting_for"),
        "agent": request.get("agent"),
        "audience_matched": request.get("audience") == EXPECTED_AUDIENCE,
        "scope": request.get("scope"),
        "context_include": request.get("context_include"),
        "output_mode": request.get("output_mode"),
        "approval_freshness": request.get("approval_freshness"),
        "max_operation_count": request.get("max_operation_count"),
        "metadata_only": request.get("metadata_only") is True,
        "report_safe": request.get("report_safe") is True,
    }


def _base_receipt(request: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": L6AK03_SCHEMA_VERSION,
        "repo": L6AK03_REPOSITORY,
        "parent_issue": L6AK03_PARENT_ISSUE,
        "rail_issue": L6AK03_RAIL_ISSUE,
        "rail_starting_source_floor": L6AK03_RAIL_STARTING_SOURCE_FLOOR,
        "source_floor_entering_slice": L6AK03_SOURCE_FLOOR_ENTERING_SLICE,
        "prior_receipt_pr": L6AK03_PRIOR_RECEIPT_PR,
        "prior_design_pr": L6AK03_PRIOR_DESIGN_PR,
        "operation_class": L6AK03_OPERATION_CLASS,
        "evidence_class": L6AK03_EVIDENCE_CLASS,
        "retry_executed": False,
        "read_authorized": False,
        "denial_before_read": True,
        "source_access_attempted": False,
        "source_discovery_attempted": False,
        "runtime_registry_consumed": False,
        "provider_route_invoked": False,
        "callback_invoked": False,
        "persistence_or_mutation_attempted": False,
        "activation_attempted": False,
        "publication_or_gate_movement_attempted": False,
        "broad_allowed_attempted": False,
        "guarded_counters": zero_l6ak03_guarded_counters(),
        "binding_summary": _binding_summary(request),
        "artifact_paths": [
            "src/memory_seam/l6ak_route_audience_auth_contract.py",
            "docs/l6ak03-non-secret-auth-contract-shim.md",
            "tests/test_l6ak03_route_audience_auth_contract.py",
        ],
    }


def _denied(request: Mapping[str, Any], reason: str) -> dict[str, Any]:
    receipt = _base_receipt(request)
    receipt.update(
        {
            "status": L6AK03_DENIED_STATUS,
            "ready_for_exact_retry": False,
            "denial_reason": reason,
        }
    )
    return receipt


def evaluate_l6ak03_route_audience_contract(request: Mapping[str, Any] | None) -> dict[str, Any]:
    """Validate non-secret auth/audience bindings without executing any read.

    The function is pure and data-only: it does not read environment variables, auth
    files, keychains, OAuth material, Runtime Registry state, provider callbacks, or
    source data. A success result is readiness metadata only, not read authorization.
    """
    if request is None:
        return _denied({}, "missing_identity_subject")

    unsafe = UNSAFE_REQUEST_KEYS.intersection(request.keys())
    if unsafe:
        if "allowed_true" in unsafe:
            return _denied(request, "broad_allowed_true_requested")
        return _denied(request, "raw_output_requested")

    if not request.get("identity_subject"):
        return _denied(request, "missing_identity_subject")
    if request.get("identity_subject") != EXPECTED_IDENTITY_SUBJECT:
        return _denied(request, "mismatched_identity_subject")
    if request.get("acting_for") != EXPECTED_ACTING_FOR or request.get("agent") != EXPECTED_AGENT:
        return _denied(request, "mismatched_agent")
    if request.get("audience") != EXPECTED_AUDIENCE:
        return _denied(request, "wrong_route_audience")
    if request.get("scope") != EXPECTED_RECALL_SCOPE or request.get("broader_scope_requested") is True:
        return _denied(request, "broadened_scope")
    if request.get("context_include") != EXPECTED_CONTEXT_INCLUDE:
        return _denied(request, "unauthorized_narrowing")
    if request.get("output_mode") != EXPECTED_OUTPUT_MODE or request.get("raw_output_requested") is True:
        return _denied(request, "raw_output_requested")
    if request.get("approval_freshness") != EXPECTED_APPROVAL_FRESHNESS:
        return _denied(request, "stale_approval")
    if request.get("max_operation_count") != EXPECTED_MAX_OPERATION_COUNT:
        return _denied(request, "broadened_scope")
    if request.get("metadata_only") is not True or request.get("report_safe") is not True:
        return _denied(request, "raw_output_requested")
    for held_key, reason in (
        ("service_activation_requested", "activation_requested"),
        ("provider_route_requested", "provider_route_requested"),
        ("runtime_registry_requested", "runtime_registry_requested"),
        ("persistence_or_mutation_requested", "persistence_or_mutation_requested"),
        ("publication_or_gate_movement_requested", "publication_or_gate_movement_requested"),
    ):
        if request.get(held_key) is True:
            return _denied(request, reason)

    receipt = _base_receipt(request)
    receipt.update(
        {
            "status": L6AK03_READY_STATUS,
            "ready_for_exact_retry": True,
            "denial_reason": None,
        }
    )
    return receipt


def assert_l6ak03_report_safe_receipt(receipt: Mapping[str, Any]) -> None:
    extra_fields = set(receipt) - L6AK03_REPORT_SAFE_FIELDS
    if extra_fields:
        raise AssertionError(f"unexpected unsafe receipt fields: {sorted(extra_fields)}")
    if receipt.get("read_authorized") is not False or receipt.get("retry_executed") is not False:
        raise AssertionError("#343 receipts must not authorize or execute reads")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero")
    for flag in (
        "source_access_attempted",
        "source_discovery_attempted",
        "runtime_registry_consumed",
        "provider_route_invoked",
        "callback_invoked",
        "persistence_or_mutation_attempted",
        "activation_attempted",
        "publication_or_gate_movement_attempted",
        "broad_allowed_attempted",
    ):
        if receipt.get(flag) is not False:
            raise AssertionError(f"held flag must remain false: {flag}")
