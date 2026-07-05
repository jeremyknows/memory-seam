from __future__ import annotations

from pathlib import Path

from memory_seam.l6ar_post_auth_usefulness_rail import (
    L6AR04_HELD_STATUS,
    L6AR04_STATUS,
    assert_l6ar04_report_safe,
    build_l6ar04_trust_boundary_review,
    evaluate_l6ar04_trust_boundary_review,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ar04-post-auth-usefulness-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ar04_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ar04-post-auth-usefulness-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ar04_trust_boundary_review.py" in inventory
    assert "L6AR.04 post-auth usefulness trust-boundary review" in inventory
    assert L6AR04_STATUS in inventory


def test_trust_boundary_review_records_pass_without_new_authority() -> None:
    receipt = build_l6ar04_trust_boundary_review()

    assert receipt["status"] == L6AR04_STATUS
    assert receipt["review_verdict"] == "PASS"
    assert receipt["parent_issue"] == 6
    assert receipt["rail_issue"] == 413
    assert receipt["rail_starting_source_floor"] == "67b5bcc1019899ed3075c8bc44dcfdb9221d9c33"
    assert receipt["system_pipes_repair_floor"] == "a709b14a33b7d22ec980dba97ce20bf56a6c2d86"
    assert receipt["parent_creation_receipt"] == "4663160613"
    assert receipt["reviewed_rail_issues"] == [410, 411, 412]
    assert receipt["reviewed_statuses"] == {
        "l6ar01": "REFERENCE_ADAPTER_RECALL_AUTHORITY_INTAKE_RELOAD_BOUNDARY_ANCHORED",
        "l6ar02": "REPORT_SAFE_USEFULNESS_QUERY_SOURCE_CARD_CANDIDATE_PACKET_READY",
        "l6ar03": "FRESH_PROCESS_METADATA_USEFULNESS_ZERO_ITEM_DEGRADED_RECEIPT_CAPTURED",
    }
    assert receipt["attempt_custody"] == {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "reference-agent",
        "acting_for": "reference-operator",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "auth_status": "tool_success",
        "degraded": True,
        "degraded_flags": ["unauthorized_narrowing"],
        "item_count": 0,
        "safe_item_labels": [],
        "attempt_count": 1,
        "second_attempt_performed": False,
        "max_operation_count": 1,
    }
    assert "zero_item_degraded_result_stops_without_second_attempt" in receipt["trust_boundary_findings"]
    assert "#412 max-one usefulness attempt is consumed and not reusable" in receipt["residual_holds"]
    assert receipt["next_issue"] == 414
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6ar04_report_safe(receipt)


def test_trust_boundary_evaluator_accepts_exact_pass_shape() -> None:
    candidate = {
        "review_verdict": "PASS",
        "reviewed_rail_issues": [410, 411, 412],
        "l6ar01_status": "REFERENCE_ADAPTER_RECALL_AUTHORITY_INTAKE_RELOAD_BOUNDARY_ANCHORED",
        "l6ar02_status": "REPORT_SAFE_USEFULNESS_QUERY_SOURCE_CARD_CANDIDATE_PACKET_READY",
        "l6ar03_status": "FRESH_PROCESS_METADATA_USEFULNESS_ZERO_ITEM_DEGRADED_RECEIPT_CAPTURED",
        "attempt_count": 1,
        "second_attempt_performed": False,
        "item_count": 0,
        "safe_item_labels": [],
    }

    result = evaluate_l6ar04_trust_boundary_review(candidate)

    assert result["status"] == L6AR04_STATUS
    assert result["review_verdict"] == "PASS"
    assert result["reasons"] == ["post_auth_usefulness_trust_boundary_passed"]
    assert result["next_issue"] == 414
    assert all(value == 0 for value in result["guarded_counters"].values())


def test_trust_boundary_evaluator_holds_unsafe_or_broadened_shapes() -> None:
    base = {
        "review_verdict": "PASS",
        "reviewed_rail_issues": [410, 411, 412],
        "l6ar01_status": "REFERENCE_ADAPTER_RECALL_AUTHORITY_INTAKE_RELOAD_BOUNDARY_ANCHORED",
        "l6ar02_status": "REPORT_SAFE_USEFULNESS_QUERY_SOURCE_CARD_CANDIDATE_PACKET_READY",
        "l6ar03_status": "FRESH_PROCESS_METADATA_USEFULNESS_ZERO_ITEM_DEGRADED_RECEIPT_CAPTURED",
        "attempt_count": 1,
        "second_attempt_performed": False,
        "item_count": 0,
        "safe_item_labels": [],
    }
    cases = [
        (base | {"review_verdict": "HOLD"}, "wrong_review_verdict"),
        (base | {"reviewed_rail_issues": [410, 411, 412, 414]}, "wrong_reviewed_rail_issues"),
        (base | {"l6ar03_status": "RAW_ITEMS_RETURNED"}, "wrong_l6ar03_status"),
        (base | {"attempt_count": 2}, "wrong_attempt_count"),
        (base | {"second_attempt_performed": True}, "wrong_second_attempt_performed"),
        (base | {"item_count": 1}, "wrong_item_count"),
        (base | {"safe_item_labels": ["unsafe"]}, "wrong_safe_item_labels"),
        (base | {"query_text": "unsafe echo"}, "forbidden_field_query_text"),
        (base | {"raw_content": "unsafe"}, "forbidden_field_raw_content"),
        (base | {"source_uri": "unsafe"}, "forbidden_field_source_uri"),
        (base | {"auth_payload": "unsafe"}, "forbidden_field_auth_payload"),
        (base | {"allowed": True}, "forbidden_field_allowed"),
        (base | {"retry_requested": True}, "retry_requested"),
        (base | {"second_attempt_requested": True}, "second_attempt_requested"),
        (base | {"source_discovery_requested": True}, "source_discovery_requested"),
        (base | {"broad_recall_requested": True}, "broad_recall_requested"),
        (base | {"provider_prod_requested": True}, "provider_prod_requested"),
        (base | {"gate_requested": True}, "gate_requested"),
        (base | {"write_requested": True}, "write_or_mutation_requested"),
    ]

    for candidate, expected_reason in cases:
        result = evaluate_l6ar04_trust_boundary_review(candidate)
        assert result["status"] == L6AR04_HELD_STATUS
        assert result["review_verdict"] == "HOLD"
        assert expected_reason in result["reasons"]
        assert result["next_issue"] == 413


def test_report_safe_assertion_rejects_unsafe_fields_or_second_attempts() -> None:
    unsafe = build_l6ar04_trust_boundary_review() | {"auth_payload": "unsafe"}
    try:
        assert_l6ar04_report_safe(unsafe)
    except AssertionError as exc:
        assert "unsafe L6AR.04 report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe top-level auth payload should fail closed")

    second = build_l6ar04_trust_boundary_review()
    second["attempt_custody"] = second["attempt_custody"] | {"attempt_count": 2}
    try:
        assert_l6ar04_report_safe(second)
    except AssertionError as exc:
        assert "consumed max-one attempt boundary" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("L6AR.04 must reject a second attempt")


def test_doc_names_pass_verdict_and_residual_holds() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AR.04 post-auth usefulness trust-boundary review",
        f"Status: `{L6AR04_STATUS}`",
        "Rail issue: #413",
        "Parent issue: #6",
        "Review verdict: `PASS`",
        "Reviewed rail issues: `#410`, `#411`, `#412`",
        "attempt count | `1`",
        "second attempt performed | `false`",
        "item count | `0`",
        "safe item labels | `[]`",
        "#412 max-one usefulness attempt is consumed and not reusable",
        "#414 source-floor parent/tracker reconciliation required before closing the rail",
        "python -m pytest -q tests/test_l6ar04_trust_boundary_review.py",
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
