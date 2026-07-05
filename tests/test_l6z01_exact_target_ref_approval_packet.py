from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6z01-exact-target-ref-approval-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

TARGET_REF_PATTERN = re.compile(r"^(descriptor|source-card):l6z/[a-z0-9]+(?:-[a-z0-9]+)*$")
EXACT_TARGET_REFS = {
    "descriptor_ref": "descriptor:l6z/report-safe-operator-preference-card",
    "source_card_ref": "source-card:l6z/report-safe-operator-preference-card",
}
UNSAFE_TARGET_VALUES = (
    "descriptor:l6y/report-safe-operator-preference-card",
    "source-card:l6z/other-card",
    "descriptor:l6z/raw-private-source-text",
    "source-card:l6z/private-path-source-uri",
    "source://operator/private/card",
    "operator-home-private-card-path",
    "platform-raw-id:12345",
    "raw prompt query payload",
    "credential token value",
    "oauth keychain auth-file material",
    "private-correlation-ref",
)

REQUIRED_BINDING_FIELDS = (
    "bound_approval_issue_id: `#232`",
    "packet_issue_id: `#231`",
    "owner_actor_association: `OWNER`",
    "subject: `jeremyknows/memory-seam`",
    "audience: `L6Z exact target-ref one-read retry`",
    "scope: `one report-safe source-card read`",
    "operation_class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
    "max_operation_count: `1`",
    "expiry_window: `<=12h from #232 owner comment timestamp`",
    "descriptor_ref_shape: `descriptor:l6z/<report-safe-slug>`",
    "source_card_ref_shape: `source-card:l6z/<report-safe-slug>`",
    "exact_executable_descriptor_ref: `descriptor:l6z/report-safe-operator-preference-card`",
    "exact_executable_source_card_ref: `source-card:l6z/report-safe-operator-preference-card`",
    "source_floor_requirement: `c7e335bf6b68e084088c6deaa4b28dd84f9ed9f6 or later`",
)

PRESERVED_HOLDS = (
    "no live/private reads in #231",
    "no raw private content",
    "no credential/auth/env/keychain/OAuth/auth-file reads",
    "no source discovery, workspace scans, family scans, broad recall, or index queries",
    "no Runtime Registry consumption",
    "no provider/backend/source-stat/source-read callbacks in #231",
    "no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation",
    "no service/listener/startup/cron activation or global runtime config mutation",
    "no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement",
    "no broad `allowed=true` route",
)

DENIAL_SHAPES = (
    "absent approval comment on #232: `DENY_BEFORE_READ`",
    "copied packet text: `DENY_BEFORE_READ`",
    "stale approval outside expiry: `DENY_BEFORE_READ`",
    "mismatched issue id: `DENY_BEFORE_READ`",
    "broadened operation class: `DENY_BEFORE_READ`",
    "broadened operation count: `DENY_BEFORE_READ`",
    "expired approval: `DENY_BEFORE_READ`",
    "non-owner or missing owner actor association: `DENY_BEFORE_READ`",
    "unsafe or missing descriptor/source-card refs: `DENY_BEFORE_READ`",
    "mismatched executable descriptor/source-card refs: `DENY_BEFORE_READ`",
)

FORBIDDEN_RAW_GRANT_MARKERS = (
    "I approve Memory Seam",
    "approval is granted",
    "live read is approved",
    "allowed=true route is present",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def target_refs_are_exact_and_report_safe(refs: dict[str, str]) -> bool:
    descriptor_ref = refs.get("descriptor_ref")
    source_card_ref = refs.get("source_card_ref")
    return (
        refs == EXACT_TARGET_REFS
        and isinstance(descriptor_ref, str)
        and isinstance(source_card_ref, str)
        and bool(TARGET_REF_PATTERN.fullmatch(descriptor_ref))
        and bool(TARGET_REF_PATTERN.fullmatch(source_card_ref))
        and descriptor_ref.removeprefix("descriptor:")
        == source_card_ref.removeprefix("source-card:")
    )


def test_l6z01_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6z01-exact-target-ref-approval-packet.md" in docs_index
    assert "tests/test_l6z01_exact_target_ref_approval_packet.py" in inventory
    assert "L6Z.01 exact target-ref approval packet and executable ref fixtures" in inventory
    assert "TARGET_REF_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION" in inventory


def test_l6z01_records_source_floor_and_preauth_anchors():
    text = normalized(DOC)

    required_terms = (
        "Status: `TARGET_REF_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION`",
        "Rail issue: #231",
        "Bound approval/read issue: #232",
        "Parent issue: #6",
        "Source floor: `c7e335bf6b68e084088c6deaa4b28dd84f9ed9f6`",
        "L6Y #225 / PR #230 merged",
        "#6 comment `4649391691`",
        "#215 comment `4649391836`",
        "Jeremy voice-message anchor recorded for the bounded L6Z rail",
        "issuecomment-4650001541",
    )
    for term in required_terms:
        assert term in text


def test_l6z01_defines_exact_issue_bound_executable_target_refs():
    text = normalized(DOC)

    for field in REQUIRED_BINDING_FIELDS:
        assert field in text
    assert "exactly one issue and max one report-safe source-card read" in text
    assert "#232 may proceed only from a fresh owner comment on #232" in text
    assert target_refs_are_exact_and_report_safe(EXACT_TARGET_REFS)


def test_l6z01_fixture_rejects_unsafe_raw_private_target_values():
    for field, exact_ref in EXACT_TARGET_REFS.items():
        assert TARGET_REF_PATTERN.fullmatch(exact_ref), field
    for unsafe_value in UNSAFE_TARGET_VALUES:
        assert not target_refs_are_exact_and_report_safe(
            {
                "descriptor_ref": unsafe_value,
                "source_card_ref": EXACT_TARGET_REFS["source_card_ref"],
            }
        )
        assert not target_refs_are_exact_and_report_safe(
            {
                "descriptor_ref": EXACT_TARGET_REFS["descriptor_ref"],
                "source_card_ref": unsafe_value,
            }
        )


def test_l6z01_non_approval_rejects_stale_mismatched_broadened_copied_expired():
    text = normalized(DOC)

    assert "This packet is not approval and cannot be copied or reused as approval" in text
    assert "Approval recognition for #232 must inspect only a fresh issue-bound owner comment on #232" in text
    assert "raw grant phrase required: `ABSENT_FROM_PACKET`" in text
    for shape in DENIAL_SHAPES:
        assert shape in text
    for marker in FORBIDDEN_RAW_GRANT_MARKERS:
        assert marker not in text


def test_l6z01_report_safe_metadata_shape_and_zero_counters():
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


def test_l6z01_preserves_all_holds_without_live_read_execution():
    text = normalized(DOC)

    for held in PRESERVED_HOLDS:
        assert held in text
    assert "No live/private read is executed by #231" in text
    assert "#232 must deny before read with guarded counters zero" in text
