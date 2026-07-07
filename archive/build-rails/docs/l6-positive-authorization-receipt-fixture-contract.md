# L6I.09 positive-authorization receipt fixture contract

Status: docs/tests/schema-fixture only. This packet is non-authoritative, non-persistent, and does not approve implementation. It does not create approval parser behavior, a positive allowed runtime path, write execution, custody transfer, custody persistence, callbacks, live/private source reads, service activation, publication, visibility change, provider/prod/canary authority, or Atlas Gate movement.

Source floor: `7980a5b` or later `origin/main`, with `docs/l6-next-implementation-slice-frontier-packet.md` recommending `SPLIT_AGAIN_DOCS_TESTS_ONLY`.

Dependency: L6I.08 closed/PASS via issue `#150` and PR `#157`.

## Purpose

L6I.09 defines a report-safe fixture shape for a hypothetical future result where an exact positive authorization reference is recognized but mutation remains held. The fixture exists only in `tests/fixtures/l6i09_positive_authorization_receipt_fixture.json`; it is not imported by runtime code and is not a durable receipt store.

This packet intentionally keeps the existing denied receipt semantics separate from the hypothetical positive-recognized/mutation-held shape. Denied receipts describe current runtime denial metadata. The L6I.09 fixture describes a future contract a later approval request may ask to implement after separate human approval.

## Required fixture fields

The positive-recognized/mutation-held fixture must include these public-safe fields:

| Field | Required value or meaning | Boundary |
| --- | --- | --- |
| `schema_version` | `l6i09-positive-authorization-receipt-shape-v0` | Versioned fixture contract only. |
| `status` | `positive_authorization_recognized_mutation_held` | Recognition is hypothetical and does not make mutation available. |
| `operation_class` | One synthetic candidate class name | No broad operation-class expansion. |
| `approval_ref` | Report-safe public approval reference placeholder | No raw approval text, raw actor ID, private correlation ref, credential, or auth material. |
| `actor_binding_ref` | Report-safe actor-binding reference placeholder | Binding is named without exposing raw platform IDs. |
| `custody_owner_role` | `librarian` | Custody remains owned/held; no transfer occurs. |
| `rollback_audit_plan_ref` | Public doc reference | Plan reference only; no rollback or audit persistence. |
| `mutation_attempted` | `false` | No write/custody/delete/reindex/rollback/cache-purge attempt. |
| `mutation_supported` | `false` | Runtime mutation remains unsupported. |
| `authorization_allowed_runtime_path` | `false` | No positive allowed runtime path is created. |
| `fixture_is_authoritative` | `false` | Fixture is not approval and cannot authorize execution. |
| `fixture_is_persistent` | `false` | Fixture is committed test data only, not a durable receipt. |
| `guarded_counters` | All guarded callback counters are `0` | Provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks remain held. |
| `report_safety` | All unsafe inclusion flags are `false`; public refs flag is `true` | Public artifact hygiene remains enforceable. |
| `held_surfaces` | Residual hard holds ledger | Runtime approval acceptance, positive allowed paths, mutation, persistence, source reads/discovery, activation, publication, visibility, provider/prod/canary authority, and Atlas Gate movement remain held. |

## Semantic separation from denied receipts

Denied receipt metadata remains the only runtime-emitted L6I write-intent receipt posture in this repository. It is characterized by denial/no-mutation status, denied-before-callback evidence, and report-safe counter summaries.

The L6I.09 fixture differs in name and schema so tests can prove the concepts do not collapse into one another:

- denied receipt semantics: `status=denied_no_mutation_path`, `approval_recognized=false`, `semantic_boundary=runtime_denial_metadata_only`;
- hypothetical positive-recognized fixture: `status=positive_authorization_recognized_mutation_held`, `mutation_attempted=false`, `mutation_supported=false`, `fixture_is_authoritative=false`, `fixture_is_persistent=false`.

## Non-persistence and non-authority contract

The fixture may be used by tests and decision packets as a schema target only. It must not be treated as runtime approval evidence, a storage migration, an audit sink, a custody record, a cache entry, a provider callback request, a source-read request, or a production/canary signal.

Explicit non-persistence flags are required: `persistent_storage_allowed=false`, `custody_receipt_persisted=false`, `audit_trail_persisted=false`, `cache_mutated=false`, and `durable_write_record_created=false`.

## Public artifact hygiene

Public issue, PR, test, and doc artifacts may include public issue numbers, repository file names, schema/status strings, boolean facts, zero-counter facts, and role names. They must not include raw private source text, credentials, auth/env/keychain material, OAuth/auth-file material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, or private correlation refs.

## L6I.09 recommendation

Proceed to L6I.10 as docs/tests-only custody persistence threat-model and storage non-goals work. Do not implement runtime approval acceptance, a positive allowed runtime path, writes, custody transfer or persistence, delete, reindex, rollback, cache purge, provider/backend/source callbacks, live/private reads, source discovery, Runtime Registry consumption, activation, publication, visibility changes, provider/prod/canary authority, or Atlas Gate movement.
