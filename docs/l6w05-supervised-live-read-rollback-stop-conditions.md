# L6W.05 rollback and stop-condition proof for future supervised live read

Status: `ROLLBACK_STOP_PROOF_ONLY_NO_APPROVAL_NO_EXECUTION`

Parent: #6
Rail issue: #203
Prerequisite: #202 closed/PASS
Source floor: `9264533` or later on `origin/main`
Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`
Scaffold dependency: `docs/l6w01-supervised-live-read-approval-packet-scaffold.md`
Denial dependency: `docs/l6w02-supervised-live-read-approval-denial-matrix.md`
Receipt dependency: `docs/l6w03-supervised-live-read-receipt-output-contract.md`
No-live smoke dependency: `docs/l6w04-supervised-live-read-approval-no-live-smoke.md`

This packet is docs/tests-only rollback and stop-condition evidence for a future supervised live-read attempt. It does not approve, recognize, implement, or execute any live/private read. It records reversible and containable stop classes that a later implementation must evaluate before provider/backend/source-stat/source-read callbacks and before source discovery, Runtime Registry consumption, credential/auth/env/keychain/OAuth/auth-file reads, persistence/audit/custody/cache writes, activation, publication, visibility change, provider/prod/canary authority, Atlas Gate movement, mutation execution, rollback execution, cache-purge execution, or any `allowed=true` route.

## Required stop invariant

Every stop class in this packet has the same safe result:

- `approval_result`: `DENIED_BEFORE_CALLBACK`
- `status`: `STOPPED_ROLLBACK_NOT_REQUIRED_NO_SIDE_EFFECTS`
- `live_read_invoked`: `false`
- `allowed`: `false`
- `allowed_result_count`: `0`
- `rollback_required`: `false`
- `rollback_executed`: `false`
- `cache_purge_executed`: `false`
- `guarded_callback_counters`: synthetic zeros for provider, backend, source-stat, source-read, write, custody, delete, reindex, rollback, and cache-purge families
- `source_discovery_counter`: `0`
- `runtime_registry_consumption_counter`: `0`
- `credential_auth_read_counter`: `0`
- `persistence_record_counter`: `0`
- `audit_record_counter`: `0`
- `custody_record_counter`: `0`
- `cache_mutation_counter`: `0`
- `activation_counter`: `0`
- `publication_or_visibility_counter`: `0`
- `provider_prod_canary_counter`: `0`
- `atlas_gate_movement_counter`: `0`

Because the stop happens before side effects, rollback is containable as `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`. A later implementation may only report that no persisted receipt, audit record, custody record, source cache, Runtime Registry state, service/listener/startup/cron activation, provider/backend action, source-stat/source-read callback, mutation, rollback, cache purge, publication, visibility change, production action, or Atlas Gate movement occurred. The recovery action is to remain held, discard the synthetic in-memory candidate, and require a fresh future issue-bound owner review when applicable.

## Stop-condition matrix

| Stop class | Required stop reason | Reversibility / containment proof |
| --- | --- | --- |
| `denial_before_callback` | `DENIED_BEFORE_CALLBACK` | evaluate approval and receipt safety before all provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks; rollback not required because counters remain zero |
| `approval_expired_or_missing` | `MISSING_OR_EXPIRED_APPROVAL` | hold until a fresh future issue-bound owner approval is provided; stale/missing approval is discarded from in-memory candidate state only |
| `approval_binding_mismatch` | `BOUND_FIELD_MISMATCH` | stop on issue, actor, owner, subject, audience, scope, operation class, max-count, or expiry mismatch; no retry or broadening without fresh review |
| `approval_variant_or_stale_source` | `STALE_VARIANT_OR_COPIED_APPROVAL` | reject variants, stale rail comments, copied unrelated approvals, labels, merge events, branch names, PR bodies, or issue closure as non-approval; no callback has been reached |
| `report_hygiene_failure` | `REPORT_HYGIENE_FAILURE` | suppress unsafe receipt output before echoing raw approval text, raw private source text, private paths, source URIs, platform IDs, prompts/queries, payloads, backend responses, private correlation refs, credentials, or auth material |
| `operator_revocation` | `OPERATOR_REVOKED_APPROVAL` | stop immediately on a future owner revocation signal; the one-operation candidate is invalidated before callback and requires a new future approval |
| `scope_broadened_or_allowed_true` | `BROADENED_SCOPE_OR_ALLOWED_TRUE` | deny broadened source access, source discovery, workspace scans, family scans, broad recall, index queries, multi-operation requests, positive allowed results, or any `allowed=true` route |
| `callback_or_mutation_requested` | `CALLBACK_OR_MUTATION_REQUESTED` | deny provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callback requests, mutation execution, rollback execution, and cache purge before counters increment |
| `registry_activation_or_production_requested` | `REGISTRY_ACTIVATION_OR_PRODUCTION_REQUESTED` | deny Runtime Registry consumption, activation/config mutation, publication, visibility change, provider/prod/canary authority, or Atlas Gate movement before any external or persistent action |

## Rollback ledger for future receipts

A future report-safe receipt for any stopped attempt may include only these rollback-safe fields:

- `rollback_status`: `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`
- `stop_reason`: one of the matrix labels above
- `operation_count`: `0`
- `max_operation_count`: `1`
- `allowed`: `false`
- `allowed_result_count`: `0`
- `callbacks_invoked`: `false`
- `live_read_invoked`: `false`
- `source_discovery_attempted`: `false`
- `runtime_registry_consumed`: `false`
- `persistence_attempted`: `false`
- `mutation_attempted`: `false`
- `production_authority_claimed`: `false`
- `guarded_counters_zero`: `true`
- synthetic zero guarded counters only

The receipt must not echo raw approval text, raw source content, private paths, source URIs, raw platform IDs, raw prompts/queries, raw payload content, raw backend responses, private correlation refs, credentials, auth/env/keychain/OAuth/auth-file material, Runtime Registry data, audit/custody/cache record bodies, or operator-local filesystem details.

## Non-approval carry-forward

This rollback/stop packet is `NO_APPROVAL_PRESENT`. It is not an approval request, not an approval grant, and not a live-read implementation. Merge events, labels, issue closure, branch names, PR text, copied text, stale approvals, variant wording, broadened comments, non-owner comments, and future comments outside the exact future approval issue remain non-approval. Future supervised live-read execution remains held unless a separate future issue-bound owner approval explicitly binds the exact operation class `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`, max-one-operation scope, expiry no later than 12 hours, report-safe receipt fields, zero-discovery expectation, stop conditions, rollback posture, and denial-before-callback behavior.
