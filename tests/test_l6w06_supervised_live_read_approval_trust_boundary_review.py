from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6w06-supervised-live-read-approval-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EVIDENCE_TERMS = (
    "L6W.01 exact supervised live-read approval packet scaffold (#199)",
    "L6W.02 stale/variant denial matrix (#200)",
    "L6W.03 report-safe receipt output contract (#201)",
    "L6W.04 local no-live approval smoke (#202)",
    "L6W.05 rollback and stop-condition proof (#203)",
)

RESIDUAL_HOLDS = (
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
)

STOP_CLASSES = (
    "denial-before-callback",
    "expiry/missing approval",
    "binding mismatch",
    "stale/variant/copy",
    "report-hygiene failure",
    "operator revocation",
    "broadened/allowed-true",
    "callback/mutation",
    "registry/activation/production",
)

UNSAFE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
    "source://",
    "I approve Memory Seam",
    "approval is granted",
    "allowed=true route is present",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6w06_review_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6w06-supervised-live-read-approval-trust-boundary-review.md" in docs_index
    assert "tests/test_l6w06_supervised_live_read_approval_trust_boundary_review.py" in inventory
    assert "L6W.06 supervised live-read approval trust-boundary review" in inventory
    assert "PASS_DECISION_ONLY_NO_APPROVAL_NO_EXECUTION" in inventory


def test_l6w06_records_pass_and_evidence_from_completed_rail():
    text = normalized(DOC)

    required_terms = [
        "Status: `PASS_DECISION_ONLY_NO_APPROVAL_NO_EXECUTION`",
        "Rail issue: #204",
        "Prerequisite: #203 closed/PASS",
        "Source floor: `9264533` or later on `origin/main`",
        "Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`",
        "Verdict vocabulary: `PASS`, `HOLD`, `FIX_BEFORE_NEXT_SLICE`",
        "Verdict: `PASS`",
        "docs/tests/default-off, synthetic/no-live, report-safe supervised live-read approval preparation rail",
    ]
    for term in required_terms:
        assert term in text
    for evidence_term in EVIDENCE_TERMS:
        assert evidence_term in text


def test_l6w06_is_decision_only_and_cannot_be_treated_as_approval():
    text = normalized(DOC)

    non_approval_terms = [
        "docs/tests-only and decision-only",
        "It does not approve, recognize, implement, enable, activate, simulate, or execute any live/private read",
        "not live-read approval",
        "not approval-recognition implementation",
        "not source/provider callback approval",
        "not Runtime Registry approval",
        "not persistence or audit/custody approval",
        "not production/canary approval",
        "not package/repository visibility approval",
        "not Atlas Gate approval",
        "not permission to treat any receipt as `allowed=true`",
        "This packet does not contain approval language that can be treated as granted",
        "It is only a recommendation to ask",
    ]
    for term in non_approval_terms:
        assert term in text
    for marker in UNSAFE_MARKERS:
        assert marker not in text


def test_l6w06_names_residual_holds_and_exact_frontier():
    text = normalized(DOC)

    assert "Frontier state: `READY_TO_ASK_OWNER_FOR_EXACT_ONE_READ_APPROVAL_OR_HOLD_FOR_MORE_NO_LIVE_PROOF`" in text
    assert "Recommended next action: ask Jeremy, in a fresh issue-bound owner comment" in text
    assert "operation class `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`" in text
    assert "If Jeremy prefers another no-live slice first" in text
    assert "new docs/tests/synthetic-only proof that consumes committed fixtures only" in text

    for held_term in RESIDUAL_HOLDS:
        assert held_term in text


def test_l6w06_carries_stop_conditions_and_rollback_forward():
    text = normalized(DOC)

    for stop_class in STOP_CLASSES:
        assert stop_class in text

    result_terms = [
        "`approval_result`: `DENIED_BEFORE_CALLBACK`",
        "`rollback_status`: `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`",
        "`live_read_invoked`: `false`",
        "`allowed`: `false`",
        "`allowed_result_count`: `0`",
        "guarded provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge counters remain synthetic zeros",
        "source-discovery, Runtime Registry, credential/auth, persistence/audit/custody/cache, activation, publication/visibility, provider/prod/canary, Atlas Gate, mutation, rollback, and cache-purge counters remain zero",
        "must stop the candidate before any live/private read or callback",
    ]
    for term in result_terms:
        assert term in text


def test_l6w06_preserves_public_report_hygiene_constraints():
    text = normalized(DOC)

    safe_terms = [
        "public issue numbers",
        "repository file names",
        "synthetic operation-class names",
        "safe descriptor/source-card refs",
        "booleans",
        "zero-counter facts",
        "status strings",
        "verification command names only",
    ]
    unsafe_terms = [
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
    ]
    for term in safe_terms + unsafe_terms:
        assert term in text
