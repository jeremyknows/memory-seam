from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6x02-supervised-one-read-deny-before-read-hold.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

ZERO_COUNTER_TERMS = (
    "approval_comments_examined: `0`",
    "valid_owner_approval_comments: `0`",
    "live_read_invoked: `false`",
    "allowed: `false`",
    "allowed_result_count: `0`",
    "provider_callbacks: `0`",
    "backend_callbacks: `0`",
    "source_stat_callbacks: `0`",
    "source_read_callbacks: `0`",
    "credential_reads: `0`",
    "runtime_registry_reads: `0`",
    "persistence_writes: `0`",
    "mutation_callbacks: `0`",
    "rollback_callbacks: `0`",
    "cache_purge_callbacks: `0`",
)

DENIAL_REASONS = (
    "approval_absent: `DENY_BEFORE_READ`",
    "owner_actor_association_missing: `DENY_BEFORE_READ`",
    "bound_issue_id_missing: `DENY_BEFORE_READ`",
    "operation_class_missing: `DENY_BEFORE_READ`",
    "expiry_missing: `DENY_BEFORE_READ`",
    "descriptor_source_card_ref_missing: `DENY_BEFORE_READ`",
)

PRESERVED_HOLDS = (
    "no live/private reads",
    "no source discovery, workspace scans, family scans, broad recall, or index queries",
    "no credential/auth/env/keychain/OAuth/auth-file reads",
    "no provider/backend/source-stat/source-read callbacks",
    "no write/custody/delete/reindex/rollback/cache-purge callbacks",
    "no persistence, audit/custody writes, or cache mutation",
    "no service/listener/startup/cron activation or global runtime config mutation",
    "no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement",
    "no mutation execution, rollback execution, cache-purge execution, or `allowed=true` route",
)

UNSAFE_MARKERS = (
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
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6x02_hold_proof_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6x02-supervised-one-read-deny-before-read-hold.md" in docs_index
    assert "tests/test_l6x02_supervised_one_read_deny_before_read_hold.py" in inventory
    assert "L6X.02 supervised one-read deny-before-read HOLD" in inventory
    assert "HOLD_DENIED_BEFORE_READ_NO_APPROVAL_NO_LIVE" in inventory


def test_l6x02_records_absent_approval_and_no_live_decision():
    text = normalized(DOC)

    required_terms = (
        "Status: `HOLD_DENIED_BEFORE_READ_NO_APPROVAL_NO_LIVE`",
        "Rail issue: #212",
        "Parent issue: #6",
        "Approval source checked: #212 owner comments",
        "Approval packet dependency: `docs/l6x01-one-read-approval-request-packet.md`",
        "Exact approval result: `ABSENT`",
        "Decision: `DENY_BEFORE_READ`",
        "No supervised report-safe source-card live read was executed",
        "No approved already-named tool path was present",
    )
    for term in required_terms:
        assert term in text


def test_l6x02_absent_approval_denies_every_required_binding_before_callbacks():
    text = normalized(DOC)

    for reason in DENIAL_REASONS:
        assert reason in text
    assert "If any future owner comment appears after this proof, it is not retroactive to this #212 attempt" in text
    assert "A copied, stale, broadened, expired, mismatched, or non-owner comment remains `DENY_BEFORE_READ`" in text


def test_l6x02_synthetic_zero_counters_and_no_allowed_route():
    text = normalized(DOC)

    for term in ZERO_COUNTER_TERMS:
        assert term in text
    assert "approval_result: `DENIED_BEFORE_CALLBACK`" in text
    assert "rollback_status: `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`" in text
    assert "operation_count_attempted: `0`" in text


def test_l6x02_preserves_holds_and_report_hygiene():
    text = normalized(DOC)

    for held in PRESERVED_HOLDS:
        assert held in text
    for unsafe in UNSAFE_MARKERS:
        assert unsafe in text
    forbidden_echoes = (
        "source://",
        "raw-secret-token",
        "operator-home-path",
        "platform-raw-id",
        "private-correlation-ref",
    )
    for marker in forbidden_echoes:
        assert marker not in text
