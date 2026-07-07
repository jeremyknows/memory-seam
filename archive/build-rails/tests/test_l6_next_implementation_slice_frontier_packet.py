from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-next-implementation-slice-frontier-packet.md"
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


def test_l6i06_frontier_packet_is_hitl_decision_only_no_execution():
    text = normalized(DOC)

    required_terms = [
        "L6I.06 next implementation-slice frontier packet",
        "Status: `HITL_DECISION_PACKET_ONLY`",
        "Recommendation: `SPLIT_AGAIN_DOCS_TESTS_ONLY`",
        "Rail issue: #142",
        "Evidence rail issues: #137, #138, #139, #140, #141",
        "docs/tests only and HITL decision-only",
        "does not approve, implement, enable, activate, schedule, simulate, or execute writes",
        "custody transfer, custody receipt persistence, delete, reindex, rollback, cache purge",
        "provider/backend/source-stat/source-read callbacks",
        "source discovery",
        "live/private source reads",
        "unsupervised reads",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "service/listener/cron/startup behavior",
        "repository visibility changes",
        "package publication",
        "Atlas Gate movement",
    ]
    for term in required_terms:
        assert term in text


def test_l6i06_frontier_recommends_split_again_without_implementation_approval():
    text = normalized(DOC)

    required_terms = [
        "Frontier decision",
        "The recommended next move is `SPLIT_AGAIN_DOCS_TESTS_ONLY`",
        "prepare a separate HITL decision packet",
        "does **not** recommend another implementation slice",
        "does **not** include an implementation approval phrase",
        "Any future implementation slice remains held until a later packet names one bounded slice",
        "This packet itself is not approval",
        "no variant, merge event, issue close, label, assignment, emoji reaction, checklist item, stale approval, unrelated comment, or CI result is implementation approval",
    ]
    for term in required_terms:
        assert term in text

    assert "I approve Memory Seam to implement" not in text


def test_l6i06_frontier_summarizes_l6i_evidence():
    text = normalized(DOC)

    required_terms = [
        "Evidence summarized from L6I.01-L6I.05",
        "L6I.01 write-intent preflight gate skeleton (#137)",
        "src/memory_seam/write_intent_preflight_gate.py",
        "operation class `write intent` only",
        "L6I.02 denial receipt metadata (#138)",
        "build_l6_write_intent_denial_receipt_metadata()",
        "Positive authorization receipt semantics remain unimplemented",
        "L6I.03 stale/mismatched approval hardening (#139)",
        "Wrong issue, wrong actor association, wrong approval reference, wrong operation class, exceeded synthetic-operation limit, stale approval window, and expired approval",
        "L6I.04 no-production smoke (#140)",
        "exactly one committed synthetic `write intent` request",
        "L6I.05 independent trust-boundary review (#141)",
        "PASS is not approval for a new implementation slice",
    ]
    for term in required_terms:
        assert term in text


def test_l6i06_frontier_names_residual_risks_and_holds():
    text = normalized(DOC)

    required_terms = [
        "Residual risks",
        "proves denial ordering only",
        "does not prove safe write execution",
        "positive authorization receipt semantics and audit persistence remain unimplemented",
        "does not carry forward to any next slice",
        "no runtime rollback execution or audit persistence authority exists",
        "fresh HITL review before implementation approval is requested",
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


def test_l6i06_frontier_is_report_safe():
    text = normalized(DOC)

    required_terms = [
        "Public/reportable hygiene constraints",
        "raw private source text",
        "credentials",
        "auth/env/keychain material",
        "OAuth material",
        "auth-file material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "raw payload content",
        "private correlation refs",
        "public issue numbers, repository file names, synthetic operation-class names, boolean/counter facts, and safe status strings only",
    ]
    for term in required_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6i06_frontier_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-next-implementation-slice-frontier-packet.md" in docs_index
    assert "tests/test_l6_next_implementation_slice_frontier_packet.py" in inventory
    assert "L6I.06 next implementation-slice frontier packet" in inventory
