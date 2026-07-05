from __future__ import annotations

from pathlib import Path

import pytest

from memory_seam.l6z_one_read_receipt import (
    L6Z_ONE_READ_GUARDED_COUNTERS,
    L6Z_ONE_READ_HOLD_STATUS,
    build_l6z02_target_ref_mismatch_hold_receipt,
    validate_l6z_one_read_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6z03-one-read-retry-receipt-redaction-verifier.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

UNSAFE_PAYLOADS = (
    {"raw_private_source_text": "raw private source text: example"},
    {"private_absolute_path": "private absolute path: /private/example/source-card.md"},
    {"source_uri": "source://private/example"},
    {"platform_id": "platform-raw-id-123"},
    {"prompt_payload": "raw prompt"},
    {"query_payload": "raw query"},
    {"backend_response": "raw backend response"},
    {"credential_value": "credential value: example"},
    {"oauth_token": "oauth token: example"},
    {"approval_text": "I approve exactly one supervised source-card read"},
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6z03_verifier_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6z03-one-read-retry-receipt-redaction-verifier.md" in docs_index
    assert "tests/test_l6z03_one_read_retry_receipt_redaction_verifier.py" in inventory
    assert "L6Z.03 one-read retry receipt and redaction verifier" in inventory
    assert "RECEIPT_REDACTION_VERIFIER_NO_ADDITIONAL_READS" in inventory


def test_l6z03_doc_records_source_floor_and_no_additional_read_boundary():
    text = normalized(DOC)

    required_terms = (
        "Status: `RECEIPT_REDACTION_VERIFIER_NO_ADDITIONAL_READS`",
        "Rail issue: #233",
        "Verified receipt issue: #232",
        "Prerequisite packet issue: #231",
        "Parent issue: #6",
        "Source floor verified before work: `a71f9f78afd5e0d254719acaf70cad8219ad23e6`",
        "#6 comment `4649391691`",
        "#215 comment `4649391836`",
        "issuecomment-4650001541",
        "performs no live/private read",
        "This verifier does not authorize another read",
    )
    for term in required_terms:
        assert term in text


def test_l6z03_accepts_exact_l6z02_hold_receipt_shape():
    receipt = build_l6z02_target_ref_mismatch_hold_receipt()

    assert validate_l6z_one_read_receipt(receipt) == []
    assert receipt["receipt_status"] == L6Z_ONE_READ_HOLD_STATUS
    assert receipt["approval_result"] == "DENY_BEFORE_READ"
    assert receipt["descriptor_ref_expected"] == "descriptor:l6z/report-safe-operator-preference-card"
    assert receipt["source_card_ref_expected"] == "source-card:l6z/report-safe-operator-preference-card"
    assert receipt["descriptor_ref_presented"] == "descriptor:l6z/operator-proof"
    assert receipt["source_card_ref_presented"] == "source-card:l6z/operator-proof"
    assert receipt["live_read_invoked"] is False
    assert receipt["allowed"] is False
    assert receipt["operation_count_attempted"] == 0
    assert receipt["allowed_result_count"] == 0
    assert receipt["redaction_status"] == "REPORT_SAFE_METADATA_ONLY_RAW_APPROVAL_TEXT_OMITTED"


def test_l6z03_rejects_nonzero_guarded_counters_outside_denial_shape():
    for counter in L6Z_ONE_READ_GUARDED_COUNTERS:
        if counter == "approval_comments_examined":
            continue
        receipt = build_l6z02_target_ref_mismatch_hold_receipt()
        receipt["guarded_counters"][counter] = 1

        assert f"unexpected_counter_{counter}" in validate_l6z_one_read_receipt(receipt)

    receipt = build_l6z02_target_ref_mismatch_hold_receipt()
    receipt["guarded_counters"]["approval_comments_examined"] = 2
    assert "unexpected_counter_approval_comments_examined" in validate_l6z_one_read_receipt(receipt)


def test_l6z03_rejects_allowed_true_operation_attempt_or_live_read():
    mutations = (
        ("allowed", True, "allowed_not_false_for_hold"),
        ("live_read_invoked", True, "live_read_invoked_not_false_for_hold"),
        ("operation_count_attempted", 1, "operation_count_attempted_not_zero"),
        ("allowed_result_count", 1, "allowed_result_count_not_zero"),
    )
    for field, value, expected_error in mutations:
        receipt = build_l6z02_target_ref_mismatch_hold_receipt()
        receipt[field] = value

        assert expected_error in validate_l6z_one_read_receipt(receipt)


def test_l6z03_rejects_raw_private_approval_and_unsafe_field_echoes():
    for unsafe_payload in UNSAFE_PAYLOADS:
        receipt = build_l6z02_target_ref_mismatch_hold_receipt() | unsafe_payload
        errors = validate_l6z_one_read_receipt(receipt)

        assert "unsafe_receipt_field_present" in errors
        assert "unsafe_receipt_key_present" in errors
        assert "unsafe_echo_marker_present" in errors


def test_l6z03_rejects_unknown_unsafe_counter_names():
    receipt = build_l6z02_target_ref_mismatch_hold_receipt()
    receipt["guarded_counters"]["raw_private_source_reads"] = 0

    errors = validate_l6z_one_read_receipt(receipt)

    assert "unsafe_guarded_counter_present" in errors
    assert "unsafe_guarded_counter_key_present" in errors


@pytest.mark.parametrize(
    "field,value,expected_error",
    (
        ("receipt_status", "PASS_EXECUTION", "unexpected_receipt_status"),
        ("approval_result", "APPROVED", "unexpected_approval_result"),
        ("descriptor_ref_expected", "descriptor:l6z/operator-proof", "unexpected_descriptor_ref_expected"),
        ("source_card_ref_expected", "source-card:l6z/operator-proof", "unexpected_source_card_ref_expected"),
        ("mismatch_reason", "NONE", "unexpected_mismatch_reason"),
    ),
)
def test_l6z03_rejects_mismatched_or_broadened_receipt_values(field: str, value: object, expected_error: str):
    receipt = build_l6z02_target_ref_mismatch_hold_receipt()
    receipt[field] = value

    assert expected_error in validate_l6z_one_read_receipt(receipt)
