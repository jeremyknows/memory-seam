from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-implementation-unhold-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6_implementation_packet_is_decision_only_no_execution():
    text = normalized(DOC)

    required_terms = [
        "L6.04 implementation unhold packet",
        "Status: `HITL_DECISION_PACKET_ONLY`",
        "Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`",
        "documentation only",
        "does not implement, enable, schedule, simulate, or execute write, custody transfer, delete, reindex, rollback",
        "service/listener activation",
        "source discovery",
        "live/private source reads",
        "provider/prod/canary authority",
        "repository visibility changes",
        "package publication",
        "Atlas Gate movement",
    ]
    for term in required_terms:
        assert term in text


def test_l6_implementation_packet_summarizes_completed_evidence_and_risk():
    text = normalized(DOC)

    required_terms = [
        "Completed evidence",
        "L5.01 no-source-read idle tick",
        "L5.08 canary one-tick unhold packet",
        "L6.01 write-intent threat model",
        "L6.02 write-like route denial matrix",
        "L6.03 custody receipt no-op fixtures",
        "Remaining risk",
        "Mutation blast radius remains unresolved",
        "Approval spoofing and stale approvals remain risks",
        "Provider/backend side effects remain held",
        "Operational activation remains separate",
        "zero source-read, source-stat, provider, backend, custody, reindex, rollback, and write counters",
    ]
    for term in required_terms:
        assert term in text


def test_l6_implementation_packet_offers_hold_split_approve_choices():
    text = normalized(DOC)

    required_terms = [
        "Choice A — HOLD",
        "I choose HOLD for L6 write/custody implementation.",
        "Choice B — SPLIT",
        "I choose SPLIT for L6.",
        "docs/l6-implementation-unhold-packet.md as context",
        "Choice C — APPROVE ONE IMPLEMENTATION SLICE",
        "I approve Memory Seam to implement exactly one bounded L6 write/custody slice named [exact slice name] under issue #[issue number]",
        "[operation class: write intent / custody receipt persistence / delete / reindex / rollback / cache purge]",
        "The implementation must preserve denial-before-callback tests with zero provider/backend/source-stat/source-read/write/custody/reindex/rollback counters on denied paths",
        "Any variant, partial quote, implied approval, merge event, issue close, emoji reaction, or unrelated comment is not implementation approval.",
    ]
    for term in required_terms:
        assert term in text


def test_l6_implementation_packet_preserves_hard_holds_and_public_hygiene():
    text = normalized(DOC)

    required_terms = [
        "Preserved held surfaces",
        "write/custody/reindex/delete/cache-purge/rollback behavior",
        "service/listener/cron/startup activation and recurring unsupervised reads",
        "live/private source reads, unsupervised reads, and source discovery",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "provider/prod/canary authority",
        "repository visibility change and package publication",
        "Atlas Gate movement and production-authoritative claims",
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


def test_l6_implementation_packet_records_future_acceptance_bar():
    text = normalized(DOC)

    required_terms = [
        "Future acceptance bar after approval",
        "exact approval phrase location, actor, issue number, expiry, and report-safe approval reference",
        "operation class, custody owner, max operation count, timeout, rollback plan, and stop conditions",
        "denial-before-callback tests proving zero provider/backend/source-stat/source-read/write/custody/reindex/rollback counters on denied paths",
        "public hygiene proof for receipts, docs, PRs, and issue comments",
        "a no-production-execution verification path unless Jeremy separately approves execution",
        "explicit statement that this L6.04 packet alone is not approval",
    ]
    for term in required_terms:
        assert term in text


def test_l6_implementation_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-implementation-unhold-packet.md" in docs_index
    assert "tests/test_l6_implementation_unhold_packet.py" in inventory
    assert "L6.04 implementation unhold packet" in inventory
