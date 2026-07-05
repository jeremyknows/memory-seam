# L6AJ.01 supervised real-read exact approval packet scaffold

Status: `PASS_APPROVAL_PACKET_SCAFFOLD_READY_NO_EXECUTION`

Rail issue: #331
Parent issue: #6
Depends on: L6AI #321-#325 closed/PASS
Roadmap step: 3 supervised real read with denial-before-read
Rail starting source floor: `e7b3e67c438891be00f4001d9cfff72026ebe4d3`
Source floor entering slice: `e7b3e67c438891be00f4001d9cfff72026ebe4d3`
Parent L6AJ successor prep comment: `4654676210`
Issue-bound scaffold authorization: #331 comment `4654676115`
Future denial harness preauthorization reference: #332 comment `4654676162`
Operation class candidate: `L6AJ_SUPERVISED_REAL_READ_EXACT_APPROVAL_PREP`
Exact future execution issue: none present; execution remains held
Verdict vocabulary: `PASS_APPROVAL_PACKET_SCAFFOLD_READY_NO_EXECUTION`, `FIX_BEFORE_DENIAL_HARNESS`, `HOLD_FOR_OWNER_DECISION`
Verdict: `PASS_APPROVAL_PACKET_SCAFFOLD_READY_NO_EXECUTION`
Next-frontier classification: `DENIAL_BEFORE_READ_FIXTURE_HARNESS_ONLY_FOR_ISSUE_332`

## Packet boundary

This #331 packet is docs/tests/fixtures/public-metadata-only. It prepares exact approval semantics for a future supervised real read, but it does not execute a supervised real read, perform a live/private read, read raw private content, read raw source text, read raw approval prose, read a source card, perform source discovery, run workspace/family scans, run broad recall or index queries, read credentials/auth/env/keychain/OAuth/auth-file material, consume Runtime Registry data, invoke real callbacks/provider routes, persist or mutate state, write/delete/reindex/cache-purge/rollback execute, activate service/listener/startup/global paths, change cron automation, publish or change visibility, move provider/prod/canary/Gate or Atlas Gate surfaces, or create broad `allowed=true` behavior.

The packet may cite only report-safe public metadata: repo name, source floor, parent issue, rail issue numbers, public comment IDs, operation-class labels, evidence classes, status labels, booleans, zero held-surface counters, issue/PR refs, and repo-relative artifact paths.

Excluded report classes remain held and must not appear in this scaffold or a future receipt: raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, auth-file material, private absolute paths, source URIs, platform IDs, prompts, queries, payloads, backend responses, private correlation refs, Runtime Registry handles, provider handles, secret values, and token-like values.

## Exact future approval field scaffold

No executable approval exists in #331. A later owner-created issue/comment would have to bind all fields below before any supervised real read can execute:

| Field | Required future binding |
| --- | --- |
| `repo` | exactly `jeremyknows/memory-seam` |
| `parent_issue` | public parent issue #6 |
| `execution_issue` | one exact future owner-created issue number, not #331 |
| `owner_actor_association` | OWNER only |
| `source_identifier_class` | one explicit report-safe source identifier class, with executable refs supplied by that future issue only |
| `query_or_prompt_constraints` | report-safe intent label and output constraints only; raw prompt/query text remains held |
| `output_constraints` | metadata-only receipt fields, safe labels, booleans, counters, and usefulness classification only |
| `max_operation_count` | exactly `1` allowed supervised real read and exactly `1` denied out-of-scope request before read, if separately approved |
| `evidence_class` | `SUPERVISED_REAL_READ_REPORT_SAFE_ONE_OPERATION` or a narrower future label |
| `approval_comment_id` | fresh exact owner comment ID on the future execution issue |
| `expiry_window` | explicit created-at/expiry ceiling; stale, missing, copied, or expired approval denies before read |
| `denial_before_read_requirement` | required for missing/stale/mismatched/broadened/out-of-scope requests before source access |
| `rollback_stop_conditions` | stop before read/callback/mutation/activation on any boundary mismatch or unsafe output request |
| `residual_holds` | all held surfaces listed in this packet remain held unless named exactly by the future approval |

The future approval must be issue-bound, fresh, non-copied, non-stale, owner-authored, max-one-operation, and narrow. Merge events, labels, issue closure, source-floor advancement, parent comments, copied wording, unrelated comments, or this scaffold PASS must not authorize execution.

## Report-safe receipt shape required before any future execution issue

A future execution receipt, if separately approved, must be limited to report-safe metadata. The allowed-read receipt shape would need to include:

- `status="PASS_SUPERVISED_REAL_READ_REPORT_SAFE_ONE_OPERATION"`
- `operation_class` equal to the future approved operation class
- `source_floor` equal to the execution issue's checked floor
- `evidence_class="SUPERVISED_REAL_READ_REPORT_SAFE_ONE_OPERATION"`
- `allowed="EXACT_SUPERVISED_REAL_READ_ONE_OPERATION"`, never boolean `allowed=true`
- `supervised_real_read_count=1`
- `denied_out_of_scope_request_count=0`
- `denial_before_read=false`
- `raw_private_content_count=0`
- `raw_source_text_count=0`
- `raw_approval_prose_count=0`
- `credential_auth_read_count=0`
- `source_discovery_count=0`
- `runtime_registry_consumed=false`
- `callback_invoked=false`
- `persistence_or_mutation_attempted=false`
- `activation_attempted=false`
- `write_attempted=false`
- `publication_or_gate_movement_attempted=false`
- `broad_allowed_attempted=false`
- all non-approved held-surface counters zero

The denied out-of-scope receipt shape would need to include:

- `status="DENIED_BEFORE_READ_OUT_OF_SCOPE_SUPERVISED_REAL_READ_REQUEST"`
- `operation_class` equal to the future approved operation class or `UNAPPROVED_SUPERVISED_REAL_READ_REQUEST`
- `evidence_class="SUPERVISED_REAL_READ_DENIAL_BEFORE_READ"`
- `allowed=false`
- `supervised_real_read_count=0`
- `denied_out_of_scope_request_count=1`
- `denial_before_read=true`
- all held-surface counters zero

The denial receipt must not echo unsafe request details. It may include only denial labels, public refs, source floor, boolean posture fields, and zero counters.

## Denial-before-read requirements

A future harness must deny before source access when any request is missing exact approval fields or asks for out-of-scope surfaces, including raw private content, raw source text, raw approval prose, credentials/auth/env/keychain/OAuth/auth-file reads, source discovery, workspace scans, family scans, broad recall, index queries, source-card reads outside exact future approval, Runtime Registry consumption, real callbacks/provider routes, persistence/mutation/write/delete/reindex/cache-purge/rollback execution, service/global activation, cron changes, publication/provider/prod/canary/Gate/Atlas Gate movement, more than the exact approved operation count, or broad `allowed=true` behavior.

Denial-before-read must occur before source-card access, provider/backend/source-stat/source-read callbacks, live adapter invocation, Runtime Registry lookup, persistence, mutation, cache mutation, rollback execution, activation, publication, or Gate movement.

## Rollback and stop conditions

Stop and report HOLD before any future read if any step requires: live/private reads without a fresh exact execution approval; raw private content; raw source text; raw approval prose; credentials/auth/env/keychain/OAuth/auth-file reads; source discovery/workspace/family scans/broad recall/index queries; source-card reads without exact executable refs; Runtime Registry consumption; real callbacks/provider routes; persistence/runtime mutation/write/delete/reindex/cache-purge/rollback execution; service/listener/startup/global activation; cron changes; publication/provider/prod/canary/Gate/Atlas Gate movement; more than one allowed read; more than one denied out-of-scope request; unsafe report output; or broad `allowed=true` behavior.

Rollback is limited to stopping before the held surface is touched and reporting the safe HOLD. #331 authorizes no rollback execution, cache purge, persistence write, mutation, or cleanup callback.

## Verification gate for #331 closeout

Before closing #331, the PR must pass:

- `python -m pytest -q tests/test_l6aj01_supervised_real_read_exact_approval_packet_scaffold.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`

## Residual holds and next issue

Residual holds preserved: supervised real-read execution until a future exact owner-created execution issue/comment binds source/query/output and operation count; #332 denial-before-read harness execution until the next tick selects #332 and revalidates live issue/approval/source-floor state; any live/private read; raw private content; raw source text; raw approval prose; credentials/auth/env/keychain/OAuth/auth-file reads; source discovery, workspace scans, family scans, broad recall, and index queries; source-card reads; Runtime Registry consumption; real callbacks/provider routes; persistence, mutation, writes, delete, reindex, rollback execution, cache purge, and runtime cache mutation; service/listener/startup/global activation and recursive cron/schedule changes; publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement; and broad `allowed=true` behavior.

Next open rail issue after #331: #332 `L6AJ.02: denial-before-read fixture harness for supervised real-read prep`.

#332 may produce only a no-live fixture-only denial-before-read harness with inert spies/counters and no source access after rechecking source floor, issue state, approval comment, and parent/tracker context. #332 must not execute a supervised real read or invoke real callbacks/provider routes.
