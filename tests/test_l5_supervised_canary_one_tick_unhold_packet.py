from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l5-supervised-canary-one-tick-unhold-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l5_supervised_canary_packet_is_no_execution_no_activation():
    text = normalized(DOC)

    required_terms = [
        "L5.08 supervised canary one-tick unhold packet",
        "NO-EXECUTION / NO-ACTIVATION decision packet",
        "Packet status: `DRAFT_PACKET_ONLY`",
        "Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`",
        "Activation authority: `HELD`",
        "does not run the bounded runner",
        "does not start any service/listener",
        "does not authorize execution by itself",
    ]
    for term in required_terms:
        assert term in text


def test_l5_supervised_canary_packet_names_exact_one_tick_scope():
    text = normalized(DOC)

    required_terms = [
        "exactly one tick; `max_ticks=1`",
        "Source family | `operator_supplied_project_doc_card` represented through the bounded-runner `project` family grant",
        "metadata-only project-document source-card fields only",
        "`agent:example` acting on one Jeremy/operator-supplied Memory Seam project-document source card",
        "`title`, `document_kind`, `section_label`, `safe_summary`, `freshness_label`, `redacted_source_card_id`",
        "Timeout | 30 seconds wall-clock for the one tick",
        "approval expires 30 minutes after Jeremy posts the exact phrase",
        "at most one metadata-only source-card read through the approved one-tick path",
    ]
    for term in required_terms:
        assert term in text


def test_l5_supervised_canary_packet_exact_future_approval_phrase_is_one_tick_only():
    text = normalized(DOC)
    approval_phrase = (
        "I approve Memory Seam to execute exactly one supervised bounded-runner canary tick "
        "under docs/l5-supervised-canary-one-tick-unhold-packet.md using one operator-supplied "
        "project-document source card, max_ticks=1, metadata-only fields only, a 30 second timeout, "
        "and a 30 minute approval expiry, with no source discovery, no raw content, no "
        "credential/auth/env/keychain/OAuth/auth-file reads, no service/listener/cron/startup "
        "activation, no Runtime Registry consumption, no global config mutation, no recurring or "
        "unsupervised reads, no provider/prod/canary authority beyond this one approved tick, no "
        "writes/custody/reindex, no repository visibility or package publication change, and no "
        "Atlas Gate movement."
    )

    assert approval_phrase in text
    assert "Any variant, partial quote, implied approval, emoji reaction, merge, issue close" in text
    assert "one supervised canary tick only" in text


def test_l5_supervised_canary_packet_preserves_hard_holds():
    text = normalized(DOC)

    required_terms = [
        "startup activation",
        "recurring unsupervised reads",
        "writes/custody/reindex",
        "provider/prod/canary authority beyond the one approved tick",
        "Atlas Gate movement",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "service/listener/cron activation",
        "source discovery",
        "live/private source reads before future approval",
        "raw private source text",
        "private absolute paths",
        "raw platform IDs",
        "raw query payloads",
        "private correlation refs",
        "credentials",
        "auth/env/keychain/OAuth/auth-file material",
        "repository visibility change",
        "package publication",
        "production-authoritative claims",
    ]
    for term in required_terms:
        assert term in text


def test_l5_supervised_canary_packet_records_future_evidence_requirements():
    text = normalized(DOC)

    required_terms = [
        "Required future evidence after an approved canary tick",
        "exact approval phrase location and expiry check",
        "tick count attempted and completed",
        "safe metadata fields returned or denial/degraded reason",
        "usefulness/verifier verdict and redaction posture",
        "denial/zero counters for source discovery",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "file-stat calls",
        "read-backend calls",
        "provider calls",
        "recurring runner activation",
        "public artifacts contain no raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, or private correlation refs",
    ]
    for term in required_terms:
        assert term in text


def test_l5_supervised_canary_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l5-supervised-canary-one-tick-unhold-packet.md" in docs_index
    assert "tests/test_l5_supervised_canary_one_tick_unhold_packet.py" in inventory
    assert "L5.08 supervised canary one-tick unhold packet" in inventory
