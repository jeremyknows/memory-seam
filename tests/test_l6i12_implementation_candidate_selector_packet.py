from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "docs" / "l6-implementation-candidate-selector-packet.md"
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

CANDIDATES = (
    "L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON",
    "L6_APPROVAL_RECOGNIZED_MUTATION_HELD_SKELETON",
    "L6_CUSTODY_RECEIPT_NONPERSISTENT_SKELETON",
)

GUARDED_COUNTERS = (
    "allowed_result_count=0",
    "provider_callback_count=0",
    "backend_callback_count=0",
    "source_stat_callback_count=0",
    "source_read_callback_count=0",
    "write_callback_count=0",
    "custody_callback_count=0",
    "delete_callback_count=0",
    "reindex_callback_count=0",
    "rollback_callback_count=0",
    "cache_purge_callback_count=0",
    "persistent_receipt_count=0",
    "durable_write_record_count=0",
    "audit_persistence_count=0",
    "cache_mutation_count=0",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6i12_packet_is_docs_tests_only_selector_non_approval():
    text = normalized(PACKET)

    required_terms = [
        "L6I.12 implementation-candidate selector packet",
        "docs/tests-only implementation-candidate selector packet",
        "preparatory",
        "non-approval",
        "non-executable",
        "does not implement runtime behavior",
        "does not add any code path returning `allowed=true`",
        "does not approve positive authorization acceptance",
        "Source floor: `7980a5b` or later `origin/main`",
        "Dependency: L6I.11 closed/PASS via issue `#153` and PR `#160`",
        "SPLIT_AGAIN_DOCS_TESTS_ONLY",
        "does not provide approval language",
        "fresh human approval packet",
    ]
    for term in required_terms:
        assert term in text

    assert "I approve Memory Seam to implement" not in text


def test_l6i12_compares_required_candidates_and_selects_exactly_one():
    text = normalized(PACKET)

    for candidate in CANDIDATES:
        assert candidate in text

    assert text.count("SELECTED_FUTURE_CANDIDATE") == 1
    assert "Selected future candidate: `L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON`" in text
    assert "`L6_APPROVAL_RECOGNIZED_MUTATION_HELD_SKELETON` | NOT_SELECTED_THIS_SLICE" in text
    assert "`L6_CUSTODY_RECEIPT_NONPERSISTENT_SKELETON` | NOT_SELECTED_THIS_SLICE" in text
    assert "Proceed to L6I.13 as a docs/tests-only HITL decision packet for `L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON`" in text


def test_l6i12_selected_candidate_is_smaller_than_custody_persistence_or_write_execution():
    text = normalized(PACKET)

    selection_terms = [
        "receipt-only positive-authorization skeleton",
        "recognize an exact future approval",
        "emit a non-persistent report-safe receipt",
        "keep mutation unsupported",
        "deny/stop before every provider, backend, source, write, custody, delete, reindex, rollback, cache-purge, storage, Runtime Registry, activation, publication, provider/prod/canary, visibility, and Atlas Gate surface",
        "smaller than custody persistence or write execution",
        "Smallest: approval-field validation boundary plus report-safe non-persistent receipt shape only",
        "no mutation executor, no custody transfer, no persistence adapter, no provider/backend/source callback",
        "custody language is too close to persistence/ownership transfer",
        "larger than receipt-only positive authorization",
    ]
    for term in selection_terms:
        assert term in text

    required_fields = [
        "issue",
        "exact phrase reference",
        "actor binding",
        "expiry",
        "max operation count of one",
        "operation class",
        "custody owner role",
        "report-safe approval reference",
        "rollback/audit reference",
        "synthetic/no-production target",
    ]
    for field in required_fields:
        assert field in text


def test_l6i12_prerequisites_stop_conditions_and_zero_counters_are_carried_forward():
    text = normalized(PACKET)

    for counter in GUARDED_COUNTERS:
        assert counter in text

    receipt_terms = [
        "status `positive_authorization_recognized_mutation_held`",
        "`mutation_attempted=false`",
        "`mutation_supported=false`",
        "`fixture_is_persistent=false`",
        "rollback is no-op/posture-only",
        "audit remains report-safe/non-persistent unless separately approved",
    ]
    for term in receipt_terms:
        assert term in text

    stop_conditions = [
        "stale approval",
        "variant approval",
        "implied by issue closure",
        "implied by PR merge",
        "copied from issue `#137`",
        "actor-mismatched",
        "subject-mismatched",
        "owner-mismatched",
        "expired",
        "over max operation count",
        "missing operation class",
        "requesting custody persistence",
        "requesting write/delete/reindex/rollback/cache-purge execution",
        "requesting provider/backend/source-stat/source-read callbacks",
        "requesting live/private reads or source discovery",
        "requesting Runtime Registry consumption",
        "requesting global configuration mutation",
        "requesting service/listener/startup/cron activation",
        "requesting publication",
        "requesting repository visibility change",
        "claiming provider/prod/canary authority",
        "moving Atlas Gate",
    ]
    for condition in stop_conditions:
        assert condition in text


def test_l6i12_residual_holds_match_or_exceed_l6i06_hard_holds():
    text = normalized(PACKET)

    held_terms = [
        "`allowed=true`",
        "mutation",
        "write execution",
        "custody transfer",
        "custody persistence",
        "delete execution",
        "reindex execution",
        "rollback execution",
        "cache-purge execution",
        "provider callbacks",
        "backend callbacks",
        "source-stat callbacks",
        "source-read callbacks",
        "persistence",
        "live/private reads",
        "source discovery",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "service/listener/startup/cron activation",
        "recurring runner activation",
        "provider/prod/canary authority",
        "repository visibility change",
        "package publication",
        "Atlas Gate movement",
        "production-authoritative claims",
    ]
    for term in held_terms:
        assert term in text


def test_l6i12_public_hygiene_and_discoverability_are_preserved():
    combined = " ".join(
        normalized(path) for path in (PACKET, DOCS_INDEX, CONTRACT_TEST_INVENTORY)
    )

    discoverability_terms = [
        "l6-implementation-candidate-selector-packet.md",
        "tests/test_l6i12_implementation_candidate_selector_packet.py",
        "L6I.12 implementation-candidate selector packet",
        "L6I.12 docs/tests-only implementation-candidate selector packet",
    ]
    for term in discoverability_terms:
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
        "raw approval text",
    ]
    for term in hygiene_terms:
        assert term in combined

    for marker in PRIVATE_MARKERS:
        assert marker not in combined
