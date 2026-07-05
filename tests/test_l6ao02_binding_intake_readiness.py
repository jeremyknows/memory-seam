from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from memory_seam.l6ao_auth_held_default_off_intake import (
    L6AO02_DENIED_STATUS,
    L6AO02_HELD_STATUS,
    L6AO02_READY_STATUS,
    assert_l6ao02_readiness_receipt_report_safe,
    build_l6ao02_ready_binding_intake_fixture,
    evaluate_l6ao02_binding_intake_readiness,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ao02-binding-intake-readiness-fixtures.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def assert_retry_held_and_counters_zero(receipt: dict[str, object]) -> None:
    counters = receipt["guarded_counters"]
    assert isinstance(counters, Mapping)
    assert receipt["retry_executed"] is False
    assert all(value == 0 for value in counters.values())
    assert_l6ao02_readiness_receipt_report_safe(receipt)


def test_l6ao02_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ao02-binding-intake-readiness-fixtures.md" in docs_index
    assert "tests/test_l6ao02_binding_intake_readiness.py" in inventory
    assert "L6AO.02 binding-intake readiness fixtures" in inventory
    assert L6AO02_READY_STATUS in inventory


def test_ready_fixture_matches_exact_default_off_target() -> None:
    fixture = build_l6ao02_ready_binding_intake_fixture()
    receipt = evaluate_l6ao02_binding_intake_readiness(fixture)

    assert fixture["endpoint"] == "memory_seam_recall"
    assert fixture["agent"] == "sax"
    assert fixture["scope"] == "wiki"
    assert fixture["n"] == 3
    assert fixture["max_operation_count"] == 1
    assert fixture["report_safe_metadata_only"] is True
    assert receipt["status"] == L6AO02_READY_STATUS
    assert receipt["reasons"] == ["exact_default_off_binding_intake_ready_retry_still_held"]
    assert_retry_held_and_counters_zero(receipt)


def test_missing_and_stale_binding_intake_hold_before_read() -> None:
    for candidate, reason in (
        ({}, "missing_binding_intake_reference"),
        (build_l6ao02_ready_binding_intake_fixture() | {"expires_at_or_one_run_custody": "stale"}, "stale_binding_intake_reference"),
        (build_l6ao02_ready_binding_intake_fixture() | {"binding_fresh": False}, "stale_binding_intake_reference"),
    ):
        receipt = evaluate_l6ao02_binding_intake_readiness(candidate)

        assert receipt["status"] == L6AO02_HELD_STATUS
        assert reason in receipt["reasons"]
        assert_retry_held_and_counters_zero(receipt)


def test_wrong_target_fields_deny_before_read() -> None:
    cases = (
        ("route_audience", "memory-seam:wrong-audience", "wrong_route_audience"),
        ("agent", "not-sax", "wrong_agent"),
        ("scope", "all", "wrong_scope"),
        ("query", "broadened query", "wrong_query"),
        ("query_label", "broad_recall", "wrong_query_label"),
        ("query_text", "broadened query", "wrong_query_text"),
        ("evidence_class", "RAW_SOURCE_READ", "wrong_evidence_class"),
        ("max_operation_count", 2, "wrong_max_operation_count"),
        ("n", 4, "wrong_n"),
        ("report_safe_metadata_only", False, "wrong_report_safe_metadata_only"),
    )

    for field, value, reason in cases:
        candidate = build_l6ao02_ready_binding_intake_fixture() | {field: value}
        receipt = evaluate_l6ao02_binding_intake_readiness(candidate)

        assert receipt["status"] == L6AO02_DENIED_STATUS
        assert reason in receipt["reasons"]
        assert_retry_held_and_counters_zero(receipt)


def test_raw_output_and_broad_allowed_true_deny_before_read() -> None:
    for field in ("raw_output_requested", "raw_private_output_requested", "raw_source_output_requested"):
        receipt = evaluate_l6ao02_binding_intake_readiness(
            build_l6ao02_ready_binding_intake_fixture() | {field: True}
        )
        assert receipt["status"] == L6AO02_DENIED_STATUS
        assert receipt["reasons"] == ["raw_output_requested"]
        assert_retry_held_and_counters_zero(receipt)

    for field in ("allowed", "broad_allowed"):
        receipt = evaluate_l6ao02_binding_intake_readiness(
            build_l6ao02_ready_binding_intake_fixture() | {field: True}
        )
        assert receipt["status"] == L6AO02_DENIED_STATUS
        assert receipt["reasons"] == ["broad_allowed_true"]
        assert_retry_held_and_counters_zero(receipt)


def test_receipt_assertion_rejects_unsafe_fields_nonzero_counters_or_retry() -> None:
    receipt = evaluate_l6ao02_binding_intake_readiness(build_l6ao02_ready_binding_intake_fixture())

    for unsafe in (
        receipt | {"raw_private_source": "forbidden"},
        receipt | {"retry_executed": True},
        receipt | {"guarded_counters": receipt["guarded_counters"] | {"source_items_returned": 1}},
    ):
        try:
            assert_l6ao02_readiness_receipt_report_safe(unsafe)
        except AssertionError:
            pass
        else:  # pragma: no cover - defensive guard
            raise AssertionError("unsafe L6AO.02 readiness receipt should fail closed")


def test_doc_names_acceptance_boundaries_and_verification() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AO.02 binding-intake readiness fixtures",
        "Rail issue: #381",
        "Parent issue: #6",
        "Source floor: `57e8bd4612824ada20718e41b1eea33210fe2974`",
        L6AO02_READY_STATUS,
        L6AO02_HELD_STATUS,
        L6AO02_DENIED_STATUS,
        "memory_seam_recall",
        "agent=`sax`",
        "scope=`wiki`",
        "n=`3`",
        "max_operation_count=`1`",
        "report_safe_metadata_only=`true`",
        "retry_executed=false",
        "guarded counters remain zero",
        "missing_binding_intake_reference",
        "stale_binding_intake_reference",
        "wrong_route_audience",
        "wrong_agent",
        "wrong_scope",
        "wrong_query",
        "wrong_evidence_class",
        "wrong_max_operation_count",
        "raw_output_requested",
        "broad_allowed_true",
        "python -m pytest -q tests/test_l6ao02_binding_intake_readiness.py",
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
        "private path value",
        "raw source text",
    ):
        assert forbidden_marker not in lowered
