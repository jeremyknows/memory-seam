from __future__ import annotations

from pathlib import Path

from memory_seam.l6an_service_operator_auth_binding_packet import (
    L6AN04_STOP_CONDITIONS,
    L6AN04_STATUS,
    assert_l6an04_review_report_safe,
    build_l6an04_trust_boundary_review,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6an04-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6an04_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6an04-trust-boundary-review.md" in docs_index
    assert "tests/test_l6an04_trust_boundary_review.py" in inventory
    assert "L6AN.04 trust-boundary review" in inventory
    assert L6AN04_STATUS in inventory


def test_trust_boundary_review_covers_prior_artifacts_and_keeps_retry_held() -> None:
    review = build_l6an04_trust_boundary_review()

    assert review["status"] == L6AN04_STATUS
    assert review["rail_issue"] == 373
    assert review["parent_issue"] == 6
    assert review["retry_executed"] is False
    assert review["reviewed_artifacts"] == [
        "#370 L6AN.01 service/operator auth-binding unblock packet",
        "#371 L6AN.02 non-secret binding-reference validator",
        "#372 L6AN.03 service-owner handoff retry-gate decision",
    ]
    assert review["boundary_findings"] == {
        "secret_like_material_present": False,
        "raw_private_data_present": False,
        "source_uri_or_provider_payload_present": False,
        "runtime_registry_payload_present": False,
        "auth_file_material_present": False,
        "broad_allowed_true_behavior_present": False,
        "usable_service_operator_handoff_present": True,
        "retry_remains_held": True,
    }
    assert all(value == 0 for value in review["guarded_counters"].values())
    assert_l6an04_review_report_safe(review)


def test_stop_conditions_name_rollback_boundaries_for_future_retry() -> None:
    review = build_l6an04_trust_boundary_review()

    assert review["rollback_stop_conditions"] == list(L6AN04_STOP_CONDITIONS)
    for condition in (
        "missing_fresh_exact_operator_service_binding_reference",
        "missing_explicit_new_max_one_retry_issue_authorization",
        "any_request_for_secret_env_keychain_oauth_auth_file_or_credential_material",
        "any_runtime_registry_provider_callback_or_service_activation_request",
        "any_raw_private_source_uri_payload_or_broad_allowed_true_behavior",
        "any_provider_prod_canary_gate_write_or_mutation_surface",
    ):
        assert condition in review["rollback_stop_conditions"]


def test_report_safe_assertion_rejects_retry_or_boundary_expansion() -> None:
    review = build_l6an04_trust_boundary_review()

    unsafe_reviews = (
        review | {"retry_executed": True},
        review | {"raw_provider_payload": "forbidden"},
        review | {"boundary_findings": review["boundary_findings"] | {"secret_like_material_present": True}},
        review | {"boundary_findings": review["boundary_findings"] | {"retry_remains_held": False}},
    )
    for unsafe in unsafe_reviews:
        try:
            assert_l6an04_review_report_safe(unsafe)
        except AssertionError:
            pass
        else:  # pragma: no cover - defensive guard
            raise AssertionError("unsafe L6AN.04 review should fail closed")


def test_doc_names_findings_stop_conditions_and_verification_commands() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AN.04 trust-boundary review for service/operator auth-binding unblock",
        f"Status: `{L6AN04_STATUS}`",
        "Rail issue: #373",
        "Reviewed artifacts: #370, #371, #372",
        "No secret-like material is carried",
        "No Runtime Registry payload is consumed or carried",
        "No broad `allowed=true` behavior is introduced",
        "missing fresh exact operator/service binding reference",
        "missing explicit new max-one retry issue authorization",
        "python -m pytest -q tests/test_l6an04_trust_boundary_review.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
