from __future__ import annotations

from pathlib import Path

from memory_seam.l6ao_auth_held_default_off_intake import (
    L6AO04_ROLLBACK_STOP_CONDITIONS,
    L6AO04_STATUS,
    assert_l6ao04_review_report_safe,
    build_l6ao04_trust_boundary_review,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ao04-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ao04_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ao04-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ao04_trust_boundary_review.py" in inventory
    assert "L6AO.04 trust-boundary review" in inventory
    assert L6AO04_STATUS in inventory


def test_trust_boundary_review_covers_artifacts_blocker_and_unblock_condition() -> None:
    review = build_l6ao04_trust_boundary_review()

    assert review["status"] == L6AO04_STATUS
    assert review["rail_issue"] == 383
    assert review["parent_issue"] == 6
    assert review["source_floor"] == "57e8bd4612824ada20718e41b1eea33210fe2974"
    assert review["reviewed_artifacts"] == [
        "#380 L6AO.01 auth-held blocker receipt and default-off binding intake",
        "#381 L6AO.02 binding-intake readiness fixtures and denial-before-read states",
        "#382 L6AO.03 max-one metadata retry execution packet scaffold",
    ]
    assert review["blocker_owner"] == "service-owner-or-operator"
    assert review["future_unblock_condition"] == (
        "fresh exact non-secret operator/service binding approval plus explicit issue-bound "
        "max-one metadata retry authorization"
    )
    assert review["retry_authorized"] is False
    assert review["retry_executed"] is False
    assert all(value == 0 for value in review["guarded_counters"].values())
    assert_l6ao04_review_report_safe(review)


def test_findings_cover_no_go_surfaces_and_default_off_readiness() -> None:
    findings = build_l6ao04_trust_boundary_review()["trust_boundary_findings"]

    assert findings == {
        "secret_private_source_or_raw_content_present": False,
        "secret_env_keychain_oauth_auth_file_or_credential_read_present": False,
        "runtime_registry_provider_callback_or_service_activation_present": False,
        "source_discovery_broad_recall_or_broad_allowed_true_present": False,
        "provider_prod_canary_gate_atlas_gate_write_or_mutation_present": False,
        "auth_blocker_owner_named": True,
        "future_unblock_condition_exact": True,
        "retry_remains_auth_held_default_off": True,
    }


def test_rollback_stop_conditions_name_hard_stops_before_future_retry() -> None:
    review = build_l6ao04_trust_boundary_review()

    assert review["rollback_stop_conditions"] == list(L6AO04_ROLLBACK_STOP_CONDITIONS)
    for condition in (
        "missing_fresh_exact_non_secret_operator_service_binding_approval",
        "missing_explicit_issue_bound_max_one_metadata_retry_authorization",
        "stale_copied_mismatched_expired_or_broadened_approval",
        "any_secret_env_keychain_oauth_auth_file_or_credential_read_request",
        "any_runtime_registry_provider_callback_or_service_activation_request",
        "any_provider_prod_canary_gate_atlas_gate_write_or_mutation_request",
        "any_nonzero_guarded_counter_or_retry_execution_attempt",
    ):
        assert condition in review["rollback_stop_conditions"]


def test_report_safe_assertion_rejects_retry_boundary_expansion_or_unsafe_fields() -> None:
    review = build_l6ao04_trust_boundary_review()

    unsafe_reviews = (
        review | {"retry_authorized": True},
        review | {"retry_executed": True},
        review | {"raw_private_source": "forbidden"},
        review | {"guarded_counters": review["guarded_counters"] | {"source_items_returned": 1}},
        review
        | {
            "trust_boundary_findings": review["trust_boundary_findings"]
            | {"secret_private_source_or_raw_content_present": True}
        },
        review
        | {
            "trust_boundary_findings": review["trust_boundary_findings"]
            | {"retry_remains_auth_held_default_off": False}
        },
    )
    for unsafe in unsafe_reviews:
        try:
            assert_l6ao04_review_report_safe(unsafe)
        except AssertionError:
            pass
        else:  # pragma: no cover - defensive guard
            raise AssertionError("unsafe L6AO.04 trust-boundary review should fail closed")


def test_doc_names_findings_stop_conditions_and_verification_commands() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AO.04 trust-boundary review for auth-held unblock rail",
        f"Status: `{L6AO04_STATUS}`",
        "Rail issue: #383",
        "Reviewed artifacts: #380, #381, #382",
        "No secret/private/source/raw content is carried",
        "No Runtime Registry payload, provider callback, or service activation is consumed or carried",
        "No source discovery, broad recall, or broad `allowed=true` behavior is introduced",
        "The blocker owner is `service-owner-or-operator`",
        "fresh exact non-secret operator/service binding approval plus explicit issue-bound max-one metadata retry authorization",
        "missing fresh exact non-secret operator/service binding approval",
        "missing explicit issue-bound max-one metadata retry authorization",
        "python -m pytest -q tests/test_l6ao04_trust_boundary_review.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
