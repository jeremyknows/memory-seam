from __future__ import annotations

from pathlib import Path

from memory_seam.l6aq_route_audience_repair import (
    L6AQ04_AUTH_STATUS_CODE,
    L6AQ04_DENIAL_REASON,
    L6AQ04_STATUS,
    L6AQ05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR,
    L6AQ05_STATUS,
    assert_l6aq05_reconciliation_report_safe,
    build_l6aq05_post_repair_reconciliation,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aq05-post-repair-source-floor-parent-tracker-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aq05_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aq05-post-repair-source-floor-parent-tracker-reconciliation.md" in docs_index
    assert "tests/test_l6aq05_post_repair_reconciliation.py" in inventory
    assert "L6AQ.05 post-repair retry decision and source-floor reconciliation" in inventory
    assert L6AQ05_STATUS in inventory


def test_l6aq05_reconciles_rail_anchors_retry_metadata_and_holds() -> None:
    receipt = build_l6aq05_post_repair_reconciliation()

    assert receipt["status"] == L6AQ05_STATUS
    assert receipt["rail_issue"] == 404
    assert receipt["parent_issue"] == 6
    assert receipt["rail_starting_source_floor"] == "755ab24e4ac5a283081f134cbc18c95c59d1c60e"
    assert receipt["final_pre_reconciliation_source_floor"] == L6AQ05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR
    assert [anchor["issue"] for anchor in receipt["rail_anchors"]] == [400, 401, 402, 403]
    assert [anchor["pr"] for anchor in receipt["rail_anchors"]] == [405, 406, 407, 408]

    retry = receipt["retry_metadata_summary"]
    assert retry["status"] == L6AQ04_STATUS
    assert retry["endpoint"] == "memory_seam_recall"
    assert retry["route_audience"] == "memory-seam:read:recall"
    assert retry["agent"] == "sax"
    assert retry["acting_for"] == "sax"
    assert retry["scope"] == "wiki"
    assert retry["n"] == 3
    assert retry["query_label"] == "supervised_metadata_readiness"
    assert retry["evidence_class"] == "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
    assert retry["items_count"] == 0
    assert retry["safe_item_labels"] == []
    assert retry["denial_reason"] == L6AQ04_DENIAL_REASON == "wrong_route_audience"
    assert retry["auth_status_code"] == L6AQ04_AUTH_STATUS_CODE == 403
    assert retry["retry_operation_count"] == 1
    assert retry["second_retry_performed"] is False
    assert all(value == 0 for value in retry["guarded_counters"].values())

    assert receipt["step3_state"] == "USEFULNESS_HELD_DENIED_EMPTY_METADATA"
    assert receipt["exact_blocker"] == "SERVICE_ROUTE_AUDIENCE_AUTH_BINDING_STILL_DENIED_AFTER_REPAIR_PROOF"
    assert receipt["external_tracker_written"] is False
    assert receipt["cron_mutated"] is False
    assert receipt["successor_issues_created"] is False
    assert receipt["second_retry_performed"] is False
    assert receipt["provider_prod_canary_gate_or_write_movement_performed"] is False
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6aq05_reconciliation_report_safe(receipt)


def test_l6aq05_reconciliation_is_report_safe_and_contains_no_second_retry_authority() -> None:
    receipt = build_l6aq05_post_repair_reconciliation()
    retry = receipt["retry_metadata_summary"]
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
        "runtime_registry_payload",
        "token",
        "allowed",
        "broad_allowed",
    }

    assert forbidden.isdisjoint(receipt)
    assert forbidden.isdisjoint(retry)
    assert "second_retry" in receipt["residual_holds"]
    assert "successor_issue_creation_from_this_writer" in receipt["residual_holds"]
    assert receipt["parent_receipt_text"].startswith("Parent #6 receipt: L6AQ route-audience repair rail complete")
    assert "no successor issues" in receipt["parent_receipt_text"]
    assert "do not create or run another retry from this rail" in receipt["tracker_update_text"]
    assert_l6aq05_reconciliation_report_safe(receipt)


def test_l6aq05_doc_names_parent_tracker_source_floor_and_boundaries() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AQ.05 post-repair retry decision and source-floor reconciliation",
        f"Status: `{L6AQ05_STATUS}`",
        "Rail issue: #404",
        "Parent issue: #6",
        "Starting source floor: `755ab24e4ac5a283081f134cbc18c95c59d1c60e`",
        "Final pre-reconciliation source floor: `d3ee131fbe566066da60b4b61a7e11957fb65352`",
        "#400 / PR #405 / `2975e5cbe301fab1333306f860993c8b5948b51c`",
        "#401 / PR #406 / `8a82c149455540c134e080735f947dba24c12034`",
        "#402 / PR #407 / `09428d5c4078bc2b9793916aed05b33958fc66f6`",
        "#403 / PR #408 / `d3ee131fbe566066da60b4b61a7e11957fb65352`",
        "Parent #6 receipt: L6AQ route-audience repair rail complete through source-floor reconciliation.",
        "Atlas tracker update text: mark Memory Seam roadmap Step 3 as POST-REPAIR METADATA RETRY ATTEMPTED / DENIED-BEFORE-READ / USEFULNESS HELD",
        "retry_operation_count=1",
        "second_retry_performed=false",
        "items_count=0",
        "safe_item_labels=[]",
        "auth_status_code=403",
        "denial_reason=wrong_route_audience",
        "SERVICE_ROUTE_AUDIENCE_AUTH_BINDING_STILL_DENIED_AFTER_REPAIR_PROOF",
        "No external tracker write, cron mutation, successor issue creation, service activation",
        "python -m pytest -q tests/test_l6aq05_post_repair_reconciliation.py",
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
