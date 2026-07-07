from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ak02-route-audience-auth-binding.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_ROUTE_AUDIENCE_AUTH_BINDING_DESIGNED_RETRY_STILL_HELD"
NEXT_FRONTIER = "NON_SECRET_AUTH_CONTRACT_SHIM_OR_TYPED_RECEIPT_IMPLEMENTATION_BEFORE_RETRY"
RAIL_STARTING_SOURCE_FLOOR = "95e7a7979ae092703da8f77c4d897f703348a308"
SOURCE_FLOOR_ENTERING_SLICE = "407a80a"
OPERATION_CLASS = "L6AK_ROUTE_AUDIENCE_AUTH_BINDING_DESIGN"
EVIDENCE_CLASS = "SUPERVISED_METADATA_READ_ROUTE_AUDIENCE_AUTH_CONTRACT"

BINDINGS = (
    "`identity_subject` | the authenticated service principal or caller subject is explicitly present as a non-secret label | `missing_identity_subject` or `mismatched_identity_subject`",
    "`acting_for` | `sax` is explicitly represented as the supervised acting agent | `mismatched_agent`",
    "`agent` | request agent is exactly `sax` | `mismatched_agent`",
    "`audience` | route audience is exactly the Memory Seam supervised metadata-read audience for atlas-query MCP | `wrong_route_audience`",
    "`scope` | recall scope is exactly `wiki`; context include is exactly `health` for the health check path | `broadened_scope` or `unauthorized_narrowing`",
    "`output_mode` | metadata-only/report-safe receipt fields only | `raw_output_requested`",
    "`approval_freshness` | approval/rail authority is fresh, issue-bound, and not copied from stale evidence | `stale_approval`",
    "`operation_count` | max one exact supervised metadata read retry after implementation is verified | `broadened_scope`",
)

DENIAL_CASES = (
    "wrong route audience | deny with `wrong_route_audience` before read | none",
    "unauthorized narrowing | deny with `unauthorized_narrowing` before read | none",
    "stale approval | deny with `stale_approval` before read | none",
    "mismatched agent | deny with `mismatched_agent` before read | none",
    "broadened scope | deny with `broadened_scope` before read | none",
    "raw-output request | deny with `raw_output_requested` before read | none",
    "missing identity subject | deny with `missing_identity_subject` before read | none",
    "all exact bindings present | may return `ready_for_exact_retry=true` as non-secret readiness only, not execute the retry | none in #342",
)

HELD_TERMS = (
    "performs no live read retry",
    "reads no credentials",
    "auth files",
    "environment values",
    "keychain entries",
    "OAuth material",
    "raw/private content",
    "source cards",
    "source URIs",
    "platform raw IDs",
    "Runtime Registry payloads",
    "callback payloads",
    "provider payloads",
    "private source identifiers",
)

FORBIDDEN_MARKERS = (
    "oauth token",
    "credential value",
    "auth-file secret",
    "private-correlation-ref",
    "source://",
    "platform-raw-id",
    "runtime registry payload value",
    "callback payload body value",
    "provider payload body value",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ak02_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ak02-route-audience-auth-binding.md" in docs_index
    assert "tests/test_l6ak02_route_audience_auth_binding.py" in inventory
    assert "L6AK.02 route-audience auth binding" in inventory
    assert STATUS in inventory


def test_l6ak02_records_issue_floor_dependency_and_verdict() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AK.02 route-audience auth binding for supervised metadata read",
        f"Status: `{STATUS}`",
        "Rail issue: #342",
        "Parent issue: #6",
        "Depends on: #341 closed/PASS safe 403 receipt",
        "Roadmap step: 3 supervised real read with denial-before-read, auth blocker points toward step 5 service/provider auth",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Prior receipt: #341 / PR #345",
        f"Operation class: `{OPERATION_CLASS}`",
        f"Evidence class: `{EVIDENCE_CLASS}`",
        "Verdict vocabulary: `PASS_ROUTE_AUDIENCE_AUTH_BINDING_DESIGNED_RETRY_STILL_HELD`, `FIX_AUTH_CONTRACT_BEFORE_IMPLEMENTATION`, `DENY_BEFORE_READ_FOR_BINDING_MISMATCH`.",
        f"Verdict: `{STATUS}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    ):
        assert term in text


def test_l6ak02_binding_contract_names_identity_acting_for_audience_scope_and_output() -> None:
    text = normalized(DOC)

    assert "A future exact supervised metadata-only retry may proceed only if a non-secret contract proves all of these bindings before source access" in text
    for binding in BINDINGS:
        assert binding in text
    assert "The contract must default-deny" in text
    assert "metadata-only denial receipt before read" in text


def test_l6ak02_denial_before_read_matrix_covers_required_auth_blockers() -> None:
    text = normalized(DOC)

    assert "Denial-before-read matrix" in text
    for case in DENIAL_CASES:
        assert case in text


def test_l6ak02_capability_matrix_keeps_retry_and_broader_reads_held() -> None:
    text = normalized(DOC)

    for term in (
        "#341 safe 403 receipt merged | satisfied",
        "Non-secret route-audience contract defined | satisfied by this design",
        "Code shim or typed receipt implementation | blocked pending #343",
        "Targeted denial-before-read tests for wrong audience and unauthorized narrowing | specified here; implementation pending #343",
        "Exact retry authorization after verified auth binding | held",
        "Broader reads or source discovery | forbidden",
        "Raw/private/source/auth material output | forbidden",
        "Runtime Registry/callback/provider payload consumption | forbidden",
        "Persistence, mutation, write/delete/reindex/cache-purge/rollback | forbidden",
        "Service activation, cron change, publication, provider/prod/canary/Gate, Atlas Gate movement | forbidden",
    ):
        assert term in text


def test_l6ak02_boundaries_and_handoff_preserve_no_secret_no_activation_posture() -> None:
    text = normalized(DOC)

    for term in HELD_TERMS:
        assert term in text
    for term in (
        "#343 may implement the smallest non-secret contract shim or typed receipt behavior needed to validate the bindings above",
        "must not load secrets",
        "read environment/auth/keychain/OAuth/auth-file material",
        "activate services",
        "call providers",
        "consume Runtime Registry data",
        "retry the real read",
        "create broad `allowed=true` behavior",
        "write/mutate outside repo docs/tests/code",
    ):
        assert term in text

    lowered = text.lower()
    for marker in FORBIDDEN_MARKERS:
        assert marker not in lowered


def test_l6ak02_verification_gate() -> None:
    text = normalized(DOC)

    for term in (
        "python -m pytest -q tests/test_l6ak02_route_audience_auth_binding.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
