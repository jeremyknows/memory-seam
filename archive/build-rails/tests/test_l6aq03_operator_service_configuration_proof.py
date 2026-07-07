from __future__ import annotations

from pathlib import Path

from memory_seam.l6aq_route_audience_repair import (
    L6AQ01_EXPECTED_ROUTE_AUDIENCE,
    L6AQ03_DENIED_STATUS,
    L6AQ03_HELD_STATUS,
    L6AQ03_READY_STATUS,
    L6AQ03_STATUS,
    assert_l6aq03_configuration_proof_report_safe,
    assert_l6aq03_validation_report_safe,
    build_l6aq03_operator_service_configuration_proof,
    build_l6aq03_operator_service_configuration_proof_fixture,
    validate_l6aq03_operator_service_configuration_proof,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aq03-operator-service-configuration-proof.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aq03_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aq03-operator-service-configuration-proof.md" in docs_index
    assert "tests/test_l6aq03_operator_service_configuration_proof.py" in inventory
    assert "L6AQ.03 operator/service configuration proof" in inventory
    assert L6AQ03_STATUS in inventory


def test_configuration_proof_binds_exact_operator_service_shape_without_retry() -> None:
    receipt = build_l6aq03_operator_service_configuration_proof()

    assert receipt["status"] == L6AQ03_STATUS
    assert receipt["rail_issue"] == 402
    assert receipt["rail_starting_source_floor"] == "755ab24e4ac5a283081f134cbc18c95c59d1c60e"
    assert receipt["retry_executed"] is False
    assert receipt["second_retry_performed"] is False
    assert all(value == 0 for value in receipt["guarded_counters"].values())

    proof = receipt["configuration_proof"]
    assert proof["endpoint"] == "memory_seam_recall"
    assert proof["route_audience"] == L6AQ01_EXPECTED_ROUTE_AUDIENCE
    assert proof["acting_for"] == "sax"
    assert proof["agent"] == "sax"
    assert proof["scope"] == "wiki"
    assert proof["n"] == 3
    assert proof["query_label"] == "supervised_metadata_readiness"
    assert proof["evidence_class"] == "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
    assert proof["configuration_proof_issue"] == 402
    assert proof["issue_bound_authority"] == "issue-bound:#402-only-proof:#403-max-one-preflight"
    assert proof["one_run_binding"] == "one-run:max-one:#403-only-after-l6aq03-pass"
    assert proof["max_operation_count"] == 1
    assert proof["report_safe_metadata_only"] is True
    assert proof["denial_before_read_required"] is True
    assert proof["metadata_only_output_contract"] is True
    assert proof["denial_before_read_stop"] is True
    assert proof["retry_authorized_by_configuration_proof"] is False
    assert "query_text" not in proof
    assert "auth_payload" not in proof
    assert "provider_payload" not in proof
    assert "source_uri" not in proof
    assert_l6aq03_configuration_proof_report_safe(receipt)


def test_validator_accepts_exact_proof_but_keeps_retry_default_off() -> None:
    result = validate_l6aq03_operator_service_configuration_proof(
        build_l6aq03_operator_service_configuration_proof_fixture()
    )

    assert result["status"] == L6AQ03_READY_STATUS
    assert result["reasons"] == ["operator_service_configuration_ready_retry_still_default_off"]
    assert result["preflight_metadata"]["route_audience"] == L6AQ01_EXPECTED_ROUTE_AUDIENCE
    assert result["preflight_metadata"]["retry_authorized_by_configuration_proof"] is False
    assert result["retry_executed"] is False
    assert result["second_retry_performed"] is False
    assert all(value == 0 for value in result["guarded_counters"].values())
    assert_l6aq03_validation_report_safe(result)


def test_validator_refuses_stale_broadened_copied_missing_multi_raw_secret_discovery_activation_and_movement() -> None:
    base = build_l6aq03_operator_service_configuration_proof_fixture()
    cases = [
        ({}, L6AQ03_HELD_STATUS, "missing_configuration_proof"),
        (base | {"operator_service_binding_ref": ""}, L6AQ03_HELD_STATUS, "missing_configuration_proof"),
        (base | {"binding_fresh": False}, L6AQ03_HELD_STATUS, "stale_binding"),
        (base | {"route_audience": "memory-seam:read:*"}, L6AQ03_DENIED_STATUS, "broadened_audience"),
        (base | {"route_audience": "memory-seam:read:context"}, L6AQ03_DENIED_STATUS, "wrong_route_audience"),
        (base | {"configuration_proof_issue": 401}, L6AQ03_DENIED_STATUS, "wrong_configuration_proof_issue"),
        (base | {"issue_bound_authority": "copied-from-stale-issue"}, L6AQ03_DENIED_STATUS, "wrong_issue_bound_authority"),
        (base | {"max_operation_count": 2}, L6AQ03_DENIED_STATUS, "multi_operation_requested"),
        (base | {"raw_output_requested": True}, L6AQ03_DENIED_STATUS, "raw_output_requested"),
        (base | {"auth_payload": "unsafe"}, L6AQ03_DENIED_STATUS, "forbidden_field_auth_payload"),
        (base | {"credential_read_requested": True}, L6AQ03_DENIED_STATUS, "credential_read_requested"),
        (base | {"source_discovery_requested": True}, L6AQ03_DENIED_STATUS, "source_discovery_requested"),
        (base | {"broad_recall_requested": True}, L6AQ03_DENIED_STATUS, "source_discovery_requested"),
        (base | {"runtime_registry_requested": True}, L6AQ03_DENIED_STATUS, "runtime_registry_requested"),
        (base | {"provider_callback_requested": True}, L6AQ03_DENIED_STATUS, "provider_callback_requested"),
        (base | {"service_activation_requested": True}, L6AQ03_DENIED_STATUS, "service_activation_requested"),
        (base | {"provider_prod_requested": True}, L6AQ03_DENIED_STATUS, "provider_prod_requested"),
        (base | {"canary_requested": True}, L6AQ03_DENIED_STATUS, "provider_prod_requested"),
        (base | {"gate_requested": True}, L6AQ03_DENIED_STATUS, "gate_requested"),
        (base | {"write_requested": True}, L6AQ03_DENIED_STATUS, "write_requested"),
        (base | {"mutation_requested": True}, L6AQ03_DENIED_STATUS, "write_requested"),
        (base | {"allowed": True}, L6AQ03_DENIED_STATUS, "broad_allowed_true"),
        (
            base | {"retry_authorized_by_configuration_proof": True},
            L6AQ03_DENIED_STATUS,
            "configuration_proof_attempted_to_authorize_retry",
        ),
    ]
    for candidate, expected_status, expected_reason in cases:
        result = validate_l6aq03_operator_service_configuration_proof(candidate)
        assert result["status"] == expected_status
        assert expected_reason in result["reasons"]
        assert result["retry_executed"] is False
        assert result["second_retry_performed"] is False
        assert_l6aq03_validation_report_safe(result)


def test_doc_names_operator_service_proof_cases_and_holds() -> None:
    text = normalized(DOC)
    for term in (
        "# L6AQ.03 operator/service configuration proof",
        f"Status: `{L6AQ03_STATUS}`",
        "Rail issue: #402",
        "Parent issue: #6",
        "Rail starting source floor: `755ab24e4ac5a283081f134cbc18c95c59d1c60e`",
        "endpoint | `memory_seam_recall`",
        "route audience | `memory-seam:read:recall`",
        "acting_for / agent | `sax` / `sax`",
        "scope / n | `wiki` / `3`",
        "query label | `supervised_metadata_readiness`",
        "configuration proof issue | `402`",
        "retry_authorized_by_configuration_proof | `false`",
        "stale binding, broadened audience, copied or wrong issue authority, missing configuration proof, multi-operation requests, raw output, secret or credential reads, source discovery, broad recall, Runtime Registry requests, provider callbacks, service activation, provider/prod/canary/Gate/write movement, and broad `allowed=true`",
        "No live retry was executed for this issue.",
        "python -m pytest -q tests/test_l6aq03_operator_service_configuration_proof.py",
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
