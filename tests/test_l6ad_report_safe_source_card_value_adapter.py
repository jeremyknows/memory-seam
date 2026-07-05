from __future__ import annotations

from memory_seam.l6ad_report_safe_source_card_value_adapter import (
    L6AE_ALLOWED_FILE_ENVELOPE,
    L6AE_DENIED_STATUS,
    L6AE_GUARDED_COUNTERS,
    L6AE_OPERATION_CLASS,
    L6AE_PASS_STATUS,
    adapt_l6ae01_report_safe_source_card_value,
    approval_denial_reasons,
    approval_matches_l6ae01,
    build_l6ae01_exact_approval_fixture,
    build_l6ae01_report_safe_fixture,
    validate_l6ae01_adapter_output,
)

FRESH_EVALUATED_AT = "2026-06-08T20:00:00Z"
EXPIRED_EVALUATED_AT = "2026-06-09T07:01:57Z"


def assert_zero_guarded_counters(receipt: dict) -> None:
    counters = receipt["guarded_counters"]
    assert set(counters) == set(L6AE_GUARDED_COUNTERS)
    assert all(value == 0 for value in counters.values())


def test_missing_approval_denies_default_off_before_adapter_action() -> None:
    receipt = adapt_l6ae01_report_safe_source_card_value(None, evaluated_at=FRESH_EVALUATED_AT)

    assert receipt["status"] == L6AE_DENIED_STATUS
    assert receipt["approval_result"] == "DENY_BEFORE_ADAPTER_ACTION"
    assert "MISSING_REQUIRED_APPROVAL_FIELDS" in receipt["denial_reasons"]
    assert receipt["allowed"] is False
    assert receipt["allowed_result_count"] == 0
    assert receipt["live_read_invoked"] is False
    assert_zero_guarded_counters(receipt)
    assert validate_l6ae01_adapter_output(receipt) == []


def test_exact_approval_fixture_returns_report_safe_value_metadata_only() -> None:
    approval = build_l6ae01_exact_approval_fixture()
    fixture = build_l6ae01_report_safe_fixture()

    receipt = adapt_l6ae01_report_safe_source_card_value(
        approval,
        fixture,
        evaluated_at=FRESH_EVALUATED_AT,
    )

    assert receipt["status"] == L6AE_PASS_STATUS
    assert receipt["approval_result"] == "EXACT_ISSUE_BOUND_OWNER_APPROVAL_MATCH_FIXTURE_ONLY"
    assert receipt["denial_reasons"] == []
    assert receipt["allowed"] == "EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER"
    assert receipt["allowed"] is not True
    assert receipt["allowed_result_count"] == 1
    assert receipt["fixture_only"] is True
    assert receipt["default_off"] is True
    assert receipt["report_safe"] is True
    assert receipt["metadata_only"] is True
    assert receipt["live_read_invoked"] is False
    assert receipt["descriptor_ref"] == fixture["descriptor_ref"]
    assert receipt["source_card_ref"] == fixture["source_card_ref"]
    assert receipt["usefulness_label"] == fixture["usefulness_label"]
    assert_zero_guarded_counters(receipt)
    assert validate_l6ae01_adapter_output(receipt) == []


def test_approval_contract_is_exact_issue_bound_owner_fresh_and_single_slice() -> None:
    approval = build_l6ae01_exact_approval_fixture()
    assert approval_matches_l6ae01(approval, evaluated_at=FRESH_EVALUATED_AT)

    variants = [
        {"source_floor": "f606ed18737d057f0b544503c2532935a9d6c258"},
        {"issue_number": 273},
        {"approval_comment_id": "4651958732"},
        {"repository": "example/other"},
        {"actor_association": "MEMBER"},
        {"operation_class": "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ"},
        {"approved_file_envelope": [*L6AE_ALLOWED_FILE_ENVELOPE, "src/memory_seam/runtime.py"]},
        {"max_slices": 2},
        {"expires_at": "2026-06-08T19:00:00Z"},
    ]
    for patch in variants:
        candidate = approval | patch
        receipt = adapt_l6ae01_report_safe_source_card_value(
            candidate,
            evaluated_at=FRESH_EVALUATED_AT,
        )
        assert receipt["status"] == L6AE_DENIED_STATUS
        assert receipt["allowed"] is False
        assert receipt["allowed_result_count"] == 0
        assert_zero_guarded_counters(receipt)
        assert validate_l6ae01_adapter_output(receipt) == []


def test_expired_approval_denies_even_when_every_other_field_matches() -> None:
    approval = build_l6ae01_exact_approval_fixture()

    reasons = approval_denial_reasons(approval, evaluated_at=EXPIRED_EVALUATED_AT)
    receipt = adapt_l6ae01_report_safe_source_card_value(
        approval,
        evaluated_at=EXPIRED_EVALUATED_AT,
    )

    assert "APPROVAL_EXPIRED" in reasons
    assert receipt["status"] == L6AE_DENIED_STATUS
    assert "APPROVAL_EXPIRED" in receipt["denial_reasons"]
    assert receipt["allowed"] is False
    assert_zero_guarded_counters(receipt)


def test_held_surface_or_broad_allow_request_denies_before_action() -> None:
    approval = build_l6ae01_exact_approval_fixture()
    held_surface_fields = [
        "live_private_reads_authorized",
        "raw_private_content_authorized",
        "additional_source_card_reads_authorized",
        "credentials_or_auth_reads_authorized",
        "source_discovery_authorized",
        "runtime_registry_authorized",
        "callbacks_authorized",
        "persistence_or_mutation_authorized",
        "activation_authorized",
        "cron_changes_authorized",
        "publication_or_visibility_authorized",
        "provider_prod_canary_or_gate_movement_authorized",
        "atlas_gate_movement_authorized",
        "broad_allowed_true_authorized",
    ]

    for field in held_surface_fields:
        receipt = adapt_l6ae01_report_safe_source_card_value(
            approval | {field: True},
            evaluated_at=FRESH_EVALUATED_AT,
        )
        assert receipt["status"] == L6AE_DENIED_STATUS
        assert "HELD_SURFACE_AUTHORIZATION_REQUESTED" in receipt["denial_reasons"]
        assert receipt["allowed"] is False
        assert_zero_guarded_counters(receipt)
        assert validate_l6ae01_adapter_output(receipt) == []


def test_unsafe_fixture_fields_and_echoes_are_rejected_without_echo() -> None:
    approval = build_l6ae01_exact_approval_fixture()
    unsafe_fixture = build_l6ae01_report_safe_fixture() | {
        "raw_source_text": "raw private source text",
        "credential_value": "credential value",
        "prompt_payload": "raw prompt",
    }

    receipt = adapt_l6ae01_report_safe_source_card_value(
        approval,
        unsafe_fixture,
        evaluated_at=FRESH_EVALUATED_AT,
    )

    assert receipt["status"] == L6AE_DENIED_STATUS
    assert "UNSAFE_OR_NON_FIXTURE_INPUT_REJECTED" in receipt["denial_reasons"]
    rendered = repr(receipt).lower()
    assert "raw private source text" not in rendered
    assert "credential value" not in rendered
    assert "raw prompt" not in rendered
    assert receipt["allowed"] is False
    assert_zero_guarded_counters(receipt)
    assert validate_l6ae01_adapter_output(receipt) == []


def test_output_validator_rejects_broad_allowed_true_and_nonzero_side_effects() -> None:
    approval = build_l6ae01_exact_approval_fixture()
    receipt = adapt_l6ae01_report_safe_source_card_value(
        approval,
        evaluated_at=FRESH_EVALUATED_AT,
    )

    assert "broad_allowed_true" in validate_l6ae01_adapter_output(receipt | {"allowed": True})
    bad_counters = receipt["guarded_counters"] | {"source_read_callbacks": 1}
    assert "guarded_counter_nonzero" in validate_l6ae01_adapter_output(
        receipt | {"guarded_counters": bad_counters}
    )


def test_allowed_file_envelope_stays_inside_issue_281_boundaries() -> None:
    assert L6AE_ALLOWED_FILE_ENVELOPE == (
        "src/memory_seam/l6ad_report_safe_source_card_value_adapter.py",
        "src/memory_seam/__init__.py",
        "tests/test_l6ad_report_safe_source_card_value_adapter.py",
        "docs/l6ae-default-off-adapter-implementation-receipt.md",
        "docs/README.md",
        "docs/contract-test-inventory.md",
    )
