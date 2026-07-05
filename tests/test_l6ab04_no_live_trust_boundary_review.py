from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ab04-no-live-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVIDENCE_TERMS = (
    "L6AB.01 report-safe source-card value comparison matrix (#251 / PR #256)",
    "L6AB.02 stale approval hardening fixtures (#252 / PR #257)",
    "L6AB.03 report-safe value evidence UX packet (#253 / PR #258)",
)

RESIDUAL_HOLDS = (
    "live/private reads remain held",
    "raw private content and raw approval text remain held",
    "callbacks remain held",
    "credentials/auth/env/keychain/OAuth/auth-file reads remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "persistence, audit/custody writes, mutation, reindex, cache purge, rollback, and delete execution remain held",
    "service/listener/startup/cron activation and global runtime config mutation remain held",
    "publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held",
    "any broad `allowed=true` route remains held",
)

UNSAFE_CLASSES = (
    "raw private content",
    "raw source text",
    "raw approval text",
    "credentials",
    "auth/env/keychain material",
    "OAuth material",
    "auth-file material",
    "source URIs",
    "private paths",
    "raw prompt/query payloads",
    "backend responses",
    "private correlation refs",
    "Runtime Registry handles",
    "provider handles",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ab04_review_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ab04-no-live-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ab04_no_live_trust_boundary_review.py" in inventory
    assert "L6AB.04 no-live trust-boundary review" in inventory
    assert "PASS_CONTINUE_NO_LIVE_TRUST_BOUNDARY_REVIEW" in inventory


def test_l6ab04_records_pass_continue_verdict_and_source_floor():
    text = normalized(DOC)

    required_terms = (
        "Status: `PASS_CONTINUE_NO_LIVE_TRUST_BOUNDARY_REVIEW`",
        "Rail issue: #254",
        "Parent issue: #6",
        "Blocked by: #253 closed/PASS",
        "Source floor entering slice: `813e24c59b8a60671240513723ba3f646fb35ab2`",
        ">= `91761ed55889f4c5432b55c445e396e727a6be93`",
        "#6 comment `4649391691`",
        "#215 comment `4649391836`",
        "Verdict vocabulary: `PASS_CONTINUE`, `FIX_BEFORE_RECONCILE`, `HOLD_FOR_OPERATOR`",
        "Verdict: `PASS_CONTINUE`",
        "ready for reconciliation",
    )
    for term in required_terms:
        assert term in text


def test_l6ab04_reviews_completed_value_chain_without_new_reads():
    text = normalized(DOC)

    for term in EVIDENCE_TERMS:
        assert term in text

    required_terms = (
        "existing repo artifacts and public GitHub issue/PR metadata only",
        "historical already-consumed evidence only",
        "all denying before read",
        "inert future approval template text",
        "No new source-card read occurred in #251, #252, #253, or #254",
        "No provider, backend, source-stat, source-read, credential, Runtime Registry, persistence, mutation, rollback, cache-purge, service, listener, startup, publication, visibility, provider/prod/canary, or Atlas Gate surface is activated",
    )
    for term in required_terms:
        assert term in text


def test_l6ab04_confirms_no_standing_approval_or_gate_movement():
    text = normalized(DOC)

    required_terms = (
        "The trust boundary held",
        "not as standing permission",
        "PASS_ONE_HISTORICAL_REPORT_SAFE_SOURCE_CARD_READ_CONSUMED",
        "No standing approval exists after this rail",
        "Merge events, issue closure, labels, prior comments, copied phrasing, inert template text, historical PASS evidence, or source-floor advancement do not authorize another source-card read",
        "No Gate movement is approved or implied",
    )
    for term in required_terms:
        assert term in text


def test_l6ab04_report_hygiene_names_only_rejected_unsafe_classes():
    text = normalized(DOC)

    assert "Report hygiene finding" in text
    assert "expose only report-safe labels" in text
    for unsafe_class in UNSAFE_CLASSES:
        assert unsafe_class in text


def test_l6ab04_names_next_blocker_and_residual_holds():
    text = normalized(DOC)

    assert "Next exact blocker: #255 source-floor anchor, parent status, and next frontier reconciliation" in text
    assert "completed #251-#254 evidence" in text
    assert "without creating successor issues or changing cron automation" in text

    for hold in RESIDUAL_HOLDS:
        assert hold in text
