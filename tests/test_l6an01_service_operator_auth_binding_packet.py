from __future__ import annotations

from pathlib import Path

from memory_seam.l6an_service_operator_auth_binding_packet import (
    L6AN01_BINDING_PROOF_SHAPE,
    L6AN01_NO_GO_SURFACES,
    L6AN01_RETRY_STATE,
    L6AN01_STATUS,
    assert_l6an01_packet_report_safe,
    build_l6an01_binding_proof_request,
    build_l6an01_exact_retry_binding,
    build_l6an01_service_operator_auth_binding_packet,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6an01-service-operator-auth-binding-unblock-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6an01_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6an01-service-operator-auth-binding-unblock-packet.md" in docs_index
    assert "tests/test_l6an01_service_operator_auth_binding_packet.py" in inventory
    assert "L6AN.01 service/operator auth-binding unblock packet" in inventory
    assert L6AN01_STATUS in inventory


def test_exact_retry_binding_uses_only_authorized_non_secret_labels() -> None:
    binding = build_l6an01_exact_retry_binding()

    assert binding == {
        "endpoint": "memory_seam_recall",
        "route_audience": "memory-seam:read:recall",
        "acting_for": "sax",
        "agent": "sax",
        "scope": "wiki",
        "n": 3,
        "query_label": "supervised_metadata_readiness",
        "query_text": "Memory Seam supervised metadata read retry source-floor readiness held surfaces denial-before-read",
        "evidence_class": "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE",
        "max_operation_count": 1,
        "report_safe_metadata_only": True,
        "denial_before_read_required": True,
    }


def test_binding_proof_request_names_reference_shape_without_authorizing_retry() -> None:
    proof = build_l6an01_binding_proof_request()

    assert proof["required_shape"] == list(L6AN01_BINDING_PROOF_SHAPE)
    assert proof["operator_service_binding_ref_required"] is True
    assert proof["expiry_or_one_run_custody_required"] is True
    assert proof["identity_subject_required"] == "supervised service caller bound to sax"
    assert proof["must_match"]["route_audience"] == "memory-seam:read:recall"
    assert proof["fresh_issue_bound_owner_or_service_owner_approval_required"] is True
    assert proof["may_contain_secret_material"] is False
    assert proof["retry_authorized_by_packet"] is False


def test_packet_records_l6am_safe_denial_and_keeps_retry_held_before_read() -> None:
    packet = build_l6an01_service_operator_auth_binding_packet()

    assert packet["status"] == L6AN01_STATUS
    assert packet["rail_issue"] == 370
    assert packet["rail_starting_source_floor"] == "c7574563ac1be1bf4c9c135586338ab760c0eb28"
    assert packet["retry_state"] == L6AN01_RETRY_STATE
    assert packet["safe_denial_metadata"] == {
        "endpoint": "memory_seam_recall",
        "auth_status": "denied_before_read",
        "auth_status_code": 403,
        "degraded_reasons": ["wrong_route_audience"],
        "item_count": 0,
        "safe_item_labels": [],
    }
    assert "parent successor receipt #6 comment 4656321058" in packet["approval_not_inferred_from"]
    assert "issue-bound preauth comment #370 4656320851" in packet["approval_not_inferred_from"]
    assert all(value == 0 for value in packet["guarded_counters"].values())
    assert_l6an01_packet_report_safe(packet)


def test_no_go_surfaces_remain_explicit_and_report_safe() -> None:
    packet = build_l6an01_service_operator_auth_binding_packet()

    for surface in (
        "live_retry",
        "secret_env_keychain_oauth_auth_file_credential_read",
        "runtime_registry_consumption",
        "provider_callback_or_service_activation",
        "source_discovery_or_broad_recall",
        "write_mutation_or_persistence",
        "provider_prod_canary_gate_movement",
        "broad_allowed_true",
    ):
        assert surface in L6AN01_NO_GO_SURFACES
        assert surface in packet["no_go_surfaces"]

    unsafe = packet | {"raw_private_source": "forbidden"}
    try:
        assert_l6an01_packet_report_safe(unsafe)
    except AssertionError as exc:
        assert "unexpected report fields" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unexpected raw field should fail closed")


def test_doc_names_operator_packet_acceptance_and_verification() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AN.01 service/operator auth-binding unblock packet",
        f"Status: `{L6AN01_STATUS}`",
        "Rail issue: #370",
        "Parent issue: #6",
        "Rail starting source floor: `c7574563ac1be1bf4c9c135586338ab760c0eb28`",
        "L6AM safe denial: `auth_status_code=403`, `wrong_route_audience`, `items=0`, safe item labels `[]`",
        "route_audience | `memory-seam:read:recall`",
        "acting_for | `sax`",
        "agent | `sax`",
        "scope | `wiki`",
        "query_label | `supervised_metadata_readiness`",
        "evidence_class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`",
        "max_operation_count | `1`",
        "report_safe_metadata_only | `true`",
        "denial_before_read_required | `true`",
        "operator/service binding reference with expiry or one-run custody",
        L6AN01_RETRY_STATE,
        "does not authorize, perform, or schedule a retry",
        "python -m pytest -q tests/test_l6an01_service_operator_auth_binding_packet.py",
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
