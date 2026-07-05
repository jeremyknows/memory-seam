from __future__ import annotations

from pathlib import Path

from memory_seam.l6an_service_operator_auth_binding_packet import (
    L6AN01_RAIL_STARTING_SOURCE_FLOOR,
    L6AN05_FINAL_SOURCE_FLOOR_BEFORE_RECONCILIATION,
    L6AN05_NEXT_FRONTIER,
    L6AN05_STATUS,
    L6AN05_TRACKER_REF,
    L6AN05_TRACKER_UPDATE_STATE,
    assert_l6an05_reconciliation_report_safe,
    build_l6an05_source_floor_parent_tracker_reconciliation,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6an05-source-floor-parent-tracker-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6an05_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6an05-source-floor-parent-tracker-reconciliation.md" in docs_index
    assert "tests/test_l6an05_source_floor_parent_tracker_reconciliation.py" in inventory
    assert "L6AN.05 source-floor parent tracker reconciliation" in inventory
    assert L6AN05_STATUS in inventory


def test_reconciliation_receipt_anchors_rail_and_parent_status() -> None:
    receipt = build_l6an05_source_floor_parent_tracker_reconciliation()

    assert receipt["status"] == L6AN05_STATUS
    assert receipt["rail_starting_source_floor"] == L6AN01_RAIL_STARTING_SOURCE_FLOOR
    assert receipt["final_source_floor_before_reconciliation"] == L6AN05_FINAL_SOURCE_FLOOR_BEFORE_RECONCILIATION
    assert [item["issue"] for item in receipt["rail_evidence"]] == [370, 371, 372, 373]
    assert [item["pr"] for item in receipt["rail_evidence"]] == [375, 376, 377, 378]
    assert receipt["service_operator_auth_binding_request_ready"] is True
    assert "retry remains held" in receipt["parent_completion_receipt"]
    assert "new max-one retry issue" in receipt["parent_completion_receipt"]
    assert_l6an05_reconciliation_report_safe(receipt)


def test_tracker_update_and_next_frontier_are_pinned() -> None:
    receipt = build_l6an05_source_floor_parent_tracker_reconciliation()

    assert receipt["tracker_ref"] == L6AN05_TRACKER_REF
    assert receipt["tracker_update_state"] == L6AN05_TRACKER_UPDATE_STATE
    assert "Step 3 becomes AUTH BINDING UNBLOCK REQUEST READY / RETRY HELD" in receipt[
        "tracker_update_summary"
    ]
    assert "current-session usefulness and fresh-agent proof remain held" in receipt[
        "tracker_update_summary"
    ]
    assert receipt["next_frontier"] == L6AN05_NEXT_FRONTIER
    assert "L6AO exact max-one metadata retry" in receipt["next_frontier"]
    assert all(value == 0 for value in receipt["guarded_counters"].values())


def test_verification_and_residual_holds_are_complete() -> None:
    receipt = build_l6an05_source_floor_parent_tracker_reconciliation()

    for command in (
        "python -m pytest -q tests/test_l6an05_source_floor_parent_tracker_reconciliation.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert command in receipt["verification_commands"]

    for hold in (
        "no_live_private_retry",
        "no_secret_env_keychain_oauth_auth_file_credential_reads",
        "no_runtime_registry_consumption",
        "no_provider_callback_or_service_activation",
        "no_source_discovery_or_broad_recall",
        "no_successor_issue_created_by_reconciliation",
        "no_cron_job_created_modified_removed_resumed_or_paused",
        "no_provider_prod_canary_gate_or_atlas_gate_movement",
    ):
        assert hold in receipt["residual_holds"]


def test_doc_names_parent_tracker_final_floor_and_next_frontier() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AN.05 source-floor parent tracker reconciliation",
        f"Status: `{L6AN05_STATUS}`",
        "Rail issue: #374",
        "Parent issue: #6",
        f"Rail starting source floor: `{L6AN01_RAIL_STARTING_SOURCE_FLOOR}`",
        f"Final source floor before reconciliation: `{L6AN05_FINAL_SOURCE_FLOOR_BEFORE_RECONCILIATION}`",
        "#370 / PR #375",
        "#371 / PR #376",
        "#372 / PR #377",
        "#373 / PR #378",
        "service/operator auth-binding request is ready",
        "retry remains held unless exact fresh binding approval exists",
        L6AN05_TRACKER_REF,
        L6AN05_TRACKER_UPDATE_STATE,
        L6AN05_NEXT_FRONTIER,
        "python -m pytest -q tests/test_l6an05_source_floor_parent_tracker_reconciliation.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
