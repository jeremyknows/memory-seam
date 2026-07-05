from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6w02-supervised-live-read-approval-denial-matrix.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

DENIAL_CASES = (
    "stale_prior_rail_comment",
    "variant_phrase_or_field_names",
    "broadened_scope_or_source_access",
    "copied_unrelated_approval",
    "wrong_actor_owner_subject_audience_scope",
    "missing_expiry_or_expired",
    "multi_operation_or_allowed_true",
    "callback_requesting_shape",
    "activation_or_config_request",
    "publication_visibility_provider_prod_canary",
    "runtime_registry_atlas_gate_persistence",
    "mutation_or_rollback_execution",
)

STOP_REASONS = (
    "STALE_OR_WRONG_ISSUE_APPROVAL",
    "VARIANT_APPROVAL_TEXT",
    "BROADENED_SCOPE_OR_SOURCE_ACCESS",
    "COPIED_OR_UNRELATED_APPROVAL",
    "BOUND_FIELD_MISMATCH",
    "MISSING_OR_EXPIRED_APPROVAL",
    "MULTI_OPERATION_OR_ALLOWED_TRUE_REQUEST",
    "CALLBACK_REQUESTED",
    "ACTIVATION_OR_CONFIG_REQUESTED",
    "PUBLICATION_OR_PRODUCTION_AUTHORITY_REQUESTED",
    "REGISTRY_GATE_OR_PERSISTENCE_REQUESTED",
    "MUTATION_OR_ROLLBACK_EXECUTION_REQUESTED",
)

ZERO_COUNTER_TERMS = (
    "provider",
    "backend",
    "source-stat",
    "source-read",
    "write",
    "custody",
    "delete",
    "reindex",
    "rollback",
    "cache-purge",
    "`source_discovery_counter`: `0`",
    "`runtime_registry_consumption_counter`: `0`",
    "`persistence_record_counter`: `0`",
    "`activation_counter`: `0`",
    "`publication_or_visibility_counter`: `0`",
    "`provider_prod_canary_counter`: `0`",
    "`atlas_gate_movement_counter`: `0`",
)

PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
    "source://",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6w02_denial_matrix_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6w02-supervised-live-read-approval-denial-matrix.md" in docs_index
    assert "tests/test_l6w02_supervised_live_read_approval_denial_matrix.py" in inventory
    assert "L6W.02 supervised live-read approval stale/variant denial matrix" in inventory
    assert "DENIAL_MATRIX_ONLY_NO_APPROVAL_NO_EXECUTION" in inventory


def test_l6w02_is_docs_tests_only_non_approval_no_execution():
    text = normalized(DOC)

    required_terms = [
        "Status: `DENIAL_MATRIX_ONLY_NO_APPROVAL_NO_EXECUTION`",
        "Rail issue: #200",
        "Prerequisite: #199 closed/PASS",
        "Source floor: `9264533` or later on `origin/main`",
        "Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`",
        "Scaffold dependency: `docs/l6w01-supervised-live-read-approval-packet-scaffold.md`",
        "docs/tests-only denial evidence",
        "does not approve, recognize, implement, or execute any live/private read",
        "`NO_APPROVAL_PRESENT`",
        "This packet does not grant that approval",
    ]
    for term in required_terms:
        assert term in text


def test_l6w02_covers_required_stale_variant_and_broadened_denial_shapes():
    text = normalized(DOC)

    for case in DENIAL_CASES:
        assert f"`{case}`" in text
    for reason in STOP_REASONS:
        assert f"`{reason}`" in text

    required_shape_terms = [
        "stale approval-like comment from L5/L6/L6U/L6V, #199, or any issue other than the exact future approval issue",
        "variant wording, renamed fields, paraphrased grant text, or altered operation-class spelling",
        "broadens source access, source discovery, workspace scans, family scans, broad recall, index queries, or raw content access",
        "copied approval text from another issue, rail, actor, subject, owner, audience, or operation class",
        "non-owner actor, wrong owner, wrong subject, wrong audience, or wrong scope",
        "missing `approval_expires_at`, expiry later than 12 hours after creation, or expired approval",
        "max operation count above one, multiple operation classes, multi-operation request, positive allowed result, or `allowed=true` route",
        "provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callback request",
        "service/listener/startup/cron activation or global Hermes/MCP/client/runtime config mutation request",
        "package publication, repository visibility change, provider/prod/canary authority, or production authority request",
        "Runtime Registry consumption, Atlas Gate movement, persistence/audit/custody record write, or cache mutation request",
        "write/custody/delete/reindex/rollback/cache-purge execution, mutation behavior, or rollback callback request",
    ]
    for term in required_shape_terms:
        assert term in text


def test_l6w02_requires_denial_before_callbacks_and_zero_synthetic_counters():
    text = normalized(DOC)

    assert text.count("`DENIED_BEFORE_CALLBACK`") >= 2
    required_result_terms = [
        "`approval_result`: `DENIED_BEFORE_CALLBACK`",
        "`live_read_invoked`: `false`",
        "`allowed`: `false`",
        "`allowed_result_count`: `0`",
        "guarded_callback_counters`: synthetic zeros",
        "deny before callbacks; no live/private read",
        "deny before any callback counter increments",
        "deny before mutation; no rollback callback",
    ]
    for term in required_result_terms:
        assert term in text
    for counter_term in ZERO_COUNTER_TERMS:
        assert counter_term in text


def test_l6w02_preserves_report_safety_and_hard_holds():
    text = normalized(DOC)

    report_safe_terms = [
        "safe refs, case ids, booleans, numeric counters, status strings, and stop-condition labels",
        "must not echo raw approval text",
        "raw source content",
        "credentials",
        "auth/env/keychain/OAuth/auth-file material",
        "raw platform IDs",
        "private absolute paths",
        "raw prompt/query payloads",
        "raw payload content",
        "raw backend responses",
        "private correlation refs",
        "source URIs",
        "Runtime Registry data",
        "persistence/audit/custody record bodies",
    ]
    for term in report_safe_terms:
        assert term in text

    held_terms = [
        "no-live/no-callback/no-production/no-persistence/no-activation/no-`allowed=true` boundaries",
        "source discovery",
        "Runtime Registry consumption",
        "persistence",
        "activation",
        "publication",
        "production/provider/prod/canary authority",
        "Atlas Gate movement",
        "mutation behavior",
        "`allowed=true` route",
    ]
    for term in held_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text
