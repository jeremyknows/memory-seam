from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6y04-post-read-usefulness-redaction-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVIDENCE_TERMS = (
    "L6Y.01 binding and target packet (#221 / PR #226)",
    "L6Y.02 approval-mismatch HOLD (#222 / PR #227)",
    "L6Y.03 receipt hygiene verifier (#223 / PR #228)",
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


def test_l6y04_review_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6y04-post-read-usefulness-redaction-review.md" in docs_index
    assert "tests/test_l6y04_post_read_usefulness_redaction_review.py" in inventory
    assert "L6Y.04 post-read usefulness and redaction review" in inventory
    assert "HOLD_FOR_ANCHOR_RECONCILE_NO_LIVE_EXECUTED" in inventory


def test_l6y04_records_allowed_verdict_and_exact_reason():
    text = normalized(DOC)

    required_terms = (
        "Status: `HOLD_FOR_ANCHOR_RECONCILE_NO_LIVE_EXECUTED`",
        "Rail issue: #224",
        "Parent issue: #6",
        "Verdict vocabulary: `PASS_CONTINUE`, `FIX_BEFORE_NEXT_SOURCE`, `HOLD_FOR_OPERATOR`, `HOLD_FOR_ANCHOR_RECONCILE`",
        "Verdict: `HOLD_FOR_ANCHOR_RECONCILE`",
        "Reason: #222 denied before read because the fresh owner comment did not supply executable report-safe descriptor/source-card refs matching the #221 binding packet",
        "No live/private read occurred in L6Y",
        "attempted source-card usefulness remained `NOT_EVALUATED_NO_READ`",
        "redaction posture remained `REPORT_SAFE_METADATA_ONLY`",
    )
    for term in required_terms:
        assert term in text


def test_l6y04_reviews_l6y_evidence_chain_without_private_reads():
    text = normalized(DOC)

    for term in EVIDENCE_TERMS:
        assert term in text
    assert "L6Y stayed within exact one-read, report-safe, deny-before-read boundaries" in text
    assert "missing executable descriptor/source-card refs" in text
    assert "every live/source/callback/credential/Runtime-Registry/persistence/mutation/rollback/cache-purge counter stayed at the preserved hold value" in text


def test_l6y04_usefulness_and_redaction_findings_are_metadata_only():
    text = normalized(DOC)

    required_terms = (
        "proves real operator value even without private content",
        "distinguishes a present-but-not-executable owner comment from absent approval",
        "identifies the exact missing blocker as executable descriptor/source-card refs",
        "useful frontier evidence, not source-content evidence",
        "The redaction boundary held",
        "only report-safe metadata: issue numbers, public comment IDs, timestamps, source-floor commits, safe status labels, booleans, counters, operation class, and missing-ref sentinel labels",
    )
    for term in required_terms:
        assert term in text

    for unsafe_class in UNSAFE_CLASSES:
        assert unsafe_class in text


def test_l6y04_cannot_authorize_another_read_or_gate_movement():
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


def test_l6y04_names_residual_holds_and_next_exact_blocker():
    text = normalized(DOC)

    assert "Next exact blocker: #225 source-floor anchor, parent status, and next frontier reconciliation" in text
    assert "fresh exact owner approval comment" in text
    assert "executable report-safe `descriptor:l6y/<report-safe-slug>` and `source-card:l6y/<report-safe-slug>` refs" in text
    assert "max one operation" in text
    assert "expires within <=12h" in text

    for held in RESIDUAL_HOLDS:
        assert held in text
