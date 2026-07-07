# L6X.01 exact one-read approval request packet

Status: `REQUEST_PACKET_ONLY_NO_APPROVAL_NO_EXECUTION`
Rail issue: #211
Bound future attempt issue: #212
Parent issue: #6
Source floor: `1a6d20e4ca10acb03dc9ffd8a4b678c950b8c41b`
Prerequisite: PR #210 / L6W.06 merged.

This packet is docs/tests-only. It defines the exact future owner-comment binding that #212 must inspect before any supervised report-safe source-card live read attempt. This packet does not approve, recognize, simulate, execute, or prepare a live/private read. It does not call providers, backends, source-stat, source-read, credentials, Runtime Registry, persistence, mutation, rollback, cache-purge, service, listener, startup, cron, publication, provider/prod/canary, repository visibility, or Atlas Gate surfaces.

## Non-approval rule

This packet is a request template only; it is not an owner approval comment. No text in this file can be copied, merged, labeled, closed, or reused as approval. Approval recognition must read only a fresh owner comment on #212 and must reject packet text, issue body text, PR body text, merge events, labels, stale comments, copied comments, unrelated issues, broadened scopes, callback requests, activation requests, provider/prod/canary requests, publication requests, visibility requests, Atlas Gate requests, mutation requests, rollback requests, cache-purge requests, or any `allowed=true` wording.

raw grant phrase required: `ABSENT_FROM_PACKET`. The intentionally absent owner phrase belongs only in a future #212 owner comment if Jeremy chooses to provide one; this file uses decision labels and field names only.

## Exact future binding fields

A #212 attempt may proceed only if a fresh owner comment on #212 supplies all fields exactly and without broadening:

- bound_issue_id: `#212`
- owner_actor_association: `OWNER`
- subject: `jeremyknows/memory-seam`
- audience: `L6X supervised one-read attempt`
- operation_class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`
- max_operation_count: `1`
- expiry_window: `<=12h from owner comment timestamp`
- descriptor_ref_shape: `descriptor:l6x/<report-safe-slug>`
- source_card_ref_shape: `source-card:l6x/<report-safe-slug>`
- request_packet_ref: `docs/l6x01-one-read-approval-request-packet.md`
- receipt_contract: report-safe metadata only, no raw private source content or raw approval text
- rollback_behavior: stop before side effects; if no side effects occurred, report `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`

## Required denial-before-read preflight outcomes

#212 must deny before any live/private read, source discovery, callback, Runtime Registry consumption, credential/auth read, persistence, mutation, activation, publication, visibility, provider/prod/canary, Atlas Gate movement, rollback execution, cache-purge execution, or `allowed=true` route for all of these shapes:

- copied packet text: `DENY_BEFORE_READ`
- stale comment outside expiry: `DENY_BEFORE_READ`
- mismatched issue id: `DENY_BEFORE_READ`
- broadened operation class or count: `DENY_BEFORE_READ`
- missing owner actor association: `DENY_BEFORE_READ`
- non-owner actor association: `DENY_BEFORE_READ`
- missing or unsafe descriptor/source-card ref: `DENY_BEFORE_READ`
- callback-requesting approval variant: `DENY_BEFORE_READ`
- credential/auth/Runtime-Registry requesting variant: `DENY_BEFORE_READ`
- persistence/audit/custody/cache mutation requesting variant: `DENY_BEFORE_READ`
- activation/publication/visibility/provider/prod/canary/Gate variant: `DENY_BEFORE_READ`
- mutation/rollback/cache-purge variant: `DENY_BEFORE_READ`
- any `allowed=true` variant: `DENY_BEFORE_READ`

If denial occurs, #212 must produce synthetic zero counters and a HOLD proof rather than executing a read.

## Report-safe receipt fields for #212

Any #212 receipt or HOLD proof must report only safe metadata:

- `receipt_status`
- `approval_result`
- `live_read_invoked`
- `allowed`
- `allowed_result_count`
- `descriptor_ref`
- `source_card_ref`
- `operation_class`
- `operation_count_attempted`
- `rollback_status`
- `guarded_counters`
- `unsafe_raw_fields_rejected_before_report`
- stop-condition status such as `DENIED_BEFORE_CALLBACK`
- rollback status such as `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`

The report must reject or omit unsafe report fields: raw private source text, credentials, auth/env/keychain material, OAuth material, auth-file material, raw platform IDs, private absolute paths, raw prompt/query payloads, raw payload content, raw backend responses, private correlation refs, source URIs, raw approval text.

## Synthetic zero counters for this packet and deny-before-read HOLDs

This #211 packet performs no live attempt, so all counters are synthetic zeros:

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

- no live/private reads
- no source discovery, workspace scans, family scans, broad recall, or index queries
- no credential/auth/env/keychain/OAuth/auth-file reads
- no provider/backend/source-stat/source-read callbacks
- no write/custody/delete/reindex/rollback/cache-purge callbacks
- no persistence, audit/custody writes, or cache mutation
- no service/listener/startup/cron activation or global runtime config mutation
- no package publication, repository visibility change, provider/prod/canary authority, or Atlas Gate movement
- no `allowed=true` route

## Completion boundary

Completion of #211 means only that the future #212 approval-request binding is documented and tested. It leaves actual one-read execution held unless #212 contains a separate, fresh, exact owner approval comment that passes every field above within the expiry window. If that approval is absent, invalid, stale, copied, mismatched, or broadened, #212 must produce a no-live deny-before-read HOLD proof with synthetic zero counters.
