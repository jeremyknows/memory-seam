from __future__ import annotations

from memory_seam.l6ap_metadata_retry_rail import (
    L6AP01_EVIDENCE_CLASS,
    L6AP_FRESH_APPROVAL_SOURCE,
    L6AP01_QUERY_TEXT,
    L6AP01_REFUSED_STATUS,
    L6AP01_STATUS,
    L6AP01_TARGET,
    assert_l6ap01_preflight_report_safe,
    assert_l6ap01_receipt_report_safe,
    build_l6ap01_fresh_binding_preflight_receipt,
    evaluate_l6ap01_max_one_retry_preflight,
)


def _ready_candidate() -> dict[str, object]:
    return {
        **L6AP01_TARGET,
        "fresh_approval_source": L6AP_FRESH_APPROVAL_SOURCE,
        "approval_fresh": True,
        "issue_bound_authorization": True,
        "authorization_issue": 390,
    }


def test_l6ap01_binds_fresh_approval_and_exact_retry_target_without_live_retry() -> None:
    receipt = build_l6ap01_fresh_binding_preflight_receipt()

    assert_l6ap01_receipt_report_safe(receipt)
    assert receipt["rail_starting_source_floor"] == "35046efe4880145d929bbe0ddb00196b83c9cc04"
    assert receipt["fresh_approval_source"] == L6AP_FRESH_APPROVAL_SOURCE
    assert receipt["target"] == L6AP01_TARGET
    assert receipt["target"]["endpoint"] == "memory_seam_recall"
    assert receipt["target"]["route_audience"] == "memory-seam:read:recall"
    assert receipt["target"]["agent"] == "sax"
    assert receipt["target"]["scope"] == "wiki"
    assert receipt["target"]["n"] == 3
    assert receipt["target"]["query_text"] == L6AP01_QUERY_TEXT
    assert receipt["target"]["evidence_class"] == L6AP01_EVIDENCE_CLASS
    assert receipt["target"]["max_operation_count"] == 1
    assert receipt["target"]["report_safe_metadata_only"] is True
    assert receipt["target"]["denial_before_read_required"] is True
    assert receipt["retry_authorized_for_l6ap02_only"] is True
    assert receipt["retry_executed"] is False
    assert all(value == 0 for value in receipt["guarded_counters"].values())


def test_l6ap01_ready_preflight_is_report_safe_metadata_only() -> None:
    preflight = evaluate_l6ap01_max_one_retry_preflight(_ready_candidate())

    assert_l6ap01_preflight_report_safe(preflight)
    assert preflight["status"] == L6AP01_STATUS
    assert preflight["preflight_ready"] is True
    assert preflight["retry_executed"] is False
    assert preflight["reasons"] == ["exact_fresh_issue_bound_max_one_preflight_ready"]
    assert "query_text" not in preflight["target_metadata"]


def test_l6ap01_refuses_stale_copied_broadened_or_missing_issue_authority_before_read() -> None:
    stale = evaluate_l6ap01_max_one_retry_preflight(
        {
            **_ready_candidate(),
            "fresh_approval_source": "copied-old-discord-message",
            "approval_state": "broadened",
            "issue_bound_authorization": False,
            "authorization_issue": 6,
        }
    )

    assert_l6ap01_preflight_report_safe(stale)
    assert stale["status"] == L6AP01_REFUSED_STATUS
    assert stale["preflight_ready"] is False
    assert "stale_copied_or_broadened_approval" in stale["reasons"]
    assert "missing_issue_bound_authorization" in stale["reasons"]
    assert stale["retry_executed"] is False


def test_l6ap01_refuses_raw_secret_runtime_source_write_and_broad_allowed_surfaces() -> None:
    denied = evaluate_l6ap01_max_one_retry_preflight(
        {
            **_ready_candidate(),
            "raw_output_requested": True,
            "auth_payload_requested": True,
            "credential_read_requested": True,
            "env_read_requested": True,
            "keychain_read_requested": True,
            "oauth_read_requested": True,
            "auth_file_read_requested": True,
            "runtime_registry_requested": True,
            "provider_callback_requested": True,
            "service_activation_requested": True,
            "source_discovery_requested": True,
            "broad_recall_requested": True,
            "broad_allowed": True,
            "allowed": True,
            "provider_prod_requested": True,
            "canary_requested": True,
            "gate_requested": True,
            "atlas_gate_requested": True,
            "write_requested": True,
            "mutation_requested": True,
        }
    )

    assert denied["status"] == L6AP01_REFUSED_STATUS
    assert denied["preflight_ready"] is False
    assert denied["retry_executed"] is False
    assert "raw_private_source_or_auth_output_requested" in denied["reasons"]
    assert "secret_env_keychain_oauth_auth_file_or_credential_read_requested" in denied["reasons"]
    assert "runtime_registry_provider_callback_or_service_activation_requested" in denied["reasons"]
    assert "source_discovery_broad_recall_or_broad_allowed_true_requested" in denied["reasons"]
    assert "provider_prod_canary_atlas_gate_write_or_mutation_requested" in denied["reasons"]


def test_l6ap01_refuses_wrong_target_or_second_retry_before_read() -> None:
    denied = evaluate_l6ap01_max_one_retry_preflight(
        {
            **_ready_candidate(),
            "endpoint": "memory_seam_context",
            "route_audience": "memory-seam:read:any",
            "agent": "watson",
            "scope": "all",
            "n": 10,
            "query": "different query",
            "query_label": "broad",
            "query_text": "different query",
            "evidence_class": "RAW",
            "max_operation_count": 2,
            "operation_count": 2,
            "report_safe_metadata_only": False,
            "denial_before_read_required": False,
        }
    )

    assert denied["status"] == L6AP01_REFUSED_STATUS
    assert denied["preflight_ready"] is False
    assert denied["retry_executed"] is False
    for reason in (
        "wrong_endpoint",
        "wrong_route_audience",
        "wrong_agent",
        "wrong_scope",
        "wrong_n",
        "wrong_query",
        "wrong_query_text",
        "wrong_query_label",
        "wrong_evidence_class",
        "max_operation_count_not_one",
        "report_safe_metadata_only_not_true",
        "denial_before_read_not_required",
    ):
        assert reason in denied["reasons"]
