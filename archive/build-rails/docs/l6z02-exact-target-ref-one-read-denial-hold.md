# L6Z.02 exact target-ref one-read retry denial HOLD

Status: `HOLD_DENIED_BEFORE_READ_APPROVAL_TARGET_REF_MISMATCH_NO_LIVE`
Rail issue: #232
Prerequisite packet issue: #231
Parent issue: #6
Source floor requirement: `c7e335bf6b68e084088c6deaa4b28dd84f9ed9f6 or later`
Evaluated source floor: `07ef81810809a0249fef2fd58be99cc57bce1746`
Evaluation timestamp: `2026-06-08T14:39:48Z`
Prerequisite packet: `docs/l6z01-exact-target-ref-approval-packet.md`
Preauthorization proof anchors: #6 comment `4649391691`; #215 comment `4649391836`; Jeremy voice-message anchor recorded for the bounded L6Z rail.
Parent L6Z rail receipt: `issuecomment-4650001541`

This artifact records the #232 one-read retry decision. It did not execute a live/private read. It did not call providers, backends, source-stat, source-read, credential/auth/env/keychain/OAuth/auth-file, Runtime Registry, persistence, mutation, write, delete, reindex, rollback, cache-purge, service, listener, startup, cron, publication, repository-visibility, provider/prod/canary, or Atlas Gate surfaces.

## Decision summary

#232 was allowed to attempt exactly one supervised report-safe source-card read only if the exact issue-bound owner approval comment on #232 was present, fresh, owner-bound, and matched the executable refs selected by #231.

The approval comment was present and owner-bound, but it did not match the #231 executable target refs. Therefore #232 denied before read.

Receipt status: `HOLD_DENIED_BEFORE_READ_APPROVAL_TARGET_REF_MISMATCH_NO_LIVE`
Approval result: `DENY_BEFORE_READ`
Stop condition: `DENIED_BEFORE_CALLBACK`
Rollback status: `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`
Live read invoked: `false`
Allowed: `false`
Allowed result count: `0`
Operation count attempted: `0`
Read usefulness label: `not_applicable_no_read_executed`
Redaction status: `REPORT_SAFE_METADATA_ONLY_RAW_APPROVAL_TEXT_OMITTED`

## Approval comment check

The only #232 approval-like owner comment examined was issue comment `4649997717`, authored by `jeremyknows`, with `owner_actor_association: OWNER`, created at `2026-06-08T14:25:56Z`.

The comment was fresh at evaluation time under the `<=12h from #232 owner comment timestamp` expectation, and it was issue-bound to #232. Freshness and owner association were not sufficient because the executable target refs did not match.

Report-safe extracted fields:

| field | expected from #231 packet | extracted from #232 owner comment | result |
| --- | --- | --- | --- |
| `bound_approval_issue_id` | `#232` | `#232` | `MATCH` |
| `packet_issue_id` | `#231` | `#231` | `MATCH` |
| `owner_actor_association` | `OWNER` | `OWNER` | `MATCH` |
| `subject` | `jeremyknows/memory-seam` | `jeremyknows/memory-seam` | `MATCH` |
| `operation_class` | `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` | `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` | `MATCH` |
| `max_operation_count` | `1` | `1` | `MATCH` |
| `descriptor_ref` | `descriptor:l6z/report-safe-operator-preference-card` | `descriptor:l6z/operator-proof` | `MISMATCH_DENY_BEFORE_READ` |
| `source_card_ref` | `source-card:l6z/report-safe-operator-preference-card` | `source-card:l6z/operator-proof` | `MISMATCH_DENY_BEFORE_READ` |

The #232 owner comment included an escape condition that could allow a stricter #231 slug only if the comment was updated before execution to match it. No updated #232 owner comment matching `descriptor:l6z/report-safe-operator-preference-card` and `source-card:l6z/report-safe-operator-preference-card` was present before this evaluation. That makes the approval mismatched rather than executable.

## Report-safe HOLD receipt

```text
receipt_status: HOLD_DENIED_BEFORE_READ_APPROVAL_TARGET_REF_MISMATCH_NO_LIVE
approval_result: DENY_BEFORE_READ
approval_comment_id_examined: 4649997717
approval_comment_author: jeremyknows
owner_actor_association: OWNER
approval_comment_created_at: 2026-06-08T14:25:56Z
approval_evaluated_at: 2026-06-08T14:39:48Z
freshness_result: FRESH_WITHIN_12H
packet_issue_id: #231
read_issue_id: #232
parent_issue_id: #6
descriptor_ref_expected: descriptor:l6z/report-safe-operator-preference-card
source_card_ref_expected: source-card:l6z/report-safe-operator-preference-card
descriptor_ref_presented: descriptor:l6z/operator-proof
source_card_ref_presented: source-card:l6z/operator-proof
mismatch_reason: EXECUTABLE_TARGET_REFS_DO_NOT_MATCH_L6Z01_PACKET
live_read_invoked: false
allowed: false
allowed_result_count: 0
operation_count_attempted: 0
read_usefulness_label: not_applicable_no_read_executed
redaction_status: REPORT_SAFE_METADATA_ONLY_RAW_APPROVAL_TEXT_OMITTED
stop_condition: DENIED_BEFORE_CALLBACK
rollback_status: NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED
unsafe_raw_fields_rejected_before_report: true
```

## Guarded counters

All guarded counters remained zero:

- approval_comments_examined: `1`
- valid_owner_approval_comments: `0`
- live_read_invocations: `0`
- operation_count_attempted: `0`
- allowed_result_count: `0`
- provider_callbacks: `0`
- backend_callbacks: `0`
- source_stat_callbacks: `0`
- source_read_callbacks: `0`
- credential_reads: `0`
- auth_env_keychain_oauth_auth_file_reads: `0`
- runtime_registry_reads: `0`
- source_discovery_queries: `0`
- workspace_scans: `0`
- family_scans: `0`
- broad_recall_queries: `0`
- index_queries: `0`
- persistence_writes: `0`
- mutation_callbacks: `0`
- rollback_callbacks: `0`
- cache_purge_callbacks: `0`
- service_listener_startup_activations: `0`
- publication_or_visibility_changes: `0`
- provider_prod_canary_or_gate_moves: `0`

`valid_owner_approval_comments` is zero because the only owner comment failed the executable target-ref match after #231 selected stricter target refs. The owner association itself was present; the approval did not become valid for execution.

## Report hygiene

This receipt intentionally omits raw approval text and raw private content. It reports only metadata needed to explain the denial. Unsafe report fields remain rejected or absent: raw private source text, credentials, auth/env/keychain material, OAuth material, auth-file material, raw platform IDs, private absolute paths, raw prompt/query payloads, raw payload content, raw backend responses, private correlation refs, source URIs, and raw approval text.

## Preserved holds

- no live/private read executed in #232
- no raw private content read or reported
- no credential/auth/env/keychain/OAuth/auth-file reads
- no source discovery, workspace scans, family scans, broad recall, or index queries
- no Runtime Registry consumption
- no provider/backend/source-stat/source-read callbacks
- no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation
- no service/listener/startup/cron activation or global runtime config mutation
- no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement
- no broad `allowed=true` route

## #233 handoff

#233 may verify this already-produced HOLD receipt and redaction posture. #233 must not perform an additional live/private read, callback, discovery query, Runtime Registry read, credential/auth read, persistence/mutation/write/delete/reindex/cache-purge/rollback execution, activation, publication/visibility change, provider/prod/canary/Gate movement, or broad `allowed=true` route.
