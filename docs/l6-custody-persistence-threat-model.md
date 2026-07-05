# L6I.10 custody persistence threat model and storage non-goals packet

Status: docs/tests-only threat-model packet. This packet is decision-only, non-approval, and non-executable. It does not approve implementation, does not unhold runtime behavior, does not create persistence, and does not create any positive allowed runtime path.

Source floor: `7980a5b` or later `origin/main`.
Dependency: L6I.09 closed/PASS via issue `#151` and PR `#158`.
Frontier basis: `docs/l6-next-implementation-slice-frontier-packet.md` recommends `SPLIT_AGAIN_DOCS_TESTS_ONLY` before any additional positive-authorization or custody-adjacent implementation request.

## Purpose

L6I.10 defines the custody receipt persistence threat model before any persistence skeleton may be requested. The only durable changes authorized by this work are normal repository docs/tests changes through review. No runtime store, audit sink, custody transfer, rollback action, background runner, or scheduled process is introduced.

The current implementation remains narrower than this packet: it only proves synthetic no-production write-intent denial-before-callback behavior and report-safe denial metadata. L6I.09 added a non-authoritative, non-persistent fixture for a hypothetical `positive_authorization_recognized_mutation_held` receipt shape. L6I.10 keeps persistence held and names the proof a future request would need before any storage class can be reconsidered.

## Held storage classes

Every storage class below remains held. Naming a class here is a non-goal, not a partial approval.

| Storage class | Held non-goal | Why it stays held |
| --- | --- | --- |
| Filesystem writes | No custody receipt files, append logs, local state files, cache files, generated receipts, or operator-path writes. | Local files can become durable audit records, leak private source context, or outlive the exact operation approval. |
| SQLite/database writes | No SQLite, embedded database, external database, migration, table, row, or audit-event persistence. | Database rows create retention, access-control, rollback, and deletion obligations that are not yet approved. |
| Object storage | No bucket/object/blob write, retention policy, object metadata, or upload callback. | Object storage can cross trust boundaries and requires explicit retention, cleanup, and access policy. |
| Remote API writes | No issue, ticket, audit, logging, webhook, telemetry, provider, backend, or source-platform write used as custody persistence. | Remote APIs can publish or persist report material outside the repository review lane. |
| Git commits | No runtime-created commit, branch, tag, note, changelog entry, generated receipt commit, or bot-authored audit trail. | Git history is durable and public-facing after visibility changes; runtime commit authority is not approved. |
| Issue/PR comments as persistence | Issue and PR comments are not custody persistence unless separately approved with exact custody-persistence authority. Normal review comments may report docs/tests verification only. | Public artifacts must not become the durable custody store by accident. |
| Runtime Registry/state mutation | No Runtime Registry consumption, registry write, global Hermes/MCP/client/runtime configuration mutation, service state, startup record, recurring runner state, or callback state mutation. | Registry and runtime state can activate behavior or carry production authority outside this rail. |

## Minimum future proof before persistence can be considered

A later HITL packet may ask to consider persistence only after all of these are bound explicitly and tested with synthetic/report-safe fixtures:

1. Exact approval: one fresh, exact approval phrase for the persistence candidate, with public issue reference and no stale reuse.
2. Single operation class: exactly one named operation class, not a family expansion and not an implied write/custody/delete/reindex/rollback/cache-purge grant.
3. Local synthetic-only target: no live/private source read, no source discovery, no provider/backend/source-stat/source-read callback, and no production/canary authority.
4. Report-safe payload: no raw private source text, credentials, auth/env/keychain material, OAuth/auth-file material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, or private correlation refs.
5. Pre-mutation receipt: any proposed receipt must be emitted before mutation remains unsupported, and must not be evidence that mutation happened.
6. Rollback/no-op posture: rollback requirements must be documented, but rollback execution remains held; the first proof must stay no-op or denial-before-mutation.
7. Stop conditions: stale approval, variant approval, actor mismatch, expiry, count overflow, unsafe payload, callback attempt, storage attempt, and private-data inclusion all stop before persistence.
8. Cleanup/retention plan: explicit retention, cleanup, redaction, access, and deletion obligations must be documented before any durable sink exists.

## Residual L6I held surfaces

This packet preserves or exceeds the L6I.06 and L6I.09 holds. It does not authorize runtime approval acceptance, a positive allowed runtime path, write execution, custody transfer, custody persistence, delete execution, reindex execution, rollback execution, cache purge execution, provider/backend callbacks, source-stat/source-read callbacks, source discovery, live/private source reads, credential/auth/env/keychain/OAuth/auth-file reads, Runtime Registry consumption, global configuration mutation, service/listener/startup/cron activation, recurring runner activation, provider/prod/canary authority, publication, repository visibility changes, Atlas Gate movement, or production-authoritative claims.

Public issue and PR artifacts may contain public issue numbers, repository file names, synthetic operation-class names, boolean/counter facts, safe status strings, and local verification command names. They must not include raw private source text, credentials, auth/env/keychain material, OAuth/auth-file material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, or private correlation refs.

## L6I.10 recommendation

Proceed to L6I.11 as docs/tests-only future allowed-path counter and callback contract work. Do not implement persistence, durable audit storage, custody transfer, rollback execution, background runners, scheduled processes, runtime approval acceptance, positive allowed runtime paths, writes, delete, reindex, cache purge, provider/backend/source callbacks, live/private reads, source discovery, Runtime Registry consumption, activation, publication, visibility changes, provider/prod/canary authority, or Atlas Gate movement.
