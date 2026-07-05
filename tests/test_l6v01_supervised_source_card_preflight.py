from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from memory_seam.supervised_source_card_preflight import (
    L6V_SUPERVISED_SOURCE_CARD_APPROVAL_REF,
    L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS,
    L6V_SUPERVISED_SOURCE_CARD_HELD_SURFACES,
    L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS,
    L6V_SUPERVISED_SOURCE_CARD_REQUIRED_APPROVAL_FIELDS,
    SupervisedSourceCardPreflightCallbackHarness,
    build_l6v_supervised_source_card_approval_context_fixture,
    build_l6v_supervised_source_card_denial_matrix_cases,
    build_l6v_supervised_source_card_preflight_fixture,
    parse_supervised_source_card_operation_class,
    run_l6v_supervised_source_card_preflight,
    validate_l6v_supervised_source_card_approval_context,
    validate_l6v_supervised_source_card_preflight_result,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6v01_docs_and_inventory_are_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6v01-supervised-source-card-preflight.md" in docs_index
    assert "tests/test_l6v01_supervised_source_card_preflight.py" in inventory
    assert "L6V.01 supervised source-card proof preflight skeleton" in inventory
    assert L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS in inventory


def test_l6v01_fixture_is_default_off_report_safe_and_no_live():
    fixture = build_l6v_supervised_source_card_preflight_fixture()

    assert fixture["source_floor"] == "876375b"
    assert fixture["upstream_packet"] == "docs/l6u05-supervised-live-use-trust-boundary-review.md"
    assert fixture["operation_class"] == L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS
    assert fixture["max_operation_count"] == 1
    assert fixture["default_off"] is True
    assert fixture["synthetic_no_live_only"] is True
    assert fixture["report_safe_only"] is True
    assert fixture["allowed"] is False
    assert fixture["allowed_result_count"] == 0
    assert fixture["live_adapter_invoked"] is False
    assert set(fixture["guarded_counters"]) == set(L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS)
    assert fixture["descriptor_fixture"]["metadata_only"] is True
    assert fixture["descriptor_fixture"]["raw_source_content_included"] is False
    assert fixture["descriptor_fixture"]["source_uri_included"] is False
    assert fixture["descriptor_fixture"]["private_path_included"] is False


def test_l6v01_recognizes_only_exact_issue_bound_operation_shape():
    approval = build_l6v_supervised_source_card_approval_context_fixture()

    assert parse_supervised_source_card_operation_class(L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS) == L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS
    for variant in (
        "supervised_report_safe_source_card_read_proof",
        "SUPERVISED-REPORT-SAFE-SOURCE-CARD-READ-PROOF",
        "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF_WITH_CALLBACK",
        "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF_AND_SOURCE_READ",
    ):
        assert parse_supervised_source_card_operation_class(variant) is None

    for field in L6V_SUPERVISED_SOURCE_CARD_REQUIRED_APPROVAL_FIELDS:
        assert field in approval
    assert approval["issue_ref"] == "#187"
    assert approval["approval_ref"] == L6V_SUPERVISED_SOURCE_CARD_APPROVAL_REF
    assert approval["max_operation_count"] == 1
    assert tuple(validate_l6v_supervised_source_card_approval_context(approval)) == ()


def test_l6v01_ready_preflight_emits_metadata_receipt_but_never_allowed_true():
    harness = SupervisedSourceCardPreflightCallbackHarness.build()
    approval = build_l6v_supervised_source_card_approval_context_fixture()
    result = run_l6v_supervised_source_card_preflight(approval, harness=harness)

    assert validate_l6v_supervised_source_card_preflight_result(result) == []
    assert result["preflight_ready"] is True
    assert result["status_detail"] == "ready_metadata_only_preflight"
    assert result["operation_count"] == 1
    assert result["max_operation_count"] == 1
    assert result["allowed"] is False
    assert result["allowed_result_count"] == 0
    assert result["allowed_true_route_present"] is False
    assert result["callbacks_invoked"] is False
    assert result["live_adapter_invoked"] is False
    assert result["mutation_attempted"] is False
    assert result["persistence_attempted"] is False
    assert all(value == 0 for value in result["counters"].values())
    assert all(value == 0 for value in harness.counters.values())

    receipt = result["receipt"]
    assert receipt["preflight_ready"] is True
    assert receipt["metadata_only"] is True
    assert receipt["non_persistent"] is True
    assert receipt["allowed"] is False
    assert receipt["allowed_result_count"] == 0
    assert receipt["allowed_true_route_present"] is False
    assert receipt["guarded_counters_zero"] is True


def test_l6v01_stale_variant_missing_and_broadened_approvals_hold_before_callbacks():
    base = build_l6v_supervised_source_card_approval_context_fixture()
    cases = []

    stale = deepcopy(base)
    stale["evaluation_time"] = "2026-06-08T15:28:46Z"
    cases.append((stale, "approval_expired"))

    variant = deepcopy(base)
    variant["operation_class"] = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF_AND_SOURCE_READ"
    cases.append((variant, "variant_or_mismatched_operation_class"))

    missing = deepcopy(base)
    del missing["descriptor_ref"]
    cases.append((missing, "missing_descriptor_ref"))

    broadened = deepcopy(base)
    broadened["max_operation_count"] = 2
    cases.append((broadened, "max_operation_count_not_exactly_one"))

    copied = deepcopy(base)
    copied["issue_ref"] = "#188"
    cases.append((copied, "mismatched_issue_ref"))

    for approval, expected_code in cases:
        harness = SupervisedSourceCardPreflightCallbackHarness.build()
        result = run_l6v_supervised_source_card_preflight(approval, harness=harness)
        assert expected_code in result["approval_denial_codes"]
        assert result["preflight_ready"] is False
        assert result["status_detail"] == "held_or_denied_before_callback"
        assert result["denied_or_held_before_callback"] is True
        assert result["callbacks_invoked"] is False
        assert result["live_adapter_invoked"] is False
        assert result["allowed"] is False
        assert result["allowed_result_count"] == 0
        assert all(value == 0 for value in result["counters"].values())
        assert all(value == 0 for value in harness.counters.values())
        assert validate_l6v_supervised_source_card_preflight_result(result) == []


def test_l6v02_denial_matrix_blocks_held_authority_and_unrelated_variants_before_callbacks():
    base = build_l6v_supervised_source_card_approval_context_fixture()
    matrix = {
        case["case_id"]: case["expected_code"]
        for case in build_l6v_supervised_source_card_denial_matrix_cases()
    }
    cases = []

    stale = deepcopy(base)
    stale["evaluation_time"] = "2026-06-08T15:28:46Z"
    cases.append(("stale_expired_approval", stale, matrix["stale_expired_approval"]))

    variant = deepcopy(base)
    variant["operation_class"] = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF_WITH_CALLBACK"
    cases.append(("variant_operation_class", variant, matrix["variant_operation_class"]))

    copied = deepcopy(base)
    copied["issue_ref"] = "#188"
    cases.append(("copied_wrong_issue", copied, matrix["copied_wrong_issue"]))

    unrelated_actor = deepcopy(base)
    unrelated_actor["actor_ref"] = "github-author-association:CONTRIBUTOR"
    cases.append(("unrelated_actor", unrelated_actor, matrix["unrelated_actor"]))

    mismatched_subject = deepcopy(base)
    mismatched_subject["subject_ref"] = "memory-seam:unrelated-subject"
    cases.append(("mismatched_subject", mismatched_subject, matrix["mismatched_subject"]))

    broadened_scope = deepcopy(base)
    broadened_scope["scope"] = "report-safe-source-card-preflight-plus-live-read"
    cases.append(("broadened_scope", broadened_scope, matrix["broadened_scope"]))

    broadened_stop_conditions = deepcopy(base)
    broadened_stop_conditions["stop_condition_refs"] = (*base["stop_condition_refs"], "allow-provider-callback")
    cases.append(("broadened_stop_conditions", broadened_stop_conditions, matrix["broadened_stop_conditions"]))

    for case_id, request_field, request_value in (
        ("callback_request", "requested_callback_family", "raw-callback-request"),
        ("activation_request", "requested_service_activation", "raw-listener-request"),
        ("publication_request", "requested_publication", "raw-publication-request"),
        ("provider_prod_canary_request", "requested_provider_prod_canary", "raw-prod-canary-request"),
        ("atlas_gate_request", "requested_atlas_gate_movement", "raw-gate-request"),
    ):
        approval = deepcopy(base)
        approval[request_field] = request_value
        cases.append((case_id, approval, matrix[case_id]))

    for case_id, approval, expected_code in cases:
        harness = SupervisedSourceCardPreflightCallbackHarness.build()
        result = run_l6v_supervised_source_card_preflight(approval, harness=harness)
        public_text = repr(result)

        assert expected_code in result["approval_denial_codes"], case_id
        assert result["preflight_ready"] is False
        assert result["denied_or_held_before_callback"] is True
        assert result["callbacks_invoked"] is False
        assert result["live_adapter_invoked"] is False
        assert result["allowed"] is False
        assert result["allowed_true_route_present"] is False
        assert all(value == 0 for value in result["counters"].values())
        assert all(value == 0 for value in harness.counters.values())
        assert validate_l6v_supervised_source_card_preflight_result(result) == []
        assert "raw-callback-request" not in public_text
        assert "raw-listener-request" not in public_text
        assert "raw-publication-request" not in public_text
        assert "raw-prod-canary-request" not in public_text
        assert "raw-gate-request" not in public_text


def test_l6v01_all_guarded_callback_source_credential_runtime_and_persistence_counters_zero():
    result = run_l6v_supervised_source_card_preflight(
        build_l6v_supervised_source_card_approval_context_fixture()
    )

    for counter in (
        "provider_callbacks",
        "backend_callbacks",
        "source_stat_callbacks",
        "source_read_callbacks",
        "write_callbacks",
        "custody_callbacks",
        "delete_callbacks",
        "reindex_callbacks",
        "rollback_callbacks",
        "cache_purge_callbacks",
        "credential_reads",
        "auth_reads",
        "env_reads",
        "keychain_reads",
        "oauth_reads",
        "auth_file_reads",
        "runtime_registry_consumptions",
        "source_discoveries",
        "workspace_scans",
        "family_scans",
        "broad_recall_queries",
        "index_queries",
        "live_private_reads",
        "persistence_writes",
        "audit_record_writes",
        "custody_record_writes",
        "cache_mutations",
        "service_activations",
        "publication_actions",
        "visibility_changes",
        "atlas_gate_movements",
    ):
        assert result["counters"][counter] == 0

    for surface in L6V_SUPERVISED_SOURCE_CARD_HELD_SURFACES:
        assert surface in result["held_surfaces"]


def test_l6v01_report_safety_excludes_raw_source_private_credentials_paths_and_payloads():
    result = run_l6v_supervised_source_card_preflight(
        build_l6v_supervised_source_card_approval_context_fixture()
    )
    text = repr(result)

    for key, value in result["report_safety"].items():
        assert value is False, key
    for marker in (
        "raw-secret-token",
        "credential-material",
        "operator-home-path",
        "platform-raw-id",
        "raw-query-payload",
        "raw-payload-content",
        "private-correlation-ref",
        "source://",
    ):
        assert marker not in text
