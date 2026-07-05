# L6I.01/L6I.02/L6I.03/L6I.04 write-intent preflight gate skeleton, denial receipt metadata, approval-denial hardening, and no-production smoke

Status: `write_intent_preflight_gate_default_off_denies`
Slice: `L6_WRITE_INTENT_PREFLIGHT_GATE_SKELETON`
Parent: #6
Rail issues: #137, #138, #139, #140
Approval reference: `issue-137-comment-4643939613`
Decision basis: `docs/l6-first-implementation-slice-decision-packet.md`
Rollback/audit reference: `docs/l6-write-custody-rollback-audit-plan.md`

This L6I.01 write-intent preflight gate skeleton now carries the L6I.02
report-safe denial receipt metadata extension, the L6I.03 stale/mismatched
approval denial hardening tests, and the L6I.04 local synthetic no-production
smoke path.

This L6I.01 artifact is a default-off, synthetic, no-production gate for
operation class `write intent` only. It parses the operation class, emits
report-safe denial metadata, and denies before provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks.

The slice is limited to maximum `1` synthetic no-production operation. It does
not execute writes, custody transfer, delete, reindex, rollback, cache purge,
and does not perform provider/backend/source-stat/source-read callbacks. It also
does not perform live/private source reads, source discovery, unsupervised reads,
credential/auth/env/keychain/OAuth/auth-file reads, Runtime Registry
consumption, global configuration mutation, recurring activation, publication,
visibility changes, or Atlas Gate movement.

## Gate behavior

`run_write_intent_preflight_gate()` performs only:

1. report-safe operation-class normalization for `write intent`;
2. default-off denial metadata construction;
3. guarded-counter copying from the synthetic callback harness.

It never calls the callback bundle. The test harness callbacks fail fast if a
regression invokes them, and the accepted denial result requires these counters
to remain zero:

- `provider_calls`
- `backend_calls`
- `source_stat_calls`
- `source_read_calls`
- `write_callbacks`
- `custody_callbacks`
- `delete_callbacks`
- `reindex_callbacks`
- `rollback_callbacks`
- `cache_purge_callbacks`

Unsupported operation classes also deny before callbacks and do not consume the
single synthetic operation count.

## Approval-denial hardening

L6I.03 adds a report-safe synthetic approval context fixture and a negative
matrix for stale or mismatched approval signals. The validator checks only safe
metadata shape:

- approval reference matches `issue-137-comment-4643939613`;
- approval issue is `137`;
- actor association is `OWNER` without including raw actor/login IDs;
- approval operation class remains `write intent`;
- maximum synthetic operation count does not exceed `1`;
- approval window timestamps parse and the evaluation time is before expiry;
- raw approval text and raw actor IDs are not included.

The hardened matrix covers wrong issue, wrong actor association, wrong approval
reference, wrong approval operation class, exceeded max count, stale approval
window, and expired approval. Every case remains default-off, denied before the
callback bundle, leaves all guarded counters at zero, and emits only report-safe
denial receipt metadata.

## Report-safe denial receipt metadata

L6I.02 adds a report-safe `denial_receipt_metadata` object only on
`denied_no_mutation_path` results. The receipt metadata includes:

- safe operation class (`write intent` or `unsupported_operation_class`);
- denial reason code;
- counter summary with guarded counter count, `guarded_counters_zero`, and
  nonzero guarded counter count;
- approval reference shape naming a public issue-comment reference while setting
  `raw_approval_text_included` to `False`;
- rollback/audit reference shape naming the repository rollback/audit document
  while setting `raw_private_text_included` to `False`;
- residual holds copied from the held-surface list;
- report-safety flags that remain false for private text, credentials/auth
  material, private paths, raw platform IDs, raw query payloads, raw payload
  content, and private correlation refs.

The metadata builder returns no receipt for authorizing, callback-invoking, or
nonzero-counter inputs. It does not add a mutation, write, custody, delete,
reindex, rollback, cache purge, provider/backend, source-stat, or source-read
path.

## Local no-production smoke

L6I.04 adds `examples/write_intent_preflight_smoke.py`, a local wrapper over the
same default-off gate. It constructs exactly one committed synthetic request:

- operation class `write intent`;
- synthetic operation count `1`;
- `production` set to `False`;
- `payload_included`, `source_read_requested`, and `credential_read_requested`
  all set to `False`.

Running `python examples/write_intent_preflight_smoke.py` prints a compact JSON
summary with only report-safe denial facts: denial reason, operation class,
operation count, denial receipt shape, validation status, and guarded-counter
summary. The smoke asserts no production execution by leaving all guarded
counters at zero and preserving `allowed=False`, `denied_before_callback=True`,
and `callbacks_invoked=False`.

## Report-safe metadata only

Denial metadata may include schema/status strings, the slice name, the safe
approval reference, the rollback/audit doc reference, the canonical operation
class, boolean posture fields, and zero-counter facts. Public artifacts must not
include raw private source text, credentials, auth/env/keychain material, OAuth
material, auth-file material, raw platform IDs, private absolute paths, raw query
payloads, raw payload content, or private correlation refs.

## Residual holds

These surfaces remain held after this slice:

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

## Verification

Acceptance for this slice requires:

- tests proving denied paths leave all guarded counters at zero;
- report-safe docs and denial metadata;
- stale/mismatched approval denial matrix for #139;
- local synthetic no-production smoke for #140;
- rollback/audit reference preserved;
- public hygiene pass;
- local verification gate pass.
