from __future__ import annotations

from pathlib import Path

from memory_seam.l6al_provider_auth_readiness_fixture import (
    EXPECTED_EVIDENCE_CLASS,
    EXPECTED_IDENTITY_SUBJECT,
    EXPECTED_ROUTE_AUDIENCE,
    EXPECTED_SCOPE,
    L6AL02_DENIED_STATUS,
    L6AL02_READY_STATUS,
    assert_l6al02_report_safe_receipt,
    build_l6al02_authorized_metadata_readiness_fixture,
    build_l6al02_denied_auth_mismatch_fixture,
    evaluate_l6al02_provider_auth_readiness,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6al02-provider-auth-readiness-fixture.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_PROVIDER_AUTH_READINESS_FIXTURE_READY_RETRY_STILL_HELD"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def assert_zero_read_and_callback_counters(receipt: dict[str, object]) -> None:
    counters = receipt["guarded_counters"]
    assert isinstance(counters, dict)
    assert counters["source_item_count"] == 0
    assert counters["source_read_callback_count"] == 0
    assert counters["provider_callback_count"] == 0
    assert counters["provider_route_invocation_count"] == 0
    assert all(value == 0 for value in counters.values())
    assert receipt["items"] == []
    assert receipt["read_authorized"] is False
    assert receipt["retry_executed"] is False


def test_l6al02_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6al02-provider-auth-readiness-fixture.md" in docs_index
    assert "tests/test_l6al02_provider_auth_readiness_fixture.py" in inventory
    assert "src/memory_seam/l6al_provider_auth_readiness_fixture.py" in inventory
    assert "L6AL.02 non-secret provider auth readiness fixture" in inventory
    assert STATUS in inventory


def test_authorized_metadata_readiness_fixture_does_not_authorize_or_execute_read() -> None:
    receipt = evaluate_l6al02_provider_auth_readiness(
        build_l6al02_authorized_metadata_readiness_fixture()
    )

    assert receipt["status"] == L6AL02_READY_STATUS
    assert receipt["auth_ready"] is True
    assert receipt["denial_reason"] is None
    assert receipt["denial_before_read"] is True
    assert receipt["binding_summary"]["route_audience_matched"] is True
    assert receipt["binding_summary"]["identity_subject_present"] is True
    assert receipt["binding_summary"]["scope"] == EXPECTED_SCOPE
    assert_zero_read_and_callback_counters(receipt)
    assert_l6al02_report_safe_receipt(receipt)


def test_wrong_route_audience_denies_before_items_or_read_callbacks() -> None:
    receipt = evaluate_l6al02_provider_auth_readiness(
        build_l6al02_denied_auth_mismatch_fixture("wrong_route_audience")
    )

    assert receipt["status"] == L6AL02_DENIED_STATUS
    assert receipt["auth_ready"] is False
    assert receipt["denial_reason"] == "wrong_route_audience"
    assert receipt["binding_summary"]["route_audience_matched"] is False
    assert_zero_read_and_callback_counters(receipt)
    assert_l6al02_report_safe_receipt(receipt)


def test_unauthorized_narrowing_denies_before_items_or_read_callbacks() -> None:
    receipt = evaluate_l6al02_provider_auth_readiness(
        build_l6al02_denied_auth_mismatch_fixture("unauthorized_narrowing")
    )

    assert receipt["status"] == L6AL02_DENIED_STATUS
    assert receipt["auth_ready"] is False
    assert receipt["denial_reason"] == "unauthorized_narrowing"
    assert receipt["binding_summary"]["authorization_narrowing"] == "context_only_without_recall"
    assert_zero_read_and_callback_counters(receipt)
    assert_l6al02_report_safe_receipt(receipt)


def test_other_auth_mismatches_deny_before_read() -> None:
    for reason in (
        "missing_identity_subject",
        "stale_approval",
        "broadened_scope_denied",
    ):
        receipt = evaluate_l6al02_provider_auth_readiness(
            build_l6al02_denied_auth_mismatch_fixture(reason)
        )
        assert receipt["status"] == L6AL02_DENIED_STATUS
        assert receipt["auth_ready"] is False
        assert receipt["denial_reason"] == reason
        assert_zero_read_and_callback_counters(receipt)
        assert_l6al02_report_safe_receipt(receipt)


def test_raw_output_secrets_provider_payloads_and_broad_allowed_deny_without_echo() -> None:
    for unsafe_key, expected_reason in (
        ("credential_value", "raw_output_denied"),
        ("auth_file_material", "raw_output_denied"),
        ("provider_payload", "raw_output_denied"),
        ("callback_payload", "raw_output_denied"),
        ("allowed_true", "broad_allowed_true_denied"),
    ):
        request = build_l6al02_authorized_metadata_readiness_fixture()
        request[unsafe_key] = "redacted-test-placeholder"
        receipt = evaluate_l6al02_provider_auth_readiness(request)
        assert receipt["denial_reason"] == expected_reason
        assert unsafe_key not in receipt
        assert_zero_read_and_callback_counters(receipt)
        assert_l6al02_report_safe_receipt(receipt)


def test_fixture_contract_uses_expected_non_secret_labels() -> None:
    fixture = build_l6al02_authorized_metadata_readiness_fixture()

    assert fixture["route_audience"] == EXPECTED_ROUTE_AUDIENCE
    assert fixture["identity_subject"] == EXPECTED_IDENTITY_SUBJECT
    assert fixture["scope"] == EXPECTED_SCOPE
    assert fixture["evidence_class"] == EXPECTED_EVIDENCE_CLASS
    assert fixture["source_read_callback"] == "fixture-inert-not-callable"
    assert "credential_value" not in fixture
    assert "provider_payload" not in fixture
    assert "runtime_registry_payload" not in fixture
    assert "allowed_true" not in fixture


def test_doc_records_boundaries_counter_proof_and_verification_gate() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AL.02 non-secret provider auth readiness fixture",
        f"Status: `{STATUS}`",
        "Rail issue: #350",
        "Depends on: L6AL.01 #349 closed/PASS",
        "performs no live/private read retry",
        "loads no secret material",
        "calls no read callback",
        "creates no route that can return broad `allowed=true` behavior",
        "`route_audience`: exactly `memory-seam:read:recall`",
        "`identity_subject`: exactly `atlas-query-supervised-metadata-reader`",
        "`authorization_narrowing=exact`",
        "`source_item_count=0`",
        "`source_read_callback_count=0`",
        "`provider_callback_count=0`",
        "The positive fixture may return `auth_ready=true`, but it still returns `read_authorized=false`, `retry_executed=false`, and `items=[]`.",
        "wrong route audience | `wrong_route_audience` | denied before source items/read callbacks",
        "unauthorized narrowing | `unauthorized_narrowing` | denied before source items/read callbacks",
        "python -m pytest -q tests/test_l6al02_provider_auth_readiness_fixture.py",
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
