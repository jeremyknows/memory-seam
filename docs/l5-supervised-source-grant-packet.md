# L5.02 supervised source-grant decision packet

Issue #102 drafts the human-in-the-loop packet for the first L5 supervised metadata-only read. This document is a **NO-EXECUTION / NO-READ decision packet**: it does not authorize execution by itself, it does not discover sources, it does not read private content, and it does not start any service or recurring runner.

## Current decision state

- Packet status: `DRAFT_PACKET_ONLY`
- Execution authority: `HELD`
- Read authority: `HELD`
- Required next gate: Jeremy must provide the exact approval phrase in issue/PR context before issue #105 can execute exactly one supervised read.
- Source floor: this packet sits after L5.01, the metadata-only idle tick proof, and does not widen that proof into unsupervised reads.

## One bounded supervised read target

If Jeremy approves this packet later, the only proposed target is:

- Source family: `operator_supplied_project_doc_card`
- Subject shape: one Jeremy-supervised Memory Seam project-document source card selected by the human operator at execution time, with no source discovery by Memory Seam.
- Allowed include/scope: metadata-only card fields needed to prove reachability and usefulness posture: `title`, `document_kind`, `section_label`, `safe_summary`, `freshness_label`, and `redacted_source_card_id`.
- Explicitly excluded: raw document body, raw private source text, raw file paths, private absolute paths, raw platform IDs, raw query payloads, private correlation refs, credentials, auth/env/keychain/OAuth/auth-file material, attachment payloads, write/custody/reindex data, and any additional neighboring source cards.
- Maximum reads: exactly one supervised metadata-only source-card read.
- Timeout: 30 seconds wall-clock for the supervised read attempt.
- Output posture: report-safe receipt only, with safe booleans/counters, relative code/test artifact names, and redacted source-card identifiers.

This target is intentionally narrow. It does not grant a family scan, workspace walk, index query, backend search, broad recall, source discovery, or recurring read permission.

## Stop conditions

The later #105 execution must stop without retrying or broadening scope if any of the following occurs:

1. The exact approval phrase is absent or altered.
2. The selected target is not one operator-supplied project-document source card.
3. More than one source card would be read.
4. The adapter would read raw content instead of metadata-only card fields.
5. Any credential/auth/env/keychain/OAuth/auth-file access would occur.
6. Any source discovery, directory walk, file stat fan-out, backend search, Runtime Registry runtime consumption, service/listener activation, cron/startup behavior, global Hermes/MCP/client/runtime configuration mutation, provider/prod/canary authority, write/custody/reindex action, repository visibility change, package publication, Atlas Gate movement, or production-authoritative claim would occur.
7. Redaction cannot produce report-safe evidence without raw private source text, raw platform IDs, raw query payloads, private absolute paths, credentials, auth material, or private correlation refs.
8. The read attempt exceeds the 30 second timeout.

## Rollback and evidence boundary

Because #102 is documentation-only, rollback is simply reverting this packet and its tests. If a future #105 supervised read is approved and executed, rollback is to discard the one-run receipt artifact, close the execution lane as HOLD/FAIL, and make no persistent source, write-custody, reindex, service, cron, global config, Runtime Registry, provider/prod/canary, publication, or Atlas Gate change.

Expected #105 evidence must include:

- exact approval phrase provenance from issue/comment context;
- `read_attempted=true` only for the one approved supervised metadata-only source-card read;
- denial/zero counters for source discovery, credential/auth/env/keychain/OAuth/auth-file reads, service_started, runtime_registry_consumed, global_config_mutation, write_custody_or_reindex, recurring_runner_activated, provider_prod_canary_authority, and atlas_gate_moved;
- redaction assertion that public artifacts contain no raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, or private correlation refs.

## Exact approval phrase for #105

Jeremy can authorize only the one supervised read described above by posting this exact phrase in issue/comment context:

> I approve Memory Seam issue #105 to execute exactly one supervised metadata-only read of one operator-supplied project-document source card under docs/l5-supervised-source-grant-packet.md, with no source discovery, no raw content, no credential/auth/env/keychain/OAuth/auth-file reads, no service/listener/cron/startup activation, no Runtime Registry consumption, no global config mutation, no provider/prod/canary authority, no writes/custody/reindex, no repository visibility or package publication change, no Atlas Gate movement, and no recurring reads.

Any variant, partial quote, implied approval, emoji reaction, merge, issue close, or statement about the ladder is not sufficient authority. The phrase authorizes one supervised read only; it does not authorize unsupervised reads, recurring runner work, canaries, L6 write custody, release/publication, or production authority.

## Preserved held surfaces

This packet preserves all adjacent holds: service/listener activation, credential/auth/env/keychain/OAuth/auth-file reads, global Hermes/MCP/client/runtime configuration mutation, Runtime Registry runtime consumption, live/private source reads before #105 approval, source discovery, unsupervised reads, cron/startup activation, recurring runner/canary activation, writes/custody/reindex behavior, provider/prod/canary authority, repository visibility change, package publication, Atlas Gate movement, and production-authoritative claims.

## #102 local verifier gate

Before this packet can close/PASS, run:

- `pytest -q`
- `python scripts/public_hygiene_scan.py`
- `python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py`
- `git diff --check`
