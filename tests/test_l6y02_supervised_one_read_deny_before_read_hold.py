from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6y02-supervised-one-read-deny-before-read-hold.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

BINDING_TERMS = (
    "Status: `HOLD_DENIED_BEFORE_READ_APPROVAL_MISMATCH_NO_LIVE`",
    "Rail issue: #222",
    "Binding packet issue: #221",
    "Parent issue: #6",
    "Source floor checked: `b268ce0a064629c823a14d3f68563607a14019b4`",
    "Approval comment inspected: #222 comment `4649485027`",
    "author association `OWNER`",
    "inspected within the `<=12h` freshness window",
    "Approval packet dependency: `docs/l6y01-one-read-binding-target-packet.md`",
)

DENIAL_TERMS = (
    "Exact approval result: `PRESENT_BUT_NOT_EXECUTABLE`",
    "Decision: `DENY_BEFORE_READ`",
    "Live read result: `NOT_ATTEMPTED`",
    "Receipt status: `HOLD`",
    "Approval result: `DENIED_BEFORE_CALLBACK`",
    "missing executable descriptor ref: `DENY_BEFORE_READ`",
    "missing executable source-card ref: `DENY_BEFORE_READ`",
    "MISSING_EXECUTABLE_REF_DENY_BEFORE_READ",
    "MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ",
)

ZERO_GUARDED_COUNTER_TERMS = (
    "`provider_callbacks` | `0`",
    "`backend_callbacks` | `0`",
    "`source_stat_callbacks` | `0`",
    "`source_read_callbacks` | `0`",
    "`credential_reads` | `0`",
    "`runtime_registry_reads` | `0`",
    "`persistence_writes` | `0`",
    "`mutation_callbacks` | `0`",
    "`rollback_callbacks` | `0`",
    "`cache_purge_callbacks` | `0`",
)

RECEIPT_TERMS = (
    "`approval_comments_examined` | `1`",
    "`valid_owner_approval_comments` | `0`",
    "`live_read_invoked` | `false`",
    "`allowed` | `false`",
    "`allowed_result_count` | `0`",
    "`operation_count_attempted` | `0`",
    "`read_usefulness_label` | `NOT_EVALUATED_NO_READ`",
    "`redaction_status` | `REPORT_SAFE_METADATA_ONLY`",
    "`rollback_status` | `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`",
    "`unsafe_raw_fields_rejected_before_report` | `true`",
)

PRESERVED_HOLDS = (
    "no live/private reads in #222",
    "no raw private content",
    "no credential/auth/env/keychain/OAuth/auth-file reads",
    "no source discovery, workspace scans, family scans, broad recall, or index queries",
    "no Runtime Registry consumption",
    "no provider/backend/source-stat/source-read callbacks in #222",
    "no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation",
    "no service/listener/startup/cron activation or global runtime config mutation",
    "no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement",
    "no broad `allowed=true` route",
)

UNSAFE_TERMS = (
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

FORBIDDEN_ECHOES = (
    "source://",
    "raw-secret-token",
    "operator-home-path",
    "platform-raw-id",
    "private-correlation-ref",
    "I approve exactly one supervised report-safe source-card read",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6y02_hold_receipt_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6y02-supervised-one-read-deny-before-read-hold.md" in docs_index
    assert "tests/test_l6y02_supervised_one_read_deny_before_read_hold.py" in inventory
    assert "L6Y.02 supervised one-read approval mismatch HOLD" in inventory
    assert "HOLD_DENIED_BEFORE_READ_APPROVAL_MISMATCH_NO_LIVE" in inventory


def test_l6y02_records_owner_comment_check_and_binding_context():
    text = normalized(DOC)

    for term in BINDING_TERMS:
        assert term in text
    assert "#6 comment `4649391691`" in text
    assert "#215 comment `4649391836`" in text
    assert "Jeremy voice-message anchor recorded in the parent L6Y rail receipt" in text


def test_l6y02_denies_before_read_because_executable_refs_are_missing():
    text = normalized(DOC)

    for term in DENIAL_TERMS:
        assert term in text
    assert "No supervised report-safe source-card live read was executed" in text
    assert "No raw private content was requested, copied, summarized, inspected, or reported" in text
    assert "#223 may verify this HOLD receipt without performing any additional live/private read" in text


def test_l6y02_receipt_has_zero_live_source_callback_and_guarded_counters():
    text = normalized(DOC)

    for term in RECEIPT_TERMS + ZERO_GUARDED_COUNTER_TERMS:
        assert term in text
    assert "`descriptor_ref` | `MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ`" in text
    assert "`source_card_ref` | `MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ`" in text


def test_l6y02_preserves_holds_and_public_hygiene():
    text = normalized(DOC)

    for held in PRESERVED_HOLDS:
        assert held in text
    for unsafe in UNSAFE_TERMS:
        assert unsafe in text
    for marker in FORBIDDEN_ECHOES:
        assert marker not in text
