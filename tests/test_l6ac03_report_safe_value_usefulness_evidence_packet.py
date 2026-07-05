from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ac03-report-safe-value-usefulness-evidence-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_VALUE_USEFULNESS_EVIDENCE_PACKET_NO_LIVE_READS"
ISSUE = "#263"
PARENT = "#6"
L6AC02_SOURCE_FLOOR = "e954c2e37e7c643dbde71e3f8d371c4aee04011c"
RAIL_STARTING_SOURCE_FLOOR = "67a1a78db2b7adca0048497cce61412de13032f1"
DESCRIPTOR_REF = "descriptor:l6ac/report-safe-operator-preference-card"
SOURCE_CARD_REF = "source-card:l6ac/report-safe-operator-preference-card"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ac03_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ac03-report-safe-value-usefulness-evidence-packet.md" in docs_index
    assert "tests/test_l6ac03_report_safe_value_usefulness_evidence_packet.py" in inventory
    assert "L6AC.03 report-safe value/usefulness evidence packet" in inventory
    assert STATUS in inventory


def test_l6ac03_doc_headline_labels_pass_and_consumed_read_boundary():
    text = normalized(DOC)

    required_terms = (
        "# L6AC.03 report-safe value/usefulness evidence packet",
        f"Status: `{STATUS}`",
        "Rail issue: #263",
        "Parent issue: #6",
        "Depends on: #262 closed/PASS receipt",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"L6AC.02 merged source floor: `{L6AC02_SOURCE_FLOOR}`",
        "Useful report-safe value was proven in #262",
        "exactly one issue-bound OWNER-approved source-card read",
        "PASS/HOLD label",
        "does not perform a second read",
        "does not reactivate the consumed approval",
        "does not add execution authority",
    )
    for term in required_terms:
        assert term in text


def test_l6ac03_packet_defines_what_receipt_proves_and_does_not_prove():
    text = normalized(DOC)

    proves_terms = (
        "Exact issue-bound owner approval comment `4651509226`",
        "author `jeremyknows` and owner association `OWNER`",
        f"#261 supplied matching executable refs: `{DESCRIPTOR_REF}` and `{SOURCE_CARD_REF}`",
        "Exactly one `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` operation was attempted and completed in #262",
        "report-safe metadata/value evidence only",
        "guarded counters",
    )
    for term in proves_terms:
        assert term in text

    not_proves_terms = (
        "does not prove ongoing or reusable permission",
        "does not authorize #263, #264, #265",
        "raw private content",
        "raw approval prose",
        "source URIs",
        "private paths",
        "prompts, queries",
        "backend responses",
        "credentials, auth material",
        "Runtime Registry data",
        "broad `allowed=true` routing",
    )
    for term in not_proves_terms:
        assert term in text


def test_l6ac03_packet_puts_value_usefulness_evidence_first_without_new_authority():
    text = normalized(DOC)

    assert text.index("Evidence headline") < text.index("What the #262 receipt proves")
    assert "Value label: `USEFUL_REPORT_SAFE_OPERATOR_PREFERENCE_METADATA_SEEN`" in text
    assert "distinguish a real owner-approved, exact-target-ref PASS" in text
    assert "unsafe raw fields are rejected before report output" in text
    assert "#264 can review the trust boundary" in text
    assert "#265 can reconcile source floors and parent status" in text
    assert "This packet contains no new approval phrase" in text
    assert "must not be interpreted as permission" in text


def test_l6ac03_report_safe_contract_preserves_no_live_boundary():
    text = normalized(DOC)

    required_safety_fields = (
        "raw_private_content_included=false",
        "raw_approval_prose_included=false",
        "credential_or_auth_material_included=false",
        "runtime_registry_data_included=false",
        "source_discovery_or_scan_included=false",
        "live_read_invoked_by_this_packet=false",
        "callbacks_invoked_by_this_packet=false",
        "approval_reusable=false",
        "future_authority_created=false",
        "atlas_gate_moved=false",
        "broad_allowed_true_route=false",
    )
    for field in required_safety_fields:
        assert field in text

    residual_holds = (
        "#264 and #265 remain docs/tests/fixtures/review/reconciliation only",
        "No live/private read",
        "credentials/auth/env/keychain/OAuth/auth-file reads",
        "source discovery",
        "workspace/family scans",
        "broad recall/index queries",
        "Runtime Registry consumption",
        "persistence/mutation/write/delete/reindex/cache-purge/rollback execution",
        "service/global activation",
        "publication/visibility changes",
        "provider/prod/canary movement",
        "Atlas Gate movement",
        "second read",
        "broad `allowed=true` route",
    )
    for hold in residual_holds:
        assert hold in text

    unsafe_markers = (
        "raw private source text",
        "oauth token",
        "credential value",
        "auth-file material",
        "private-correlation-ref",
        "source://",
    )
    lowered = text.lower()
    for marker in unsafe_markers:
        assert marker not in lowered
