from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "docs" / "l6-custody-persistence-threat-model.md"
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


def test_l6i10_packet_is_docs_tests_only_decision_non_approval():
    text = normalized(PACKET)

    required_terms = [
        "L6I.10 custody persistence threat model and storage non-goals packet",
        "docs/tests-only threat-model packet",
        "decision-only",
        "non-approval",
        "non-executable",
        "does not approve implementation",
        "does not unhold runtime behavior",
        "does not create persistence",
        "does not create any positive allowed runtime path",
        "Source floor: `7980a5b` or later `origin/main`",
        "Dependency: L6I.09 closed/PASS via issue `#151` and PR `#158`",
        "SPLIT_AGAIN_DOCS_TESTS_ONLY",
        "only proves synthetic no-production write-intent denial-before-callback behavior",
    ]
    for term in required_terms:
        assert term in text

    assert "I approve Memory Seam to implement" not in text
    assert "allowed=true" not in text


def test_l6i10_names_all_held_storage_classes_as_non_goals():
    text = normalized(PACKET)

    held_storage_classes = [
        "Filesystem writes",
        "SQLite/database writes",
        "Object storage",
        "Remote API writes",
        "Git commits",
        "Issue/PR comments as persistence",
        "Runtime Registry/state mutation",
    ]
    for storage_class in held_storage_classes:
        assert storage_class in text

    non_goal_terms = [
        "No custody receipt files",
        "No SQLite, embedded database, external database, migration, table, row, or audit-event persistence",
        "No bucket/object/blob write",
        "No issue, ticket, audit, logging, webhook, telemetry, provider, backend, or source-platform write used as custody persistence",
        "No runtime-created commit, branch, tag, note, changelog entry, generated receipt commit, or bot-authored audit trail",
        "Issue and PR comments are not custody persistence unless separately approved with exact custody-persistence authority",
        "No Runtime Registry consumption, registry write, global Hermes/MCP/client/runtime configuration mutation",
    ]
    for term in non_goal_terms:
        assert term in text


def test_l6i10_minimum_future_proof_is_specific_before_persistence_considered():
    text = normalized(PACKET)

    proof_terms = [
        "Exact approval",
        "one fresh, exact approval phrase",
        "Single operation class",
        "exactly one named operation class",
        "Local synthetic-only target",
        "no live/private source read",
        "Report-safe payload",
        "Pre-mutation receipt",
        "Rollback/no-op posture",
        "Stop conditions",
        "Cleanup/retention plan",
        "retention, cleanup, redaction, access, and deletion obligations",
    ]
    for term in proof_terms:
        assert term in text

    stop_conditions = [
        "stale approval",
        "variant approval",
        "actor mismatch",
        "expiry",
        "count overflow",
        "unsafe payload",
        "callback attempt",
        "storage attempt",
        "private-data inclusion",
    ]
    for condition in stop_conditions:
        assert condition in text


def test_l6i10_preserves_l6i06_and_l6i09_held_surfaces():
    text = normalized(PACKET)

    held_terms = [
        "runtime approval acceptance",
        "positive allowed runtime path",
        "write execution",
        "custody transfer",
        "custody persistence",
        "delete execution",
        "reindex execution",
        "rollback execution",
        "cache purge execution",
        "provider/backend callbacks",
        "source-stat/source-read callbacks",
        "source discovery",
        "live/private source reads",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "Runtime Registry consumption",
        "global configuration mutation",
        "service/listener/startup/cron activation",
        "recurring runner activation",
        "provider/prod/canary authority",
        "publication",
        "repository visibility changes",
        "Atlas Gate movement",
        "production-authoritative claims",
    ]
    for term in held_terms:
        assert term in text


def test_l6i10_public_hygiene_and_discoverability_are_preserved():
    combined = " ".join(
        normalized(path) for path in (PACKET, DOCS_INDEX, CONTRACT_TEST_INVENTORY)
    )

    discoverability_terms = [
        "l6-custody-persistence-threat-model.md",
        "tests/test_l6i10_custody_persistence_threat_model.py",
        "L6I.10 docs/tests-only custody persistence threat model",
        "Proceed to L6I.11 as docs/tests-only future allowed-path counter and callback contract work",
    ]
    for term in discoverability_terms:
        assert term in combined

    safe_public_terms = [
        "public issue numbers",
        "repository file names",
        "synthetic operation-class names",
        "boolean/counter facts",
        "safe status strings",
    ]
    for term in safe_public_terms:
        assert term in combined

    hygiene_terms = [
        "raw private source text",
        "credentials",
        "auth/env/keychain material",
        "OAuth/auth-file material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "raw payload content",
        "private correlation refs",
    ]
    for term in hygiene_terms:
        assert term in combined

    for marker in PRIVATE_MARKERS:
        assert marker not in combined
