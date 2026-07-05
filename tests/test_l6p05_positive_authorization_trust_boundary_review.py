from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-positive-authorization-trust-boundary-review.md"
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


def test_l6p05_trust_boundary_review_is_decision_only_no_execution():
    text = normalized(DOC)

    required_terms = [
        "L6P.05 positive-authorization skeleton trust-boundary review packet",
        "Status: `TRUST_BOUNDARY_REVIEW_PACKET_ONLY`",
        "Review verdict: `PASS`",
        "Rail issue: #167",
        "Reviewed rail issues: #163, #164, #165, #166",
        "docs/tests only, no-edit against runtime behavior, and decision-only",
        "does not add implementation behavior",
        "execute mutation, persist receipts or audit records, transfer custody, write, delete, reindex, rollback, cache purge",
        "provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "discover sources",
        "live/private source reads",
        "credential/auth/env/keychain/OAuth/auth-file material",
        "Runtime Registry",
        "global Hermes/MCP/client/runtime configuration",
        "service/listener/cron/startup path",
        "publish a package",
        "change repository visibility",
        "move Atlas Gate",
    ]
    for term in required_terms:
        assert term in text


def test_l6p05_trust_boundary_review_states_required_verdict_vocabulary():
    text = normalized(DOC)

    assert "The review outcome vocabulary is exactly `PASS`, `HOLD`, or `FIX_BEFORE_NEXT_SLICE`." in text
    assert "This packet records `PASS`" in text
    assert "The PASS is not approval for a new implementation slice" in text
    assert "not approval for live/private reads" in text
    assert "does not unhold any residual surface" in text


def test_l6p05_trust_boundary_review_summarizes_l6p_evidence():
    text = normalized(DOC)

    required_terms = [
        "Evidence reviewed",
        "L6P.01 positive-authorization receipt skeleton (#163)",
        "src/memory_seam/positive_authorization_receipt.py",
        "tests/test_l6p01_positive_authorization_receipt_skeleton.py",
        "docs/l6-positive-authorization-receipt-skeleton.md",
        "status `positive_authorization_recognized_mutation_held`",
        "L6P.02 stale/variant denial hardening (#164)",
        "tests/test_l6p02_positive_authorization_denial_hardening.py",
        "Stale windows, copied #137 approval references, copied template-style approvals without a fresh #163 event",
        "L6P.03 report hygiene (#165)",
        "tests/test_l6p03_positive_receipt_report_hygiene.py",
        "Unsafe raw approval, payload, path, token-shaped, platform, correlation, query, and content inputs",
        "L6P.04 no-production smoke (#166)",
        "examples/l6_positive_authorization_no_production_smoke.py",
        "exactly one committed synthetic/no-production operation",
        "zero-counter",
    ]
    for term in required_terms:
        assert term in text


def test_l6p05_trust_boundary_review_records_pass_findings_for_acceptance_scope():
    text = normalized(DOC)

    required_terms = [
        "Exact approval recognition: PASS.",
        "bound to the public issue #163 approval source",
        "operation class `positive authorization receipt skeleton`",
        "max-one operation",
        "24-hour freshness window",
        "report-safe approval phrase digest",
        "Report-safe receipt: PASS.",
        "Non-persistence: PASS.",
        "Mutation-held posture: PASS.",
        "Denial before callbacks: PASS.",
        "Residual holds: PASS with holds preserved.",
    ]
    for term in required_terms:
        assert term in text


def test_l6p05_trust_boundary_review_preserves_positive_receipt_invariants():
    text = normalized(DOC)

    required_terms = [
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
        "No `allowed=true` path exists",
    ]
    for term in required_terms:
        assert term in text


def test_l6p05_trust_boundary_review_preserves_hard_holds():
    text = normalized(DOC)

    required_terms = [
        "Residual held surfaces",
        "mutation execution and any `allowed=true` result path",
        "write execution",
        "custody transfer and custody receipt persistence",
        "delete execution",
        "reindex execution",
        "rollback execution",
        "cache purge execution",
        "provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "source discovery",
        "live/private source reads",
        "unsupervised reads",
        "service/listener/cron/startup behavior and recurring runner behavior",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "provider/prod/canary authority",
        "repository visibility changes",
        "package publication",
        "Atlas Gate movement and production-authoritative claims",
    ]
    for term in required_terms:
        assert term in text


def test_l6p05_trust_boundary_review_is_report_safe():
    text = normalized(DOC)

    required_terms = [
        "excludes raw approval text",
        "raw actor IDs",
        "raw private source text",
        "credentials",
        "auth/env/keychain material",
        "OAuth material",
        "auth-file material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "raw payload content",
        "token-shaped submitted input",
        "private correlation refs",
    ]
    for term in required_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6p05_trust_boundary_review_recommends_l6p06_packet_only():
    text = normalized(DOC)

    required_terms = [
        "Proceed to L6P.06 as a docs/tests-only live-use pivot frontier packet",
        "must not implement behavior",
        "treat this `PASS` as approval",
        "perform live/private reads",
        "add provider/source callbacks",
        "unhold any production or mutation surface",
    ]
    for term in required_terms:
        assert term in text


def test_l6p05_trust_boundary_review_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-positive-authorization-trust-boundary-review.md" in docs_index
    assert "tests/test_l6p05_positive_authorization_trust_boundary_review.py" in inventory
    assert "L6P.05 positive-authorization skeleton trust-boundary review packet" in inventory
    assert "decision-only" in inventory
