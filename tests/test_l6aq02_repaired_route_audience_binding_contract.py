from __future__ import annotations

from pathlib import Path

from memory_seam.l6aq_route_audience_repair import (
    L6AQ01_EXPECTED_ROUTE_AUDIENCE,
    L6AQ01_REPAIR_TARGET,
    L6AQ02_DENIED_STATUS,
    L6AQ02_HELD_STATUS,
    L6AQ02_READY_STATUS,
    L6AQ02_STATUS,
    assert_l6aq02_contract_report_safe,
    assert_l6aq02_validation_report_safe,
    build_l6aq02_repaired_binding_contract_fixture,
    build_l6aq02_repaired_route_audience_binding_contract,
    validate_l6aq02_repaired_binding_contract,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aq02-repaired-route-audience-binding-contract.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aq02_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aq02-repaired-route-audience-binding-contract.md" in docs_index
    assert "tests/test_l6aq02_repaired_route_audience_binding_contract.py" in inventory
    assert "L6AQ.02 repaired route-audience binding contract" in inventory
    assert L6AQ02_STATUS in inventory


def test_contract_defines_exact_repaired_binding_default_off() -> None:
    receipt = build_l6aq02_repaired_route_audience_binding_contract()

    assert receipt["status"] == L6AQ02_STATUS
    assert receipt["rail_issue"] == 401
    assert receipt["rail_starting_source_floor"] == "755ab24e4ac5a283081f134cbc18c95c59d1c60e"
    assert receipt["repair_target"] == L6AQ01_REPAIR_TARGET
    assert receipt["default_off_until"] == "issue_403_preflight_and_max_one_retry_authority_pass"
    assert receipt["retry_executed"] is False
    assert receipt["second_retry_performed"] is False
    assert all(value == 0 for value in receipt["guarded_counters"].values())

    contract = receipt["binding_contract"]
    assert contract["endpoint"] == "memory_seam_recall"
    assert contract["route_audience"] == L6AQ01_EXPECTED_ROUTE_AUDIENCE
    assert contract["acting_for"] == "sax"
    assert contract["agent"] == "sax"
    assert contract["scope"] == "wiki"
    assert contract["n"] == 3
    assert contract["query_label"] == "supervised_metadata_readiness"
    assert contract["evidence_class"] == "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
    assert contract["max_operation_count"] == 1
    assert contract["report_safe_metadata_only"] is True
    assert contract["denial_before_read_required"] is True
    assert contract["default_off_until_issue_403_preflight"] is True
    assert contract["retry_authorized_by_contract"] is False
    assert "query_text" not in contract
    assert "auth_payload" not in contract
    assert "provider_payload" not in contract
    assert "source_uri" not in contract
    assert_l6aq02_contract_report_safe(receipt)


def test_validator_accepts_exact_contract_but_keeps_retry_default_off() -> None:
    result = validate_l6aq02_repaired_binding_contract(build_l6aq02_repaired_binding_contract_fixture())

    assert result["status"] == L6AQ02_READY_STATUS
    assert result["reasons"] == ["repaired_route_audience_binding_ready_retry_still_default_off"]
    assert result["ready_metadata"]["route_audience"] == L6AQ01_EXPECTED_ROUTE_AUDIENCE
    assert result["ready_metadata"]["retry_authorized_by_contract"] is False
    assert result["retry_executed"] is False
    assert result["second_retry_performed"] is False
    assert all(value == 0 for value in result["guarded_counters"].values())
    assert_l6aq02_validation_report_safe(result)


def test_validator_refuses_missing_stale_wrong_broadened_raw_and_movement_shapes() -> None:
    base = build_l6aq02_repaired_binding_contract_fixture()
    cases = [
        ({}, L6AQ02_HELD_STATUS, "missing_binding"),
        (base | {"operator_service_binding_ref": ""}, L6AQ02_HELD_STATUS, "missing_binding"),
        (base | {"expires_at_or_one_run_custody": "stale"}, L6AQ02_HELD_STATUS, "stale_binding"),
        (base | {"binding_fresh": False}, L6AQ02_HELD_STATUS, "stale_binding"),
        (base | {"route_audience": "memory-seam:read:wrong"}, L6AQ02_DENIED_STATUS, "wrong_route_audience"),
        (base | {"route_audience": "memory-seam:read:*"}, L6AQ02_DENIED_STATUS, "broadened_audience"),
        (base | {"scope": "all"}, L6AQ02_DENIED_STATUS, "wrong_scope"),
        (base | {"n": 10}, L6AQ02_DENIED_STATUS, "wrong_n"),
        (base | {"max_operation_count": 2}, L6AQ02_DENIED_STATUS, "wrong_max_operation_count"),
        (base | {"report_safe_metadata_only": False}, L6AQ02_DENIED_STATUS, "wrong_report_safe_metadata_only"),
        (base | {"default_off_until_issue_403_preflight": False}, L6AQ02_DENIED_STATUS, "default_off_bypassed"),
        (base | {"retry_authorized_by_contract": True}, L6AQ02_DENIED_STATUS, "contract_attempted_to_authorize_retry"),
        (base | {"allowed": True}, L6AQ02_DENIED_STATUS, "broad_allowed_true"),
        (base | {"raw_output_requested": True}, L6AQ02_DENIED_STATUS, "raw_output_requested"),
        (base | {"query_text": "unsafe echo"}, L6AQ02_DENIED_STATUS, "forbidden_field_query_text"),
        (base | {"provider_prod_requested": True}, L6AQ02_DENIED_STATUS, "provider_prod_requested"),
        (base | {"canary_requested": True}, L6AQ02_DENIED_STATUS, "provider_prod_requested"),
        (base | {"gate_requested": True}, L6AQ02_DENIED_STATUS, "gate_requested"),
        (base | {"write_requested": True}, L6AQ02_DENIED_STATUS, "write_requested"),
        (base | {"runtime_registry_requested": True}, L6AQ02_DENIED_STATUS, "runtime_registry_requested"),
        (base | {"provider_callback_requested": True}, L6AQ02_DENIED_STATUS, "provider_callback_requested"),
        (base | {"service_activation_requested": True}, L6AQ02_DENIED_STATUS, "service_activation_requested"),
        (base | {"source_discovery_requested": True}, L6AQ02_DENIED_STATUS, "source_discovery_requested"),
    ]
    for candidate, expected_status, expected_reason in cases:
        result = validate_l6aq02_repaired_binding_contract(candidate)
        assert result["status"] == expected_status
        assert expected_reason in result["reasons"]
        assert result["retry_executed"] is False
        assert result["second_retry_performed"] is False
        assert_l6aq02_validation_report_safe(result)


def test_doc_names_contract_mismatch_cases_and_holds() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AQ.02 repaired route-audience binding contract",
        f"Status: `{L6AQ02_STATUS}`",
        "Rail issue: #401",
        "Parent issue: #6",
        "Rail starting source floor: `755ab24e4ac5a283081f134cbc18c95c59d1c60e`",
        "repair target | `memory_seam_recall_service_operator_route_audience_binding`",
        "endpoint | `memory_seam_recall`",
        "route audience | `memory-seam:read:recall`",
        "default-off until | `issue_403_preflight_and_max_one_retry_authority_pass`",
        "retry_authorized_by_contract | `false`",
        "wrong route audience, missing binding, stale binding, broadened audience, broad `allowed=true`, raw output, provider/prod/canary/Gate/write movement",
        "No live retry was executed for this issue.",
        "python -m pytest -q tests/test_l6aq02_repaired_route_audience_binding_contract.py",
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
        "platform-raw-id value",
        "private-correlation-ref value",
    ):
        assert forbidden_marker not in lowered
