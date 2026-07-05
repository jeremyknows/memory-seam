from __future__ import annotations

from pathlib import Path

import pytest

from memory_seam.l6x_one_read_receipt import (
    L6X_ONE_READ_GUARDED_COUNTERS,
    L6X_ONE_READ_OPERATION_CLASS,
    build_l6x02_absent_approval_hold_receipt,
    validate_l6x_one_read_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6x03-one-read-receipt-verifier.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

UNSAFE_ATTEMPTS = (
    ("descriptor_ref", "raw private source text"),
    ("descriptor_ref", "private path"),
    ("source_card_ref", "source://unsafe"),
    ("source_card_ref", "platform-raw-id"),
    ("stop_status", "raw prompt"),
    ("stop_status", "raw query"),
    ("rollback_status", "raw backend response"),
    ("rollback_status", "credential"),
    ("rollback_status", "auth material"),
    ("descriptor_ref", "private-correlation-ref"),
    ("source_card_ref", "raw approval text"),
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6x03_verifier_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6x03-one-read-receipt-verifier.md" in docs_index
    assert "tests/test_l6x03_one_read_receipt_verifier.py" in inventory
    assert "L6X.03 report-safe one-read receipt verifier" in inventory
    assert "RECEIPT_VERIFIER_NO_ADDITIONAL_READS" in inventory


def test_l6x03_accepts_l6x02_absent_approval_hold_receipt():
    receipt = build_l6x02_absent_approval_hold_receipt()

    assert validate_l6x_one_read_receipt(receipt) == []
    assert receipt["operation_class"] == L6X_ONE_READ_OPERATION_CLASS
    assert receipt["receipt_status"] == "HOLD"
    assert receipt["approval_result"] == "DENIED_BEFORE_CALLBACK"
    assert receipt["live_read_invoked"] is False
    assert receipt["operation_count_attempted"] == 0
    assert receipt["allowed"] is False
    assert receipt["allowed_result_count"] == 0
    assert all(receipt["guarded_counters"][counter] == 0 for counter in L6X_ONE_READ_GUARDED_COUNTERS)


@pytest.mark.parametrize(("field", "unsafe_value"), UNSAFE_ATTEMPTS)
def test_l6x03_rejects_unsafe_echo_markers(field: str, unsafe_value: str):
    receipt = build_l6x02_absent_approval_hold_receipt()
    receipt[field] = unsafe_value

    errors = validate_l6x_one_read_receipt(receipt)

    assert "unsafe_echo_marker_present" in errors


def test_l6x03_rejects_unknown_fields_and_nonzero_guarded_counters():
    receipt = build_l6x02_absent_approval_hold_receipt()
    receipt["raw_payload"] = "metadata-looking but unapproved"
    receipt["guarded_counters"]["source_read_callbacks"] = 1

    errors = validate_l6x_one_read_receipt(receipt)

    assert "unsafe_receipt_field_present" in errors
    assert "nonzero_counter_source_read_callbacks" in errors


def test_l6x03_doc_preserves_hold_posture_and_hygiene_scope():
    text = normalized(DOC)

    required_terms = (
        "Status: `RECEIPT_VERIFIER_NO_ADDITIONAL_READS`",
        "Rail issue: #213",
        "Depends on: L6X.02 HOLD proof",
        "verifies an already supplied receipt mapping only",
        "does not perform source discovery, live/private reads, callbacks, credential/auth reads, Runtime Registry consumption, persistence, activation, mutation, rollback, cache purge, publication, provider/prod/canary authority, repository visibility changes, Atlas Gate movement, or `allowed=true` routing",
        "raw source text",
        "private paths",
        "source URIs",
        "platform IDs",
        "prompts/queries",
        "backend responses",
        "credentials/auth material",
        "private correlation refs",
        "raw approval text",
    )
    for term in required_terms:
        assert term in text
