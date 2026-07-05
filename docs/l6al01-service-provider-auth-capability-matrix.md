# L6AL.01 service/provider auth capability matrix for Memory Seam read retry

Status: `PASS_CAPABILITY_MATRIX_READY_RETRY_STILL_HELD`

Rail issue: #349
Parent issue: #6
Depends on: L6AK #341-#344 closed/PASS
Roadmap step: 5 service/provider auth prerequisite for a future Step 3 exact supervised metadata read retry
Rail starting source floor: `f335f09891a41f43583fbf434482cfb096a04fcd`
Operation classified: `L6AL_SERVICE_PROVIDER_AUTH_CAPABILITY_MATRIX`
Evidence class: `SERVICE_PROVIDER_AUTH_MATRIX_DOCS_TESTS_ONLY`
Verdict vocabulary: `AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY`, `AUTH_HELD_SERVICE_PROVIDER_BINDING_INCOMPLETE`, `FIX_AUTH_MATRIX_BEFORE_READINESS_DECISION`.
Verdict: `PASS_CAPABILITY_MATRIX_READY_RETRY_STILL_HELD`

This packet is a committed capability matrix only. It performs no live/private read retry, loads no secret material, invokes no provider callback, consumes no Runtime Registry payload, starts no service, and creates no route that can return broad `allowed=true` behavior.

## Endpoint capability matrix

| Memory Seam read endpoint | Future purpose | Required route audience | Required acting-for / identity subject | Required scope | Required agent binding | Expiry / freshness | Evidence class | Current state |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `context` | exact supervised metadata context read retry after L6AK safe 403 | `memory-seam:read:context` | `acting_for` must equal the issue-bound owner subject and `identity_subject` must equal the invoking Hermes profile/service subject | `metadata_only`, exact descriptor/source/query refs, `max_operation_count=1`, `report_safe_output` | `agent=sax` or the future explicitly issue-bound Hermes agent, not inherited by other agents | fresh approval only, expiry present, stale approval denied | `SUPERVISED_METADATA_CONTEXT_READ_RETRY` | auth-held until service/provider binding exists |
| `recall` | exact supervised metadata recall retry after L6AK safe 403 | `memory-seam:read:recall` | `acting_for` must equal the issue-bound owner subject and `identity_subject` must equal the invoking Hermes profile/service subject | `metadata_only`, exact recall query refs, no broad family/workspace/index expansion, `max_operation_count=1`, `report_safe_output` | `agent=sax` or the future explicitly issue-bound Hermes agent, not inherited by other agents | fresh approval only, expiry present, stale approval denied | `SUPERVISED_METADATA_RECALL_READ_RETRY` | auth-held until service/provider binding exists |
| `health` | readiness/denial posture check only, never item retrieval | `memory-seam:read:health` | `acting_for` and `identity_subject` required when the health check would narrow a supervised retry context | `metadata_only`, no item retrieval, no raw provider payload, no callback | exact issue-bound agent or no supervised retry readiness claim | freshness required for retry-readiness classification; otherwise health remains posture-only | `SUPERVISED_METADATA_HEALTH_AUTH_POSTURE` | safe to report posture, not sufficient for retry execution |

## Required service/provider auth fields

A future exact supervised metadata read retry can be classified `AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY` only if a non-secret service/provider auth contract proves every field below without broadening trust boundaries:

- `route_audience`: exactly one endpoint audience, such as `memory-seam:read:context`, `memory-seam:read:recall`, or posture-only `memory-seam:read:health`.
- `acting_for`: the owner/principal on whose behalf the supervised retry is being attempted; it must match the fresh issue-bound approval subject.
- `identity_subject`: the invoking service/profile identity; missing identity denies before read.
- `scope`: metadata-only, report-safe output, exact target/query refs, max one operation, no source discovery, no workspace/family scan, no index query, no broad recall.
- `agent`: exact future issue-bound agent identity; current Sax rail authority does not become standing authority for another Hermes profile or provider.
- `expiry`: explicit approval expiry and freshness check; stale approval, missing expiry, copied text, merge events, labels, issue closure, or old parent receipts deny before read.
- `evidence_class`: one of `SUPERVISED_METADATA_CONTEXT_READ_RETRY`, `SUPERVISED_METADATA_RECALL_READ_RETRY`, or `SUPERVISED_METADATA_HEALTH_AUTH_POSTURE`, never raw/private/source content.

## Default-deny matrix

Each case must deny before source/provider/backend/callback/read behavior and return report-safe metadata only:

| Case | Required denial reason | Boundary preserved |
| --- | --- | --- |
| wrong audience | `wrong_route_audience` | no endpoint fallback or cross-route narrowing |
| unauthorized narrowing | `unauthorized_narrowing` | no acting-for/scope substitution |
| missing identity | `missing_identity_subject` | no anonymous service/provider read |
| stale approval | `stale_approval` | no reuse of historical owner comments or L6AK/L6AA/L6AC read receipts |
| broadened scope | `broadened_scope_denied` | no broad recall, source discovery, workspace/family scan, index query, or more than one operation |
| raw-output request | `raw_output_denied` | no raw private content, raw source text, raw approval prose, private paths, source URIs, platform IDs, backend payloads, prompts, queries, credentials, auth values, tokens, OAuth material, keychain material, environment values, auth-file material, or private correlation refs |
| provider/callback/write/Gate movement | `held_surface_requested` | no provider callback invocation, no provider route execution, no write/custody/delete/reindex/rollback/cache-purge, no persistence, no service activation, no cron change, no publication, no visibility change, no provider/prod/canary/Gate movement, no Atlas Gate movement |
| broad allow | `broad_allowed_true_denied` | no `allowed=true` or standing authorization path |

## Report-safe receipt vocabulary

Auth-ready receipt vocabulary:

- `AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY`: all required non-secret service/provider bindings are present, fresh, exact, metadata-only, one-operation, issue-bound, and endpoint-specific. This still does not execute a read by itself; it only permits a separately issue-bound retry packet to be prepared.
- `AUTH_HELD_SERVICE_PROVIDER_BINDING_INCOMPLETE`: one or more service/provider binding fields are missing or unverifiable without secrets/live/private reads; retry remains held.
- `FIX_AUTH_MATRIX_BEFORE_READINESS_DECISION`: the matrix, fixture, or contract evidence is inconsistent and must be corrected before #352 readiness classification.

Report-safe denial receipt fields may include endpoint label, audience label, denial reason, freshness status, evidence class, guarded zero counters, `read_authorized=false`, `retry_executed=false`, and `items=[]`. They must not include raw item content, raw approval prose, credential/auth material, provider payloads, callback payloads, source URIs, private paths, platform raw IDs, token-like values, Runtime Registry payloads, or private correlation refs.

## Acceptance and verification gate

L6AL.01 is complete when this matrix and its contract test are committed, discoverable from the docs index and contract-test inventory, and the following commands pass:

- `python -m pytest -q tests/test_l6al01_service_provider_auth_capability_matrix.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`

Residual holds after this packet: no secret/env/keychain/OAuth/auth-file/credential reads; no live/private read retry; no source discovery; no broad recall/index queries; no Runtime Registry consumption; no provider callback invocation; no service activation; no cron changes; no persistence/mutation/write/delete/reindex/rollback/cache-purge; no publication/visibility/provider/prod/canary/Gate movement; no Atlas Gate movement; no broad `allowed=true` behavior.
