from __future__ import annotations

from pathlib import Path

from memory_seam.l6ao_auth_held_default_off_intake import (
    L6AO05_FINAL_SOURCE_FLOOR,
    L6AO05_PARENT_RECEIPT_TEXT,
    L6AO05_RAIL_ANCHORS,
    L6AO05_STATUS,
    L6AO05_TRACKER_UPDATE_TEXT,
    assert_l6ao05_reconciliation_report_safe,
    build_l6ao05_source_floor_parent_tracker_reconciliation,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ao05-source-floor-parent-tracker-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ao05_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ao05-source-floor-parent-tracker-reconciliation.md" in docs_index
    assert "tests/test_l6ao05_source_floor_parent_tracker_reconciliation.py" in inventory
    assert "L6AO.05 source-floor parent tracker reconciliation" in inventory
    assert L6AO05_STATUS in inventory


def test_reconciliation_records_issue_pr_and_source_floor_summary() -> None:
    receipt = build_l6ao05_source_floor_parent_tracker_reconciliation()

    assert receipt["status"] == L6AO05_STATUS
    assert receipt["rail_issue"] == 384
    assert receipt["parent_issue"] == 6
    assert receipt["rail_starting_source_floor"] == "57e8bd4612824ada20718e41b1eea33210fe2974"
    assert receipt["final_source_floor"] == L6AO05_FINAL_SOURCE_FLOOR
    assert receipt["rail_anchors"] == [dict(anchor) for anchor in L6AO05_RAIL_ANCHORS]
    assert [anchor["issue"] for anchor in receipt["rail_anchors"]] == [380, 381, 382, 383]
    assert [anchor["pr"] for anchor in receipt["rail_anchors"]] == [385, 386, 387, 388]
    assert_l6ao05_reconciliation_report_safe(receipt)


def test_final_result_and_retry_hold_require_exact_future_authority() -> None:
    receipt = build_l6ao05_source_floor_parent_tracker_reconciliation()

    assert receipt["final_result"] == "auth-held unblock rail complete"
    assert receipt["retry_state"] == (
        "retry remains held unless fresh exact non-secret binding approval plus explicit "
        "max-one retry issue exists"
    )
    assert receipt["retry_authorized"] is False
    assert receipt["retry_executed"] is False
    assert all(value == 0 for value in receipt["guarded_counters"].values())


def test_parent_receipt_and_tracker_update_text_are_inert_and_report_safe() -> None:
    receipt = build_l6ao05_source_floor_parent_tracker_reconciliation()

    assert receipt["parent_receipt_text"] == L6AO05_PARENT_RECEIPT_TEXT
    assert receipt["tracker_update_text"] == L6AO05_TRACKER_UPDATE_TEXT
    for text in (receipt["parent_receipt_text"], receipt["tracker_update_text"]):
        assert "auth-held/default-off unblock rail complete" in text
        assert "fresh exact non-secret binding approval" in text
        assert "explicit max-one retry issue" in text
    assert receipt["external_tracker_written"] is False
    assert receipt["cron_mutated"] is False


def test_residual_holds_preserve_hard_boundaries() -> None:
    receipt = build_l6ao05_source_floor_parent_tracker_reconciliation()

    for hold in (
        "live_retry",
        "raw_private_source_or_auth_content",
        "secret_env_keychain_oauth_auth_file_or_credential_reads",
        "runtime_registry_provider_callback_or_service_activation",
        "source_discovery_broad_recall_or_broad_allowed_true",
        "external_tracker_write_or_cron_mutation_from_writer",
        "provider_prod_canary_gate_atlas_gate_write_or_mutation",
    ):
        assert hold in receipt["residual_holds"]


def test_report_safe_assertion_rejects_retry_external_mutation_and_unsafe_fields() -> None:
    receipt = build_l6ao05_source_floor_parent_tracker_reconciliation()

    unsafe_receipts = (
        receipt | {"retry_authorized": True},
        receipt | {"retry_executed": True},
        receipt | {"external_tracker_written": True},
        receipt | {"cron_mutated": True},
        receipt | {"raw_private_source": "forbidden"},
        receipt | {"guarded_counters": receipt["guarded_counters"] | {"source_items_returned": 1}},
        receipt | {"rail_anchors": receipt["rail_anchors"][1:]},
    )
    for unsafe in unsafe_receipts:
        try:
            assert_l6ao05_reconciliation_report_safe(unsafe)
        except AssertionError:
            pass
        else:  # pragma: no cover - defensive guard
            raise AssertionError("unsafe L6AO.05 reconciliation should fail closed")


def test_doc_names_parent_receipt_tracker_update_and_verification_commands() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AO.05 source-floor parent tracker reconciliation for auth-held unblock rail",
        f"Status: `{L6AO05_STATUS}`",
        "Rail issue: #384",
        "Parent issue: #6",
        "Starting source floor: `57e8bd4612824ada20718e41b1eea33210fe2974`",
        f"Final pre-reconciliation source floor: `{L6AO05_FINAL_SOURCE_FLOOR}`",
        "#380 / PR #385 / `e012328ec4156b778b797d48b6a16c8363398cac`",
        "#381 / PR #386 / `d7bbb00f955522baf8a62c3c3b5daa8604e39424`",
        "#382 / PR #387 / `2ca36d07ba02bda0f33de9db7955ae6ffd0b1b54`",
        "#383 / PR #388 / `93481ca84ca2e1f3535acbb68d22199e09ed41be`",
        "auth-held unblock rail complete; retry remains held unless fresh exact non-secret binding approval plus explicit max-one retry issue exists",
        L6AO05_PARENT_RECEIPT_TEXT,
        L6AO05_TRACKER_UPDATE_TEXT,
        "No external tracker write or cron mutation is performed by this writer",
        "python -m pytest -q tests/test_l6ao05_source_floor_parent_tracker_reconciliation.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
