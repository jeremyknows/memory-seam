from __future__ import annotations

from pathlib import Path

from memory_seam.l6ar_post_auth_usefulness_rail import (
    L6AR01_FRESH_STDIO_AUTH_STATE,
    L6AR01_HELD_STATUS,
    L6AR01_RELOAD_BOUNDARY,
    L6AR01_STALE_CACHE_STATE,
    L6AR01_STATUS,
    assert_l6ar01_report_safe,
    build_l6ar01_recall_authority_intake,
    evaluate_l6ar01_reload_boundary,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ar01-reference-adapter-recall-authority-intake.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ar01_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ar01-reference-adapter-recall-authority-intake.md" in docs_index
    assert "tests/test_l6ar01_recall_authority_intake.py" in inventory
    assert "L6AR.01 reference adapter recall-authority intake" in inventory
    assert L6AR01_STATUS in inventory


def test_recall_authority_intake_records_reload_boundary_without_attempt() -> None:
    receipt = build_l6ar01_recall_authority_intake()

    assert receipt["status"] == L6AR01_STATUS
    assert receipt["parent_issue"] == 6
    assert receipt["rail_issue"] == 410
    assert receipt["rail_starting_source_floor"] == "67b5bcc1019899ed3075c8bc44dcfdb9221d9c33"
    assert receipt["system_pipes_repair_floor"] == "a709b14a33b7d22ec980dba97ce20bf56a6c2d86"
    assert receipt["parent_creation_receipt"] == "4663160613"
    assert receipt["fresh_stdio_auth_state"] == L6AR01_FRESH_STDIO_AUTH_STATE
    assert receipt["stale_cache_state"] == L6AR01_STALE_CACHE_STATE
    assert receipt["reload_boundary"] == L6AR01_RELOAD_BOUNDARY
    assert receipt["retry_executed"] is False
    assert receipt["attempt_count"] == 0
    assert receipt["second_attempt_performed"] is False
    assert receipt["next_issue"] == 411
    assert all(value == 0 for value in receipt["guarded_counters"].values())

    target = receipt["recall_target"]
    assert target == {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "reference-agent",
        "acting_for": "reference-operator",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "report_safe_metadata_only": True,
        "max_operation_count": 1,
    }
    assert_l6ar01_report_safe(receipt)


def test_reload_boundary_evaluator_accepts_only_report_safe_no_attempt_shape() -> None:
    candidate = {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "reference-agent",
        "acting_for": "reference-operator",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "fresh_stdio_auth_state": L6AR01_FRESH_STDIO_AUTH_STATE,
        "stale_cache_state": L6AR01_STALE_CACHE_STATE,
        "retry_executed": False,
        "attempt_count": 0,
        "second_attempt_performed": False,
    }

    result = evaluate_l6ar01_reload_boundary(candidate)

    assert result["status"] == L6AR01_STATUS
    assert result["reasons"] == ["reload_boundary_anchored_no_attempt"]
    assert result["retry_executed"] is False
    assert result["attempt_count"] == 0
    assert result["second_attempt_performed"] is False
    assert result["next_issue"] == 411
    assert all(value == 0 for value in result["guarded_counters"].values())


def test_reload_boundary_evaluator_refuses_live_raw_broad_or_second_attempt_shapes() -> None:
    base = {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "reference-agent",
        "acting_for": "reference-operator",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "fresh_stdio_auth_state": L6AR01_FRESH_STDIO_AUTH_STATE,
        "stale_cache_state": L6AR01_STALE_CACHE_STATE,
        "retry_executed": False,
        "attempt_count": 0,
        "second_attempt_performed": False,
    }
    cases = [
        (base | {"route_audience": "memory-seam:read:*"}, "wrong_route_audience"),
        (base | {"scope": "all"}, "wrong_scope"),
        (base | {"retry_executed": True}, "wrong_retry_executed"),
        (base | {"attempt_count": 1}, "wrong_attempt_count"),
        (base | {"second_attempt_performed": True}, "wrong_second_attempt_performed"),
        (base | {"query_text": "unsafe echo"}, "forbidden_field_query_text"),
        (base | {"raw_content": "unsafe"}, "forbidden_field_raw_content"),
        (base | {"source_uri": "unsafe"}, "forbidden_field_source_uri"),
        (base | {"auth_payload": "unsafe"}, "forbidden_field_auth_payload"),
        (base | {"allowed": True}, "forbidden_field_allowed"),
        (base | {"source_discovery_requested": True}, "source_discovery_requested"),
        (base | {"broad_recall_requested": True}, "broad_recall_requested"),
        (base | {"provider_prod_requested": True}, "provider_prod_requested"),
        (base | {"write_requested": True}, "write_or_mutation_requested"),
    ]

    for candidate, expected_reason in cases:
        result = evaluate_l6ar01_reload_boundary(candidate)
        assert result["status"] == L6AR01_HELD_STATUS
        assert expected_reason in result["reasons"]
        assert result["retry_executed"] is False
        assert result["attempt_count"] == 0
        assert result["next_issue"] == 410


def test_report_safe_assertion_rejects_unsafe_fields_or_attempt_counts() -> None:
    unsafe = build_l6ar01_recall_authority_intake() | {"query_text": "unsafe"}
    try:
        assert_l6ar01_report_safe(unsafe)
    except AssertionError as exc:
        assert "unsafe L6AR.01 report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe top-level query echo should fail closed")

    attempted = build_l6ar01_recall_authority_intake() | {"attempt_count": 1}
    try:
        assert_l6ar01_report_safe(attempted)
    except AssertionError as exc:
        assert "attempt count must stay zero" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("L6AR.01 must not record an attempt")


def test_doc_names_fresh_stdio_vs_stale_cache_and_holds() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AR.01 reference adapter recall-authority intake",
        f"Status: `{L6AR01_STATUS}`",
        "Rail issue: #410",
        "Parent issue: #6",
        "Rail starting source floor: `67b5bcc1019899ed3075c8bc44dcfdb9221d9c33`",
        "Reference adapter repair floor: `a709b14a33b7d22ec980dba97ce20bf56a6c2d86`",
        "fresh adapter process | `AUTH_UNBLOCKED_IN_FRESH_ADAPTER_PROCESS_AFTER_REFERENCE_REPAIR`",
        "stale client cache | `STALE_CLIENT_CACHE_NOT_RELIED_ON_FOR_RETRY_AUTHORITY`",
        "No recall/usefulness attempt was executed for #410.",
        "#412 owns at most one fresh-process report-safe metadata attempt after #410 and #411 pass.",
        "python -m pytest -q tests/test_l6ar01_recall_authority_intake.py",
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
