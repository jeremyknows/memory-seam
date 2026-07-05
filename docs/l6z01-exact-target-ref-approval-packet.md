# L6Z.01 exact target-ref approval packet and executable ref fixtures

Status: `TARGET_REF_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION`
Rail issue: #231
Bound approval/read issue: #232
Parent issue: #6
Source floor: `c7e335bf6b68e084088c6deaa4b28dd84f9ed9f6`
Prerequisite: L6Y #225 / PR #230 merged.
Parent L6Z rail receipt: `issuecomment-4650001541`
Preauthorization proof anchors: #6 comment `4649391691`; #215 comment `4649391836`; Jeremy voice-message anchor recorded for the bounded L6Z rail.

This packet is docs/tests/fixture-only. It defines the exact executable target refs that #232 must compare against before any supervised report-safe source-card read attempt. No live/private read is executed by #231. #231 does not call providers, backends, source-stat, source-read, credential/auth/env/keychain/OAuth/auth-file, Runtime Registry, persistence, mutation, write, delete, reindex, rollback, cache-purge, service, listener, startup, cron, publication, repository-visibility, provider/prod/canary, or Atlas Gate surfaces.

## Non-approval rule

This packet is not approval and cannot be copied or reused as approval. Approval recognition for #232 must inspect only a fresh issue-bound owner comment on #232. Issue bodies, this packet, PR bodies, merge events, labels, closures, unrelated comments, copied snippets, stale comments, broad phrases, approval-looking summaries, or status reports do not authorize a read.

raw grant phrase required: `ABSENT_FROM_PACKET`. The intentionally absent owner phrase may exist only in a future #232 owner comment if Jeremy chooses to provide one; this packet uses safe field names, exact target refs, and denial labels only.

## Exact #232 target binding fields

#232 may proceed only from a fresh owner comment on #232 that supplies every field below exactly and without broadening. The binding is to exactly one issue and max one report-safe source-card read:

- bound_approval_issue_id: `#232`
- packet_issue_id: `#231`
- owner_actor_association: `OWNER`
- subject: `jeremyknows/memory-seam`
- audience: `L6Z exact target-ref one-read retry`
- scope: `one report-safe source-card read`
- operation_class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`
- max_operation_count: `1`
- expiry_window: `<=12h from #232 owner comment timestamp`
- descriptor_ref_shape: `descriptor:l6z/<report-safe-slug>`
- source_card_ref_shape: `source-card:l6z/<report-safe-slug>`
- exact_executable_descriptor_ref: `descriptor:l6z/report-safe-operator-preference-card`
- exact_executable_source_card_ref: `source-card:l6z/report-safe-operator-preference-card`
- request_packet_ref: `docs/l6z01-exact-target-ref-approval-packet.md`
- source_floor_requirement: `c7e335bf6b68e084088c6deaa4b28dd84f9ed9f6 or later`
- preauth_anchor_refs: #6 comment `4649391691`, #215 comment `4649391836`, Jeremy voice-message anchor recorded for the bounded L6Z rail (public-safe redacted here)
- receipt_contract: report-safe metadata only, no raw private source content or raw approval text
- stop_condition_contract: deny before callback/read for any absent, invalid, stale, copied, broadened, expired, mismatched, unsafe, or non-owner approval shape
- rollback_behavior: stop before side effects; if no side effects occurred, report `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`

## Synthetic executable target-ref fixture

Committed fixture values for #232 comparison are public-safe metadata only:

| fixture field | exact value |
| --- | --- |
| `fixture_status` | `SYNTHETIC_REPORT_SAFE_TARGET_REFS_ONLY` |
| `descriptor_ref` | `descriptor:l6z/report-safe-operator-preference-card` |
| `source_card_ref` | `source-card:l6z/report-safe-operator-preference-card` |
| `slug` | `report-safe-operator-preference-card` |
| `metadata_only` | `true` |
| `report_safe` | `true` |
| `raw_private_content_present` | `false` |
| `live_read_executed_by_packet` | `false` |
| `approval_granted_by_packet` | `false` |

Unsafe target values are rejected before any read or callback:

- descriptor/source-card refs outside the `l6z` namespace: `DENY_BEFORE_READ`
- descriptor/source-card refs with different slugs: `DENY_BEFORE_READ`
- missing descriptor or source-card ref: `DENY_BEFORE_READ`
- private absolute paths: `DENY_BEFORE_READ`
- source URIs: `DENY_BEFORE_READ`
- raw platform IDs: `DENY_BEFORE_READ`
- raw prompt/query payloads: `DENY_BEFORE_READ`
- raw payload content: `DENY_BEFORE_READ`
- raw backend responses: `DENY_BEFORE_READ`
- private correlation refs: `DENY_BEFORE_READ`
- credentials, auth/env/keychain material, OAuth material, or auth-file material: `DENY_BEFORE_READ`
- raw approval text: `DENY_BEFORE_READ`
- broad `allowed=true` route: `DENY_BEFORE_READ`

## Required #232 denial-before-read outcomes

#232 must deny before any live/private read, source discovery, workspace scan, family scan, broad recall, index query, provider/backend/source-stat/source-read callback, Runtime Registry consumption, credential/auth read, persistence, mutation, activation, publication, visibility change, provider/prod/canary action, Atlas Gate movement, rollback execution, cache-purge execution, or broad `allowed=true` route for all of these shapes:

- absent approval comment on #232: `DENY_BEFORE_READ`
- copied packet text: `DENY_BEFORE_READ`
- stale approval outside expiry: `DENY_BEFORE_READ`
- mismatched issue id: `DENY_BEFORE_READ`
- broadened operation class: `DENY_BEFORE_READ`
- broadened operation count: `DENY_BEFORE_READ`
- expired approval: `DENY_BEFORE_READ`
- non-owner or missing owner actor association: `DENY_BEFORE_READ`
- unsafe or missing descriptor/source-card refs: `DENY_BEFORE_READ`
- mismatched executable descriptor/source-card refs: `DENY_BEFORE_READ`
- missing source floor or preauth-anchor references: `DENY_BEFORE_READ`
- callback-requesting approval variant: `DENY_BEFORE_READ`
- credential/auth/Runtime-Registry requesting variant: `DENY_BEFORE_READ`
- persistence/audit/custody/cache mutation requesting variant: `DENY_BEFORE_READ`
- activation/publication/visibility/provider/prod/canary/Gate variant: `DENY_BEFORE_READ`
- mutation/rollback/cache-purge variant: `DENY_BEFORE_READ`
- any broad `allowed=true` variant: `DENY_BEFORE_READ`

If any field is absent, invalid, stale, copied, broadened, expired, mismatched, or unsafe, #232 must deny before read with guarded counters zero and produce a report-safe HOLD. If and only if all exact #232 approval fields are present, fresh, owner-bound, safe, and exactly match this packet's executable refs, #232 may attempt exactly one supervised report-safe source-card read and report only safe metadata.

## Report-safe metadata shape

Any #232 receipt or HOLD proof must report only safe metadata fields:

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

## Synthetic zero counters for #231 and any #232 deny-before-read HOLD

This #231 packet performs no approval scan and no live attempt, so all counters are synthetic zeros:

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

- no live/private reads in #231
- no raw private content
- no credential/auth/env/keychain/OAuth/auth-file reads
- no source discovery, workspace scans, family scans, broad recall, or index queries
- no Runtime Registry consumption
- no provider/backend/source-stat/source-read callbacks in #231
- no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation
- no service/listener/startup/cron activation or global runtime config mutation
- no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement
- no broad `allowed=true` route

## Completion boundary

Completion of #231 means only that the #232 issue-bound target packet and exact executable refs are documented and tested. It does not approve or execute a live/private read. #232 remains blocked unless a separate, fresh, exact owner approval comment appears on #232, is within expiry, matches every binding field above including both executable refs, and remains report-safe. Otherwise #232 must deny before read with guarded counters zero and preserve all holds.
