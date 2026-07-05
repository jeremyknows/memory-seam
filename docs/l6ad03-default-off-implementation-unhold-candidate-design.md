# L6AD.03 default-off implementation unhold candidate design and rollback plan

Status: `PASS_DESIGN_PACKET_READY_IMPLEMENTATION_NOT_APPROVED`

Rail issue: #273  
Parent issue: #6  
Rail starting source floor: `f606ed18737d057f0b544503c2532935a9d6c258`  
Source floor entering slice: `5157d40a5903ba54129b61ad5c8417df467300c8`  
Parent successor comment: `4651958877`  
Issue-bound authorization: #273 owner-created issue body and owner comment `4651958732`  
Prerequisite decision packet: [`l6ad02-implementation-or-hold-decision-packet.md`](l6ad02-implementation-or-hold-decision-packet.md)

L6AD.03 is a docs/tests/design-only unhold candidate packet. It refines the future default-off implementation shape, allowed repo-relative touch targets, rollback plan, test gates, stop conditions, and exact future approval wording. It does not implement code/runtime behavior, execute a source-card read, consume Runtime Registry, touch credentials/auth material, perform callbacks, mutate persistence, activate services, change cron schedules, publish, move provider/prod/canary state, move Atlas Gate, or create broad `allowed=true` behavior.

## Design result

Result: `PASS_DEFAULT_OFF_IMPLEMENTATION_CANDIDATE_READY_IMPLEMENTATION_NOT_APPROVED`.

Meaning:

- `PASS`: L6AD.02 found the evidence floor ready for a future exact owner-created implementation issue; L6AD.03 now packages the candidate design and rollback envelope for that later issue.
- `DEFAULT-OFF`: Any future implementation must deny by default unless an exact, fresh, issue-bound OWNER approval matches the operation class, issue number, file envelope, expiry, and residual holds.
- `NOT APPROVAL`: This packet is not itself implementation authority, runtime execution authority, read authority, Gate authority, or deployment authority.
- `NEXT`: The next L6AD rail issue is #274, a no-live trust-boundary review over #271-#273 before any implementation authority can be granted.

## Future implementation candidate name

Future issue title shape:

`L6AD.N: default-off report-safe source-card value adapter implementation slice`

Future operation class:

`L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON`

The candidate implementation should be a narrow adapter skeleton that accepts fixture/report-safe inputs and returns report-safe value metadata only. It must not add a live/private source-read path, source discovery, workspace or family scans, broad recall, index query, Runtime Registry consumption, provider/backend/source-stat/source-read callbacks, persistence/mutation/write/delete/reindex/cache-purge/rollback execution, service/global activation, publication, provider/prod/canary movement, Atlas Gate movement, cron changes, or broad `allowed=true` behavior.

## Future allowed repo-relative touch targets

These are candidate future touch targets only. L6AD.03 authorizes no implementation edits to them now, and a later owner-created issue must bind the exact final list before work begins.

Allowed in the future implementation slice:

- `src/memory_seam/l6ad_report_safe_source_card_value_adapter.py` — new module containing a default-off, fixture-only adapter skeleton, explicit denial reasons, report-safe output schema, and guarded zero side-effect counters.
- `src/memory_seam/__init__.py` — optional export only if the future issue requires an importable package symbol; no startup, service, registry, provider, or Gate wiring.
- `tests/test_l6ad_report_safe_source_card_value_adapter.py` — targeted unit tests for default-off denial, exact approval matching, expired/stale/copied/broadened/non-owner denial, report-safe output, and all guarded counters remaining zero.
- `docs/l6ad-future-default-off-adapter-implementation-receipt.md` — optional future receipt describing the implementation slice, checks, rollback instructions, and residual holds after merge.
- `docs/README.md` — discoverability row only for the optional future receipt.
- `docs/contract-test-inventory.md` — contract inventory row only for the future targeted test.

Explicitly excluded unless a separate later owner approval narrows and authorizes them:

- examples, CLI entry points, release/package publishing files, cron/schedule files, service/listener/startup files, provider adapters, runtime registry code, source-discovery code, workspace/family scan code, broad recall/index-query code, persistence/custody/audit/write/delete/reindex/cache-purge code, rollback executors, publication/visibility controls, production/provider/canary controls, and Atlas Gate files.

The future implementation must not use a production/read-source clone as a write target and must not write or cache private content, source content, approval text, platform identifiers, paths, prompts, payloads, backend responses, credentials, auth material, or private correlation references.

## Default-off approval contract

The future implementation should expose an explicit approval contract object or function parameter rather than reading credentials, environment, keychain, OAuth material, auth files, GitHub comments, issue text, Runtime Registry, or any private source. Tests should pass fixture values directly.

Required approval fields:

- repository: `jeremyknows/memory-seam`;
- issue number: exact future owner-created implementation issue;
- actor association: `OWNER`;
- operation class: `L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON`;
- max slices: exactly one;
- approved file envelope: exact repo-relative list named by the future issue;
- expiry: fresh UTC timestamp;
- deny flags for live/private reads, source discovery, Runtime Registry, callbacks, persistence/mutation, activation, publication, provider/prod/canary/Gate movement, cron changes, and broad `allowed=true` behavior.

Deny before any adapter action if approval is missing, stale, copied from prior issue, expired, broadened, mismatched to repo/issue/operation/files, non-owner, permits more than one slice, permits any held surface, requests callbacks, requests Runtime Registry, requests persistence/mutation, requests service activation, requests publication/provider/prod/canary/Gate movement, changes cron/schedule behavior, or attempts broad `allowed=true`.

## Report-safe fixture-only behavior

The future adapter should accept only committed fixture/report-safe input shaped like:

- public descriptor reference string;
- public source-card reference string;
- usefulness label;
- booleans for exact approval match and default-off denial;
- integer counters for guarded held surfaces, all expected to stay zero;
- report-safe status strings.

The future adapter output should contain only:

- `status` such as `DENIED_DEFAULT_OFF`, `PASS_REPORT_SAFE_VALUE_ADAPTER_FIXTURE_ONLY`, or `HOLD_FOR_OWNER_DECISION`;
- public descriptor/source-card refs;
- usefulness labels;
- denial reason codes;
- booleans and integer counters;
- residual hold labels.

The future adapter output must never include raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain/OAuth/auth-file material, source locations, platform identifiers, prompts, queries, payload bodies, backend responses, private correlation references, or secret values.

## Future exact owner approval wording

A future implementation issue should use this exact approval sentence shape, filling only the placeholders with the future issue number, exact merged L6AD.03 source floor, exact allowed files, and a fresh UTC expiry:

`I approve exactly one Memory Seam default-off implementation slice for issue #<future_issue>: L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON. Scope is limited to source floor <source_floor_after_l6ad03>, repository jeremyknows/memory-seam, and these repo-relative files only: <exact_file_list>. The implementation must be fixture-only and default-off unless this exact approval matches the future issue, OWNER actor, operation class, file envelope, and unexpired UTC window. No live/private reads, raw private content, additional source-card reads, credentials/auth/env/keychain/OAuth/auth-file reads, source discovery, workspace/family scans, broad recall, index query, Runtime Registry consumption, callbacks, persistence/mutation/write/delete/reindex/cache-purge/rollback execution, service/global activation, cron changes, publication, provider/prod/canary/Gate movement, Atlas Gate movement, or broad allowed=true behavior are authorized. Approval expires at <UTC timestamp>.`

This wording is inert documentation in #273. It must be copied into a later owner-created implementation issue by an OWNER before it can bind any implementation work.

## Future targeted tests

A future implementation issue must add `tests/test_l6ad_report_safe_source_card_value_adapter.py` with cases proving:

- missing approval denies with `DENIED_DEFAULT_OFF` and all guarded counters zero;
- stale source floor, stale issue number, copied prior rail wording, broadened file envelope, expired UTC window, mismatched operation class, mismatched repository, non-owner actor, and max-slice count greater than one deny before any adapter action;
- attempts to authorize live/private reads, raw private content, additional source-card reads, credentials/auth/env/keychain/OAuth/auth-file reads, source discovery, workspace/family scans, broad recall, index queries, Runtime Registry consumption, callbacks, persistence/mutation/write/delete/reindex/cache-purge/rollback execution, service/global activation, cron changes, publication, provider/prod/canary/Gate movement, Atlas Gate movement, or broad `allowed=true` deny before any held surface;
- exact valid fixture-only approval returns report-safe metadata and labels only;
- output rejects unsafe raw/private/credential/source-location/platform/prompt/query/payload/backend/correlation material;
- all callback/source/provider/registry/persistence/mutation/write/custody/delete/reindex/rollback/cache-purge counters remain zero.

Required future verification gate:

- `python -m pytest tests/test_l6ad_report_safe_source_card_value_adapter.py -q`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`

## Rollback plan for the future issue

Rollback must be limited to the future implementation PR:

1. Revert the single future implementation merge commit or PR.
2. Remove `src/memory_seam/l6ad_report_safe_source_card_value_adapter.py` and any optional export in `src/memory_seam/__init__.py`.
3. Remove `tests/test_l6ad_report_safe_source_card_value_adapter.py` and optional future receipt/docs inventory rows created by that future PR.
4. Confirm no service, provider, registry, cron, publication, persistence, Gate, or activation files were touched; if they were touched, stop for owner decision rather than executing rollback machinery.
5. Run `python -m pytest -q`, `python scripts/public_hygiene_scan.py`, `git diff --check`, and `python -m compileall -q src tests examples`.

Rollback execution itself remains held in L6AD.03; this section is a plan only, not permission to mutate runtime state, persistence, cache, indexes, deployment, provider controls, or Gate state.

## Stop conditions

Stop and hold for owner decision if any future implementation attempt:

- asks for a live/private read, any additional source-card read, raw private content, raw source text, or raw approval prose;
- asks to read credentials, auth material, environment variables, keychain, OAuth material, or auth files;
- asks for source discovery, workspace/family scans, broad recall, index query, Runtime Registry consumption, callbacks, persistence, mutation, write/delete/reindex/cache-purge, rollback execution, service/global activation, cron changes, publication, provider/prod/canary movement, Atlas Gate movement, or broad `allowed=true` behavior;
- cannot remain fixture-only, report-safe, and default-off;
- expands beyond the exact future owner-approved file envelope;
- fails targeted pytest, full pytest, hygiene scan, whitespace diff check, compileall, or GitHub PR checks.

## Residual holds after L6AD.03

The following remain held after this design packet:

- implementation/runtime execution until a separate exact owner-created future implementation issue approval exists;
- live/private reads and any additional source-card read beyond the consumed historical #262 evidence;
- raw private content, raw source text, raw approval prose, credentials, auth material, env/keychain/OAuth/auth-file reads;
- source discovery, workspace scans, family scans, broad recall, and index queries;
- Runtime Registry consumption;
- provider/backend/source-stat/source-read callbacks;
- persistence, mutation, audit/custody writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation;
- service/listener/startup/global activation and recursive cron/schedule changes;
- publication, visibility changes, provider/prod/canary authority, and Atlas Gate movement;
- broad `allowed=true` behavior.

## Next issue

Next open rail issue after #273: #274 `L6AD.04: no-live trust-boundary review for implementation-or-hold rail`.

#274 should review #271-#273 no-live artifacts, confirm #262 approval remains consumed and not reusable, verify no implementation/runtime/private-read/persistence/provider/prod/canary/Gate movement occurred in L6AD, and classify the next frontier without performing implementation.
