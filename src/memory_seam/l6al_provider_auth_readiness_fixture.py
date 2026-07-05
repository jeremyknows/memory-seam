from __future__ import annotations

from collections.abc import Mapping
from typing import Any

L6AL02_SCHEMA_VERSION = "l6al02-provider-auth-readiness-fixture-v1"
L6AL02_REPOSITORY = "jeremyknows/memory-seam"
L6AL02_PARENT_ISSUE = 6
L6AL02_RAIL_ISSUE = 350
L6AL02_RAIL_STARTING_SOURCE_FLOOR = "f335f09891a41f43583fbf434482cfb096a04fcd"
L6AL02_OPERATION_CLASS = "L6AL_PROVIDER_AUTH_READINESS_FIXTURE"
L6AL02_EVIDENCE_CLASS = "NO_LIVE_SERVICE_PROVIDER_AUTH_READINESS_FIXTURE"
L6AL02_READY_STATUS = "AUTH_READY_FIXTURE_VERIFIED_READ_NOT_EXECUTED"
L6AL02_DENIED_STATUS = "DENIED_BEFORE_READ_AUTH_MISMATCH"

EXPECTED_ROUTE_AUDIENCE = "memory-seam:read:recall"
EXPECTED_ACTING_FOR = "sax"
EXPECTED_IDENTITY_SUBJECT = "atlas-query-supervised-metadata-reader"
EXPECTED_AGENT = "sax"
EXPECTED_SCOPE = "metadata_only:wiki:health:max_one"
EXPECTED_EVIDENCE_CLASS = "SUPERVISED_METADATA_RECALL_READ_RETRY"
EXPECTED_EXPIRY_STATE = "fresh_issue_bound_not_expired"

L6AL02_GUARDED_COUNTERS = (
    "source_item_count",
    "source_read_callback_count",
    "provider_callback_count",
    "provider_route_invocation_count",
    "live_private_read_count",
    "source_discovery_count",
    "runtime_registry_read_count",
    "credential_or_secret_read_count",
    "persistence_or_mutation_attempt_count",
    "activation_attempt_count",
    "publication_or_gate_movement_attempt_count",
    "broad_allowed_attempt_count",
)

L6AL02_REPORT_SAFE_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "operation_class",
        "evidence_class",
        "status",
        "auth_ready",
        "read_authorized",
        "retry_executed",
        "denial_before_read",
        "denial_reason",
        "items",
        "guarded_counters",
        "binding_summary",
        "artifact_paths",
    }
)

UNSAFE_REQUEST_KEYS = frozenset(
    {
        "credential_value",
        "auth_value",
        "env_value",
        "keychain_value",
        "oauth_value",
        "auth_file_material",
        "raw_private_content",
        "raw_source_text",
        "raw_output_requested",
        "provider_payload",
        "callback_payload",
        "runtime_registry_payload",
        "allowed_true",
    }
)


def zero_l6al02_guarded_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6AL02_GUARDED_COUNTERS}


def build_l6al02_authorized_metadata_readiness_fixture() -> dict[str, Any]:
    """Return a non-secret positive readiness fixture; it is not read authority."""

    return {
        "route_audience": EXPECTED_ROUTE_AUDIENCE,
        "acting_for": EXPECTED_ACTING_FOR,
        "identity_subject": EXPECTED_IDENTITY_SUBJECT,
        "agent": EXPECTED_AGENT,
        "scope": EXPECTED_SCOPE,
        "evidence_class": EXPECTED_EVIDENCE_CLASS,
        "expiry": EXPECTED_EXPIRY_STATE,
        "metadata_only": True,
        "report_safe": True,
        "max_operation_count": 1,
        "provider_binding_present": True,
        "service_binding_present": True,
        "authorization_narrowing": "exact",
        "source_read_callback": "fixture-inert-not-callable",
    }


def build_l6al02_denied_auth_mismatch_fixture(reason: str) -> dict[str, Any]:
    request = build_l6al02_authorized_metadata_readiness_fixture()
    if reason == "wrong_route_audience":
        request["route_audience"] = "memory-seam:read:context"
    elif reason == "unauthorized_narrowing":
        request["authorization_narrowing"] = "context_only_without_recall"
    elif reason == "missing_identity_subject":
        request.pop("identity_subject", None)
    elif reason == "stale_approval":
        request["expiry"] = "stale_or_missing"
    elif reason == "broadened_scope_denied":
        request["scope"] = "metadata_and_raw_or_all"
    else:
        request["authorization_narrowing"] = reason
    return request


def _binding_summary(request: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "route_audience_matched": request.get("route_audience") == EXPECTED_ROUTE_AUDIENCE,
        "acting_for": request.get("acting_for"),
        "identity_subject_present": bool(request.get("identity_subject")),
        "agent": request.get("agent"),
        "scope": request.get("scope"),
        "evidence_class": request.get("evidence_class"),
        "expiry": request.get("expiry"),
        "provider_binding_present": request.get("provider_binding_present") is True,
        "service_binding_present": request.get("service_binding_present") is True,
        "authorization_narrowing": request.get("authorization_narrowing"),
        "metadata_only": request.get("metadata_only") is True,
        "report_safe": request.get("report_safe") is True,
    }


def _base_receipt(request: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": L6AL02_SCHEMA_VERSION,
        "repo": L6AL02_REPOSITORY,
        "parent_issue": L6AL02_PARENT_ISSUE,
        "rail_issue": L6AL02_RAIL_ISSUE,
        "rail_starting_source_floor": L6AL02_RAIL_STARTING_SOURCE_FLOOR,
        "operation_class": L6AL02_OPERATION_CLASS,
        "evidence_class": L6AL02_EVIDENCE_CLASS,
        "read_authorized": False,
        "retry_executed": False,
        "denial_before_read": True,
        "items": [],
        "guarded_counters": zero_l6al02_guarded_counters(),
        "binding_summary": _binding_summary(request),
        "artifact_paths": [
            "src/memory_seam/l6al_provider_auth_readiness_fixture.py",
            "docs/l6al02-provider-auth-readiness-fixture.md",
            "tests/test_l6al02_provider_auth_readiness_fixture.py",
        ],
    }


def _denied(request: Mapping[str, Any], reason: str) -> dict[str, Any]:
    receipt = _base_receipt(request)
    receipt.update(
        {
            "status": L6AL02_DENIED_STATUS,
            "auth_ready": False,
            "denial_reason": reason,
        }
    )
    return receipt


def evaluate_l6al02_provider_auth_readiness(request: Mapping[str, Any] | None) -> dict[str, Any]:
    """Evaluate fixture-only service/provider auth readiness without reading anything.

    The evaluator accepts non-secret labels only. It does not load environment values,
    keychain entries, OAuth material, auth files, credentials, Runtime Registry data,
    provider payloads, callback payloads, source descriptors, source items, or private
    content, and it never invokes callbacks/routes/services.
    """

    if request is None:
        return _denied({}, "missing_identity_subject")

    unsafe = UNSAFE_REQUEST_KEYS.intersection(request.keys())
    if unsafe:
        if "allowed_true" in unsafe:
            return _denied(request, "broad_allowed_true_denied")
        return _denied(request, "raw_output_denied")

    if not request.get("identity_subject"):
        return _denied(request, "missing_identity_subject")
    if request.get("identity_subject") != EXPECTED_IDENTITY_SUBJECT:
        return _denied(request, "mismatched_identity_subject")
    if request.get("acting_for") != EXPECTED_ACTING_FOR or request.get("agent") != EXPECTED_AGENT:
        return _denied(request, "mismatched_agent")
    if request.get("route_audience") != EXPECTED_ROUTE_AUDIENCE:
        return _denied(request, "wrong_route_audience")
    if request.get("authorization_narrowing") != "exact":
        return _denied(request, "unauthorized_narrowing")
    if request.get("scope") != EXPECTED_SCOPE or request.get("max_operation_count") != 1:
        return _denied(request, "broadened_scope_denied")
    if request.get("metadata_only") is not True or request.get("report_safe") is not True:
        return _denied(request, "raw_output_denied")
    if request.get("expiry") != EXPECTED_EXPIRY_STATE:
        return _denied(request, "stale_approval")
    if request.get("evidence_class") != EXPECTED_EVIDENCE_CLASS:
        return _denied(request, "mismatched_evidence_class")
    if request.get("provider_binding_present") is not True or request.get("service_binding_present") is not True:
        return _denied(request, "service_provider_binding_incomplete")

    receipt = _base_receipt(request)
    receipt.update(
        {
            "status": L6AL02_READY_STATUS,
            "auth_ready": True,
            "denial_reason": None,
        }
    )
    return receipt


def assert_l6al02_report_safe_receipt(receipt: Mapping[str, Any]) -> None:
    extra_fields = set(receipt) - L6AL02_REPORT_SAFE_FIELDS
    if extra_fields:
        raise AssertionError(f"unexpected unsafe receipt fields: {sorted(extra_fields)}")
    if receipt.get("read_authorized") is not False or receipt.get("retry_executed") is not False:
        raise AssertionError("#350 receipts must not authorize or execute reads")
    if receipt.get("items") != []:
        raise AssertionError("#350 receipts must not return source items")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero before auth/read execution")
    for counter in ("source_item_count", "source_read_callback_count", "provider_callback_count"):
        if counters.get(counter) != 0:
            raise AssertionError(f"read/provider callback counter must stay zero: {counter}")
