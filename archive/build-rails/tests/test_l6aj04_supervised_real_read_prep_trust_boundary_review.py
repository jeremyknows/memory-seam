from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aj04-supervised-real-read-prep-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_PREP_TRUST_BOUNDARY_REVIEW_EXECUTION_STILL_HELD"
RAIL_STARTING_SOURCE_FLOOR = "e7b3e67c438891be00f4001d9cfff72026ebe4d3"
SOURCE_FLOOR_ENTERING_SLICE = "1d96bb793b50a6146496c1dba28c3d80b7015ed7"
PARENT_SUCCESSOR_PREP_COMMENT = "4654676210"
SCAFFOLD_AUTH_COMMENT = "4654676115"
DENIAL_HARNESS_PREAUTH_COMMENT = "4654676162"
OPERATION_CLASS = "L6AJ_SUPERVISED_REAL_READ_PREP_TRUST_BOUNDARY_REVIEW"
EVIDENCE_CLASS = "SUPERVISED_REAL_READ_PREP_PUBLIC_METADATA_TRUST_BOUNDARY_REVIEW"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aj04_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aj04-supervised-real-read-prep-trust-boundary-review.md" in docs_index
    assert "tests/test_l6aj04_supervised_real_read_prep_trust_boundary_review.py" in inventory
    assert "L6AJ.04 supervised real-read prep trust-boundary review" in inventory
    assert STATUS in inventory


def test_l6aj04_doc_records_issue_floor_dependencies_and_verdict() -> None:
    text = normalized(DOC)
    required_terms = (
        "# L6AJ.04 supervised real-read prep trust-boundary and stop-condition review",
        f"Status: `{STATUS}`",
        "Rail issue: #334",
        "Parent issue: #6",
        "Depends on: #331-#333 closed/PASS",
        "Roadmap step: 3 supervised real read with denial-before-read",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent L6AJ successor prep comment: `{PARENT_SUCCESSOR_PREP_COMMENT}`",
        f"Prior scaffold authorization reference: #331 comment `{SCAFFOLD_AUTH_COMMENT}`",
        f"Prior denial harness preauthorization reference: #332 comment `{DENIAL_HARNESS_PREAUTH_COMMENT}`",
        f"Operation class: `{OPERATION_CLASS}`",
        f"Evidence class: `{EVIDENCE_CLASS}`",
        "Verdict vocabulary: `PASS_PREP_TRUST_BOUNDARY_REVIEW_EXECUTION_STILL_HELD`, `FIX_PREP_BEFORE_RECONCILIATION`, `HOLD_FOR_EXACT_OWNER_EXECUTION_APPROVAL`.",
        f"Verdict: `{STATUS}`",
        "Next open rail issue after #334: #335 `L6AJ.05: source-floor parent tracker reconciliation for supervised real-read prep`.",
    )
    for term in required_terms:
        assert term in text


def test_l6aj04_review_names_only_committed_prep_artifacts() -> None:
    text = normalized(DOC)
    required_artifacts = (
        "docs/l6aj01-supervised-real-read-exact-approval-packet-scaffold.md",
        "src/memory_seam/l6aj_denial_before_read_harness.py",
        "docs/l6aj02-denial-before-read-fixture-harness.md",
        "src/memory_seam/l6aj_report_safe_envelope.py",
        "docs/l6aj03-report-safe-source-query-output-envelope.md",
    )
    for artifact in required_artifacts:
        assert artifact in text

    assert "This review consumes only committed repo docs, tests, fixtures, small prep modules, issue numbers, comment identifiers, and source-floor metadata." in text
    assert "It does not execute a supervised real read and does not authorize one." in text


def test_l6aj04_trust_boundary_findings_preserve_prep_only_posture() -> None:
    text = normalized(DOC)
    required_terms = (
        "Finding: `PASS_PREP_BOUNDARY_INTACT`.",
        "execution remains false/held in the prep packet, denial harness, and envelope",
        "allowed behavior is narrow status vocabulary and fixture/report-safe metadata only, not broad `allowed=true`",
        "future approval must be owner-created, issue-bound, fresh, exact, bounded to max one supervised real-read operation",
        "paired with exactly one denied out-of-scope request before source access",
        "synthetic source/query refs are placeholders and do not dereference real private sources, source cards, Runtime Registry entries, provider routes, callback routes, credentials, local workspaces, families, indexes, or raw source text",
        "raw/private/source/approval/credential echo fields are rejected or forbidden in report-safe output",
        "guarded counters for live/private reads, source-card reads, raw/private/credential access, discovery, Runtime Registry, callbacks/provider routes, persistence/mutation/writes, activation, cron, publication/Gate movement, and broad-allow variants remain zero",
    )
    for term in required_terms:
        assert term in text


def test_l6aj04_stop_conditions_deny_before_read_for_missing_or_unsafe_bindings() -> None:
    text = normalized(DOC)
    required_terms = (
        "missing fresh owner-created execution issue/comment",
        "stale, copied, broadened, non-owner, unrelated, expired, closed-issue-only, or comment-mismatch approval",
        "missing or mismatched parent issue, rail issue, repo, source-floor, actor association, source binding, descriptor/source-card ref, query binding, output purpose, operation class, max-operation count, denied-request count, expiry, or report-safe receipt contract",
        "request attempts more than one supervised real-read operation or more than one denied out-of-scope request",
        "denial-before-read cannot be proven before source access",
        "output would expose raw private content, raw source text, raw approval prose, credential/auth/env/keychain/OAuth/auth-file material",
        "Runtime Registry read, real callback/provider route, persistence/mutation/write/delete/reindex/cache-purge/rollback execution",
        "service/listener/startup/global activation, cron change, publication/visibility/provider/prod/canary/Gate movement, Atlas Gate movement, or broad `allowed=true` behavior",
        "Stop action: return/report a metadata-only HOLD or DENIED-BEFORE-READ receipt and do not read, discover, callback, persist, mutate, activate, publish, move Gate/Atlas Gate, roll back, cache purge, or retry through a broader path.",
    )
    for term in required_terms:
        assert term in text


def test_l6aj04_boundary_preserved_and_residual_holds_are_explicit() -> None:
    text = normalized(DOC)
    required_terms = (
        "does not execute a supervised real read",
        "does not perform a live/private read",
        "does not read source cards",
        "does not read raw private content/source text/approval prose",
        "does not read credentials/auth/env/keychain/OAuth/auth-file material",
        "does not perform source discovery, workspace scans, family scans, broad recall, or index queries",
        "does not consume Runtime Registry data",
        "does not invoke real callbacks/provider routes",
        "does not persist, mutate, write, delete, reindex, cache-purge, rollback execute, or mutate runtime cache",
        "does not activate service/listener/startup/global paths",
        "does not change cron automation",
        "does not publish, change visibility, move provider/prod/canary/Gate surfaces, or move Atlas Gate",
        "does not create broad `allowed=true` behavior",
        "Residual holds: supervised real-read execution",
        "publication/provider/prod/canary/Gate movement and Atlas Gate movement, writes, and broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6aj04_carries_reconciliation_only_next_step() -> None:
    text = normalized(DOC)
    assert "The L6AJ prep artifacts are ready for #335 source-floor/parent/tracker reconciliation." in text
    assert "Roadmap step 3 execution remains held." in text
    assert "#335 may reconcile source floor, parent status, and the Atlas roadmap tracker only" in text
    assert "supervised real-read execution remains held pending a future exact owner-created execution issue/comment binding source/query/output and operation count" in text
