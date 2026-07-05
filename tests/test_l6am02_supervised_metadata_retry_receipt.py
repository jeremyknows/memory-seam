from __future__ import annotations

from pathlib import Path

from memory_seam.l6am_supervised_metadata_retry_packet import L6AM01_QUERY_TEXT
from memory_seam.l6am_supervised_metadata_retry_receipt import (
    L6AM02_BLOCKER_CLASSIFICATION,
    L6AM02_DENIED_MISMATCH_STATUS,
    L6AM02_REPORT_SAFE_OUTPUT_FIELDS,
    L6AM02_STATUS,
    assert_l6am02_receipt_report_safe,
    build_l6am02_safe_denial_receipt,
    exact_l6am02_retry_binding,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6am02-supervised-metadata-retry-safe-denial-receipt.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6am02_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6am02-supervised-metadata-retry-safe-denial-receipt.md" in docs_index
    assert "tests/test_l6am02_supervised_metadata_retry_receipt.py" in inventory
    assert "L6AM.02 supervised metadata retry safe-denial receipt" in inventory
    assert L6AM02_STATUS in inventory


def test_exact_retry_binding_matches_l6am01_packet() -> None:
    assert exact_l6am02_retry_binding() == {
        "tool": "memory_seam_recall",
        "agent": "sax",
        "scope": "wiki",
        "n": 3,
        "query": L6AM01_QUERY_TEXT,
    }


def test_safe_denial_receipt_records_only_report_safe_metadata() -> None:
    receipt = build_l6am02_safe_denial_receipt()

    assert receipt["status"] == L6AM02_STATUS
    assert receipt["blocker_classification"] == L6AM02_BLOCKER_CLASSIFICATION
    assert receipt["endpoint"] == "memory_seam_recall"
    assert receipt["packet_endpoint"] == "recall"
    assert receipt["agent"] == "sax"
    assert receipt["scope_requested"] == "wiki"
    assert receipt["scope_effective"] == []
    assert receipt["n"] == 3
    assert receipt["query_label"] == "supervised_metadata_readiness"
    assert receipt["auth_status"] == "denied_before_read"
    assert receipt["auth_status_code"] == 403
    assert receipt["degraded"] is True
    assert receipt["degraded_reasons"] == ["wrong_route_audience"]
    assert receipt["partial"] is True
    assert receipt["item_count"] == 0
    assert receipt["safe_item_labels"] == []
    assert receipt["denial_before_read_mismatch_check"] == L6AM02_DENIED_MISMATCH_STATUS
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6am02_receipt_report_safe(receipt)


def test_receipt_rejects_raw_private_source_and_unexpected_fields() -> None:
    forbidden = {
        "text",
        "content",
        "raw_text",
        "raw_content",
        "raw_item_text",
        "raw_source_text",
        "source_uri",
        "private_path",
        "platform_raw_id",
        "credential_value",
        "auth_value",
        "token",
        "provider_payload",
        "callback_payload",
        "runtime_registry_payload",
    }
    assert forbidden.isdisjoint(L6AM02_REPORT_SAFE_OUTPUT_FIELDS)

    unsafe = build_l6am02_safe_denial_receipt() | {"raw_item_text": "forbidden"}
    try:
        assert_l6am02_receipt_report_safe(unsafe)
    except AssertionError as exc:
        assert "unsafe report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe raw report field should fail closed")

    unexpected = build_l6am02_safe_denial_receipt() | {"query": L6AM01_QUERY_TEXT}
    try:
        assert_l6am02_receipt_report_safe(unexpected)
    except AssertionError as exc:
        assert "unexpected report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unexpected query echo should fail closed")


def test_doc_names_retry_result_blocker_and_no_second_live_mismatch_check() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AM.02 supervised metadata retry safe-denial receipt",
        f"Status: `{L6AM02_STATUS}`",
        "Rail issue: #358",
        "Parent issue: #6",
        "Rail starting source floor: `9ea7cd0ab724292b8a2841c9e2c080f14a524ee2`",
        "endpoint | `memory_seam_recall` / packet endpoint `recall`",
        "agent | `sax`",
        "scope | requested `wiki`; effective `[]`",
        "n | `3`",
        "query label | `supervised_metadata_readiness`",
        "auth status | `denied_before_read`; `auth_status_code=403`",
        "degraded | `true`; reasons `wrong_route_audience`",
        "items | `0`; safe item labels `[]`",
        L6AM02_BLOCKER_CLASSIFICATION,
        L6AM02_DENIED_MISMATCH_STATUS,
        "No raw item text/content, source URI, private path, auth material, provider payload, callback payload, or Runtime Registry payload was recorded.",
        "No broad recall/index/source discovery was performed.",
        "python -m pytest -q tests/test_l6am02_supervised_metadata_retry_receipt.py",
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
    ):
        assert forbidden_marker not in lowered
