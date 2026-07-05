from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-first-implementation-slice-decision-packet.md"
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


def test_first_slice_packet_is_hitl_only_no_execution():
    text = normalized(DOC)

    required_terms = [
        "L6S.06 first implementation-slice decision packet",
        "Status: `HITL_DECISION_PACKET_ONLY`",
        "Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`",
        "This packet is docs/tests only.",
        "does not approve, implement, enable, activate, schedule, simulate, or execute writes, custody transfer, delete, reindex, rollback, cache purge",
        "service/listener/cron/ startup behavior",
        "recurring runner behavior",
        "unsupervised reads",
        "source discovery",
        "live/private source reads",
        "provider/backend/source-stat/source-read callbacks",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "provider/prod/canary authority",
        "repository visibility changes",
        "package publication",
        "Atlas Gate movement",
        "This L6S.06 packet is not approval.",
        "Work remains held unless Jeremy posts the exact approval phrase",
    ]
    for term in required_terms:
        assert term in text


def test_first_slice_packet_names_one_bounded_recommended_slice():
    text = normalized(DOC)

    required_terms = [
        "Recommended slice name: `L6_WRITE_INTENT_PREFLIGHT_GATE_SKELETON`",
        "Recommended future implementation slice: `L6_WRITE_INTENT_PREFLIGHT_GATE_SKELETON`.",
        "Bounded purpose: add the smallest non-production implementation skeleton that can parse and deny a synthetic write-intent operation before mutation callbacks.",
        "default-off preflight gate and tests around denied paths",
        "Allowed operation class for this first slice: `write intent` only.",
        "Custody receipt persistence, delete, reindex, rollback, and cache purge remain future operation classes and are not included",
    ]
    for term in required_terms:
        assert term in text


def test_first_slice_packet_requires_exact_approval_language_without_implied_approval():
    text = normalized(DOC)

    required_terms = [
        "Exact approval language required",
        "Jeremy may approve only by posting this exact language, filling every bracketed field with concrete values",
        "I approve Memory Seam to implement exactly one bounded L6 write/custody slice named L6_WRITE_INTENT_PREFLIGHT_GATE_SKELETON under issue #[issue number] and docs/l6-first-implementation-slice-decision-packet.md.",
        "The approved slice is limited to operation class write intent, with maximum [number] synthetic no-production operations",
        "no production execution",
        "no recurring runner/canary/startup/cron/service/listener activation",
        "no Runtime Registry consumption",
        "no global Hermes/MCP/client/runtime configuration mutation",
        "no credential/auth/env/keychain/OAuth/auth-file reads",
        "no source discovery",
        "no live/private source reads",
        "no provider/prod/canary authority beyond this named slice",
        "no repository visibility change",
        "no package publication",
        "no Atlas Gate movement",
        "zero provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge counters on denied paths",
        "stop when approval expires at [timestamp or duration]",
        "Any variant, partial quote, implied approval, merge event, issue close, label, assignment, emoji reaction, checklist item, stale approval, or unrelated comment is not implementation approval.",
    ]
    for term in required_terms:
        assert term in text


def test_first_slice_packet_records_limits_rollback_audit_and_residual_holds():
    text = normalized(DOC)

    required_terms = [
        "Required limits for the approved slice",
        "Operation class: `write intent` only.",
        "the packet recommends `1` for the first run of implementation work",
        "Mutation boundary: denied paths must stop before write, custody, delete, reindex, rollback, cache purge, provider, backend, source-stat, source-read",
        "Rollback and audit requirements",
        "docs/l6-write-custody-rollback-audit-plan.md",
        "rollback plan reference",
        "audit event schema reference",
        "custody owner and approver references",
        "exact approval reference that is report-safe",
        "failure modes for approval mismatch, stale approval, exceeded operation count, denied callback, hygiene failure, and verification failure",
        "This packet does not create a rollback implementation and does not authorize a rollback execution.",
        "Residual held surfaces",
        "write execution",
        "custody transfer and custody receipt persistence",
        "delete execution",
        "reindex execution",
        "rollback execution",
        "cache purge execution",
        "provider/backend/source-stat/source-read callbacks",
        "service/listener/cron/startup behavior and recurring runner behavior",
        "Atlas Gate movement and production-authoritative claims",
    ]
    for term in required_terms:
        assert term in text


def test_first_slice_packet_preserves_public_hygiene_constraints():
    text = normalized(DOC)

    required_terms = [
        "Public/reportable hygiene constraints",
        "Public issue, PR, test, and doc artifacts for this packet are report-safe.",
        "raw private source text",
        "credentials",
        "auth/env/keychain material",
        "OAuth material",
        "auth-file material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "raw payload content",
        "private correlation refs",
        "issue numbers, file names, synthetic operation-class names, boolean/counter facts, and safe error-code style terms only",
    ]
    for term in required_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_first_slice_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-first-implementation-slice-decision-packet.md" in docs_index
    assert "tests/test_l6_first_implementation_slice_decision_packet.py" in inventory
    assert "L6S.06 first implementation-slice decision packet" in inventory
