from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ad04-no-live-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_TRUST_BOUNDARY_REVIEW_OWNER_DECISION_HOLD"
VERDICT = "PASS_TRUST_BOUNDARY_REVIEW"
NEXT_FRONTIER = "OWNER_DECISION_HOLD_FOR_IMPLEMENTATION_AUTHORITY"
RAIL_STARTING_SOURCE_FLOOR = "f606ed18737d057f0b544503c2532935a9d6c258"
SOURCE_FLOOR_ENTERING_SLICE = "6c4c1b8bb27c09d099c62dc84139b03a4f6f4abd"
PARENT_SUCCESSOR_COMMENT = "4651958877"
OPERATION_CLASS = "L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON"
DESCRIPTOR_REF = "descriptor:l6ac/report-safe-operator-preference-card"
SOURCE_CARD_REF = "source-card:l6ac/report-safe-operator-preference-card"

EVIDENCE_TERMS = (
    "L6AD.01 post-L6AC evidence inventory and implementation blocker map (#271 / PR #276 / source floor `5d42de21671bb885433bc23d6f5aac9e2be094dc`)",
    "L6AD.02 implementation-or-hold decision packet (#272 / PR #277 / source floor `5157d40a5903ba54129b61ad5c8417df467300c8`)",
    "L6AD.03 default-off implementation unhold candidate design (#273 / PR #278 / source floor `6c4c1b8bb27c09d099c62dc84139b03a4f6f4abd`)",
)

RESIDUAL_HOLDS = (
    "implementation/runtime execution remains held until a separate exact owner-created future implementation issue approval exists",
    "live/private reads and any additional source-card read beyond the consumed historical #262 evidence remain held",
    "raw private content, raw source text, raw approval prose, credentials, auth material, env/keychain/OAuth/auth-file reads remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "provider/backend/source-stat/source-read callbacks remain held",
    "persistence, mutation, audit/custody writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation remain held",
    "service/listener/startup/global activation and recursive cron/schedule changes remain held",
    "publication, visibility changes, provider/prod/canary authority, and Atlas Gate movement remain held",
    "broad `allowed=true` behavior remains held",
)

UNSAFE_CLASSES = (
    "raw private content",
    "raw source text",
    "raw approval prose",
    "credentials",
    "auth material",
    "environment values",
    "keychain material",
    "OAuth material",
    "auth-file material",
    "source locations",
    "platform identifiers",
    "private paths",
    "prompt/query/payload bodies",
    "backend responses",
    "private correlation references",
    "Runtime Registry handles",
    "provider handles",
    "secret values",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ad04_review_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ad04-no-live-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ad04_no_live_trust_boundary_review.py" in inventory
    assert "L6AD.04 no-live trust-boundary review" in inventory
    assert STATUS in inventory


def test_l6ad04_records_status_source_floor_and_owner_decision_hold():
    text = normalized(DOC)

    required_terms = (
        "# L6AD.04 no-live trust-boundary review for implementation-or-hold rail",
        f"Status: `{STATUS}`",
        "Rail issue: #274",
        "Parent issue: #6",
        "Blocked by: #273 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        "Verdict vocabulary: `PASS_TRUST_BOUNDARY_REVIEW`, `FIX_BEFORE_RECONCILE`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
        "The next implementation frontier is therefore an owner-decision HOLD",
    )
    for term in required_terms:
        assert term in text


def test_l6ad04_reviews_l6ad_chain_and_no_live_boundary():
    text = normalized(DOC)

    for term in EVIDENCE_TERMS:
        assert term in text

    required_terms = (
        "inventoried #261-#265 and PR #266-#270",
        "returned `PASS_UNHOLD_PACKET_READY_IMPLEMENTATION_NOT_APPROVED`",
        "remaining docs/tests/design-only with no code/runtime implementation",
        "committed repository docs/tests and public GitHub issue/PR metadata only",
        "no live/private read, no raw private content access, no additional source-card read",
        "no credential/auth/env/keychain/OAuth/auth-file read",
        "no Runtime Registry consumption",
        "no persistence, no mutation, no write/delete/reindex/cache-purge",
        "no service/global activation",
        "no provider/prod/canary movement, no Atlas Gate movement",
        "no cron change, and no broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6ad04_confirms_consumed_262_approval_not_reusable():
    text = normalized(DOC)

    required_terms = (
        "The #262 one-read approval remains consumed historical evidence only",
        "authorized exactly one L6AC `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
        f"`{DESCRIPTOR_REF}` and `{SOURCE_CARD_REF}`",
        "that one approved read was completed and merged before L6AD began",
        "not reusable by parent #6, parent successor comment `4651958877`, L6AD issue creation, #271 inventory authorization, #272 decision wording, #273 candidate future approval wording, #274 review PASS, #275 reconciliation",
        "PR merges, issue closures, labels, copied text, stale comments, source-floor advancement, rail continuity, or any future implementation issue",
    )
    for term in required_terms:
        assert term in text


def test_l6ad04_verifies_no_implementation_or_runtime_occurrence():
    text = normalized(DOC)

    required_terms = (
        "No L6AD artifact in #271-#274 implements or activates the future adapter candidate",
        "future file names and approval sentence in #272/#273 are design artifacts only",
        "They do not create `src/memory_seam/l6ad_report_safe_source_card_value_adapter.py`",
        "do not export a runtime symbol",
        "do not start a service",
        "do not call a provider",
        "do not consume Runtime Registry data",
        "do not persist receipts",
        "do not mutate caches or indexes",
        "do not execute rollback machinery",
        "do not move provider/prod/canary state or Atlas Gate",
        f"operation class `{OPERATION_CLASS}`",
        "fresh OWNER approval",
        "exact file envelope, fixture-only inputs, report-safe outputs",
    )
    for term in required_terms:
        assert term in text


def test_l6ad04_report_hygiene_and_stale_approval_resistance():
    text = normalized(DOC)

    assert "Report-safe redaction finding" in text
    assert "expose only report-safe issue anchors" in text
    for unsafe_class in UNSAFE_CLASSES:
        assert unsafe_class in text

    stale_terms = (
        "Stale approval resistance held",
        "rejects implied approval from consumed historical reads, parent comments, issue creation, design wording, copied future approval templates, PR merges, issue closures, labels, rail continuity, source-floor advancement, or PASS review language",
        "deny before any adapter action if approval is missing, stale, copied from prior issue, broadened, expired, mismatched to repository/issue/operation/files, non-owner",
        "permits more than one slice",
        "permits live/private reads",
        "asks for another source-card read",
        "requests credentials/auth/env/keychain/OAuth/auth-file access",
        "requests source discovery or Runtime Registry consumption",
        "requests callbacks",
        "requests publication/provider/prod/canary/Gate movement",
        "attempts broad `allowed=true` behavior",
    )
    for term in stale_terms:
        assert term in text


def test_l6ad04_names_next_blocker_and_residual_holds():
    text = normalized(DOC)

    assert "Next exact blocker: #275 source-floor anchor, parent status, and next frontier reconciliation" in text
    assert "reconcile completed #271-#274 evidence" in text
    assert "carry the owner-decision HOLD for implementation authority" in text
    assert "without creating successor issues, changing cron automation, moving Atlas Gate, authorizing implementation/runtime execution, or authorizing another read" in text

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    unsafe_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
    )
    lowered = text.lower()
    for marker in unsafe_markers:
        assert marker not in lowered
