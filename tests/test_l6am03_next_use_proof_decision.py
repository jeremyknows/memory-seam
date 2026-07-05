from __future__ import annotations

from pathlib import Path

from memory_seam.l6am_next_use_proof_decision import (
    L6AM03_DECISION,
    L6AM03_MISSING_BINDING_FIELDS,
    L6AM03_NEXT_FRONTIER,
    L6AM03_STATUS,
    L6AM03_STOP_CONDITIONS,
    L6AM03_USER_VISIBLE_PROOF_STATE,
    assert_l6am03_decision_report_safe,
    build_l6am03_auth_unblock_packet,
    build_l6am03_next_use_proof_decision,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6am03-next-use-proof-auth-unblock-decision.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6am03_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6am03-next-use-proof-auth-unblock-decision.md" in docs_index
    assert "tests/test_l6am03_next_use_proof_decision.py" in inventory
    assert "L6AM.03 next use-proof auth-unblock decision" in inventory
    assert L6AM03_STATUS in inventory


def test_decision_chooses_auth_unblock_after_l6am02_denied_empty_result() -> None:
    decision = build_l6am03_next_use_proof_decision()

    assert decision["status"] == L6AM03_STATUS
    assert decision["decision"] == L6AM03_DECISION
    assert decision["next_frontier"] == L6AM03_NEXT_FRONTIER
    assert decision["user_visible_proof_state"] == L6AM03_USER_VISIBLE_PROOF_STATE
    assert decision["retry_result_metadata"] == {
        "endpoint": "memory_seam_recall",
        "auth_status": "denied_before_read",
        "auth_status_code": 403,
        "degraded": True,
        "degraded_reasons": ["wrong_route_audience"],
        "item_count": 0,
        "safe_item_labels": [],
    }
    assert "route_audience=memory-seam:read:recall (recall endpoint)" in decision["missing_binding_fields"]
    assert "operator/service binding reference with expiry or one-run custody" in decision[
        "missing_binding_fields"
    ]
    assert all(value == 0 for value in decision["guarded_counters"].values())
    assert_l6am03_decision_report_safe(decision)


def test_auth_unblock_packet_binds_exact_future_retry_without_authorizing_it() -> None:
    packet = build_l6am03_auth_unblock_packet()

    assert packet["operation_class"] == L6AM03_NEXT_FRONTIER
    assert packet["endpoint"] == "memory_seam_recall"
    assert packet["route_audience_required"] == "memory-seam:read:recall"
    assert packet["acting_for_required"] == "sax"
    assert packet["agent_required"] == "sax"
    assert packet["scope_required"] == "wiki"
    assert packet["n_required"] == 3
    assert packet["query_label_required"] == "supervised_metadata_readiness"
    assert packet["evidence_class_required"] == "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
    assert packet["max_operation_count"] == 1
    assert packet["report_safe_metadata_only"] is True
    assert packet["denial_before_read_required"] is True
    assert packet["requires_fresh_operator_service_binding"] is True
    assert "L6AM.02 safe-denial receipt" in packet["approval_not_inferred_from"]


def test_missing_binding_fields_and_stop_conditions_are_exact() -> None:
    assert "route_audience=memory-seam:read:recall (recall endpoint)" in L6AM03_MISSING_BINDING_FIELDS
    assert "identity_subject bound to the supervised service caller" in L6AM03_MISSING_BINDING_FIELDS
    assert "acting_for=sax" in L6AM03_MISSING_BINDING_FIELDS
    assert "operator/service binding reference with expiry or one-run custody" in L6AM03_MISSING_BINDING_FIELDS

    for stop in (
        "auth_status_code_403",
        "wrong_route_audience",
        "unauthorized_narrowing",
        "empty_items",
        "source_discovery_or_broad_recall_request",
        "runtime_registry_or_provider_callback_request",
        "service_activation_or_prod_canary_gate_request",
        "write_mutation_or_persistence_request",
        "broad_allowed_true_request",
    ):
        assert stop in L6AM03_STOP_CONDITIONS


def test_doc_names_plain_english_progress_and_exact_next_packet() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AM.03 next use-proof auth-unblock decision",
        f"Status: `{L6AM03_STATUS}`",
        "Rail issue: #359",
        "Parent issue: #6",
        "Rail starting source floor: `9ea7cd0ab724292b8a2841c9e2c080f14a524ee2`",
        "L6AM.02 returned a real, bounded service denial, not another theoretical hold.",
        "safe retry metadata: `auth_status_code=403`, `wrong_route_audience`, `items=0`, safe item labels `[]`",
        L6AM03_DECISION,
        L6AM03_NEXT_FRONTIER,
        L6AM03_USER_VISIBLE_PROOF_STATE,
        "route_audience=memory-seam:read:recall (recall endpoint)",
        "identity_subject bound to the supervised service caller",
        "acting_for=sax",
        "operator/service binding reference with expiry or one-run custody",
        "current-session usefulness proof and fresh-agent proof remain held until the exact metadata retry returns safe labels/items",
        "No additional live read retry was performed for L6AM.03.",
        "python -m pytest -q tests/test_l6am03_next_use_proof_decision.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
