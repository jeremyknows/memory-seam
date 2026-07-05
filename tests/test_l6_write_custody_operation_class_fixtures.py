from __future__ import annotations

from pathlib import Path

from memory_seam.write_custody_operation_classes import (
    L6_WRITE_CUSTODY_OPERATION_CLASS_FIXTURES,
    L6_WRITE_CUSTODY_OPERATION_CLASS_HELD_SURFACES,
    L6_WRITE_CUSTODY_OPERATION_CLASS_NAMES,
    L6_WRITE_CUSTODY_OPERATION_CLASS_REQUIRED_FIELDS,
    L6_WRITE_CUSTODY_OPERATION_CLASS_SCHEMA_VERSION,
    L6_WRITE_CUSTODY_OPERATION_CLASS_STATUS,
    build_l6_write_custody_operation_class_fixtures,
    validate_l6_write_custody_operation_class_fixture,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-write-custody-operation-class-fixtures.md"
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


def test_operation_class_doc_is_non_executing_and_preserves_holds():
    text = normalized(DOC)

    required_terms = [
        "L6S.03 operation-class schema fixtures for future write/custody slice",
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
        "This L6S.03 packet is not approval.",
    ]
    for term in required_terms:
        assert term in text


def test_operation_class_doc_names_required_fields_and_classes():
    text = normalized(DOC)

    required_terms = [
        "Every fixture carries",
        "Covered operation classes",
        "Required references",
        "Denied/no-op posture",
        "`runtime_route.supported`: `False`",
        "`runtime_route.registered`: `False`",
        "`runtime_route.executable`: `False`",
        "`denied_before_mutation`: `True`",
        "`no_op_only`: `True`",
    ]
    for term in required_terms:
        assert term in text
    for field in L6_WRITE_CUSTODY_OPERATION_CLASS_REQUIRED_FIELDS:
        assert f"`{field}`" in text
    for operation_class in L6_WRITE_CUSTODY_OPERATION_CLASS_NAMES:
        assert f"`{operation_class}`" in text


def test_operation_class_doc_lists_report_safety_rules():
    text = normalized(DOC)

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


def test_operation_class_schema_fixtures_cover_required_classes_without_side_effects():
    fixtures = build_l6_write_custody_operation_class_fixtures()

    assert L6_WRITE_CUSTODY_OPERATION_CLASS_STATUS == "schema_fixture_implementation_held"
    assert len(fixtures) == len(L6_WRITE_CUSTODY_OPERATION_CLASS_NAMES)
    assert tuple(fixture["operation_class"] for fixture in fixtures) == L6_WRITE_CUSTODY_OPERATION_CLASS_NAMES
    for fixture in fixtures:
        assert set(L6_WRITE_CUSTODY_OPERATION_CLASS_REQUIRED_FIELDS).issubset(fixture)
        assert fixture["schema_version"] == L6_WRITE_CUSTODY_OPERATION_CLASS_SCHEMA_VERSION
        assert fixture["status"] == L6_WRITE_CUSTODY_OPERATION_CLASS_STATUS
        assert tuple(fixture["held_surfaces"]) == L6_WRITE_CUSTODY_OPERATION_CLASS_HELD_SURFACES
        assert all(value == 0 for value in fixture["side_effects"].values())
        assert validate_l6_write_custody_operation_class_fixture(fixture) == []


def test_operation_class_fixtures_require_owner_count_timeout_rollback_and_approval_refs():
    for fixture in build_l6_write_custody_operation_class_fixtures():
        assert fixture["custody_owner_role"] == "named_memory_custody_owner_required"
        assert fixture["max_operation_count"] == 1
        assert fixture["timeout_ref"] == "future_slice_timeout_required_before_execution"
        assert fixture["rollback_ref"] == "l6s-02-rollback-audit-plan-public-safe-fixture"
        assert fixture["approval_ref"] == "l6s-01-approval-model-public-safe-reference-required"


def test_operation_class_fixtures_are_denied_noop_and_not_runtime_routes():
    for fixture in build_l6_write_custody_operation_class_fixtures():
        assert fixture["runtime_route"] == {
            "supported": False,
            "registered": False,
            "executable": False,
            "authority": "held_until_exact_jeremy_approval",
        }
        assert fixture["denied_before_mutation"] is True
        assert fixture["no_op_only"] is True
        assert "write_execution" in fixture["held_surfaces"]
        assert "custody_transfer" in fixture["held_surfaces"]
        assert "delete_execution" in fixture["held_surfaces"]
        assert "reindex_execution" in fixture["held_surfaces"]
        assert "rollback_execution" in fixture["held_surfaces"]
        assert "cache_purge_execution" in fixture["held_surfaces"]


def test_operation_class_fixtures_are_report_safe_and_do_not_echo_private_material():
    fixtures = build_l6_write_custody_operation_class_fixtures()
    rendered = repr(fixtures)

    for marker in PRIVATE_MARKERS:
        assert marker not in rendered
    for fixture in fixtures:
        assert fixture["report_safety"] == {
            "raw_private_text": False,
            "credentials_or_auth_material": False,
            "private_paths": False,
            "raw_platform_ids": False,
            "raw_query_payloads": False,
            "raw_payload_content": False,
            "private_correlation_refs": False,
        }


def test_operation_class_validator_rejects_regressions_with_safe_error_codes():
    fixture = build_l6_write_custody_operation_class_fixtures()[0]
    fixture["operation_class"] = "unexpected"
    fixture["custody_owner_role"] = ""
    fixture["max_operation_count"] = 0
    fixture["timeout_ref"] = ""
    fixture["rollback_ref"] = ""
    fixture["approval_ref"] = ""
    fixture["runtime_route"]["supported"] = True
    fixture["denied_before_mutation"] = False
    fixture["no_op_only"] = False
    fixture["side_effects"]["write_callbacks"] = 1
    fixture["report_safety"]["raw_payload_content"] = True
    fixture["held_surfaces"] = tuple(
        surface for surface in fixture["held_surfaces"] if surface != "cache_purge_execution"
    )

    errors = validate_l6_write_custody_operation_class_fixture(fixture)

    assert errors == [
        "unexpected_operation_class",
        "missing_custody_owner_role",
        "invalid_max_operation_count",
        "missing_timeout_ref",
        "missing_rollback_ref",
        "missing_approval_ref",
        "runtime_route_not_held",
        "denied_before_mutation_not_true",
        "no_op_only_not_true",
        "nonzero_side_effect_counter",
        "unsafe_report_safety_flag",
        "missing_held_surface_cache_purge_execution",
    ]


def test_builder_returns_copies_so_operation_class_contract_stays_stable():
    fixture = build_l6_write_custody_operation_class_fixtures()[0]
    fixture["side_effects"]["write_callbacks"] = 1
    fixture["report_safety"]["credentials_or_auth_material"] = True
    fixture["runtime_route"]["registered"] = True

    fresh_fixture = build_l6_write_custody_operation_class_fixtures()[0]

    assert fresh_fixture["side_effects"]["write_callbacks"] == 0
    assert fresh_fixture["report_safety"]["credentials_or_auth_material"] is False
    assert fresh_fixture["runtime_route"]["registered"] is False
    assert L6_WRITE_CUSTODY_OPERATION_CLASS_FIXTURES[0]["side_effects"]["write_callbacks"] == 0


def test_operation_class_fixture_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-write-custody-operation-class-fixtures.md" in docs_index
    assert "tests/test_l6_write_custody_operation_class_fixtures.py" in inventory
    assert "L6S.03 operation-class schema fixtures for future write/custody slice" in inventory
