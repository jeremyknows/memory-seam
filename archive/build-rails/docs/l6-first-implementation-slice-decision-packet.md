# L6S.06 first implementation-slice decision packet

Status: `HITL_DECISION_PACKET_ONLY`
Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`
Parent: #6
Rail issue: #130
Decision basis: Choice B / SPLIT from `docs/l6-implementation-unhold-packet.md`
Recommended slice name: `L6_WRITE_INTENT_PREFLIGHT_GATE_SKELETON`

This packet is docs/tests only. It asks for one exact future decision; it does
not approve, implement, enable, activate, schedule, simulate, or execute writes,
custody transfer, delete, reindex, rollback, cache purge, service/listener/cron/
startup behavior, recurring runner behavior, unsupervised reads, source
discovery, live/private source reads, provider/backend/source-stat/source-read
callbacks, Runtime Registry consumption, global Hermes/MCP/client/runtime
configuration mutation, credential/auth/env/keychain/OAuth/auth-file reads,
provider/prod/canary authority, repository visibility changes, package
publication, production-authoritative claims, or Atlas Gate movement.

This L6S.06 packet is not approval. Work remains held unless Jeremy posts the
exact approval phrase below for issue #130 or a successor issue that explicitly
carries this packet forward.

## Recommended first slice

Recommended future implementation slice:
`L6_WRITE_INTENT_PREFLIGHT_GATE_SKELETON`.

Bounded purpose: add the smallest non-production implementation skeleton that
can parse and deny a synthetic write-intent operation before mutation callbacks.
The slice should wire only a default-off preflight gate and tests around denied
paths. It must not perform write execution, custody transfer, delete execution,
reindex execution, rollback execution, cache purge execution, provider/backend
callbacks, source-stat/source-read callbacks, live/private reads, source
discovery, Runtime Registry consumption, activation, publication, visibility
changes, or Atlas Gate movement.

Allowed operation class for this first slice: `write intent` only. Custody
receipt persistence, delete, reindex, rollback, and cache purge remain future
operation classes and are not included in this recommended first slice.

## Exact approval language required

Jeremy may approve only by posting this exact language, filling every bracketed
field with concrete values:

> I approve Memory Seam to implement exactly one bounded L6 write/custody slice named L6_WRITE_INTENT_PREFLIGHT_GATE_SKELETON under issue #[issue number] and docs/l6-first-implementation-slice-decision-packet.md. The approved slice is limited to operation class write intent, with maximum [number] synthetic no-production operations, no production execution, no recurring runner/canary/startup/cron/service/listener activation, no Runtime Registry consumption, no global Hermes/MCP/client/runtime configuration mutation, no credential/auth/env/keychain/OAuth/auth-file reads, no source discovery, no live/private source reads, no provider/prod/canary authority beyond this named slice, no repository visibility change, no package publication, and no Atlas Gate movement. The implementation must preserve denial-before-callback tests with zero provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge counters on denied paths, emit only report-safe receipts or denial metadata, keep rollback and audit requirements from docs/l6-write-custody-rollback-audit-plan.md, and stop when approval expires at [timestamp or duration].

Any variant, partial quote, implied approval, merge event, issue close, label,
assignment, emoji reaction, checklist item, stale approval, or unrelated comment
is not implementation approval.

## Required limits for the approved slice

If exact approval is later granted, the first implementation slice must stay
inside these limits:

1. Operation class: `write intent` only.
2. Maximum operation count: the concrete count Jeremy fills into the approval
   phrase; the packet recommends `1` for the first run of implementation work.
3. Execution boundary: no production execution and no live/private source reads.
4. Mutation boundary: denied paths must stop before write, custody, delete,
   reindex, rollback, cache purge, provider, backend, source-stat, source-read,
   audit-persistence, Runtime Registry, activation, publication, visibility, or
   Atlas Gate callbacks.
5. Time boundary: stop when the filled expiry timestamp or duration is reached.
6. Evidence boundary: public artifacts may include issue numbers, file names,
   synthetic operation-class names, boolean/counter facts, and safe error-code
   style terms only.

## Rollback and audit requirements

A future approved implementation must carry rollback and audit requirements from
`docs/l6-write-custody-rollback-audit-plan.md` before merge:

- rollback plan reference;
- audit event schema reference;
- custody owner and approver references;
- exact approval reference that is report-safe;
- timeout and stop conditions;
- failure modes for approval mismatch, stale approval, exceeded operation count,
  denied callback, hygiene failure, and verification failure;
- no-op rollback posture for denied/no-mutation paths;
- public-safe receipt or denial metadata only.

This packet does not create a rollback implementation and does not authorize a
rollback execution.

## Residual held surfaces

These surfaces remain held after this packet unless a later exact approval names
them explicitly:

- write execution;
- custody transfer and custody receipt persistence;
- delete execution;
- reindex execution;
- rollback execution;
- cache purge execution;
- provider/backend/source-stat/source-read callbacks;
- source discovery;
- live/private source reads;
- unsupervised reads;
- service/listener/cron/startup behavior and recurring runner behavior;
- Runtime Registry consumption;
- global Hermes/MCP/client/runtime configuration mutation;
- credential/auth/env/keychain/OAuth/auth-file reads;
- provider/prod/canary authority;
- repository visibility changes;
- package publication;
- Atlas Gate movement and production-authoritative claims.

## Public/reportable hygiene constraints

Public issue, PR, test, and doc artifacts for this packet are report-safe. They
must not include raw private source text, credentials, auth/env/keychain
material, OAuth material, auth-file material, raw platform IDs, private absolute
paths, raw query payloads, raw payload content, or private correlation refs.

## Acceptance evidence

The companion tests prove this packet is discoverable, asks for exact future
approval language without implying approval, names one bounded implementation
slice, preserves residual holds, carries rollback/audit requirements, and stays
inside public hygiene constraints.
