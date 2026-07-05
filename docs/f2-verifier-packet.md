# F2 verifier packet

## Verdict

**F2 PASS — portable policy/control-plane schema hardening is complete for the collapsed F2 tranche, and the next eligible lane is F3 supervised pull dogfood only.**

This packet is a verifier/decision aid. It does **not** authorize issue `#6`, L5/L6 implementation, service/listener activation, credential/auth/env/keychain/OAuth/auth-file reads, global Hermes/MCP/client/runtime configuration mutation, Runtime Registry runtime consumption, live/private source reads or source discovery, unsupervised reads, cron/startup activation, canaries, provider/prod authority, writes/custody/reindex/thread-retirement behavior, repository visibility changes, package publication, Atlas Gate movement, or production-authoritative claims.

## Source floor

- Repository: `jeremyknows/memory-seam`
- L4 closure floor: `8e23e9f Add final L4 closure review packet (#70)` or later.
- F2 verifier floor at packet creation: `6e9b05a Add F2 policy semantics decision note (#90)`.
- Current selected issue: `#76` F2.06.
- Issues `#71` through `#75` are closed.
- Issue `#6` remains open and held unless Jeremy explicitly unholds it.

## F2 issue and PR evidence

| Issue | Status | PR evidence | CI evidence | Contribution |
| --- | --- | --- | --- | --- |
| `#71` F2.01 schema contract consolidation | closed | `#86` Add portable schema contract consolidation, merged as `9072d9514fc177cfa8b0cf9932a191573ea0b970` | GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed | Consolidated descriptor, grant/control-plane, receipt/source-floor, degraded/no-live, and disclosure-label contracts; blank/missing grants and unknown families deny by default before source materialization. |
| `#72` F2.02 denial fixture matrix | closed | `#87` Add denial fixture matrix, merged as `c7c34448afeef8fb9933cb9d891a3656952dd3a1` | GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed | Added table-driven negative coverage for unknown family, blank grant, missing descriptor, disabled grant, subject mismatch, and audience/scope mismatch with explicit zero-read/stat/backend/provider evidence. |
| `#73` F2.03 router parser and redaction edge cases | closed | `#88` Add router redaction edge-case tests, merged as `58a2b88966a9d95f46cbfcd2e01bc81cc46b94d9` | GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed | Covered malformed/repeated read-receipt params, unexpected endpoints/methods, numeric parsing denials, degraded/no-live labels, and unsafe fragment rejection while preserving no-live/read-only behavior. |
| `#74` F2.04 adapter import-boundary compatibility | closed | `#89` Add adapter import-boundary compatibility proof, merged as `eed1c4389a7a418e49d5395b13656d29d127dda6` | GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed | Proved Memory Seam core imports stay package-local/stdlib-only and downstream adapters depend on the package rather than reversing the dependency into core. |
| `#75` F2.05 policy semantics decision note | closed | `#90` Add F2 policy semantics decision note, merged as `6e9b05a281b048648a30f6a34b16b17d5d98db21` | GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed | Recorded fail-closed descriptor/grant intersection semantics, reportable-safe denial reasons, no-live source-floor labels, held authority, and the F3 unlock condition. |
| `#76` F2.06 verifier packet | this packet | PR that lands this document | Must pass local verifier plus GitHub CI before merge | Collects F2 evidence, current issue state, residual holds, and next-lane decision. |

## Current open and held issue state

At F2 verifier creation, the open rail state is:

- `#76` F2.06: in progress by this packet.
- `#77` F3.01: next eligible target only after `#76` closes/PASS.
- `#78` F3.02: locked behind `#77`.
- `#79` F3.03: locked behind `#78`.
- `#80` F4.01 through `#82` F4.03: locked behind `#79` closing/PASS.
- `#83` F10.01 through `#85` F10.03: locked behind `#82` closing/PASS or an explicit F4 verifier hold/safe-hygiene decision.
- `#6` L5/L6: HOLD unless Jeremy explicitly unholds it.

## Verifier commands

The full local verifier for this packet is:

```bash
pytest -q
python scripts/public_hygiene_scan.py
python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py
git diff --check
```

Focused verifier for this issue:

```bash
pytest -q tests/test_f2_verifier_packet.py
```

The PR that lands this packet must also pass GitHub CI before merge. Prior F2 PRs `#86` through `#90` each passed the repository's Python `pytest` matrix before merge.

## Trust-boundary finding

F2 preserved denial-before-read as a tranche invariant:

- Schema contract consolidation denies blank/missing grants and unknown families before source stat/backend/provider reads.
- The denial fixture matrix asserts zero source-read, stat, backend, and provider counters for named negative cases.
- Router/parser edge cases reject malformed, unsupported, or write-like paths before handler/provider/source/backend reads.
- Import-boundary coverage keeps live/downstream adapter surfaces outside the portable core.
- Policy semantics record descriptor registration and grant authority as an intersection, not a union, with reportable denial reasons that avoid raw/private details.

Public/reportable artifacts for F2 should remain free of raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, and private correlation references.

## Holds preserved after F2

F2 closes only portable policy/control-plane schema hardening. The following remain held:

- `#6` L5/L6 unsupervised read ladder and write-custody companion.
- Service/listener activation or installation.
- Credential/auth/env/keychain/OAuth/auth-file reads.
- Global Hermes/MCP/client/runtime configuration mutation.
- Runtime Registry runtime consumption.
- Live/private source reads or source discovery.
- Unsupervised reads, cron/startup activation, canaries, provider/prod authority.
- Writes, custody, reindex, thread-retirement behavior.
- Repository visibility changes and package publication.
- Atlas Gate movement or production-authoritative claims.

## Next-lane decision

Proceed to **`#77` F3.01: manual pull dogfood harness/runbook** after this packet lands, local verification passes, GitHub CI passes, and issue `#76` closes/PASS.

F3 should remain design/runbook/supervised-pull only: manual, read-only, source-card-first, no startup injection, no cron, no broader recall authority, no writes/custody/reindex, no service/listener, no Runtime Registry runtime consumption, no provider/prod/canary, no Atlas Gate movement, and no repository visibility or package-publication decision.
