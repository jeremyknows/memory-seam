from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ac01-fresh-owner-approved-source-card-read-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

TARGET_REF_PATTERN = re.compile(r"^(descriptor|source-card):l6ac/[a-z0-9]+(?:-[a-z0-9]+)*$")
EXACT_TARGET_REFS = {
    "descriptor_ref": "descriptor:l6ac/report-safe-operator-preference-card",
    "source_card_ref": "source-card:l6ac/report-safe-operator-preference-card",
}
REQUIRED_BINDING_FIELDS = (
    "packet_issue_id: `#261`",
    "bound_approval_read_issue_id: `#262`",
    "parent_issue_id: `#6`",
    "approval_comment_id_required: `4651509226`",
    "approval_comment_author_required: `jeremyknows`",
    "owner_actor_association: `OWNER`",
    "subject: `jeremyknows/memory-seam`",
    "audience: `L6AC owner-approved report-safe source-card read`",
    "scope: `one report-safe source-card read`",
    "operation_class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
    "max_operation_count: `1`",
    "expiry_window: `<=12h from #262 owner comment timestamp`",
    "descriptor_ref_shape: `descriptor:l6ac/<report-safe-slug>`",
    "source_card_ref_shape: `source-card:l6ac/<report-safe-slug>`",
    "exact_executable_descriptor_ref: `descriptor:l6ac/report-safe-operator-preference-card`",
    "exact_executable_source_card_ref: `source-card:l6ac/report-safe-operator-preference-card`",
    "source_floor_requirement: `67a1a78db2b7adca0048497cce61412de13032f1 or later`",
)
DENIAL_SHAPES = (
    "approval absent on #262: `DENY_BEFORE_READ`",
    "approval comment id is not `4651509226`: `DENY_BEFORE_READ`",
    "approval stale or outside <=12h expiry: `DENY_BEFORE_READ`",
    "copied approval text or copied packet text: `DENY_BEFORE_READ`",
    "broadened operation class or max-operation count: `DENY_BEFORE_READ`",
    "mismatched issue, subject, audience, scope, descriptor ref, or source-card ref: `DENY_BEFORE_READ`",
    "non-owner or missing owner actor association: `DENY_BEFORE_READ`",
    "unsafe target refs or raw/private target values: `DENY_BEFORE_READ`",
    "any request for discovery, workspace/family scan, broad recall, index query, credentials, Runtime Registry, persistence, activation, publication, provider/prod/canary/Gate movement, mutation, rollback, cache purge, or `allowed=true`: `DENY_BEFORE_READ`",
)
PRESERVED_HOLDS = (
    "no live/private reads in #261",
    "no raw private content",
    "no credential/auth/env/keychain/OAuth/auth-file reads",
    "no source discovery, workspace scans, family scans, broad recall, or index queries",
    "no Runtime Registry consumption",
    "no provider/backend/source-stat/source-read callbacks in #261",
    "no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation",
    "no service/listener/startup/cron activation or global runtime config mutation",
    "no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement",
    "no broad `allowed=true` route",
)
UNSAFE_TARGET_VALUES = (
    "descriptor:l6aa/report-safe-operator-preference-card",
    "source-card:l6aa/report-safe-operator-preference-card",
    "descriptor:l6ac/raw-private-source-text",
    "source-card:l6ac/private-path-source-uri",
    "source://operator/private/card",
    "operator-home-private-card-path",
    "platform-raw-id:12345",
    "raw prompt query payload",
    "credential token value",
    "oauth keychain auth-file material",
    "private-correlation-ref",
)
FORBIDDEN_APPROVAL_MARKERS = (
    "I approve Sax to execute",
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


def test_l6ac01_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ac01-fresh-owner-approved-source-card-read-packet.md" in docs_index
    assert "tests/test_l6ac01_fresh_owner_approved_source_card_read_packet.py" in inventory
    assert "L6AC.01 fresh owner-approved source-card read packet" in inventory
    assert "FRESH_OWNER_APPROVED_PACKET_ONLY_NO_LIVE_READS" in inventory


def test_l6ac01_records_source_floor_and_owner_approval_anchors():
    text = normalized(DOC)

    required_terms = (
        "Status: `FRESH_OWNER_APPROVED_PACKET_ONLY_NO_LIVE_READS`",
        "Rail issue: #261",
        "Bound approval/read issue: #262",
        "Parent issue: #6",
        "Source floor: `67a1a78db2b7adca0048497cce61412de13032f1`",
        "Parent successor comment: `issuecomment-4651509390`",
        "Issue-bound prep comment: `issuecomment-4651509094`",
        "Exact max-one read approval comment: `issuecomment-4651509226`",
        "Approval comment author: `jeremyknows` / `OWNER`",
    )
    for term in required_terms:
        assert term in text


def test_l6ac01_defines_exact_executable_descriptor_and_source_card_refs():
    text = normalized(DOC)

    for field in REQUIRED_BINDING_FIELDS:
        assert field in text
    assert "matching exact executable descriptor/source-card target refs" in text
    assert "#262 may proceed only from approval comment `4651509226` on #262" in text
    assert target_refs_are_exact_and_report_safe(EXACT_TARGET_REFS)


def test_l6ac01_rejects_unsafe_or_stale_target_values():
    for unsafe_value in UNSAFE_TARGET_VALUES:
        assert not target_refs_are_exact_and_report_safe(
            {"descriptor_ref": unsafe_value, "source_card_ref": EXACT_TARGET_REFS["source_card_ref"]}
        )
        assert not target_refs_are_exact_and_report_safe(
            {"descriptor_ref": EXACT_TARGET_REFS["descriptor_ref"], "source_card_ref": unsafe_value}
        )


def test_l6ac01_denial_matrix_and_non_approval_boundary():
    text = normalized(DOC)

    assert "This packet is not itself the live-read execution" in text
    assert "This packet cannot be copied, broadened, moved to another issue, or reused after expiry" in text
    assert "Approval recognition must inspect public issue-comment metadata only; it must not echo raw approval text" in text
    for shape in DENIAL_SHAPES:
        assert shape in text
    for marker in FORBIDDEN_APPROVAL_MARKERS:
        assert marker not in text


def test_l6ac01_report_safe_metadata_and_zero_counter_shape():
    text = normalized(DOC)

    terms = (
        "receipt_status",
        "approval_result",
        "live_read_invoked",
        "allowed",
        "allowed_result_count",
        "operation_count_attempted",
        "descriptor_ref",
        "source_card_ref",
        "read_usefulness_label",
        "redaction_status",
        "guarded_counters",
        "unsafe_raw_fields_rejected_before_report",
        "approval_comments_examined: `0` in #261",
        "valid_owner_approval_comments: `0` in #261",
        "provider_callbacks: `0` in #261",
        "backend_callbacks: `0` in #261",
        "source_stat_callbacks: `0` in #261",
        "source_read_callbacks: `0` in #261",
        "credential_reads: `0` in #261",
        "runtime_registry_reads: `0` in #261",
        "persistence_writes: `0` in #261",
        "mutation_callbacks: `0` in #261",
        "rollback_callbacks: `0` in #261",
        "cache_purge_callbacks: `0` in #261",
    )
    for term in terms:
        assert term in text


def test_l6ac01_preserves_holds_without_live_read_execution():
    text = normalized(DOC)

    for held in PRESERVED_HOLDS:
        assert held in text
    assert "No live/private read is executed by #261" in text
    assert "#262 must deny before read unless every bound approval and executable-ref field matches" in text
