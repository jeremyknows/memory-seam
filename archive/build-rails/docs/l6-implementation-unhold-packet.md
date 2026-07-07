# L6.04 implementation unhold packet

Status: `HITL_DECISION_PACKET_ONLY`.

Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`.

This packet packages the L6 decision point after the L5 supervised-read ladder and the L6 write-custody companion. It is documentation only: it does not implement, enable, schedule, simulate, or execute write, custody transfer, delete, reindex, rollback, service/listener activation, source discovery, live/private source reads, provider/prod/canary authority, repository visibility changes, package publication, Atlas Gate movement, or production-authoritative claims.

## Completed evidence

| Slice | Evidence now on `origin/main` | Decision-only takeaway |
| --- | --- | --- |
| L5.01 no-source-read idle tick | `docs/l5-idle-tick-contract.md`; `tests/test_l5_idle_tick_contract.py` | Idle checks are metadata-only and prove zero source/provider/file-stat/backend reads. |
| L5.02 supervised source-grant packet | `docs/l5-supervised-source-grant-packet.md`; `tests/test_l5_supervised_source_grant_packet.py` | One future supervised metadata-only project-doc source-card read required exact Jeremy approval. |
| L5.03 denied-before-read spy harness | `tests/test_l5_denied_before_read_spy_harness.py` | Denied read paths stop before provider/source/file-stat/read-backend/Runtime Registry callbacks. |
| L5.04 supervised one-read runbook | `docs/l5-supervised-one-read-runbook.md`; `scripts/l5_supervised_one_read.py`; `tests/test_l5_supervised_one_read_runbook.py` | The helper defaults to dry-run/no-exec and denies altered approvals before read surfaces. |
| L5.05 supervised one-read receipt | `docs/l5-supervised-one-read-receipt.md`; `tests/test_l5_supervised_one_read_receipt.py` | The approved read produced a report-safe metadata-only receipt and preserved write/custody/Gate holds. |
| L5.06 post-read verifier | `docs/l5-post-read-verifier.md`; `scripts/l5_post_read_verifier.py`; `tests/test_l5_post_read_verifier.py` | Usefulness and redaction checks consume committed receipt evidence without additional reads. |
| L5.07 bounded recurring runner design | `docs/l5-bounded-runner.md`; `tests/test_l5_bounded_runner.py` | Bounded ticks are readiness-only, default-off, finite, approval-bound, and not activated. |
| L5.08 canary one-tick unhold packet | `docs/l5-supervised-canary-one-tick-unhold-packet.md`; `tests/test_l5_supervised_canary_one_tick_unhold_packet.py` | A future one-tick canary still requires exact Jeremy approval and preserves activation/write/Gate holds. |
| L6.01 write-intent threat model | `docs/l6-write-intent-threat-model.md`; `tests/test_l6_write_intent_threat_model.py` | Write intent, custody, delete, reindex, cache purge, rollback, and read-receipt boundaries are defined; runtime write-like surfaces remain unsupported. |
| L6.02 write-like route denial matrix | `tests/test_l6_write_like_denial_matrix.py` | Write-like routes and custody-shaped payloads fail closed before read/provider/backend/source-stat/custody/reindex callbacks. |
| L6.03 custody receipt no-op fixtures | `src/memory_seam/custody_receipts.py`; `docs/l6-custody-receipt-noop-fixtures.md`; `tests/test_l6_custody_receipt_noop_fixtures.py` | Metadata-only custody receipt shapes exist as no-op fixtures; actual implementation remains held. |

## Remaining risk

1. **Mutation blast radius remains unresolved.** Any real write/custody/reindex implementation could affect memory/source/index state and needs a separately reviewed rollback, audit, approval, and owner model.
2. **Approval spoofing and stale approvals remain risks.** Any future unhold must bind to an issue number, exact phrase, expiry, actor, operation class, max operation count, and report-safe approval reference.
3. **Private data leakage remains a public-artifact risk.** Future receipts must continue to exclude raw private source text, credentials, auth/env/keychain/OAuth/auth-file material, private absolute paths, raw platform IDs, raw query/payload content, and private correlation refs.
4. **Provider/backend side effects remain held.** Denial and preflight evidence must keep zero source-read, source-stat, provider, backend, custody, reindex, rollback, and write counters until a named implementation slice is explicitly approved.
5. **Operational activation remains separate.** Cron/startup/service/listener/canary/recurring runner activation is not included in any L6 implementation decision unless Jeremy names that surface in a later approval.

## Decision choices

### Choice A — HOLD

Keep all L6 implementation surfaces held. Continue using only the current docs, tests, no-op fixtures, and denial matrices. This is the safest choice when there is no immediate write/custody need.

Exact language to choose HOLD:

> I choose HOLD for L6 write/custody implementation. Keep Memory Seam read-only and implementation-held; do not implement writes, custody transfer, delete, reindex, rollback, activation, source discovery, provider/prod/canary authority, publication, visibility changes, or Atlas Gate movement.

### Choice B — SPLIT

Approve only a new planning/design issue, not implementation. The next slice may refine schema, ownership, rollback planning, or audit review while still adding no write/custody/reindex behavior.

Exact language to choose SPLIT:

> I choose SPLIT for L6. Create a new bounded AFK planning issue for [name the exact non-executing slice] using docs/l6-implementation-unhold-packet.md as context. The slice may update docs/tests/schema fixtures only and must not implement or execute writes, custody transfer, delete, reindex, rollback, service/listener/cron/startup activation, source discovery, live/private reads, provider/prod/canary authority, publication, visibility changes, or Atlas Gate movement.

### Choice C — APPROVE ONE IMPLEMENTATION SLICE

Approve exactly one future implementation slice. This packet does not perform the slice; it only defines the language a future issue must contain before work may start.

Exact language required before any future implementation work:

> I approve Memory Seam to implement exactly one bounded L6 write/custody slice named [exact slice name] under issue #[issue number] and docs/l6-implementation-unhold-packet.md. The approved slice is limited to [operation class: write intent / custody receipt persistence / delete / reindex / rollback / cache purge], with maximum [number] operations, no production execution, no recurring runner/canary/startup/cron/service/listener activation, no Runtime Registry consumption, no global Hermes/MCP/client/runtime configuration mutation, no credential/auth/env/keychain/OAuth/auth-file reads, no source discovery, no live/private source reads unless separately named, no provider/prod/canary authority beyond the named slice, no repository visibility change, no package publication, and no Atlas Gate movement. The implementation must preserve denial-before-callback tests with zero provider/backend/source-stat/source-read/write/custody/reindex/rollback counters on denied paths, emit only report-safe receipts, and stop when approval expires at [timestamp or duration].

Any variant, partial quote, implied approval, merge event, issue close, emoji reaction, or unrelated comment is not implementation approval.

## Preserved held surfaces

Unless Jeremy posts exact future approval for a named next slice, these surfaces remain held:

- write/custody/reindex/delete/cache-purge/rollback behavior;
- service/listener/cron/startup activation and recurring unsupervised reads;
- live/private source reads, unsupervised reads, and source discovery;
- credential/auth/env/keychain/OAuth/auth-file reads;
- Runtime Registry consumption;
- global Hermes/MCP/client/runtime configuration mutation;
- provider/prod/canary authority;
- repository visibility change and package publication;
- Atlas Gate movement and production-authoritative claims;
- public artifacts containing raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, or private correlation refs.

## Future acceptance bar after approval

A future implementation issue, if explicitly approved, must include:

- exact approval phrase location, actor, issue number, expiry, and report-safe approval reference;
- operation class, custody owner, max operation count, timeout, rollback plan, and stop conditions;
- denial-before-callback tests proving zero provider/backend/source-stat/source-read/write/custody/reindex/rollback counters on denied paths;
- public hygiene proof for receipts, docs, PRs, and issue comments;
- a no-production-execution verification path unless Jeremy separately approves execution;
- explicit statement that this L6.04 packet alone is not approval.

## Verification

`tests/test_l6_implementation_unhold_packet.py` proves this packet remains decision-only, exposes approve/hold/split choices with exact future language, preserves held surfaces, records completed evidence and remaining risk, and is discoverable from the documentation index and contract-test inventory.
