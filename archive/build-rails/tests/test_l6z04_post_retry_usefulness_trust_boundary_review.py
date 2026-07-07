from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6z04-post-retry-usefulness-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVIDENCE_TERMS = (
    "L6Z.01 exact target-ref approval packet (#231 / PR #236)",
    "L6Z.02 exact target-ref one-read retry denial HOLD (#232 / PR #237)",
    "L6Z.03 one-read retry receipt and redaction verifier (#233 / PR #238)",
)

RESIDUAL_HOLDS = (
    "live/private reads remain held",
    "raw private content remains held",
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

UNSAFE_CLASSES = (
    "raw private source text",
    "raw private content",
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


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6z04_review_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6z04-post-retry-usefulness-trust-boundary-review.md" in docs_index
    assert "tests/test_l6z04_post_retry_usefulness_trust_boundary_review.py" in inventory
    assert "L6Z.04 post-retry usefulness and trust-boundary review" in inventory
    assert "HOLD_FOR_ANCHOR_RECONCILE_NO_LIVE_EXECUTED" in inventory


def test_l6z04_records_allowed_verdict_and_exact_reason():
    text = normalized(DOC)

    required_terms = (
        "Status: `HOLD_FOR_ANCHOR_RECONCILE_NO_LIVE_EXECUTED`",
        "Rail issue: #234",
        "Parent issue: #6",
        "Reviewed retry issue: #232",
        "Verifier issue: #233",
        "Source floor entering slice: `4a7b390fd1a82efd561fdebebd16c651e12117b4`",
        "#6 comment `4649391691`",
        "#215 comment `4649391836`",
        "issuecomment-4650001541",
        "Verdict vocabulary: `PASS_CONTINUE`, `FIX_BEFORE_NEXT_SOURCE`, `HOLD_FOR_OPERATOR`, `HOLD_FOR_ANCHOR_RECONCILE`",
        "Verdict: `HOLD_FOR_ANCHOR_RECONCILE`",
        "Reason: #232 denied before read because the fresh owner comment's executable target refs",
        "descriptor:l6z/operator-proof",
        "source-card:l6z/operator-proof",
        "descriptor:l6z/report-safe-operator-preference-card",
        "source-card:l6z/report-safe-operator-preference-card",
        "No live/private read occurred in L6Z",
        "NOT_APPLICABLE_NO_READ_EXECUTED",
        "REPORT_SAFE_METADATA_ONLY_RAW_APPROVAL_TEXT_OMITTED",
    )
    for term in required_terms:
        assert term in text


def test_l6z04_reviews_l6z_evidence_chain_without_private_reads():
    text = normalized(DOC)

    for term in EVIDENCE_TERMS:
        assert term in text
    assert "L6Z stayed within exact one-read, report-safe, deny-before-read boundaries" in text
    assert "target-ref mismatch against #231" in text
    assert "every live/source/callback/credential/Runtime-Registry/persistence/mutation/rollback/cache-purge counter stayed at the preserved hold value" in text


def test_l6z04_usefulness_and_redaction_findings_are_metadata_only():
    text = normalized(DOC)

    required_terms = (
        "proves real operator value even without private content",
        "distinguishes a fresh owner comment with mismatched executable target refs from an executable approval",
        "identifies the exact blocker as #232/#231 descriptor/source-card target-ref mismatch",
        "useful frontier evidence, not source-content evidence",
        "does not yet have useful report-safe source-card evidence from a live read",
        "useful report-safe control-plane evidence",
        "The redaction boundary held",
        "only report-safe metadata: issue numbers, public comment IDs, timestamps, source-floor commits, safe status labels, booleans, counters, operation class, descriptor/source-card refs, and mismatch sentinel labels",
    )
    for term in required_terms:
        assert term in text

    for unsafe_class in UNSAFE_CLASSES:
        assert unsafe_class in text


def test_l6z04_cannot_authorize_another_read_or_gate_movement():
    text = normalized(DOC)

    forbidden_unholds = (
        "cannot authorize another read",
        "does not authorize more live reads by inertia",
        "does not move any Gate",
        "No additional unhold is created by this review",
        "This review is no-edit/no-execution",
    )
    for term in forbidden_unholds:
        assert term in text

    gated_surfaces = (
        "callback",
        "source discovery",
        "Runtime Registry use",
        "credential/auth access",
        "persistence",
        "mutation",
        "rollback/cache-purge execution",
        "service or cron activation",
        "publication",
        "visibility change",
        "provider/prod/canary movement",
        "Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for term in gated_surfaces:
        assert term in text


def test_l6z04_names_residual_holds_and_next_exact_blocker():
    text = normalized(DOC)

    assert "Next exact blocker: #235 source-floor anchor, parent status, and next frontier reconciliation" in text
    assert "fresh exact owner approval comment" in text
    assert "executable report-safe `descriptor:l6z/report-safe-operator-preference-card` and `source-card:l6z/report-safe-operator-preference-card` refs" in text
    assert "max one operation" in text
    assert "expires within <=12h" in text

    for held in RESIDUAL_HOLDS:
        assert held in text
