from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ah02-post-implementation-fixture-only-integration-receipt-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
IMPLEMENTATION = REPO_ROOT / "src" / "memory_seam" / "l6ag_default_off_runtime_integration.py"

STATUS = "PASS_POST_IMPLEMENTATION_RECEIPT_REVIEW_FIXTURE_ONLY_DEFAULT_OFF_RUNTIME_INTEGRATION"
VERDICT = "PASS_POST_IMPLEMENTATION_RECEIPT_REVIEW"
RAIL_STARTING_SOURCE_FLOOR = "df8e034cd0d53c675212b6f7aa594abd4bd272d3"
ENTERING_SOURCE_FLOOR = "365dd286566ad3d1a1c34bd7752ad7fa4f41b483"
IMPLEMENTATION_PR = "#316"
IMPLEMENTATION_MERGE_COMMIT = "365dd286566ad3d1a1c34bd7752ad7fa4f41b483"
CONSUMED_APPROVAL_COMMENT = "4654131093"
PARENT_SUCCESSOR_COMMENT = "4654131206"
OPERATION_CLASS = "L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE"

ALLOWED_FILES = (
    "src/memory_seam/l6ag_default_off_runtime_integration.py",
    "tests/test_l6ag_default_off_runtime_integration.py",
    "docs/l6ah01-default-off-runtime-integration-receipt.md",
    "docs/README.md",
    "docs/contract-test-inventory.md",
)

HELD_COUNTER_TERMS = (
    "live/private reads and source-card reads",
    "additional adapter calls or runtime-use smokes",
    "raw private content, raw source text, and raw approval prose reads",
    "credential/auth/env/keychain/OAuth/auth-file reads",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry reads",
    "provider/backend/source-stat/source-read callbacks and provider routes",
    "persistence, mutation, write/delete/reindex/cache-purge/rollback callbacks",
    "service/listener/startup/global activation and cron changes",
    "publication/visibility changes",
    "provider/prod/canary/Gate movement and Atlas Gate movement",
    "broad `allowed=true` results",
)

RESIDUAL_HOLDS = (
    "live/private reads and source-card reads",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "callbacks, provider/backend/source-stat/source-read routes, and provider routes",
    "persistence, mutation, audit/custody writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
    "service/listener/startup/global activation and cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, and Gate movement",
    "Atlas Gate movement",
    "additional adapter calls or runtime-use smokes beyond already-consumed historical evidence unless separately exact-approved",
    "broad `allowed=true` behavior",
)

FORBIDDEN_IMPORT_ROOTS = {
    "os",
    "subprocess",
    "requests",
    "httpx",
    "urllib",
    "keyring",
    "sqlite3",
    "socket",
}


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ah02_review_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ah02-post-implementation-fixture-only-integration-receipt-review.md" in docs_index
    assert "tests/test_l6ah02_post_implementation_fixture_only_integration_receipt_review.py" in inventory
    assert "L6AH.02 post-implementation fixture-only integration receipt review" in inventory
    assert STATUS in inventory


def test_l6ah02_records_status_source_floor_and_review_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AH.02 post-implementation fixture-only integration receipt review",
        f"Status: `{STATUS}`",
        "Rail issue: #312",
        "Parent issue: #6",
        "Depends on: #311 closed/PASS via PR #316",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{ENTERING_SOURCE_FLOOR}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Reviewed implementation PR: {IMPLEMENTATION_PR}",
        f"Reviewed implementation merge commit: `{IMPLEMENTATION_MERGE_COMMIT}`",
        f"Issue-bound approval consumed: #311 comment `{CONSUMED_APPROVAL_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        f"Verdict: `{VERDICT}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ah02_verifies_allowed_file_envelope_only() -> None:
    text = normalized(DOC)

    for path in ALLOWED_FILES:
        assert f"`{path}`" in text
    assert "That set matches the exact #311 runtime-integration implementation envelope" in text
    assert "No runtime service, provider route, Runtime Registry, callback, Gate, cron, persistence, source discovery, credential, environment, keychain, OAuth, auth-file, publication, visibility, rollback-execution, cache, index, production-control, or global activation files were added or modified" in text


def test_l6ah02_verifies_fixture_only_default_off_and_report_safe_output() -> None:
    text = normalized(DOC)

    required_terms = (
        "stayed inside the exact default-off, fixture-only, report-safe runtime-integration envelope",
        "default-off unless caller-supplied approval metadata exactly matches",
        "`max_integration_slices=1`",
        "`max_runtime_use_smokes=0`",
        "every held-surface authorization flag false",
        "accepts caller-supplied committed report-safe adapter-value metadata only",
        "does not call the adapter, execute another runtime-use smoke",
        "does not call the adapter, execute another runtime-use smoke, fetch GitHub approval text, inspect local/private source files, read credentials",
        "Reportable PASS output is limited to schema/status strings, public descriptor/adapter-value/source-card fixture refs, usefulness labels",
        "a narrow non-boolean integration scope label",
        "`integration_slice_count=1`",
        "`runtime_use_smoke_count=0`",
        "Denied output keeps `allowed=false`",
        "`integration_slice_count=0`",
        "`live_adapter_invoked=false`",
        "output validator rejects broad `allowed=true`",
        "non-fixture adapter-value inputs",
    )
    for term in required_terms:
        assert term in text


def test_l6ah02_all_held_surface_counters_remain_zero() -> None:
    text = normalized(DOC)

    assert "All held-surface counters remain zero" in text
    for term in HELD_COUNTER_TERMS:
        assert term in text


def test_l6ah02_confirms_311_approval_consumed_once_not_standing_authority() -> None:
    text = normalized(DOC)

    required_terms = (
        "The #311 issue-bound approval was consumed exactly once by the merged #316 implementation slice",
        "cannot be reused by this #312 review",
        "parent #6 continuity",
        "source-floor advancement",
        "#313-#315 follow-up reviews",
        "future implementation work",
        "additional adapter calls or runtime-use smokes",
        "runtime activation",
        "live/private reads",
        "source-card reads",
        "Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6ah02_preserves_residual_holds_and_avoids_raw_private_examples() -> None:
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text

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


def test_l6ah02_implementation_uses_standard_library_only_and_no_side_effect_imports() -> None:
    tree = ast.parse(IMPLEMENTATION.read_text(encoding="utf-8"))
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])

    assert "collections" in imported_roots
    assert "typing" in imported_roots
    assert imported_roots.isdisjoint(FORBIDDEN_IMPORT_ROOTS)
