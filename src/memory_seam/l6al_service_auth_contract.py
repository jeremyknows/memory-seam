from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal

L6AL03_SCHEMA_VERSION = "l6al03-service-auth-contract-v1"
L6AL03_REPOSITORY = "jeremyknows/memory-seam"
L6AL03_PARENT_ISSUE = 6
L6AL03_RAIL_ISSUE = 351
L6AL03_RAIL_STARTING_SOURCE_FLOOR = "f335f09891a41f43583fbf434482cfb096a04fcd"
L6AL03_OPERATION_CLASS = "L6AL_MINIMAL_NON_SECRET_SERVICE_AUTH_CONTRACT"
L6AL03_EVIDENCE_CLASS = "SERVICE_PROVIDER_AUTH_CONTRACT_TYPED_RECEIPT"
L6AL03_READY_STATUS = "AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY"
L6AL03_HELD_STATUS = "AUTH_HELD_SERVICE_PROVIDER_BINDING_INCOMPLETE"
L6AL03_DENIED_STATUS = "DENIED_BEFORE_READ_AUTH_CONTRACT_MISMATCH"

Endpoint = Literal["context", "recall", "health"]

ENDPOINT_AUDIENCES: dict[Endpoint, str] = {
    "context": "memory-seam:read:context",
    "recall": "memory-seam:read:recall",
    "health": "memory-seam:read:health",
}
ENDPOINT_EVIDENCE_CLASSES: dict[Endpoint, str] = {
    "context": "SUPERVISED_METADATA_CONTEXT_READ_RETRY",
    "recall": "SUPERVISED_METADATA_RECALL_READ_RETRY",
    "health": "SUPERVISED_METADATA_HEALTH_AUTH_POSTURE",
}

EXPECTED_ACTING_FOR = "sax"
EXPECTED_IDENTITY_SUBJECT = "atlas-query-supervised-metadata-reader"
EXPECTED_AGENT = "sax"
EXPECTED_SCOPE = "metadata_only:wiki:health:max_one"
EXPECTED_EXPIRY = "fresh_issue_bound_not_expired"

L6AL03_GUARDED_COUNTERS = (
    "source_access_count",
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

L6AL03_REPORT_SAFE_FIELDS = frozenset(
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
        "auth_held",
        "read_authorized",
        "retry_executed",
        "denial_before_read",
        "denial_reason",
        "hold_reason",
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
        "raw_approval_prose",
        "raw_output_requested",
        "source_uri",
        "private_path",
        "platform_raw_id",
        "provider_payload",
        "callback_payload",
        "runtime_registry_payload",
        "allowed_true",
    }
)


@dataclass(frozen=True)
class ServiceAuthContract:
    endpoint: Endpoint
    route_audience: str
    acting_for: str
    identity_subject: str
    agent: str
    scope: str
    evidence_class: str
    expiry: str
    provider_binding_present: bool
    service_binding_present: bool
    metadata_only: bool = True
    report_safe: bool = True
    max_operation_count: int = 1
    authorization_narrowing: str = "exact"

    def as_fixture(self) -> dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "route_audience": self.route_audience,
            "acting_for": self.acting_for,
            "identity_subject": self.identity_subject,
            "agent": self.agent,
            "scope": self.scope,
            "evidence_class": self.evidence_class,
            "expiry": self.expiry,
            "provider_binding_present": self.provider_binding_present,
            "service_binding_present": self.service_binding_present,
            "metadata_only": self.metadata_only,
            "report_safe": self.report_safe,
            "max_operation_count": self.max_operation_count,
            "authorization_narrowing": self.authorization_narrowing,
        }


def build_l6al03_exact_service_auth_contract(endpoint: Endpoint = "recall") -> ServiceAuthContract:
    return ServiceAuthContract(
        endpoint=endpoint,
        route_audience=ENDPOINT_AUDIENCES[endpoint],
        acting_for=EXPECTED_ACTING_FOR,
        identity_subject=EXPECTED_IDENTITY_SUBJECT,
        agent=EXPECTED_AGENT,
        scope=EXPECTED_SCOPE,
        evidence_class=ENDPOINT_EVIDENCE_CLASSES[endpoint],
        expiry=EXPECTED_EXPIRY,
        provider_binding_present=True,
        service_binding_present=True,
    )


def zero_l6al03_guarded_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6AL03_GUARDED_COUNTERS}


def _binding_summary(request: Mapping[str, Any]) -> dict[str, Any]:
    endpoint = request.get("endpoint")
    expected_audience = ENDPOINT_AUDIENCES.get(endpoint) if endpoint in ENDPOINT_AUDIENCES else None
    expected_evidence = (
        ENDPOINT_EVIDENCE_CLASSES.get(endpoint) if endpoint in ENDPOINT_EVIDENCE_CLASSES else None
    )
    return {
        "endpoint": endpoint,
        "known_endpoint": endpoint in ENDPOINT_AUDIENCES,
        "route_audience_matched": request.get("route_audience") == expected_audience,
        "acting_for_matched": request.get("acting_for") == EXPECTED_ACTING_FOR,
        "identity_subject_present": bool(request.get("identity_subject")),
        "identity_subject_matched": request.get("identity_subject") == EXPECTED_IDENTITY_SUBJECT,
        "agent_matched": request.get("agent") == EXPECTED_AGENT,
        "scope_matched": request.get("scope") == EXPECTED_SCOPE,
        "evidence_class_matched": request.get("evidence_class") == expected_evidence,
        "expiry_fresh": request.get("expiry") == EXPECTED_EXPIRY,
        "provider_binding_present": request.get("provider_binding_present") is True,
        "service_binding_present": request.get("service_binding_present") is True,
        "metadata_only": request.get("metadata_only") is True,
        "report_safe": request.get("report_safe") is True,
        "max_operation_count": request.get("max_operation_count"),
        "authorization_narrowing": request.get("authorization_narrowing"),
    }


def _base_receipt(request: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": L6AL03_SCHEMA_VERSION,
        "repo": L6AL03_REPOSITORY,
        "parent_issue": L6AL03_PARENT_ISSUE,
        "rail_issue": L6AL03_RAIL_ISSUE,
        "rail_starting_source_floor": L6AL03_RAIL_STARTING_SOURCE_FLOOR,
        "operation_class": L6AL03_OPERATION_CLASS,
        "evidence_class": L6AL03_EVIDENCE_CLASS,
        "read_authorized": False,
        "retry_executed": False,
        "denial_before_read": True,
        "items": [],
        "guarded_counters": zero_l6al03_guarded_counters(),
        "binding_summary": _binding_summary(request),
        "artifact_paths": [
            "src/memory_seam/l6al_service_auth_contract.py",
            "docs/l6al03-minimal-service-auth-contract.md",
            "tests/test_l6al03_service_auth_contract.py",
        ],
    }


def _denied(request: Mapping[str, Any], reason: str) -> dict[str, Any]:
    receipt = _base_receipt(request)
    receipt.update(
        {
            "status": L6AL03_DENIED_STATUS,
            "auth_ready": False,
            "auth_held": False,
            "denial_reason": reason,
            "hold_reason": None,
        }
    )
    return receipt


def _held(request: Mapping[str, Any], reason: str) -> dict[str, Any]:
    receipt = _base_receipt(request)
    receipt.update(
        {
            "status": L6AL03_HELD_STATUS,
            "auth_ready": False,
            "auth_held": True,
            "denial_reason": None,
            "hold_reason": reason,
        }
    )
    return receipt


def evaluate_l6al03_service_auth_contract(request: Mapping[str, Any] | ServiceAuthContract | None) -> dict[str, Any]:
    """Evaluate a non-secret service/provider auth contract without side effects.

    This helper never loads env vars, keychain entries, OAuth material, auth files,
    credentials, Runtime Registry entries, provider payloads, callbacks, source refs,
    source items, or raw content. A ready receipt is readiness metadata only: it keeps
    read authorization false and does not execute any retry.
    """

    if request is None:
        return _denied({}, "missing_identity_subject")
    if isinstance(request, ServiceAuthContract):
        request = request.as_fixture()

    unsafe = UNSAFE_REQUEST_KEYS.intersection(request.keys())
    if unsafe:
        if "allowed_true" in unsafe:
            return _denied(request, "broad_allowed_true_denied")
        return _denied(request, "raw_output_denied")

    endpoint = request.get("endpoint")
    if endpoint not in ENDPOINT_AUDIENCES:
        return _denied(request, "unknown_endpoint")
    if not request.get("identity_subject"):
        return _denied(request, "missing_identity_subject")
    if request.get("identity_subject") != EXPECTED_IDENTITY_SUBJECT:
        return _denied(request, "mismatched_identity_subject")
    if request.get("acting_for") != EXPECTED_ACTING_FOR or request.get("agent") != EXPECTED_AGENT:
        return _denied(request, "mismatched_agent")
    if request.get("route_audience") != ENDPOINT_AUDIENCES[endpoint]:
        return _denied(request, "wrong_route_audience")
    if request.get("authorization_narrowing") != "exact":
        return _denied(request, "unauthorized_narrowing")
    if request.get("scope") != EXPECTED_SCOPE or request.get("max_operation_count") != 1:
        return _denied(request, "broadened_scope_denied")
    if request.get("metadata_only") is not True or request.get("report_safe") is not True:
        return _denied(request, "raw_output_denied")
    if request.get("expiry") != EXPECTED_EXPIRY:
        return _denied(request, "stale_approval")
    if request.get("evidence_class") != ENDPOINT_EVIDENCE_CLASSES[endpoint]:
        return _denied(request, "mismatched_evidence_class")
    if request.get("provider_binding_present") is not True:
        return _held(request, "provider_binding_missing")
    if request.get("service_binding_present") is not True:
        return _held(request, "service_binding_missing")

    receipt = _base_receipt(request)
    receipt.update(
        {
            "status": L6AL03_READY_STATUS,
            "auth_ready": True,
            "auth_held": False,
            "denial_reason": None,
            "hold_reason": None,
        }
    )
    return receipt


def assert_l6al03_report_safe_receipt(receipt: Mapping[str, Any]) -> None:
    extra_fields = set(receipt) - L6AL03_REPORT_SAFE_FIELDS
    if extra_fields:
        raise AssertionError(f"unexpected unsafe receipt fields: {sorted(extra_fields)}")
    if receipt.get("read_authorized") is not False or receipt.get("retry_executed") is not False:
        raise AssertionError("#351 receipts must not authorize or execute reads")
    if receipt.get("items") != []:
        raise AssertionError("#351 receipts must not return source items")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero")
