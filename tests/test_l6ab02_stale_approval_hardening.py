from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from memory_seam.l6aa_value_proof import (
    L6AA_DESCRIPTOR_REF,
    L6AA_SOURCE_CARD_REF,
    approval_matches_l6aa_packet,
    execute_l6aa02_value_proof,
    validate_l6aa_value_proof_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ab02-stale-approval-hardening.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVALUATED_AT = "2026-06-08T15:35:55Z"
CONSUMED_L6AA_APPROVAL = {
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
    "safe_summary": "Report-safe metadata only; raw source content omitted.",
    "reportable": True,
    "redaction_applied": True,
    "redaction_labels": ["raw-source-content-omitted", "credential-material-not-read"],
}


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def stale_approval_variants() -> Mapping[str, Mapping[str, object]]:
    """Report-safe fixture variants derived from prior HOLD rails and L6AA PASS metadata.

    The fixtures contain no raw private/source-card content and no raw approval text.
    Each negative case mutates a public metadata binding that must deny before read.
    """

    return {
        "stale_issue_number": CONSUMED_L6AA_APPROVAL | {"read_issue_id": "#222"},
        "copied_owner_text_wrong_comment": CONSUMED_L6AA_APPROVAL
        | {"approval_comment_id": "4650520977-copy", "read_issue_id": "#253"},
        "broadened_operation_count": CONSUMED_L6AA_APPROVAL | {"max_operation_count": 2},
        "expired_approval_window": CONSUMED_L6AA_APPROVAL
        | {"approval_comment_created_at": "2026-06-07T15:22:54Z"},
        "mismatched_descriptor_ref": CONSUMED_L6AA_APPROVAL
        | {"descriptor_ref": "descriptor:l6z/operator-proof"},
        "mismatched_source_card_ref": CONSUMED_L6AA_APPROVAL
        | {"source_card_ref": "source-card:l6z/operator-proof"},
        "non_owner_approval": CONSUMED_L6AA_APPROVAL | {"owner_actor_association": "MEMBER"},
        "broad_allowed_true_variant": CONSUMED_L6AA_APPROVAL
        | {"max_operation_count": 2, "allowed": True},
    }


def test_l6ab02_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ab02-stale-approval-hardening.md" in docs_index
    assert "tests/test_l6ab02_stale_approval_hardening.py" in inventory
    assert "L6AB.02 stale approval hardening" in inventory
    assert "STALE_APPROVAL_HARDENING_FIXTURES_NO_LIVE_READS" in inventory


def test_l6ab02_doc_records_required_fixture_classes_and_holds():
    text = normalized(DOC)

    required_terms = (
        "Status: `STALE_APPROVAL_HARDENING_FIXTURES_NO_LIVE_READS`",
        "Rail issue: #252",
        "Parent issue: #6",
        "Depends on: #251 closed/PASS",
        "stale issue numbers",
        "copied owner text",
        "broadened operation counts",
        "expired approval windows",
        "mismatched descriptor/source-card refs",
        "non-owner approval",
        "broad `allowed=true` variants",
        "The exact #242 PASS fixture is consumed historical evidence only",
        "no live/private reads",
    )
    for term in required_terms:
        assert term in text


def test_l6ab02_negative_approval_fixtures_deny_before_read():
    for case_id, approval in stale_approval_variants().items():
        called = False

        def reader(_descriptor_ref: str, _source_card_ref: str) -> dict[str, object]:
            nonlocal called
            called = True
            return dict(SAFE_SOURCE_CARD_METADATA)

        assert approval_matches_l6aa_packet(approval, evaluated_at=EVALUATED_AT) is False, case_id
        receipt = execute_l6aa02_value_proof(
            approval,
            evaluated_at=EVALUATED_AT,
            read_report_safe_source_card=reader,
        )

        assert called is False, case_id
        assert receipt["receipt_status"] == "HOLD_DENIED_BEFORE_READ", case_id
        assert receipt["live_read_invoked"] is False, case_id
        assert receipt["allowed"] is False, case_id
        assert receipt["allowed_result_count"] == 0, case_id
        assert receipt["operation_count_attempted"] == 0, case_id
        assert validate_l6aa_value_proof_receipt(receipt) == [], case_id


def test_l6ab02_exact_l6aa_pass_fixture_is_single_consumed_read_not_standing_authority():
    receipt = execute_l6aa02_value_proof(
        CONSUMED_L6AA_APPROVAL,
        evaluated_at=EVALUATED_AT,
        read_report_safe_source_card=lambda _descriptor_ref, _source_card_ref: dict(SAFE_SOURCE_CARD_METADATA),
    )

    assert validate_l6aa_value_proof_receipt(receipt) == []
    assert receipt["receipt_status"] == "PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ"
    assert receipt["read_issue_id"] == "#242"
    assert receipt["allowed"] == "EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY"
    assert receipt["allowed"] is not True
    assert receipt["allowed_result_count"] == 1
    assert receipt["operation_count_attempted"] == 1

    replay_as_new_issue = CONSUMED_L6AA_APPROVAL | {"read_issue_id": "#252"}
    assert approval_matches_l6aa_packet(replay_as_new_issue, evaluated_at=EVALUATED_AT) is False


def test_l6ab02_receipt_validator_rejects_broad_allowed_true_variants():
    receipt = execute_l6aa02_value_proof(
        CONSUMED_L6AA_APPROVAL,
        evaluated_at=EVALUATED_AT,
        read_report_safe_source_card=lambda _descriptor_ref, _source_card_ref: dict(SAFE_SOURCE_CARD_METADATA),
    )

    broad_allowed = dict(receipt) | {"allowed": True}
    broadened_counter = dict(receipt)
    broadened_counter["guarded_counters"] = dict(receipt["guarded_counters"]) | {
        "allowed_result_count": 2,
    }

    assert "allowed_broadened_or_missing" in validate_l6aa_value_proof_receipt(broad_allowed)
    assert "unexpected_counter_allowed_result_count" in validate_l6aa_value_proof_receipt(broadened_counter)
