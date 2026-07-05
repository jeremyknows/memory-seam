from __future__ import annotations

from copy import deepcopy
from typing import Any

from memory_seam.positive_authorization_receipt import (
    L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS,
    L6_POSITIVE_AUTHORIZATION_FORBIDDEN_REPORT_INPUT_FIELDS,
    L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS,
    L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
    L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS,
    build_l6_positive_authorization_approval_context_fixture,
    run_positive_authorization_receipt_skeleton,
    validate_l6_positive_authorization_approval_context,
    validate_l6_positive_authorization_receipt_result,
)


def unsafe_report_input_attempts() -> dict[str, Any]:
    """Synthetic unsafe values built without committing live-looking secrets."""

    return {
        "raw_approval_text": "I approve Memory Seam synthetic unsafe raw approval text attempt",
        "raw_payload": {"nested": "synthetic raw payload attempt"},
        "private_path": "/".join(["", "Users", "example", "synthetic-private-path"]),
        "token_shaped_string": "".join(["gh", "p_", "syntheticTokenShapeOnly0000"]),
        "raw_platform_id": "".join(["U0", "SYNTHETICID"]),
        "private_correlation_ref": "private-correlation-ref-synthetic-attempt",
        "raw_query_payload": "raw query payload synthetic attempt",
        "raw_payload_content": "raw payload content synthetic attempt",
    }


def test_l6p03_unsafe_report_inputs_are_rejected_before_positive_receipt_output():
    base = build_l6_positive_authorization_approval_context_fixture()

    for field, value in unsafe_report_input_attempts().items():
        context = deepcopy(base)
        context[field] = value
        denial_codes = validate_l6_positive_authorization_approval_context(context)
        result = run_positive_authorization_receipt_skeleton(
            L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
            approval_context=context,
        )

        assert field in L6_POSITIVE_AUTHORIZATION_FORBIDDEN_REPORT_INPUT_FIELDS
        assert f"unsafe_report_input_{field}" in denial_codes
        assert result["status"] == L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS
        assert result["recognized_positive_authorization"] is False
        assert result["positive_authorization_receipt_metadata"] is None
        assert result["callbacks_invoked"] is False
        assert result["allowed"] is False
        assert result["mutation_attempted"] is False
        assert result["mutation_supported"] is False
        assert result["counters"] == {counter: 0 for counter in L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS}
        assert validate_l6_positive_authorization_receipt_result(result) == []


def test_l6p03_combined_unsafe_inputs_do_not_echo_values_in_report_safe_result():
    context = build_l6_positive_authorization_approval_context_fixture()
    context.update(unsafe_report_input_attempts())

    result = run_positive_authorization_receipt_skeleton(
        L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
        approval_context=context,
    )
    report_text = repr(result)

    assert result["positive_authorization_receipt_metadata"] is None
    for field in L6_POSITIVE_AUTHORIZATION_FORBIDDEN_REPORT_INPUT_FIELDS:
        assert f"unsafe_report_input_{field}" in result["approval_denial_codes"]
    for unsafe_value in unsafe_report_input_attempts().values():
        if isinstance(unsafe_value, dict):
            assert "synthetic raw payload attempt" not in report_text
        else:
            assert unsafe_value not in report_text
    assert "I approve Memory Seam synthetic unsafe raw approval text attempt" not in report_text
    assert "syntheticTokenShapeOnly0000" not in report_text
    assert "private-correlation-ref-synthetic-attempt" not in report_text
    assert result["report_safety"] == {
        "raw_approval_text_included": False,
        "raw_actor_id_included": False,
        "raw_private_text_included": False,
        "credentials_or_auth_material_included": False,
        "private_paths_included": False,
        "raw_platform_ids_included": False,
        "raw_query_payloads_included": False,
        "raw_payload_content_included": False,
        "private_correlation_refs_included": False,
    }


def test_l6p03_positive_receipt_metadata_contains_only_safe_reference_shapes():
    result = run_positive_authorization_receipt_skeleton(
        L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
        approval_context=build_l6_positive_authorization_approval_context_fixture(),
    )
    receipt = result["positive_authorization_receipt_metadata"]
    receipt_text = repr(receipt)

    assert result["status"] == L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS
    assert receipt["status"] == L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS
    assert set(receipt) == {
        "schema_version",
        "status",
        "operation_class",
        "operation_count",
        "max_operation_count",
        "allowed",
        "mutation_attempted",
        "mutation_supported",
        "fixture_is_persistent",
        "counter_summary",
        "approval_reference_shape",
        "decision_packet_reference_shape",
        "residual_holds",
        "report_safety",
    }
    assert set(receipt["approval_reference_shape"]) == {
        "kind",
        "reference",
        "issue",
        "phrase_sha256",
        "raw_approval_text_included",
        "raw_actor_id_included",
    }
    assert set(receipt["decision_packet_reference_shape"]) == {
        "kind",
        "reference",
        "raw_private_text_included",
    }
    assert receipt["allowed"] is False
    assert receipt["mutation_attempted"] is False
    assert receipt["mutation_supported"] is False
    assert receipt["fixture_is_persistent"] is False
    assert receipt["counter_summary"]["allowed_result_count"] == 0
    for unsafe_value in unsafe_report_input_attempts().values():
        if isinstance(unsafe_value, dict):
            assert "synthetic raw payload attempt" not in receipt_text
        else:
            assert unsafe_value not in receipt_text
