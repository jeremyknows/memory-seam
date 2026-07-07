# L6AG.03 default-off integration candidate design and rollback plan

Status: `PASS_DESIGN_PACKET_READY_RUNTIME_INTEGRATION_NOT_APPROVED`

Rail issue: #303  
Parent issue: #6  
Blocked by: #301-#302 closed/PASS  
Rail starting source floor: `b7fe89f752372de4f42d5f7e1084acad99c5ebf0`  
Source floor entering slice: `1ff55c0056248162b7726f966f7a5a31e9a8241f`  
Parent successor comment: `4653805965`  
Issue-bound design authorization: #303 owner-created issue body and owner comment `4653805892`  
Prerequisite decision packet: [`l6ag02-runtime-integration-or-continued-hold-decision-packet.md`](l6ag02-runtime-integration-or-continued-hold-decision-packet.md)  
Historical runtime-use smoke approval consumed by L6AF.02: #292 comment `4653350823`

Decision vocabulary: `PASS_DESIGN_PACKET_READY`, `FIX_BEFORE_DESIGN_PACKET`, `HOLD_FOR_OWNER_DECISION`  
Decision: `PASS_DESIGN_PACKET_READY`

L6AG.03 is a docs/tests/design-only default-off runtime-integration candidate and rollback/stop-condition plan. It refines the future exact issue-bound runtime-integration slice shape, allowed repo-relative touch targets, fixture/live input boundary, report-safe output contract, max operation count, denial-before-callback behavior, rollback plan, stop conditions, and residual held surfaces. It does not implement runtime integration, wire adapters into runtime routes, execute another adapter call or smoke, perform live/private reads, read source cards, inspect raw private content/source text/approval prose, read credentials/auth/env/keychain/OAuth/auth-file material, perform source discovery/workspace/family scans/broad recall/index queries, consume Runtime Registry data, invoke callbacks/provider routes, persist or mutate state, write/delete/reindex/cache-purge, execute rollback, activate services/listeners/startup/global routes, create or modify cron automation, publish or change visibility, move provider/prod/canary/Gate or Atlas Gate state, or introduce broad `allowed=true` behavior.

## Design result

Result: `PASS_DEFAULT_OFF_RUNTIME_INTEGRATION_CANDIDATE_READY_RUNTIME_INTEGRATION_NOT_APPROVED`.

Meaning:

- `PASS`: L6AG.02 found public post-smoke evidence ready for a design-only future integration candidate; L6AG.03 now packages that design and rollback envelope.
- `DEFAULT-OFF`: Any future integration must deny by default unless an exact, fresh, issue-bound OWNER approval matches the operation class, issue number, source floor, file envelope, expiry, and residual holds.
- `NOT APPROVAL`: This packet is not runtime-integration authority, implementation authority, another adapter-call or smoke authority, live/private-read authority, Runtime Registry/callback/provider-route authority, persistence/mutation authority, activation authority, cron authority, publication/provider/prod/canary/Gate authority, Atlas Gate authority, or broad `allowed=true` authority.
- `NEXT`: The next L6AG rail issue is #304, a no-live trust-boundary review over #301-#303 before any integration authority can be granted.

## Future runtime-integration candidate name

Future issue title shape:

`L6AG.N: default-off report-safe adapter runtime-integration slice`

Future operation class:

`L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE`

The candidate integration should be a narrow default-off shim that proves a package-level runtime can accept report-safe fixture values from the existing adapter boundary without live/private reads, source-card reads, callbacks, Runtime Registry consumption, persistence, activation, provider routes, cron changes, Gate movement, or broad `allowed=true` behavior. The historical #292 fixture-only adapter runtime-use smoke is evidence only; it is consumed and cannot authorize another call, smoke, or integration path.

## Future allowed repo-relative touch targets

These are candidate future touch targets only. L6AG.03 authorizes no implementation edits to them now, and a later owner-created issue must bind the exact final list before work begins.

Allowed in the future integration slice:

- `src/memory_seam/l6ag_default_off_runtime_integration.py` — new module containing a default-off runtime-integration shim, explicit approval object, denial reasons, report-safe output schema, max-operation accounting, and guarded zero held-surface counters.
- `src/memory_seam/__init__.py` — optional export only if the future issue requires an importable package symbol; no startup, listener, service, registry, provider, callback, or Gate wiring.
- `tests/test_l6ag_default_off_runtime_integration.py` — targeted unit contract for missing/stale/copied/broadened/mismatched/expired/non-owner approval denial, no extra smoke, report-safe outputs, max-operation count, and all guarded counters remaining zero.
- `docs/l6ag-future-default-off-runtime-integration-receipt.md` — optional future receipt describing the implementation slice, checks, rollback instructions, and residual holds after merge.
- `docs/README.md` — discoverability row only for the optional future receipt.
- `docs/contract-test-inventory.md` — contract inventory row only for the future targeted test.

Explicitly excluded unless a separate later owner approval narrows and authorizes them:

- examples, CLI entry points, release/package publishing files, cron/schedule files, service/listener/startup files, provider adapters, Runtime Registry code, source-discovery code, workspace/family scan code, broad recall/index-query code, persistence/custody/audit/write/delete/reindex/cache-purge code, rollback executors, publication/visibility controls, production/provider/canary controls, Atlas Gate files, and any Atlas Gate movement hooks.

The future integration must not use a production/read-source clone as an input or write target and must not write, cache, or echo private content, source content, approval prose, platform identifiers, source locations, prompts, payloads, backend responses, credentials, auth material, or private correlation references.

## Future approval contract

The future integration should expose an explicit approval contract object or function parameter rather than reading credentials, environment values, keychain material, OAuth material, auth files, GitHub comments, issue text, Runtime Registry state, provider routes, callbacks, workspace indexes, family scans, or any private source. Tests should pass committed fixture values directly.

Required approval fields:

- repository: `jeremyknows/memory-seam`;
- issue number: exact future owner-created runtime-integration issue;
- actor association: `OWNER`;
- operation class: `L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE`;
- source floor: exact source floor after L6AG.03 and any #304/#305 prerequisite reconciliation that the future issue names;
- max operation count: exactly one integration slice and zero extra runtime-use smokes unless separately and exactly approved in that same future issue;
- approved file envelope: exact repo-relative list named by the future issue;
- expiry: fresh UTC timestamp;
- denied-surface flags for live/private reads, source-card reads, raw private/source/approval material, credential/auth/env/keychain/OAuth/auth-file reads, discovery/scans/broad recall/index queries, Runtime Registry consumption, callbacks/provider routes, persistence/mutation/write/delete/reindex/cache-purge/rollback execution, service/listener/startup/global activation, cron changes, publication/visibility/provider/prod/canary/Gate movement, Atlas Gate movement, and broad `allowed=true` behavior.

Deny before any adapter action, provider route, Runtime Registry read, callback, persistence, activation, live/private read, source-card read, source discovery, cron change, Gate movement, or broad allow result if approval is missing, stale, copied from prior issue, expired, broadened, mismatched to repo/issue/source-floor/operation/files, non-owner, permits more than one slice, permits another smoke, permits any held surface, requests callbacks, requests Runtime Registry, requests persistence/mutation, requests service activation, requests publication/provider/prod/canary/Gate movement, changes cron/schedule behavior, or attempts broad `allowed=true`.

## Fixture/live input boundary choices

Future implementation inputs should be limited to committed fixture/report-safe values shaped like:

- public descriptor reference string;
- public adapter value reference string or already-safe value label;
- operation class and approval metadata fields listed above;
- booleans for exact approval match, default-off denial, and runtime integration attempted;
- integer max-operation and guarded held-surface counters, all expected to stay zero except a future explicit `integration_slice_count` that may be `1` only under exact approval;
- report-safe status and denial-code strings.

Live/private inputs remain held. The future integration must not request or accept live source text, source-card content, source locations, platform identifiers, prompts, queries, payload bodies, backend responses, credentials, auth material, Runtime Registry state, callbacks, provider route handles, or private correlation references.

## Report-safe output contract

The future integration output should contain only:

- `status` such as `DENIED_DEFAULT_OFF`, `PASS_DEFAULT_OFF_RUNTIME_INTEGRATION_FIXTURE_ONLY`, or `HOLD_FOR_OWNER_DECISION`;
- public descriptor/value refs and operation-class refs;
- denial reason codes;
- booleans for approval matched, default-off denied, live adapter invoked, callback invoked, registry consumed, persistence attempted, activation attempted, and broad allow attempted;
- integer counters for `integration_slice_count`, `runtime_use_smoke_count`, provider/backend/source-stat/source-read/callback/registry/persistence/mutation/write/custody/delete/reindex/rollback/cache-purge/service/cron/publication/Gate families;
- max-operation metadata;
- residual hold labels.

The future output must never include raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain/OAuth/auth-file material, source locations, platform identifiers, prompts, queries, payload bodies, backend responses, private correlation references, secret values, or broad `allowed=true` as an authorization result.

## Future exact owner approval wording

A future runtime-integration issue should use this exact approval sentence shape, filling only the placeholders with the future issue number, exact source floor after L6AG.03/#304/#305 prerequisites, exact allowed files, and a fresh UTC expiry:

`I approve exactly one Memory Seam default-off runtime-integration slice for issue #<future_issue>: L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE. Scope is limited to source floor <source_floor_after_l6ag03_and_prerequisites>, repository jeremyknows/memory-seam, and these repo-relative files only: <exact_file_list>. The implementation must be fixture-only, report-safe, and default-off unless this exact approval matches the future issue, OWNER actor, operation class, file envelope, max operation count, and unexpired UTC window. No additional runtime-use smoke or adapter call beyond what this exact issue separately names, no live/private reads, source-card reads, raw private content, raw source text, raw approval prose, credentials/auth/env/keychain/OAuth/auth-file reads, source discovery, workspace/family scans, broad recall, index query, Runtime Registry consumption, callbacks/provider routes, persistence/mutation/write/delete/reindex/cache-purge/rollback execution, service/listener/startup/global activation, cron changes, publication, visibility changes, provider/prod/canary/Gate movement, Atlas Gate movement, or broad allowed=true behavior are authorized. Approval expires at <UTC timestamp>.`

This wording is inert documentation in #303. It must be copied into a later owner-created runtime-integration issue by an OWNER before it can bind any implementation work. L6AG.03 itself is not approval. No live/private reads, source-card reads, raw private content, raw source text, raw approval prose, credentials, discovery, callbacks, Registry use, persistence, activation, cron changes, Gate movement, or broad `allowed=true` behavior are authorized by this design packet.

## Future targeted tests

A future implementation issue must add `tests/test_l6ag_default_off_runtime_integration.py` with cases proving:

- missing approval denies with `DENIED_DEFAULT_OFF` and all guarded counters zero;
- stale source floor, stale issue number, copied prior rail wording, broadened file envelope, expired UTC window, mismatched operation class, mismatched repository, non-owner actor, max-operation count greater than one, and extra-smoke permission deny before any adapter action;
- attempts to authorize live/private reads, source-card reads, raw private content, raw source text, raw approval prose, credentials/auth/env/keychain/OAuth/auth-file reads, source discovery, workspace/family scans, broad recall, index queries, Runtime Registry consumption, callbacks/provider routes, persistence/mutation/write/delete/reindex/cache-purge/rollback execution, service/listener/startup/global activation, cron changes, publication, visibility changes, provider/prod/canary/Gate movement, Atlas Gate movement, or broad `allowed=true` deny before any held surface;
- exact valid fixture-only approval returns report-safe metadata and labels only, with `integration_slice_count=1` and `runtime_use_smoke_count=0` unless the exact future issue separately authorizes a smoke;
- output rejects unsafe raw/private/credential/source-location/platform/prompt/query/payload/backend/correlation material;
- all provider/backend/source-stat/source-read/callback/registry/persistence/mutation/write/custody/delete/reindex/rollback/cache-purge/service/cron/publication/Gate counters remain zero;
- `live_adapter_invoked=false`, `callback_invoked=false`, `registry_consumed=false`, `persistence_attempted=false`, `activation_attempted=false`, and `broad_allowed_attempted=false` in report-safe outputs.

Required future verification gate:

- `python -m pytest tests/test_l6ag_default_off_runtime_integration.py -q`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`

## Rollback plan for the future issue

Rollback must be limited to the future runtime-integration PR:

1. Revert the single future runtime-integration merge commit or PR.
2. Remove `src/memory_seam/l6ag_default_off_runtime_integration.py` and any optional export in `src/memory_seam/__init__.py`.
3. Remove `tests/test_l6ag_default_off_runtime_integration.py` and optional future receipt/docs inventory rows created by that future PR.
4. Confirm no examples, CLI, service, listener, startup, provider adapter, Runtime Registry, cron, publication, persistence, mutation, rollback executor, Gate, Atlas Gate, or activation files were touched; if they were touched, stop for owner decision rather than executing rollback machinery.
5. Run `python -m pytest -q`, `python scripts/public_hygiene_scan.py`, `git diff --check`, and `python -m compileall -q src tests examples`.

Rollback execution itself remains held in L6AG.03; this section is a plan only, not permission to mutate runtime state, persistence, cache, indexes, deployment, provider controls, or Gate state.

## Stop conditions

Stop and hold for owner decision if any future runtime-integration attempt:

- asks for runtime integration not exactly bound by a fresh owner-created issue approval;
- asks for another runtime-use smoke or adapter call outside the exact future issue envelope;
- asks for a live/private read, source-card read, raw private content, raw source text, or raw approval prose;
- asks to read credentials, auth material, environment variables, keychain material, OAuth material, or auth files;
- asks for source discovery, workspace/family scans, broad recall, index query, Runtime Registry consumption, callbacks/provider routes, persistence, mutation, write/delete/reindex/cache-purge, rollback execution, service/listener/startup/global activation, cron changes, publication, visibility changes, provider/prod/canary movement, Gate movement, Atlas Gate movement, or broad `allowed=true` behavior;
- cannot remain fixture-only, report-safe, default-off, denial-before-callback, and no-live by default;
- expands beyond the exact future owner-approved file envelope;
- fails targeted pytest, full pytest, hygiene scan, whitespace diff check, compileall, or GitHub PR checks.

## Residual holds after L6AG.03

The following remain held after this design packet:

- runtime integration and adapter wiring until a separate exact owner-created future runtime-integration issue approval exists;
- any additional runtime-use smoke or adapter call beyond #292's consumed one-smoke approval;
- live/private reads and any source-card reads;
- raw private content, raw source text, raw approval prose, credentials, auth material, env/keychain/OAuth/auth-file reads;
- source discovery, workspace scans, family scans, broad recall, and index queries;
- Runtime Registry consumption;
- provider/backend/source-stat/source-read callbacks and provider routes;
- persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation;
- service/listener/startup/global activation and recursive cron/schedule changes;
- publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement;
- broad `allowed=true` behavior.

## Next issue

Next open rail issue after #303: #304 `L6AG.04: no-live trust-boundary review for post-smoke integration rail`.

#304 should review #301-#303 no-live artifacts, confirm #292 approval remains consumed and not reusable, verify no L6AG runtime integration, additional adapter call/smoke, private read, Runtime Registry consumption, callback, persistence, activation, cron change, publication/provider/prod/canary/Gate movement, Atlas Gate movement, or broad `allowed=true` behavior occurred, and classify the next frontier without implementing integration.
