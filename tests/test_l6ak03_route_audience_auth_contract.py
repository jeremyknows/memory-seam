from __future__ import annotations

from pathlib import Path

from memory_seam.l6ak_route_audience_auth_contract import (
    EXPECTED_AUDIENCE,
    EXPECTED_CONTEXT_INCLUDE,
    EXPECTED_RECALL_SCOPE,
    L6AK03_DENIED_STATUS,
    L6AK03_READY_STATUS,
    build_l6ak03_exact_binding_fixture,
    evaluate_l6ak03_route_audience_contract,
    assert_l6ak03_report_safe_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ak03-non-secret-auth-contract-shim.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_NON_SECRET_AUTH_CONTRACT_SHIM_READY_RETRY_STILL_HELD"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ak03_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ak03-non-secret-auth-contract-shim.md" in docs_index
    assert "tests/test_l6ak03_route_audience_auth_contract.py" in inventory
    assert "src/memory_seam/l6ak_route_audience_auth_contract.py" in inventory
    assert "L6AK.03 non-secret auth contract shim" in inventory
    assert STATUS in inventory


def test_exact_binding_returns_readiness_without_authorizing_or_executing_retry() -> None:
    receipt = evaluate_l6ak03_route_audience_contract(build_l6ak03_exact_binding_fixture())

    assert receipt["status"] == L6AK03_READY_STATUS
    assert receipt["ready_for_exact_retry"] is True
    assert receipt["read_authorized"] is False
    assert receipt["retry_executed"] is False
    assert receipt["denial_before_read"] is True
    assert receipt["source_access_attempted"] is False
    assert receipt["binding_summary"]["audience_matched"] is True
    assert receipt["binding_summary"]["scope"] == EXPECTED_RECALL_SCOPE
    assert receipt["binding_summary"]["context_include"] == EXPECTED_CONTEXT_INCLUDE
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert_l6ak03_report_safe_receipt(receipt)


def test_wrong_route_audience_denies_before_read() -> None:
    request = build_l6ak03_exact_binding_fixture()
    request["audience"] = "memory-seam:wrong-audience"

    receipt = evaluate_l6ak03_route_audience_contract(request)

    assert receipt["status"] == L6AK03_DENIED_STATUS
    assert receipt["denial_reason"] == "wrong_route_audience"
    assert receipt["ready_for_exact_retry"] is False
    assert receipt["source_access_attempted"] is False
    assert receipt["binding_summary"]["audience_matched"] is False
    assert_l6ak03_report_safe_receipt(receipt)


def test_unauthorized_narrowing_denies_before_read() -> None:
    request = build_l6ak03_exact_binding_fixture()
    request["context_include"] = "profile"

    receipt = evaluate_l6ak03_route_audience_contract(request)

    assert receipt["status"] == L6AK03_DENIED_STATUS
    assert receipt["denial_reason"] == "unauthorized_narrowing"
    assert receipt["source_access_attempted"] is False
    assert_l6ak03_report_safe_receipt(receipt)


def test_stale_approval_denies_before_read() -> None:
    request = build_l6ak03_exact_binding_fixture()
    request["approval_freshness"] = "copied_stale_prior_receipt"

    receipt = evaluate_l6ak03_route_audience_contract(request)

    assert receipt["denial_reason"] == "stale_approval"
    assert receipt["source_access_attempted"] is False
    assert_l6ak03_report_safe_receipt(receipt)


def test_mismatched_agent_denies_before_read() -> None:
    request = build_l6ak03_exact_binding_fixture()
    request["agent"] = "watson"

    receipt = evaluate_l6ak03_route_audience_contract(request)

    assert receipt["denial_reason"] == "mismatched_agent"
    assert receipt["source_access_attempted"] is False
    assert_l6ak03_report_safe_receipt(receipt)


def test_broadened_scope_denies_before_read() -> None:
    request = build_l6ak03_exact_binding_fixture()
    request["scope"] = "all"

    receipt = evaluate_l6ak03_route_audience_contract(request)

    assert receipt["denial_reason"] == "broadened_scope"
    assert receipt["source_access_attempted"] is False
    assert_l6ak03_report_safe_receipt(receipt)


def test_raw_output_and_unsafe_echo_requests_deny_before_read() -> None:
    raw_request = build_l6ak03_exact_binding_fixture()
    raw_request["raw_output_requested"] = True
    raw_receipt = evaluate_l6ak03_route_audience_contract(raw_request)
    assert raw_receipt["denial_reason"] == "raw_output_requested"
    assert_l6ak03_report_safe_receipt(raw_receipt)

    unsafe_request = build_l6ak03_exact_binding_fixture()
    unsafe_request["credential_value"] = "redacted-test-placeholder"
    unsafe_receipt = evaluate_l6ak03_route_audience_contract(unsafe_request)
    assert unsafe_receipt["denial_reason"] == "raw_output_requested"
    assert "credential_value" not in unsafe_receipt
    assert_l6ak03_report_safe_receipt(unsafe_receipt)


def test_missing_identity_and_broad_allowed_true_deny_before_read() -> None:
    missing_identity = build_l6ak03_exact_binding_fixture()
    missing_identity.pop("identity_subject")
    missing_receipt = evaluate_l6ak03_route_audience_contract(missing_identity)
    assert missing_receipt["denial_reason"] == "missing_identity_subject"
    assert_l6ak03_report_safe_receipt(missing_receipt)

    broad_allowed = build_l6ak03_exact_binding_fixture()
    broad_allowed["allowed_true"] = True
    broad_receipt = evaluate_l6ak03_route_audience_contract(broad_allowed)
    assert broad_receipt["denial_reason"] == "broad_allowed_true_requested"
    assert broad_receipt["broad_allowed_attempted"] is False
    assert_l6ak03_report_safe_receipt(broad_receipt)


def test_doc_records_non_secret_boundaries_and_verification_gate() -> None:
    text = normalized(DOC)

    for term in (
        f"Status: `{STATUS}`",
        "Rail issue: #343",
        "Depends on: #341-#342 closed/PASS",
        "`identity_subject`",
        "`acting_for`",
        f"`{EXPECTED_AUDIENCE}`",
        "does not load secrets",
        "does not read environment values, keychain entries, OAuth material, auth files, credentials, Runtime Registry data, callback payloads, provider payloads, source cards, source URIs, platform raw IDs, raw private content, or raw source text",
        "returns `ready_for_exact_retry=true` only as non-secret readiness metadata",
        "does not execute the retry",
        "does not create broad `allowed=true` behavior",
        "python -m pytest -q tests/test_l6ak03_route_audience_auth_contract.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
