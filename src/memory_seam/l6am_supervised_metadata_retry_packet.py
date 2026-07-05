from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal

from memory_seam.l6al_service_auth_contract import (
    ENDPOINT_AUDIENCES,
    L6AL03_READY_STATUS,
    build_l6al03_exact_service_auth_contract,
    evaluate_l6al03_service_auth_contract,
    zero_l6al03_guarded_counters,
)

L6AM01_SCHEMA_VERSION = "l6am01-supervised-metadata-retry-packet-v1"
L6AM01_REPOSITORY = "jeremyknows/memory-seam"
L6AM01_PARENT_ISSUE = 6
L6AM01_RAIL_ISSUE = 357
L6AM01_RAIL_STARTING_SOURCE_FLOOR = "9ea7cd0ab724292b8a2841c9e2c080f14a524ee2"
L6AM01_OPERATION_CLASS = "L6AM_EXACT_SUPERVISED_METADATA_RETRY_PACKET"
L6AM01_EVIDENCE_CLASS = "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
L6AM01_QUERY_LABEL = "supervised_metadata_readiness"
L6AM01_QUERY_TEXT = (
    "Memory Seam supervised metadata read retry source-floor readiness held "
    "surfaces denial-before-read"
)
L6AM01_ENDPOINT: Literal["recall"] = "recall"
L6AM01_AGENT = "sax"
L6AM01_SCOPE = "wiki"
L6AM01_N = 3
L6AM01_STATUS = "PASS_EXACT_SUPERVISED_METADATA_RETRY_PACKET_READY"
L6AM01_DENIED_STATUS = "DENIED_BEFORE_READ_OUT_OF_SCOPE_MISMATCH"

L6AM01_REPORT_SAFE_OUTPUT_FIELDS = frozenset(
    {
        "schema_version",
        "repo",
        "parent_issue",
        "rail_issue",
        "rail_starting_source_floor",
        "operation_class",
        "evidence_class",
        "status",
        "endpoint",
        "auth_status",
        "degraded",
        "degraded_reasons",
        "item_count",
        "safe_item_labels",
        "denial_reason",
        "guarded_counters",
    }
)

L6AM01_FORBIDDEN_OUTPUT_FIELDS = frozenset(
    {
        "text",
        "content",
        "raw_text",
        "raw_content",
        "raw_item_text",
        "raw_source_text",
        "source_uri",
        "private_path",
        "platform_raw_id",
        "credential_value",
        "auth_value",
        "token",
        "provider_payload",
        "callback_payload",
        "runtime_registry_payload",
    }
)

L6AM01_STOP_CONDITIONS = (
    "auth_status_code_403",
    "empty_items",
    "wrong_route_audience",
    "unauthorized_narrowing",
    "raw_output_request",
    "source_discovery_request",
    "broad_recall_or_index_query",
    "runtime_registry_request",
    "service_activation_request",
    "provider_callback_or_route_request",
    "provider_prod_canary_or_gate_movement_request",
    "write_mutation_or_persistence_request",
    "broad_allowed_true_request",
)

L6AM01_DENIAL_CASES = (
    "wrong_route_audience",
    "unauthorized_narrowing",
)


@dataclass(frozen=True)
class SupervisedMetadataRetryPacket:
    endpoint: Literal["recall"]
    agent: str
    scope: str
    n: int
    query_label: str
    query_text: str
    evidence_class: str
    max_operation_count: int
    report_safe: bool
    metadata_only: bool
    denial_before_read_required: bool
    denied_mismatch_case: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "agent": self.agent,
            "scope": self.scope,
            "n": self.n,
            "query_label": self.query_label,
            "query_text": self.query_text,
            "evidence_class": self.evidence_class,
            "max_operation_count": self.max_operation_count,
            "report_safe": self.report_safe,
            "metadata_only": self.metadata_only,
            "denial_before_read_required": self.denial_before_read_required,
            "denied_mismatch_case": self.denied_mismatch_case,
        }


def build_l6am01_exact_retry_packet() -> SupervisedMetadataRetryPacket:
    return SupervisedMetadataRetryPacket(
        endpoint=L6AM01_ENDPOINT,
        agent=L6AM01_AGENT,
        scope=L6AM01_SCOPE,
        n=L6AM01_N,
        query_label=L6AM01_QUERY_LABEL,
        query_text=L6AM01_QUERY_TEXT,
        evidence_class=L6AM01_EVIDENCE_CLASS,
        max_operation_count=1,
        report_safe=True,
        metadata_only=True,
        denial_before_read_required=True,
        denied_mismatch_case="wrong_route_audience",
    )


def build_l6am01_service_auth_binding_receipt() -> dict[str, Any]:
    """Return non-secret readiness metadata for the exact recall retry packet."""

    contract_receipt = evaluate_l6al03_service_auth_contract(
        build_l6al03_exact_service_auth_contract(endpoint=L6AM01_ENDPOINT)
    )
    return {
        "schema_version": L6AM01_SCHEMA_VERSION,
        "repo": L6AM01_REPOSITORY,
        "parent_issue": L6AM01_PARENT_ISSUE,
        "rail_issue": L6AM01_RAIL_ISSUE,
        "rail_starting_source_floor": L6AM01_RAIL_STARTING_SOURCE_FLOOR,
        "operation_class": L6AM01_OPERATION_CLASS,
        "evidence_class": L6AM01_EVIDENCE_CLASS,
        "status": L6AM01_STATUS,
        "endpoint": L6AM01_ENDPOINT,
        "auth_contract_status": contract_receipt["status"],
        "auth_ready_for_one_attempt": contract_receipt["status"] == L6AL03_READY_STATUS,
        "retry_executed": False,
        "packet": build_l6am01_exact_retry_packet().as_dict(),
        "required_tool_call": {
            "tool": "memory_seam_recall",
            "agent": L6AM01_AGENT,
            "scope": L6AM01_SCOPE,
            "n": L6AM01_N,
            "query": L6AM01_QUERY_TEXT,
        },
        "required_denial_cases": list(L6AM01_DENIAL_CASES),
        "report_safe_output_fields": sorted(L6AM01_REPORT_SAFE_OUTPUT_FIELDS),
        "stop_conditions": list(L6AM01_STOP_CONDITIONS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def build_l6am01_denied_mismatch_receipt(reason: str = "wrong_route_audience") -> dict[str, Any]:
    """Return a denied-before-read mismatch receipt without source/provider access."""

    contract = build_l6al03_exact_service_auth_contract(endpoint=L6AM01_ENDPOINT).as_fixture()
    if reason == "wrong_route_audience":
        contract["route_audience"] = ENDPOINT_AUDIENCES["context"]
    elif reason == "unauthorized_narrowing":
        contract["authorization_narrowing"] = "context_only_without_recall"
    else:
        raise ValueError(f"unsupported L6AM.01 denial case: {reason}")

    contract_receipt = evaluate_l6al03_service_auth_contract(contract)
    return {
        "schema_version": L6AM01_SCHEMA_VERSION,
        "repo": L6AM01_REPOSITORY,
        "parent_issue": L6AM01_PARENT_ISSUE,
        "rail_issue": L6AM01_RAIL_ISSUE,
        "rail_starting_source_floor": L6AM01_RAIL_STARTING_SOURCE_FLOOR,
        "operation_class": L6AM01_OPERATION_CLASS,
        "evidence_class": L6AM01_EVIDENCE_CLASS,
        "status": L6AM01_DENIED_STATUS,
        "endpoint": L6AM01_ENDPOINT,
        "auth_status": "denied_before_read",
        "denial_reason": contract_receipt["denial_reason"],
        "retry_executed": False,
        "items": [],
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6am01_retry_packet_report_safe(receipt: Mapping[str, Any]) -> None:
    forbidden = L6AM01_FORBIDDEN_OUTPUT_FIELDS.intersection(receipt.keys())
    if forbidden:
        raise AssertionError(f"unsafe report fields present: {sorted(forbidden)}")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("guarded counters must remain zero before the exact retry")
    if receipt.get("retry_executed") is not False:
        raise AssertionError("L6AM.01 creates the packet only; it must not execute the retry")
