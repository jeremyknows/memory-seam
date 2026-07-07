from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6w01-supervised-live-read-approval-packet-scaffold.md"
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
    "source://",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6w01_scaffold_is_non_approval_and_no_execution():
    text = normalized(DOC)

    required_terms = [
        "L6W.01 supervised live-read approval packet scaffold",
        "Status: `HITL_SCAFFOLD_ONLY_NO_APPROVAL_NO_EXECUTION`",
        "Rail issue: #199",
        "Source floor: `9264533` or later on `origin/main`",
        "Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`",
        "docs/tests-only HITL scaffold",
        "It is not approval, not execution, not implementation",
        "not a merge-triggered grant",
        "not authority for any current or future agent to perform a live/private read from this file alone",
        "does not include approval wording that can be treated as already granted",
        "`NO_APPROVAL_PRESENT`",
    ]
    for term in required_terms:
        assert term in text


def test_l6w01_binds_required_future_approval_fields_without_granting_them():
    text = normalized(DOC)

    required_bindings = [
        "`approval_issue_ref`",
        "the fresh future approval issue number, not #199 and not any prior issue",
        "`approval_author_association`",
        "`OWNER`",
        "`approval_owner_ref`",
        "`repo-owner:jeremyknows`",
        "`approval_subject_ref`",
        "one report-safe Memory Seam source-card descriptor subject chosen in the future issue",
        "`approval_audience`",
        "Memory Seam supervised live-read approval only",
        "`approval_scope`",
        "one report-safe source-card descriptor read only",
        "`operation_class`",
        "`SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
        "`max_operation_count`",
        "exactly `1`",
        "`approval_created_at`",
        "`approval_expires_at`",
        "no later than 12 hours after `approval_created_at`",
        "`report_safe_output_shape`",
        "safe refs, booleans, zero/non-zero counters, status strings, and usefulness classification only",
        "`zero_discovery_expectation`",
        "no source discovery, workspace scans, family scans, broad recall, or index queries",
        "`denial_before_callback`",
        "deny before provider/backend/source-stat/source-read callbacks",
        "`stop_conditions`",
        "`rollback_behavior`",
        "no rollback callback; stop, emit report-safe denial/held receipt metadata only",
    ]
    for term in required_bindings:
        assert term in text

    assert "must not broaden these requirements" in text
    assert "separate future issue-bound owner approval" in text


def test_l6w01_rejects_implied_or_broadened_approval_sources():
    text = normalized(DOC)

    non_approval_terms = [
        "this document being merged",
        "issue #199 closing",
        "labels, milestones, branch names, PR titles, or PR bodies",
        "stale comments from earlier L5/L6/L6U/L6V rails",
        "copied approval text from another issue",
        "comments by non-owner actors",
        "comments that omit any required binding field",
        "comments that broaden operation count, scope, source access, discovery, callback, persistence, activation, production, publication, visibility, provider/prod/canary, Atlas Gate, mutation, or `allowed=true` authority",
    ]
    for term in non_approval_terms:
        assert term in text


def test_l6w01_preserves_hard_holds_and_report_safety():
    text = normalized(DOC)

    held_terms = [
        "live/private reads until a separate future issue-bound owner approval and later approved implementation recognition exist",
        "raw source content and raw private text",
        "source discovery, workspace scans, family scans, broad recall, and index queries",
        "source-stat/source-read/provider/backend callbacks",
        "credentials, auth files, environment secrets, keychain entries, OAuth material, and auth-file reads",
        "Runtime Registry consumption",
        "write/custody/delete/reindex/rollback/cache-purge callbacks and all mutation execution",
        "persistence, audit/custody record writes, and cache mutation",
        "service/listener/startup/cron activation and global Hermes/MCP/client/runtime configuration mutation",
        "package publication, repository visibility changes, provider/prod/canary or production authority, and Atlas Gate movement",
        "any `allowed=true` route",
    ]
    for term in held_terms:
        assert term in text

    report_safe_terms = [
        "public issue/PR numbers and repository file names",
        "operation-class names and schema/status strings",
        "booleans and numeric counters",
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
    ]
    for term in report_safe_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6w01_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6w01-supervised-live-read-approval-packet-scaffold.md" in docs_index
    assert "tests/test_l6w01_supervised_live_read_approval_packet_scaffold.py" in inventory
    assert "L6W.01 supervised live-read approval packet scaffold" in inventory
    assert "HITL_SCAFFOLD_ONLY_NO_APPROVAL_NO_EXECUTION" in inventory
