from __future__ import annotations

from pathlib import Path

from memory_seam.l6ao_auth_held_default_off_intake import (
    L6AO01_DEFAULT_OFF_FLAGS,
    L6AO01_INTAKE_STATE,
    L6AO01_PREAUTH_COMMENT,
    L6AO01_RETRY_STATE,
    L6AO01_STATUS,
    assert_l6ao01_receipt_report_safe,
    build_l6ao01_auth_held_default_off_intake_receipt,
    build_l6ao01_binding_intake_packet,
    build_l6ao01_source_blocker_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ao01-auth-held-default-off-binding-intake.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ao01_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ao01-auth-held-default-off-binding-intake.md" in docs_index
    assert "tests/test_l6ao01_auth_held_default_off_intake.py" in inventory
    assert "L6AO.01 auth-held blocker receipt and default-off binding intake" in inventory
    assert L6AO01_STATUS in inventory


def test_source_blocker_receipt_is_report_safe_and_auth_held() -> None:
    receipt = build_l6ao01_source_blocker_receipt()

    assert receipt == {
        "blocker": "auth_held_missing_fresh_operator_service_binding",
        "prior_denial_summary": "L6AM/L6AN safe denial: auth_status_code=403 wrong_route_audience items=0",
        "prior_request_class": "memory_seam_recall_report_safe_metadata_only_max_one",
        "default_decision": "deny_before_read_and_hold_retry",
        "source_floor": "57e8bd4612824ada20718e41b1eea33210fe2974",
        "raw_or_private_content_included": False,
        "credential_or_auth_material_included": False,
        "live_retry_executed": False,
    }


def test_binding_intake_packet_names_exact_non_secret_default_off_shape() -> None:
    intake = build_l6ao01_binding_intake_packet()

    for field in (
        "operator_service_binding_ref",
        "binding_owner",
        "identity_subject",
        "route_audience",
        "acting_for",
        "agent",
        "scope",
        "query_label",
        "evidence_class",
        "max_operation_count",
        "report_safe_metadata_only",
        "denial_before_read_required",
        "expires_at_or_one_run_custody",
        "issue_bound_authorization_ref",
    ):
        assert field in intake["required_fields"]

    assert intake["must_match"] == {
        "route_audience": "memory-seam:read:recall",
        "acting_for": "sax",
        "agent": "sax",
        "scope": "wiki",
        "query_label": "supervised_metadata_readiness",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "max_operation_count": 1,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
    }
    assert intake["may_contain_secret_material"] is False
    assert intake["may_contain_raw_private_or_source_content"] is False
    assert intake["runtime_or_provider_lookup_allowed"] is False
    assert intake["default_off_until_later_packet"] is True
    assert intake["retry_authorized_by_intake"] is False


def test_auth_held_default_off_receipt_keeps_retry_and_all_surfaces_off() -> None:
    receipt = build_l6ao01_auth_held_default_off_intake_receipt()

    assert receipt["schema_version"] == "l6ao01-auth-held-default-off-binding-intake-v1"
    assert receipt["repo"] == "jeremyknows/memory-seam"
    assert receipt["parent_issue"] == 6
    assert receipt["rail_issue"] == 380
    assert receipt["rail_starting_source_floor"] == "57e8bd4612824ada20718e41b1eea33210fe2974"
    assert receipt["status"] == L6AO01_STATUS
    assert receipt["preauth_comment"] == L6AO01_PREAUTH_COMMENT
    assert receipt["parent_rail_created_comment"] == "4656626203"
    assert receipt["retry_state"] == L6AO01_RETRY_STATE
    assert receipt["intake_state"] == L6AO01_INTAKE_STATE
    assert receipt["default_off_flags"] == L6AO01_DEFAULT_OFF_FLAGS
    assert all(value is False for value in receipt["default_off_flags"].values())
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert "issue-bound preauth comment #380 4656625129" in receipt["approval_not_inferred_from"]
    assert_l6ao01_receipt_report_safe(receipt)


def test_receipt_assertion_rejects_unsafe_or_enabled_surfaces() -> None:
    receipt = build_l6ao01_auth_held_default_off_intake_receipt()

    unsafe = receipt | {"raw_private_source": "forbidden"}
    try:
        assert_l6ao01_receipt_report_safe(unsafe)
    except AssertionError as exc:
        assert "unexpected L6AO.01 receipt fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unexpected raw field should fail closed")

    enabled = receipt | {"default_off_flags": receipt["default_off_flags"] | {"live_retry_enabled": True}}
    try:
        assert_l6ao01_receipt_report_safe(enabled)
    except AssertionError as exc:
        assert "default-off flags" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("enabled live retry flag should fail closed")


def test_doc_names_acceptance_boundaries_and_verification() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AO.01 auth-held blocker receipt and default-off binding intake",
        f"Status: `{L6AO01_STATUS}`",
        "Rail issue: #380",
        "Parent issue: #6",
        "Rail starting source floor: `57e8bd4612824ada20718e41b1eea33210fe2974`",
        "Preauth comment: `4656625129`",
        "Parent rail-created receipt: `4656626203`",
        "auth_held_missing_fresh_operator_service_binding",
        L6AO01_RETRY_STATE,
        "DEFAULT_OFF_REPORT_SAFE_NON_SECRET_BINDING_INTAKE_ONLY",
        "route_audience | `memory-seam:read:recall`",
        "acting_for | `sax`",
        "agent | `sax`",
        "scope | `wiki`",
        "query_label | `supervised_metadata_readiness`",
        "evidence_class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`",
        "max_operation_count | `1`",
        "report_safe_metadata_only | `true`",
        "denial_before_read_required | `true`",
        "issue_bound_authorization_ref",
        "does not authorize, perform, schedule, or enable a live retry",
        "python -m pytest -q tests/test_l6ao01_auth_held_default_off_intake.py",
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
        "private path value",
        "raw source text",
    ):
        assert forbidden_marker not in lowered
