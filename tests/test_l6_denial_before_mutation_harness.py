from __future__ import annotations

from pathlib import Path

from l6_denial_before_mutation_harness_helper import (
    L6_DENIAL_BEFORE_MUTATION_AUTHORITY,
    L6_DENIAL_BEFORE_MUTATION_CALLBACKS,
    L6_DENIAL_BEFORE_MUTATION_FIXTURE,
    L6_DENIAL_BEFORE_MUTATION_HELD_SURFACES,
    L6_DENIAL_BEFORE_MUTATION_OPERATION_CLASSES,
    L6_DENIAL_BEFORE_MUTATION_REPORT_SAFETY,
    L6_DENIAL_BEFORE_MUTATION_SCHEMA_VERSION,
    L6_DENIAL_BEFORE_MUTATION_STATUS,
    SyntheticCallbackHarness,
    build_l6_denial_before_mutation_fixture,
    run_denied_before_mutation_preflight,
    validate_l6_denial_before_mutation_result,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-denial-before-mutation-harness.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_harness_doc_is_non_executing_and_preserves_holds():
    text = normalized(DOC)

    required_terms = [
        "L6S.04 denied-before-mutation callback harness",
        "Status: `denied_before_mutation_harness_non_executing`",
        "Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`",
        "planning/design only",
        "does not implement, authorize, activate, schedule, simulate, or execute writes, custody transfer, delete, reindex, rollback, cache purge",
        "provider/backend/source-stat/source-read callbacks",
        "service/listener/cron/startup behavior",
        "source discovery",
        "unsupervised reads",
        "live/private source reads",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "provider/prod/canary authority",
        "repository visibility changes",
        "Atlas Gate movement",
        "This L6S.04 packet is not approval.",
    ]
    for term in required_terms:
        assert term in text


def test_harness_doc_names_all_zero_callback_counters_and_report_safety():
    text = normalized(DOC)

    required_terms = [
        "Denied-before-mutation proof rule",
        "Synthetic callback bundle",
        "All guarded callback counters must remain `0`",
        "Known operation classes",
        "Unknown operation classes also deny before callbacks",
        "raw private source text",
        "credentials",
        "auth/env/keychain material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "raw payload content",
        "private correlation refs",
    ]
    for term in required_terms:
        assert term in text
    for callback_name in L6_DENIAL_BEFORE_MUTATION_CALLBACKS:
        assert f"`{callback_name}`" in text
    for operation_class in L6_DENIAL_BEFORE_MUTATION_OPERATION_CLASSES:
        assert f"`{operation_class}`" in text


def test_fixture_is_synthetic_noop_and_non_executable():
    fixture = build_l6_denial_before_mutation_fixture()

    assert fixture["schema_version"] == L6_DENIAL_BEFORE_MUTATION_SCHEMA_VERSION
    assert fixture["status"] == L6_DENIAL_BEFORE_MUTATION_STATUS
    assert fixture["authority"] == L6_DENIAL_BEFORE_MUTATION_AUTHORITY
    assert fixture["operation_classes"] == L6_DENIAL_BEFORE_MUTATION_OPERATION_CLASSES
    assert fixture["guarded_callbacks"] == L6_DENIAL_BEFORE_MUTATION_CALLBACKS
    assert fixture["preflight_result"] == "denied_before_mutation"
    assert fixture["mutation_possible"] is False
    assert fixture["callback_invocation_allowed"] is False
    assert fixture["synthetic_only"] is True
    assert fixture["runtime_route"] == {
        "supported": False,
        "registered": False,
        "executable": False,
        "authority": L6_DENIAL_BEFORE_MUTATION_AUTHORITY,
    }
    assert tuple(fixture["held_surfaces"]) == L6_DENIAL_BEFORE_MUTATION_HELD_SURFACES
    assert fixture["report_safety"] == L6_DENIAL_BEFORE_MUTATION_REPORT_SAFETY


def test_preflight_denies_each_known_operation_before_guarded_callbacks():
    for operation_class in L6_DENIAL_BEFORE_MUTATION_OPERATION_CLASSES:
        harness = SyntheticCallbackHarness.build()
        result = run_denied_before_mutation_preflight(operation_class, harness)

        assert result["operation_class"] == operation_class
        assert result["allowed"] is False
        assert result["denied_before_mutation"] is True
        assert result["denial_reason"] == "held_surface_preflight_denied"
        assert result["callbacks_invoked"] is False
        assert result["counters"] == {name: 0 for name in L6_DENIAL_BEFORE_MUTATION_CALLBACKS}
        assert harness.counters == {name: 0 for name in L6_DENIAL_BEFORE_MUTATION_CALLBACKS}
        assert validate_l6_denial_before_mutation_result(result) == []


def test_preflight_denies_unknown_operation_before_guarded_callbacks():
    harness = SyntheticCallbackHarness.build()
    result = run_denied_before_mutation_preflight("unknown_future_write_like_surface", harness)

    assert result["operation_class"] == "unknown_operation_class"
    assert result["allowed"] is False
    assert result["denied_before_mutation"] is True
    assert result["denial_reason"] == "unknown_operation_class_denied"
    assert result["callbacks_invoked"] is False
    assert result["counters"] == {name: 0 for name in L6_DENIAL_BEFORE_MUTATION_CALLBACKS}
    assert harness.counters == {name: 0 for name in L6_DENIAL_BEFORE_MUTATION_CALLBACKS}
    assert validate_l6_denial_before_mutation_result(result) == []


def test_guarded_callbacks_are_fail_fast_if_called_by_regression():
    harness = SyntheticCallbackHarness.build()
    callback_name = L6_DENIAL_BEFORE_MUTATION_CALLBACKS[0]

    try:
        harness.callbacks[callback_name]()
    except AssertionError as exc:
        assert str(exc) == f"unexpected_callback_invoked:{callback_name}"
    else:  # pragma: no cover - defensive proof that callback cannot silently pass
        raise AssertionError("callback unexpectedly returned")

    assert harness.counters[callback_name] == 1


def test_harness_validator_rejects_nonzero_or_authorizing_regressions_with_safe_codes():
    result = run_denied_before_mutation_preflight("write_intent")
    result["schema_version"] = "unexpected"
    result["status"] = "unexpected"
    result["allowed"] = True
    result["denied_before_mutation"] = False
    result["callbacks_invoked"] = True
    result["counters"]["write_callback"] = 1
    result["report_safety"]["raw_payload_content"] = True
    result["held_surfaces"] = tuple(
        surface for surface in result["held_surfaces"] if surface != "cache_purge_execution"
    )

    assert validate_l6_denial_before_mutation_result(result) == [
        "unexpected_schema_version",
        "unexpected_status",
        "allowed_not_false",
        "denied_before_mutation_not_true",
        "callbacks_invoked_not_false",
        "nonzero_counter_write_callback",
        "unsafe_report_safety_flag",
        "missing_held_surface_cache_purge_execution",
    ]


def test_builder_returns_copies_so_harness_fixture_stays_stable():
    fixture = build_l6_denial_before_mutation_fixture()
    fixture["runtime_route"]["registered"] = True
    fixture["report_safety"]["credentials_or_auth_material"] = True

    fresh_fixture = build_l6_denial_before_mutation_fixture()

    assert fresh_fixture["runtime_route"]["registered"] is False
    assert fresh_fixture["report_safety"]["credentials_or_auth_material"] is False
    assert L6_DENIAL_BEFORE_MUTATION_FIXTURE["runtime_route"]["registered"] is False


def test_harness_artifacts_are_report_safe_and_discoverable():
    fixture = build_l6_denial_before_mutation_fixture()
    rendered = repr(fixture) + repr(run_denied_before_mutation_preflight("write_intent"))

    for marker in PRIVATE_MARKERS:
        assert marker not in rendered
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)
    assert "l6-denial-before-mutation-harness.md" in docs_index
    assert "tests/test_l6_denial_before_mutation_harness.py" in inventory
    assert "L6S.04 denied-before-mutation callback harness" in inventory
