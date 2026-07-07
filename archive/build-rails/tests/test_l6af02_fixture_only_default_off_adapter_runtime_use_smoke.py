from __future__ import annotations

from pathlib import Path

from memory_seam.l6ad_report_safe_source_card_value_adapter import (
    L6AE_DENIED_STATUS,
    L6AE_GUARDED_COUNTERS,
    L6AE_PASS_STATUS,
    adapt_l6ae01_report_safe_source_card_value,
    build_l6ae01_exact_approval_fixture,
    build_l6ae01_report_safe_fixture,
    validate_l6ae01_adapter_output,
)

ARTIFACT = Path("docs/l6af02-fixture-only-default-off-adapter-runtime-use-smoke.md")
EVALUATED_AT = "2026-06-08T20:54:57Z"
L6AF_OPERATION_CLASS = "L6AF_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE"
L6AF_APPROVAL_COMMENT_ID = "4653350823"


def _assert_zero_guarded_counters(receipt: dict) -> None:
    counters = receipt["guarded_counters"]
    assert set(counters) == set(L6AE_GUARDED_COUNTERS)
    assert all(value == 0 for value in counters.values())


def test_l6af02_single_fixture_only_runtime_use_smoke_receipt() -> None:
    missing_approval_receipt = adapt_l6ae01_report_safe_source_card_value(
        None,
        evaluated_at=EVALUATED_AT,
    )
    exact_fixture_receipt = adapt_l6ae01_report_safe_source_card_value(
        build_l6ae01_exact_approval_fixture(),
        build_l6ae01_report_safe_fixture(),
        evaluated_at=EVALUATED_AT,
    )

    assert missing_approval_receipt["status"] == L6AE_DENIED_STATUS
    assert missing_approval_receipt["approval_result"] == "DENY_BEFORE_ADAPTER_ACTION"
    assert "MISSING_REQUIRED_APPROVAL_FIELDS" in missing_approval_receipt["denial_reasons"]
    assert missing_approval_receipt["allowed"] is False
    assert missing_approval_receipt["allowed_result_count"] == 0
    assert missing_approval_receipt["live_read_invoked"] is False
    _assert_zero_guarded_counters(missing_approval_receipt)
    assert validate_l6ae01_adapter_output(missing_approval_receipt) == []

    assert exact_fixture_receipt["status"] == L6AE_PASS_STATUS
    assert exact_fixture_receipt["approval_result"] == "EXACT_ISSUE_BOUND_OWNER_APPROVAL_MATCH_FIXTURE_ONLY"
    assert exact_fixture_receipt["denial_reasons"] == []
    assert exact_fixture_receipt["allowed"] == "EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER"
    assert exact_fixture_receipt["allowed"] is not True
    assert exact_fixture_receipt["allowed_result_count"] == 1
    assert exact_fixture_receipt["fixture_only"] is True
    assert exact_fixture_receipt["default_off"] is True
    assert exact_fixture_receipt["report_safe"] is True
    assert exact_fixture_receipt["metadata_only"] is True
    assert exact_fixture_receipt["live_read_invoked"] is False
    _assert_zero_guarded_counters(exact_fixture_receipt)
    assert validate_l6ae01_adapter_output(exact_fixture_receipt) == []


def test_l6af02_receipt_artifact_is_report_safe_and_issue_bound() -> None:
    text = ARTIFACT.read_text()

    required = [
        "PASS_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE",
        "Rail issue: #292",
        "Parent issue: #6",
        f"Operation class: `{L6AF_OPERATION_CLASS}`",
        f"Runtime-use approval comment: `{L6AF_APPROVAL_COMMENT_ID}`",
        "Target adapter module: `src/memory_seam/l6ad_report_safe_source_card_value_adapter.py`",
        "missing approval denial status | `DENIED_DEFAULT_OFF`",
        "exact fixture positive status | `PASS_REPORT_SAFE_VALUE_ADAPTER_FIXTURE_ONLY`",
        "allowed label | `EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER`",
        "broad `allowed=true` | `false`",
        "guarded counters | all zero",
        "live/private reads invoked | `false`",
        "Runtime Registry consumed | `false`",
        "callbacks invoked | `false`",
        "persistence or mutation invoked | `false`",
        "service/listener/startup/global activation invoked | `false`",
        "provider/prod/canary/Gate movement invoked | `false`",
        "Atlas Gate movement invoked | `false`",
    ]
    for marker in required:
        assert marker in text

    forbidden_markers = [
        "credential value",
        "oauth token",
        "keychain material",
        "auth-file material",
        "source://",
        "platform-raw-id",
        "private absolute path",
        "raw prompt",
        "raw query",
        "backend response",
    ]
    lowered = text.lower()
    for marker in forbidden_markers:
        assert marker not in lowered
