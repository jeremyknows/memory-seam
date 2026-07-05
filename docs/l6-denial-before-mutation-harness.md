# L6S.04 denied-before-mutation callback harness

Status: `denied_before_mutation_harness_non_executing`
Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`
Parent: #6
Rail issue: #128
Decision basis: Choice B / SPLIT from `l6-implementation-unhold-packet.md`

This packet is planning/design only. It adds a synthetic callback harness and
contract tests for future write/custody surfaces. It does not implement,
authorize, activate, schedule, simulate, or execute writes, custody transfer,
delete, reindex, rollback, cache purge, provider/backend/source-stat/source-read
callbacks, service/listener/cron/startup behavior, source discovery,
unsupervised reads, live/private source reads, Runtime Registry consumption,
global Hermes/MCP/client/runtime configuration mutation, provider/prod/canary
authority, repository visibility changes, package publication, or Atlas Gate
movement.

This L6S.04 packet is not approval. It only defines how a future implementation
slice must prove denial ordering before any mutation-capable callback can be
reachable.

## Denied-before-mutation proof rule

For every covered future operation class, a denied path must stop at preflight
classification and return a report-safe denial result before any guarded
callback is invoked. Unknown operation classes also deny before callbacks.

Required result shape:

- `allowed`: `False`
- `denied_before_mutation`: `True`
- `callbacks_invoked`: `False`
- `counters`: every guarded callback counter remains `0`
- `held_surfaces`: includes all hard-held mutation, read, activation, provider,
  publication, visibility, and Gate surfaces
- `report_safety`: all private-leakage flags remain `False`

## Synthetic callback bundle

The harness exposes callbacks that increment a synthetic counter and fail fast if
called. A passing denial proof must never call them. All guarded callback
counters must remain `0` after both known-operation and unknown-operation
preflight denial.

Guarded callback counters:

- `provider_callback`
- `backend_callback`
- `source_stat_callback`
- `source_read_callback`
- `write_callback`
- `custody_callback`
- `delete_callback`
- `reindex_callback`
- `rollback_callback`
- `cache_purge_callback`
- `audit_persistence_callback`
- `runtime_registry_callback`
- `activation_callback`

Known operation classes:

- `write_intent`
- `custody_receipt_persistence`
- `delete`
- `reindex`
- `rollback`
- `cache_purge`

## Held surfaces preserved

The harness keeps these surfaces held:

- write execution
- custody transfer
- delete execution
- reindex execution
- rollback execution
- cache purge execution
- provider/backend/source-stat/source-read callbacks
- source discovery
- live/private source reads
- unsupervised reads
- service/listener/cron/startup behavior
- Runtime Registry consumption
- global Hermes/MCP/client/runtime configuration mutation
- credential/auth/env/keychain/OAuth/auth-file reads
- provider/prod/canary authority
- repository visibility changes
- package publication
- Atlas Gate movement

## Public/report-safe artifact rules

Public issue, PR, test, and doc artifacts must not include raw private source
text, credentials, auth/env/keychain material, raw platform IDs, private absolute
paths, raw query payloads, raw payload content, or private correlation refs. The
harness uses only synthetic operation names and report-safe error codes.

## Acceptance evidence

The companion tests assert that:

1. known operation classes deny before provider/backend/source-stat/source-read,
   write, custody, delete, reindex, rollback, cache-purge, audit, Runtime
   Registry, or activation callbacks;
2. unknown operation classes also deny before callbacks;
3. all guarded callback counters stay at `0` for denied paths;
4. fail-fast callbacks would expose any ordering regression if a future change
   incorrectly invokes them;
5. report-safety flags stay false and discoverability is maintained through the
   documentation index and contract-test inventory.
