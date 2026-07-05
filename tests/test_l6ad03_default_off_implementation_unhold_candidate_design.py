from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ad03-default-off-implementation-unhold-candidate-design.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_DESIGN_PACKET_READY_IMPLEMENTATION_NOT_APPROVED"
RESULT = "PASS_DEFAULT_OFF_IMPLEMENTATION_CANDIDATE_READY_IMPLEMENTATION_NOT_APPROVED"
RAIL_STARTING_SOURCE_FLOOR = "f606ed18737d057f0b544503c2532935a9d6c258"
SOURCE_FLOOR_ENTERING_SLICE = "5157d40a5903ba54129b61ad5c8417df467300c8"
PARENT_SUCCESSOR_COMMENT = "4651958877"
AUTH_COMMENT = "4651958732"
OPERATION_CLASS = "L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ad03_design_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ad03-default-off-implementation-unhold-candidate-design.md" in docs_index
    assert "tests/test_l6ad03_default_off_implementation_unhold_candidate_design.py" in inventory
    assert "L6AD.03 default-off implementation unhold candidate design" in inventory
    assert STATUS in inventory


def test_l6ad03_records_status_source_floor_and_authorization():
    text = normalized(DOC)

    required_terms = (
        "# L6AD.03 default-off implementation unhold candidate design and rollback plan",
        f"Status: `{STATUS}`",
        "Rail issue: #273",
        "Parent issue: #6",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound authorization: #273 owner-created issue body and owner comment `{AUTH_COMMENT}`",
        "Prerequisite decision packet: [`l6ad02-implementation-or-hold-decision-packet.md`](l6ad02-implementation-or-hold-decision-packet.md)",
        f"Result: `{RESULT}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ad03_preserves_design_only_no_runtime_boundary():
    text = normalized(DOC)

    required_terms = (
        "docs/tests/design-only unhold candidate packet",
        "does not implement code/runtime behavior",
        "execute a source-card read, consume Runtime Registry, touch credentials/auth material, perform callbacks, mutate persistence, activate services, change cron schedules, publish, move provider/prod/canary state, move Atlas Gate",
        "create broad `allowed=true` behavior",
        "`NOT APPROVAL`: This packet is not itself implementation authority, runtime execution authority, read authority, Gate authority, or deployment authority",
        "The future implementation must not use a production/read-source clone as a write target",
    )
    for term in required_terms:
        assert term in text


def test_l6ad03_names_future_candidate_and_allowed_file_envelope():
    text = normalized(DOC)

    required_terms = (
        "`L6AD.N: default-off report-safe source-card value adapter implementation slice`",
        f"`{OPERATION_CLASS}`",
        "`src/memory_seam/l6ad_report_safe_source_card_value_adapter.py` — new module containing a default-off, fixture-only adapter skeleton",
        "`src/memory_seam/__init__.py` — optional export only if the future issue requires an importable package symbol",
        "`tests/test_l6ad_report_safe_source_card_value_adapter.py` — targeted unit tests",
        "`docs/l6ad-future-default-off-adapter-implementation-receipt.md` — optional future receipt",
        "`docs/README.md` — discoverability row only",
        "`docs/contract-test-inventory.md` — contract inventory row only",
        "Explicitly excluded unless a separate later owner approval narrows and authorizes them",
        "examples, CLI entry points, release/package publishing files, cron/schedule files, service/listener/startup files, provider adapters, runtime registry code",
        "Atlas Gate files",
    )
    for term in required_terms:
        assert term in text


def test_l6ad03_defines_default_off_approval_contract_and_denials():
    text = normalized(DOC)

    required_terms = (
        "explicit approval contract object or function parameter rather than reading credentials, environment, keychain, OAuth material, auth files, GitHub comments, issue text, Runtime Registry, or any private source",
        "repository: `jeremyknows/memory-seam`",
        "actor association: `OWNER`",
        f"operation class: `{OPERATION_CLASS}`",
        "Deny before any adapter action if approval is missing, stale, copied from prior issue, expired, broadened, mismatched to repo/issue/operation/files, non-owner",
        "permits any held surface, requests callbacks, requests Runtime Registry, requests persistence/mutation, requests service activation, requests publication/provider/prod/canary/Gate movement, changes cron/schedule behavior, or attempts broad `allowed=true`",
    )
    for term in required_terms:
        assert term in text


def test_l6ad03_report_safe_fixture_only_shape_and_future_approval_wording():
    text = normalized(DOC)

    required_terms = (
        "public descriptor reference string",
        "public source-card reference string",
        "guarded held surfaces, all expected to stay zero",
        "`DENIED_DEFAULT_OFF`, `PASS_REPORT_SAFE_VALUE_ADAPTER_FIXTURE_ONLY`, or `HOLD_FOR_OWNER_DECISION`",
        "The future adapter output must never include raw private content, raw source text, raw approval prose",
        "A future implementation issue should use this exact approval sentence shape",
        f"{OPERATION_CLASS}",
        "Scope is limited to source floor <source_floor_after_l6ad03>, repository jeremyknows/memory-seam, and these repo-relative files only: <exact_file_list>",
        "This wording is inert documentation in #273",
    )
    for term in required_terms:
        assert term in text


def test_l6ad03_future_tests_rollback_and_stop_conditions():
    text = normalized(DOC)

    required_terms = (
        "A future implementation issue must add `tests/test_l6ad_report_safe_source_card_value_adapter.py`",
        "missing approval denies with `DENIED_DEFAULT_OFF` and all guarded counters zero",
        "stale source floor, stale issue number, copied prior rail wording, broadened file envelope, expired UTC window, mismatched operation class, mismatched repository, non-owner actor",
        "exact valid fixture-only approval returns report-safe metadata and labels only",
        "all callback/source/provider/registry/persistence/mutation/write/custody/delete/reindex/rollback/cache-purge counters remain zero",
        "python -m pytest tests/test_l6ad_report_safe_source_card_value_adapter.py -q",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
        "Rollback must be limited to the future implementation PR",
        "Rollback execution itself remains held in L6AD.03",
        "Stop and hold for owner decision",
        "cannot remain fixture-only, report-safe, and default-off",
    )
    for term in required_terms:
        assert term in text


def test_l6ad03_residual_holds_and_next_issue():
    text = normalized(DOC)

    residual_holds = (
        "implementation/runtime execution until a separate exact owner-created future implementation issue approval exists",
        "live/private reads and any additional source-card read beyond the consumed historical #262 evidence",
        "raw private content, raw source text, raw approval prose, credentials, auth material, env/keychain/OAuth/auth-file reads",
        "source discovery, workspace scans, family scans, broad recall, and index queries",
        "Runtime Registry consumption",
        "provider/backend/source-stat/source-read callbacks",
        "persistence, mutation, audit/custody writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
        "service/listener/startup/global activation and recursive cron/schedule changes",
        "publication, visibility changes, provider/prod/canary authority, and Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for hold in residual_holds:
        assert hold in text

    assert "Next open rail issue after #273: #274 `L6AD.04: no-live trust-boundary review for implementation-or-hold rail`" in text
    assert "#274 should review #271-#273 no-live artifacts" in text

    unsafe_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
    )
    lowered = text.lower()
    for marker in unsafe_markers:
        assert marker not in lowered
