from __future__ import annotations

from pathlib import Path

from memory_seam.l6aa_value_proof import (
    L6AA_DESCRIPTOR_REF,
    L6AA_GUARDED_COUNTERS,
    L6AA_PASS_STATUS,
    L6AA_SOURCE_CARD_REF,
    approval_matches_l6aa_packet,
    execute_l6aa02_value_proof,
    validate_l6aa_value_proof_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aa02-owner-approved-one-read-value-proof.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVALUATED_AT = "2026-06-08T15:35:55Z"

APPROVAL_CONTEXT = {
    "approval_comment_id": "4650520977",
    "approval_comment_author": "jeremyknows",
    "owner_actor_association": "OWNER",
    "approval_comment_created_at": "2026-06-08T15:22:54Z",
    "packet_issue_id": "#241",
    "read_issue_id": "#242",
    "parent_issue_id": "#6",
    "subject": "jeremyknows/memory-seam",
    "audience": "L6AA owner-approved target-ref live-read value proof",
    "scope": "one report-safe source-card read",
    "operation_class": "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ",
    "max_operation_count": 1,
    "descriptor_ref": L6AA_DESCRIPTOR_REF,
    "source_card_ref": L6AA_SOURCE_CARD_REF,
    "source_floor_requirement": "b141f7be878a5b0d136cced3beb12ef38f0a25c9 or later",
    "preauth_anchor_refs_present": True,
    "report_safe_output_only": True,
    "deny_before_read_on_mismatch": True,
}

SAFE_SOURCE_CARD_METADATA = {
    "card_id": "l6aa-report-safe-operator-preference-card",
    "source_tier": "operator-preference-card",
    "private_class": "report-safe-redacted",
    "canonicality": "current-preference-signal",
    "retrieval_backend": "supervised-one-read-source-card",
    "title": "Operator preference card metadata",
    "safe_summary": "Report-safe metadata confirms a bounded operator-preference card was available for usefulness proof; raw source content is omitted.",
    "reportable": True,
    "redaction_applied": True,
    "redaction_labels": ["raw-source-content-omitted", "credential-material-not-read"],
}

UNSAFE_PAYLOADS = (
    {"raw_private_source_text": "raw private source text: example"},
    {"private_absolute_path": "private absolute path: /private/example/source-card.md"},
    {"source_uri": "source://private/example"},
    {"platform_id": "platform-raw-id-123"},
    {"prompt_payload": "raw prompt"},
    {"query_payload": "raw query"},
    {"backend_response": "raw backend response"},
    {"credential_value": "credential value: example"},
    {"oauth_token": "oauth token: example"},
    {"approval_text": "I approve exactly one supervised source-card read"},
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def read_exact_report_safe_card(descriptor_ref: str, source_card_ref: str) -> dict[str, object]:
    assert descriptor_ref == L6AA_DESCRIPTOR_REF
    assert source_card_ref == L6AA_SOURCE_CARD_REF
    return dict(SAFE_SOURCE_CARD_METADATA)


def test_l6aa02_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aa02-owner-approved-one-read-value-proof.md" in docs_index
    assert "tests/test_l6aa02_owner_approved_value_proof.py" in inventory
    assert "L6AA.02 owner-approved one-read value proof" in inventory
    assert "PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ" in inventory


def test_l6aa02_doc_records_live_approval_check_and_source_floor():
    text = normalized(DOC)

    required_terms = (
        "Status: `PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ`",
        "Rail issue: #242",
        "Prerequisite packet issue: #241 closed/PASS",
        "Parent issue: #6",
        "Source floor verified before work: `169bcaf040277441f5f4b2a2e90f3f894817046d`",
        "#242 owner comment `4650520977`",
        "owner_actor_association: `OWNER`",
        "freshness_result: `FRESH_WITHIN_12H`",
        "descriptor:l6aa/report-safe-operator-preference-card",
        "source-card:l6aa/report-safe-operator-preference-card",
        "exactly one supervised report-safe source-card read",
        "no raw private source content is reported",
    )
    for term in required_terms:
        assert term in text


def test_l6aa02_approval_matches_exact_packet_and_executes_one_read():
    call_count = 0

    def reader(descriptor_ref: str, source_card_ref: str) -> dict[str, object]:
        nonlocal call_count
        call_count += 1
        return read_exact_report_safe_card(descriptor_ref, source_card_ref)

    assert approval_matches_l6aa_packet(APPROVAL_CONTEXT, evaluated_at=EVALUATED_AT)
    receipt = execute_l6aa02_value_proof(
        APPROVAL_CONTEXT,
        evaluated_at=EVALUATED_AT,
        read_report_safe_source_card=reader,
    )

    assert call_count == 1
    assert validate_l6aa_value_proof_receipt(receipt) == []
    assert receipt["receipt_status"] == L6AA_PASS_STATUS
    assert receipt["approval_result"] == "APPROVED_EXACT_OWNER_ISSUE_BOUND_FRESH_TARGET_REF_MATCH"
    assert receipt["live_read_invoked"] is True
    assert receipt["allowed"] == "EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY"
    assert receipt["allowed_result_count"] == 1
    assert receipt["operation_count_attempted"] == 1
    assert receipt["read_usefulness_label"] == "USEFUL_REPORT_SAFE_OPERATOR_PREFERENCE_METADATA_SEEN"
    assert "safe_summary" in receipt["source_card_report_safe_fields_seen"]


def test_l6aa02_denies_before_read_for_stale_mismatched_broadened_or_non_owner():
    variants = []
    for field, value in (
        ("read_issue_id", "#6"),
        ("owner_actor_association", "MEMBER"),
        ("operation_class", "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ_PLUS_CALLBACKS"),
        ("max_operation_count", 2),
        ("descriptor_ref", "descriptor:l6z/operator-proof"),
        ("source_card_ref", "source-card:l6aa/other-card"),
        ("approval_comment_created_at", "2026-06-07T15:22:54Z"),
        ("report_safe_output_only", False),
    ):
        variant = dict(APPROVAL_CONTEXT)
        variant[field] = value
        variants.append(variant)

    for variant in variants:
        called = False

        def reader(_descriptor_ref: str, _source_card_ref: str) -> dict[str, object]:
            nonlocal called
            called = True
            return dict(SAFE_SOURCE_CARD_METADATA)

        receipt = execute_l6aa02_value_proof(
            variant,
            evaluated_at=EVALUATED_AT,
            read_report_safe_source_card=reader,
        )
        assert called is False
        assert receipt["receipt_status"] == "HOLD_DENIED_BEFORE_READ"
        assert receipt["live_read_invoked"] is False
        assert receipt["allowed"] is False
        assert receipt["allowed_result_count"] == 0
        assert receipt["operation_count_attempted"] == 0
        assert validate_l6aa_value_proof_receipt(receipt) == []
        for counter in L6AA_GUARDED_COUNTERS:
            expected = 1 if counter == "approval_comments_examined" else 0
            assert receipt["guarded_counters"][counter] == expected


def test_l6aa02_rejects_unsafe_source_card_metadata_before_report():
    for unsafe_payload in UNSAFE_PAYLOADS:
        receipt = execute_l6aa02_value_proof(
            APPROVAL_CONTEXT,
            evaluated_at=EVALUATED_AT,
            read_report_safe_source_card=lambda _descriptor_ref, _source_card_ref: unsafe_payload,
        )

        assert receipt["receipt_status"] == "HOLD_DENIED_BEFORE_READ"
        assert receipt["live_read_invoked"] is False
        assert "source_card_report_safe_fields_seen" in receipt
        assert receipt["source_card_report_safe_fields_seen"] == []


def test_l6aa02_receipt_validator_rejects_raw_echoes_and_allowed_true_broadening():
    receipt = execute_l6aa02_value_proof(
        APPROVAL_CONTEXT,
        evaluated_at=EVALUATED_AT,
        read_report_safe_source_card=read_exact_report_safe_card,
    )
    mutated = dict(receipt)
    mutated["allowed"] = True
    assert "allowed_broadened_or_missing" in validate_l6aa_value_proof_receipt(mutated)

    raw = dict(receipt)
    raw["raw_private_source_text"] = "raw private source text: example"
    errors = validate_l6aa_value_proof_receipt(raw)
    assert "unsafe_receipt_field_present" in errors
    assert "unsafe_receipt_key_present" in errors
    assert "unsafe_echo_marker_present" in errors
