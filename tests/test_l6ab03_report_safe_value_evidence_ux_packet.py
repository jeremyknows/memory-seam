from __future__ import annotations

from pathlib import Path

from memory_seam.l6ab_value_comparison import (
    L6AB03_FUTURE_APPROVAL_TEMPLATE,
    L6AB03_REQUIRED_NOT_PROVES,
    L6AB03_REQUIRED_PROVES,
    L6AB03_SAFE_PACKET_FIELDS,
    L6AB03_SCHEMA_VERSION,
    L6AB03_STATUS,
    build_l6ab03_value_evidence_ux_packet,
    validate_l6ab03_value_evidence_ux_packet,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ab03-report-safe-value-evidence-ux-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ab03_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ab03-report-safe-value-evidence-ux-packet.md" in docs_index
    assert "tests/test_l6ab03_report_safe_value_evidence_ux_packet.py" in inventory
    assert "L6AB.03 report-safe value evidence UX packet" in inventory
    assert L6AB03_STATUS in inventory


def test_l6ab03_doc_headline_consumed_read_and_future_template():
    text = normalized(DOC)

    required_terms = (
        "Status: `REPORT_SAFE_VALUE_EVIDENCE_UX_PACKET_NO_LIVE_READS`",
        "Rail issue: #253",
        "Parent issue: #6",
        "Depends on: #252 closed/PASS",
        "Useful report-safe value was proven once",
        "#242/#245 consumed exactly one report-safe source-card read",
        "is not reusable approval",
        "Future approval template text only",
        "inert documentation only",
        "It is not active authorization",
        "raw private content",
        "raw approval text",
        "source URIs",
        "private paths",
        "prompts, queries",
        "backend responses",
        "credentials, or auth material",
        "no broad allowed=true route",
    )
    for term in required_terms:
        assert term in text

    assert L6AB03_FUTURE_APPROVAL_TEMPLATE.startswith("I authorize exactly one future")
    assert "<ISSUE>" in L6AB03_FUTURE_APPROVAL_TEMPLATE
    assert "<DESCRIPTOR_REF>" in L6AB03_FUTURE_APPROVAL_TEMPLATE
    assert "<SOURCE_CARD_REF>" in L6AB03_FUTURE_APPROVAL_TEMPLATE


def test_l6ab03_packet_is_concise_report_safe_and_inert():
    packet = build_l6ab03_value_evidence_ux_packet()

    assert validate_l6ab03_value_evidence_ux_packet(packet) == []
    assert set(packet) == L6AB03_SAFE_PACKET_FIELDS
    assert packet["schema_version"] == L6AB03_SCHEMA_VERSION
    assert packet["status"] == L6AB03_STATUS
    assert packet["rail_issue_id"] == "#253"
    assert packet["depends_on"] == "#252 closed/PASS"
    assert packet["evidence_headline"].startswith("Useful report-safe value was proven once")
    assert "consumed exactly one report-safe source-card read" in packet["consumed_approval_read_statement"]
    assert "not reusable approval" in packet["consumed_approval_read_statement"]
    assert packet["future_approval_template_text_only"] == L6AB03_FUTURE_APPROVAL_TEMPLATE
    assert packet["template_is_active_authorization"] is False
    assert packet["report_safe"] is True


def test_l6ab03_packet_states_proves_not_proves_and_preserved_holds():
    packet = build_l6ab03_value_evidence_ux_packet()

    assert packet["what_the_evidence_proves"] == list(L6AB03_REQUIRED_PROVES)
    assert packet["what_the_evidence_does_not_prove"] == list(L6AB03_REQUIRED_NOT_PROVES)
    assert any("one historical report-safe source-card metadata receipt" in item for item in packet["what_the_evidence_proves"])
    assert any("does not prove ongoing permission" in item for item in packet["what_the_evidence_does_not_prove"])
    assert "no_live_or_private_reads" in packet["residual_holds"]
    assert "no_broad_allowed_true_route" in packet["residual_holds"]


def test_l6ab03_packet_rejects_unsafe_output_or_active_authorization():
    packet = build_l6ab03_value_evidence_ux_packet()

    unsafe_mutations = {
        "raw_private_content_included": "unsafe_raw_private_content_included",
        "raw_approval_text_included": "unsafe_raw_approval_text_included",
        "source_uri_included": "unsafe_source_uri_included",
        "private_path_included": "unsafe_private_path_included",
        "prompt_or_query_payload_included": "unsafe_prompt_or_query_payload_included",
        "backend_response_included": "unsafe_backend_response_included",
        "credential_or_auth_material_included": "unsafe_credential_or_auth_material_included",
        "live_read_invoked": "unsafe_live_read_invoked",
        "callbacks_invoked": "unsafe_callbacks_invoked",
    }
    for field, expected_error in unsafe_mutations.items():
        mutated = dict(packet) | {field: True}
        assert expected_error in validate_l6ab03_value_evidence_ux_packet(mutated)

    active_template = dict(packet) | {"template_is_active_authorization": True}
    assert "template_treated_as_active_authorization" in validate_l6ab03_value_evidence_ux_packet(active_template)

    wrong_template = dict(packet) | {"future_approval_template_text_only": "approval granted"}
    assert "unexpected_future_template" in validate_l6ab03_value_evidence_ux_packet(wrong_template)
