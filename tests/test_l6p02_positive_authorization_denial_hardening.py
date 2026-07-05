from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from memory_seam.positive_authorization_receipt import (
    L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS,
    L6_POSITIVE_AUTHORIZATION_FORBIDDEN_REQUEST_FLAGS,
    L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS,
    L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
    PositiveAuthorizationCallbackHarness,
    build_l6_positive_authorization_approval_context_fixture,
    run_positive_authorization_receipt_skeleton,
    validate_l6_positive_authorization_approval_context,
    validate_l6_positive_authorization_receipt_result,
)

COPIED_L6I13_TEMPLATE_DIGEST = "1" * 64
COPIED_ISSUE_137_APPROVAL_REF = "issue-137-comment-4643939613"


def assert_denied_before_callbacks(result: Mapping[str, Any], harness: PositiveAuthorizationCallbackHarness) -> None:
    assert result["status"] == L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS
    assert result["recognized_positive_authorization"] is False
    assert result["allowed"] is False
    assert result["mutation_attempted"] is False
    assert result["mutation_supported"] is False
    assert result["denied_before_callback"] is True
    assert result["callbacks_invoked"] is False
    assert result["fixture_is_persistent"] is False
    assert result["positive_authorization_receipt_metadata"] is None
    assert result["counters"] == {counter: 0 for counter in L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS}
    assert harness.counters == result["counters"]


def deny_case(mutated_context: dict[str, Any] | None) -> dict[str, Any]:
    harness = PositiveAuthorizationCallbackHarness.build()
    result = run_positive_authorization_receipt_skeleton(
        L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
        harness=harness,
        approval_context=mutated_context,
    )
    assert_denied_before_callbacks(result, harness)
    assert validate_l6_positive_authorization_receipt_result(dict(result)) == []
    return result


def test_l6p02_required_negative_matrix_denies_before_receipt_recognition():
    base = build_l6_positive_authorization_approval_context_fixture()
    cases: dict[str, tuple[dict[str, Any] | None, str]] = {
        "stale_approval_window": ({**base, "approval_created_at": "2026-06-06T23:48:01Z"}, "stale_or_broadened_approval_window"),
        "copied_issue_137_approval": ({**base, "approval_ref": COPIED_ISSUE_137_APPROVAL_REF}, "mismatched_approval_ref"),
        "copied_l6i13_template_without_fresh_event": (
            {**base, "approval_phrase_sha256": COPIED_L6I13_TEMPLATE_DIGEST, "approval_ref": "l6i13-template-no-fresh-event"},
            "mismatched_approval_ref",
        ),
        "issue_mismatch": ({**base, "approval_issue": 164}, "mismatched_approval_issue"),
        "actor_mismatch": ({**base, "implementation_actor_role": "not-sax"}, "mismatched_implementation_actor_role"),
        "subject_mismatch": ({**base, "approval_subject": "broadened-write-authorization"}, "mismatched_approval_subject"),
        "owner_scope_mismatch": ({**base, "approval_owner_scope": "jeremyknows/other-repo#163"}, "mismatched_approval_owner_scope"),
        "expiry": ({**base, "evaluation_time": "2026-06-08T23:48:01Z"}, "approval_expired"),
        "over_max_operation_count": ({**base, "operation_count": 2}, "invalid_operation_count"),
        "missing_operation_class": ({key: value for key, value in base.items() if key != "operation_class"}, "missing_operation_class"),
        "storage_persistence_request": ({**base, "storage_persistence_requested": True}, "forbidden_storage_persistence_requested"),
        "callback_request": ({**base, "provider_callback_requested": True}, "forbidden_provider_callback_requested"),
        "live_private_read_request": ({**base, "live_private_read_requested": True}, "forbidden_live_private_read_requested"),
        "activation_publication_gate_request": (
            {**base, "service_listener_startup_cron_activation_requested": True, "publication_requested": True, "atlas_gate_movement_requested": True},
            "forbidden_service_listener_startup_cron_activation_requested",
        ),
    }

    for name, (context, expected_code) in cases.items():
        result = deny_case(context)
        denial_codes = result["approval_denial_codes"]
        assert expected_code in denial_codes, name
        assert context is not None
        assert validate_l6_positive_authorization_approval_context(context) == denial_codes, name


def test_l6p02_every_forbidden_callback_and_authority_request_flag_denies_before_callbacks():
    base = build_l6_positive_authorization_approval_context_fixture()

    for request_flag in L6_POSITIVE_AUTHORIZATION_FORBIDDEN_REQUEST_FLAGS:
        context = deepcopy(base)
        context[request_flag] = True
        result = deny_case(context)
        assert f"forbidden_{request_flag}" in result["approval_denial_codes"], request_flag


def test_l6p02_negative_matrix_never_leaks_raw_or_private_approval_material():
    base = build_l6_positive_authorization_approval_context_fixture()
    context = {**base, "approval_ref": COPIED_ISSUE_137_APPROVAL_REF, "raw_payload_content_included": True}

    result = deny_case(context)
    report_text = repr(result)

    assert "I approve Memory Seam" not in report_text
    assert "This approval expires 24 hours after this comment" not in report_text
    assert "raw-secret-token" not in report_text
    assert "credential-material" not in report_text
    assert "private-correlation-ref" not in report_text
    assert "unsafe_raw_payload_content_included" in result["approval_denial_codes"]
