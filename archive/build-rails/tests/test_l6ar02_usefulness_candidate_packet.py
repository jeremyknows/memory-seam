from __future__ import annotations

from pathlib import Path

from memory_seam.l6ar_post_auth_usefulness_rail import (
    L6AR02_HELD_STATUS,
    L6AR02_STATUS,
    assert_l6ar02_report_safe,
    build_l6ar02_usefulness_candidate_packet,
    evaluate_l6ar02_usefulness_candidate,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ar02-report-safe-usefulness-candidate-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ar02_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ar02-report-safe-usefulness-candidate-packet.md" in docs_index
    assert "tests/test_l6ar02_usefulness_candidate_packet.py" in inventory
    assert "L6AR.02 report-safe usefulness query/source-card candidate packet" in inventory
    assert L6AR02_STATUS in inventory


def test_usefulness_candidate_packet_is_report_safe_and_no_read() -> None:
    receipt = build_l6ar02_usefulness_candidate_packet()

    assert receipt["status"] == L6AR02_STATUS
    assert receipt["parent_issue"] == 6
    assert receipt["rail_issue"] == 411
    assert receipt["rail_starting_source_floor"] == "67b5bcc1019899ed3075c8bc44dcfdb9221d9c33"
    assert receipt["system_pipes_repair_floor"] == "a709b14a33b7d22ec980dba97ce20bf56a6c2d86"
    assert receipt["parent_creation_receipt"] == "4663160613"
    assert receipt["retry_executed"] is False
    assert receipt["live_private_read_executed"] is False
    assert receipt["attempt_count"] == 0
    assert receipt["second_attempt_performed"] is False
    assert receipt["next_issue"] == 412
    assert all(value == 0 for value in receipt["guarded_counters"].values())

    assert receipt["usefulness_candidate"] == {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "reference-agent",
        "acting_for": "reference-operator",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "usefulness_goal_label": "post_auth_metadata_usefulness_signal",
        "report_safe_metadata_only": True,
        "max_operation_count": 1,
        "fresh_process_required": True,
    }
    assert receipt["source_card_candidate"] == {
        "descriptor_candidate_label": "report_safe_metadata_descriptor_candidate",
        "source_card_candidate_label": "report_safe_metadata_usefulness_candidate",
        "expected_evidence_labels": [
            "endpoint_route_audience_alignment",
            "auth_status_label",
            "item_count_scalar",
            "safe_item_label_set",
            "degraded_flag_set",
        ],
        "raw_content_required": False,
        "source_path_or_uri_required": False,
        "private_identifier_required": False,
    }
    assert_l6ar02_report_safe(receipt)


def test_candidate_evaluator_accepts_exact_report_safe_no_read_shape() -> None:
    candidate = {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "reference-agent",
        "acting_for": "reference-operator",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "source_card_candidate_label": "report_safe_metadata_usefulness_candidate",
        "descriptor_candidate_label": "report_safe_metadata_descriptor_candidate",
        "retry_executed": False,
        "live_private_read_executed": False,
        "attempt_count": 0,
        "second_attempt_performed": False,
    }

    result = evaluate_l6ar02_usefulness_candidate(candidate)

    assert result["status"] == L6AR02_STATUS
    assert result["reasons"] == ["report_safe_candidate_ready_no_read"]
    assert result["retry_executed"] is False
    assert result["live_private_read_executed"] is False
    assert result["attempt_count"] == 0
    assert result["second_attempt_performed"] is False
    assert result["next_issue"] == 412
    assert all(value == 0 for value in result["guarded_counters"].values())


def test_candidate_evaluator_refuses_raw_live_broad_or_second_attempt_shapes() -> None:
    base = {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "reference-agent",
        "acting_for": "reference-operator",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "source_card_candidate_label": "report_safe_metadata_usefulness_candidate",
        "descriptor_candidate_label": "report_safe_metadata_descriptor_candidate",
        "retry_executed": False,
        "live_private_read_executed": False,
        "attempt_count": 0,
        "second_attempt_performed": False,
    }
    cases = [
        (base | {"route_audience": "memory-seam:read:*"}, "wrong_route_audience"),
        (base | {"scope": "all"}, "wrong_scope"),
        (base | {"retry_executed": True}, "wrong_retry_executed"),
        (base | {"live_private_read_executed": True}, "wrong_live_private_read_executed"),
        (base | {"attempt_count": 1}, "wrong_attempt_count"),
        (base | {"second_attempt_performed": True}, "wrong_second_attempt_performed"),
        (base | {"query_text": "unsafe echo"}, "forbidden_field_query_text"),
        (base | {"raw_content": "unsafe"}, "forbidden_field_raw_content"),
        (base | {"source_uri": "unsafe"}, "forbidden_field_source_uri"),
        (base | {"auth_payload": "unsafe"}, "forbidden_field_auth_payload"),
        (base | {"allowed": True}, "forbidden_field_allowed"),
        (base | {"raw_content_required": True}, "raw_content_required"),
        (base | {"source_path_or_uri_required": True}, "source_path_or_uri_required"),
        (base | {"private_identifier_required": True}, "private_identifier_required"),
        (base | {"source_discovery_requested": True}, "source_discovery_requested"),
        (base | {"broad_recall_requested": True}, "broad_recall_requested"),
        (base | {"provider_prod_requested": True}, "provider_prod_requested"),
        (base | {"write_requested": True}, "write_or_mutation_requested"),
    ]

    for candidate, expected_reason in cases:
        result = evaluate_l6ar02_usefulness_candidate(candidate)
        assert result["status"] == L6AR02_HELD_STATUS
        assert expected_reason in result["reasons"]
        assert result["retry_executed"] is False
        assert result["attempt_count"] == 0
        assert result["next_issue"] == 411


def test_report_safe_assertion_rejects_unsafe_fields_or_attempt_counts() -> None:
    unsafe = build_l6ar02_usefulness_candidate_packet() | {"query_text": "unsafe"}
    try:
        assert_l6ar02_report_safe(unsafe)
    except AssertionError as exc:
        assert "unsafe L6AR.02 report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe top-level query echo should fail closed")

    attempted = build_l6ar02_usefulness_candidate_packet() | {"attempt_count": 1}
    try:
        assert_l6ar02_report_safe(attempted)
    except AssertionError as exc:
        assert "attempt count must stay zero" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("L6AR.02 must not record an attempt")


def test_doc_names_candidate_packet_and_holds() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AR.02 report-safe usefulness query/source-card candidate packet",
        f"Status: `{L6AR02_STATUS}`",
        "Rail issue: #411",
        "Parent issue: #6",
        "Rail starting source floor: `67b5bcc1019899ed3075c8bc44dcfdb9221d9c33`",
        "Reference adapter repair floor: `a709b14a33b7d22ec980dba97ce20bf56a6c2d86`",
        "No live/private read, recall attempt, source discovery, or source-card read is executed for #411.",
        "#412 owns at most one fresh-process report-safe metadata usefulness attempt after #410 and #411 pass.",
        "report_safe_metadata_usefulness_candidate",
        "endpoint_route_audience_alignment",
        "auth_status_label",
        "item_count_scalar",
        "safe_item_label_set",
        "degraded_flag_set",
        "python -m pytest -q tests/test_l6ar02_usefulness_candidate_packet.py",
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
