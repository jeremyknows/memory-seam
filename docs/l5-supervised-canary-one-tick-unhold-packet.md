# L5.08 supervised canary one-tick unhold packet

This is a **NO-EXECUTION / NO-ACTIVATION decision packet** for a future bounded-runner canary. It drafts the human gate only. It does not run the bounded runner, schedule anything, does not start any service/listener, discover sources, perform live/private reads, consume Runtime Registry, mutate global configuration, or touch write/custody/reindex surfaces.

## Status

- Packet schema: `memory_seam_l5_supervised_canary_one_tick_unhold_packet_v0`
- Packet status: `DRAFT_PACKET_ONLY`
- Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`
- Activation authority: `HELD`
- Runner authority: `ONE_TICK_ONLY_AFTER_FUTURE_APPROVAL`
- Related readiness code: `src/memory_seam/l5_bounded_runner.py`
- Prior dependency: L5.07 default-off bounded runner readiness in `docs/l5-bounded-runner.md`

## Exact future canary scope

If Jeremy later gives the exact approval phrase below, the future canary is limited to:

| Field | Bound |
| --- | --- |
| Runner | `run_bounded_read_ticks(...)` invoked in-process only |
| Tick count | exactly one tick; `max_ticks=1` |
| Source family | `operator_supplied_project_doc_card` represented through the bounded-runner `project` family grant |
| Include/scope | metadata-only project-document source-card fields only |
| Subject | `agent:example` acting on one Jeremy/operator-supplied Memory Seam project-document source card |
| Allowed metadata fields | `title`, `document_kind`, `section_label`, `safe_summary`, `freshness_label`, `redacted_source_card_id` |
| Timeout | 30 seconds wall-clock for the one tick |
| Expiry | approval expires 30 minutes after Jeremy posts the exact phrase, or immediately after one tick, whichever comes first |
| Receipt target | a report-safe future canary receipt under `docs/` named for that future issue/PR |
| Runtime posture | no startup, no cron, no listener/service, no Runtime Registry, no global config mutation |
| Maximum reads | at most one metadata-only source-card read through the approved one-tick path |

The future approval does not grant a workspace scan, family scan, index query, broad recall, raw content read, source discovery pass, recurring runner, startup activation, provider/prod/canary authority beyond the one approved tick, Atlas Gate movement, repository visibility change, package publication, or any L6 write/custody/reindex behavior.

## Exact Jeremy approval phrase for a future canary tick

Jeremy must provide this exact phrase in the future issue/comment context before any canary tick can run:

> I approve Memory Seam to execute exactly one supervised bounded-runner canary tick under docs/l5-supervised-canary-one-tick-unhold-packet.md using one operator-supplied project-document source card, max_ticks=1, metadata-only fields only, a 30 second timeout, and a 30 minute approval expiry, with no source discovery, no raw content, no credential/auth/env/keychain/OAuth/auth-file reads, no service/listener/cron/startup activation, no Runtime Registry consumption, no global config mutation, no recurring or unsupervised reads, no provider/prod/canary authority beyond this one approved tick, no writes/custody/reindex, no repository visibility or package publication change, and no Atlas Gate movement.

Any variant, partial quote, implied approval, emoji reaction, merge, issue close, or approval for a different issue is insufficient. The phrase authorizes one supervised canary tick only after it appears in the future execution issue context. This L5.08 packet does not authorize execution by itself.

## Stop conditions

A future canary executor must stop before read or after the single permitted tick if any of these occur:

- exact approval phrase missing, altered, expired, or scoped to a different issue;
- source card is not operator supplied;
- more than one source card is present;
- requested fields exceed `title`, `document_kind`, `section_label`, `safe_summary`, `freshness_label`, or `redacted_source_card_id`;
- subject is not `agent:example` or the bounded runner grant does not match the packet;
- timeout would exceed 30 seconds wall-clock;
- bounded runner config requests `max_ticks` other than `1`;
- runtime returns denial, degraded/backend error, or unsafe hygiene finding;
- any credential/auth/env/keychain/OAuth/auth-file read would be required;
- source discovery, raw content, file-stat/backend/provider escape hatch, Runtime Registry, service/listener/cron/startup activation, global config mutation, write/custody/reindex, repository visibility/package publication, provider/prod authority, or Atlas Gate movement would occur.

## Rollback path

Rollback for the future one-tick canary is report-only and local:

1. Stop immediately after the single tick or earlier stop condition.
2. Do not retry broadly, reschedule, recurse, or activate any background runner.
3. Discard any non-report-safe transient value before writing a public artifact.
4. Preserve only the safe receipt fields, redaction labels, posture counters, stop condition, and usefulness/verifier outcome.
5. Leave default-off runner code and all held surfaces unchanged.

## Required future evidence after an approved canary tick

A future execution artifact must record, in report-safe form only:

- exact approval phrase location and expiry check;
- source family, include/scope, subject shape, timeout, and `max_ticks=1`;
- tick count attempted and completed;
- safe metadata fields returned or denial/degraded reason;
- usefulness/verifier verdict and redaction posture;
- denial/zero counters for source discovery, raw content, credential/auth/env/keychain/OAuth/auth-file reads, file-stat calls, read-backend calls, provider calls, Runtime Registry consumption, service/listener/cron/startup activation, global configuration mutation, recurring runner activation, provider/prod/canary authority beyond the one approved tick, write/custody/reindex, repository visibility/package publication, and Atlas Gate movement;
- confirmation that public artifacts contain no raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, or private correlation refs.

## Held surfaces preserved by this packet

This packet explicitly forbids startup activation, recurring unsupervised reads, broad canary behavior, writes/custody/reindex, provider/prod/canary authority beyond the one approved tick, Atlas Gate movement, Runtime Registry consumption, global Hermes/MCP/client/runtime configuration mutation, service/listener/cron activation, source discovery, live/private source reads before future approval, raw private source text, raw file paths, private absolute paths, raw platform IDs, raw query payloads, private correlation refs, credentials, auth/env/keychain/OAuth/auth-file material, repository visibility change, package publication, and production-authoritative claims.

## Verification

Required gate for this packet:

```bash
pytest -q
python scripts/public_hygiene_scan.py
python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py
git diff --check
```
