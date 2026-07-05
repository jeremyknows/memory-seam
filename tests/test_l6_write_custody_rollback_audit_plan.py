from __future__ import annotations

from pathlib import Path

from memory_seam.write_custody_rollback_audit import (
    L6_WRITE_CUSTODY_ROLLBACK_AUDIT_FIXTURE,
    L6_WRITE_CUSTODY_ROLLBACK_AUDIT_HELD_SURFACES,
    L6_WRITE_CUSTODY_ROLLBACK_AUDIT_OPERATION_CLASSES,
    L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_AUDIT_FIELDS,
    L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FAILURE_MODES,
    L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FIELDS,
    L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_STOP_CONDITIONS,
    L6_WRITE_CUSTODY_ROLLBACK_AUDIT_SCHEMA_VERSION,
    L6_WRITE_CUSTODY_ROLLBACK_AUDIT_STATUS,
    build_l6_write_custody_rollback_audit_fixture,
    validate_l6_write_custody_rollback_audit_fixture,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-write-custody-rollback-audit-plan.md"
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


def test_rollback_audit_doc_is_non_executing_and_preserves_holds():
    text = normalized(DOC)

    required_terms = [
        "L6S.02 rollback and audit plan for first write/custody slice",
        "Status: `schema_fixture_implementation_held`",
        "Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`",
        "planning/design only",
        "does not implement, authorize, activate, schedule, simulate, or execute writes, custody transfer, delete, reindex, rollback, cache purge",
        "service/listener/cron/startup behavior",
        "source discovery",
        "unsupervised reads",
        "live/private source reads",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "provider/prod/canary authority",
        "repository visibility changes",
        "Atlas Gate movement",
        "This L6S.02 packet is not approval.",
    ]
    for term in required_terms:
        assert term in text


def test_rollback_audit_doc_names_required_plan_audit_stop_timeout_and_failure_fields():
    text = normalized(DOC)

    required_terms = [
        "Required rollback plan shape",
        "Required audit event fields",
        "Stop conditions",
        "Timeout and failure modes",
        "`plan_ref`",
        "`scope`",
        "`preconditions`",
        "`steps`",
        "`postconditions`",
        "`future_slice_timeout_required_before_execution`",
        "Recurring retry is forbidden and activation remains disallowed.",
        "Rollback planning is required, but rollback execution remains held.",
    ]
    for term in required_terms:
        assert term in text
    for field in L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_AUDIT_FIELDS:
        assert f"`{field}`" in text
    for stop_condition in L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_STOP_CONDITIONS:
        assert f"`{stop_condition}`" in text
    for failure_mode in L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FAILURE_MODES:
        assert f"`{failure_mode}`" in text


def test_rollback_audit_doc_lists_operation_classes_and_report_safety_rules():
    text = normalized(DOC)

    for operation_class in L6_WRITE_CUSTODY_ROLLBACK_AUDIT_OPERATION_CLASSES:
        assert f"`{operation_class}`" in text
    required_terms = [
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


def test_rollback_audit_schema_fixture_covers_required_fields_without_side_effects():
    fixture = build_l6_write_custody_rollback_audit_fixture()

    assert L6_WRITE_CUSTODY_ROLLBACK_AUDIT_STATUS == "schema_fixture_implementation_held"
    assert set(L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FIELDS).issubset(fixture)
    assert fixture["schema_version"] == L6_WRITE_CUSTODY_ROLLBACK_AUDIT_SCHEMA_VERSION
    assert fixture["status"] == L6_WRITE_CUSTODY_ROLLBACK_AUDIT_STATUS
    assert tuple(fixture["operation_classes"]) == L6_WRITE_CUSTODY_ROLLBACK_AUDIT_OPERATION_CLASSES
    assert tuple(fixture["held_surfaces"]) == L6_WRITE_CUSTODY_ROLLBACK_AUDIT_HELD_SURFACES
    assert all(value == 0 for value in fixture["side_effects"].values())
    assert validate_l6_write_custody_rollback_audit_fixture(fixture) == []


def test_rollback_audit_fixture_requires_plan_audit_stop_timeout_and_failure_shape():
    fixture = build_l6_write_custody_rollback_audit_fixture()

    assert fixture["rollback_plan"]["plan_ref"] == "rollback-plan-public-safe-fixture"
    assert "separate_future_rollback_approval_required_before_execution" in fixture["rollback_plan"]["preconditions"]
    assert tuple(fixture["audit_event_fields"]) == L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_AUDIT_FIELDS
    assert tuple(fixture["stop_conditions"]) == L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_STOP_CONDITIONS
    assert fixture["timeout"] == {
        "max_duration_ref": "future_slice_timeout_required_before_execution",
        "on_timeout": "stop_before_mutation_or_stop_after_bounded_future_operation_and_require_human_triage",
        "recurring_retry": False,
        "activation_allowed": False,
    }
    assert tuple(fixture["failure_modes"]) == L6_WRITE_CUSTODY_ROLLBACK_AUDIT_REQUIRED_FAILURE_MODES


def test_rollback_audit_fixture_keeps_runtime_mutation_unsupported_and_held():
    fixture = build_l6_write_custody_rollback_audit_fixture()

    assert fixture["runtime_mutation"] == {
        "supported": False,
        "attempted": False,
        "approval_from_this_fixture": False,
        "rollback_execution_supported": False,
    }
    assert "rollback_execution" in fixture["held_surfaces"]
    assert "write_execution" in fixture["held_surfaces"]
    assert "provider_backend_calls" in fixture["held_surfaces"]
    assert "live_private_source_reads" in fixture["held_surfaces"]


def test_rollback_audit_fixture_is_report_safe_and_does_not_echo_private_material():
    fixture = build_l6_write_custody_rollback_audit_fixture()
    rendered = repr(fixture)

    for marker in PRIVATE_MARKERS:
        assert marker not in rendered
    assert fixture["report_safety"] == {
        "raw_private_text": False,
        "credentials_or_auth_material": False,
        "private_paths": False,
        "raw_platform_ids": False,
        "raw_query_payloads": False,
        "raw_payload_content": False,
        "private_correlation_refs": False,
    }


def test_rollback_audit_validator_rejects_regressions_with_safe_error_codes():
    fixture = build_l6_write_custody_rollback_audit_fixture()
    fixture["rollback_plan"] = {}
    fixture["audit_event_fields"] = tuple(
        field for field in fixture["audit_event_fields"] if field != "approval_ref"
    )
    fixture["stop_conditions"] = tuple(
        condition for condition in fixture["stop_conditions"] if condition != "timeout_elapsed"
    )
    fixture["failure_modes"] = tuple(
        mode for mode in fixture["failure_modes"] if mode != "do_not_retry_automatically"
    )
    fixture["timeout"]["activation_allowed"] = True
    fixture["runtime_mutation"]["supported"] = True
    fixture["side_effects"]["rollback_callbacks"] = 1
    fixture["report_safety"]["raw_payload_content"] = True
    fixture["held_surfaces"] = tuple(
        surface for surface in fixture["held_surfaces"] if surface != "rollback_execution"
    )

    errors = validate_l6_write_custody_rollback_audit_fixture(fixture)

    assert errors == [
        "missing_rollback_plan",
        "missing_audit_field_approval_ref",
        "missing_stop_condition_timeout_elapsed",
        "missing_failure_mode_do_not_retry_automatically",
        "invalid_timeout_plan",
        "runtime_mutation_not_held",
        "nonzero_side_effect_counter",
        "unsafe_report_safety_flag",
        "missing_held_surface_rollback_execution",
    ]


def test_builder_returns_copies_so_rollback_audit_contract_stays_stable():
    fixture = build_l6_write_custody_rollback_audit_fixture()
    fixture["side_effects"]["rollback_callbacks"] = 1
    fixture["report_safety"]["credentials_or_auth_material"] = True
    fixture["rollback_plan"]["plan_ref"] = "changed"

    fresh_fixture = build_l6_write_custody_rollback_audit_fixture()

    assert fresh_fixture["side_effects"]["rollback_callbacks"] == 0
    assert fresh_fixture["report_safety"]["credentials_or_auth_material"] is False
    assert fresh_fixture["rollback_plan"]["plan_ref"] == "rollback-plan-public-safe-fixture"
    assert L6_WRITE_CUSTODY_ROLLBACK_AUDIT_FIXTURE["side_effects"]["rollback_callbacks"] == 0


def test_rollback_audit_plan_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-write-custody-rollback-audit-plan.md" in docs_index
    assert "tests/test_l6_write_custody_rollback_audit_plan.py" in inventory
    assert "L6S.02 rollback and audit plan for first write/custody slice" in inventory
