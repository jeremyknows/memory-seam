from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from memory_seam.l6aa_value_proof import (
    L6AA_DESCRIPTOR_REF,
    L6AA_SOURCE_CARD_REF,
    execute_l6aa02_value_proof,
    verify_l6aa03_receipt_reportable_hygiene,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aa03-value-proof-receipt-hygiene-verifier.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVALUATED_AT = "2026-06-08T15:35:55Z"

APPROVAL_CONTEXT = {
    "approval_comment_id": "4650520977",
    "approval_comment_author": "jeremyknows",
    "owner_actor_association": "OWNER",
    "approval_comment_created_at": "2026-06-08T15:22:54Z",
    "packet_issue_id": "#241",
    "read_issue_id": "#242",
    "parent_issue_id": "#6",
    "subject": "jeremyknows/memory-seam",
    "audience": "L6AA owner-approved target-ref live-read value proof",
    "scope": "one report-safe source-card read",
    "operation_class": "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ",
    "max_operation_count": 1,
    "descriptor_ref": L6AA_DESCRIPTOR_REF,
    "source_card_ref": L6AA_SOURCE_CARD_REF,
    "source_floor_requirement": "b141f7be878a5b0d136cced3beb12ef38f0a25c9 or later",
    "preauth_anchor_refs_present": True,
    "report_safe_output_only": True,
    "deny_before_read_on_mismatch": True,
}

SAFE_SOURCE_CARD_METADATA = {
    "card_id": "l6aa-report-safe-operator-preference-card",
    "source_tier": "operator-preference-card",
    "private_class": "report-safe-redacted",
    "canonicality": "current-preference-signal",
    "retrieval_backend": "supervised-one-read-source-card",
    "title": "Operator preference card metadata",
    "safe_summary": "Report-safe metadata confirms a bounded operator-preference card was available for usefulness proof; raw source content is omitted.",
    "reportable": True,
    "redaction_applied": True,
    "redaction_labels": ["raw-source-content-omitted", "credential-material-not-read"],
}

UNSAFE_RECEIPT_VARIANTS = (
    ("raw_private_source_text", "raw private source text: example", "unsafe_receipt_key_present"),
    ("private_absolute_path", "private absolute path: /private/example/source-card.md", "unsafe_receipt_key_present"),
    ("source_uri", "source://private/example", "unsafe_receipt_key_present"),
    ("platform_id", "platform-raw-id-123", "unsafe_receipt_key_present"),
    ("prompt_payload", "raw prompt", "unsafe_receipt_key_present"),
    ("query_payload", "raw query", "unsafe_receipt_key_present"),
    ("backend_response", "raw backend response", "unsafe_receipt_key_present"),
    ("credential_value", "credential value: example", "unsafe_receipt_key_present"),
    ("oauth_token", "oauth token: example", "unsafe_receipt_key_present"),
    ("approval_text", "I approve exactly one supervised source-card read", "unsafe_receipt_key_present"),
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def pass_receipt() -> dict[str, object]:
    return execute_l6aa02_value_proof(
        APPROVAL_CONTEXT,
        evaluated_at=EVALUATED_AT,
        read_report_safe_source_card=lambda descriptor_ref, source_card_ref: dict(
            SAFE_SOURCE_CARD_METADATA
        ),
    )


def test_l6aa03_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aa03-value-proof-receipt-hygiene-verifier.md" in docs_index
    assert "tests/test_l6aa03_value_proof_receipt_hygiene_verifier.py" in inventory
    assert "L6AA.03 value-proof receipt hygiene verifier" in inventory
    assert "RECEIPT_REPORTABLE_HYGIENE_VERIFIER_NO_ADDITIONAL_READS" in inventory


def test_l6aa03_doc_records_verifier_only_boundary_and_source_floor():
    text = normalized(DOC)

    required_terms = (
        "Status: `RECEIPT_REPORTABLE_HYGIENE_VERIFIER_NO_ADDITIONAL_READS`",
        "Rail issue: #243",
        "Verified receipt issue: #242 closed/PASS",
        "Prerequisite packet issue: #241 closed/PASS",
        "Parent issue: #6",
        "Source floor verified before work: `4a01bf9b2ff8feec9c56b038bab5c7dbf2991241`",
        "PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ",
        "descriptor:l6aa/report-safe-operator-preference-card",
        "source-card:l6aa/report-safe-operator-preference-card",
        "no additional live/private reads",
        "broad `allowed=true` variants are rejected",
    )
    for term in required_terms:
        assert term in text


def test_l6aa03_accepts_exact_l6aa02_pass_receipt_without_additional_read():
    receipt = pass_receipt()
    verifier = verify_l6aa03_receipt_reportable_hygiene(receipt)

    assert verifier["accepted"] is True
    assert verifier["errors"] == []
    assert verifier["verifier_status"] == "RECEIPT_REPORTABLE_HYGIENE_VERIFIER_NO_ADDITIONAL_READS"
    assert verifier["receipt_status_examined"] == "PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ"
    assert verifier["additional_live_read_invoked"] is False
    assert verifier["callbacks_invoked"] is False
    assert verifier["metadata_only"] is True
    assert verifier["report_safe"] is True
    assert verifier["broad_allowed_true_accepted"] is False


def test_l6aa03_rejects_raw_private_and_unsafe_receipt_echoes():
    for key, value, expected_error in UNSAFE_RECEIPT_VARIANTS:
        receipt = pass_receipt()
        receipt[key] = value

        verifier = verify_l6aa03_receipt_reportable_hygiene(receipt)

        assert verifier["accepted"] is False
        assert expected_error in verifier["errors"]
        assert "unsafe_receipt_field_present" in verifier["errors"]
        assert "unsafe_echo_marker_present" in verifier["errors"]


def test_l6aa03_rejects_broad_allowed_true_and_nonzero_forbidden_counters():
    broad_allowed = pass_receipt()
    broad_allowed["allowed"] = True
    verifier = verify_l6aa03_receipt_reportable_hygiene(broad_allowed)
    assert verifier["accepted"] is False
    assert "allowed_broadened_or_missing" in verifier["errors"]
    assert "l6aa03_pass_allowed_scope_not_exact" in verifier["errors"]

    forbidden_counter = pass_receipt()
    guarded_counters = cast(dict[str, Any], forbidden_counter["guarded_counters"])
    forbidden_counter["guarded_counters"] = dict(guarded_counters)
    cast(dict[str, Any], forbidden_counter["guarded_counters"])["provider_callbacks"] = 1
    verifier = verify_l6aa03_receipt_reportable_hygiene(forbidden_counter)
    assert verifier["accepted"] is False
    assert "unexpected_counter_provider_callbacks" in verifier["errors"]
    assert "l6aa03_pass_forbidden_nonzero_counter_provider_callbacks" in verifier["errors"]


def test_l6aa03_rejects_unapproved_hold_with_live_or_allowed_counts():
    receipt = pass_receipt()
    receipt["receipt_status"] = "HOLD_DENIED_BEFORE_READ"
    receipt["approval_result"] = "DENY_BEFORE_READ"
    receipt["allowed"] = False
    receipt["live_read_invoked"] = False
    receipt["operation_count_attempted"] = 1
    receipt["allowed_result_count"] = 1

    verifier = verify_l6aa03_receipt_reportable_hygiene(receipt)

    assert verifier["accepted"] is False
    assert "l6aa03_hold_operation_count_not_zero" in verifier["errors"]
    assert "l6aa03_hold_allowed_result_count_not_zero" in verifier["errors"]
    assert "l6aa03_unapproved_nonzero_counter_live_read_invocations" in verifier["errors"]
