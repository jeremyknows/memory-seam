# L6W.02 supervised live-read approval stale/variant denial matrix

Status: `DENIAL_MATRIX_ONLY_NO_APPROVAL_NO_EXECUTION`

Parent: #6  
Rail issue: #200  
Prerequisite: #199 closed/PASS  
Source floor: `9264533` or later on `origin/main`  
Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`  
Scaffold dependency: `docs/l6w01-supervised-live-read-approval-packet-scaffold.md`

This packet is docs/tests-only denial evidence for future supervised live-read approval recognition. It does not approve, recognize, implement, or execute any live/private read. It defines synthetic stale/variant denial cases that any later implementation must reject before provider/backend/source-stat/source-read callbacks and before any source discovery, Runtime Registry consumption, persistence, activation, publication, production/provider/prod/canary authority, Atlas Gate movement, mutation behavior, or `allowed=true` route.

## Required denial invariant

Every case in this matrix has the same safe result:

- `approval_result`: `DENIED_BEFORE_CALLBACK`
- `live_read_invoked`: `false`
- `allowed`: `false`
- `allowed_result_count`: `0`
- `guarded_callback_counters`: synthetic zeros for provider, backend, source-stat, source-read, write, custody, delete, reindex, rollback, and cache-purge families
- `source_discovery_counter`: `0`
- `runtime_registry_consumption_counter`: `0`
- `persistence_record_counter`: `0`
- `activation_counter`: `0`
- `publication_or_visibility_counter`: `0`
- `provider_prod_canary_counter`: `0`
- `atlas_gate_movement_counter`: `0`

The denial receipt may report only safe refs, case ids, booleans, numeric counters, status strings, and stop-condition labels. It must not echo raw approval text, raw source content, credentials, auth/env/keychain/OAuth/auth-file material, raw platform IDs, private absolute paths, raw prompt/query payloads, raw payload content, raw backend responses, private correlation refs, source URIs, Runtime Registry data, or persistence/audit/custody record bodies.

## Synthetic denial matrix

| Case id | Unsafe approval shape | Required stop reason | Required proof |
| --- | --- | --- | --- |
| `stale_prior_rail_comment` | stale approval-like comment from L5/L6/L6U/L6V, #199, or any issue other than the exact future approval issue | `STALE_OR_WRONG_ISSUE_APPROVAL` | deny before callbacks; no live/private read |
| `variant_phrase_or_field_names` | variant wording, renamed fields, paraphrased grant text, or altered operation-class spelling | `VARIANT_APPROVAL_TEXT` | deny before callbacks; no live/private read |
| `broadened_scope_or_source_access` | approval-like shape that broadens source access, source discovery, workspace scans, family scans, broad recall, index queries, or raw content access | `BROADENED_SCOPE_OR_SOURCE_ACCESS` | deny before callbacks; zero discovery |
| `copied_unrelated_approval` | copied approval text from another issue, rail, actor, subject, owner, audience, or operation class | `COPIED_OR_UNRELATED_APPROVAL` | deny before callbacks; no approval reuse |
| `wrong_actor_owner_subject_audience_scope` | non-owner actor, wrong owner, wrong subject, wrong audience, or wrong scope | `BOUND_FIELD_MISMATCH` | deny before callbacks; no live/private read |
| `missing_expiry_or_expired` | missing `approval_expires_at`, expiry later than 12 hours after creation, or expired approval | `MISSING_OR_EXPIRED_APPROVAL` | deny before callbacks; no retry without fresh review |
| `multi_operation_or_allowed_true` | max operation count above one, multiple operation classes, multi-operation request, positive allowed result, or `allowed=true` route | `MULTI_OPERATION_OR_ALLOWED_TRUE_REQUEST` | deny before callbacks; `allowed=false` |
| `callback_requesting_shape` | provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callback request | `CALLBACK_REQUESTED` | deny before any callback counter increments |
| `activation_or_config_request` | service/listener/startup/cron activation or global Hermes/MCP/client/runtime config mutation request | `ACTIVATION_OR_CONFIG_REQUESTED` | deny before activation; no config mutation |
| `publication_visibility_provider_prod_canary` | package publication, repository visibility change, provider/prod/canary authority, or production authority request | `PUBLICATION_OR_PRODUCTION_AUTHORITY_REQUESTED` | deny before publication/production authority |
| `runtime_registry_atlas_gate_persistence` | Runtime Registry consumption, Atlas Gate movement, persistence/audit/custody record write, or cache mutation request | `REGISTRY_GATE_OR_PERSISTENCE_REQUESTED` | deny before registry, Gate, or persistence action |
| `mutation_or_rollback_execution` | write/custody/delete/reindex/rollback/cache-purge execution, mutation behavior, or rollback callback request | `MUTATION_OR_ROLLBACK_EXECUTION_REQUESTED` | deny before mutation; no rollback callback |

## Non-approval carry-forward

This matrix itself must be interpreted as `NO_APPROVAL_PRESENT`. Merge events, issue closure, labels, milestones, branch names, PR bodies, copied text, stale comments, broadened comments, missing-field comments, non-owner comments, and future comments outside the exact future approval issue remain non-approval.

A later implementation may only become eligible after a separate future owner approval comment binds the exact issue, actor association, owner, subject, audience, scope, operation class `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`, `max_operation_count=1`, creation time, expiry no later than 12 hours, report-safe output shape, zero-discovery expectation, stop conditions, and denial-before-callback behavior. This packet does not grant that approval.

## Acceptance checklist

This denial matrix is acceptable only if tests prove that it:

1. is discoverable in the docs index and contract-test inventory;
2. records `DENIAL_MATRIX_ONLY_NO_APPROVAL_NO_EXECUTION` and `NO_APPROVAL_PRESENT`;
3. covers stale, variant, broadened, copied, wrong-actor/owner/subject/audience/scope, missing-expiry, expired, multi-operation, callback-requesting, activation/config-requesting, publication/visibility/provider/prod/canary, Runtime Registry, Atlas Gate, persistence, mutation/rollback, and `allowed=true` shapes;
4. requires `DENIED_BEFORE_CALLBACK`, all-zero synthetic guarded counters, `allowed=false`, `allowed_result_count=0`, and `live_read_invoked=false` for every matrix case;
5. preserves no-live/no-callback/no-production/no-persistence/no-activation/no-`allowed=true` boundaries.
