from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6x01-one-read-approval-request-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

REQUIRED_BINDING_FIELDS = (
    "bound_issue_id: `#212`",
    "owner_actor_association: `OWNER`",
    "subject: `jeremyknows/memory-seam`",
    "audience: `L6X supervised one-read attempt`",
    "operation_class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
    "max_operation_count: `1`",
    "expiry_window: `<=12h from owner comment timestamp`",
    "descriptor_ref_shape: `descriptor:l6x/<report-safe-slug>`",
    "source_card_ref_shape: `source-card:l6x/<report-safe-slug>`",
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
    "no `allowed=true` route",
)

FORBIDDEN_RAW_GRANT_MARKERS = (
    "I approve Memory Seam",
    "approval is granted",
    "allowed=true route is present",
    "live read is approved",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6x01_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6x01-one-read-approval-request-packet.md" in docs_index
    assert "tests/test_l6x01_one_read_approval_request_packet.py" in inventory
    assert "L6X.01 exact one-read approval request packet" in inventory
    assert "REQUEST_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION" in inventory


def test_l6x01_defines_exact_future_binding_fields():
    text = normalized(DOC)

    assert "Status: `REQUEST_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION`" in text
    assert "Rail issue: #211" in text
    assert "Bound future attempt issue: #212" in text
    assert "Parent issue: #6" in text
    assert "Source floor: `1a6d20e4ca10acb03dc9ffd8a4b678c950b8c41b`" in text
    for field in REQUIRED_BINDING_FIELDS:
        assert field in text


def test_l6x01_packet_is_non_approval_and_not_copyable_or_staleable():
    text = normalized(DOC)

    non_approval_terms = (
        "This packet is a request template only; it is not an owner approval comment",
        "No text in this file can be copied, merged, labeled, closed, or reused as approval",
        "Approval recognition must read only a fresh owner comment on #212",
        "copied packet text: `DENY_BEFORE_READ`",
        "stale comment outside expiry: `DENY_BEFORE_READ`",
        "mismatched issue id: `DENY_BEFORE_READ`",
        "broadened operation class or count: `DENY_BEFORE_READ`",
        "missing owner actor association: `DENY_BEFORE_READ`",
        "raw grant phrase required: `ABSENT_FROM_PACKET`",
    )
    for term in non_approval_terms:
        assert term in text
    for marker in FORBIDDEN_RAW_GRANT_MARKERS:
        assert marker not in text


def test_l6x01_receipt_and_denial_before_callback_fields_are_report_safe():
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
        "rollback_status",
        "guarded_counters",
        "unsafe_raw_fields_rejected_before_report",
        "`DENIED_BEFORE_CALLBACK`",
        "`NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`",
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
    for term in report_safe_terms + unsafe_terms:
        assert term in text


def test_l6x01_preserves_all_holds_and_zero_counter_preflight():
    text = normalized(DOC)

    for held in PRESERVED_HOLDS:
        assert held in text
    zero_counter_terms = (
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
    for term in zero_counter_terms:
        assert term in text
