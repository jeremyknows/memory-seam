# L6AL.04 supervised metadata read retry readiness decision

Status: `RAIL_PASS_AUTH_CONTRACT_READY_RUNTIME_RETRY_AUTH_HELD`

Rail issue: #352
Parent issue: #6
Depends on: L6AL.01-L6AL.03 closed/PASS
Roadmap step: 5 service/provider auth decision for a future Step 3 exact supervised metadata read retry
Rail starting source floor: `f335f09891a41f43583fbf434482cfb096a04fcd`
Decision source floor entering slice: `a5c87db`
Decision class: `SUPERVISED_METADATA_RETRY_READINESS_DECISION`

## Decision

L6AL produced the repo-side, non-secret service/provider auth contract needed to distinguish auth-ready, auth-held, and denied-before-read states. That is enough to prepare operator/service configuration handoff language, but it is not enough to open a live/private exact supervised metadata read retry from this rail.

Decision: `AUTH_CONTRACT_READY_RUNTIME_RETRY_AUTH_HELD`.

The retry remains held because this cron rail did not and must not verify external runtime/service/provider configuration, read secrets, inspect environment/auth files/keychains/OAuth material, activate a service, invoke a provider route, invoke callbacks, consume Runtime Registry data, or perform a live/private read retry. The prior L6AK Step 3 raw usefulness proof remains incomplete because the bounded attempt returned `auth_status_code=403`, `items=[]`, `wrong_route_audience`, and `unauthorized_narrowing`.

## Evidence consumed

| Rail | Issue / PR | Receipt | Evidence |
| --- | --- | --- | --- |
| L6AL.01 | #349 / #353 | `PASS_CAPABILITY_MATRIX_READY_RETRY_STILL_HELD` | Endpoint capability matrix for Memory Seam `context`, `recall`, and `health`, required route-audience/acting-for/identity/scope/agent/expiry/evidence fields, default-deny cases, report-safe auth-ready/auth-held vocabulary. |
| L6AL.02 | #350 / #354 | `PASS_PROVIDER_AUTH_READINESS_FIXTURE_READY_RETRY_STILL_HELD` | No-live provider auth readiness fixture with authorized metadata-read readiness shape, denied-before-read auth mismatch fixtures, zero source-item/read-callback/provider-callback counters, and explicit `wrong_route_audience` / `unauthorized_narrowing` coverage. |
| L6AL.03 | #351 / #355 | `PASS_MINIMAL_SERVICE_AUTH_CONTRACT_READY_RETRY_STILL_HELD` | Typed non-secret `ServiceAuthContract` for `context`, `recall`, and `health`, auth-ready vs auth-held receipts, default-deny mismatch receipts, receipt-safe output, `read_authorized=false`, `retry_executed=false`, `items=[]`, and zero guarded counters. |

## What is ready

- Repo code/docs/tests now define a report-safe contract vocabulary for `AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY`, `AUTH_HELD_SERVICE_PROVIDER_BINDING_INCOMPLETE`, and denied-before-read mismatch receipts.
- The contract can classify exact non-secret labels for `context`, `recall`, and `health` route audiences.
- Default-deny cases are covered for wrong route audience, unauthorized narrowing, missing/mismatched identity, stale approval, broadened scope, raw output, unsafe payload keys, unknown endpoints, service/provider binding gaps, and broad `allowed=true` attempts.
- Tests prove exact readiness remains metadata-only and does not authorize or execute a read.
- Tests prove auth mismatches deny before source access with zero source/callback/provider/secret/Registry counters.

## Blocker before an exact live retry rail

A future exact supervised metadata read retry remains blocked until an operator/service configuration handoff can provide, without broadening trust boundaries:

1. exact service/provider identity binding for the selected endpoint audience;
2. exact `acting_for`, `identity_subject`, `agent`, `scope`, `expiry`, and `evidence_class` labels matching the L6AL.03 contract;
3. assurance that the service route will use the exact Memory Seam audience and will not fall back across endpoints;
4. assurance that callback/provider execution remains absent until the retry rail explicitly authorizes one max-one metadata-only read;
5. a fresh issue-bound retry packet naming source/query/output/denial cases and stop conditions.

This blocker is service/operator configuration readiness, not repo contract absence. L6AL.03 gives the acceptance shape; it does not prove runtime credentials or activate the provider.

## Next issue packet when operator/service config is ready

Do not open this as an executable retry until the blocker above is satisfied. The smallest next packet should be shaped as:

- Title: `L6AM.01: exact supervised metadata read retry after service auth binding`
- Parent: #6
- Depends on: L6AL #349-#352 closed/PASS and a fresh operator/service auth-binding approval comment.
- Scope: one max-one metadata-only supervised Memory Seam retry, issue-bound to the selected endpoint (`recall` preferred if the operator approval names the prior `wiki` query; otherwise exact endpoint named by the approval).
- Required input labels: `route_audience`, `acting_for`, `identity_subject`, `agent`, `scope`, `expiry`, `evidence_class`, exact query/source label, output envelope, stop conditions, denial-before-read cases.
- Required denial cases: `wrong_route_audience`, `unauthorized_narrowing`, missing/mismatched identity, stale approval, broadened scope, raw-output request, service/provider binding missing, callback/provider movement requested, Runtime Registry requested, and broad `allowed=true`.
- Required output: report-safe receipt only; `items=[]` if denied; if allowed, metadata-only item fields with no raw/private/source/auth/provider/callback payloads.
- Boundary: no source discovery, no broad recall/index queries, no secret/env/keychain/OAuth/auth-file/credential reads, no provider/prod/canary/Gate movement, no service activation from the issue runner, no writes/mutations.

## Parent #6 and tracker update receipt

After merge, parent #6 and the Atlas tracker should record:

- L6AL #349-#352 closed/PASS, PRs #353-#356 merged.
- Final L6AL source floor from the merge commit.
- Verification summary: targeted #352 pytest, full pytest, public hygiene scan, git diff --check, compileall, and GitHub checks py3.10/3.11/3.12.
- Roadmap step 5 state: `AUTH CONTRACT READY / RUNTIME RETRY AUTH HELD`.
- Roadmap step 3 state remains `AUTH BLOCKER RECONCILED / RAW USEFULNESS PROOF INCOMPLETE / RETRY HELD` until a future exact authorized retry returns items.
- Next frontier: operator/service auth binding handoff or L6AM exact retry packet only after fresh service-auth binding approval.

## Verification gate

L6AL.04 is complete when this decision packet and contract test are committed, discoverable from the docs index and contract-test inventory, parent #6 and the tracker are updated after merge, and the following commands pass:

- `python -m pytest -q tests/test_l6al04_readiness_decision.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`

Residual holds after this packet: no live/private read retry; no secret/env/keychain/OAuth/auth-file/credential reads; no source discovery; no broad recall/index queries; no Runtime Registry consumption; no provider callback invocation; no provider route execution; no service activation; no cron changes; no persistence/mutation/write/delete/reindex/rollback/cache-purge; no publication/visibility/provider/prod/canary/Gate movement; no Atlas Gate movement; no broad `allowed=true` behavior.
