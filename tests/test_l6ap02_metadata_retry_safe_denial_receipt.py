from __future__ import annotations

from pathlib import Path

from memory_seam.l6ap_metadata_retry_rail import (
    L6AP02_BLOCKER_CLASSIFICATION,
    L6AP02_REPORT_SAFE_OUTPUT_FIELDS,
    L6AP02_STATUS,
    assert_l6ap02_receipt_report_safe,
    build_l6ap02_safe_denial_receipt,
    exact_l6ap02_retry_binding,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ap02-supervised-metadata-retry-safe-denial-receipt.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ap02_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ap02-supervised-metadata-retry-safe-denial-receipt.md" in docs_index
    assert "tests/test_l6ap02_metadata_retry_safe_denial_receipt.py" in inventory
    assert "L6AP.02 supervised metadata retry safe-denial receipt" in inventory
    assert L6AP02_STATUS in inventory


def test_exact_retry_binding_excludes_source_bearing_query_text() -> None:
    assert exact_l6ap02_retry_binding() == {
        "tool": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "sax",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "max_operation_count": 1,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
    }


def test_safe_denial_receipt_records_only_report_safe_metadata() -> None:
    receipt = build_l6ap02_safe_denial_receipt()

    assert receipt["status"] == L6AP02_STATUS
    assert receipt["blocker_classification"] == L6AP02_BLOCKER_CLASSIFICATION
    assert receipt["endpoint"] == "memory_seam_recall"
    assert receipt["route_audience"] == "memory-seam:read:recall"
    assert receipt["agent"] == "sax"
    assert receipt["scope"] == "wiki"
    assert receipt["n"] == 3
    assert receipt["query_label"] == "supervised_metadata_readiness"
    assert receipt["evidence_class"] == "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
    assert receipt["items_count"] == 0
    assert receipt["safe_item_labels"] == []
    assert receipt["denial_reason"] == "wrong_route_audience"
    assert receipt["auth_status_code"] == 403
    assert receipt["partial"] is True
    assert receipt["degraded"] is True
    assert receipt["max_operation_count"] == 1
    assert receipt["retry_operation_count"] == 1
    assert receipt["second_retry_performed"] is False
    assert receipt["report_safe_metadata_only"] is True
    assert receipt["denial_before_read_required"] is True
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6ap02_receipt_report_safe(receipt)


def test_receipt_rejects_raw_private_source_query_items_and_unexpected_fields() -> None:
    forbidden = {
        "text",
        "content",
        "raw_text",
        "raw_content",
        "raw_item_text",
        "raw_source_text",
        "source_uri",
        "source_path",
        "private_path",
        "platform_raw_id",
        "credential_value",
        "auth_payload",
        "token",
        "provider_payload",
        "callback_payload",
        "runtime_registry_payload",
        "query",
        "query_text",
        "items",
        "source_labels",
    }
    assert forbidden.isdisjoint(L6AP02_REPORT_SAFE_OUTPUT_FIELDS)

    unsafe = build_l6ap02_safe_denial_receipt() | {"raw_item_text": "forbidden"}
    try:
        assert_l6ap02_receipt_report_safe(unsafe)
    except AssertionError as exc:
        assert "unsafe L6AP.02 report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe raw report field should fail closed")

    unexpected = build_l6ap02_safe_denial_receipt() | {"query_text": "forbidden echo"}
    try:
        assert_l6ap02_receipt_report_safe(unexpected)
    except AssertionError as exc:
        assert "unsafe L6AP.02 report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unexpected query echo should fail closed")


def test_doc_names_retry_result_blocker_and_no_second_retry() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AP.02 supervised metadata retry safe-denial receipt",
        f"Status: `{L6AP02_STATUS}`",
        "Rail issue: #391",
        "Parent issue: #6",
        "Rail starting source floor: `35046efe4880145d929bbe0ddb00196b83c9cc04`",
        "endpoint | `memory_seam_recall`",
        "route audience | `memory-seam:read:recall`",
        "agent | `sax`",
        "scope | `wiki`",
        "n | `3`",
        "query label | `supervised_metadata_readiness`",
        "evidence class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`",
        "denial | `wrong_route_audience`; `auth_status_code=403`",
        "items | `0`; safe item labels `[]`",
        L6AP02_BLOCKER_CLASSIFICATION,
        "No second retry was performed.",
        "No raw item text/content, source URI/path, private path, auth material, provider payload, callback payload, Runtime Registry payload, or query text was recorded.",
        "python -m pytest -q tests/test_l6ap02_metadata_retry_safe_denial_receipt.py",
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
        "platform-raw-id value",
        "private-correlation-ref value",
        "allowed=true",
    ):
        assert forbidden_marker not in lowered
