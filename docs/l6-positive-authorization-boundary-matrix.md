# L6I.08 positive-authorization boundary matrix packet

Status: docs/tests-only preparation packet. This packet does not approve implementation, does not unhold runtime behavior, and does not create any positive allowed runtime path.

Source floor: `7980a5b` or later `origin/main`, with `docs/l6-next-implementation-slice-frontier-packet.md` recommending `SPLIT_AGAIN_DOCS_TESTS_ONLY` before any further implementation slice.

Dependency: L6I.07 closed/PASS via issue `#149` and PR `#156`.

## Purpose

L6I.08 names the report-safe boundary matrix that a later approval request must satisfy before any positive-authorization implementation is considered. It is intentionally a packet of constraints, not a runtime design change.

The current Memory Seam implementation remains limited to default-off synthetic write-intent preflight denial-before-callback behavior. The only proven runtime posture is denial/unsupported handling with zero guarded callback counters for provider, backend, source-stat, source-read, write, custody, delete, reindex, rollback, and cache-purge surfaces.

## Boundary matrix

| Boundary axis | Current permitted state | Future approval packet must bind | Still held after this packet |
| --- | --- | --- | --- |
| Authorization result | Deny or unsupported only; no positive allowed runtime path. | Exact human approval phrase, bounded expiry, actor, subject, operation class, max operation count, and report-safe approval reference. | Any implementation path returning an allowed result. |
| Operation class | Synthetic write-intent preflight shapes only, denied before mutation callbacks. | One named implementation-candidate operation class selected by a later packet. | Write execution, custody transfer, custody receipt persistence, delete, reindex, rollback, cache purge, and broad operation-class expansion. |
| Source and provider access | No live/private source reads, no source discovery, no credential/auth/keychain/env reads, no Runtime Registry consumption. | Explicit statement that the candidate slice does not require live/private reads or source discovery unless separately approved outside this rail. | Provider/backend/source-stat/source-read callbacks and private source material. |
| Runtime activation | Local tests and synthetic examples only; no recurring runner, service, listener, startup, cron, canary, provider/prod authority, or Atlas Gate movement. | Bounded local verification commands and a rollback/audit proof shape. | Service/listener/startup/cron activation, canary authority, production authority, repository visibility changes, package publication, and Atlas Gate movement. |
| Receipt shape | Report-safe denial metadata only, with boolean/counter facts and safe status strings. | Non-persistent positive-authorization receipt fixture contract, including redaction rules and no raw payload storage. | Persistent custody receipts, raw private source text, raw platform IDs, raw query payloads, raw payload content, credentials, auth files, OAuth material, and private correlation refs. |
| Callback counters | Existing tests prove denied paths stop before guarded callbacks increment. | Future counter contract must name every callback family that remains zero until an approved candidate explicitly narrows one surface. | Provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callback execution. |
| Persistence | No persistence beyond committed docs/tests/schema fixtures. | Explicit non-persistence statement for any fixture-only receipt shape. | Storage engines, custody persistence, cache mutation, rollback materialization, and durable write records. |

## Required future approval binding

A later implementation-candidate packet must be specific enough that a human can approve or reject one bounded slice without inferring authority from this packet. It must include:

1. exact candidate operation class and non-goals;
2. exact future approval language, separated from documentation examples;
3. actor, subject, owner, approver, expiry, max-operation-count, and rollback/audit expectations;
4. explicit callback families that must remain at zero and any one callback family proposed for change;
5. receipt fields that are report-safe and non-persistent unless a separate custody-persistence approval exists;
6. public artifact hygiene rules for issue, PR, test, and doc output.

## Public artifact hygiene

Public issue and PR artifacts for this packet may include public issue numbers, repository file names, synthetic operation-class names, boolean/counter facts, and safe status strings. They must not include raw private source text, credentials, auth/env/keychain material, OAuth/auth-file material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, or private correlation refs.

## L6I.08 recommendation

Proceed to L6I.09 as docs/tests/schema-fixture work only: define a non-persistent positive-authorization receipt shape fixture contract. Do not implement runtime approval, writes, custody persistence, callbacks, source reads, service activation, publication, visibility changes, or Atlas Gate movement.
