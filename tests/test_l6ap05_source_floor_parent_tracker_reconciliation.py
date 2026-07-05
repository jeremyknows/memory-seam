from __future__ import annotations

from pathlib import Path

from memory_seam.l6ap_metadata_retry_rail import (
    L6AP05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR,
    L6AP05_PARENT_RECEIPT_TEXT,
    L6AP05_RAIL_ANCHORS,
    L6AP05_STATUS,
    L6AP05_TRACKER_UPDATE_TEXT,
    assert_l6ap05_reconciliation_report_safe,
    build_l6ap05_source_floor_parent_tracker_reconciliation,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ap05-source-floor-parent-tracker-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ap05_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ap05-source-floor-parent-tracker-reconciliation.md" in docs_index
    assert "tests/test_l6ap05_source_floor_parent_tracker_reconciliation.py" in inventory
    assert "L6AP.05 source-floor parent tracker reconciliation" in inventory
    assert L6AP05_STATUS in inventory


def test_reconciliation_records_issue_pr_and_source_floor_summary() -> None:
    receipt = build_l6ap05_source_floor_parent_tracker_reconciliation()

    assert receipt["status"] == L6AP05_STATUS
    assert receipt["rail_issue"] == 394
    assert receipt["parent_issue"] == 6
    assert receipt["rail_starting_source_floor"] == "35046efe4880145d929bbe0ddb00196b83c9cc04"
    assert receipt["final_pre_reconciliation_source_floor"] == L6AP05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR
    assert receipt["rail_anchors"] == [dict(anchor) for anchor in L6AP05_RAIL_ANCHORS]
    assert [anchor["issue"] for anchor in receipt["rail_anchors"]] == [390, 391, 392, 393]
    assert [anchor["pr"] for anchor in receipt["rail_anchors"]] == [395, 396, 397, 398]
    assert_l6ap05_reconciliation_report_safe(receipt)


def test_retry_metadata_keeps_step3_held_without_successor_execution() -> None:
    receipt = build_l6ap05_source_floor_parent_tracker_reconciliation()

    assert receipt["final_result"] == "metadata retry rail reconciled; Step 3 usefulness remains held"
    assert receipt["next_frontier"] == (
        "service route-audience auth binding repair or operator/service configuration proof "
        "before any newly authorized max-one metadata retry"
    )
    assert receipt["retry_metadata_summary"] == {
        "status": "SUPERVISED_METADATA_RETRY_SAFE_DENIAL_CAPTURED",
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "sax",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "items_count": 0,
        "safe_item_labels": [],
        "denial_reason": "wrong_route_audience",
        "auth_status_code": 403,
        "retry_operation_count": 1,
        "second_retry_performed": False,
        "guarded_counters": receipt["retry_metadata_summary"]["guarded_counters"],
    }
    assert all(value == 0 for value in receipt["retry_metadata_summary"]["guarded_counters"].values())
    assert receipt["successor_execution_rail_created"] is False


def test_parent_receipt_and_tracker_update_text_are_inert_and_report_safe() -> None:
    receipt = build_l6ap05_source_floor_parent_tracker_reconciliation()

    assert receipt["parent_receipt_text"] == L6AP05_PARENT_RECEIPT_TEXT
    assert receipt["tracker_update_text"] == L6AP05_TRACKER_UPDATE_TEXT
    for text in (receipt["parent_receipt_text"], receipt["tracker_update_text"]):
        assert "auth_status_code=403" in text or "auth_status_code 403" in text
        assert "wrong_route_audience" in text
        assert "items_count=0" in text or "items_count 0" in text
        assert "no second retry" in text
    assert receipt["external_tracker_written"] is False
    assert receipt["cron_mutated"] is False
    assert receipt["provider_prod_canary_gate_or_write_movement_performed"] is False


def test_residual_holds_preserve_hard_boundaries() -> None:
    receipt = build_l6ap05_source_floor_parent_tracker_reconciliation()

    for hold in (
        "step3_current_session_usefulness",
        "successor_execution_rail",
        "second_retry",
        "raw_private_source_content_or_source_path_uri",
        "auth_provider_payload_secret_env_keychain_oauth_auth_file_or_credential_reads",
        "runtime_registry_provider_callback_or_service_activation",
        "source_discovery_broad_recall_or_broad_allowed_true",
        "external_tracker_write_or_cron_mutation_from_writer",
        "provider_prod_canary_gate_atlas_gate_write_or_mutation",
    ):
        assert hold in receipt["residual_holds"]


def test_report_safe_assertion_rejects_retry_external_mutation_and_unsafe_fields() -> None:
    receipt = build_l6ap05_source_floor_parent_tracker_reconciliation()

    unsafe_receipts = (
        receipt | {"successor_execution_rail_created": True},
        receipt | {"external_tracker_written": True},
        receipt | {"cron_mutated": True},
        receipt | {"provider_prod_canary_gate_or_write_movement_performed": True},
        receipt | {"raw_source_text": "forbidden"},
        receipt | {"guarded_counters": receipt["guarded_counters"] | {"source_items_returned": 1}},
        receipt | {"rail_anchors": receipt["rail_anchors"][1:]},
        receipt
        | {
            "retry_metadata_summary": receipt["retry_metadata_summary"]
            | {"retry_operation_count": 2}
        },
    )
    for unsafe in unsafe_receipts:
        try:
            assert_l6ap05_reconciliation_report_safe(unsafe)
        except AssertionError:
            pass
        else:  # pragma: no cover - defensive guard
            raise AssertionError("unsafe L6AP.05 reconciliation should fail closed")


def test_doc_names_parent_receipt_tracker_update_and_verification_commands() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AP.05 source-floor parent tracker reconciliation for metadata retry rail",
        f"Status: `{L6AP05_STATUS}`",
        "Rail issue: #394",
        "Parent issue: #6",
        "Starting source floor: `35046efe4880145d929bbe0ddb00196b83c9cc04`",
        f"Final pre-reconciliation source floor: `{L6AP05_FINAL_PRE_RECONCILIATION_SOURCE_FLOOR}`",
        "#390 / PR #395 / `55ee79090eea1ac62bdc6dc3760e6f8c28fb55bf`",
        "#391 / PR #396 / `e5efaa1a61cca0573c5ce5c6a325f15de14e9ca7`",
        "#392 / PR #397 / `e19be48cd1e2085f4af9deff9bfd0912dd043f2a`",
        "#393 / PR #398 / `87c1f917eb48b77e19257dd4f8e6dd3740f13be4`",
        "metadata retry rail reconciled; Step 3 usefulness remains held",
        L6AP05_PARENT_RECEIPT_TEXT,
        L6AP05_TRACKER_UPDATE_TEXT,
        "No external tracker write or cron mutation is performed by this writer",
        "python -m pytest -q tests/test_l6ap05_source_floor_parent_tracker_reconciliation.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
