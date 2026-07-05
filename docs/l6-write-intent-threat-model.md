# L6.01 write-intent threat model and custody boundary

Status: **NO WRITE IMPLEMENTATION ADDED**. This document is a threat model and custody-boundary note only. It does not add, enable, schedule, authorize, simulate, or execute write/custody/reindex/delete/cache-purge behavior.

Parent rail: #6 L5/L6 unsupervised read ladder and write-custody companion. Selected issue: #109 L6.01.

## Boundary summary

Memory Seam remains a read-only, default-off package surface. L6 write/custody work is held until Jeremy explicitly approves a future implementation slice. This packet only defines vocabulary, risks, future approval requirements, audit fields, rollback expectations, and current unsupported surfaces.

Current posture:

- Write implementation: `UNSUPPORTED_HELD`
- Custody implementation: `UNSUPPORTED_HELD`
- Delete implementation: `UNSUPPORTED_HELD`
- Reindex implementation: `UNSUPPORTED_HELD`
- Cache purge implementation: `UNSUPPORTED_HELD`
- Read receipt behavior: `READ_ONLY_METADATA_RECEIPT`
- Provider/backend/source/file-stat calls for write-like paths: `DENIED_BEFORE_CALLBACKS`
- Runtime Registry consumption: `HELD`
- Global Hermes/MCP/client/runtime configuration mutation: `HELD`
- Service/listener/cron/startup activation: `HELD`

## Definitions

| Surface | Meaning | Current authority |
| --- | --- | --- |
| Write intent | A request, proposal, or plan to mutate memory/source/custody state. It may include target class, reason, expected effect, and rollback expectation. | Documentation-only. No mutation path exists or is authorized. |
| Custody | Ownership and responsibility for approving, sequencing, recording, and rolling back any future memory/source mutation. Custody is distinct from the read-only Memory Seam runtime. | Held for a future Jeremy-approved design. |
| Delete | Removing memory/source/index/cached state or marking it as removed. | Unsupported; must deny before provider/backend/custody/reindex callbacks. |
| Reindex | Rebuilding, refreshing, or changing retrieval/index state. | Unsupported; must deny before provider/backend/custody/reindex callbacks. |
| Cache purge | Invalidating or removing cached read/source/index artifacts. | Unsupported; may be named as rollback expectation but not performed. |
| Read receipt | Metadata-only evidence that a read-only request was allowed, denied, or degraded. | Supported only as read-only/report-safe metadata; not a write/custody receipt and not approval to mutate. |

## Non-goals for L6.01

This issue does not:

- add a write API, custody API, delete API, reindex API, cache-purge API, worker, service, listener, cron job, startup hook, or recurring runner;
- perform live/private source reads, source discovery, provider/prod/canary actions, or Runtime Registry consumption;
- read credentials, auth material, environment secrets, keychain data, OAuth state, or auth files;
- mutate global Hermes/MCP/client/runtime configuration;
- change repository visibility, publish a package, move Atlas Gate state, or make production-authoritative claims;
- create raw private source text, private absolute paths, raw platform IDs, raw query payloads, private correlation refs, or credentials in public artifacts.

## Threat model

### Assets to protect

- Public/reportable Memory Seam artifacts and PR/issue comments.
- Private source text and private source locations.
- Credential/auth/env/keychain/OAuth/auth-file material.
- Platform IDs, raw query/payload content, and private correlation references.
- Read-only trust posture for existing Memory Seam runtime, router, provider, and receipt contracts.
- Future custody authority, which must remain separate from read-only read receipts.

### Actors and misuse cases

| Actor or pressure | Misuse case | Required response |
| --- | --- | --- |
| Benign operator | Attempts to use a write-like route as if Memory Seam supports mutation. | Deny before provider/backend/source/file-stat/custody/reindex callbacks and return report-safe reason. |
| Confused downstream adapter | Treats read receipt metadata as write approval or custody evidence. | Documentation and tests must state read receipts are not custody receipts and cannot authorize mutation. |
| Malicious payload | Embeds secrets, private paths, platform IDs, or raw payload content in write-like body fields. | Denial/error text must not echo raw payload or sensitive-looking identifiers. |
| Release pressure | Tries to publish or mark the repo production-ready because L6 docs exist. | Preserve repository visibility, package publication, provider/prod/canary, and Gate holds. |
| Automation drift | Converts a no-op design into a runner, cron, service, or recurring write path. | Keep all L6.01 artifacts docs/tests only and assert no activation is created. |

### Primary risks

1. **Read/write boundary confusion** — read-only receipts could be mistaken for custody receipts.
2. **Premature mutation authority** — a helper or route could appear that writes, deletes, reindexes, purges, or queues custody work.
3. **Sensitive echo** — denial responses could print raw payloads, private paths, platform IDs, or token-like values.
4. **Backend-before-denial regression** — write-like requests could instantiate provider/backend/source/file-stat/custody/reindex callbacks before denial.
5. **Authority creep** — docs could imply release, production, canary, Atlas Gate, Runtime Registry, or global config authority.

## Required future approvals before any write/custody design or execution

A future issue must be opened and Jeremy must provide explicit approval naming the exact slice. The approval must include:

- issue number and document path for the approved slice;
- operation class: write intent, custody receipt design, delete, reindex, cache purge, or implementation;
- target family and subject shape using report-safe labels only;
- allowed metadata fields and forbidden raw/private fields;
- maximum number of operations and timeout/expiry;
- required denial-before-callback counters;
- custody owner and human review path;
- rollback expectation and stop conditions;
- public hygiene requirements;
- explicit preservation or unhold status for repository visibility, package publication, live/private reads, service/listener/cron/startup activation, Runtime Registry, global config mutation, provider/prod/canary authority, and Atlas Gate movement.

Absent that exact future approval, every write/custody/delete/reindex/cache-purge route remains unsupported.

## Future audit fields required before mutation is even designed

Any later no-op schema or implementation proposal must define report-safe audit fields before action:

- `schema` and schema version;
- `operation_class` from `write_intent`, `custody`, `delete`, `reindex`, `cache_purge`, or `read_receipt`;
- `decision` such as `denied_before_write`, `held_for_approval`, or `rollback_required`;
- `approval_issue` and `approval_phrase_hash` or other report-safe approval reference, not raw private correlation refs;
- `subject_shape`, not raw subject payload;
- `target_family`, not private absolute path or raw platform ID;
- `allowed_metadata_fields` and redaction labels;
- posture counters proving zero provider/backend/source/file-stat/custody/reindex callbacks when denied;
- `write_custody_or_reindex` boolean, expected to remain `false` until a later explicit unhold;
- `rollback_required`, `rollback_owner`, and `stop_conditions`;
- public hygiene verdict.

## Rollback expectations

Because L6.01 performs no mutation, rollback is documentation-only: revert the PR or remove this document/test if it is found to imply authority. Future mutation-capable work must define rollback before implementation, including who owns custody, how to stop further actions, how to mark stale artifacts, and how to report safely without raw private data.

Current read-only rollback hints may mention `cache_purge_required` or `write_custody_or_reindex_required` as false/metadata expectations; they do not perform cache purge, write custody, delete, or reindex actions.

## Current unsupported-surface assertions

L6.01 keeps these current package invariants intact:

- credential/auth/env/keychain/OAuth/auth-file material remains held and is never read.
- `LocalReadOnlyRuntime.idle_tick()` reports `write_custody_or_reindex=false` and `write_custody_unheld=false`.
- `LocalReadOnlyRuntime` denies configured write-like routes before provider/backend/source/file-stat/custody/reindex callbacks.
- The router reports write-like routes unavailable rather than dispatching mutation handlers.
- `RUNTIME_HELD_SURFACES` includes `write_custody_reindex`.
- No source discovery, live/private source reads, credential/auth/env/keychain/OAuth/auth-file read, Runtime Registry consumption, global Hermes/MCP/client/runtime configuration mutation, service/listener/cron/startup activation, repository visibility change, package publication, provider/prod/canary authority, or Atlas Gate movement is introduced.

## Public hygiene requirements

Public docs, tests, issue comments, PR bodies, and receipts for this lane must not contain raw private source text, credentials, auth/env/keychain/OAuth/auth-file material, raw platform IDs, private absolute paths, raw query payloads, or private correlation refs. Write-like denial bodies must use stable reason codes instead of echoing raw payloads.

## Decision for #109

PASS criteria for this issue are docs/tests only: this threat model exists, distinguishes write intent/custody/delete/reindex/cache purge/read receipt behavior, lists future approvals and audit fields, preserves all held surfaces, and asserts current write/custody surfaces remain unsupported. It does not unhold #110 implementation beyond the next AFK denial-matrix test slice.
