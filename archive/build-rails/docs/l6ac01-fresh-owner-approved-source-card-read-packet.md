# L6AC.01 fresh owner-approved source-card read packet

Status: `FRESH_OWNER_APPROVED_PACKET_ONLY_NO_LIVE_READS`
Rail issue: #261
Bound approval/read issue: #262
Parent issue: #6
Source floor: `67a1a78db2b7adca0048497cce61412de13032f1`
Parent successor comment: `issuecomment-4651509390`
Issue-bound prep comment: `issuecomment-4651509094`
Exact max-one read approval comment: `issuecomment-4651509226`
Approval comment author: `jeremyknows` / `OWNER`

## Purpose

This L6AC.01 packet prepares the exact descriptor/source-card target refs and denial-before-read fixture requirements for the next issue-bound execution slice. It is docs/tests/fixtures only. No live/private read is executed by #261, no source-card callback is invoked, and no raw private content or approval text is recorded.

This packet is not itself the live-read execution. The only candidate execution issue is #262, and #262 may proceed only from approval comment `4651509226` on #262, only while fresh under the rail expiry, and only when it matches the executable refs below. This packet cannot be copied, broadened, moved to another issue, or reused after expiry.

## Exact issue-bound executable refs

The #262 read gate must require matching exact executable descriptor/source-card target refs:

- packet_issue_id: `#261`
- bound_approval_read_issue_id: `#262`
- parent_issue_id: `#6`
- approval_comment_id_required: `4651509226`
- approval_comment_author_required: `jeremyknows`
- owner_actor_association: `OWNER`
- subject: `jeremyknows/memory-seam`
- audience: `L6AC owner-approved report-safe source-card read`
- scope: `one report-safe source-card read`
- operation_class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`
- max_operation_count: `1`
- expiry_window: `<=12h from #262 owner comment timestamp`
- descriptor_ref_shape: `descriptor:l6ac/<report-safe-slug>`
- source_card_ref_shape: `source-card:l6ac/<report-safe-slug>`
- exact_executable_descriptor_ref: `descriptor:l6ac/report-safe-operator-preference-card`
- exact_executable_source_card_ref: `source-card:l6ac/report-safe-operator-preference-card`
- source_floor_requirement: `67a1a78db2b7adca0048497cce61412de13032f1 or later`

The descriptor ref and source-card ref are intentionally same-slug, report-safe metadata targets. They do not encode source URIs, private paths, platform IDs, prompt/query payloads, credential material, raw private source content, or private correlation refs.

## Denial-before-read matrix

Approval recognition must inspect public issue-comment metadata only; it must not echo raw approval text. #262 must deny before read unless every bound approval and executable-ref field matches. Required denial shapes:

- approval absent on #262: `DENY_BEFORE_READ`
- approval comment id is not `4651509226`: `DENY_BEFORE_READ`
- approval stale or outside <=12h expiry: `DENY_BEFORE_READ`
- copied approval text or copied packet text: `DENY_BEFORE_READ`
- broadened operation class or max-operation count: `DENY_BEFORE_READ`
- mismatched issue, subject, audience, scope, descriptor ref, or source-card ref: `DENY_BEFORE_READ`
- non-owner or missing owner actor association: `DENY_BEFORE_READ`
- unsafe target refs or raw/private target values: `DENY_BEFORE_READ`
- any request for discovery, workspace/family scan, broad recall, index query, credentials, Runtime Registry, persistence, activation, publication, provider/prod/canary/Gate movement, mutation, rollback, cache purge, or `allowed=true`: `DENY_BEFORE_READ`

## Report-safe receipt/output fields for the next slice

If #262 later executes the approved max-one operation, its report must remain metadata/value only and may expose only bounded receipt fields such as:

- receipt_status
- approval_result
- live_read_invoked
- allowed
- allowed_result_count
- operation_count_attempted
- descriptor_ref
- source_card_ref
- read_usefulness_label
- redaction_status
- guarded_counters
- unsafe_raw_fields_rejected_before_report

#261 itself keeps the prep counters at zero:

- approval_comments_examined: `0` in #261
- valid_owner_approval_comments: `0` in #261
- provider_callbacks: `0` in #261
- backend_callbacks: `0` in #261
- source_stat_callbacks: `0` in #261
- source_read_callbacks: `0` in #261
- credential_reads: `0` in #261
- runtime_registry_reads: `0` in #261
- persistence_writes: `0` in #261
- mutation_callbacks: `0` in #261
- rollback_callbacks: `0` in #261
- cache_purge_callbacks: `0` in #261

## Preserved holds

- no live/private reads in #261
- no raw private content
- no credential/auth/env/keychain/OAuth/auth-file reads
- no source discovery, workspace scans, family scans, broad recall, or index queries
- no Runtime Registry consumption
- no provider/backend/source-stat/source-read callbacks in #261
- no persistence, mutation, write, delete, reindex, cache-purge, rollback, audit/custody writes, or cache mutation
- no service/listener/startup/cron activation or global runtime config mutation
- no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement
- no broad `allowed=true` route

## Residual holds for #262

#262 remains bounded to at most one `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` operation under exact issue-bound approval comment `4651509226`. It must stop before read on stale, copied, broadened, mismatched, unsafe, non-owner, missing-ref, callback-requesting, discovery-requesting, credential-requesting, Runtime-Registry-requesting, persistence-requesting, activation-requesting, publication-requesting, provider/prod/canary/Gate-moving, mutation/requesting, rollback/cache-purge-requesting, second-read, or broad-allow variants.
