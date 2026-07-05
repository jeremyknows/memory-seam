# L6Y.01 preauthorized one-read binding and target packet

Status: `BINDING_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION`
Rail issue: #221
Bound approval/read issue: #222
Parent issue: #6
Source floor: `e0d5b4158049870b50aa5f553f828f891716be92`
Prerequisite: L6X #215 / PR #220 merged.
Preauthorization proof anchors: #6 comment `4649391691`; #215 comment `4649391836`; Jeremy voice-message anchor recorded in the parent L6Y rail receipt (public-safe redacted here to satisfy hygiene scanning).

This packet is docs/tests-only. It binds the next possible supervised report-safe source-card read attempt to #222 and defines the target packet that #222 must compare against before any read. No live/private read is executed by #221. #221 does not call providers, backends, source-stat, source-read, credential/auth/env/keychain/OAuth/auth-file, Runtime Registry, persistence, mutation, write, delete, reindex, rollback, cache-purge, service, listener, startup, cron, publication, repository-visibility, provider/prod/canary, or Atlas Gate surfaces.

## Non-approval rule

This packet is not approval and cannot be copied or reused as approval. Approval recognition must inspect only a fresh issue-bound owner comment on #222. Issue bodies, this packet, PR bodies, merge events, labels, closures, unrelated comments, copied snippets, stale comments, broad phrases, approval-looking summaries, or status reports do not authorize a read.

raw grant phrase required: `ABSENT_FROM_PACKET`. The intentionally absent owner phrase may exist only in a future #222 owner comment if Jeremy chooses to provide one; this packet uses safe field names and denial labels only.

## Exact #222 target binding fields

#222 may proceed only from a fresh owner comment on #222 that supplies every field below exactly and without broadening. The binding is to exactly one issue and max one report-safe source-card read:

- bound_approval_issue_id: `#222`
- packet_issue_id: `#221`
- owner_actor_association: `OWNER`
- subject: `jeremyknows/memory-seam`
- audience: `L6Y supervised one-read attempt`
- scope: `one report-safe source-card read`
- operation_class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`
- max_operation_count: `1`
- expiry_window: `<=12h from #222 owner comment timestamp`
- descriptor_ref_shape: `descriptor:l6y/<report-safe-slug>`
- source_card_ref_shape: `source-card:l6y/<report-safe-slug>`
- request_packet_ref: `docs/l6y01-one-read-binding-target-packet.md`
- preauth_anchor_refs: #6 comment `4649391691`, #215 comment `4649391836`, Jeremy voice-message anchor recorded in the parent L6Y rail receipt (public-safe redacted here)
- receipt_contract: report-safe metadata only, no raw private source content or raw approval text
- stop_condition_contract: deny before callback/read for any absent, copied, stale, mismatched, broadened, expired, unsafe, or non-owner approval shape
- rollback_behavior: stop before side effects; if no side effects occurred, report `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`

## Required #222 denial-before-read outcomes

#222 must deny before any live/private read, source discovery, workspace scan, family scan, broad recall, index query, provider/backend/source-stat/source-read callback, Runtime Registry consumption, credential/auth read, persistence, mutation, activation, publication, visibility change, provider/prod/canary action, Atlas Gate movement, rollback execution, cache-purge execution, or broad `allowed=true` route for all of these shapes:

- absent approval comment on #222: `DENY_BEFORE_READ`
- copied packet text: `DENY_BEFORE_READ`
- stale approval outside expiry: `DENY_BEFORE_READ`
- mismatched issue id: `DENY_BEFORE_READ`
- broadened operation class: `DENY_BEFORE_READ`
- broadened operation count: `DENY_BEFORE_READ`
- expired approval: `DENY_BEFORE_READ`
- non-owner or missing owner actor association: `DENY_BEFORE_READ`
- unsafe or missing descriptor/source-card refs: `DENY_BEFORE_READ`
- missing source floor or preauth-anchor references: `DENY_BEFORE_READ`
- callback-requesting approval variant: `DENY_BEFORE_READ`
- credential/auth/Runtime-Registry requesting variant: `DENY_BEFORE_READ`
- persistence/audit/custody/cache mutation requesting variant: `DENY_BEFORE_READ`
- activation/publication/visibility/provider/prod/canary/Gate variant: `DENY_BEFORE_READ`
- mutation/rollback/cache-purge variant: `DENY_BEFORE_READ`
- any broad `allowed=true` variant: `DENY_BEFORE_READ`

If any field is absent, invalid, stale, copied, broadened, expired, mismatched, or unsafe, #222 must deny before read with guarded counters zero and produce a report-safe HOLD.

## Report-safe metadata shape

Any #222 receipt or HOLD proof must report only safe metadata fields:

- `receipt_status`
- `approval_result`
- `live_read_invoked`
- `allowed`
- `allowed_result_count`
- `descriptor_ref`
- `source_card_ref`
- `operation_class`
- `operation_count_attempted`
- `read_usefulness_label`
- `redaction_status`
- `rollback_status`
- `guarded_counters`
- `unsafe_raw_fields_rejected_before_report`
- stop-condition status such as `DENIED_BEFORE_CALLBACK`
- rollback status such as `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`

The report must reject or omit unsafe report fields: raw private source text, credentials, auth/env/keychain material, OAuth material, auth-file material, raw platform IDs, private absolute paths, raw prompt/query payloads, raw payload content, raw backend responses, private correlation refs, source URIs, raw approval text.

## Synthetic zero counters for #221 and any #222 deny-before-read HOLD

This #221 packet performs no approval scan and no live attempt, so all counters are synthetic zeros:

- approval_comments_examined: `0`
- valid_owner_approval_comments: `0`
- provider_callbacks: `0`
- backend_callbacks: `0`
- source_stat_callbacks: `0`
- source_read_callbacks: `0`
- credential_reads: `0`
- runtime_registry_reads: `0`
- persistence_writes: `0`
- mutation_callbacks: `0`
- rollback_callbacks: `0`
- cache_purge_callbacks: `0`

## Preserved holds

- no live/private reads in #221
- no raw private content
- no credential/auth/env/keychain/OAuth/auth-file reads
- no source discovery, workspace scans, family scans, broad recall, or index queries
- no Runtime Registry consumption
- no provider/backend/source-stat/source-read callbacks in #221
- no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation
- no service/listener/startup/cron activation or global runtime config mutation
- no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement
- no broad `allowed=true` route

## Completion boundary

Completion of #221 means only that the #222 issue-bound target packet is documented and tested. It does not approve or execute a live/private read. #222 remains blocked unless a separate, fresh, exact owner approval comment appears on #222, is within expiry, matches every binding field above, and remains report-safe. Otherwise #222 must deny before read with guarded counters zero and preserve all holds.
