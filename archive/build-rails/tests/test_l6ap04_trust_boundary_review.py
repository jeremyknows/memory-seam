from __future__ import annotations

from pathlib import Path

from memory_seam.l6ap_metadata_retry_rail import (
    L6AP02_BLOCKER_CLASSIFICATION,
    L6AP04_DECISION,
    L6AP04_ROLLBACK_STOP_CONDITIONS,
    L6AP04_STATUS,
    assert_l6ap04_trust_review_report_safe,
    build_l6ap04_trust_boundary_review,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ap04-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ap04_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ap04-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ap04_trust_boundary_review.py" in inventory
    assert "L6AP.04 trust-boundary review" in inventory
    assert L6AP04_STATUS in inventory


def test_l6ap04_reviews_prior_artifacts_and_retry_receipt_metadata_only() -> None:
    review = build_l6ap04_trust_boundary_review()

    assert review["status"] == L6AP04_STATUS
    assert review["decision"] == L6AP04_DECISION
    assert review["rail_issue"] == 393
    assert review["parent_issue"] == 6
    assert review["rail_starting_source_floor"] == "35046efe4880145d929bbe0ddb00196b83c9cc04"
    assert review["reviewed_artifacts"] == [
        "#390 L6AP.01 fresh binding approval and max-one retry preflight",
        "#391 L6AP.02 supervised metadata retry safe-denial receipt",
        "#392 L6AP.03 post-retry Step 3 usefulness decision",
    ]
    assert review["source_consumption_scope"] == [
        "committed L6AP docs/tests/module metadata",
        "public issue and PR metadata only",
        "L6AP.02 report-safe retry receipt metadata only",
    ]
    assert review["retry_receipt_metadata"] == {
        "status": "SUPERVISED_METADATA_RETRY_SAFE_DENIAL_CAPTURED",
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "agent": "sax",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "items_count": 0,
        "safe_item_labels": [],
        "denial_reason": "wrong_route_audience",
        "auth_status_code": 403,
        "retry_operation_count": 1,
        "second_retry_performed": False,
        "guarded_counters": review["retry_receipt_metadata"]["guarded_counters"],
    }
    assert all(value == 0 for value in review["retry_receipt_metadata"]["guarded_counters"].values())
    assert_l6ap04_trust_review_report_safe(review)


def test_l6ap04_findings_prove_hard_no_go_boundaries_and_exactly_one_retry() -> None:
    review = build_l6ap04_trust_boundary_review()

    assert review["trust_boundary_findings"] == {
        "raw_private_source_content_or_source_path_uri_present": False,
        "auth_provider_payload_secret_env_keychain_oauth_auth_file_or_credential_present": False,
        "runtime_registry_provider_callback_or_service_activation_present": False,
        "source_discovery_broad_recall_or_broad_allowed_true_present": False,
        "provider_prod_canary_gate_atlas_gate_write_or_mutation_present": False,
        "exactly_one_retry_performed": True,
        "denied_before_read_with_zero_items": True,
        "step3_usefulness_remains_held": True,
        "next_lane_limited_to_source_floor_reconciliation": True,
    }
    assert review["retry_operation_count"] == 1
    assert review["second_retry_performed"] is False
    assert review["runtime_registry_or_service_activation_performed"] is False
    assert review["provider_prod_canary_gate_or_write_movement_performed"] is False
    assert review["successor_execution_rail_created"] is False
    assert all(value == 0 for value in review["guarded_counters"].values())


def test_l6ap04_rollback_stop_conditions_and_residual_holds_are_explicit() -> None:
    review = build_l6ap04_trust_boundary_review()

    assert review["rollback_stop_conditions"] == list(L6AP04_ROLLBACK_STOP_CONDITIONS)
    for condition in (
        "raw_private_source_content_or_source_path_uri_requested",
        "auth_provider_payload_secret_env_keychain_oauth_auth_file_or_credential_requested",
        "runtime_registry_provider_callback_or_service_activation_requested",
        "source_discovery_broad_recall_or_broad_allowed_true_requested",
        "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested",
        "retry_operation_count_greater_than_one_or_second_retry_requested",
        "any_nonzero_guarded_counter",
    ):
        assert condition in review["rollback_stop_conditions"]

    for hold in (
        "no second retry",
        "no raw/private/source/auth/provider/callback output",
        "no source paths or URIs",
        "no secret/env/keychain/OAuth/auth-file/credential reads",
        "no Runtime Registry/provider callback/service activation",
        "no provider/prod/canary/Gate/write movement",
        "no broad allowed=true behavior",
    ):
        assert hold in review["residual_holds"]


def test_l6ap04_rejects_unsafe_boundary_expansion() -> None:
    review = build_l6ap04_trust_boundary_review()
    unsafe_reviews = (
        review | {"retry_operation_count": 2},
        review | {"second_retry_performed": True},
        review | {"successor_execution_rail_created": True},
        review | {"runtime_registry_or_service_activation_performed": True},
        review | {"provider_prod_canary_gate_or_write_movement_performed": True},
        review | {"raw_source_text": "forbidden"},
        review | {"guarded_counters": review["guarded_counters"] | {"source_items_returned": 1}},
        review
        | {
            "trust_boundary_findings": review["trust_boundary_findings"]
            | {"raw_private_source_content_or_source_path_uri_present": True}
        },
        review
        | {
            "trust_boundary_findings": review["trust_boundary_findings"]
            | {"exactly_one_retry_performed": False}
        },
    )
    for unsafe in unsafe_reviews:
        try:
            assert_l6ap04_trust_review_report_safe(unsafe)
        except AssertionError:
            pass
        else:  # pragma: no cover - defensive guard
            raise AssertionError("unsafe L6AP.04 trust-boundary review should fail closed")


def test_doc_names_findings_stop_conditions_and_verification_commands() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AP.04 trust-boundary review for max-one metadata retry rail",
        f"Status: `{L6AP04_STATUS}`",
        "Rail issue: #393",
        "Reviewed artifacts: #390, #391, #392",
        "L6AP.02 retry receipt metadata recorded `auth_status_code=403`, `wrong_route_audience`, `items_count=0`, safe item labels `[]`, `retry_operation_count=1`, and `second_retry_performed=false`.",
        "No raw/private/source content, source paths, or source URIs are carried.",
        "No auth payloads, provider payloads, secrets, environment values, keychain material, OAuth material, auth-file material, or credential material is read or carried.",
        "No Runtime Registry payload, provider callback, or service activation is consumed or carried.",
        "No source discovery, broad recall, or broad `allowed=true` behavior is introduced.",
        "No provider/prod/canary/Gate, Atlas Gate, write, or mutation movement is introduced.",
        "Exactly one metadata retry was performed; no second retry was performed.",
        L6AP02_BLOCKER_CLASSIFICATION,
        "python -m pytest -q tests/test_l6ap04_trust_boundary_review.py",
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
