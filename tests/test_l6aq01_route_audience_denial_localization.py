from __future__ import annotations

from pathlib import Path

from memory_seam.l6aq_route_audience_repair import (
    L6AQ01_BLOCKER_CLASSIFICATION,
    L6AQ01_EXPECTED_ROUTE_AUDIENCE,
    L6AQ01_REFUSED_STATUS,
    L6AQ01_REPAIR_TARGET,
    L6AQ01_STATUS,
    assert_l6aq01_localization_report_safe,
    build_l6aq01_route_audience_denial_localization,
    evaluate_l6aq01_route_audience_localization_input,
)
from memory_seam.l6ap_metadata_retry_rail import build_l6ap02_safe_denial_receipt

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aq01-route-audience-auth-denial-localization.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aq01_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aq01-route-audience-auth-denial-localization.md" in docs_index
    assert "tests/test_l6aq01_route_audience_denial_localization.py" in inventory
    assert "L6AQ.01 route-audience auth denial localization" in inventory
    assert L6AQ01_STATUS in inventory


def test_localization_consumes_only_prior_report_safe_metadata() -> None:
    receipt = build_l6aq01_route_audience_denial_localization()

    assert receipt["status"] == L6AQ01_STATUS
    assert receipt["rail_issue"] == 400
    assert receipt["rail_starting_source_floor"] == "755ab24e4ac5a283081f134cbc18c95c59d1c60e"
    assert receipt["expected_binding"]["endpoint"] == "memory_seam_recall"
    assert receipt["expected_binding"]["route_audience"] == L6AQ01_EXPECTED_ROUTE_AUDIENCE
    assert receipt["expected_binding"]["agent"] == "sax"
    assert receipt["expected_binding"]["scope"] == "wiki"
    assert receipt["expected_binding"]["n"] == 3
    assert receipt["expected_binding"]["query_label"] == "supervised_metadata_readiness"
    assert receipt["observed_denial"] == {
        "denial_reason": "wrong_route_audience",
        "auth_status_code": 403,
        "items_count": 0,
        "safe_item_labels": [],
        "denied_before_read": True,
    }
    assert receipt["blocker_classification"] == L6AQ01_BLOCKER_CLASSIFICATION
    assert receipt["repair_target"] == L6AQ01_REPAIR_TARGET
    assert receipt["retry_executed"] is False
    assert receipt["second_retry_performed"] is False
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6aq01_localization_report_safe(receipt)

    prior = receipt["prior_retry_metadata"]
    assert prior["denial_reason"] == "wrong_route_audience"
    assert prior["auth_status_code"] == 403
    assert prior["items_count"] == 0
    assert prior["safe_item_labels"] == []
    assert "query_text" not in prior
    assert "items" not in prior
    assert "source_uri" not in prior
    assert "auth_payload" not in prior


def test_input_evaluator_accepts_exact_prior_safe_denial_metadata() -> None:
    prior = build_l6ap02_safe_denial_receipt()
    candidate = {
        "endpoint": prior["endpoint"],
        "route_audience": prior["route_audience"],
        "agent": prior["agent"],
        "scope": prior["scope"],
        "n": prior["n"],
        "query_label": prior["query_label"],
        "evidence_class": prior["evidence_class"],
        "denial_reason": prior["denial_reason"],
        "auth_status_code": prior["auth_status_code"],
        "items_count": prior["items_count"],
        "safe_item_labels": prior["safe_item_labels"],
        "report_safe_metadata_only": prior["report_safe_metadata_only"],
        "denial_before_read_required": prior["denial_before_read_required"],
        "retry_operation_count": prior["retry_operation_count"],
        "second_retry_performed": prior["second_retry_performed"],
    }

    result = evaluate_l6aq01_route_audience_localization_input(candidate)

    assert result["status"] == L6AQ01_STATUS
    assert result["reasons"] == ["report_safe_wrong_route_audience_denial_localized"]
    assert result["repair_target"] == L6AQ01_REPAIR_TARGET
    assert result["retry_executed"] is False
    assert all(value == 0 for value in result["guarded_counters"].values())


def test_input_evaluator_refuses_wrong_missing_broad_or_raw_shapes_before_read() -> None:
    prior = build_l6ap02_safe_denial_receipt()
    base = {
        "endpoint": prior["endpoint"],
        "route_audience": prior["route_audience"],
        "agent": prior["agent"],
        "scope": prior["scope"],
        "n": prior["n"],
        "query_label": prior["query_label"],
        "evidence_class": prior["evidence_class"],
        "denial_reason": prior["denial_reason"],
        "auth_status_code": prior["auth_status_code"],
        "items_count": prior["items_count"],
        "safe_item_labels": prior["safe_item_labels"],
        "report_safe_metadata_only": prior["report_safe_metadata_only"],
        "denial_before_read_required": prior["denial_before_read_required"],
        "retry_operation_count": prior["retry_operation_count"],
        "second_retry_performed": prior["second_retry_performed"],
    }

    cases = [
        (base | {"route_audience": "memory-seam:read:*"}, "wrong_route_audience"),
        (base | {"agent": "other-agent"}, "wrong_agent"),
        (base | {"scope": "all"}, "wrong_scope"),
        (base | {"denial_reason": "unauthorized_narrowing"}, "wrong_denial_reason"),
        (base | {"items_count": 1}, "wrong_items_count"),
        (base | {"safe_item_labels": ["unsafe"]}, "wrong_safe_item_labels"),
        (base | {"report_safe_metadata_only": False}, "wrong_report_safe_metadata_only"),
        (base | {"second_retry_performed": True}, "wrong_second_retry_performed"),
        (base | {"query_text": "unsafe echo"}, "forbidden_field_query_text"),
        (base | {"raw_content": "unsafe"}, "forbidden_field_raw_content"),
        (base | {"allowed": True}, "forbidden_field_allowed"),
        (base | {"source_discovery_requested": True}, "source_discovery_requested"),
        (base | {"runtime_registry_requested": True}, "runtime_registry_requested"),
        (base | {"service_activation_requested": True}, "service_activation_requested"),
        (base | {"write_requested": True}, "write_requested"),
    ]
    for candidate, expected_reason in cases:
        result = evaluate_l6aq01_route_audience_localization_input(candidate)
        assert result["status"] == L6AQ01_REFUSED_STATUS
        assert expected_reason in result["reasons"]
        assert result["repair_target"] is None
        assert result["retry_executed"] is False


def test_report_safe_assertion_rejects_unsafe_top_level_or_prior_metadata_fields() -> None:
    unsafe_top_level = build_l6aq01_route_audience_denial_localization() | {"query_text": "unsafe echo"}
    try:
        assert_l6aq01_localization_report_safe(unsafe_top_level)
    except AssertionError as exc:
        assert "unsafe L6AQ.01 report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe top-level query echo should fail closed")

    unsafe_prior = build_l6aq01_route_audience_denial_localization()
    unsafe_prior["prior_retry_metadata"] = unsafe_prior["prior_retry_metadata"] | {"source_uri": "unsafe"}
    try:
        assert_l6aq01_localization_report_safe(unsafe_prior)
    except AssertionError as exc:
        assert "unsafe prior retry metadata fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsafe prior metadata should fail closed")


def test_doc_names_blocker_repair_target_and_holds() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AQ.01 route-audience auth denial localization",
        f"Status: `{L6AQ01_STATUS}`",
        "Rail issue: #400",
        "Parent issue: #6",
        "Rail starting source floor: `755ab24e4ac5a283081f134cbc18c95c59d1c60e`",
        "endpoint | `memory_seam_recall`",
        "expected route audience | `memory-seam:read:recall`",
        "observed denial | `wrong_route_audience`; `auth_status_code=403`",
        "items | `0`; safe item labels `[]`",
        L6AQ01_BLOCKER_CLASSIFICATION,
        L6AQ01_REPAIR_TARGET,
        "No live retry was executed for this issue.",
        "No raw item text/content, source URI/path, private path, auth material, provider payload, callback payload, Runtime Registry payload, or query text was recorded.",
        "python -m pytest -q tests/test_l6aq01_route_audience_denial_localization.py",
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
