from __future__ import annotations

from memory_seam.l6an_service_operator_auth_binding_packet import (
    L6AN02_DENIED_STATUS,
    L6AN02_HELD_STATUS,
    L6AN02_READY_STATUS,
    assert_l6an02_receipt_report_safe,
    build_l6an02_exact_binding_reference_fixture,
    validate_l6an02_binding_reference,
)


def assert_zero_counters(receipt: dict[str, object]) -> None:
    counters = receipt["guarded_counters"]
    assert isinstance(counters, dict)
    assert all(value == 0 for value in counters.values())


def test_l6an02_exact_reference_is_auth_binding_ready_but_retry_held() -> None:
    receipt = validate_l6an02_binding_reference(build_l6an02_exact_binding_reference_fixture())

    assert receipt["status"] == L6AN02_READY_STATUS
    assert receipt["reasons"] == ["exact_non_secret_binding_reference_present_retry_still_held"]
    assert receipt["retry_executed"] is False
    assert receipt["ready_metadata"] == {
        "operator_service_binding_ref_present": True,
        "route_audience": "memory-seam:read:recall",
        "acting_for": "sax",
        "agent": "sax",
        "scope": "wiki",
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "max_operation_count": 1,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
        "expiry_or_one_run_custody_present": True,
    }
    assert_zero_counters(receipt)
    assert_l6an02_receipt_report_safe(receipt)


def test_l6an02_missing_or_stale_reference_holds_before_read() -> None:
    for candidate in ({}, {"operator_service_binding_ref": "ref", "binding_fresh": False}):
        receipt = validate_l6an02_binding_reference(candidate)

        assert receipt["status"] == L6AN02_HELD_STATUS
        assert "missing_or_stale_operator_service_binding_ref" in receipt["reasons"]
        assert receipt["retry_executed"] is False
        assert_zero_counters(receipt)
        assert_l6an02_receipt_report_safe(receipt)


def test_l6an02_mismatched_required_labels_deny_before_read() -> None:
    variants = [
        ("route_audience", "memory-seam:read:context", "wrong_route_audience"),
        ("agent", "watson", "wrong_agent"),
        ("acting_for", "watson", "wrong_acting_for"),
        ("scope", "all", "wrong_scope"),
        ("query_label", "broad_recall", "wrong_query_label"),
        ("evidence_class", "RAW_PRIVATE_READ", "wrong_evidence_class"),
    ]

    for field, value, reason in variants:
        candidate = build_l6an02_exact_binding_reference_fixture() | {field: value}
        receipt = validate_l6an02_binding_reference(candidate)

        assert receipt["status"] == L6AN02_DENIED_STATUS
        assert reason in receipt["reasons"]
        assert receipt["retry_executed"] is False
        assert_zero_counters(receipt)
        assert_l6an02_receipt_report_safe(receipt)


def test_l6an02_raw_broad_runtime_provider_activation_requests_deny() -> None:
    forbidden = [
        ("raw_output_requested", "raw_output_requested"),
        ("broad_allowed", "broad_allowed_true"),
        ("allowed", "broad_allowed_true"),
        ("provider_callback_requested", "provider_callback_requested"),
        ("runtime_registry_requested", "runtime_registry_requested"),
        ("service_activation_requested", "service_activation_requested"),
    ]

    for flag, reason in forbidden:
        candidate = build_l6an02_exact_binding_reference_fixture() | {flag: True}
        receipt = validate_l6an02_binding_reference(candidate)

        assert receipt["status"] == L6AN02_DENIED_STATUS
        assert reason in receipt["reasons"]
        assert receipt["retry_executed"] is False
        assert_zero_counters(receipt)
        assert_l6an02_receipt_report_safe(receipt)


def test_l6an02_report_safe_assertion_rejects_retry_or_extra_fields() -> None:
    receipt = validate_l6an02_binding_reference(build_l6an02_exact_binding_reference_fixture())

    for unsafe in (receipt | {"retry_executed": True}, receipt | {"raw_binding_secret": "forbidden"}):
        try:
            assert_l6an02_receipt_report_safe(unsafe)
        except AssertionError:
            pass
        else:  # pragma: no cover - defensive guard
            raise AssertionError("unsafe L6AN.02 receipt should fail closed")
