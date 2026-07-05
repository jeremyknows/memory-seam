from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-live-use-pivot-frontier-packet.md"
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
    "Next L6 custody persistence planning",
    "Supervised live-read adapter approval packet",
    "Hermes/Atlas Query integration smoke",
    "Dogfood/use-proof prompt set",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6p06_frontier_packet_is_docs_tests_only_no_approval():
    text = normalized(DOC)

    required_terms = [
        "L6P.06 live-use pivot frontier packet",
        "Status: `LIVE_USE_PIVOT_FRONTIER_PACKET_ONLY`",
        "Review verdict: `RECOMMEND_SUPERVISED_LIVE_READ_ADAPTER_APPROVAL_PACKET`",
        "Rail issue: #168",
        "Prerequisite: #167 closed/PASS",
        "docs/tests only, no-execution, no-approval, and decision-only",
        "does not implement behavior",
        "approve live use",
        "perform live/private reads",
        "discover sources",
        "provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "execute mutation",
        "persist receipts or audit records",
        "Runtime Registry",
        "credential/auth/env/keychain/OAuth/auth-file material",
        "global Hermes/MCP/client/runtime configuration",
        "service/listener/startup/cron path",
        "publish a package",
        "change repository visibility",
        "provider/prod/canary authority",
        "move Atlas Gate",
    ]
    for term in required_terms:
        assert term in text


def test_l6p06_frontier_summarizes_positive_authorization_evidence_and_gap():
    text = normalized(DOC)

    required_terms = [
        "L6P.01-L6P.05 proved a narrow synthetic/no-production positive-authorization receipt skeleton",
        "exact issue #163 approval-field recognition",
        "L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON",
        "positive_authorization_recognized_mutation_held",
        "allowed=false",
        "mutation_attempted=false",
        "mutation_supported=false",
        "allowed_result_count=0",
        "operation_count=1",
        "max_operation_count=1",
        "fixture_is_persistent=false",
        "persistent_receipt_count=0",
        "durable_write_record_count=0",
        "audit_persistence_count=0",
        "cache_mutation_count=0",
        "deny before callbacks",
        "L6P.05 recorded PASS",
        "live-use gap",
        "lacks an approved, bounded, supervised path for one operator-valuable read-side proof",
    ]
    for term in required_terms:
        assert term in text


def test_l6p06_frontier_compares_all_required_candidates():
    text = normalized(DOC)

    for candidate in CANDIDATES:
        assert candidate in text

    assert "Near-term operator value" in text
    assert "Safety/readiness fit" in text
    assert "Why not selected now" in text
    assert "It deepens mutation/custody planning while the biggest current gap is useful read-side proof" in text
    assert "Too implementation-adjacent as the immediate next move" in text
    assert "Better as evidence inside or after the supervised approval packet" in text


def test_l6p06_frontier_recommends_exactly_one_next_tranche():
    text = DOC.read_text(encoding="utf-8")

    assert "Recommended next tranche: `SUPERVISED_LIVE_READ_ADAPTER_APPROVAL_PACKET`." in text
    assert text.count("Recommended next tranche:") == 1
    assert text.count("Selected.") == 1
    assert "This recommendation is singular." in text
    assert "rejects parallel recommendation of custody persistence planning" in text
    assert "immediate Atlas Query smoke implementation" in text
    assert "dogfood prompt-set-only work" in text


def test_l6p06_frontier_prioritizes_supervised_read_side_usefulness_without_execution():
    text = normalized(DOC)

    required_terms = [
        "prioritize near-term useful read-side benefit",
        "one future supervised live-read adapter/use-proof slice",
        "exactly one future read-side operation class",
        "L6_SUPERVISED_LIVE_READ_ADAPTER_ONE_PROOF",
        "exactly one operator-approved target shape",
        "report-safe source-card or bounded descriptor",
        "no source discovery or broad recall",
        "max one operation",
        "short expiry",
        "exact approval phrase requirements",
        "denial-before-callback proof",
        "public hygiene and full verification gates",
        "before any later implementation PR",
    ]
    for term in required_terms:
        assert term in text


def test_l6p06_frontier_preserves_hard_holds():
    text = normalized(DOC)

    required_terms = [
        "Preserved holds",
        "any implementation or execution of live/private reads",
        "source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, or Runtime Registry consumption",
        "mutation execution, `allowed=true` result paths, write execution, custody transfer, custody receipt persistence, delete, reindex, rollback, and cache purge",
        "provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "receipt persistence, audit persistence, durable write records, cache mutation",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "service/listener/startup/cron activation or recurring runner behavior",
        "global Hermes/MCP/client/runtime configuration mutation",
        "package publication, repository visibility changes, provider/prod/canary authority, production authority, and Atlas Gate movement",
    ]
    for term in required_terms:
        assert term in text


def test_l6p06_frontier_is_report_safe():
    text = normalized(DOC)

    required_terms = [
        "exclude raw private source text",
        "credentials",
        "auth/env/keychain/OAuth/auth-file material",
        "private paths",
        "raw platform IDs",
        "raw query/payload content",
        "private correlation refs",
        "token-shaped inputs",
    ]
    for term in required_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6p06_frontier_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-live-use-pivot-frontier-packet.md" in docs_index
    assert "tests/test_l6p06_live_use_pivot_frontier_packet.py" in inventory
    assert "L6P.06 live-use pivot frontier packet" in inventory
    assert "SUPERVISED_LIVE_READ_ADAPTER_APPROVAL_PACKET" in inventory
    assert "exactly one next tranche" in inventory
