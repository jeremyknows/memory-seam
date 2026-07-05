# L6I.11 future allowed-path counter and callback contract

Status: docs/tests-only counter and callback contract. This packet is preparatory, non-approval, non-executable, and does not implement runtime behavior. It does not create any `allowed=true` path, does not approve positive authorization acceptance, and does not unhold mutation, callbacks, persistence, source reads, activation, publication, provider/prod/canary authority, repository visibility change, or Atlas Gate movement.

Source floor: `7980a5b` or later `origin/main`.
Dependency: L6I.10 closed/PASS via issue `#152` and PR `#159`.
Frontier basis: `docs/l6-next-implementation-slice-frontier-packet.md` recommends `SPLIT_AGAIN_DOCS_TESTS_ONLY` before any additional implementation slice.

## Purpose

L6I.11 names the future allowed-path counter and callback contract that a later implementation-candidate packet must satisfy before asking for one exact positive-authorization slice. It is a measurement and stop-condition packet only. The current runtime remains denial/no-mutation only, and existing guarded callback families remain zero on denied paths.

This packet exists so the next selector packet can compare candidate slices without inventing counter semantics during approval review. It does not choose a slice, implement a parser, emit receipts, call providers, call backends, read sources, execute writes, transfer custody, persist receipts, delete, reindex, roll back, purge caches, start services, or consume Runtime Registry state.

## Counter contract for future approval requests

A later approval request must bind every counter below before any future positive-authorization implementation can be considered. Unless one callback family is explicitly selected by a later packet and separately approved by a human, the required value remains `0`.

| Counter family | Required current/future-held value | Future approval packet must state | Stop condition |
| --- | --- | --- | --- |
| Authorization result counters | `allowed_result_count=0`; denied/unsupported counts may be reported only as safe metadata. | Whether a proposed slice asks to create exactly one allowed-result path and the exact operation class it would cover. | Any implicit, stale, variant, broad, or unbounded allowed result stops before mutation or callback. |
| Provider callback counters | `provider_callback_count=0`. | Provider callbacks remain held unless the selected candidate names one synthetic local callback and separate proof. | Any provider callback attempt outside exact approval stops before provider access. |
| Backend callback counters | `backend_callback_count=0`. | Backend callbacks remain held and cannot be used as persistence, telemetry, audit, or source access. | Any backend callback attempt stops before backend access. |
| Source-stat callback counters | `source_stat_callback_count=0`. | Source-stat callbacks remain held; no source discovery or metadata probing is implied. | Any stat/probe/list attempt stops before source access. |
| Source-read callback counters | `source_read_callback_count=0`. | Source-read callbacks remain held; no live/private read is authorized by positive authorization prep. | Any source-read attempt stops before reading raw source material. |
| Write callback counters | `write_callback_count=0`. | Write execution remains held unless a later HITL packet selects one synthetic no-production candidate and exact approval. | Any write attempt without exact approved slice stops before mutation. |
| Custody callback counters | `custody_callback_count=0`. | Custody transfer remains held; custody owner may be named only as report-safe metadata. | Any custody transfer attempt stops before ownership or state change. |
| Delete callback counters | `delete_callback_count=0`. | Delete execution remains held and is not bundled with write intent. | Any delete attempt stops before deletion. |
| Reindex callback counters | `reindex_callback_count=0`. | Reindex execution remains held and cannot be inferred from read, write, or custody language. | Any reindex attempt stops before index mutation. |
| Rollback callback counters | `rollback_callback_count=0`. | Rollback requirements may be documented, but rollback execution remains held. | Any rollback execution attempt stops before rollback materialization. |
| Cache-purge callback counters | `cache_purge_callback_count=0`. | Cache purge remains held and cannot be used as cleanup without exact approval. | Any cache-purge attempt stops before cache mutation. |
| Persistence counters | `persistent_receipt_count=0`; `durable_write_record_count=0`; `audit_persistence_count=0`; `cache_mutation_count=0`. | Persistence remains held under the L6I.10 storage non-goals unless separately approved. | Any storage attempt stops before filesystem, database, object-store, remote API, Git, issue/PR-comment-as-custody-store, or Runtime Registry/state mutation. |

## Callback contract language for the next selector packet

The next implementation-candidate selector packet must include these report-safe statements for each candidate it compares:

1. the candidate operation class and whether it proposes any future change from all-zero guarded callback counters;
2. the single callback family, if any, proposed for later human approval;
3. every callback family that remains held at `0`;
4. the exact pre-callback stop conditions for stale approval, variant approval, actor mismatch, subject mismatch, owner mismatch, expiry, max-operation-count overflow, unsafe payload, callback attempt, storage attempt, source-read attempt, source-discovery attempt, Runtime Registry attempt, activation attempt, and private-data inclusion;
5. the report-safe counter names that may appear in issue, PR, test, and doc output;
6. an explicit statement that the selector packet is not implementation approval and cannot authorize `allowed=true`, mutation, persistence, callbacks, source reads, activation, publication, visibility changes, provider/prod/canary authority, or Atlas Gate movement.

## Public/reportable counter fields

Public artifacts may report only boolean and integer counter facts, public issue and PR numbers, repository file names, synthetic operation-class names, safe status strings, and role names. They must not include raw private source text, credentials, auth/env/keychain material, OAuth/auth-file material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, private correlation refs, or raw approval text.

A future receipt or test fixture may name the following report-safe counter fields only if it also states that mutation and persistence remain held: `allowed_result_count`, `provider_callback_count`, `backend_callback_count`, `source_stat_callback_count`, `source_read_callback_count`, `write_callback_count`, `custody_callback_count`, `delete_callback_count`, `reindex_callback_count`, `rollback_callback_count`, `cache_purge_callback_count`, `persistent_receipt_count`, `durable_write_record_count`, `audit_persistence_count`, and `cache_mutation_count`.

## Residual held surfaces

This packet preserves all L6I hard holds. It does not authorize runtime approval acceptance, any implementation path returning `allowed=true`, write execution, custody transfer, custody persistence, delete execution, reindex execution, rollback execution, cache-purge execution, provider/backend/source-stat/source-read callbacks, source discovery, live/private source reads, credential/auth/env/keychain/OAuth/auth-file reads, Runtime Registry consumption, global Hermes/MCP/client/runtime configuration mutation, service/listener/startup/cron activation, recurring runner activation, provider/prod/canary authority, repository visibility changes, package publication, Atlas Gate movement, or production-authoritative claims.

## L6I.11 recommendation

Proceed to L6I.12 as docs/tests-only implementation-candidate selector packet work for one next slice. The selector may compare candidates and recommend one future approval request, but it must not implement runtime behavior, add a positive allowed runtime path, execute or persist writes/custody/delete/reindex/rollback/cache-purge, call provider/backend/source callbacks, read or discover live/private sources, consume Runtime Registry, mutate configuration, activate services or recurring jobs, publish packages, change repository visibility, claim provider/prod/canary authority, or move Atlas Gate.
