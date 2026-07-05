from __future__ import annotations

from pathlib import Path

from memory_seam.l6ar_post_auth_usefulness_rail import (
    L6AR03_HELD_STATUS,
    L6AR03_STATUS,
    assert_l6ar03_report_safe,
    build_l6ar03_fresh_process_usefulness_attempt_receipt,
    evaluate_l6ar03_usefulness_attempt_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ar03-fresh-process-metadata-usefulness-attempt.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ar03_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ar03-fresh-process-metadata-usefulness-attempt.md" in docs_index
    assert "tests/test_l6ar03_fresh_process_usefulness_attempt.py" in inventory
    assert "L6AR.03 fresh-process report-safe metadata usefulness attempt" in inventory
    assert L6AR03_STATUS in inventory


def test_fresh_process_usefulness_attempt_receipt_is_report_safe() -> None:
    receipt = build_l6ar03_fresh_process_usefulness_attempt_receipt()

    assert receipt["status"] == L6AR03_STATUS
    assert receipt["parent_issue"] == 6
    assert receipt["rail_issue"] == 412
    assert receipt["rail_starting_source_floor"] == "67b5bcc1019899ed3075c8bc44dcfdb9221d9c33"
    assert receipt["system_pipes_repair_floor"] == "a709b14a33b7d22ec980dba97ce20bf56a6c2d86"
    assert receipt["parent_creation_receipt"] == "4663160613"
    assert receipt["preflight"] == {
        "l6ar01_status": "REFERENCE_ADAPTER_RECALL_AUTHORITY_INTAKE_RELOAD_BOUNDARY_ANCHORED",
        "l6ar02_status": "REPORT_SAFE_USEFULNESS_QUERY_SOURCE_CARD_CANDIDATE_PACKET_READY",
        "l6ar01_rail_issue": 410,
        "l6ar02_rail_issue": 411,
        "preflight_passed": True,
    }
    assert receipt["operation_class"] == "memory_seam_recall_report_safe_metadata_usefulness_attempt"
    assert receipt["endpoint"] == "memory_seam_recall"
    assert receipt["route_audience"] == "memory-seam:read:recall"
    assert receipt["agent"] == "reference-agent"
    assert receipt["acting_for"] == "reference-operator"
    assert receipt["scope"] == "wiki"
    assert receipt["n"] == 3
    assert receipt["query_label"] == "supervised_metadata_readiness"
    assert receipt["evidence_class"] == "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
    assert receipt["auth_status"] == "tool_success"
    assert receipt["denial_reason_label"] == "unauthorized_narrowing"
    assert receipt["degraded"] is True
    assert receipt["degraded_flags"] == ["unauthorized_narrowing"]
    assert receipt["item_count"] == 0
    assert receipt["safe_item_labels"] == []
    assert receipt["attempt_count"] == 1
    assert receipt["second_attempt_performed"] is False
    assert receipt["fresh_process_boundary"] == "reference-agent fresh adapter process via Atlas Query"
    assert receipt["report_safe_metadata_only"] is True
    assert receipt["max_operation_count"] == 1
    assert receipt["next_issue"] == 413
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6ar03_report_safe(receipt)


def test_attempt_evaluator_accepts_exact_safe_scalar_label_receipt() -> None:
    candidate = {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "reference-agent",
        "acting_for": "reference-operator",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "auth_status": "tool_success",
        "denial_reason_label": "unauthorized_narrowing",
        "degraded": True,
        "degraded_flags": ["unauthorized_narrowing"],
        "item_count": 0,
        "safe_item_labels": [],
        "attempt_count": 1,
        "second_attempt_performed": False,
        "report_safe_metadata_only": True,
        "max_operation_count": 1,
    }

    result = evaluate_l6ar03_usefulness_attempt_receipt(candidate)

    assert result["status"] == L6AR03_STATUS
    assert result["reasons"] == ["fresh_process_metadata_usefulness_zero_item_degraded_receipt_captured"]
    assert result["attempt_count"] == 1
    assert result["second_attempt_performed"] is False
    assert result["next_issue"] == 413
    assert all(value == 0 for value in result["guarded_counters"].values())


def test_attempt_evaluator_refuses_raw_broad_write_or_second_attempt_shapes() -> None:
    base = {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "reference-agent",
        "acting_for": "reference-operator",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "auth_status": "tool_success",
        "denial_reason_label": "unauthorized_narrowing",
        "degraded": True,
        "degraded_flags": ["unauthorized_narrowing"],
        "item_count": 0,
        "safe_item_labels": [],
        "attempt_count": 1,
        "second_attempt_performed": False,
        "report_safe_metadata_only": True,
        "max_operation_count": 1,
    }
    cases = [
        (base | {"route_audience": "memory-seam:read:*"}, "wrong_route_audience"),
        (base | {"scope": "all"}, "wrong_scope"),
        (base | {"auth_status": "auth_payload_echo"}, "wrong_auth_status"),
        (base | {"item_count": 1}, "wrong_item_count"),
        (base | {"safe_item_labels": ["unsafe"]}, "wrong_safe_item_labels"),
        (base | {"attempt_count": 2}, "wrong_attempt_count"),
        (base | {"second_attempt_performed": True}, "wrong_second_attempt_performed"),
        (base | {"query_text": "unsafe echo"}, "forbidden_field_query_text"),
        (base | {"items": []}, "forbidden_field_items"),
        (base | {"raw_content": "unsafe"}, "forbidden_field_raw_content"),
        (base | {"source_uri": "unsafe"}, "forbidden_field_source_uri"),
        (base | {"auth_payload": "unsafe"}, "forbidden_field_auth_payload"),
        (base | {"allowed": True}, "forbidden_field_allowed"),
        (base | {"source_discovery_requested": True}, "source_discovery_requested"),
        (base | {"broad_recall_requested": True}, "broad_recall_requested"),
        (base | {"provider_prod_requested": True}, "provider_prod_requested"),
        (base | {"gate_requested": True}, "gate_requested"),
        (base | {"write_requested": True}, "write_or_mutation_requested"),
    ]

    for candidate, expected_reason in cases:
        result = evaluate_l6ar03_usefulness_attempt_receipt(candidate)
        assert result["status"] == L6AR03_HELD_STATUS
        assert expected_reason in result["reasons"]
        assert result["attempt_count"] == 1
        assert result["second_attempt_performed"] is False
        assert result["next_issue"] == 412


def test_report_safe_assertion_rejects_unsafe_fields_or_second_attempts() -> None:
    unsafe = build_l6ar03_fresh_process_usefulness_attempt_receipt() | {"query_text": "unsafe"}
    try:
        assert_l6ar03_report_safe(unsafe)
    except AssertionError as exc:
        assert "unsafe L6AR.03 report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe top-level query echo should fail closed")

    second = build_l6ar03_fresh_process_usefulness_attempt_receipt() | {"attempt_count": 2}
    try:
        assert_l6ar03_report_safe(second)
    except AssertionError as exc:
        assert "exactly one attempt" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("L6AR.03 must reject second attempts")


def test_doc_names_attempt_receipt_and_holds() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AR.03 fresh-process report-safe metadata usefulness attempt receipt",
        f"Status: `{L6AR03_STATUS}`",
        "Rail issue: #412",
        "Parent issue: #6",
        "Rail starting source floor: `67b5bcc1019899ed3075c8bc44dcfdb9221d9c33`",
        "Reference adapter repair floor: `a709b14a33b7d22ec980dba97ce20bf56a6c2d86`",
        "auth status | `tool_success`",
        "denial reason label | `unauthorized_narrowing`",
        "degraded | `true`",
        "degraded flags | `[unauthorized_narrowing]`",
        "item count | `0`",
        "safe item labels | `[]`",
        "attempt count | `1`",
        "second attempt performed | `false`",
        "#413 trust-boundary review required before reconciliation",
        "python -m pytest -q tests/test_l6ar03_fresh_process_usefulness_attempt.py",
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
