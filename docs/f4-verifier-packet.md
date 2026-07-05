# F4 no-service identity verifier packet

## Verdict

**F4 PASS — no-service identity hardening is complete for the committed in-process fixture authority surface, and the next eligible lane is F10 public/private hygiene preparation only.**

This packet is a verifier/decision aid. It does **not** authorize issue `#6`, service/listener activation or installation, localhost binding, startup injection, cron, broad recall authority, credential/auth/env/keychain/OAuth/auth-file reads, global Hermes/MCP/client/runtime configuration mutation, Runtime Registry runtime consumption, live/private source reads or source discovery, unsupervised reads, canaries, provider/prod authority, writes/custody/reindex/thread-retirement behavior, repository visibility changes, package publication, Atlas Gate movement, or production-authoritative claims.

## Source floor

- Repository: `jeremyknows/memory-seam`
- L4 closure floor: `8e23e9f Add final L4 closure review packet (#70)` or later.
- F2 verifier floor: `86cf112 Add F2 verifier packet (#91)`.
- F3 verifier floor: `cd6b979 Add F3 supervised-pull verifier packet`.
- F4 negative-matrix floor: `f278146 Add no-service identity negative matrix (#95)`.
- F4 semantics floor at packet creation: `f50781f Add no-service identity semantics note (#96)`.
- Current selected issue: `#82` F4.03.
- Issues `#80` and `#81` are closed.
- Issue `#6` remains open and held unless Jeremy explicitly unholds it.

## F4 issue and PR evidence

| Issue | Status | PR evidence | CI evidence | Contribution |
| --- | --- | --- | --- | --- |
| `#80` F4.01 no-service identity negative matrix | closed | `#95` Add no-service identity negative matrix, merged as `f278146329f25182a7c2832963a255cd8d5dae00` | GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed | Added `tests/test_no_service_identity_negative_matrix.py`, covering forged subject, wrong audience/scope, expired/invalid fixture token shape, query/body mismatch, confused-deputy routing, and no-service health posture. |
| `#81` F4.02 no-service identity semantics note | closed | `#96` Add no-service identity semantics note, merged as `f50781ffe97659282be81733e892862f1f895cb9` | GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed | Added `docs/no-service-identity-semantics.md`, defining caller subject, acting-for, audience/scope, descriptor subject, query/body mismatch, denial-before-read evidence, and explicit cannot-prove boundaries. |
| `#82` F4.03 verifier packet | this packet | PR that lands this document | Must pass local verifier plus GitHub CI before merge | Collects F4 evidence, current issue state, residual holds, and next-lane decision. |

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
pytest -q tests/test_f4_verifier_packet.py
```

The PR that lands this packet must also pass GitHub CI before merge. Prior F4 PRs `#95` and `#96` each passed the repository's Python `pytest` matrix before merge.

## Trust-boundary finding

F4 preserved a local, in-process, no-service identity invariant:

- Identity authority is fixture/verifier output plus request metadata intersection, not request-body assertions, query smuggling, ambient process identity, descriptor presence, or acting-for metadata alone.
- The negative matrix proves forged subject, wrong audience, wrong scope, expired token shape, invalid token shape, query/body agent mismatch, query/body include mismatch, and confused-deputy worker recall are denied before provider/backend reads.
- Public test evidence includes the `ReadSpyProvider` and the explicit assertion `provider.read_calls == 0`, which is equivalent zero source-read/stat/backend counter evidence for the exercised identity-denial paths.
- No persistent listener or service has been started, installed, authorized, or required by F4.
- F4 did not read credentials, auth files, env secrets, keychains, OAuth stores, Runtime Registry entries, live sources, private sources, source discovery surfaces, provider/prod surfaces, or write/custody/reindex paths.
- F4 receipts and health posture remain metadata-only and preserve `service_started=false`, `service_start_allowed=false`, `runtime_registry_consumed=false`, `audit_persisted=false`, and `write_custody_or_reindex=false`.

## Current open and held issue state

At F4 verifier creation, the open rail state is:

- `#82` F4.03: in progress by this packet.
- `#83` F10.01 public/private hygiene inventory: next eligible target only after this packet lands, local verification passes, GitHub CI passes, and issue `#82` closes/PASS.
- `#84` F10.02 and `#85` F10.03: locked behind the preceding F10 issue order.
- `#6` L5/L6: HOLD unless Jeremy explicitly unholds it.

## Holds preserved after F4

F4 closes only no-service identity negative hardening and semantics for committed synthetic fixtures. The following remain held:

- `#6` L5/L6 unsupervised read ladder and write-custody companion.
- Startup injection and cron.
- Broad recall authority.
- Service/listener activation, installation, localhost binding, or persistent runtime execution.
- Credential/auth/env/keychain/OAuth/auth-file reads or real external identity-provider verification.
- Global Hermes/MCP/client/runtime configuration mutation.
- Runtime Registry runtime consumption.
- Live/private source reads or source discovery.
- Unsupervised reads, canaries, provider/prod authority.
- Writes, custody, reindex, thread-retirement behavior, or persistent audit-sink writes.
- Repository visibility changes and package publication.
- Atlas Gate movement or production-authoritative claims.

## F5 design-only recommendation

F4 does **not** unlock F5 execution. Any later F5 packet should remain design-only unless Jeremy separately and explicitly authorizes a service/listener boundary. A safe future F5 design-only packet may define proposed localhost-only service semantics, explicit start/stop proof requirements, kill-switch and rollback evidence, metadata-only audit-sink constraints, and denial-before-read identity requirements, while keeping service activation, credential reads, Runtime Registry consumption, live/private reads, writes/custody/reindex, provider/prod/canary authority, publication, and Gate movement held.

## Next-lane decision

Proceed to **`#83` F10.01: public/private hygiene inventory** after this packet lands, local verification passes, GitHub CI passes, and issue `#82` closes/PASS.

F10 should stay hygiene/prep only: inventory public/private artifact classes, package boundary docs, release hold evidence, scanner results, and private provenance quarantine. It must not change repository visibility, publish a package, expose private Atlas fixtures, read credentials or live sources, activate services/listeners, consume Runtime Registry, perform writes/custody/reindex, or move Atlas Gate status.
