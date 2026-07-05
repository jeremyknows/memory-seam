from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-supervised-live-use-next-rail-decision-packet.md"
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

ISSUE_TITLES = (
    "L6U.01: supervised live-use adapter wiring map",
    "L6U.02: supervised live-read approval packet",
    "L6U.03: local integration smoke design",
    "L6U.04: dogfood/use-proof prompt set",
    "L6U.05: supervised live-use trust-boundary review",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6p07_packet_selects_issue_rail_only_not_approval_phrase():
    text = normalized(DOC)

    required_terms = [
        "L6P.07 supervised live-use next-rail decision packet",
        "Status: `HITL_ISSUE_RAIL_PACKET_ONLY`",
        "Decision: `SELECT_SUPERVISED_LIVE_USE_ISSUE_RAIL`",
        "Rail issue: #169",
        "Prerequisite: #168 closed/PASS",
        "Selected next artifact type: `ISSUE_RAIL`",
        "Rejected next artifact type: `FUTURE_APPROVAL_PHRASE`",
        "not an implementation approval phrase",
        "does not include future exact approval language",
        "the next rail is an issue rail only",
        "No implementation approval phrase is drafted in this packet",
    ]
    for term in required_terms:
        assert term in text

    assert text.count("Selected next artifact type:") == 1
    assert text.count("Rejected next artifact type:") == 1


def test_l6p07_packet_preserves_no_execution_no_live_boundaries():
    text = normalized(DOC)

    required_terms = [
        "docs/tests only, HITL-only, no-execution, and no-approval",
        "does not approve implementation",
        "does not perform live/private reads",
        "does not read credentials",
        "does not discover sources",
        "provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "does not persist receipts or audit records",
        "does not consume Runtime Registry data",
        "does not mutate global Hermes/MCP/client/runtime configuration",
        "does not activate a service/listener/startup/cron path",
        "does not publish a package",
        "does not change repository visibility",
        "does not claim provider/prod/canary authority",
        "does not move Atlas Gate",
    ]
    for term in required_terms:
        assert term in text


def test_l6p07_packet_carries_forward_l6p06_evidence_and_gap():
    text = normalized(DOC)

    required_terms = [
        "positive_authorization_recognized_mutation_held",
        "allowed=false",
        "mutation_attempted=false",
        "mutation_supported=false",
        "allowed_result_count=0",
        "callback, persistence, source, activation, publication, provider/prod/canary, production, and Atlas Gate surfaces remain held",
        "near-term value gap is one supervised read-side usefulness proof over an operator-approved target",
        "supervised live-read adapter approval packet",
        "needs its own issue-bound HITL drafting and tests",
    ]
    for term in required_terms:
        assert term in text


def test_l6p07_packet_proposes_all_five_deck_friendly_issues_with_acceptance():
    text = normalized(DOC)

    for title in ISSUE_TITLES:
        assert title in text

    # Every issue section carries the bounded shape the operator can turn into GitHub issues.
    assert text.count("Scope:") >= len(ISSUE_TITLES)
    assert text.count("No-go:") >= len(ISSUE_TITLES)
    assert text.count("Acceptance:") >= len(ISSUE_TITLES)

    required_terms = [
        "Map the minimal adapter boundary for one future supervised live-use proof",
        "Draft future-only exact approval requirements for one bounded supervised read-side proof",
        "Define a local no-live smoke plan for adapter import/wiring using committed synthetic fixtures only",
        "Draft report-safe dogfood prompts and usefulness rubric for one future supervised read-side proof",
        "Summarize L6U.01-L6U.04 evidence and decide PASS/HOLD/FIX_BEFORE_NEXT_SLICE",
    ]
    for term in required_terms:
        assert term in text


def test_l6p07_packet_orders_rail_and_keeps_implementation_held():
    text = normalized(DOC)

    assert "Recommended order: L6U.01 adapter wiring map → L6U.02 approval packet → L6U.03 local integration smoke design → L6U.04 dogfood/use-proof prompt set → L6U.05 trust-boundary review." in text
    assert "parallel-friendly for deck review" in text
    assert "merge/execution order should stay gated" in text
    assert "no implementation or live/private read work should begin until the approval packet and trust-boundary review produce an explicit PASS" in text
    assert "Jeremy supplies any required fresh approval" in text


def test_l6p07_packet_is_report_safe_and_restates_preserved_holds():
    text = normalized(DOC)

    required_terms = [
        "implementation and execution of live/private reads",
        "source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, and Runtime Registry consumption",
        "mutation execution, `allowed=true` result paths, write execution, custody transfer, custody receipt persistence, delete, reindex, rollback, and cache purge",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "service/listener/startup/cron activation and recurring runner behavior",
        "global Hermes/MCP/client/runtime configuration mutation",
        "package publication, repository visibility changes, provider/prod/canary authority, production authority, and Atlas Gate movement",
    ]
    for term in required_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6p07_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-supervised-live-use-next-rail-decision-packet.md" in docs_index
    assert "tests/test_l6p07_supervised_live_use_next_rail_decision_packet.py" in inventory
    assert "L6P.07 supervised live-use next-rail decision packet" in inventory
    assert "SELECT_SUPERVISED_LIVE_USE_ISSUE_RAIL" in inventory
    assert "future approval phrase" in inventory
