# L6AA.01 exact owner-approved target-ref packet and executable ref fixtures

Status: `TARGET_REF_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION`
Rail issue: #241
Bound approval/read issue: #242
Parent issue: #6
Source floor: `b141f7be878a5b0d136cced3beb12ef38f0a25c9`
Prerequisite: L6Z #235 / PR #240 merged.
Parent L6AA rail receipt: `issuecomment-4650524341`
Preauthorization proof anchors: #6 comment `4649391691`; #215 comment `4649391836`; Jeremy voice-message anchor recorded for the bounded L6AA rail.

This packet is docs/tests/fixture-only. It defines the exact owner-approved executable target refs that #242 must compare against before any supervised report-safe source-card read attempt. No live/private read is executed by #241. #241 does not call providers, backends, source-stat, source-read, credential/auth/env/keychain/OAuth/auth-file, Runtime Registry, persistence, mutation, write, delete, reindex, rollback, cache-purge, service, listener, startup, cron, publication, repository-visibility, provider/prod/canary, or Atlas Gate surfaces.

## Non-approval rule

This packet is not approval and cannot be copied or reused as approval. Approval recognition for #242 must inspect only a fresh issue-bound owner comment on #242. Issue bodies, this packet, PR bodies, merge events, labels, closures, unrelated comments, copied snippets, stale comments, broad phrases, approval-looking summaries, or status reports do not authorize a read.

exact owner approval phrase required: `ABSENT_FROM_PACKET`. The intentionally absent owner phrase may exist only in a future #242 owner comment if Jeremy chooses to provide one; this packet uses safe field names, exact target refs, and denial labels only.

## Exact #242 target binding fields

#242 may proceed only from a fresh owner comment on #242 that supplies every field below exactly and without broadening. The binding is to exactly one issue and max one report-safe source-card read:

- bound_approval_issue_id: `#242`
- packet_issue_id: `#241`
- owner_actor_association: `OWNER`
- subject: `jeremyknows/memory-seam`
- audience: `L6AA owner-approved target-ref live-read value proof`
- scope: `one report-safe source-card read`
- operation_class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`
- max_operation_count: `1`
- expiry_window: `<=12h from #242 owner comment timestamp`
- descriptor_ref_shape: `descriptor:l6aa/<report-safe-slug>`
- source_card_ref_shape: `source-card:l6aa/<report-safe-slug>`
- exact_executable_descriptor_ref: `descriptor:l6aa/report-safe-operator-preference-card`
- exact_executable_source_card_ref: `source-card:l6aa/report-safe-operator-preference-card`
- request_packet_ref: `docs/l6aa01-exact-owner-approved-target-ref-packet.md`
- source_floor_requirement: `b141f7be878a5b0d136cced3beb12ef38f0a25c9 or later`
- preauth_anchor_refs: #6 comment `4649391691`, #215 comment `4649391836`, Jeremy voice-message anchor recorded for the bounded L6AA rail (public-safe redacted here)
- receipt_contract: report-safe metadata only, no raw private source content or raw approval text
- stop_condition_contract: deny before callback/read for any absent, invalid, stale, copied, broadened, expired, mismatched, unsafe, or non-owner approval shape
- rollback_behavior: stop before side effects; if no side effects occurred, report `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`

## Synthetic executable target-ref fixture

Committed fixture values for #242 comparison are public-safe metadata only:

| fixture field | exact value |
| --- | --- |
| `fixture_status` | `SYNTHETIC_REPORT_SAFE_TARGET_REFS_ONLY` |
| `descriptor_ref` | `descriptor:l6aa/report-safe-operator-preference-card` |
| `source_card_ref` | `source-card:l6aa/report-safe-operator-preference-card` |
| `slug` | `report-safe-operator-preference-card` |
| `metadata_only` | `true` |
| `report_safe` | `true` |
| `raw_private_content_present` | `false` |
| `live_read_executed_by_packet` | `false` |
| `approval_granted_by_packet` | `false` |

Unsafe target values are rejected before any read or callback:

- descriptor/source-card refs outside the `l6aa` namespace: `DENY_BEFORE_READ`
- stale copied L6Z proof refs such as `descriptor:l6z/operator-proof` or `source-card:l6z/operator-proof`: `DENY_BEFORE_READ`
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

## Required #242 denial-before-read outcomes

#242 must deny before any live/private read, source discovery, workspace scan, family scan, broad recall, index query, provider/backend/source-stat/source-read callback, Runtime Registry consumption, credential/auth read, persistence, mutation, activation, publication, visibility change, provider/prod/canary action, Atlas Gate movement, rollback execution, cache-purge execution, or broad `allowed=true` route for all of these shapes:

- absent approval comment on #242: `DENY_BEFORE_READ`
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

If any field is absent, invalid, stale, copied, broadened, expired, mismatched, or unsafe, #242 must deny before read with guarded counters zero and produce a report-safe HOLD. If and only if all exact #242 approval fields are present, fresh, owner-bound, safe, and exactly match this packet's executable refs, #242 may attempt exactly one supervised report-safe source-card read and report only safe metadata.

## Report-safe metadata shape

Any #242 receipt or HOLD proof must report only safe metadata fields:

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

## Synthetic zero counters for #241 and any #242 deny-before-read HOLD

This #241 packet performs no approval scan and no live attempt, so all counters are synthetic zeros:

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

- no live/private reads in #241
- no raw private content
- no credential/auth/env/keychain/OAuth/auth-file reads
- no source discovery, workspace scans, family scans, broad recall, or index queries
- no Runtime Registry consumption
- no provider/backend/source-stat/source-read callbacks in #241
- no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation
- no service/listener/startup/cron activation or global runtime config mutation
- no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement
- no broad `allowed=true` route

## Completion boundary

Completion of #241 means only that the #242 issue-bound target packet and exact executable refs are documented and tested. It does not approve or execute a live/private read. #242 remains blocked unless a separate, fresh, exact owner approval comment appears on #242, is within expiry, matches every binding field above including both executable refs, and remains report-safe. Otherwise #242 must deny before read with guarded counters zero and preserve all holds.
