from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ac04-no-live-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_CONTINUE_NO_LIVE_TRUST_BOUNDARY_REVIEW"
RAIL_STARTING_SOURCE_FLOOR = "67a1a78db2b7adca0048497cce61412de13032f1"
SOURCE_FLOOR_ENTERING_SLICE = "734fe3a05158d8412b5d27d8c2998b6afcd4678c"
L6AC01_SOURCE_FLOOR = "ca81a18fbba9603f5f35a8fa57410963e028c904"
L6AC02_SOURCE_FLOOR = "e954c2e37e7c643dbde71e3f8d371c4aee04011c"
L6AC03_SOURCE_FLOOR = "734fe3a05158d8412b5d27d8c2998b6afcd4678c"
DESCRIPTOR_REF = "descriptor:l6ac/report-safe-operator-preference-card"
SOURCE_CARD_REF = "source-card:l6ac/report-safe-operator-preference-card"

EVIDENCE_TERMS = (
    "L6AC.01 fresh owner-approved source-card read approval packet (#261 / PR #266",
    "L6AC.02 owner-approved one-read receipt (#262 / PR #267",
    "L6AC.03 report-safe value/usefulness evidence packet (#263 / PR #268",
)

RESIDUAL_HOLDS = (
    "live/private reads remain held except for the already-consumed single #262 PASS receipt",
    "raw private content, raw source text, and raw approval prose remain held",
    "credentials/auth/env/keychain/OAuth/auth-file reads remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "callbacks and provider/backend/source-stat/source-read routes remain held outside the consumed #262 receipt",
    "persistence, audit/custody writes, mutation, write/delete/reindex/cache-purge, rollback execution, and cache mutation remain held",
    "service/listener/startup/cron activation and global runtime config mutation remain held",
    "publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held",
    "a second read remains held",
    "any broad `allowed=true` route remains held",
)

UNSAFE_CLASSES = (
    "raw private content",
    "raw source text",
    "raw approval prose",
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


def test_l6ac04_review_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ac04-no-live-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ac04_no_live_trust_boundary_review.py" in inventory
    assert "L6AC.04 no-live trust-boundary review" in inventory
    assert STATUS in inventory


def test_l6ac04_records_pass_continue_verdict_and_source_floors():
    text = normalized(DOC)

    required_terms = (
        "# L6AC.04 no-live trust-boundary review for fresh-read rail",
        f"Status: `{STATUS}`",
        "Rail issue: #264",
        "Parent issue: #6",
        "Blocked by: #263 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Verdict vocabulary: `PASS_CONTINUE`, `FIX_BEFORE_RECONCILE`, `HOLD_FOR_OPERATOR`",
        "Verdict: `PASS_CONTINUE`",
        "ready for reconciliation",
    )
    for term in required_terms:
        assert term in text


def test_l6ac04_reviews_completed_fresh_read_chain_without_second_read():
    text = normalized(DOC)

    for term in EVIDENCE_TERMS:
        assert term in text

    required_terms = (
        f"source floor `{L6AC01_SOURCE_FLOOR}`",
        f"source floor `{L6AC02_SOURCE_FLOOR}`",
        f"source floor `{L6AC03_SOURCE_FLOOR}`",
        "bound the next execution candidate to #262 approval comment `4651509226`",
        "executed exactly one report-safe source-card read",
        "consumed only the already-merged #262 receipt",
        "committed repo artifacts and public GitHub issue/PR metadata only",
        "No live/private read occurred in #261, #263, or #264",
        "#262 executed exactly one approved read and no second read",
        "No source discovery, workspace scan, family scan, broad recall, index query",
        "Atlas Gate movement, or broad `allowed=true` route is activated by this review",
    )
    for term in required_terms:
        assert term in text


def test_l6ac04_confirms_max_one_read_custody_and_consumed_approval():
    text = normalized(DOC)

    required_terms = (
        "The max-one read custody boundary held",
        "#262 is the only L6AC issue that carried read authority",
        "exact owner approval comment `4651509226`",
        "exact operation `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
        f"exact descriptor ref `{DESCRIPTOR_REF}`",
        f"exact source-card ref `{SOURCE_CARD_REF}`",
        "report-safe metadata/value output",
        "approval is consumed and not reusable",
        "#263, #264, #265, parent #6, PR merges, issue closures, comments, copied approval phrasing, stale timestamps, rail continuity, source-floor advancement, and this PASS review do not authorize another read",
    )
    for term in required_terms:
        assert term in text


def test_l6ac04_report_hygiene_and_stale_approval_resistance():
    text = normalized(DOC)

    assert "Report-safe redaction finding" in text
    assert "expose only report-safe issue anchors" in text
    for unsafe_class in UNSAFE_CLASSES:
        assert unsafe_class in text

    stale_terms = (
        "Stale approval resistance held",
        "denies before read if approval is absent, stale, copied, broadened, expired, mismatched, unsafe, non-owner",
        "lacks exact executable refs",
        "requests unsafe output",
        "asks for a second read",
        "attempts broad `allowed=true` behavior",
        "Future approval text remains inert unless separately fresh, owner-authored, issue-bound, target-ref-matched, and explicitly authorized on a later issue",
    )
    for term in stale_terms:
        assert term in text


def test_l6ac04_names_next_blocker_and_residual_holds():
    text = normalized(DOC)

    assert "Next exact blocker: #265 source-floor anchor, parent status, and next frontier reconciliation" in text
    assert "completed #261-#264 evidence" in text
    assert "without creating successor issues, changing cron automation, moving Atlas Gate, or authorizing another read" in text

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    unsafe_markers = (
        "raw private source text",
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
    )
    lowered = text.lower()
    for marker in unsafe_markers:
        assert marker not in lowered
