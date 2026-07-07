from __future__ import annotations

from pathlib import Path

from memory_seam.l6ab_value_comparison import (
    L6AB01_PRESERVED_HOLDS,
    L6AB01_SAFE_MATRIX_FIELDS,
    L6AB01_SAFE_PACKET_FIELDS,
    L6AB01_SCHEMA_VERSION,
    L6AB01_STATUS,
    build_l6ab01_value_comparison_matrix,
    validate_l6ab01_value_comparison_packet,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ab01-report-safe-source-card-value-comparison-matrix.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ab01_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ab01-report-safe-source-card-value-comparison-matrix.md" in docs_index
    assert "tests/test_l6ab01_report_safe_source_card_value_comparison.py" in inventory
    assert "L6AB.01 report-safe source-card value comparison matrix" in inventory
    assert L6AB01_STATUS in inventory


def test_l6ab01_doc_records_matrix_and_boundaries():
    text = normalized(DOC)

    required_terms = (
        "Status: `REPORT_SAFE_VALUE_COMPARISON_MATRIX_NO_LIVE_READS`",
        "Rail issue: #251",
        "Parent issue: #6",
        "Depends on: L6AA rail closed at source floor `91761ed55889f4c5432b55c445e396e727a6be93`",
        "Absent approval",
        "Missing target refs",
        "Mismatched target refs",
        "Exact owner-approved target refs",
        "PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ",
        "EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY",
        "The L6AA PASS row is historical evidence for the already-consumed #242 one-read allowance",
        "It is not reusable approval and cannot authorize another read",
        "no live/private read",
        "no broad `allowed=true` route",
    )
    for term in required_terms:
        assert term in text


def test_l6ab01_matrix_distinguishes_required_outcomes_in_order():
    packet = build_l6ab01_value_comparison_matrix()

    assert validate_l6ab01_value_comparison_packet(packet) == []
    assert packet["schema_version"] == L6AB01_SCHEMA_VERSION
    assert packet["status"] == L6AB01_STATUS
    rows = packet["matrix"]
    assert [row["case_id"] for row in rows] == [
        "absent-approval",
        "missing-target-refs",
        "mismatched-target-refs",
        "exact-owner-approved-target-refs",
    ]
    assert rows[0]["approval_state"] == "ABSENT_OWNER_APPROVAL"
    assert rows[0]["target_ref_state"] == "NOT_REACHED_NO_APPROVAL"
    assert rows[1]["target_ref_state"] == "MISSING_EXECUTABLE_DESCRIPTOR_AND_SOURCE_CARD_REFS"
    assert rows[2]["target_ref_state"] == "MISMATCHED_EXECUTABLE_DESCRIPTOR_OR_SOURCE_CARD_REFS"
    assert rows[3]["approval_state"] == "APPROVED_EXACT_OWNER_ISSUE_BOUND_FRESH_TARGET_REF_MATCH"
    assert rows[3]["target_ref_state"] == "EXACT_DESCRIPTOR_AND_SOURCE_CARD_REF_MATCH"


def test_l6ab01_matrix_is_metadata_only_and_cannot_authorize_another_read():
    packet = build_l6ab01_value_comparison_matrix()

    assert set(packet) == L6AB01_SAFE_PACKET_FIELDS
    assert packet["additional_live_read_invoked"] is False
    assert packet["callbacks_invoked"] is False
    assert packet["metadata_only"] is True
    assert packet["report_safe"] is True
    assert packet["cannot_authorize_another_read"] is True
    for held in L6AB01_PRESERVED_HOLDS:
        assert held in packet["preserved_holds"]
    for row in packet["matrix"]:
        assert set(row) == L6AB01_SAFE_MATRIX_FIELDS
        assert row["cannot_authorize_another_read"] is True
        assert row["allowed"] is not True


def test_l6ab01_hold_rows_cannot_smuggle_read_authority():
    packet = build_l6ab01_value_comparison_matrix()

    for row in packet["matrix"][:-1]:
        assert row["live_read_invoked"] is False
        assert row["allowed"] is False
        assert row["allowed_result_count"] == 0
        assert row["operation_count_attempted"] == 0
        assert row["descriptor_ref_match"] is False
        assert row["source_card_ref_match"] is False

    for mutation in (
        {"matrix": [dict(packet["matrix"][0]) | {"allowed": True}] + packet["matrix"][1:]},
        {"matrix": [dict(packet["matrix"][0]) | {"live_read_invoked": True}] + packet["matrix"][1:]},
        {"matrix": [dict(packet["matrix"][0]) | {"allowed_result_count": 1}] + packet["matrix"][1:]},
    ):
        mutated = dict(packet) | mutation
        assert validate_l6ab01_value_comparison_packet(mutated)


def test_l6ab01_pass_row_is_exactly_one_historical_consumed_read_only():
    packet = build_l6ab01_value_comparison_matrix()
    pass_row = packet["matrix"][-1]

    assert pass_row["source_rail"] == "L6AA"
    assert pass_row["issue_anchor"] == "#242/#245"
    assert pass_row["receipt_status"] == "PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ"
    assert pass_row["comparison_outcome"] == "PASS_ONE_HISTORICAL_REPORT_SAFE_SOURCE_CARD_READ_CONSUMED"
    assert pass_row["live_read_invoked"] is True
    assert pass_row["allowed"] == "EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY"
    assert pass_row["allowed_result_count"] == 1
    assert pass_row["operation_count_attempted"] == 1
    assert pass_row["descriptor_ref_match"] is True
    assert pass_row["source_card_ref_match"] is True

    broadened = dict(packet)
    broadened["matrix"] = packet["matrix"][:-1] + [dict(pass_row) | {"allowed": True}]
    assert "broad_allowed_true_present" in validate_l6ab01_value_comparison_packet(broadened)
