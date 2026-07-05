# F3 supervised-pull verifier packet

## Verdict

**F3 PASS — supervised source-card-first manual pull dogfood is complete for committed synthetic fixtures, and the next eligible lane is F4 no-service identity negative hardening only.**

This packet is a verifier/decision aid. It does **not** authorize issue `#6`, service/listener activation, startup injection, cron, broad recall authority, credential/auth/env/keychain/OAuth/auth-file reads, global Hermes/MCP/client/runtime configuration mutation, Runtime Registry runtime consumption, live/private source reads or source discovery, unsupervised reads, canaries, provider/prod authority, writes/custody/reindex/thread-retirement behavior, repository visibility changes, package publication, Atlas Gate movement, or production-authoritative claims.

## Source floor

- Repository: `jeremyknows/memory-seam`
- L4 closure floor: `8e23e9f Add final L4 closure review packet (#70)` or later.
- F2 verifier floor: `86cf112 Add F2 verifier packet (#91)`.
- F3 verifier floor at packet creation: `2394853 Add source-card usefulness proof packet (#93)`.
- Current selected issue: `#79` F3.03.
- Issues `#77` and `#78` are closed.
- Issue `#6` remains open and held unless Jeremy explicitly unholds it.

## F3 issue and PR evidence

| Issue | Status | PR evidence | CI evidence | Contribution |
| --- | --- | --- | --- | --- |
| `#77` F3.01 manual pull dogfood harness/runbook | closed | `#92` Add F3 manual pull dogfood runbook, merged as `2eb0310f50a585915698de7d9c7a4cc448280386` | GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed | Added `examples/manual_pull_dogfood.py` and `docs/f3-manual-pull-dogfood.md`, proving one manual source-card-first `/context` request and one `/recall` request over committed synthetic fixtures only. |
| `#78` F3.02 source-card usefulness proof packet | closed | `#93` Add source-card usefulness proof packet, merged as `23948532e73e9f4850ffb65766700b5afc4a7468` | GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed | Recorded PASS/HOLD/FAIL answerability outcomes, report-safe source-card IDs, degraded classifications, fallback avoidance, and no-live posture for the manual-pull proof. |
| `#79` F3.03 verifier packet | this packet | PR that lands this document | Must pass local verifier plus GitHub CI before merge | Collects F3 evidence, current issue state, residual holds, and next-lane decision. |

## Current open and held issue state

At F3 verifier creation, the open rail state is:

- `#79` F3.03: in progress by this packet.
- `#80` F4.01: next eligible target only after `#79` closes/PASS.
- `#81` F4.02 and `#82` F4.03: locked behind the preceding F4 issue order.
- `#83` F10.01 through `#85` F10.03: locked behind `#82` closing/PASS, unless the F4 verifier explicitly holds further F4 and says F10 hygiene is safe.
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
pytest -q tests/test_f3_verifier_packet.py
```

The PR that lands this packet must also pass GitHub CI before merge. Prior F3 PRs `#92` and `#93` each passed the repository's Python `pytest` matrix before merge.

## Trust-boundary finding

F3 preserved a no-live, source-card-first supervised pull invariant:

- The manual dogfood harness uses `synthetic_safe_content_provider()` and committed synthetic fixtures only.
- The context proof requires `source_card_count` of at least `2`, report-safe source-card IDs, useful read receipts, and no raw fallback.
- The recall proof requires a useful receipt while preserving the same safe posture.
- The usefulness packet records PASS/HOLD/FAIL outcomes without raw private source text, private absolute paths, raw platform IDs, raw query payloads, credentials, auth/env/keychain material, or private correlation references.
- The F3 path introduces no new live denial route. Equivalent no-live assertions are `raw_fallback_used=false`, `read_backend_called=false`, `service_started=false`, `runtime_registry_consumed=false`, and `write_custody_or_reindex=false`.
- If a future supervised-pull packet adds a negative path, it must prove denial before source/provider/file/stat/backend reads with zero counters or equivalent monkeypatch/spy assertions before it can be recorded as PASS.

## Holds preserved after F3

F3 closes only supervised, manual, read-only, source-card-first dogfood over committed synthetic fixtures. The following remain held:

- `#6` L5/L6 unsupervised read ladder and write-custody companion.
- Startup injection and cron.
- Broad recall authority.
- Service/listener activation or installation.
- Credential/auth/env/keychain/OAuth/auth-file reads.
- Global Hermes/MCP/client/runtime configuration mutation.
- Runtime Registry runtime consumption.
- Live/private source reads or source discovery.
- Unsupervised reads, canaries, provider/prod authority.
- Writes, custody, reindex, thread-retirement behavior.
- Repository visibility changes and package publication.
- Atlas Gate movement or production-authoritative claims.

## Next-lane decision

Proceed to **`#80` F4.01: no-service identity negative matrix** after this packet lands, local verification passes, GitHub CI passes, and issue `#79` closes/PASS.

F4 should remain no-service identity hardening only: in-process verifier semantics, forged-subject/wrong-audience/expired-token/query-body-mismatch/confused-deputy negatives, denial before provider/source/file/stat/backend reads, no persistent listener, no credential store reads, no live/private source reads, no Runtime Registry runtime consumption, no writes/custody/reindex, no provider/prod/canary authority, no Atlas Gate movement, and no repository visibility or package-publication decision.
