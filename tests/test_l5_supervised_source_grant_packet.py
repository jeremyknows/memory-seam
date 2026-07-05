from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l5-supervised-source-grant-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l5_supervised_source_grant_packet_is_no_execution_no_read():
    text = normalized(DOC)

    required_terms = [
        "L5.02 supervised source-grant decision packet",
        "NO-EXECUTION / NO-READ decision packet",
        "Packet status: `DRAFT_PACKET_ONLY`",
        "Execution authority: `HELD`",
        "Read authority: `HELD`",
        "does not authorize execution by itself",
        "does not discover sources",
        "does not read private content",
        "does not start any service or recurring runner",
    ]
    for term in required_terms:
        assert term in text


def test_l5_supervised_source_grant_packet_names_one_bounded_target():
    text = normalized(DOC)

    required_terms = [
        "Source family: `operator_supplied_project_doc_card`",
        "one Jeremy-supervised Memory Seam project-document source card",
        "no source discovery by Memory Seam",
        "Allowed include/scope: metadata-only card fields",
        "`title`, `document_kind`, `section_label`, `safe_summary`, `freshness_label`, and `redacted_source_card_id`",
        "Maximum reads: exactly one supervised metadata-only source-card read",
        "Timeout: 30 seconds wall-clock",
        "does not grant a family scan, workspace walk, index query, backend search, broad recall, source discovery, or recurring read permission",
    ]
    for term in required_terms:
        assert term in text


def test_l5_supervised_source_grant_packet_preserves_held_surfaces():
    text = normalized(DOC)

    required_terms = [
        "raw document body",
        "raw private source text",
        "raw file paths",
        "private absolute paths",
        "raw platform IDs",
        "raw query payloads",
        "private correlation refs",
        "credentials",
        "auth/env/keychain/OAuth/auth-file material",
        "service/listener activation",
        "global Hermes/MCP/client/runtime configuration mutation",
        "Runtime Registry runtime consumption",
        "live/private source reads before #105 approval",
        "source discovery",
        "unsupervised reads",
        "cron/startup activation",
        "recurring runner/canary activation",
        "writes/custody/reindex behavior",
        "provider/prod/canary authority",
        "repository visibility change",
        "package publication",
        "Atlas Gate movement",
        "production-authoritative claims",
    ]
    for term in required_terms:
        assert term in text


def test_l5_supervised_source_grant_packet_exact_approval_phrase_is_single_read_only():
    text = normalized(DOC)

    approval_phrase = (
        "I approve Memory Seam issue #105 to execute exactly one supervised metadata-only read "
        "of one operator-supplied project-document source card under "
        "docs/l5-supervised-source-grant-packet.md, with no source discovery, no raw content, "
        "no credential/auth/env/keychain/OAuth/auth-file reads, no service/listener/cron/startup "
        "activation, no Runtime Registry consumption, no global config mutation, no provider/prod/canary "
        "authority, no writes/custody/reindex, no repository visibility or package publication change, "
        "no Atlas Gate movement, and no recurring reads."
    )
    assert approval_phrase in text
    assert "Any variant, partial quote, implied approval, emoji reaction, merge, issue close" in text
    assert "The phrase authorizes one supervised read only" in text
    assert "does not authorize unsupervised reads, recurring runner work, canaries, L6 write custody" in text


def test_l5_supervised_source_grant_packet_records_future_denial_counters():
    text = normalized(DOC)

    required_terms = [
        "denial/zero counters for source discovery",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "service_started",
        "runtime_registry_consumed",
        "global_config_mutation",
        "write_custody_or_reindex",
        "recurring_runner_activated",
        "provider_prod_canary_authority",
        "atlas_gate_moved",
        "public artifacts contain no raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, or private correlation refs",
    ]
    for term in required_terms:
        assert term in text


def test_l5_supervised_source_grant_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l5-supervised-source-grant-packet.md" in docs_index
    assert "tests/test_l5_supervised_source_grant_packet.py" in inventory
    assert "L5 supervised source-grant decision packet" in inventory
