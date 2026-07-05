from __future__ import annotations

import ast
from pathlib import Path

from memory_seam.l6ag_default_off_runtime_integration import (
    L6AH_GUARDED_COUNTERS,
    build_l6ah01_exact_approval_fixture,
    integrate_l6ah01_report_safe_adapter_value,
    validate_l6ah01_runtime_integration_output,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ah03-no-live-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
IMPLEMENTATION = REPO_ROOT / "src" / "memory_seam" / "l6ag_default_off_runtime_integration.py"

STATUS = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW_DEFAULT_OFF_RUNTIME_INTEGRATION_RAIL"
VERDICT = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW"
NEXT_FRONTIER = "USE_PROOF_PACKET_AND_HELD_ACTIVATION_MAP_ALLOWED_FOR_ISSUE_314_ONLY"
RAIL_STARTING_SOURCE_FLOOR = "df8e034cd0d53c675212b6f7aa594abd4bd272d3"
ENTERING_SOURCE_FLOOR = "91538337422bffc46ca4a53540fcf728f669f8cf"
IMPLEMENTATION_SOURCE_FLOOR = "365dd286566ad3d1a1c34bd7752ad7fa4f41b483"
RECEIPT_REVIEW_SOURCE_FLOOR = "91538337422bffc46ca4a53540fcf728f669f8cf"
CONSUMED_APPROVAL_COMMENT = "4654131093"
PARENT_SUCCESSOR_COMMENT = "4654131206"
OPERATION_CLASS = "L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE"

REVIEWED_SURFACES = (
    "src/memory_seam/l6ag_default_off_runtime_integration.py",
    "tests/test_l6ag_default_off_runtime_integration.py",
    "docs/l6ah01-default-off-runtime-integration-receipt.md",
    "docs/l6ah02-post-implementation-fixture-only-integration-receipt-review.md",
    "tests/test_l6ah02_post_implementation_fixture_only_integration_receipt_review.py",
)

TRUST_BOUNDARY_FINDINGS = (
    "#311 implementation approval status | consumed once by PR #316",
    "additional adapter calls or runtime-use smokes in #311-#313 | `0`",
    "live/private reads invoked in #311-#313 | `false`",
    "source-card reads invoked in #311-#313 | `false`",
    "raw private content/source text/approval prose reads invoked | `false`",
    "credentials/auth/env/keychain/OAuth/auth-file reads invoked | `false`",
    "source discovery/workspace/family scans/broad recall/index queries invoked | `false`",
    "Runtime Registry consumed in #311-#313 | `false`",
    "callbacks or provider routes invoked in #311-#313 | `false`",
    "persistence or runtime mutation invoked in #311-#313 | `false`",
    "write/delete/reindex/cache-purge or rollback executed | `false`",
    "service/listener/startup/global activation invoked | `false`",
    "cron changes invoked | `false`",
    "publication or visibility changes invoked | `false`",
    "provider/prod/canary/Gate movement invoked | `false`",
    "Atlas Gate movement invoked | `false`",
    "broad `allowed=true` created | `false`",
)

RESIDUAL_HOLDS = (
    "live/private reads and source-card reads",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "callbacks/provider routes, provider/backend/source-stat/source-read callbacks",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
    "service/listener/startup/global activation and cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement",
    "additional adapter calls or runtime-use smokes unless separately exact-approved",
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


def test_l6ah03_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ah03-no-live-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ah03_no_live_trust_boundary_review.py" in inventory
    assert "L6AH.03 no-live trust-boundary review" in inventory
    assert STATUS in inventory


def test_l6ah03_records_status_source_floor_and_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AH.03 no-live trust-boundary review for integration implementation rail",
        f"Status: `{STATUS}`",
        "Rail issue: #313",
        "Parent issue: #6",
        "Depends on: #311-#312 closed/PASS via PRs #316-#317",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{ENTERING_SOURCE_FLOOR}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        "Reviewed implementation PR: #316",
        "Reviewed receipt-review PR: #317",
        f"Implementation merge source floor: `{IMPLEMENTATION_SOURCE_FLOOR}`",
        f"Receipt-review merge source floor: `{RECEIPT_REVIEW_SOURCE_FLOOR}`",
        f"Consumed implementation approval: #311 comment `{CONSUMED_APPROVAL_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        "Verdict vocabulary: `PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW`, `FIX_BEFORE_RECONCILIATION`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ah03_reviews_public_metadata_and_committed_surfaces_only() -> None:
    text = normalized(DOC)

    required_terms = (
        "inspected committed repository code/docs/tests surfaces plus public issue/PR/source-floor metadata only",
        "did not perform live/private reads",
        "did not read source cards",
        "did not fetch or publish raw approval prose",
        "did not read credentials/auth/env/keychain/OAuth/auth-file material",
        "did not discover sources",
        "did not scan workspaces or families",
        "did not run broad recall or index queries",
        "did not consume Runtime Registry data",
        "did not invoke callbacks or provider routes",
        "did not persist or mutate state",
        "did not activate a service/listener/startup/global route",
        "did not create or modify cron automation",
        "did not publish or change visibility",
        "did not move provider/prod/canary/Gate or Atlas Gate state",
        "did not execute an additional adapter call or runtime-use smoke",
        "did not create broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text
    for surface in REVIEWED_SURFACES:
        assert f"`{surface}`" in text


def test_l6ah03_reviews_311_312_evidence_and_consumed_approval_boundary() -> None:
    text = normalized(DOC)

    required_terms = (
        "L6AH.01 default-off runtime-integration implementation (#311 / PR #316",
        "fixture-only, report-safe default-off integration seam",
        "does not call an adapter, provider route, callback, Runtime Registry, persistence layer, activation path, live/private reader, or source-card reader",
        "L6AH.02 post-implementation fixture-only integration receipt review (#312 / PR #317",
        "verified the #311/#316 implementation file envelope",
        "side-effect import hygiene without executing another integration slice or adapter call",
        "stayed inside the exact default-off repository code/docs/tests/fixtures slice authorized by #311 comment",
        "approval was consumed by #311 / PR #316 only",
        "do not reuse the implementation approval as standing authority",
    )
    for term in required_terms:
        assert term in text
    for finding in TRUST_BOUNDARY_FINDINGS:
        assert finding in text


def test_l6ah03_default_off_behavior_and_guarded_counters_are_held() -> None:
    text = normalized(DOC)
    denied = integrate_l6ah01_report_safe_adapter_value(None)
    exact = integrate_l6ah01_report_safe_adapter_value(build_l6ah01_exact_approval_fixture())

    required_terms = (
        "default-off unless caller-supplied approval metadata exactly matches",
        "`max_integration_slices=1`",
        "`max_runtime_use_smokes=0`",
        "Denied output keeps `allowed=false`",
        "`approval_matched=false`",
        "`default_off_denied=true`",
        "`integration_slice_count=0`",
        "`runtime_use_smoke_count=0`",
        "`live_adapter_invoked=false`",
        "`callback_invoked=false`",
        "`registry_consumed=false`",
        "`persistence_attempted=false`",
        "`activation_attempted=false`",
        "`broad_allowed_attempted=false`",
        "narrow non-boolean label `EXACT_FIXTURE_ONLY_RUNTIME_INTEGRATION_SLICE`",
        "does not create broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text

    assert validate_l6ah01_runtime_integration_output(denied) == []
    assert validate_l6ah01_runtime_integration_output(exact) == []
    assert denied["allowed"] is False
    assert denied["integration_slice_count"] == 0
    assert exact["allowed"] == "EXACT_FIXTURE_ONLY_RUNTIME_INTEGRATION_SLICE"
    assert exact["allowed"] is not True
    assert exact["integration_slice_count"] == 1
    for output in (denied, exact):
        assert output["runtime_use_smoke_count"] == 0
        assert output["live_adapter_invoked"] is False
        assert output["callback_invoked"] is False
        assert output["registry_consumed"] is False
        assert output["persistence_attempted"] is False
        assert output["activation_attempted"] is False
        assert output["broad_allowed_attempted"] is False
        assert all(output["guarded_counters"][counter] == 0 for counter in L6AH_GUARDED_COUNTERS)


def test_l6ah03_approval_by_inertia_and_future_denial_before_action() -> None:
    text = normalized(DOC)

    required_terms = (
        "The #311 approval is not reusable by #312, this #313 review, #314, #315, parent #6 continuity",
        "source-floor advancement",
        "copied comments, stale comments, broadened comments",
        "future implementation work",
        "additional adapter calls",
        "runtime-use smokes",
        "live/private reads",
        "source-card reads",
        "Runtime Registry consumption",
        "callbacks/provider routes",
        "Atlas Gate movement",
        "broad `allowed=true` behavior",
        "Any future use beyond the exact #311 implementation must deny before adapter action, provider route, Runtime Registry read, callback, persistence, activation, live/private read, source-card read, source discovery, cron change, Gate movement, or broad allow result",
        "later exact owner-created issue binds that future operation, file envelope, source floor, max operation count, report-safe output",
    )
    for term in required_terms:
        assert term in text


def test_l6ah03_report_safety_and_absent_runtime_surfaces() -> None:
    text = normalized(DOC)

    assert "Reportable evidence in this review is limited" in text
    for unsafe_class in UNSAFE_REPORT_CLASSES:
        assert unsafe_class in text

    required_terms = (
        "No Runtime Registry consumer",
        "registry handle",
        "provider route",
        "provider callback",
        "backend callback",
        "source-stat callback",
        "source-read callback",
        "write/custody/delete/reindex/rollback/cache-purge callback",
        "persistence store",
        "mutation route",
        "audit/custody write",
        "cache mutation",
        "rollback executor",
        "service/listener startup hook",
        "global activation path",
        "cron change",
        "publication route",
        "visibility change",
        "provider/prod/canary control",
        "Gate control",
        "Atlas Gate control",
        "Rollback remains documentation-only",
        "#313 itself is a review packet and not a service, adapter, provider, Registry, callback, persistence, activation, publication, cron, or Gate operation",
    )
    for term in required_terms:
        assert term in text


def test_l6ah03_implementation_has_no_side_effect_imports() -> None:
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


def test_l6ah03_residual_holds_next_issue_and_no_unsafe_examples() -> None:
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text
    required_terms = (
        "Next open rail issue after #313: #314 `L6AH.04: integration use-proof packet and held-activation map`",
        "#314 is docs/tests/fixtures/public-metadata-only use-proof and held-activation-map scope",
        "may explain how the integration is invoked in fixture-only/default-off contexts",
        "must not execute another adapter call",
        "another runtime-use smoke",
        "a live/private read",
        "a source-card read",
        "Runtime Registry consumption",
        "callbacks/provider routes",
        "persistence/runtime mutation",
        "activation",
        "cron changes",
        "provider/prod/canary/Gate movement",
        "Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text

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
