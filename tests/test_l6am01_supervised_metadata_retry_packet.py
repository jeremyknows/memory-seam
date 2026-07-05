from __future__ import annotations

from pathlib import Path

from memory_seam.l6am_supervised_metadata_retry_packet import (
    L6AM01_EVIDENCE_CLASS,
    L6AM01_QUERY_TEXT,
    L6AM01_REPORT_SAFE_OUTPUT_FIELDS,
    L6AM01_STATUS,
    assert_l6am01_retry_packet_report_safe,
    build_l6am01_denied_mismatch_receipt,
    build_l6am01_exact_retry_packet,
    build_l6am01_service_auth_binding_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6am01-supervised-metadata-retry-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6am01_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6am01-supervised-metadata-retry-packet.md" in docs_index
    assert "tests/test_l6am01_supervised_metadata_retry_packet.py" in inventory
    assert "L6AM.01 exact supervised metadata retry packet" in inventory
    assert L6AM01_STATUS in inventory


def test_exact_retry_packet_binds_only_the_authorized_metadata_recall() -> None:
    packet = build_l6am01_exact_retry_packet()

    assert packet.endpoint == "recall"
    assert packet.agent == "sax"
    assert packet.scope == "wiki"
    assert packet.n == 3
    assert packet.query_label == "supervised_metadata_readiness"
    assert packet.query_text == L6AM01_QUERY_TEXT
    assert packet.evidence_class == L6AM01_EVIDENCE_CLASS
    assert packet.max_operation_count == 1
    assert packet.report_safe is True
    assert packet.metadata_only is True
    assert packet.denial_before_read_required is True


def test_service_auth_binding_receipt_is_ready_but_does_not_execute_retry() -> None:
    receipt = build_l6am01_service_auth_binding_receipt()

    assert receipt["status"] == L6AM01_STATUS
    assert receipt["endpoint"] == "recall"
    assert receipt["auth_ready_for_one_attempt"] is True
    assert receipt["retry_executed"] is False
    assert receipt["required_tool_call"] == {
        "tool": "memory_seam_recall",
        "agent": "sax",
        "scope": "wiki",
        "n": 3,
        "query": L6AM01_QUERY_TEXT,
    }
    assert receipt["guarded_counters"]
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6am01_retry_packet_report_safe(receipt)


def test_denied_mismatch_case_denies_before_read_with_zero_counters() -> None:
    receipt = build_l6am01_denied_mismatch_receipt("wrong_route_audience")

    assert receipt["status"] == "DENIED_BEFORE_READ_OUT_OF_SCOPE_MISMATCH"
    assert receipt["auth_status"] == "denied_before_read"
    assert receipt["denial_reason"] == "wrong_route_audience"
    assert receipt["retry_executed"] is False
    assert receipt["items"] == []
    assert all(value == 0 for value in receipt["guarded_counters"].values())

    narrowing = build_l6am01_denied_mismatch_receipt("unauthorized_narrowing")
    assert narrowing["denial_reason"] == "unauthorized_narrowing"
    assert narrowing["items"] == []
    assert all(value == 0 for value in narrowing["guarded_counters"].values())


def test_report_safe_output_envelope_rejects_raw_private_source_and_auth_fields() -> None:
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

    assert forbidden.isdisjoint(L6AM01_REPORT_SAFE_OUTPUT_FIELDS)

    unsafe = build_l6am01_service_auth_binding_receipt() | {"raw_item_text": "forbidden"}
    try:
        assert_l6am01_retry_packet_report_safe(unsafe)
    except AssertionError as exc:
        assert "unsafe report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe raw report field should fail closed")


def test_doc_names_packet_denial_case_stop_conditions_and_residual_holds() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AM.01 exact supervised metadata retry packet from service-auth floor",
        f"Status: `{L6AM01_STATUS}`",
        "Rail issue: #357",
        "Parent issue: #6",
        "Rail starting source floor: `9ea7cd0ab724292b8a2841c9e2c080f14a524ee2`",
        "endpoint | `recall` / `memory_seam_recall`",
        "agent | `sax`",
        "scope | `wiki`",
        "n | `3`",
        "query label | `supervised_metadata_readiness`",
        L6AM01_QUERY_TEXT,
        "max operation count | `1`",
        "No other recall, index, source discovery",
        "Report-safe output envelope for #358",
        "safe source/evidence labels if present",
        "must not quote raw item text",
        "Required denied-before-read mismatch case",
        "`DENIED_BEFORE_READ_OUT_OF_SCOPE_MISMATCH`",
        "`denial_reason=wrong_route_audience`",
        "all guarded counters zero",
        "no broad `allowed=true` behavior",
    ):
        assert term in text

    for command in (
        "python -m pytest -q tests/test_l6am01_supervised_metadata_retry_packet.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert command in text

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
