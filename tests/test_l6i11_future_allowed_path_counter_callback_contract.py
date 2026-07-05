from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "docs" / "l6-future-allowed-path-counter-callback-contract.md"
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


def test_l6i11_packet_is_docs_tests_only_counter_contract_non_approval():
    text = normalized(PACKET)

    required_terms = [
        "L6I.11 future allowed-path counter and callback contract",
        "docs/tests-only counter and callback contract",
        "preparatory",
        "non-approval",
        "non-executable",
        "does not implement runtime behavior",
        "does not create any `allowed=true` path",
        "does not approve positive authorization acceptance",
        "Source floor: `7980a5b` or later `origin/main`",
        "Dependency: L6I.10 closed/PASS via issue `#152` and PR `#159`",
        "SPLIT_AGAIN_DOCS_TESTS_ONLY",
        "current runtime remains denial/no-mutation only",
    ]
    for term in required_terms:
        assert term in text

    assert "I approve Memory Seam to implement" not in text


def test_l6i11_names_all_guarded_counter_families_and_zero_values():
    text = normalized(PACKET)

    counter_terms = [
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
    ]
    for term in counter_terms:
        assert term in text

    callback_families = [
        "Authorization result counters",
        "Provider callback counters",
        "Backend callback counters",
        "Source-stat callback counters",
        "Source-read callback counters",
        "Write callback counters",
        "Custody callback counters",
        "Delete callback counters",
        "Reindex callback counters",
        "Rollback callback counters",
        "Cache-purge callback counters",
        "Persistence counters",
    ]
    for family in callback_families:
        assert family in text


def test_l6i11_selector_packet_contract_requires_one_narrow_callback_binding():
    text = normalized(PACKET)

    selector_terms = [
        "the candidate operation class and whether it proposes any future change from all-zero guarded callback counters",
        "the single callback family, if any, proposed for later human approval",
        "every callback family that remains held at `0`",
        "report-safe counter names",
        "selector packet is not implementation approval",
        "cannot authorize `allowed=true`, mutation, persistence, callbacks, source reads, activation, publication, visibility changes, provider/prod/canary authority, or Atlas Gate movement",
        "Proceed to L6I.12 as docs/tests-only implementation-candidate selector packet work for one next slice",
    ]
    for term in selector_terms:
        assert term in text

    stop_conditions = [
        "stale approval",
        "variant approval",
        "actor mismatch",
        "subject mismatch",
        "owner mismatch",
        "expiry",
        "max-operation-count overflow",
        "unsafe payload",
        "callback attempt",
        "storage attempt",
        "source-read attempt",
        "source-discovery attempt",
        "Runtime Registry attempt",
        "activation attempt",
        "private-data inclusion",
    ]
    for condition in stop_conditions:
        assert condition in text


def test_l6i11_residual_holds_and_persistence_boundaries_are_preserved():
    text = normalized(PACKET)

    held_terms = [
        "runtime approval acceptance",
        "any implementation path returning `allowed=true`",
        "write execution",
        "custody transfer",
        "custody persistence",
        "delete execution",
        "reindex execution",
        "rollback execution",
        "cache-purge execution",
        "provider/backend/source-stat/source-read callbacks",
        "source discovery",
        "live/private source reads",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "service/listener/startup/cron activation",
        "recurring runner activation",
        "provider/prod/canary authority",
        "repository visibility changes",
        "package publication",
        "Atlas Gate movement",
        "production-authoritative claims",
    ]
    for term in held_terms:
        assert term in text

    storage_boundaries = [
        "filesystem",
        "database",
        "object-store",
        "remote API",
        "Git",
        "issue/PR-comment-as-custody-store",
        "Runtime Registry/state mutation",
    ]
    for boundary in storage_boundaries:
        assert boundary in text


def test_l6i11_public_hygiene_and_discoverability_are_preserved():
    combined = " ".join(
        normalized(path) for path in (PACKET, DOCS_INDEX, CONTRACT_TEST_INVENTORY)
    )

    discoverability_terms = [
        "l6-future-allowed-path-counter-callback-contract.md",
        "tests/test_l6i11_future_allowed_path_counter_callback_contract.py",
        "L6I.11 docs/tests-only future allowed-path counter and callback contract",
        "Proceed to L6I.12 as docs/tests-only implementation-candidate selector packet work for one next slice",
    ]
    for term in discoverability_terms:
        assert term in combined

    safe_public_terms = [
        "boolean and integer counter facts",
        "public issue and PR numbers",
        "repository file names",
        "synthetic operation-class names",
        "safe status strings",
        "role names",
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
        "raw approval text",
    ]
    for term in hygiene_terms:
        assert term in combined

    for marker in PRIVATE_MARKERS:
        assert marker not in combined
