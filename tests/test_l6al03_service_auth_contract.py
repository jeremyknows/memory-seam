from __future__ import annotations

from pathlib import Path

from memory_seam.l6al_service_auth_contract import (
    ENDPOINT_AUDIENCES,
    ENDPOINT_EVIDENCE_CLASSES,
    EXPECTED_IDENTITY_SUBJECT,
    EXPECTED_SCOPE,
    L6AL03_DENIED_STATUS,
    L6AL03_HELD_STATUS,
    L6AL03_READY_STATUS,
    assert_l6al03_report_safe_receipt,
    build_l6al03_exact_service_auth_contract,
    evaluate_l6al03_service_auth_contract,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6al03-minimal-service-auth-contract.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_MINIMAL_SERVICE_AUTH_CONTRACT_READY_RETRY_STILL_HELD"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def assert_no_read_side_effects(receipt: dict[str, object]) -> None:
    counters = receipt["guarded_counters"]
    assert isinstance(counters, dict)
    assert counters["source_access_count"] == 0
    assert counters["source_item_count"] == 0
    assert counters["source_read_callback_count"] == 0
    assert counters["provider_callback_count"] == 0
    assert counters["runtime_registry_read_count"] == 0
    assert counters["credential_or_secret_read_count"] == 0
    assert all(value == 0 for value in counters.values())
    assert receipt["read_authorized"] is False
    assert receipt["retry_executed"] is False
    assert receipt["items"] == []
    assert_l6al03_report_safe_receipt(receipt)


def test_l6al03_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6al03-minimal-service-auth-contract.md" in docs_index
    assert "tests/test_l6al03_service_auth_contract.py" in inventory
    assert "src/memory_seam/l6al_service_auth_contract.py" in inventory
    assert "L6AL.03 minimal non-secret service auth contract" in inventory
    assert STATUS in inventory


def test_exact_service_auth_contract_returns_readiness_metadata_only_for_each_endpoint() -> None:
    for endpoint, audience in ENDPOINT_AUDIENCES.items():
        receipt = evaluate_l6al03_service_auth_contract(
            build_l6al03_exact_service_auth_contract(endpoint)
        )

        assert receipt["status"] == L6AL03_READY_STATUS
        assert receipt["auth_ready"] is True
        assert receipt["auth_held"] is False
        assert receipt["denial_reason"] is None
        assert receipt["hold_reason"] is None
        assert receipt["binding_summary"]["endpoint"] == endpoint
        assert receipt["binding_summary"]["route_audience_matched"] is True
        assert receipt["binding_summary"]["scope_matched"] is True
        assert audience in ENDPOINT_AUDIENCES.values()
        assert_no_read_side_effects(receipt)


def test_missing_provider_or_service_binding_is_auth_held_not_ready() -> None:
    for missing_key, hold_reason in (
        ("provider_binding_present", "provider_binding_missing"),
        ("service_binding_present", "service_binding_missing"),
    ):
        request = build_l6al03_exact_service_auth_contract("recall").as_fixture()
        request[missing_key] = False
        receipt = evaluate_l6al03_service_auth_contract(request)

        assert receipt["status"] == L6AL03_HELD_STATUS
        assert receipt["auth_ready"] is False
        assert receipt["auth_held"] is True
        assert receipt["hold_reason"] == hold_reason
        assert receipt["denial_reason"] is None
        assert_no_read_side_effects(receipt)


def test_auth_mismatches_deny_before_source_access() -> None:
    variants = (
        ("route_audience", "memory-seam:read:context", "wrong_route_audience"),
        ("authorization_narrowing", "context_only_without_recall", "unauthorized_narrowing"),
        ("identity_subject", "other-service", "mismatched_identity_subject"),
        ("acting_for", "watson", "mismatched_agent"),
        ("scope", "all", "broadened_scope_denied"),
        ("max_operation_count", 2, "broadened_scope_denied"),
        ("metadata_only", False, "raw_output_denied"),
        ("expiry", "stale_or_missing", "stale_approval"),
        ("evidence_class", "SUPERVISED_METADATA_CONTEXT_READ_RETRY", "mismatched_evidence_class"),
    )

    for key, value, reason in variants:
        request = build_l6al03_exact_service_auth_contract("recall").as_fixture()
        request[key] = value
        receipt = evaluate_l6al03_service_auth_contract(request)

        assert receipt["status"] == L6AL03_DENIED_STATUS
        assert receipt["auth_ready"] is False
        assert receipt["auth_held"] is False
        assert receipt["denial_reason"] == reason
        assert_no_read_side_effects(receipt)


def test_missing_identity_and_unknown_endpoint_deny_before_read() -> None:
    missing_identity = build_l6al03_exact_service_auth_contract("recall").as_fixture()
    missing_identity.pop("identity_subject")
    missing_receipt = evaluate_l6al03_service_auth_contract(missing_identity)
    assert missing_receipt["denial_reason"] == "missing_identity_subject"
    assert_no_read_side_effects(missing_receipt)

    unknown_endpoint = build_l6al03_exact_service_auth_contract("recall").as_fixture()
    unknown_endpoint["endpoint"] = "write"
    unknown_receipt = evaluate_l6al03_service_auth_contract(unknown_endpoint)
    assert unknown_receipt["denial_reason"] == "unknown_endpoint"
    assert_no_read_side_effects(unknown_receipt)


def test_unsafe_payload_and_broad_allowed_keys_deny_without_echo() -> None:
    for unsafe_key, expected_reason in (
        ("credential_value", "raw_output_denied"),
        ("env_value", "raw_output_denied"),
        ("keychain_value", "raw_output_denied"),
        ("oauth_value", "raw_output_denied"),
        ("auth_file_material", "raw_output_denied"),
        ("provider_payload", "raw_output_denied"),
        ("callback_payload", "raw_output_denied"),
        ("runtime_registry_payload", "raw_output_denied"),
        ("source_uri", "raw_output_denied"),
        ("allowed_true", "broad_allowed_true_denied"),
    ):
        request = build_l6al03_exact_service_auth_contract("recall").as_fixture()
        request[unsafe_key] = "redacted-test-placeholder"
        receipt = evaluate_l6al03_service_auth_contract(request)

        assert receipt["denial_reason"] == expected_reason
        assert unsafe_key not in receipt
        assert_no_read_side_effects(receipt)


def test_contract_builder_uses_endpoint_specific_audience_and_evidence_class() -> None:
    for endpoint in ("context", "recall", "health"):
        contract = build_l6al03_exact_service_auth_contract(endpoint)
        fixture = contract.as_fixture()

        assert fixture["endpoint"] == endpoint
        assert fixture["route_audience"] == ENDPOINT_AUDIENCES[endpoint]
        assert fixture["identity_subject"] == EXPECTED_IDENTITY_SUBJECT
        assert fixture["scope"] == EXPECTED_SCOPE
        assert fixture["evidence_class"] == ENDPOINT_EVIDENCE_CLASSES[endpoint]
        assert "credential_value" not in fixture
        assert "provider_payload" not in fixture
        assert "allowed_true" not in fixture


def test_doc_records_contract_boundaries_and_verification_gate() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AL.03 minimal non-secret service auth contract",
        f"Status: `{STATUS}`",
        "Rail issue: #351",
        "Depends on: L6AL.01-L6AL.02 closed/PASS",
        "`ServiceAuthContract`",
        "`evaluate_l6al03_service_auth_contract`",
        "`memory-seam:read:context`",
        "`memory-seam:read:recall`",
        "`memory-seam:read:health`",
        "`AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY`",
        "`AUTH_HELD_SERVICE_PROVIDER_BINDING_INCOMPLETE`",
        "`DENIED_BEFORE_READ_AUTH_CONTRACT_MISMATCH`",
        "`read_authorized=false`, `retry_executed=false`, `items=[]`",
        "`wrong_route_audience`",
        "`unauthorized_narrowing`",
        "`provider_binding_missing`",
        "`service_binding_missing`",
        "`source_access_count=0`",
        "`credential_or_secret_read_count=0`",
        "does not load secrets",
        "python -m pytest -q tests/test_l6al03_service_auth_contract.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text

    lowered = text.lower()
    for marker in (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref value",
        "source://",
        "platform-raw-id value",
    ):
        assert marker not in lowered
