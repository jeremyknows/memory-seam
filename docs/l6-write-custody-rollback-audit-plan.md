# L6S.02 rollback and audit plan for first write/custody slice

Status: `schema_fixture_implementation_held`.

Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`.

This packet defines the rollback, audit, stop-condition, timeout, and failure-mode requirements for one future bounded L6 write/custody implementation slice. It is planning/design only: it does not implement, authorize, activate, schedule, simulate, or execute writes, custody transfer, delete, reindex, rollback, cache purge, service/listener/cron/startup behavior, recurring runners, source discovery, unsupervised reads, live/private source reads, provider/backend calls, Runtime Registry consumption, global Hermes/MCP/client/runtime configuration mutation, provider/prod/canary authority, package publication, repository visibility changes, Atlas Gate movement, or production-authoritative claims.

This L6S.02 packet is not approval. It cannot be combined with the L6S.01 approval model, issue closure, a merged PR, cron identity, or repository access to imply write/custody/rollback authority.

## Required rollback plan shape

Every future implementation issue that asks to unhold a bounded write/custody slice must include a public/report-safe rollback plan before any code may cross a held surface. The plan must name:

- `plan_ref` — public-safe rollback plan reference.
- `scope` — exactly one future, explicitly approved, bounded implementation issue.
- `preconditions` — approval model fields validated, pre-mutation guard passed in the future slice, report-safe audit fields ready, and separate future rollback approval required before rollback execution.
- `steps` — capture a report-safe pre-mutation audit receipt, deny this schema fixture before mutation, record only reversible operation references if a separate future mutation is approved, and stop for human triage on uncertain or unsafe state.
- `postconditions` — no current runtime mutation support, rollback execution remains held, and public artifacts remain report-safe.

Rollback planning is required, but rollback execution remains held. A future write/custody implementation approval does not automatically approve rollback execution unless the exact future approval explicitly says so.

## Required audit event fields

Future audit receipts must carry these report-safe fields before any future bounded implementation slice may attempt a mutation:

- `schema_version`
- `event_ref`
- `approval_ref`
- `operation_class`
- `actor_binding_ref`
- `custody_owner_role`
- `approver_role`
- `pre_mutation_guard_result`
- `mutation_supported`
- `mutation_attempted`
- `rollback_required`
- `rollback_plan_ref`
- `stop_condition_ref`
- `timeout_ref`
- `failure_mode_ref`
- `side_effect_counters`
- `report_safe_reference`

Audit receipts must not include raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, or private correlation refs. Audit persistence is not added by this packet; the fixture records schema requirements only.

## Stop conditions

A future slice must stop before mutation, or stop after at most its separately approved bounded operation, when any of these conditions appear:

- `approval_missing_or_mismatched`
- `actor_binding_mismatch`
- `approval_expired`
- `max_operation_count_exhausted`
- `pre_mutation_guard_denied`
- `unsupported_runtime_mutation_surface`
- `audit_field_missing`
- `rollback_plan_missing`
- `timeout_elapsed`
- `report_safety_violation`

Stop conditions are fail-closed. They do not permit automatic retries, recurring runner activation, source discovery, live/private reads, provider/backend calls, write/custody/reindex/delete/cache-purge behavior, or rollback execution.

## Timeout and failure modes

The future implementation issue must define `future_slice_timeout_required_before_execution`. On timeout, the slice must stop before mutation or, if a separately approved future operation already happened, stop after that bounded operation and require human triage. Recurring retry is forbidden and activation remains disallowed.

Required failure modes:

- `deny_before_mutation`
- `emit_report_safe_audit_receipt_only`
- `require_human_triage_for_any_future_mutation_attempt`
- `do_not_retry_automatically`
- `do_not_execute_rollback_without_separate_approval`

## Schema fixture

`src/memory_seam/write_custody_rollback_audit.py` defines `L6_WRITE_CUSTODY_ROLLBACK_AUDIT_FIXTURE`, a public-safe non-executing fixture for the future L6 operation classes:

- `write_intent`
- `custody_receipt_persistence`
- `delete_intent`
- `reindex_intent`
- `rollback_intent`
- `cache_purge_intent`

The fixture records rollback plan shape, required audit event fields, stop conditions, timeout behavior, failure modes, held runtime mutation support, zero side-effect counters, held surfaces, and report-safety flags. It does not call providers, read sources, persist audit artifacts, execute rollback, or mutate runtime state.

## Preserved held surfaces

Unless Jeremy posts exact future approval for a named implementation slice, these surfaces remain held:

- write/custody/reindex/delete/cache-purge/rollback behavior;
- service/listener/cron/startup activation, recurring runners, and recurring unsupervised reads;
- unsupervised reads, live/private source reads, and source discovery;
- credential/auth/env/keychain/OAuth/auth-file reads;
- Runtime Registry consumption;
- global Hermes/MCP/client/runtime configuration mutation;
- provider/prod/canary authority;
- repository visibility change and package publication;
- Atlas Gate movement and production-authoritative claims;
- public artifacts containing raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, or private correlation refs.

## Verification

`tests/test_l6_write_custody_rollback_audit_plan.py` proves the doc and fixture are discoverable, require rollback/audit/stop-condition/timeout/failure-mode fields, keep runtime mutation unsupported, preserve zero side effects, reject unsafe fixture regressions with report-safe error codes, and keep all implementation and activation surfaces held.
