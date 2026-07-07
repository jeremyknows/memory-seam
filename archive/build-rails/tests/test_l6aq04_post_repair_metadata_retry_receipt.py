from __future__ import annotations

from pathlib import Path

from memory_seam.l6aq_route_audience_repair import (
    L6AQ01_EXPECTED_ROUTE_AUDIENCE,
    L6AQ02_READY_STATUS,
    L6AQ03_READY_STATUS,
    L6AQ04_AUTH_STATUS_CODE,
    L6AQ04_DENIAL_REASON,
    L6AQ04_STATUS,
    assert_l6aq04_retry_receipt_report_safe,
    build_l6aq04_post_repair_metadata_retry_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aq04-post-repair-metadata-retry-denial-receipt.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aq04_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aq04-post-repair-metadata-retry-denial-receipt.md" in docs_index
    assert "tests/test_l6aq04_post_repair_metadata_retry_receipt.py" in inventory
    assert "L6AQ.04 post-repair metadata retry denial receipt" in inventory
    assert L6AQ04_STATUS in inventory


def test_post_repair_retry_receipt_records_exactly_one_denied_metadata_attempt() -> None:
    receipt = build_l6aq04_post_repair_metadata_retry_receipt()

    assert receipt["status"] == L6AQ04_STATUS
    assert receipt["rail_issue"] == 403
    assert receipt["rail_starting_source_floor"] == "755ab24e4ac5a283081f134cbc18c95c59d1c60e"
    assert receipt["preflight"]["binding_contract_status"] == L6AQ02_READY_STATUS
    assert receipt["preflight"]["configuration_proof_status"] == L6AQ03_READY_STATUS
    assert receipt["preflight"]["preflight_passed"] is True
    assert receipt["endpoint"] == "memory_seam_recall"
    assert receipt["route_audience"] == L6AQ01_EXPECTED_ROUTE_AUDIENCE
    assert receipt["agent"] == "sax"
    assert receipt["acting_for"] == "sax"
    assert receipt["scope"] == "wiki"
    assert receipt["n"] == 3
    assert receipt["query_label"] == "supervised_metadata_readiness"
    assert receipt["evidence_class"] == "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
    assert receipt["items_count"] == 0
    assert receipt["safe_item_labels"] == []
    assert receipt["denial_reason"] == L6AQ04_DENIAL_REASON == "wrong_route_audience"
    assert receipt["auth_status_code"] == L6AQ04_AUTH_STATUS_CODE == 403
    assert receipt["retry_operation_count"] == 1
    assert receipt["second_retry_performed"] is False
    assert receipt["max_operation_count"] == 1
    assert receipt["report_safe_metadata_only"] is True
    assert receipt["denial_before_read_required"] is True
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6aq04_retry_receipt_report_safe(receipt)


def test_post_repair_retry_receipt_contains_no_source_payload_or_second_retry_fields() -> None:
    receipt = build_l6aq04_post_repair_metadata_retry_receipt()
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
    assert forbidden.isdisjoint(receipt["preflight"])
    assert receipt["retry_operation_count"] == 1
    assert receipt["second_retry_performed"] is False
    assert_l6aq04_retry_receipt_report_safe(receipt)


def test_doc_names_retry_metadata_preflight_stop_and_holds() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AQ.04 post-repair metadata retry denial receipt",
        f"Status: `{L6AQ04_STATUS}`",
        "Rail issue: #403",
        "Parent issue: #6",
        "Rail starting source floor: `755ab24e4ac5a283081f134cbc18c95c59d1c60e`",
        "#401/#402 preflight: `passed`",
        "endpoint | `memory_seam_recall`",
        "route audience | `memory-seam:read:recall`",
        "acting_for / agent | `sax` / `sax`",
        "scope / n | `wiki` / `3`",
        "query label | `supervised_metadata_readiness`",
        "evidence class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`",
        "retry operation count | `1`",
        "second retry performed | `false`",
        "items count | `0`",
        "safe item labels | `[]`",
        "denial reason | `wrong_route_audience`",
        "auth status code | `403`",
        "The denied/empty result stopped the rail issue; no second retry was performed.",
        "python -m pytest -q tests/test_l6aq04_post_repair_metadata_retry_receipt.py",
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
