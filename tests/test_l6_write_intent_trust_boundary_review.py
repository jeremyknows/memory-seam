from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-write-intent-trust-boundary-review.md"
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


def test_l6i_trust_boundary_review_is_decision_only_no_execution():
    text = normalized(DOC)

    required_terms = [
        "L6I.05 write-intent skeleton trust-boundary review packet",
        "Status: `TRUST_BOUNDARY_REVIEW_PACKET_ONLY`",
        "Review verdict: `PASS`",
        "Rail issue: #141",
        "Reviewed rail issues: #137, #138, #139, #140",
        "docs/tests only and decision-only",
        "does not add implementation behavior",
        "execute writes, transfer custody, persist custody receipts, delete, reindex, rollback, cache purge",
        "provider/backend/source-stat/source-read callbacks",
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


def test_l6i_trust_boundary_review_states_required_verdict_vocabulary():
    text = normalized(DOC)

    assert "The review outcome vocabulary is exactly `PASS`, `HOLD`, or `FIX_BEFORE_NEXT_SLICE`." in text
    assert "This packet records `PASS`" in text
    assert "The PASS is not approval for a new implementation slice" in text
    assert "does not unhold any residual surface" in text


def test_l6i_trust_boundary_review_summarizes_l6i_evidence():
    text = normalized(DOC)

    required_terms = [
        "Evidence reviewed",
        "L6I.01 write-intent preflight gate skeleton (#137)",
        "src/memory_seam/write_intent_preflight_gate.py",
        "tests/test_l6_write_intent_preflight_gate.py",
        "docs/l6-write-intent-preflight-gate.md",
        "operation class `write intent` only",
        "L6I.02 denial receipt metadata (#138)",
        "build_l6_write_intent_denial_receipt_metadata()",
        "denied no-mutation paths with zero guarded counters",
        "L6I.03 approval-denial hardening (#139)",
        "Wrong issue, wrong actor association, wrong approval reference, wrong operation class, exceeded synthetic-operation limit, stale approval window, and expired approval",
        "L6I.04 local no-production smoke (#140)",
        "examples/write_intent_preflight_smoke.py",
        "exactly one committed synthetic `write intent` request",
        "guarded counters at zero",
    ]
    for term in required_terms:
        assert term in text


def test_l6i_trust_boundary_review_records_pass_findings_and_residual_risks():
    text = normalized(DOC)

    required_terms = [
        "Trust-boundary findings",
        "Public hygiene: PASS.",
        "Denial before callback: PASS.",
        "No-production posture: PASS.",
        "Approval binding: PASS for the reviewed slice only.",
        "Residual holds: PASS with holds preserved.",
        "issue-137-comment-4643939613",
        "Residual risks before any next slice",
        "preflight denial ordering only",
        "positive authorization receipt semantics remain unimplemented",
        "any next slice needs its own HITL decision packet and exact approval",
        "no runtime rollback execution or audit persistence authority exists",
        "synthetic denied path",
    ]
    for term in required_terms:
        assert term in text


def test_l6i_trust_boundary_review_preserves_hard_holds():
    text = normalized(DOC)

    required_terms = [
        "Residual held surfaces",
        "write execution",
        "custody transfer and custody receipt persistence",
        "delete execution",
        "reindex execution",
        "rollback execution",
        "cache purge execution",
        "provider/backend/source-stat/source-read callbacks",
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


def test_l6i_trust_boundary_review_is_report_safe():
    text = normalized(DOC)

    required_terms = [
        "Public artifacts must still exclude raw private source text",
        "credentials",
        "auth/env/keychain material",
        "OAuth material",
        "auth-file material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "raw payload content",
        "private correlation refs",
    ]
    for term in required_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6i_trust_boundary_review_recommends_l6i06_packet_only():
    text = normalized(DOC)

    required_terms = [
        "Proceed to L6I.06 as a HITL decision packet only.",
        "must not implement behavior",
        "must not treat this `PASS` as approval",
        "own exact Jeremy approval bound to a named issue, operation class, max operation count, expiry, rollback/audit expectations, no-go surfaces, and report-safe evidence requirements",
    ]
    for term in required_terms:
        assert term in text


def test_l6i_trust_boundary_review_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-write-intent-trust-boundary-review.md" in docs_index
    assert "tests/test_l6_write_intent_trust_boundary_review.py" in inventory
    assert "L6I.05 write-intent skeleton trust-boundary review packet" in inventory
