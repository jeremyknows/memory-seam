from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ag04-no-live-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW_POST_SMOKE_INTEGRATION_RAIL"
VERDICT = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW"
NEXT_FRONTIER = "SOURCE_FLOOR_PARENT_STATUS_RECONCILIATION_ALLOWED_FOR_ISSUE_305_ONLY"
RAIL_STARTING_SOURCE_FLOOR = "b7fe89f752372de4f42d5f7e1084acad99c5ebf0"
SOURCE_FLOOR_ENTERING_SLICE = "f8a91ccd7bdefab08d7bca5a5784e34609e1bc10"
INVENTORY_SOURCE_FLOOR = "49688202b1fdde0231f417ca3077b544e20781a6"
DECISION_SOURCE_FLOOR = "1ff55c0056248162b7726f966f7a5a31e9a8241f"
DESIGN_SOURCE_FLOOR = "f8a91ccd7bdefab08d7bca5a5784e34609e1bc10"
PARENT_SUCCESSOR_COMMENT = "4653805965"
INVENTORY_AUTH_COMMENT = "4653805822"
DESIGN_AUTH_COMMENT = "4653805892"
HISTORICAL_SMOKE_APPROVAL_COMMENT = "4653350823"
OPERATION_CLASS = "L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE"

REVIEWED_SURFACES = (
    "docs/l6ag01-post-smoke-integration-evidence-inventory-blocker-map.md",
    "docs/l6ag02-runtime-integration-or-continued-hold-decision-packet.md",
    "docs/l6ag03-default-off-integration-candidate-design-rollback-plan.md",
    "tests/test_l6ag01_post_smoke_integration_evidence_inventory_blocker_map.py",
    "tests/test_l6ag02_runtime_integration_or_continued_hold_decision_packet.py",
    "tests/test_l6ag03_default_off_integration_candidate_design_rollback_plan.py",
)

TRUST_BOUNDARY_FINDINGS = (
    "#292 runtime-use approval status | consumed historical authority only",
    "runtime integration implemented in #301-#304 | `false`",
    "adapter runtime-use smoke or adapter call in #301-#304 | `0`",
    "live/private reads invoked in #301-#304 | `false`",
    "source-card reads invoked in #301-#304 | `false`",
    "Runtime Registry consumed in #301-#304 | `false`",
    "callbacks or provider routes invoked in #301-#304 | `false`",
    "persistence or mutation invoked in #301-#304 | `false`",
    "write/delete/reindex/cache-purge or rollback executed | `false`",
    "service/listener/startup/global activation invoked | `false`",
    "cron changes invoked | `false`",
    "publication or visibility changes invoked | `false`",
    "provider/prod/canary/Gate movement invoked | `false`",
    "Atlas Gate movement invoked | `false`",
    "broad `allowed=true` created | `false`",
)

RESIDUAL_HOLDS = (
    "runtime integration and adapter wiring until a separate exact owner-created future runtime-integration issue approval exists",
    "any additional runtime-use smoke or adapter call beyond #292's consumed one-smoke approval",
    "live/private reads and any source-card reads",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "callbacks/provider routes, provider/backend/source-stat/source-read callbacks",
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


def test_l6ag04_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ag04-no-live-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ag04_no_live_trust_boundary_review.py" in inventory
    assert "L6AG.04 no-live trust-boundary review" in inventory
    assert STATUS in inventory


def test_l6ag04_records_status_source_floor_and_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AG.04 no-live trust-boundary review for post-smoke integration rail",
        f"Status: `{STATUS}`",
        "Rail issue: #304",
        "Parent issue: #6",
        "Depends on: #301-#303 closed/PASS via PRs #306-#308",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Reviewed inventory PR: #306",
        "Reviewed decision-packet PR: #307",
        "Reviewed design-packet PR: #308",
        f"Inventory merge source floor: `{INVENTORY_SOURCE_FLOOR}`",
        f"Decision-packet merge source floor: `{DECISION_SOURCE_FLOOR}`",
        f"Design-packet merge source floor: `{DESIGN_SOURCE_FLOOR}`",
        f"Parent L6AG successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound inventory authorization: #301 comment `{INVENTORY_AUTH_COMMENT}`",
        f"Issue-bound design authorization: #303 comment `{DESIGN_AUTH_COMMENT}`",
        f"Historical runtime-use smoke approval consumed by L6AF.02: #292 comment `{HISTORICAL_SMOKE_APPROVAL_COMMENT}`",
        f"Future operation class reviewed as design-only: `{OPERATION_CLASS}`",
        "Verdict vocabulary: `PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW`, `FIX_BEFORE_RECONCILIATION`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ag04_reviews_public_metadata_and_committed_surfaces_only() -> None:
    text = normalized(DOC)

    required_terms = (
        "inspected committed repository docs/tests surfaces plus public issue/PR/source-floor metadata only",
        "did not implement runtime integration",
        "did not wire adapters into runtime routes",
        "did not execute another adapter call or runtime-use smoke",
        "did not perform a live/private read",
        "did not read a source card",
        "did not fetch or publish raw approval prose",
        "did not read credentials/auth/env/keychain/OAuth/auth-file material",
        "did not discover sources",
        "did not scan workspaces or families",
        "did not run broad recall or index queries",
        "did not consume Runtime Registry data",
        "did not invoke callbacks or provider routes",
        "did not persist or mutate state",
        "did not activate a service/listener/startup/global path",
        "did not create or modify cron automation",
        "did not publish or change visibility",
        "did not move provider/prod/canary/Gate or Atlas Gate state",
        "did not create broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text
    for surface in REVIEWED_SURFACES:
        assert f"`{surface}`" in text


def test_l6ag04_reviews_301_303_evidence_and_consumed_smoke_boundary() -> None:
    text = normalized(DOC)

    required_terms = (
        "L6AG.01 post-smoke integration evidence inventory and blocker map (#301 / PR #306",
        "distinguished the already-consumed #292 fixture-only runtime-use smoke from runtime integration authority",
        "L6AG.02 runtime-integration-or-continued-hold decision packet (#302 / PR #307",
        "rejected approval-by-inertia from #292, #295, #301, parent receipts",
        "L6AG.03 default-off integration candidate design and rollback plan (#303 / PR #308",
        "remained docs/tests/design-only",
        "The #301-#303 rail stayed inside docs/tests/fixtures/public-metadata-only boundaries",
        "Its only runtime-use evidence is historical",
        "L6AG did not repeat, extend, refresh, or broaden that smoke",
    )
    for term in required_terms:
        assert term in text

    for finding in TRUST_BOUNDARY_FINDINGS:
        assert finding in text

    assert "not reusable by #293, #294, #295, #301, #302, #303, this #304 review, #305, parent #6" in text


def test_l6ag04_approval_by_inertia_and_future_denial_before_action() -> None:
    text = normalized(DOC)

    required_terms = (
        f"L6AG.02 and L6AG.03 correctly name `{OPERATION_CLASS}` as a future exact issue-bound operation class candidate only",
        "The phrase is not approval",
        "future approval wording is inert documentation until a later owner-created issue binds the exact issue number",
        "A future integration attempt must deny before any adapter action, provider route, Runtime Registry read, callback, persistence, activation, live/private read, source-card read, source discovery, cron change, Gate movement, or broad allow result",
        "approval is missing, stale, copied from prior issues, expired, broadened, mismatched to repo/issue/source-floor/operation/files, non-owner",
        "permits another smoke, permits any held surface, requests callbacks, requests Runtime Registry, requests persistence/mutation",
        "changes cron/schedule behavior, or attempts broad `allowed=true`",
    )
    for term in required_terms:
        assert term in text


def test_l6ag04_report_safety_and_absent_runtime_surfaces() -> None:
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
        "#304 itself is a review packet and not a service, adapter, provider, Registry, callback, persistence, activation, publication, cron, or Gate operation",
    )
    for term in required_terms:
        assert term in text


def test_l6ag04_future_integration_expectations_residual_holds_and_next_issue() -> None:
    text = normalized(DOC)

    required_terms = (
        "deny missing, stale, copied, expired, broadened, non-owner, wrong-repository, wrong-issue, wrong-source-floor, wrong-operation-class, wrong-file-envelope, or max-operation-count greater than one approvals before adapter action",
        "deny any request for additional runtime-use smoke or adapter call unless the exact future issue separately names and bounds it",
        "deny live/private reads, source-card reads, raw private content, raw source text, raw approval prose",
        "emit only report-safe metadata, status labels, safe refs, booleans, operation counts, zero guarded counters, denial reasons, and residual hold labels",
        "stop for owner decision if the future candidate cannot remain fixture-only, report-safe, default-off, denial-before-callback, no-live by default",
        "Next open rail issue after #304: #305 `L6AG.05: source-floor anchor, parent status, and next frontier reconciliation`",
        "#305 is docs/tests/public-metadata-only reconciliation scope",
        "may anchor #301-#305 PR/source floors and provide the parent #6 completion receipt template after merge",
        "must not execute runtime integration",
        "another runtime-use smoke",
        "another adapter call",
        "live/private reads",
        "source-card reads",
        "Runtime Registry consumption",
        "callbacks/provider routes",
        "cron changes",
        "Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text
    for hold in RESIDUAL_HOLDS:
        assert hold in text


def test_l6ag04_report_safe_doc_excludes_obvious_unsafe_examples() -> None:
    text = normalized(DOC).lower()

    unsafe_example_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
        "platform-raw-id",
    )
    for marker in unsafe_example_markers:
        assert marker not in text
