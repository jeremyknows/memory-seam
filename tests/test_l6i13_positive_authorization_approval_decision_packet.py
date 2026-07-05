from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "docs" / "l6-positive-authorization-approval-decision-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

APPROVAL_PHRASE = (
    "I approve Memory Seam to implement `L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON` "
    "for synthetic/no-production testing only, limited to max one operation"
)

PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
)

GUARDED_COUNTERS = (
    "allowed_result_count=0",
    "provider_callback_count=0",
    "backend_callback_count=0",
    "source_stat_callback_count=0",
    "source_read_callback_count=0",
    "write_callback_count=0",
    "custody_callback_count=0",
    "delete_callback_count=0",
    "reindex_callback_count=0",
    "rollback_callback_count=0",
    "cache_purge_callback_count=0",
    "persistent_receipt_count=0",
    "durable_write_record_count=0",
    "audit_persistence_count=0",
    "cache_mutation_count=0",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6i13_packet_is_hitl_decision_only_not_approval():
    text = normalized(PACKET)

    required_terms = [
        "L6I.13 positive-authorization approval decision packet",
        "docs/tests-only HITL decision packet",
        "request artifact only",
        "future-only",
        "non-executable",
        "not approval by itself",
        "does not implement runtime behavior",
        "does not add any code path returning `allowed=true`",
        "does not recognize approval at runtime",
        "Source floor: `7980a5b` or later `origin/main`",
        "Dependency: L6I.12 closed/PASS via issue `#154` and PR `#161`",
        "Selected candidate from L6I.12: `L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON`",
        "SPLIT_AGAIN_DOCS_TESTS_ONLY",
        "This quoted language is future-only approval language",
        "Its presence in this repository, this issue, a PR body, a merged commit, or a closed issue is not approval",
        "template requiring a later explicit human approval event",
    ]
    for term in required_terms:
        assert term in text


def test_l6i13_exact_future_approval_language_is_present_and_bounded():
    text = normalized(PACKET)

    assert text.count(APPROVAL_PHRASE) == 1

    approval_terms = [
        "L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON",
        "synthetic/no-production testing only",
        "limited to max one operation",
        "named issue and actor binding",
        "recognizing only this exact fresh approval phrase and its required fields",
        "emitting only a non-persistent report-safe receipt",
        "status `positive_authorization_recognized_mutation_held`",
        "keeping mutation unsupported",
        "`mutation_attempted=false`",
        "`mutation_supported=false`",
        "preserving `allowed_result_count=0`",
        "denying or stopping before all provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "persistence",
        "source discovery",
        "live/private reads",
        "Runtime Registry consumption",
        "global configuration mutation",
        "service/listener/startup/cron activation",
        "publication",
        "repository visibility change",
        "provider/prod/canary authority",
        "Atlas Gate movement",
    ]
    for term in approval_terms:
        assert term in text


def test_l6i13_rejects_stale_variant_implied_and_copied_approval():
    text = normalized(PACKET)

    rejected_terms = [
        "stale approval",
        "variant approval",
        "paraphrased approval",
        "implied approval",
        "approval implied by issue closure",
        "approval implied by PR merge",
        "approval implied by labels, milestones, project placement, branch names, or check success",
        "approval copied from issue `#137`",
        "approval copied from this packet without a later explicit human approval event",
        "actor-mismatched approval",
        "subject-mismatched approval",
        "owner-mismatched approval",
        "expired approval",
        "missing operation class",
        "over max operation count",
        "not issue `#137`",
        "Reject stale reuse, copied approvals, unrelated issue references, issue-closure inference, or PR-merge inference",
        "Reject variant approval, paraphrase, implied approval, label-only approval, title-only approval, or approval copied from issue `#137`",
    ]
    for term in rejected_terms:
        assert term in text


def test_l6i13_required_fields_and_future_acceptance_gates_are_bound():
    text = normalized(PACKET)

    required_fields = [
        "Issue binding",
        "Exact phrase reference",
        "Actor binding",
        "Expiry",
        "Max operation count",
        "Operation class",
        "Target posture",
        "Receipt posture",
        "fresh, exact, issue-bound, actor-bound, unexpired",
        "receipt-only positive-authorization recognition",
        "synthetic/no-production only",
        "non-persistent and report-safe",
        "`fixture_is_persistent=false`",
        "rollback remains no-op/posture-only",
        "audit remains report-safe/non-persistent unless a separate later approval explicitly authorizes durable audit storage",
    ]
    for term in required_fields:
        assert term in text

    for counter in GUARDED_COUNTERS:
        assert counter in text


def test_l6i13_residual_holds_and_rollback_audit_requirements_are_carried_forward():
    text = normalized(PACKET)

    held_terms = [
        "does not authorize implementation",
        "runtime approval acceptance",
        "any positive allowed runtime path",
        "`allowed=true`",
        "mutation",
        "write execution",
        "custody transfer",
        "custody persistence",
        "delete execution",
        "reindex execution",
        "rollback execution",
        "cache-purge execution",
        "provider callbacks",
        "backend callbacks",
        "source-stat callbacks",
        "source-read callbacks",
        "persistence",
        "live/private reads",
        "source discovery",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "service/listener/startup/cron activation",
        "recurring runner activation",
        "provider/prod/canary authority",
        "repository visibility change",
        "package publication",
        "Atlas Gate movement",
        "production-authoritative claims",
        "Without that fresh approval event, the correct next state remains HOLD",
    ]
    for term in held_terms:
        assert term in text


def test_l6i13_public_hygiene_and_discoverability_are_preserved():
    combined = " ".join(
        normalized(path) for path in (PACKET, DOCS_INDEX, CONTRACT_TEST_INVENTORY)
    )

    discoverability_terms = [
        "l6-positive-authorization-approval-decision-packet.md",
        "tests/test_l6i13_positive_authorization_approval_decision_packet.py",
        "L6I.13 positive-authorization approval decision packet",
        "L6I.13 docs/tests-only HITL decision packet",
    ]
    for term in discoverability_terms:
        assert term in combined

    hygiene_terms = [
        "raw private source text",
        "credentials",
        "auth/env/keychain material",
        "OAuth/auth-file material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "raw payload content",
        "private correlation refs",
        "raw approval text",
    ]
    for term in hygiene_terms:
        assert term in combined

    for marker in PRIVATE_MARKERS:
        assert marker not in combined
