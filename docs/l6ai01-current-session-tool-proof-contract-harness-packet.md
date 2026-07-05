# L6AI.01 current-session tool proof contract and harness packet

Status: `PASS_CONTRACT_PACKET_READY_NO_PROOF_EXECUTION`

Rail issue: #321
Parent issue: #6
Depends on: L6AH #311-#315 closed/PASS
Roadmap step: 2 current-session tool proof
Rail starting source floor: `9c706d0b430f64e0b3ea9fd85b220f6abcb0c497`
Source floor entering slice: `9c706d0b430f64e0b3ea9fd85b220f6abcb0c497`
Parent L6AI successor comment: `4654450317`
Issue-bound contract authorization: #321 comment `4654450209`
Future proof approval reference: #322 comment `4654450262`
Operation class: `L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF`
Exact future proof issue: #322
Verdict vocabulary: `PASS_CONTRACT_PACKET_READY_NO_PROOF_EXECUTION`, `FIX_BEFORE_PROOF`, `HOLD_FOR_OWNER_DECISION`
Verdict: `PASS_CONTRACT_PACKET_READY_NO_PROOF_EXECUTION`
Next-frontier classification: `CURRENT_SESSION_PROOF_ALLOWED_FOR_ISSUE_322_ONLY`

## Packet boundary

This #321 packet is docs/tests/fixtures/public-metadata-only. It defines the contract and harness envelope for the next issue. It does not execute the current-session proof, invoke a live/private read, read a source card, consume Runtime Registry data, invoke callbacks/provider routes, persist or mutate runtime state, start services, activate global behavior, change cron automation, publish or change visibility, move provider/prod/canary/Gate/Atlas Gate surfaces, execute writes, or introduce broad `allowed=true` behavior.

The packet may cite only report-safe public metadata: source floor, parent issue, rail issue numbers, public comment IDs, operation-class labels, evidence classes, status labels, booleans, zero held-surface counters, and repo-relative artifact paths.

Excluded report classes remain held and must not appear in the proof or this packet: raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, auth-file material, private absolute paths, source URIs, platform IDs, prompts, queries, payloads, backend responses, private correlation refs, Runtime Registry handles, provider handles, secret values, and token-like values.

## Current-session proof contract

#322 may execute exactly two current-session requests under the #322 approval, and no more:

1. One allowed no-live/report-safe current-session Memory Seam tool/shim proof for operation `L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF`.
2. One denied out-of-scope current-session request that denies before source access.

Both requests must remain in repository `jeremyknows/memory-seam`, bind source floor `9c706d0b430f64e0b3ea9fd85b220f6abcb0c497`, and produce report-safe metadata only. The allowed proof is not a broad allow route; it may emit a narrow string label such as `EXACT_NO_LIVE_CURRENT_SESSION_TOOL_PROOF`, never boolean `allowed=true`.

Expected allowed proof receipt shape:

- `status="PASS_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"`
- `operation_class="L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"`
- `source_floor="9c706d0b430f64e0b3ea9fd85b220f6abcb0c497"`
- `evidence_class="CURRENT_SESSION_TOOL_SHIM_NO_LIVE_REPORT_SAFE"`
- `allowed="EXACT_NO_LIVE_CURRENT_SESSION_TOOL_PROOF"`
- `current_session_tool_proof_count=1`
- `denied_out_of_scope_request_count=0`
- `live_private_read_count=0`
- `source_card_read_count=0`
- `raw_private_content_count=0`
- `raw_source_text_count=0`
- `raw_approval_prose_count=0`
- `credential_auth_read_count=0`
- `discovery_query_count=0`
- `runtime_registry_consumed=false`
- `callback_invoked=false`
- `persistence_or_mutation_attempted=false`
- `activation_attempted=false`
- `write_attempted=false`
- `publication_or_gate_movement_attempted=false`
- `broad_allowed_attempted=false`
- all held-surface counters zero

Expected denied request receipt shape:

- `status="DENIED_BEFORE_SOURCE_ACCESS_OUT_OF_SCOPE_CURRENT_SESSION_REQUEST"`
- `operation_class="L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"`
- `source_floor="9c706d0b430f64e0b3ea9fd85b220f6abcb0c497"`
- `evidence_class="CURRENT_SESSION_DENIAL_BEFORE_SOURCE_ACCESS"`
- `allowed=false`
- `current_session_tool_proof_count=0`
- `denied_out_of_scope_request_count=1`
- `denial_before_source_access=true`
- all held-surface counters zero

## Harness packet fields

The committed harness packet for #322 should record these public-safe fields only:

| Field | Allowed value class |
| --- | --- |
| `repo` | `jeremyknows/memory-seam` |
| `rail_issue` | public issue number #322 |
| `parent_issue` | public issue number #6 |
| `source_floor` | commit hash `9c706d0b430f64e0b3ea9fd85b220f6abcb0c497` |
| `parent_successor_comment` | public comment ID `4654450317` |
| `contract_authorization_comment` | public comment ID `4654450209` |
| `proof_approval_comment` | public comment ID `4654450262` |
| `operation_class` | `L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF` |
| `evidence_class` | safe labels only |
| `artifact_paths` | repo-relative docs/tests paths only |
| `guarded_counters` | integer zero values only unless the exact proof count or denied count is the one authorized operation |
| `held_surface_flags` | booleans proving held surfaces were not touched |

## Denial-before-source-access expectations

The denied request in #322 must deny before source access when it requests any out-of-scope surface, including: raw private content, raw source text, raw approval prose, credentials/auth/env/keychain/OAuth/auth-file reads, discovery/workspace/family scans, broad recall, index queries, live/private reads, source-card reads outside committed no-live fixture/surrogate proof, Runtime Registry consumption, callbacks/provider routes, persistence/runtime mutation/write/delete/reindex/cache-purge/rollback execution, service/global activation, cron changes, publication/provider/prod/canary/Gate/Atlas Gate movement, writes, or broad `allowed=true` behavior.

The denial receipt must not echo unsafe request details. It may include only denial labels, boolean `denial_before_source_access=true`, the operation class, the source floor, public issue/comment refs, and all-zero held-surface counters.

## Stop conditions for #322

Stop and report HOLD before execution if any step requires: raw private content; raw source text; raw approval prose; credentials/auth/env/keychain/OAuth/auth-file reads; discovery/workspace/family scans; broad recall or index queries; live/private reads; source-card reads outside a committed no-live fixture/surrogate proof; Runtime Registry consumption; callbacks/provider routes; persistence/runtime mutation/write/delete/reindex/cache-purge/rollback execution; service/global activation; cron changes; publication/provider/prod/canary/Gate/Atlas Gate movement; writes; more than one allowed proof; more than one denied request; or broad `allowed=true` behavior.

## Verification gate for #321 closeout

Before closing #321, the PR must pass:

- `python -m pytest -q tests/test_l6ai01_current_session_tool_proof_contract_harness_packet.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`

## Residual holds and next issue

Residual holds preserved: #322 proof execution until the next tick selects #322 and revalidates live issue/approval/source-floor state; any current-session proof beyond exactly one allowed no-live/report-safe proof under #322; any denied request beyond exactly one out-of-scope denial under #322; raw private content; raw source text; raw approval prose; credentials/auth/env/keychain/OAuth/auth-file reads; discovery, workspace scans, family scans, broad recall, and index queries; live/private reads; source-card reads outside committed no-live fixture/surrogate proof; Runtime Registry consumption; callbacks/provider routes; persistence, mutation, writes, delete, reindex, rollback execution, cache purge, and runtime cache mutation; service/listener/startup/global activation and recursive cron/schedule changes; publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement; and broad `allowed=true` behavior.

Next open rail issue after #321: #322 `L6AI.02: execute current-session allowed and denied no-live tool proof`.

#322 may perform exactly one allowed no-live/report-safe current-session Memory Seam tool/shim proof and exactly one denied out-of-scope current-session request only after rechecking source floor, issue state, approval comment, and parent/tracker context.
