from __future__ import annotations

from pathlib import Path

from memory_seam.l6an_service_operator_auth_binding_packet import (
    L6AN02_DENIED_STATUS,
    L6AN03_RETRY_GATE_DECISION,
    L6AN03_STATUS,
    assert_l6an03_handoff_report_safe,
    build_l6an02_exact_binding_reference_fixture,
    build_l6an03_service_owner_handoff_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6an03-service-owner-handoff-retry-gate.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def assert_zero_counters(receipt: dict[str, object]) -> None:
    counters = receipt["guarded_counters"]
    assert isinstance(counters, dict)
    assert all(value == 0 for value in counters.values())


def test_l6an03_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6an03-service-owner-handoff-retry-gate.md" in docs_index
    assert "tests/test_l6an03_service_owner_handoff.py" in inventory
    assert "L6AN.03 service-owner handoff receipt and retry gate" in inventory
    assert L6AN03_STATUS in inventory


def test_service_owner_handoff_names_exact_future_evidence_without_retry() -> None:
    receipt = build_l6an03_service_owner_handoff_receipt()

    assert receipt["status"] == L6AN03_STATUS
    assert receipt["rail_issue"] == 372
    assert receipt["parent_issue"] == 6
    assert receipt["retry_gate_decision"] == L6AN03_RETRY_GATE_DECISION
    assert receipt["actual_retry_executed"] is False
    assert receipt["current_ready_receipt"]["retry_executed"] is False
    assert receipt["service_owner_request"] == {
        "request_class": "exact_non_secret_service_operator_binding_for_future_l6ao_retry",
        "may_include_secret_material": False,
        "runtime_or_provider_inspection_requested": False,
        "live_retry_requested": False,
        "new_successor_issue_requested": False,
        "must_match": {
            "endpoint": "memory_seam_recall",
            "route_audience": "memory-seam:read:recall",
            "acting_for": "sax",
            "agent": "sax",
            "scope": "wiki",
            "n": 3,
            "query_label": "supervised_metadata_readiness",
            "query_text": "Memory Seam supervised metadata read retry source-floor readiness held surfaces denial-before-read",
            "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
            "max_operation_count": 1,
            "report_safe_metadata_only": True,
            "denial_before_read_required": True,
        },
    }
    for required in (
        "operator_service_binding_ref",
        "identity_subject_bound_to_sax_service_caller",
        "route_audience_memory_seam_read_recall",
        "explicit_new_max_one_retry_issue_authorization",
    ):
        assert required in receipt["required_future_evidence"]
    assert_zero_counters(receipt)
    assert_l6an03_handoff_report_safe(receipt)


def test_retry_gate_remains_held_even_when_candidate_binding_is_ready() -> None:
    receipt = build_l6an03_service_owner_handoff_receipt(build_l6an02_exact_binding_reference_fixture())

    assert receipt["current_ready_receipt"]["status"] == "AUTH_BINDING_READY_RETRY_HELD"
    assert receipt["retry_gate_decision"] == L6AN03_RETRY_GATE_DECISION
    assert receipt["actual_retry_executed"] is False
    assert "live_retry" in receipt["held_surfaces"]
    assert "provider_callback_or_service_activation" in receipt["held_surfaces"]
    assert_l6an03_handoff_report_safe(receipt)


def test_handoff_carries_denied_candidate_as_pre_read_decision_only() -> None:
    bad = build_l6an02_exact_binding_reference_fixture() | {"runtime_registry_requested": True}
    receipt = build_l6an03_service_owner_handoff_receipt(bad)

    assert receipt["current_ready_receipt"]["status"] == L6AN02_DENIED_STATUS
    assert "runtime_registry_requested" in receipt["current_ready_receipt"]["reasons"]
    assert receipt["actual_retry_executed"] is False
    assert_zero_counters(receipt)
    assert_l6an03_handoff_report_safe(receipt)


def test_report_safe_assertion_rejects_execution_secret_or_runtime_expansion() -> None:
    receipt = build_l6an03_service_owner_handoff_receipt()

    unsafe_receipts = (
        receipt | {"actual_retry_executed": True},
        receipt | {"raw_auth_secret": "forbidden"},
        receipt
        | {
            "service_owner_request": receipt["service_owner_request"]
            | {"may_include_secret_material": True}
        },
        receipt
        | {
            "service_owner_request": receipt["service_owner_request"]
            | {"runtime_or_provider_inspection_requested": True}
        },
    )
    for unsafe in unsafe_receipts:
        try:
            assert_l6an03_handoff_report_safe(unsafe)
        except AssertionError:
            pass
        else:  # pragma: no cover - defensive guard
            raise AssertionError("unsafe L6AN.03 handoff should fail closed")


def test_doc_names_handoff_gate_and_verification_commands() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AN.03 service-owner handoff receipt and retry gate",
        f"Status: `{L6AN03_STATUS}`",
        "Rail issue: #372",
        "Parent issue: #6",
        L6AN03_RETRY_GATE_DECISION,
        "exact non-secret service/operator binding proof",
        "explicit new max-one retry issue authorization",
        "does not execute another read",
        "does not activate services/providers/callbacks",
        "does not consume Runtime Registry",
        "python -m pytest -q tests/test_l6an03_service_owner_handoff.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text

    lowered = text.lower()
    for forbidden_marker in (
        "oauth token",
        "credential value",
        "auth-file secret",
        "raw source text",
        "private path value",
    ):
        assert forbidden_marker not in lowered
