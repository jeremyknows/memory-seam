# L6AK.02 route-audience auth binding for supervised metadata read

Status: `PASS_ROUTE_AUDIENCE_AUTH_BINDING_DESIGNED_RETRY_STILL_HELD`

Rail issue: #342
Parent issue: #6
Depends on: #341 closed/PASS safe 403 receipt
Roadmap step: 3 supervised real read with denial-before-read, auth blocker points toward step 5 service/provider auth
Rail starting source floor: `95e7a7979ae092703da8f77c4d897f703348a308`
Source floor entering slice: `407a80a`
Prior receipt: #341 / PR #345
Operation class: `L6AK_ROUTE_AUDIENCE_AUTH_BINDING_DESIGN`
Evidence class: `SUPERVISED_METADATA_READ_ROUTE_AUDIENCE_AUTH_CONTRACT`

## Verdict

Verdict vocabulary: `PASS_ROUTE_AUDIENCE_AUTH_BINDING_DESIGNED_RETRY_STILL_HELD`, `FIX_AUTH_CONTRACT_BEFORE_IMPLEMENTATION`, `DENY_BEFORE_READ_FOR_BINDING_MISMATCH`.
Verdict: `PASS_ROUTE_AUDIENCE_AUTH_BINDING_DESIGNED_RETRY_STILL_HELD`
Next-frontier classification: `NON_SECRET_AUTH_CONTRACT_SHIM_OR_TYPED_RECEIPT_IMPLEMENTATION_BEFORE_RETRY`

This design consumes only the #341 safe 403 receipt, committed repo docs/tests, public issue/PR/source-floor metadata, and report-safe denial labels. It performs no live read retry and reads no credentials, auth files, environment values, keychain entries, OAuth material, raw/private content, source cards, source URIs, platform raw IDs, Runtime Registry payloads, callback payloads, provider payloads, or private source identifiers.

## Binding contract

A future exact supervised metadata-only retry may proceed only if a non-secret contract proves all of these bindings before source access:

| Binding | Required value/semantics | Denial if absent or mismatched |
| --- | --- | --- |
| `identity_subject` | the authenticated service principal or caller subject is explicitly present as a non-secret label | `missing_identity_subject` or `mismatched_identity_subject` |
| `acting_for` | `sax` is explicitly represented as the supervised acting agent | `mismatched_agent` |
| `agent` | request agent is exactly `sax` | `mismatched_agent` |
| `audience` | route audience is exactly the Memory Seam supervised metadata-read audience for atlas-query MCP | `wrong_route_audience` |
| `scope` | recall scope is exactly `wiki`; context include is exactly `health` for the health check path | `broadened_scope` or `unauthorized_narrowing` |
| `output_mode` | metadata-only/report-safe receipt fields only | `raw_output_requested` |
| `approval_freshness` | approval/rail authority is fresh, issue-bound, and not copied from stale evidence | `stale_approval` |
| `operation_count` | max one exact supervised metadata read retry after implementation is verified | `broadened_scope` |

The contract must default-deny. It must return a metadata-only denial receipt before read when any binding is missing, stale, broadened, mismatched, or raw-output requesting.

## Denial-before-read matrix

| Case | Required outcome | Source access |
| --- | --- | --- |
| wrong route audience | deny with `wrong_route_audience` before read | none |
| unauthorized narrowing | deny with `unauthorized_narrowing` before read | none |
| stale approval | deny with `stale_approval` before read | none |
| mismatched agent | deny with `mismatched_agent` before read | none |
| broadened scope | deny with `broadened_scope` before read | none |
| raw-output request | deny with `raw_output_requested` before read | none |
| missing identity subject | deny with `missing_identity_subject` before read | none |
| all exact bindings present | may return `ready_for_exact_retry=true` as non-secret readiness only, not execute the retry | none in #342 |

## Report-safe retry capability matrix

| Future retry prerequisite | #342 status |
| --- | --- |
| #341 safe 403 receipt merged | satisfied |
| Non-secret route-audience contract defined | satisfied by this design |
| Code shim or typed receipt implementation | blocked pending #343 |
| Targeted denial-before-read tests for wrong audience and unauthorized narrowing | specified here; implementation pending #343 |
| Exact retry authorization after verified auth binding | held |
| Broader reads or source discovery | forbidden |
| Raw/private/source/auth material output | forbidden |
| Runtime Registry/callback/provider payload consumption | forbidden |
| Persistence, mutation, write/delete/reindex/cache-purge/rollback | forbidden |
| Service activation, cron change, publication, provider/prod/canary/Gate, Atlas Gate movement | forbidden |

## Handoff to #343

#343 may implement the smallest non-secret contract shim or typed receipt behavior needed to validate the bindings above. It must not load secrets, read environment/auth/keychain/OAuth/auth-file material, activate services, call providers, consume Runtime Registry data, retry the real read, create broad `allowed=true` behavior, or write/mutate outside repo docs/tests/code.

## Verification gate

Required verification for the #342 PR:

- `python -m pytest -q tests/test_l6ak02_route_audience_auth_binding.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`
