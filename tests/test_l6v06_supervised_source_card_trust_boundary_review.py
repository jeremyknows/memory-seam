from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6v06-supervised-source-card-trust-boundary-review.md"
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


def test_l6v06_review_is_decision_only_and_cannot_approve_execution():
    text = normalized(DOC)

    required_terms = [
        "L6V.06 supervised source-card trust-boundary review and next-use frontier",
        "Status: `PASS_DECISION_ONLY_NO_EXECUTION`",
        "Rail issue: #192",
        "Evidence rail issues: #187, #188, #189, #190, #191",
        "Source floor: `876375b` or later on `origin/main`",
        "Upstream packet: `docs/l6u05-supervised-live-use-trust-boundary-review.md`",
        "docs/tests-only and decision-only",
        "does not approve, implement, enable, activate, schedule, simulate, or execute",
        "live/private read",
        "source discovery",
        "credential/auth/env/keychain/OAuth/auth-file read",
        "Runtime Registry consumption",
        "provider/backend/source-stat/source-read callback",
        "write/custody/delete/reindex/rollback/cache-purge callback",
        "service/listener/startup/cron behavior",
        "package publication",
        "repository visibility change",
        "provider/prod/canary or production authority",
        "Atlas Gate movement",
        "`allowed=true` route",
    ]
    for term in required_terms:
        assert term in text


def test_l6v06_records_pass_without_unholding_live_or_allowed_true():
    text = normalized(DOC)

    required_terms = [
        "Verdict vocabulary: `PASS`, `HOLD`, `FIX_BEFORE_NEXT_SLICE`",
        "Verdict: `PASS`",
        "default-off, synthetic/no-live, report-safe supervised source-card proof preflight skeleton",
        "cannot perform real operator use by itself",
        "`PASS` here means the completed L6V rail is internally coherent and safe to report",
        "not live-read approval",
        "not provider/source callback approval",
        "not Runtime Registry approval",
        "not production/canary approval",
        "not package/repository visibility approval",
        "not Atlas Gate approval",
        "not permission to treat any receipt as `allowed=true`",
    ]
    for term in required_terms:
        assert term in text


def test_l6v06_summarizes_l6v01_through_l6v05_evidence():
    text = normalized(DOC)

    required_terms = [
        "Evidence summarized from L6V.01-L6V.05",
        "L6V.01 supervised source-card proof preflight skeleton (#187)",
        "src/memory_seam/supervised_source_card_preflight.py",
        "`SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`",
        "`max_operation_count=1`",
        "L6V.02 supervised proof stale/variant denial matrix (#188)",
        "tests/test_l6v01_supervised_source_card_preflight.py",
        "stale, variant, missing, copied, broadened",
        "L6V.03 report-safe source-card descriptor fixture proof (#189)",
        "tests/test_l6v03_report_safe_source_card_descriptor_fixture.py",
        "committed descriptor/source-card fixture is metadata-only",
        "L6V.04 local no-live supervised proof smoke (#190)",
        "examples/l6v_supervised_source_card_no_live_smoke.py",
        "tests/test_l6v04_supervised_source_card_no_live_smoke.py",
        "L6V.05 supervised proof public-hygiene scanner ratchet (#191)",
        "scripts/public_hygiene_scan.py",
        "tests/test_public_hygiene_scan.py",
        "docs/public-hygiene.md",
    ]
    for term in required_terms:
        assert term in text


def test_l6v06_names_residual_holds_and_next_frontier():
    text = normalized(DOC)

    residual_terms = [
        "Residual holds",
        "live/private reads and raw source content",
        "source discovery, workspace scans, family scans, broad recall, and index queries",
        "provider/backend/source-stat/source-read callbacks",
        "write/custody/delete/reindex/rollback/cache-purge callbacks and all mutation execution",
        "credentials, auth files, environment secrets, keychain entries, OAuth material, and auth-file reads",
        "Runtime Registry consumption",
        "persistence, audit/custody record writes, and cache mutation",
        "service/listener/startup/cron activation and global Hermes/MCP/client/runtime config mutation",
        "package publication, repository visibility changes, provider/prod/canary or production authority, and Atlas Gate movement",
        "any `allowed=true` route",
    ]
    for term in residual_terms:
        assert term in text

    next_terms = [
        "Recommendation: `ASK_FOR_EXACT_ISSUE_BOUND_SUPERVISED_LIVE_READ_APPROVAL_PACKET`",
        "docs/tests-only HITL approval packet",
        "exactly one future supervised live/private read",
        "fresh issue-bound approval",
        "bind issue, actor association, owner, subject, audience, scope, operation class, expiry, max-one-operation, stop conditions",
        "This recommendation is not approval text and deliberately contains no future approval phrase",
        "If Jeremy instead wants another no-live current-session integration proof first",
        "separate issue-railed docs/tests/code slice with committed synthetic fixtures only",
    ]
    for term in next_terms:
        assert term in text


def test_l6v06_is_report_safe_and_discoverable():
    text = normalized(DOC)
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    hygiene_terms = [
        "Public/reportable hygiene constraints",
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
        "public issue numbers, repository file names, synthetic operation-class names, safe descriptor/source-card refs, booleans, zero-counter facts, status strings, and verification command names only",
    ]
    for term in hygiene_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text

    assert "l6v06-supervised-source-card-trust-boundary-review.md" in docs_index
    assert "tests/test_l6v06_supervised_source_card_trust_boundary_review.py" in inventory
    assert "L6V.06 supervised source-card trust-boundary review and next-use frontier" in inventory
