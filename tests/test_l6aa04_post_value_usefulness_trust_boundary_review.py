from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aa04-post-value-usefulness-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVIDENCE_TERMS = (
    "L6AA.01 exact owner-approved target-ref packet (#241 / PR #246)",
    "L6AA.02 owner-approved one-read value proof (#242 / PR #247)",
    "L6AA.03 value-proof receipt hygiene verifier (#243 / PR #248)",
)

RESIDUAL_HOLDS = (
    "additional live/private reads remain held",
    "raw private content remains held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "credential/auth/env/keychain/OAuth/auth-file reads remain held",
    "provider/backend/source-stat callbacks remain held",
    "Runtime Registry consumption remains held",
    "persistence, audit/custody writes, and cache mutation remain held",
    "service/listener/startup/cron activation and global runtime config mutation remain held",
    "publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held",
    "mutation, rollback, and cache-purge execution remain held",
    "any broad `allowed=true` route remains held",
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


def test_l6aa04_review_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aa04-post-value-usefulness-trust-boundary-review.md" in docs_index
    assert "tests/test_l6aa04_post_value_usefulness_trust_boundary_review.py" in inventory
    assert "L6AA.04 post-value usefulness and trust-boundary review" in inventory
    assert "PASS_CONTINUE_REPORT_SAFE_SOURCE_CARD_EVIDENCE" in inventory


def test_l6aa04_records_allowed_verdict_and_exact_reason():
    text = normalized(DOC)

    required_terms = (
        "Status: `PASS_CONTINUE_REPORT_SAFE_SOURCE_CARD_EVIDENCE`",
        "Rail issue: #244",
        "Parent issue: #6",
        "Value-proof read issue: #242",
        "Verifier issue: #243",
        "Source floor entering slice: `4df614bec8c0a1523f2be177eed512b9c769d424`",
        "#6 comment `4649391691`",
        "#215 comment `4649391836`",
        "issuecomment-4650524341",
        "Verdict vocabulary: `PASS_CONTINUE`, `FIX_BEFORE_NEXT_SOURCE`, `HOLD_FOR_OPERATOR`, `HOLD_FOR_ANCHOR_RECONCILE`",
        "Verdict: `PASS_CONTINUE`",
        "Reason: #242 passed because the fresh #242 OWNER approval comment matched the #241 executable target refs",
        "descriptor:l6aa/report-safe-operator-preference-card",
        "source-card:l6aa/report-safe-operator-preference-card",
        "PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ",
        "USEFUL_REPORT_SAFE_OPERATOR_PREFERENCE_METADATA_SEEN",
        "REPORT_SAFE_METADATA_ONLY_RAW_SOURCE_CONTENT_OMITTED",
    )
    for term in required_terms:
        assert term in text


def test_l6aa04_reviews_l6aa_evidence_chain_without_new_private_reads():
    text = normalized(DOC)

    for term in EVIDENCE_TERMS:
        assert term in text
    assert "L6AA stayed within exact one-read, report-safe, deny-before-read boundaries" in text
    assert "exactly one report-safe source-card read occurred in #242" in text
    assert "no additional live/private read occurred in #243 or #244" in text
    assert "all provider/backend/source-stat/credential/Runtime-Registry/persistence/mutation/rollback/cache-purge counters stayed at zero" in text


def test_l6aa04_usefulness_and_redaction_findings_are_metadata_only():
    text = normalized(DOC)

    required_terms = (
        "the system now has useful report-safe source-card evidence",
        "proves the target card existed, was reportable, and carried redaction labels",
        "useful source-card evidence, not raw source-content evidence",
        "not blocked on exact approval, target-ref, size, or safety constraints for the completed #242 proof",
        "does not imply a reusable approval or any standing live-read authority",
        "The redaction boundary held",
        "only report-safe metadata: issue numbers, public comment IDs, timestamps, source-floor commits, safe status labels, booleans, counters, operation class, descriptor/source-card refs, redaction labels, and usefulness labels",
    )
    for term in required_terms:
        assert term in text

    for unsafe_class in UNSAFE_CLASSES:
        assert unsafe_class in text


def test_l6aa04_cannot_authorize_another_read_or_gate_movement():
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


def test_l6aa04_names_residual_holds_and_next_exact_blocker():
    text = normalized(DOC)

    assert "Next exact blocker: #245 source-floor anchor, parent status, and next frontier reconciliation" in text
    assert "parent #6 status" in text
    assert "source-floor anchor" in text
    assert "no successor issues or cron changes" in text

    for held in RESIDUAL_HOLDS:
        assert held in text
