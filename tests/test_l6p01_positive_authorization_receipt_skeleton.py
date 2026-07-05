from __future__ import annotations

from copy import deepcopy

from memory_seam.positive_authorization_receipt import (
    L6_POSITIVE_AUTHORIZATION_APPROVAL_PHRASE_SHA256,
    L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS,
    L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS,
    L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
    L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS,
    PositiveAuthorizationCallbackHarness,
    build_l6_positive_authorization_approval_context_fixture,
    run_positive_authorization_receipt_skeleton,
    validate_l6_positive_authorization_approval_context,
    validate_l6_positive_authorization_receipt_result,
)

PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
)


def assert_all_counters_zero(counters: dict[str, int]) -> None:
    assert set(counters) == set(L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS)
    assert all(value == 0 for value in counters.values())
    assert counters["allowed_result_count"] == 0
    assert counters["provider_callback_count"] == 0
    assert counters["backend_callback_count"] == 0
    assert counters["source_stat_callback_count"] == 0
    assert counters["source_read_callback_count"] == 0
    assert counters["write_callback_count"] == 0
    assert counters["custody_callback_count"] == 0
    assert counters["delete_callback_count"] == 0
    assert counters["reindex_callback_count"] == 0
    assert counters["rollback_callback_count"] == 0
    assert counters["cache_purge_callback_count"] == 0
    assert counters["persistent_receipt_count"] == 0
    assert counters["durable_write_record_count"] == 0
    assert counters["audit_persistence_count"] == 0
    assert counters["cache_mutation_count"] == 0


def test_l6p01_exact_fresh_approval_emits_nonpersistent_mutation_held_receipt():
    harness = PositiveAuthorizationCallbackHarness.build()
    approval_context = build_l6_positive_authorization_approval_context_fixture()

    result = run_positive_authorization_receipt_skeleton(
        L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
        harness=harness,
        approval_context=approval_context,
    )

    assert validate_l6_positive_authorization_approval_context(approval_context) == ()
    assert validate_l6_positive_authorization_receipt_result(result) == []
    assert result["status"] == L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS
    assert result["recognized_positive_authorization"] is True
    assert result["operation_count"] == 1
    assert result["max_operation_count"] == 1
    assert result["allowed"] is False
    assert result["mutation_attempted"] is False
    assert result["mutation_supported"] is False
    assert result["callbacks_invoked"] is False
    assert result["fixture_is_persistent"] is False
    assert_all_counters_zero(result["counters"])
    assert_all_counters_zero(harness.counters)

    receipt = result["positive_authorization_receipt_metadata"]
    assert receipt["status"] == "positive_authorization_recognized_mutation_held"
    assert receipt["allowed"] is False
    assert receipt["mutation_attempted"] is False
    assert receipt["mutation_supported"] is False
    assert receipt["fixture_is_persistent"] is False
    assert receipt["counter_summary"] == result["counters"]
    assert receipt["approval_reference_shape"]["phrase_sha256"] == L6_POSITIVE_AUTHORIZATION_APPROVAL_PHRASE_SHA256
    assert receipt["approval_reference_shape"]["raw_approval_text_included"] is False
    assert receipt["approval_reference_shape"]["raw_actor_id_included"] is False
    assert receipt["decision_packet_reference_shape"]["raw_private_text_included"] is False


def test_l6p01_stale_variant_and_broadened_approvals_deny_before_callbacks():
    base_context = build_l6_positive_authorization_approval_context_fixture()
    variants = {
        "missing_context": None,
        "variant_phrase_digest": {**base_context, "approval_phrase_sha256": "0" * 64},
        "wrong_issue": {**base_context, "approval_issue": 164},
        "copied_source": {**base_context, "approval_ref": "issue-137-comment-4643939613"},
        "broadened_operation_count": {**base_context, "operation_count": 2},
        "broadened_max_count": {**base_context, "max_operation_count": 2},
        "wrong_operation_class": {**base_context, "operation_class": "write intent"},
        "actor_mismatch": {**base_context, "implementation_actor_role": "other-agent"},
        "expired": {**base_context, "evaluation_time": "2026-06-08T23:48:01Z"},
        "open_ended_window": {**base_context, "approval_expires_at": "2026-06-09T23:48:01Z"},
        "raw_text_included": {**base_context, "raw_approval_text_included": True},
    }

    for name, approval_context in variants.items():
        harness = PositiveAuthorizationCallbackHarness.build()
        result = run_positive_authorization_receipt_skeleton(
            L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
            harness=harness,
            approval_context=approval_context,
        )

        assert result["status"] == L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS, name
        assert result["recognized_positive_authorization"] is False, name
        assert result["allowed"] is False, name
        assert result["mutation_attempted"] is False, name
        assert result["mutation_supported"] is False, name
        assert result["callbacks_invoked"] is False, name
        assert result["positive_authorization_receipt_metadata"] is None, name
        assert validate_l6_positive_authorization_receipt_result(result) == [], name
        assert_all_counters_zero(result["counters"])
        assert_all_counters_zero(harness.counters)


def test_l6p01_unsupported_operation_class_denies_before_callbacks():
    approval_context = build_l6_positive_authorization_approval_context_fixture()
    result = run_positive_authorization_receipt_skeleton(
        "L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON_AND_WRITE_EXECUTION",
        harness=PositiveAuthorizationCallbackHarness.build(),
        approval_context=approval_context,
    )

    assert result["status"] == L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS
    assert result["operation_count"] == 0
    assert result["operation_class"] == "unsupported_operation_class"
    assert result["recognized_positive_authorization"] is False
    assert result["allowed"] is False
    assert result["mutation_attempted"] is False
    assert result["mutation_supported"] is False
    assert result["callbacks_invoked"] is False
    assert result["positive_authorization_receipt_metadata"] is None
    assert validate_l6_positive_authorization_receipt_result(result) == []
    assert_all_counters_zero(result["counters"])


def test_l6p01_receipt_is_report_safe_and_nonpersistent():
    result = run_positive_authorization_receipt_skeleton(
        L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
        approval_context=build_l6_positive_authorization_approval_context_fixture(),
    )
    receipt = result["positive_authorization_receipt_metadata"]

    text = repr(receipt)
    assert "I approve Memory Seam" not in text
    assert "This approval expires 24 hours after this comment" not in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text
    for safety_field, included in receipt["report_safety"].items():
        assert included is False, safety_field
    assert receipt["fixture_is_persistent"] is False
    assert receipt["counter_summary"]["persistent_receipt_count"] == 0
    assert receipt["counter_summary"]["durable_write_record_count"] == 0
    assert receipt["counter_summary"]["audit_persistence_count"] == 0
    assert receipt["counter_summary"]["cache_mutation_count"] == 0


def test_l6p01_approval_context_validation_is_report_safe():
    context = build_l6_positive_authorization_approval_context_fixture()
    unsafe = deepcopy(context)
    unsafe["raw_actor_id_included"] = True

    assert validate_l6_positive_authorization_approval_context(context) == ()
    assert "unsafe_raw_actor_id_included" in validate_l6_positive_authorization_approval_context(unsafe)
    assert "I approve Memory Seam" not in repr(context)
