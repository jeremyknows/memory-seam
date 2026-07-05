from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from memory_seam.supervised_source_card_preflight import (
    L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FALSE_FLAGS,
    L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_REQUIRED_FIELDS,
    L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_UNSAFE_FIELDS,
    L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS,
    L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS,
    build_l6v_report_safe_source_card_descriptor_fixture,
    build_l6v_report_safe_source_card_descriptor_proof,
    validate_l6v_report_safe_source_card_descriptor_fixture,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
L6V_DOC = REPO_ROOT / "docs" / "l6v01-supervised-source-card-preflight.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6v03_docs_and_inventory_are_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)
    l6v_doc = normalized(L6V_DOC)

    assert "L6V.03" in docs_index
    assert "tests/test_l6v03_report_safe_source_card_descriptor_fixture.py" in inventory
    assert "report-safe source-card descriptor fixture proof" in inventory
    assert "L6V.03 report-safe source-card descriptor fixture proof" in l6v_doc


def test_l6v03_safe_descriptor_fixture_is_metadata_only_and_synthetic():
    fixture = build_l6v_report_safe_source_card_descriptor_fixture()

    for field in L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_REQUIRED_FIELDS:
        assert field in fixture
    assert fixture["descriptor_ref"] == "synthetic_descriptor:l6v-report-safe-project-doc-v1"
    assert fixture["source_card_ref"] == "synthetic_source_card:l6v-report-safe-project-doc-v1"
    assert fixture["fixture_ref"] == "committed_synthetic_fixture:l6v-report-safe-project-doc-v1"
    assert fixture["metadata_only"] is True
    assert fixture["committed_synthetic"] is True
    assert fixture["report_safe"] is True
    for flag in L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FALSE_FLAGS:
        assert fixture[flag] is False
    for unsafe_field in L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_UNSAFE_FIELDS:
        assert unsafe_field not in fixture
    assert validate_l6v_report_safe_source_card_descriptor_fixture(fixture) == ()


def test_l6v03_report_safe_descriptor_proof_contains_only_safe_refs_booleans_counters_and_status():
    proof = build_l6v_report_safe_source_card_descriptor_proof()
    text = repr(proof)

    assert proof["issue_ref"] == "#189"
    assert proof["source_floor"] == "876375b"
    assert proof["upstream_packet"] == "docs/l6u05-supervised-live-use-trust-boundary-review.md"
    assert proof["operation_class"] == L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS
    assert proof["status_detail"] == "descriptor_fixture_report_safe"
    assert proof["descriptor_valid"] is True
    assert proof["metadata_only"] is True
    assert proof["report_safe_only"] is True
    assert proof["synthetic_no_live_only"] is True
    assert proof["allowed"] is False
    assert proof["allowed_result_count"] == 0
    assert proof["allowed_true_route_present"] is False
    assert proof["callbacks_invoked"] is False
    assert proof["live_adapter_invoked"] is False
    assert proof["mutation_attempted"] is False
    assert proof["persistence_attempted"] is False
    assert proof["descriptor_denial_codes"] == ()
    assert proof["unsafe_fixture_value_echoed"] is False
    assert set(proof["counters"]) == set(L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS)
    assert all(value == 0 for value in proof["counters"].values())
    for marker in (
        "raw-secret-token",
        "credential-material",
        "operator-home-path",
        "platform-raw-id",
        "raw-query-payload",
        "raw-payload-content",
        "raw-backend-response",
        "private-correlation-ref",
        "source://",
    ):
        assert marker not in text


def test_l6v03_unsafe_descriptor_fields_fail_closed_before_report_output_without_echo():
    base = build_l6v_report_safe_source_card_descriptor_fixture()
    unsafe_cases = {
        "raw_source_content": "raw-source-content-marker",
        "private_path": "operator-home-path",
        "source_uri": "source://private/document",
        "credential_material": "credential-material",
        "auth_material": "auth-material",
        "token": "raw-secret-token",
        "raw_query_text": "raw-query-payload",
        "raw_prompt_text": "raw-prompt-text",
        "raw_payload_content": "raw-payload-content",
        "raw_backend_response": "raw-backend-response",
        "raw_platform_id": "platform-raw-id",
        "private_correlation_ref": "private-correlation-ref",
    }

    for unsafe_field, unsafe_value in unsafe_cases.items():
        fixture = deepcopy(base)
        fixture[unsafe_field] = unsafe_value
        errors = validate_l6v_report_safe_source_card_descriptor_fixture(fixture)
        proof = build_l6v_report_safe_source_card_descriptor_proof(fixture)
        public_text = repr(proof)

        assert f"unsafe_{unsafe_field}_present" in errors
        assert proof["status_detail"] == "descriptor_fixture_rejected_before_report"
        assert proof["descriptor_valid"] is False
        assert proof["metadata_only"] is False
        assert proof["allowed"] is False
        assert proof["allowed_result_count"] == 0
        assert proof["allowed_true_route_present"] is False
        assert proof["callbacks_invoked"] is False
        assert proof["live_adapter_invoked"] is False
        assert proof["unsafe_fixture_value_echoed"] is False
        assert unsafe_value not in public_text
        assert all(value == 0 for value in proof["counters"].values())


def test_l6v03_unsafe_descriptor_flags_and_mismatches_fail_closed():
    base = build_l6v_report_safe_source_card_descriptor_fixture()
    cases = []

    for flag in L6V_SUPERVISED_SOURCE_CARD_DESCRIPTOR_FALSE_FLAGS:
        fixture = deepcopy(base)
        fixture[flag] = True
        cases.append((fixture, f"unsafe_{flag}"))

    missing = deepcopy(base)
    del missing["fixture_ref"]
    cases.append((missing, "missing_fixture_ref"))

    broadened = deepcopy(base)
    broadened["scope"] = "report-safe-source-card-preflight-plus-live-read"
    cases.append((broadened, "broadened_scope"))

    for fixture, expected_code in cases:
        proof = build_l6v_report_safe_source_card_descriptor_proof(fixture)

        assert expected_code in proof["descriptor_denial_codes"]
        assert proof["descriptor_valid"] is False
        assert proof["allowed"] is False
        assert proof["callbacks_invoked"] is False
        assert proof["live_adapter_invoked"] is False
        assert all(value == 0 for value in proof["counters"].values())
