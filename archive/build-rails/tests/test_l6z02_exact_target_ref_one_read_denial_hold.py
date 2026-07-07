from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6z02-exact-target-ref-one-read-denial-hold.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

EXPECTED_REFS = {
    "descriptor_ref": "descriptor:l6z/report-safe-operator-preference-card",
    "source_card_ref": "source-card:l6z/report-safe-operator-preference-card",
}
PRESENTED_REFS = {
    "descriptor_ref": "descriptor:l6z/operator-proof",
    "source_card_ref": "source-card:l6z/operator-proof",
}

ZERO_COUNTER_TERMS = (
    "live_read_invocations: `0`",
    "operation_count_attempted: `0`",
    "allowed_result_count: `0`",
    "provider_callbacks: `0`",
    "backend_callbacks: `0`",
    "source_stat_callbacks: `0`",
    "source_read_callbacks: `0`",
    "credential_reads: `0`",
    "auth_env_keychain_oauth_auth_file_reads: `0`",
    "runtime_registry_reads: `0`",
    "source_discovery_queries: `0`",
    "workspace_scans: `0`",
    "family_scans: `0`",
    "broad_recall_queries: `0`",
    "index_queries: `0`",
    "persistence_writes: `0`",
    "mutation_callbacks: `0`",
    "rollback_callbacks: `0`",
    "cache_purge_callbacks: `0`",
    "service_listener_startup_activations: `0`",
    "publication_or_visibility_changes: `0`",
    "provider_prod_canary_or_gate_moves: `0`",
)

FORBIDDEN_REPORT_MARKERS = (
    "raw private source text:",
    "credential value:",
    "oauth token:",
    "auth-file path:",
    "private absolute path:",
    "raw backend response:",
    "raw approval text:",
    "allowed: true",
    "live_read_invoked: true",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6z02_hold_receipt_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6z02-exact-target-ref-one-read-denial-hold.md" in docs_index
    assert "tests/test_l6z02_exact_target_ref_one_read_denial_hold.py" in inventory
    assert "L6Z.02 exact target-ref one-read retry denial HOLD" in inventory
    assert "HOLD_DENIED_BEFORE_READ_APPROVAL_TARGET_REF_MISMATCH_NO_LIVE" in inventory


def test_l6z02_records_source_floor_and_prerequisite_binding():
    text = normalized(DOC)

    required_terms = (
        "Status: `HOLD_DENIED_BEFORE_READ_APPROVAL_TARGET_REF_MISMATCH_NO_LIVE`",
        "Rail issue: #232",
        "Prerequisite packet issue: #231",
        "Parent issue: #6",
        "Source floor requirement: `c7e335bf6b68e084088c6deaa4b28dd84f9ed9f6 or later`",
        "Evaluated source floor: `07ef81810809a0249fef2fd58be99cc57bce1746`",
        "Prerequisite packet: `docs/l6z01-exact-target-ref-approval-packet.md`",
        "#6 comment `4649391691`",
        "#215 comment `4649391836`",
        "issuecomment-4650001541",
    )
    for term in required_terms:
        assert term in text


def test_l6z02_denies_before_read_on_target_ref_mismatch():
    text = normalized(DOC)

    for ref in EXPECTED_REFS.values():
        assert ref in text
    for ref in PRESENTED_REFS.values():
        assert ref in text
    mismatch_terms = (
        "The approval comment was present and owner-bound, but it did not match the #231 executable target refs",
        "No updated #232 owner comment matching `descriptor:l6z/report-safe-operator-preference-card` and `source-card:l6z/report-safe-operator-preference-card` was present",
        "MISMATCH_DENY_BEFORE_READ",
        "mismatch_reason: EXECUTABLE_TARGET_REFS_DO_NOT_MATCH_L6Z01_PACKET",
        "Approval result: `DENY_BEFORE_READ`",
        "Stop condition: `DENIED_BEFORE_CALLBACK`",
    )
    for term in mismatch_terms:
        assert term in text


def test_l6z02_records_owner_comment_metadata_without_raw_approval_echo():
    text = normalized(DOC)

    safe_metadata_terms = (
        "issue comment `4649997717`",
        "authored by `jeremyknows`",
        "owner_actor_association: OWNER",
        "created at `2026-06-08T14:25:56Z`",
        "approval_evaluated_at: 2026-06-08T14:39:48Z",
        "freshness_result: FRESH_WITHIN_12H",
        "REPORT_SAFE_METADATA_ONLY_RAW_APPROVAL_TEXT_OMITTED",
    )
    for term in safe_metadata_terms:
        assert term in text

    assert "This receipt intentionally omits raw approval text" in text
    assert "I approve exactly one supervised" not in DOC.read_text(encoding="utf-8")


def test_l6z02_hold_receipt_zeroes_guarded_counters_and_no_live_read():
    text = normalized(DOC)

    receipt_terms = (
        "live_read_invoked: false",
        "allowed: false",
        "allowed_result_count: 0",
        "operation_count_attempted: 0",
        "Live read invoked: `false`",
        "Allowed: `false`",
        "Allowed result count: `0`",
        "Operation count attempted: `0`",
        "Rollback status: `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`",
    )
    for term in receipt_terms + ZERO_COUNTER_TERMS:
        assert term in text


def test_l6z02_preserves_holds_and_rejects_unsafe_report_fields():
    text = normalized(DOC)

    preserved_holds = (
        "no live/private read executed in #232",
        "no raw private content read or reported",
        "no credential/auth/env/keychain/OAuth/auth-file reads",
        "no source discovery, workspace scans, family scans, broad recall, or index queries",
        "no Runtime Registry consumption",
        "no provider/backend/source-stat/source-read callbacks",
        "no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation",
        "no service/listener/startup/cron activation or global runtime config mutation",
        "no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement",
        "no broad `allowed=true` route",
    )
    unsafe_terms = (
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
    for term in preserved_holds + unsafe_terms:
        assert term in text
    for marker in FORBIDDEN_REPORT_MARKERS:
        assert marker not in DOC.read_text(encoding="utf-8")


def test_l6z02_handoff_to_verifier_allows_no_additional_read():
    text = normalized(DOC)

    assert "#233 may verify this already-produced HOLD receipt and redaction posture" in text
    assert "#233 must not perform an additional live/private read" in text
