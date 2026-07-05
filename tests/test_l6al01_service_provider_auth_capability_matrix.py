from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6al01-service-provider-auth-capability-matrix.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_CAPABILITY_MATRIX_READY_RETRY_STILL_HELD"
OPERATION_CLASS = "L6AL_SERVICE_PROVIDER_AUTH_CAPABILITY_MATRIX"
EVIDENCE_CLASS = "SERVICE_PROVIDER_AUTH_MATRIX_DOCS_TESTS_ONLY"
READY = "AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY"
HELD = "AUTH_HELD_SERVICE_PROVIDER_BINDING_INCOMPLETE"
FIX = "FIX_AUTH_MATRIX_BEFORE_READINESS_DECISION"

ENDPOINT_ROWS = (
    "`context` | exact supervised metadata context read retry after L6AK safe 403 | `memory-seam:read:context`",
    "`recall` | exact supervised metadata recall retry after L6AK safe 403 | `memory-seam:read:recall`",
    "`health` | readiness/denial posture check only, never item retrieval | `memory-seam:read:health`",
)

REQUIRED_FIELDS = (
    "`route_audience`: exactly one endpoint audience",
    "`acting_for`: the owner/principal on whose behalf the supervised retry is being attempted",
    "`identity_subject`: the invoking service/profile identity; missing identity denies before read",
    "`scope`: metadata-only, report-safe output, exact target/query refs, max one operation",
    "`agent`: exact future issue-bound agent identity",
    "`expiry`: explicit approval expiry and freshness check",
    "`evidence_class`: one of `SUPERVISED_METADATA_CONTEXT_READ_RETRY`, `SUPERVISED_METADATA_RECALL_READ_RETRY`, or `SUPERVISED_METADATA_HEALTH_AUTH_POSTURE`",
)

DENIAL_ROWS = (
    "wrong audience | `wrong_route_audience`",
    "unauthorized narrowing | `unauthorized_narrowing`",
    "missing identity | `missing_identity_subject`",
    "stale approval | `stale_approval`",
    "broadened scope | `broadened_scope_denied`",
    "raw-output request | `raw_output_denied`",
    "provider/callback/write/Gate movement | `held_surface_requested`",
    "broad allow | `broad_allowed_true_denied`",
)

RESIDUAL_HOLDS = (
    "no secret/env/keychain/OAuth/auth-file/credential reads",
    "no live/private read retry",
    "no source discovery",
    "no broad recall/index queries",
    "no Runtime Registry consumption",
    "no provider callback invocation",
    "no service activation",
    "no cron changes",
    "no persistence/mutation/write/delete/reindex/rollback/cache-purge",
    "no publication/visibility/provider/prod/canary/Gate movement",
    "no Atlas Gate movement",
    "no broad `allowed=true` behavior",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6al01_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6al01-service-provider-auth-capability-matrix.md" in docs_index
    assert "tests/test_l6al01_service_provider_auth_capability_matrix.py" in inventory
    assert "L6AL.01 service/provider auth capability matrix" in inventory
    assert STATUS in inventory


def test_l6al01_records_status_scope_and_verdict_vocabulary() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AL.01 service/provider auth capability matrix for Memory Seam read retry",
        f"Status: `{STATUS}`",
        "Rail issue: #349",
        "Parent issue: #6",
        "Depends on: L6AK #341-#344 closed/PASS",
        "Roadmap step: 5 service/provider auth prerequisite for a future Step 3 exact supervised metadata read retry",
        "Rail starting source floor: `f335f09891a41f43583fbf434482cfb096a04fcd`",
        f"Operation classified: `{OPERATION_CLASS}`",
        f"Evidence class: `{EVIDENCE_CLASS}`",
        f"Verdict vocabulary: `{READY}`, `{HELD}`, `{FIX}`.",
        f"Verdict: `{STATUS}`",
        "performs no live/private read retry",
        "loads no secret material",
        "creates no route that can return broad `allowed=true` behavior",
    ):
        assert term in text


def test_l6al01_endpoint_capability_matrix_covers_read_endpoints() -> None:
    text = normalized(DOC)

    assert "Endpoint capability matrix" in text
    for row in ENDPOINT_ROWS:
        assert row in text
    for term in (
        "`SUPERVISED_METADATA_CONTEXT_READ_RETRY`",
        "`SUPERVISED_METADATA_RECALL_READ_RETRY`",
        "`SUPERVISED_METADATA_HEALTH_AUTH_POSTURE`",
        "auth-held until service/provider binding exists",
        "safe to report posture, not sufficient for retry execution",
    ):
        assert term in text


def test_l6al01_required_auth_fields_are_explicit() -> None:
    text = normalized(DOC)

    for field in REQUIRED_FIELDS:
        assert field in text
    for term in (
        "acting_for` must equal the issue-bound owner subject",
        "identity_subject` must equal the invoking Hermes profile/service subject",
        "fresh approval only, expiry present, stale approval denied",
        "not inherited by other agents",
        "no source discovery, no workspace/family scan, no index query, no broad recall",
    ):
        assert term in text


def test_l6al01_default_denial_matrix_preserves_denial_before_read() -> None:
    text = normalized(DOC)

    assert "Default-deny matrix" in text
    assert "Each case must deny before source/provider/backend/callback/read behavior" in text
    for row in DENIAL_ROWS:
        assert row in text
    for term in (
        "no endpoint fallback or cross-route narrowing",
        "no anonymous service/provider read",
        "no reuse of historical owner comments or L6AK/L6AA/L6AC read receipts",
        "no provider callback invocation",
        "no provider route execution",
        "no write/custody/delete/reindex/rollback/cache-purge",
        "no `allowed=true` or standing authorization path",
    ):
        assert term in text


def test_l6al01_report_safe_receipt_vocabulary_and_residual_holds() -> None:
    text = normalized(DOC)

    for term in (
        f"`{READY}`: all required non-secret service/provider bindings are present",
        f"`{HELD}`: one or more service/provider binding fields are missing",
        f"`{FIX}`: the matrix, fixture, or contract evidence is inconsistent",
        "read_authorized=false",
        "retry_executed=false",
        "items=[]",
    ):
        assert term in text
    for hold in RESIDUAL_HOLDS:
        assert hold in text

    lowered = text.lower()
    for marker in (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref value",
        "source://",
        "platform-raw-id value",
    ):
        assert marker not in lowered


def test_l6al01_verification_gate() -> None:
    text = normalized(DOC)

    for term in (
        "python -m pytest -q tests/test_l6al01_service_provider_auth_capability_matrix.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
