from __future__ import annotations

from pathlib import Path

from memory_seam.l6am_source_floor_reconciliation import (
    L6AM04_ACTIVE_FINAL_POKE_ID,
    L6AM04_ACTIVE_WRITER_ID,
    L6AM04_DISPATCH_POKE_STATE,
    L6AM04_FINAL_SOURCE_FLOOR,
    L6AM04_STATUS,
    L6AM04_TRACKER_REF,
    L6AM04_TRACKER_UPDATE_STATE,
    assert_l6am04_reconciliation_report_safe,
    build_l6am04_reconciliation_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6am04-source-floor-parent-tracker-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6am04_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6am04-source-floor-parent-tracker-reconciliation.md" in docs_index
    assert "tests/test_l6am04_source_floor_reconciliation.py" in inventory
    assert "L6AM.04 source-floor parent tracker reconciliation" in inventory
    assert L6AM04_STATUS in inventory


def test_reconciliation_receipt_pins_rail_prs_source_floor_and_retry_outcome() -> None:
    receipt = build_l6am04_reconciliation_receipt()

    assert receipt["status"] == L6AM04_STATUS
    assert receipt["rail_starting_source_floor"] == "9ea7cd0ab724292b8a2841c9e2c080f14a524ee2"
    assert receipt["final_source_floor"] == L6AM04_FINAL_SOURCE_FLOOR
    assert [item["issue"] for item in receipt["rail_evidence"]] == [357, 358, 359]
    assert [item["pr"] for item in receipt["rail_evidence"]] == [366, 367, 368]
    assert receipt["retry_outcome"] == {
        "auth_status_code": 403,
        "degraded_reason": "wrong_route_audience",
        "item_count": 0,
        "blocker_classification": "SERVICE_ROUTE_AUDIENCE_AUTH_BINDING_BLOCKED_DENIAL_BEFORE_READ",
    }
    assert receipt["next_frontier"].startswith("fresh operator/service auth binding")
    assert_l6am04_reconciliation_report_safe(receipt)


def test_tracker_and_dispatch_poke_are_boundary_labeled() -> None:
    receipt = build_l6am04_reconciliation_receipt()

    assert receipt["tracker_ref"] == L6AM04_TRACKER_REF
    assert receipt["tracker_update_state"] == L6AM04_TRACKER_UPDATE_STATE
    assert "Step 3 becomes AUTH UNBLOCK PACKET READY / RETRY HELD" in receipt[
        "tracker_update_summary"
    ]
    assert receipt["dispatch_poke_state"] == L6AM04_DISPATCH_POKE_STATE
    assert receipt["active_writer_id"] == L6AM04_ACTIVE_WRITER_ID
    assert receipt["active_final_poke_id"] == L6AM04_ACTIVE_FINAL_POKE_ID
    assert all(value == 0 for value in receipt["guarded_counters"].values())


def test_verification_and_residual_holds_are_complete() -> None:
    receipt = build_l6am04_reconciliation_receipt()

    for command in (
        "python -m pytest -q tests/test_l6am04_source_floor_reconciliation.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert command in receipt["verification_commands"]

    for hold in (
        "no_live_read_retry",
        "no_secret_env_keychain_oauth_auth_file_reads",
        "no_runtime_registry_consumption",
        "no_service_activation",
        "no_provider_prod_canary_gate_movement",
        "no_write_mutation_persistence",
        "no_new_cron_created_inside_cron_run",
    ):
        assert hold in receipt["residual_holds"]


def test_doc_names_parent_tracker_poke_and_next_frontier() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AM.04 source-floor parent tracker reconciliation",
        f"Status: `{L6AM04_STATUS}`",
        "Rail issue: #360",
        "Parent issue: #6",
        "Rail starting source floor: `9ea7cd0ab724292b8a2841c9e2c080f14a524ee2`",
        f"Final source floor: `{L6AM04_FINAL_SOURCE_FLOOR}`",
        "#357 / PR #366",
        "#358 / PR #367",
        "#359 / PR #368",
        "`auth_status_code=403`, `wrong_route_audience`, `items=0`",
        "fresh operator/service auth binding for exact metadata recall before current-session or fresh-agent proof",
        L6AM04_TRACKER_REF,
        L6AM04_TRACKER_UPDATE_STATE,
        L6AM04_DISPATCH_POKE_STATE,
        f"writer `{L6AM04_ACTIVE_WRITER_ID}`",
        f"conditional final poke `{L6AM04_ACTIVE_FINAL_POKE_ID}`",
        "No new cron was created from inside this cron run.",
        "python -m pytest -q tests/test_l6am04_source_floor_reconciliation.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
