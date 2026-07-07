from __future__ import annotations

from pathlib import Path

from memory_seam.l6ac_one_read_receipt import (
    L6AC_APPROVAL_COMMENT_ID,
    L6AC_DESCRIPTOR_REF,
    L6AC_HOLD_STATUS,
    L6AC_PASS_STATUS,
    L6AC_SOURCE_CARD_REF,
    approval_matches_l6ac_packet,
    build_l6ac02_approval_metadata,
    execute_l6ac02_one_read,
    validate_l6ac02_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ac02-owner-approved-one-read-receipt.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVALUATED_AT = "2026-06-08T17:26:20Z"
SOURCE_FLOOR = "ca81a18fbba9603f5f35a8fa57410963e028c904"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def report_safe_card(descriptor_ref: str, source_card_ref: str) -> dict[str, object]:
    assert descriptor_ref == L6AC_DESCRIPTOR_REF
    assert source_card_ref == L6AC_SOURCE_CARD_REF
    return {
        "card_id": "l6ac-report-safe-operator-preference-card",
        "source_tier": "owner-approved-source-card",
        "private_class": "metadata-only-report-safe",
        "canonicality": "exact-issue-bound-target-ref",
        "retrieval_backend": "supervised-report-safe-source-card-callback",
        "title": "Operator preference card metadata",
        "safe_summary": "Report-safe metadata confirms the target card is present and redacted.",
        "reportable": True,
        "redaction_applied": True,
        "redaction_labels": ["no_raw_private_content", "metadata_only"],
    }


def test_l6ac02_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ac02-owner-approved-one-read-receipt.md" in docs_index
    assert "tests/test_l6ac02_owner_approved_one_read_receipt.py" in inventory
    assert "L6AC.02 owner-approved one-read receipt" in inventory
    assert "PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ" in inventory


def test_exact_owner_approval_metadata_matches_l6ac01_refs_and_fresh_window():
    approval = build_l6ac02_approval_metadata()

    assert approval["approval_comment_id"] == L6AC_APPROVAL_COMMENT_ID
    assert approval["approval_comment_author"] == "jeremyknows"
    assert approval["owner_actor_association"] == "OWNER"
    assert approval["packet_issue_id"] == "#261"
    assert approval["read_issue_id"] == "#262"
    assert approval["descriptor_ref"] == L6AC_DESCRIPTOR_REF
    assert approval["source_card_ref"] == L6AC_SOURCE_CARD_REF
    assert approval_matches_l6ac_packet(approval, evaluated_at=EVALUATED_AT)


def test_denies_before_read_for_stale_mismatched_broadened_or_non_owner_variants():
    variants = []
    for key, bad_value in (
        ("approval_comment_id", "4651509094"),
        ("approval_comment_author", "someone-else"),
        ("owner_actor_association", "MEMBER"),
        ("packet_issue_id", "#251"),
        ("read_issue_id", "#263"),
        ("operation_class", "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ_AND_SCAN"),
        ("max_operation_count", 2),
        ("descriptor_ref", "descriptor:l6ac/operator-proof"),
        ("source_card_ref", "source-card:l6ac/operator-proof"),
        ("preauth_anchor_refs_present", False),
        ("report_safe_output_only", False),
        ("deny_before_read_on_mismatch", False),
    ):
        variant = build_l6ac02_approval_metadata()
        variant[key] = bad_value
        variants.append(variant)
    stale = build_l6ac02_approval_metadata()
    stale["approval_comment_created_at"] = "2026-06-08T00:00:00Z"
    variants.append(stale)

    for variant in variants:
        calls: list[tuple[str, str]] = []

        def forbidden_read(descriptor_ref: str, source_card_ref: str) -> dict[str, object]:
            calls.append((descriptor_ref, source_card_ref))
            return report_safe_card(descriptor_ref, source_card_ref)

        receipt = execute_l6ac02_one_read(
            variant,
            evaluated_at=EVALUATED_AT,
            read_report_safe_source_card=forbidden_read,
            source_floor_verified_commit=SOURCE_FLOOR,
        )
        assert receipt["receipt_status"] == L6AC_HOLD_STATUS
        assert receipt["approval_result"] == "DENY_BEFORE_READ"
        assert receipt["live_read_invoked"] is False
        assert receipt["allowed"] is False
        assert calls == []
        assert validate_l6ac02_receipt(receipt) == []


def test_executes_exactly_one_report_safe_source_card_read_for_valid_approval():
    calls: list[tuple[str, str]] = []

    def one_read(descriptor_ref: str, source_card_ref: str) -> dict[str, object]:
        calls.append((descriptor_ref, source_card_ref))
        return report_safe_card(descriptor_ref, source_card_ref)

    receipt = execute_l6ac02_one_read(
        build_l6ac02_approval_metadata(),
        evaluated_at=EVALUATED_AT,
        read_report_safe_source_card=one_read,
        source_floor_verified_commit=SOURCE_FLOOR,
    )

    assert calls == [(L6AC_DESCRIPTOR_REF, L6AC_SOURCE_CARD_REF)]
    assert receipt["receipt_status"] == L6AC_PASS_STATUS
    assert receipt["approval_result"] == "APPROVED_EXACT_OWNER_ISSUE_BOUND_FRESH_TARGET_REF_MATCH"
    assert receipt["live_read_invoked"] is True
    assert receipt["allowed"] == "EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY"
    assert receipt["allowed_result_count"] == 1
    assert receipt["operation_count_attempted"] == 1
    assert receipt["source_floor_verified_commit"] == SOURCE_FLOOR
    assert receipt["source_card_report_safe_fields_seen"] == sorted(
        {
            "card_id",
            "source_tier",
            "private_class",
            "canonicality",
            "retrieval_backend",
            "title",
            "safe_summary",
            "reportable",
            "redaction_applied",
            "redaction_labels",
        }
    )
    assert validate_l6ac02_receipt(receipt) == []


def test_rejects_unsafe_source_card_metadata_after_single_attempt_before_report_output():
    calls: list[tuple[str, str]] = []

    def unsafe_read(descriptor_ref: str, source_card_ref: str) -> dict[str, object]:
        calls.append((descriptor_ref, source_card_ref))
        return report_safe_card(descriptor_ref, source_card_ref) | {
            "raw_source_text": "raw private source text"
        }

    receipt = execute_l6ac02_one_read(
        build_l6ac02_approval_metadata(),
        evaluated_at=EVALUATED_AT,
        read_report_safe_source_card=unsafe_read,
        source_floor_verified_commit=SOURCE_FLOOR,
    )

    assert calls == [(L6AC_DESCRIPTOR_REF, L6AC_SOURCE_CARD_REF)]
    assert receipt["receipt_status"] == L6AC_HOLD_STATUS
    assert receipt["live_read_invoked"] is False
    assert receipt["allowed"] is False
    assert receipt["unsafe_raw_fields_rejected_before_report"] is True
    assert validate_l6ac02_receipt(receipt) == []


def test_l6ac02_receipt_doc_records_pass_without_raw_private_content_or_broad_allow():
    text = normalized(DOC)

    required_terms = (
        "Status: `PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ`",
        "Rail issue: #262",
        "Preparation packet issue: #261",
        "Parent issue: #6",
        "Exact max-one read approval comment: `issuecomment-4651509226`",
        "approval_comment_author: `jeremyknows` / `OWNER`",
        "source_floor_verified_commit: `ca81a18fbba9603f5f35a8fa57410963e028c904`",
        "descriptor_ref: `descriptor:l6ac/report-safe-operator-preference-card`",
        "source_card_ref: `source-card:l6ac/report-safe-operator-preference-card`",
        "live_read_invoked: `true`",
        "allowed: `EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY`",
        "allowed_result_count: `1`",
        "operation_count_attempted: `1`",
        "source_read_callbacks: `1`",
        "credential_reads: `0`",
        "runtime_registry_reads: `0`",
        "persistence_writes: `0`",
        "provider_prod_canary_or_gate_moves: `0`",
        "No raw private content was recorded",
        "No broad `allowed=true` route was used",
    )
    for term in required_terms:
        assert term in text
    assert "raw private source text" not in text
    assert "credential value" not in text
    assert "oauth token" not in text
