from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6af03-runtime-use-smoke-value-receipt-held-surface-map.md"
SMOKE_DOC = REPO_ROOT / "docs" / "l6af02-fixture-only-default-off-adapter-runtime-use-smoke.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_VALUE_RECEIPT_HELD_SURFACE_MAP_FIXTURE_ONLY_RUNTIME_USE_SMOKE"
VERDICT = "PASS_VALUE_RECEIPT_HELD_SURFACE_MAP"
NEXT_FRONTIER = "NO_LIVE_TRUST_BOUNDARY_REVIEW_ALLOWED_FOR_ISSUE_294_ONLY"
RAIL_STARTING_SOURCE_FLOOR = "f321708b1e8f708345194fc34c0d0968c620c03e"
SOURCE_FLOOR_ENTERING_SLICE = "d995a5ac2c9dca2e571d8eb5fdb1009482031f06"
APPROVAL_PACKET_SOURCE_FLOOR = "daf68ecd9e7cc55690bc70fdbbaf2d3707abd1f6"
SMOKE_SOURCE_FLOOR = "d995a5ac2c9dca2e571d8eb5fdb1009482031f06"
PREP_AUTH_COMMENT = "4653350694"
RUNTIME_USE_APPROVAL_COMMENT = "4653350823"
OPERATION_CLASS = "L6AF_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE"

VALUE_RECEIPT_TERMS = (
    "smoke status | `PASS_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE`",
    "missing approval status | `DENIED_DEFAULT_OFF`",
    "missing approval result | `DENY_BEFORE_ADAPTER_ACTION`",
    "missing approval reason | `MISSING_REQUIRED_APPROVAL_FIELDS`",
    "exact fixture positive status | `PASS_REPORT_SAFE_VALUE_ADAPTER_FIXTURE_ONLY`",
    "exact fixture positive result | `EXACT_ISSUE_BOUND_OWNER_APPROVAL_MATCH_FIXTURE_ONLY`",
    "allowed label | `EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER`",
    "broad `allowed=true` | `false`",
    "exact fixture allowed result count | `1`",
    "missing approval allowed result count | `0`",
    "guarded counters | all zero",
    "live/private reads invoked | `false`",
    "Runtime Registry consumed | `false`",
    "callbacks invoked | `false`",
    "persistence or mutation invoked | `false`",
    "service/listener/startup/global activation invoked | `false`",
    "Atlas Gate movement invoked | `false`",
)

HELD_SURFACES = (
    "Additional runtime-use smoke",
    "Live/private source-card read",
    "Additional source-card read",
    "Source discovery / workspace-family scan / broad recall / index query",
    "Runtime Registry",
    "Provider/backend/source callbacks",
    "Persistence / mutation / custody / rollback / cache purge",
    "Service/listener/startup/global activation",
    "Credentials/auth/env/keychain/OAuth/auth files",
    "Publication / visibility / provider-prod-canary / Gate / Atlas Gate",
    "Broad `allowed=true`",
    "Cron / automation",
)

RESIDUAL_HOLDS = (
    "any additional runtime-use smoke or adapter call beyond #292's consumed one-smoke approval",
    "live/private reads and any additional source-card reads",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "provider/backend/source-stat/source-read callbacks",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
    "service/listener/startup/global activation and cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement",
    "broad `allowed=true` behavior",
)

UNSAFE_REPORT_CLASSES = (
    "raw private content",
    "raw source text",
    "raw approval prose",
    "credentials",
    "auth material",
    "environment values",
    "keychain material",
    "OAuth material",
    "auth-file material",
    "private absolute paths",
    "source URIs",
    "platform IDs",
    "prompts",
    "queries",
    "payloads",
    "backend responses",
    "private correlation refs",
    "Runtime Registry handles",
    "provider handles",
    "secret values",
    "token-like values",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6af03_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6af03-runtime-use-smoke-value-receipt-held-surface-map.md" in docs_index
    assert "tests/test_l6af03_runtime_use_smoke_value_receipt_held_surface_map.py" in inventory
    assert "L6AF.03 runtime-use smoke value receipt" in inventory
    assert STATUS in inventory


def test_l6af03_records_status_source_floor_and_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AF.03 runtime-use smoke value receipt and held-surface map",
        f"Status: `{STATUS}`",
        "Rail issue: #293",
        "Parent issue: #6",
        "Depends on: #292 closed/PASS via PR #297",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Reviewed approval-packet PR: #296",
        "Reviewed runtime-use smoke PR: #297",
        f"Approval-packet merge source floor: `{APPROVAL_PACKET_SOURCE_FLOOR}`",
        f"Runtime-use smoke merge source floor: `{SMOKE_SOURCE_FLOOR}`",
        f"Issue-bound prep authorization: #291 comment `{PREP_AUTH_COMMENT}`",
        f"Consumed runtime-use approval: #292 comment `{RUNTIME_USE_APPROVAL_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        "Reviewed smoke artifact: `docs/l6af02-fixture-only-default-off-adapter-runtime-use-smoke.md`",
        "Verdict vocabulary: `PASS_VALUE_RECEIPT_HELD_SURFACE_MAP`, `FIX_BEFORE_TRUST_BOUNDARY_REVIEW`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
        "docs/tests/review scope only",
        "performs no additional adapter runtime-use smoke",
    )
    for term in required_terms:
        assert term in text


def test_l6af03_packages_prior_smoke_value_receipt_without_new_smoke() -> None:
    text = normalized(DOC)
    smoke_text = normalized(SMOKE_DOC)

    assert "Status: `PASS_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE`" in smoke_text
    assert "Runtime-use approval comment: `4653350823`" in smoke_text
    assert "broad `allowed=true` | `false`" in smoke_text

    assert "Report-safe value receipt from #292" in text
    for term in VALUE_RECEIPT_TERMS:
        assert term in text
    for term in (
        "one local fixture-only import/call of the committed default-off adapter module",
        "The useful result is control-plane evidence",
        "not a live source-card value proof",
        "not runtime integration",
        "not service activation",
        "not standing authority for another smoke",
    ):
        assert term in text


def test_l6af03_default_off_behavior_and_consumed_approval_boundary() -> None:
    text = normalized(DOC)

    for term in (
        "Default-off behavior remains intact",
        "Missing approval metadata returned `DENIED_DEFAULT_OFF`",
        "`allowed=false`",
        "`allowed_result_count=0`",
        "`live_read_invoked=false`",
        "narrow string label, not boolean `allowed=true`",
        "fixture-only, default-off, report-safe, metadata-only",
        "No guarded held-surface counter incremented",
        "The approval was consumed for #292 only",
        "#293 does not refresh, extend, or reuse runtime-use approval",
    ):
        assert term in text


def test_l6af03_held_surface_map_names_remaining_blockers() -> None:
    text = normalized(DOC)

    assert "Held-surface map after the smoke" in text
    for surface in HELD_SURFACES:
        assert surface in text
    for hold in RESIDUAL_HOLDS:
        assert hold in text
    for term in (
        "Any second smoke or broader runtime exercise requires fresh exact owner approval",
        "fixture refs are not read authority",
        "denial-before-registry proof",
        "denial-before-callback behavior",
        "Human release/Gate authority remains required",
        "General allow semantics remain held",
        "Automation changes remain held",
    ):
        assert term in text


def test_l6af03_report_safe_boundaries_and_next_blocker() -> None:
    text = normalized(DOC)

    assert "Report-safe boundaries" in text
    for unsafe_class in UNSAFE_REPORT_CLASSES:
        assert unsafe_class in text

    unsafe_example_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
        "platform-raw-id",
    )
    lowered = text.lower()
    for marker in unsafe_example_markers:
        assert marker not in lowered

    for term in (
        "Next open rail issue after #293: #294",
        "#294 is docs/tests/review scope only",
        "does not authorize an additional runtime-use smoke",
        "live/private read",
        "source-card read",
        "callback",
        "Runtime Registry consumption",
        "persistence/mutation",
        "activation",
        "cron change",
        "provider/prod/canary/Gate movement",
        "Atlas Gate movement",
        "broad `allowed=true` behavior",
    ):
        assert term in text
