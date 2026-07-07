from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6y01-one-read-binding-target-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

REQUIRED_BINDING_FIELDS = (
    "bound_approval_issue_id: `#222`",
    "packet_issue_id: `#221`",
    "owner_actor_association: `OWNER`",
    "subject: `jeremyknows/memory-seam`",
    "audience: `L6Y supervised one-read attempt`",
    "scope: `one report-safe source-card read`",
    "operation_class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
    "max_operation_count: `1`",
    "expiry_window: `<=12h from #222 owner comment timestamp`",
    "descriptor_ref_shape: `descriptor:l6y/<report-safe-slug>`",
    "source_card_ref_shape: `source-card:l6y/<report-safe-slug>`",
)

PRESERVED_HOLDS = (
    "no live/private reads in #221",
    "no raw private content",
    "no credential/auth/env/keychain/OAuth/auth-file reads",
    "no source discovery, workspace scans, family scans, broad recall, or index queries",
    "no Runtime Registry consumption",
    "no provider/backend/source-stat/source-read callbacks in #221",
    "no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation",
    "no service/listener/startup/cron activation or global runtime config mutation",
    "no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement",
    "no broad `allowed=true` route",
)

DENIAL_SHAPES = (
    "absent approval comment on #222: `DENY_BEFORE_READ`",
    "copied packet text: `DENY_BEFORE_READ`",
    "stale approval outside expiry: `DENY_BEFORE_READ`",
    "mismatched issue id: `DENY_BEFORE_READ`",
    "broadened operation class: `DENY_BEFORE_READ`",
    "broadened operation count: `DENY_BEFORE_READ`",
    "expired approval: `DENY_BEFORE_READ`",
    "non-owner or missing owner actor association: `DENY_BEFORE_READ`",
    "unsafe or missing descriptor/source-card refs: `DENY_BEFORE_READ`",
)

FORBIDDEN_RAW_GRANT_MARKERS = (
    "I approve Memory Seam",
    "approval is granted",
    "live read is approved",
    "allowed=true route is present",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6y01_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6y01-one-read-binding-target-packet.md" in docs_index
    assert "tests/test_l6y01_one_read_binding_target_packet.py" in inventory
    assert "L6Y.01 preauthorized one-read binding and target packet" in inventory
    assert "BINDING_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION" in inventory


def test_l6y01_records_source_floor_and_preauth_anchors():
    text = normalized(DOC)

    required_terms = (
        "Status: `BINDING_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION`",
        "Rail issue: #221",
        "Bound approval/read issue: #222",
        "Parent issue: #6",
        "Source floor: `e0d5b4158049870b50aa5f553f828f891716be92`",
        "L6X #215 / PR #220 merged",
        "#6 comment `4649391691`",
        "#215 comment `4649391836`",
        "Jeremy voice-message anchor recorded in the parent L6Y rail receipt",
    )
    for term in required_terms:
        assert term in text


def test_l6y01_defines_exact_issue_bound_target_fields():
    text = normalized(DOC)

    for field in REQUIRED_BINDING_FIELDS:
        assert field in text
    assert "exactly one issue and max one report-safe source-card read" in text
    assert "#222 may proceed only from a fresh owner comment on #222" in text


def test_l6y01_non_approval_rejects_stale_mismatched_broadened_copied_expired():
    text = normalized(DOC)

    assert "This packet is not approval and cannot be copied or reused as approval" in text
    assert "Approval recognition must inspect only a fresh issue-bound owner comment on #222" in text
    assert "raw grant phrase required: `ABSENT_FROM_PACKET`" in text
    for shape in DENIAL_SHAPES:
        assert shape in text
    for marker in FORBIDDEN_RAW_GRANT_MARKERS:
        assert marker not in text


def test_l6y01_report_safe_metadata_shape_and_zero_counters():
    text = normalized(DOC)

    report_safe_terms = (
        "receipt_status",
        "approval_result",
        "live_read_invoked",
        "allowed",
        "allowed_result_count",
        "descriptor_ref",
        "source_card_ref",
        "operation_count_attempted",
        "read_usefulness_label",
        "redaction_status",
        "rollback_status",
        "guarded_counters",
        "unsafe_raw_fields_rejected_before_report",
        "`DENIED_BEFORE_CALLBACK`",
        "`NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`",
    )
    zero_counter_terms = (
        "approval_comments_examined: `0`",
        "valid_owner_approval_comments: `0`",
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
    for term in report_safe_terms + zero_counter_terms + unsafe_terms:
        assert term in text


def test_l6y01_preserves_all_holds_without_live_read_execution():
    text = normalized(DOC)

    for held in PRESERVED_HOLDS:
        assert held in text
    assert "No live/private read is executed by #221" in text
    assert "#222 must deny before read with guarded counters zero" in text
