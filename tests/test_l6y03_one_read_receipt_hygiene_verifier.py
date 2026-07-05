from __future__ import annotations

from pathlib import Path

import pytest

from memory_seam.l6y_one_read_receipt import (
    L6Y_ONE_READ_GUARDED_COUNTERS,
    L6Y_ONE_READ_HOLD_STATUS,
    L6Y_ONE_READ_OPERATION_CLASS,
    build_l6y02_approval_mismatch_hold_receipt,
    validate_l6y_one_read_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6y03-one-read-receipt-hygiene-verifier.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

UNSAFE_VALUE_ATTEMPTS = (
    ("descriptor_ref", "raw private source text"),
    ("descriptor_ref", "private path"),
    ("source_card_ref", "source://unsafe"),
    ("source_card_ref", "platform-raw-id"),
    ("read_usefulness_label", "raw prompt"),
    ("read_usefulness_label", "raw query"),
    ("redaction_status", "query payload"),
    ("redaction_status", "raw payload"),
    ("rollback_status", "raw backend response"),
    ("rollback_status", "credential"),
    ("rollback_status", "auth material"),
    ("rollback_status", "OAuth material"),
    ("rollback_status", "keychain material"),
    ("rollback_status", "auth-file material"),
    ("descriptor_ref", "private-correlation-ref"),
    ("source_card_ref", "raw approval text"),
)

UNSAFE_UNKNOWN_FIELDS = (
    "raw_private_content",
    "private_absolute_path",
    "source_uri",
    "platform_id",
    "prompt_payload",
    "query_payload",
    "backend_response",
    "credential_material",
    "auth_material",
    "oauth_token",
    "keychain_secret",
    "env_secret",
    "private_correlation_ref",
    "source_text",
    "approval_text",
)

BROADENING_ATTEMPTS = (
    ("allowed", True, "allowed_not_false"),
    ("allowed_result_count", 1, "allowed_result_count_not_zero"),
    ("live_read_invoked", True, "live_read_invoked_not_false_for_hold"),
    ("operation_count_attempted", 1, "operation_count_not_zero_for_hold"),
    ("receipt_status", "PASS_EXECUTION", "unexpected_receipt_status"),
    ("approval_result", "APPROVED", "unexpected_approval_result"),
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6y03_verifier_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6y03-one-read-receipt-hygiene-verifier.md" in docs_index
    assert "tests/test_l6y03_one_read_receipt_hygiene_verifier.py" in inventory
    assert "L6Y.03 report-safe one-read receipt hygiene verifier" in inventory
    assert "RECEIPT_HYGIENE_VERIFIER_NO_ADDITIONAL_READS" in inventory


def test_l6y03_accepts_l6y02_approval_mismatch_hold_receipt():
    receipt = build_l6y02_approval_mismatch_hold_receipt()

    assert validate_l6y_one_read_receipt(receipt) == []
    assert receipt["receipt_status"] == L6Y_ONE_READ_HOLD_STATUS
    assert receipt["operation_class"] == L6Y_ONE_READ_OPERATION_CLASS
    assert receipt["approval_result"] == "DENIED_BEFORE_CALLBACK"
    assert receipt["live_read_invoked"] is False
    assert receipt["operation_count_attempted"] == 0
    assert receipt["allowed"] is False
    assert receipt["allowed_result_count"] == 0
    assert receipt["descriptor_ref"] == "MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ"
    assert receipt["source_card_ref"] == "MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ"
    assert receipt["redaction_status"] == "REPORT_SAFE_METADATA_ONLY"
    assert receipt["guarded_counters"]["approval_comments_examined"] == 1
    assert receipt["guarded_counters"]["valid_owner_approval_comments"] == 0
    guarded_zero = [
        counter
        for counter in L6Y_ONE_READ_GUARDED_COUNTERS
        if counter != "approval_comments_examined"
    ]
    assert all(receipt["guarded_counters"][counter] == 0 for counter in guarded_zero)


@pytest.mark.parametrize(("field", "unsafe_value"), UNSAFE_VALUE_ATTEMPTS)
def test_l6y03_rejects_raw_private_and_unsafe_echo_markers(field: str, unsafe_value: str):
    receipt = build_l6y02_approval_mismatch_hold_receipt()
    receipt[field] = unsafe_value

    errors = validate_l6y_one_read_receipt(receipt)

    assert "unsafe_echo_marker_present" in errors


@pytest.mark.parametrize("unsafe_field", UNSAFE_UNKNOWN_FIELDS)
def test_l6y03_rejects_unknown_unsafe_key_names(unsafe_field: str):
    receipt = build_l6y02_approval_mismatch_hold_receipt()
    receipt[unsafe_field] = "metadata-looking but unapproved"

    errors = validate_l6y_one_read_receipt(receipt)

    assert "unsafe_receipt_field_present" in errors
    assert "unsafe_receipt_key_present" in errors


def test_l6y03_rejects_unknown_safe_looking_fields_and_extra_guarded_counters():
    receipt = build_l6y02_approval_mismatch_hold_receipt()
    receipt["review_note"] = "metadata-looking but unapproved"
    receipt["guarded_counters"]["review_counter"] = 0

    errors = validate_l6y_one_read_receipt(receipt)

    assert "unsafe_receipt_field_present" in errors
    assert "unsafe_guarded_counter_present" in errors


def test_l6y03_rejects_nonzero_guarded_counters_outside_approved_hold_shape():
    for counter in L6Y_ONE_READ_GUARDED_COUNTERS:
        receipt = build_l6y02_approval_mismatch_hold_receipt()
        receipt["guarded_counters"][counter] = 2 if counter == "approval_comments_examined" else 1

        errors = validate_l6y_one_read_receipt(receipt)

        assert f"nonzero_counter_{counter}" in errors or (
            counter == "approval_comments_examined"
            and "unexpected_counter_approval_comments_examined" in errors
        )


@pytest.mark.parametrize(("field", "value", "expected_error"), BROADENING_ATTEMPTS)
def test_l6y03_rejects_allowed_true_and_status_broadening(field: str, value: object, expected_error: str):
    receipt = build_l6y02_approval_mismatch_hold_receipt()
    receipt[field] = value

    errors = validate_l6y_one_read_receipt(receipt)

    assert expected_error in errors


def test_l6y03_doc_preserves_verifier_only_hold_posture_and_hygiene_scope():
    text = normalized(DOC)

    required_terms = (
        "Status: `RECEIPT_HYGIENE_VERIFIER_NO_ADDITIONAL_READS`",
        "Rail issue: #223",
        "Depends on: L6Y.02 HOLD receipt artifact",
        "accepts the already supplied #222 HOLD receipt shape only when it remains metadata-only",
        "does not perform source discovery, workspace scans, family scans, broad recall, index queries, live/private reads",
        "credentials/auth material",
        "private paths/source URIs",
        "raw platform IDs",
        "prompt/query payloads",
        "raw backend responses",
        "raw approval text",
        "unknown unsafe fields",
        "nonzero guarded counters outside the approved #222 shape",
        "`allowed=true`",
        "creates no new approval",
        "#224 may perform the post-read usefulness and redaction review over this verifier evidence without any additional live/private read",
    )
    for term in required_terms:
        assert term in text
