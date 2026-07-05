from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6u02-supervised-live-read-approval-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF"

NON_APPROVAL_SIGNALS = (
    "this packet text or tests",
    "PR merge events",
    "issue labels or project fields",
    "stale comments",
    "issue closure",
    "unrelated approvals",
)

DENIAL_CASES = (
    "stale_approval",
    "variant_approval",
    "copied_approval",
    "mismatched_approval",
    "broadened_approval",
    "callback_requesting_approval",
    "activation_requesting_approval",
    "publication_requesting_approval",
    "provider_prod_canary_approval",
    "atlas_gate_approval",
)

REQUIRED_APPROVAL_FIELDS = (
    "approval_packet_ref",
    "issue_ref",
    "operation_class",
    "max_operation_count",
    "actor_ref",
    "subject_ref",
    "owner_ref",
    "audience",
    "scope",
    "approval_ref",
    "approval_timestamp_ref",
    "expires_at_ref",
    "stop_conditions_ref",
    "rollback_expectation_ref",
    "audit_expectation_ref",
    "public_hygiene_ref",
)

FORBIDDEN_HELD_SURFACES = (
    "no implementation or execution of live/private reads",
    "no credentials, auth, env, keychain, OAuth, or auth-file reads",
    "no source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, or Runtime Registry consumption",
    "no provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
    "no mutation execution, no `allowed=true` path",
    "no persistence/audit/custody records",
    "no cache mutation",
    "no service/listener/startup/cron activation",
    "global Hermes/MCP/client/runtime config mutation",
    "package publication",
    "repository visibility change",
    "provider/prod/canary authority",
    "production authority",
    "Atlas Gate movement",
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


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6u02_approval_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6u02-supervised-live-read-approval-packet.md" in docs_index
    assert "tests/test_l6u02_supervised_live_read_approval_packet.py" in inventory
    assert "L6U.02 supervised live-read approval packet" in inventory
    assert OPERATION_CLASS in inventory


def test_l6u02_is_hitl_only_future_only_and_not_approval():
    text = normalized(DOC)

    required_terms = [
        "Status: `HITL_ONLY_FUTURE_APPROVAL_PACKET_NOT_APPROVAL`",
        "future human-in-the-loop approval requirements",
        "The packet itself is not approval",
        "does not recognize approval",
        "does not implement or execute any live/private read",
        "documentation and contract-test evidence only",
        "must not treat this packet, a merge event, label, issue closure, stale comment, unrelated approval, or copied text as approval",
    ]
    for term in required_terms:
        assert term in text

    for signal in NON_APPROVAL_SIGNALS:
        assert signal in text


def test_l6u02_names_exactly_one_future_operation_class_and_max_one_operation():
    text = normalized(DOC)

    assert f"Future operation class: `{OPERATION_CLASS}`." in text
    assert text.count("Future operation class:") == 1
    assert "exactly one supervised read-side operation class" in text
    assert "max-one-operation limit: `max_operation_count=1`" in text
    assert "`max_operation_count`: `1`" in text
    assert "`max_operation_count=1`" in text
    assert "more than one attempted operation" in text


def test_l6u02_requires_exact_issue_actor_subject_owner_expiry_and_hygiene_binding():
    text = normalized(DOC)

    for field in REQUIRED_APPROVAL_FIELDS:
        assert f"`{field}`" in text

    required_binding_terms = [
        "exact, fresh, issue-bound, actor/subject/owner-bound, unexpired, max-one-operation",
        "scoped to the single operation class above",
        "`actor_ref`: report-safe operator actor reference",
        "`subject_ref`: report-safe caller subject reference",
        "`owner_ref`: report-safe source owner / acting-for reference",
        "`expires_at_ref`: report-safe expiry reference",
        "`public_hygiene_ref`: `l6u02.public.hygiene.v1`",
    ]
    for term in required_binding_terms:
        assert term in text


def test_l6u02_denies_stale_variant_copied_mismatched_broadened_and_callback_requests_before_callbacks():
    text = normalized(DOC)

    for case in DENIAL_CASES:
        assert f"`{case}`" in text

    assert text.count("`DENIED_BEFORE_CALLBACK`") >= len(DENIAL_CASES)
    assert "denied before callbacks" in text
    assert "Any missing, mismatched, broadened, copied, stale, variant, callback-requesting, activation-requesting, publication-requesting, provider/prod/canary, or Atlas Gate-moving approval text is denied before callbacks" in text
    assert "provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks were requested" in text
    assert "service/listener/startup/cron activation or global Hermes/MCP/client/runtime config mutation was requested" in text
    assert "package publication or repository visibility change was requested" in text
    assert "provider/prod/canary authority or production authority was requested" in text
    assert "Atlas Gate movement was requested" in text


def test_l6u02_report_safe_receipt_fields_exclude_private_content():
    text = normalized(DOC)

    report_fields = [
        "issue_ref",
        "operation_class",
        "operation_attempt_count",
        "actor_ref",
        "subject_ref",
        "owner_ref",
        "approval_ref",
        "expires_at_ref",
        "stop_reason_ref",
        "rollback_expectation_ref",
        "audit_expectation_ref",
        "public_hygiene_result",
        "guarded_callback_counters",
    ]
    for field in report_fields:
        assert f"`{field}`" in text

    assert "excludes raw source content, source path, source URI, credential material, raw platform identifiers, raw query/payload content, private correlation references, backend response bodies, Runtime Registry data, persistence record bodies, and audit/custody record bodies" in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6u02_preserves_no_live_no_callback_no_production_holds():
    text = normalized(DOC)

    for surface in FORBIDDEN_HELD_SURFACES:
        assert surface in text

    assert "no source discovery" in text
    assert "no Runtime Registry consumption" in text
    assert "no `allowed=true` path" in text
    assert "no persistence/audit/custody records" in text
    assert "no service/listener/startup/cron activation" in text


def test_l6u02_rolls_audit_and_public_hygiene_forward_without_persistence():
    text = normalized(DOC)

    required_terms = [
        "Rollback expectation: because this packet authorizes no execution",
        "no mutation rollback",
        "write/custody/delete/reindex/rollback/cache-purge behavior as unsupported",
        "this packet creates no persistence/audit/custody records and no cache mutation",
        "A later issue must define any audit receipt separately before implementation",
        "all artifacts must pass `python scripts/public_hygiene_scan.py`",
        "must not include secrets, credentials, private paths, raw document content, raw prompt/query text, live source identifiers, OAuth/keychain/env material, Runtime Registry references, raw backend responses, or private correlation references",
    ]
    for term in required_terms:
        assert term in text
