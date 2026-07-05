# L6W.04 local no-live supervised live-read approval smoke

Status: `LOCAL_SYNTHETIC_NO_LIVE_APPROVAL_SMOKE`

Parent: #6
Rail issue: #202
Prerequisite: #201 closed/PASS
Source floor: `9264533` or later on `origin/main`
Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`
Scaffold dependency: `docs/l6w01-supervised-live-read-approval-packet-scaffold.md`
Denial dependency: `docs/l6w02-supervised-live-read-approval-denial-matrix.md`
Receipt dependency: `docs/l6w03-supervised-live-read-receipt-output-contract.md`

This slice adds `examples/l6w_supervised_live_read_approval_no_live_smoke.py`, a local stdout-only smoke over committed synthetic metadata only for the L6W supervised live-read approval preparation rail. The smoke does not recognize approval, request approval, consume approval, or execute a live/private read. It proves that the current local posture remains held as `NO_APPROVAL_PRESENT` and `NO_APPROVAL_RECOGNIZED`; the smoke is held before provider/backend/source-stat/source-read callbacks.

The smoke is default-off, synthetic, no-live, and report-safe. It emits one compact stdout-only JSON object containing public-safe refs, source floor, upstream packet/doc refs, operation class, stop/status labels, descriptor/source-card refs, booleans, denial labels, validation errors, and synthetic zero counters.

## Local command

```bash
python examples/l6w_supervised_live_read_approval_no_live_smoke.py
```

The command returns exit code `0` only when the summary proves:

- `status=HELD_FOR_FUTURE_APPROVAL`
- `approval_status=NO_APPROVAL_PRESENT`
- `recognition_status=NO_APPROVAL_RECOGNIZED`
- `operation_count=0`
- `max_operation_count=1`
- `one_operation_binding=true`
- `metadata_only=true`
- `stdout_only=true`
- `non_persistent=true`
- `allowed=false`
- `allowed_result_count=0`
- `allowed_true_route_present=false`
- `callbacks_invoked=false`
- `live_read_invoked=false`
- `live_adapter_invoked=false`
- `source_discovery_attempted=false`
- `runtime_registry_consumed=false`
- `mutation_attempted=false`
- `persistence_attempted=false`
- `production_authority_claimed=false`
- `guarded_counters_zero=true`
- every guarded counter is present and exactly zero
- `denial_codes=["NO_APPROVAL_PRESENT"]`
- `validation_errors=[]`

## Held surfaces preserved

The smoke preserves no source discovery, no Runtime Registry consumption, no persistence, no activation, no production authority, no Atlas Gate movement, no mutation execution, and no `allowed=true` route. It does not expose raw source content, scan workspaces, scan source families, perform broad recall, query indexes, call source-stat/source-read, invoke provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks, read credentials/auth/env/keychain/OAuth/auth files, persist audit/custody/cache records, mutate caches, activate services/listeners/startup/cron paths, mutate global Hermes/MCP/client/runtime config, publish packages, change repository visibility, claim provider/prod/canary authority, move Atlas Gate, execute mutations, run rollback/cache-purge behavior, or create custody/write/delete/reindex behavior.

## Companion tests

`tests/test_l6w04_supervised_live_read_approval_no_live_smoke.py` imports the smoke helper directly and runs the CLI path through `subprocess`. The tests prove stdout-only JSON, source-card/descriptor citation refs, zero held counters, no stderr, no unsafe marker leakage, no live adapter invocation, no callbacks, no source discovery, no Runtime Registry consumption, no persistence, no production authority, and no `allowed=true` behavior.
