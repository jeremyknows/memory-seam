from __future__ import annotations

from pathlib import Path

from memory_seam.l6ap_metadata_retry_rail import (
    L6AP02_BLOCKER_CLASSIFICATION,
    L6AP03_DECISION,
    L6AP03_NEXT_BOUNDED_PROOF_LANE,
    L6AP03_STATUS,
    L6AP03_STEP3_STATE,
    assert_l6ap03_decision_report_safe,
    build_l6ap03_post_retry_step3_decision,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ap03-post-retry-step3-usefulness-decision.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ap03_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ap03-post-retry-step3-usefulness-decision.md" in docs_index
    assert "tests/test_l6ap03_post_retry_step3_decision.py" in inventory
    assert "L6AP.03 post-retry Step 3 usefulness decision" in inventory
    assert L6AP03_STATUS in inventory


def test_l6ap03_keeps_step3_held_after_denied_empty_retry() -> None:
    decision = build_l6ap03_post_retry_step3_decision()

    assert decision["status"] == L6AP03_STATUS
    assert decision["decision"] == L6AP03_DECISION
    assert decision["step3_state"] == L6AP03_STEP3_STATE
    assert decision["next_bounded_proof_lane"] == L6AP03_NEXT_BOUNDED_PROOF_LANE
    assert decision["precise_blocker"] == L6AP02_BLOCKER_CLASSIFICATION
    assert decision["usefulness_readiness_receipt_created"] is False
    assert decision["successor_execution_rail_created"] is False
    assert all(value == 0 for value in decision["guarded_counters"].values())
    assert_l6ap03_decision_report_safe(decision)


def test_l6ap03_consumes_only_report_safe_retry_metadata() -> None:
    decision = build_l6ap03_post_retry_step3_decision()

    assert decision["retry_result_metadata"] == {
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
        "guarded_counters": decision["retry_result_metadata"]["guarded_counters"],
    }
    assert all(value == 0 for value in decision["retry_result_metadata"]["guarded_counters"].values())


def test_l6ap03_rejects_unsafe_or_success_claiming_shapes() -> None:
    unsafe = build_l6ap03_post_retry_step3_decision() | {"query_text": "forbidden echo"}
    try:
        assert_l6ap03_decision_report_safe(unsafe)
    except AssertionError as exc:
        assert "unsafe L6AP.03 report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe query echo should fail closed")

    false_success = build_l6ap03_post_retry_step3_decision() | {
        "usefulness_readiness_receipt_created": True
    }
    try:
        assert_l6ap03_decision_report_safe(false_success)
    except AssertionError as exc:
        assert "cannot claim usefulness readiness" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("denied/empty metadata cannot become usefulness readiness")


def test_doc_names_precise_blocker_holds_and_verification() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AP.03 post-retry Step 3 usefulness decision",
        f"Status: `{L6AP03_STATUS}`",
        "Rail issue: #392",
        "Parent issue: #6",
        "Rail starting source floor: `35046efe4880145d929bbe0ddb00196b83c9cc04`",
        "L6AP.02 returned denied/empty report-safe metadata: `auth_status_code=403`, `wrong_route_audience`, `items_count=0`, safe item labels `[]`.",
        L6AP03_DECISION,
        L6AP03_STEP3_STATE,
        L6AP02_BLOCKER_CLASSIFICATION,
        "No current-session usefulness-readiness receipt was created because no safe metadata items or labels returned.",
        "No successor execution rail was created from momentum.",
        "Next bounded proof lane: `L6AP_TRUST_BOUNDARY_REVIEW_THEN_SOURCE_FLOOR_RECONCILIATION`",
        "No second retry was performed for L6AP.03.",
        "python -m pytest -q tests/test_l6ap03_post_retry_step3_decision.py",
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
