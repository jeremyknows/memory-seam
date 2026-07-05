# L5.04 supervised one-read runbook and dry-run harness

Issue #104 builds the local command shape for the future #105 supervised metadata-only read. This runbook and helper are **DRY-RUN / NO-EXECUTION / NO-READ** artifacts. They do not authorize #105, do not perform source discovery, do not read live/private sources, do not inspect credentials or environment secrets, and do not start service/listener/cron/startup behavior.

## Current decision state

- Packet status: `DRY_RUN_HARNESS_ONLY`
- Execution authority: `HELD_FOR_105`
- Read authority: `HELD_FOR_105`
- Default behavior: dry-run/no-exec
- Required gate before any real read: Jeremy must post the exact approval phrase from `docs/l5-supervised-source-grant-packet.md` in issue/comment context for #105.

## One bounded supervised read path

The helper is pinned to exactly the bounded path from the L5.02 packet:

- Source family: `operator_supplied_project_doc_card`
- Subject shape: one operator-supplied Memory Seam project-document source card selected by the human operator at execution time, with no source discovery by Memory Seam.
- Include/scope: `title`, `document_kind`, `section_label`, `safe_summary`, `freshness_label`, and `redacted_source_card_id`.
- Timeout: 30 seconds wall-clock for the future supervised read attempt.
- Redaction posture: report-safe metadata only; no raw private source text, raw platform IDs, raw query payloads, credentials/auth material, private absolute paths, or private correlation refs.
- Receipt target: `docs/l5-supervised-one-read-receipt.md` as a future #105 artifact only.

## Dry-run command

From the repository root:

```bash
python scripts/l5_supervised_one_read.py
```

The dry-run output shows the intended source family, include/scope, subject shape, timeout, redaction posture, receipt target, stop conditions, rollback posture, and explicit zero counters for provider/source/file-stat/backend calls. It does not read sources.

## Execution preflight shape for #105

This #104 helper refuses execution before read unless `--execute` and an exact approval phrase are supplied. Even when the phrase matches, #104 remains no-exec and returns `APPROVAL_MATCHED_BUT_EXECUTION_HELD_FOR_105`; the later #105 issue owns any actual supervised one-read execution receipt after explicit approval exists in issue/comment context.

The copy/paste shape for a future #105 preflight is:

```bash
python scripts/l5_supervised_one_read.py \
  --execute \
  --approval-phrase 'I approve Memory Seam issue #105 to execute exactly one supervised metadata-only read of one operator-supplied project-document source card under docs/l5-supervised-source-grant-packet.md, with no source discovery, no raw content, no credential/auth/env/keychain/OAuth/auth-file reads, no service/listener/cron/startup activation, no Runtime Registry consumption, no global config mutation, no provider/prod/canary authority, no writes/custody/reindex, no repository visibility or package publication change, no Atlas Gate movement, and no recurring reads.'
```

Any missing, altered, partial, implicit, emoji, merge, close, or ladder-level approval is denied before read.

## Stop conditions

A future #105 execution must stop without retrying or widening scope if any of these occur:

1. The exact approval phrase is absent or altered.
2. The target is not one operator-supplied project-document source card.
3. More than one source card would be read.
4. The adapter would read raw content instead of metadata-only card fields.
5. Any credential/auth/env/keychain/OAuth/auth-file access would occur.
6. Any source discovery, directory walk, file stat fan-out, backend search, Runtime Registry consumption, service/listener activation, cron/startup behavior, global configuration mutation, provider/prod/canary authority, write/custody/reindex action, repository visibility change, package publication, Atlas Gate movement, or production-authoritative claim would occur.
7. Redaction cannot produce public-safe evidence.
8. The attempt exceeds 30 seconds wall-clock.

## Rollback

For #104, rollback is reverting this runbook, helper, and tests. For a future approved #105 read, rollback is to stop without retrying, discard any one-run receipt draft, mark the lane HOLD/FAIL, and make no persistent source, write/custody/reindex, service, cron, global config, Runtime Registry, provider/prod/canary, publication, or Atlas Gate change.

## Held surfaces preserved

The #104 harness preserves: no source discovery, no source reads, no credential/auth/env/keychain/OAuth/auth-file reads, no Runtime Registry consumption, no global config mutation, no service/listener/cron/startup activation, no provider/prod/canary authority, no recurring runner/canary activation, no writes/custody/reindex, no repository visibility or package publication change, no Atlas Gate movement, and no production-authoritative claims.
