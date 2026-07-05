from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6x04-post-attempt-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVIDENCE_TERMS = (
    "L6X.01 request packet (#211 / PR #216)",
    "L6X.02 absent-approval HOLD (#212 / PR #217)",
    "L6X.03 receipt verifier (#213 / PR #218)",
)

RESIDUAL_HOLDS = (
    "live/private reads remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "credential/auth/env/keychain/OAuth/auth-file reads remain held",
    "provider/backend/source-stat/source-read callbacks remain held",
    "Runtime Registry consumption remains held",
    "persistence, audit/custody writes, and cache mutation remain held",
    "service/listener/startup/cron activation and global runtime config mutation remain held",
    "publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held",
    "mutation, rollback, and cache-purge execution remain held",
    "any `allowed=true` route remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6x04_review_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6x04-post-attempt-trust-boundary-review.md" in docs_index
    assert "tests/test_l6x04_post_attempt_trust_boundary_review.py" in inventory
    assert "L6X.04 post-attempt trust-boundary frontier review" in inventory
    assert "HOLD_FOR_ANCHOR_RECONCILE_NO_LIVE_EXECUTED" in inventory


def test_l6x04_records_verdict_and_reason():
    text = normalized(DOC)

    required_terms = (
        "Status: `HOLD_FOR_ANCHOR_RECONCILE_NO_LIVE_EXECUTED`",
        "Rail issue: #214",
        "Parent issue: #6",
        "Verdict vocabulary: `PASS_CONTINUE`, `FIX_BEFORE_NEXT_SOURCE`, `HOLD_FOR_ANCHOR_RECONCILE`, `HOLD_FOR_OPERATOR`",
        "Verdict: `HOLD_FOR_ANCHOR_RECONCILE`",
        "Reason: #212 had no exact owner approval comment, so no first read executed",
        "No live/private read occurred in L6X",
        "No additional unhold is created by this review",
    )
    for term in required_terms:
        assert term in text


def test_l6x04_reviews_l6x_evidence_chain():
    text = normalized(DOC)

    for term in EVIDENCE_TERMS:
        assert term in text
    assert "L6X stayed within exact one-read, report-safe, deny-before-callback boundaries" in text
    assert "guarded counters remained synthetic zero for the HOLD path" in text


def test_l6x04_names_next_exact_requirement_without_authorizing_more_reads():
    text = normalized(DOC)

    required_terms = (
        "Next exact unhold requirement: a new fresh owner approval comment would be required before any future supervised report-safe source-card live read",
        "It must bind issue id, owner actor association, subject, audience, operation class `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`, max one operation, expiry <=12h, and report-safe descriptor/source-card refs",
        "This review does not authorize more live reads by inertia",
        "Anchor reconciliation is the next safe issue-bound step",
    )
    for term in required_terms:
        assert term in text


def test_l6x04_preserves_residual_holds_and_report_hygiene():
    text = normalized(DOC)

    for held in RESIDUAL_HOLDS:
        assert held in text
    unsafe_terms = (
        "raw private source text",
        "credentials",
        "auth/env/keychain material",
        "OAuth material",
        "auth-file material",
        "raw platform IDs",
        "private absolute paths",
        "raw prompt/query payloads",
        "raw payload content",
        "raw backend responses",
        "private correlation refs",
        "source URIs",
        "raw approval text",
    )
    for term in unsafe_terms:
        assert term in text
