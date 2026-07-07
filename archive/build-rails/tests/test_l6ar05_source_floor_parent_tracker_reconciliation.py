from __future__ import annotations

from pathlib import Path

from memory_seam.l6ar_post_auth_usefulness_rail import (
    L6AR03_DEGRADED_FLAGS,
    L6AR03_STATUS,
    L6AR04_REVIEW_VERDICT,
    L6AR04_STATUS,
    L6AR05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR,
    L6AR05_STATUS,
    assert_l6ar05_report_safe,
    build_l6ar05_source_floor_parent_tracker_reconciliation,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ar05-source-floor-parent-tracker-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ar05_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ar05-source-floor-parent-tracker-reconciliation.md" in docs_index
    assert "tests/test_l6ar05_source_floor_parent_tracker_reconciliation.py" in inventory
    assert "L6AR.05 source-floor parent/tracker reconciliation" in inventory
    assert L6AR05_STATUS in inventory


def test_l6ar05_reconciles_source_floor_parent_tracker_and_next_frontier() -> None:
    receipt = build_l6ar05_source_floor_parent_tracker_reconciliation()

    assert receipt["status"] == L6AR05_STATUS
    assert receipt["rail_issue"] == 414
    assert receipt["parent_issue"] == 6
    assert receipt["rail_starting_source_floor"] == "67b5bcc1019899ed3075c8bc44dcfdb9221d9c33"
    assert receipt["system_pipes_repair_floor"] == "a709b14a33b7d22ec980dba97ce20bf56a6c2d86"
    assert receipt["parent_creation_receipt"] == "4663160613"
    assert receipt["final_pre_reconciliation_source_floor"] == L6AR05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR
    assert [anchor["issue"] for anchor in receipt["rail_anchors"]] == [410, 411, 412, 413]
    assert [anchor["pr"] for anchor in receipt["rail_anchors"]] == [415, 416, 417, 418]

    attempt = receipt["attempt_metadata_summary"]
    assert attempt["status"] == L6AR03_STATUS
    assert attempt["endpoint"] == "memory_seam_recall"
    assert attempt["route_audience"] == "memory-seam:read:recall"
    assert attempt["agent"] == "reference-agent"
    assert attempt["acting_for"] == "reference-operator"
    assert attempt["scope"] == "wiki"
    assert attempt["n"] == 3
    assert attempt["query_label"] == "supervised_metadata_readiness"
    assert attempt["evidence_class"] == "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
    assert attempt["auth_status"] == "tool_success"
    assert attempt["denial_reason_label"] == "unauthorized_narrowing"
    assert attempt["degraded"] is True
    assert attempt["degraded_flags"] == list(L6AR03_DEGRADED_FLAGS)
    assert attempt["item_count"] == 0
    assert attempt["safe_item_labels"] == []
    assert attempt["attempt_count"] == 1
    assert attempt["second_attempt_performed"] is False
    assert all(value == 0 for value in attempt["guarded_counters"].values())

    review = receipt["trust_boundary_review"]
    assert review["status"] == L6AR04_STATUS
    assert review["review_verdict"] == L6AR04_REVIEW_VERDICT
    assert review["reviewed_rail_issues"] == [410, 411, 412]
    assert all(value == 0 for value in review["guarded_counters"].values())

    assert receipt["external_tracker_written"] is False
    assert receipt["cron_mutated"] is False
    assert receipt["successor_issues_created"] is False
    assert receipt["second_attempt_performed"] is False
    assert receipt["provider_prod_canary_gate_or_write_movement_performed"] is False
    assert "external tracker updates remain maintainer-owned" in receipt["next_frontier"]
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6ar05_report_safe(receipt)


def test_l6ar05_reconciliation_is_report_safe_and_does_not_widen_authority() -> None:
    receipt = build_l6ar05_source_floor_parent_tracker_reconciliation()
    attempt = receipt["attempt_metadata_summary"]
    forbidden = {
        "query",
        "query_text",
        "items",
        "text",
        "content",
        "raw_text",
        "raw_content",
        "source_uri",
        "source_path",
        "auth_payload",
        "provider_payload",
        "callback_payload",
        "token",
        "secret",
        "allowed",
        "broad_allowed",
    }

    assert forbidden.isdisjoint(receipt)
    assert forbidden.isdisjoint(attempt)
    assert "external tracker edits remain owned by the release maintainer" in receipt["residual_holds"]
    assert "L6AR rail closed without successor issue creation or scheduler mutation" in receipt["residual_holds"]
    assert receipt["parent_receipt_text"].startswith("Parent #6 receipt: L6AR post-auth usefulness rail complete")
    assert "raw/private/source item content" in receipt["parent_receipt_text"]
    assert "do not create or run another usefulness attempt from this rail" in receipt["tracker_update_text"]
    assert_l6ar05_report_safe(receipt)


def test_l6ar05_doc_names_parent_tracker_source_floor_and_boundaries() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AR.05 source-floor parent/tracker reconciliation and next frontier",
        f"Status: `{L6AR05_STATUS}`",
        "Rail issue: #414",
        "Parent issue: #6",
        "Starting source floor: `67b5bcc1019899ed3075c8bc44dcfdb9221d9c33`",
        "Reference adapter repair floor: `a709b14a33b7d22ec980dba97ce20bf56a6c2d86`",
        "Final pre-reconciliation source floor: `0fb18605f2a1150c2f683f1f69b05d5a10f48447`",
        "#410 / PR #415 / `8e1d22cadc8830c00f4cb1578e1cede97b9f4199`",
        "#411 / PR #416 / `6b24532d3f3083bb336466ce7b939aa4d0a60b23`",
        "#412 / PR #417 / `0b460e1127b5cd479cc378dd9059409fde05c270`",
        "#413 / PR #418 / `0fb18605f2a1150c2f683f1f69b05d5a10f48447`",
        "Parent #6 receipt: L6AR post-auth usefulness rail complete through source-floor reconciliation.",
        "Reference tracker update text: mark Memory Seam post-auth usefulness successor rail L6AR as RECONCILED",
        "attempt_count=1",
        "second_attempt_performed=false",
        "item_count=0",
        "safe_item_labels=[]",
        "degraded_flags=[unauthorized_narrowing]",
        "External tracker edits remain maintainer-owned",
        "No external tracker write, scheduler mutation, successor issue creation, second attempt",
        "python -m pytest -q tests/test_l6ar05_source_floor_parent_tracker_reconciliation.py",
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
        "source://",
        "raw item text value",
        "private path value",
        "provider payload value",
    ):
        assert forbidden_marker not in lowered
