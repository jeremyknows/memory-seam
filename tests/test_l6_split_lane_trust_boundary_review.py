from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-split-lane-trust-boundary-review.md"
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


def test_trust_boundary_review_is_decision_only_no_execution():
    text = normalized(DOC)

    required_terms = [
        "L6S.05 split-lane trust-boundary review packet",
        "Status: `TRUST_BOUNDARY_REVIEW_PACKET_ONLY`",
        "Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`",
        "docs/tests only",
        "does not implement, authorize, activate, schedule, simulate, or execute writes, custody transfer, delete, reindex, rollback, cache purge",
        "service/listener/cron/startup behavior",
        "source discovery",
        "unsupervised reads",
        "live/private source reads",
        "provider/backend/source-stat/source-read callbacks",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "provider/prod/canary authority",
        "repository visibility changes",
        "package publication",
        "Atlas Gate movement",
        "This L6S.05 packet is not approval.",
    ]
    for term in required_terms:
        assert term in text


def test_trust_boundary_review_summarizes_l6s_evidence():
    text = normalized(DOC)

    required_terms = [
        "Completed L6S evidence",
        "L6S.01 ownership and approval model",
        "docs/l6-write-custody-approval-model.md",
        "tests/test_l6_write_custody_approval_model.py",
        "operation class, custody owner, Jeremy as exact approver, actor binding, expiry, max operation count, and report-safe approval reference",
        "L6S.02 rollback and audit plan",
        "docs/l6-write-custody-rollback-audit-plan.md",
        "tests/test_l6_write_custody_rollback_audit_plan.py",
        "rollback shape, audit fields, stop conditions, timeout, and failure modes",
        "L6S.03 operation-class fixtures",
        "docs/l6-write-custody-operation-class-fixtures.md",
        "tests/test_l6_write_custody_operation_class_fixtures.py",
        "Write intent, custody receipt persistence, delete, reindex, rollback, and cache purge",
        "L6S.04 denied-before-mutation harness",
        "docs/l6-denial-before-mutation-harness.md",
        "tests/test_l6_denial_before_mutation_harness.py",
        "all guarded counters stay at `0`",
    ]
    for term in required_terms:
        assert term in text


def test_trust_boundary_review_records_residual_risks_and_holds():
    text = normalized(DOC)

    required_terms = [
        "Residual risks",
        "Mutation blast radius remains unproven.",
        "Approval spoofing and stale approval remain risks.",
        "Rollback readiness remains paper-only.",
        "Callback isolation remains a contract.",
        "Operational activation remains out of scope.",
        "Residual held surfaces",
        "write execution",
        "custody transfer",
        "delete execution",
        "reindex execution",
        "rollback execution",
        "cache purge execution",
        "provider/backend/source-stat/source-read callbacks",
        "service/listener/cron/startup behavior",
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


def test_trust_boundary_review_recommends_exact_future_approval_request_only():
    text = normalized(DOC)

    required_terms = [
        "Recommendation",
        "ASK JEREMY FOR ONE EXACT IMPLEMENTATION-SLICE APPROVAL",
        "Do not HOLD solely because the split-lane planning lacks execution evidence",
        "Do not SPLIT again unless Jeremy wants more paper design",
        "one bounded, non-production implementation slice that remains non-executing unless a separate execution approval is later granted",
        "The recommended future ask should be drafted by L6S.06",
        "the packet itself is not approval",
        "implementation is still held until Jeremy posts the exact approval phrase for the named issue",
    ]
    for term in required_terms:
        assert term in text


def test_trust_boundary_review_is_report_safe():
    text = normalized(DOC)

    required_terms = [
        "Public/reportable hygiene status",
        "public issue numbers, file names, synthetic operation-class names, boolean/counter facts, and safe error-code style terms",
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
    ]
    for term in required_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_trust_boundary_review_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-split-lane-trust-boundary-review.md" in docs_index
    assert "tests/test_l6_split_lane_trust_boundary_review.py" in inventory
    assert "L6S.05 split-lane trust-boundary review packet" in inventory
