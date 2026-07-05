# L6V.04 local no-live supervised proof smoke

Status: `LOCAL_SYNTHETIC_NO_LIVE_SMOKE`

Parent: #6  
Issue: #190  
Source floor: `876375b` or later on `origin/main`  
Upstream packet: `docs/l6u05-supervised-live-use-trust-boundary-review.md`  
Approval source: `fixture:l6v-supervised-source-card-approval-source:internal-review-2026`

This slice adds `examples/l6v_supervised_source_card_no_live_smoke.py`, a local stdout-only smoke over the committed synthetic L6V supervised source-card preflight fixtures. The smoke exercises exactly one recognized `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF` preflight using the issue #187 approval context fixture and reports the L6V.04 smoke issue (`#190`) separately from the preflight approval issue (`#187`).

The smoke is default-off, no-live, synthetic, and report-safe. It emits one compact JSON object containing only public-safe metadata: issue refs, source floor, upstream packet, operation class, status/status detail, descriptor/source-card refs, metadata/non-persistence booleans, approval denial codes, validation errors, and guarded zero counters.

## Local command

```bash
python examples/l6v_supervised_source_card_no_live_smoke.py
```

The command returns exit code `0` only when the summary proves:

- `recognized_operation=true`
- `preflight_ready=true`
- `operation_count=1`
- `max_operation_count=1`
- `metadata_only=true`
- `non_persistent=true`
- `allowed=false`
- `allowed_result_count=0`
- `allowed_true_route_present=false`
- `callbacks_invoked=false`
- `live_adapter_invoked=false`
- `mutation_attempted=false`
- `persistence_attempted=false`
- `guarded_counters_zero=true`
- all guarded counters are present and exactly zero
- `approval_denial_codes=[]`
- `validation_errors=[]`

## Held surfaces preserved

The smoke does not execute live/private reads, expose raw source content, discover sources, scan workspaces or source families, perform broad recall, query indexes, call source-stat/source-read, invoke provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks, read credentials/auth/env/keychain/OAuth/auth files, consume Runtime Registry data, persist audit/custody/cache records, mutate caches, activate services/listeners/startup/cron paths, mutate global Hermes/MCP/client/runtime config, publish packages, change repository visibility, claim provider/prod/canary or production authority, move Atlas Gate, execute mutations, or introduce any `allowed=true` route.

## Companion tests

`tests/test_l6v04_supervised_source_card_no_live_smoke.py` imports the smoke helper directly and runs the CLI path through `subprocess`. The tests prove stdout-only JSON, source-card/descriptor citation refs, zero held counters, no stderr, no raw unsafe marker leakage, no live adapter invocation, no callbacks, no persistence, and no `allowed=true` behavior.
