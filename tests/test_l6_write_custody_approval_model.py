from __future__ import annotations

from pathlib import Path

from memory_seam.write_custody_approval import (
    L6_WRITE_CUSTODY_APPROVAL_FIXTURES,
    L6_WRITE_CUSTODY_APPROVAL_REQUIRED_FIELDS,
    L6_WRITE_CUSTODY_APPROVAL_SCHEMA_VERSION,
    L6_WRITE_CUSTODY_APPROVAL_STATUS,
    L6_WRITE_CUSTODY_HELD_SURFACES,
    L6_WRITE_CUSTODY_OPERATION_CLASSES,
    L6_WRITE_CUSTODY_REQUIRED_APPROVAL_FIELDS,
    build_l6_write_custody_approval_fixtures,
    validate_l6_write_custody_approval_fixture,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-write-custody-approval-model.md"
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


def test_approval_model_doc_is_non_executing_and_preserves_holds():
    text = normalized(DOC)

    required_terms = [
        "L6S.01 write/custody ownership and approval model",
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
        "This L6S.01 packet is not approval.",
    ]
    for term in required_terms:
        assert term in text


def test_approval_model_doc_names_exact_approval_fields_and_ownership_roles():
    text = normalized(DOC)

    required_terms = [
        "Required approval fields",
        "`approval_phrase_ref`",
        "`approval_issue`",
        "`operation_class`",
        "`custody_owner_role`",
        "`approver_role`",
        "`actor_binding`",
        "`expires_at`",
        "`max_operation_count`",
        "`report_safe_reference`",
        "The `custody_owner_role` is accountable",
        "The `approver_role` is the human approval authority",
        "The `actor_binding` must name the exact future actor and acting-for subject",
        "A broad agent class, implied repo access, merge permission, or cron identity is insufficient.",
        "Ownership does not transfer just because a schema fixture exists, a PR merges, or an issue closes.",
    ]
    for term in required_terms:
        assert term in text


def test_approval_model_doc_lists_operation_classes_and_report_safety_rules():
    text = normalized(DOC)

    for operation_class in L6_WRITE_CUSTODY_OPERATION_CLASSES:
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


def test_approval_schema_fixtures_cover_required_operation_classes_without_side_effects():
    fixtures = build_l6_write_custody_approval_fixtures()

    assert L6_WRITE_CUSTODY_APPROVAL_STATUS == "schema_fixture_implementation_held"
    assert {fixture["operation_class"] for fixture in fixtures} == set(L6_WRITE_CUSTODY_OPERATION_CLASSES)
    assert len(fixtures) == len(L6_WRITE_CUSTODY_OPERATION_CLASSES)
    for fixture in fixtures:
        assert set(L6_WRITE_CUSTODY_APPROVAL_REQUIRED_FIELDS).issubset(fixture)
        assert fixture["schema_version"] == L6_WRITE_CUSTODY_APPROVAL_SCHEMA_VERSION
        assert fixture["status"] == L6_WRITE_CUSTODY_APPROVAL_STATUS
        assert fixture["approval_state"] == "not_approved_schema_only"
        assert fixture["max_operation_count"] == 1
        assert tuple(fixture["held_surfaces"]) == L6_WRITE_CUSTODY_HELD_SURFACES
        assert all(value == 0 for value in fixture["side_effects"].values())
        assert validate_l6_write_custody_approval_fixture(fixture) == []


def test_approval_schema_requires_actor_expiry_count_and_report_safe_reference():
    fixture = build_l6_write_custody_approval_fixtures()[0]

    for field in L6_WRITE_CUSTODY_REQUIRED_APPROVAL_FIELDS:
        assert fixture[field]
    assert fixture["custody_owner_role"] == "named_memory_custody_owner_required"
    assert fixture["approver_role"] == "jeremy_exact_human_approver_required"
    assert fixture["actor_binding"] == "named_actor_and_acting_for_subject_required"
    assert fixture["expires_at"] == "future_expiry_timestamp_required"
    assert fixture["report_safe_reference"] == "approval-reference-public-safe-redacted-link"


def test_approval_fixtures_are_report_safe_and_do_not_echo_private_material():
    fixtures = build_l6_write_custody_approval_fixtures()
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


def test_approval_fixture_validator_rejects_regressions_with_safe_error_codes():
    fixture = build_l6_write_custody_approval_fixtures()[0]
    fixture["max_operation_count"] = 0
    fixture["actor_binding"] = ""
    fixture["side_effects"]["write_callbacks"] = 1
    fixture["report_safety"]["raw_payload_content"] = True
    fixture["held_surfaces"] = tuple(
        surface for surface in fixture["held_surfaces"] if surface != "write_execution"
    )

    errors = validate_l6_write_custody_approval_fixture(fixture)

    assert errors == [
        "missing_required_approval_field_actor_binding",
        "invalid_max_operation_count",
        "nonzero_side_effect_counter",
        "unsafe_report_safety_flag",
        "missing_held_surface_write_execution",
    ]


def test_builder_returns_copies_so_approval_fixture_contract_stays_stable():
    fixtures = build_l6_write_custody_approval_fixtures()
    fixtures[0]["side_effects"]["write_callbacks"] = 1
    fixtures[0]["report_safety"]["credentials_or_auth_material"] = True

    fresh_fixtures = build_l6_write_custody_approval_fixtures()

    assert fresh_fixtures[0]["side_effects"]["write_callbacks"] == 0
    assert fresh_fixtures[0]["report_safety"]["credentials_or_auth_material"] is False
    assert L6_WRITE_CUSTODY_APPROVAL_FIXTURES[0]["side_effects"]["write_callbacks"] == 0


def test_approval_model_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-write-custody-approval-model.md" in docs_index
    assert "tests/test_l6_write_custody_approval_model.py" in inventory
    assert "L6S.01 write/custody ownership and approval model" in inventory
