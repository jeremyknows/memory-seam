# L5.07 bounded recurring runner design without activation

This packet defines the default-off bounded runner shape for future repeated Memory Seam reads. It is readiness only. It does **not** schedule a cron job, install a startup hook, start a service/listener, consume Runtime Registry, mutate global MCP/client/runtime config, perform unsupervised reads, or unhold write/custody/reindex behavior.

## Status

- Schema: `memory_seam_l5_bounded_runner_v0`
- Status label: `default_off_bounded_runner_readiness_only`
- Implementation: `src/memory_seam/l5_bounded_runner.py`
- Tests: `tests/test_l5_bounded_runner.py`

## Runner shape

The runner can only be invoked in-process by calling `run_bounded_read_ticks(runtime, config, current_tick=...)`. It has no background loop and no activation path.

Required config before any tick can be attempted:

| Field | Requirement | Held-surface purpose |
| --- | --- | --- |
| `enabled` | Must be `True`; default is `False`. | Merely importing or constructing the runner cannot read. |
| `execution_approved` | Must be `True`; default is `False`. | Future canary/HITL approval remains separate from readiness code. |
| `grant` | Must be a `BoundedReadGrant`. | No implicit source family, subject, or include scope. |
| `grant.metadata_only` | Must be `True`. | Raw/private content reads remain held. |
| `grant.source_family` | Currently limited to `project`. | No broad source discovery or family expansion. |
| `grant.include_scope` | Currently limited to `project`. | No unsupported include/scope expansion. |
| `max_ticks` | 1 through 5. | Finite repeat count; no unbounded recurring loop. |
| `expires_after_tick` | Must be at or after the supplied `current_tick`. | Expiry is checked before and during the loop. |
| `recursion_guard_token` | Denies if already active. | Anti-recursion protection. |

## Stop conditions

The runner stops and returns a metadata-only receipt when any of these occur:

- runner default-off;
- execution approval missing;
- explicit source grant missing;
- metadata-only flag missing;
- finite repeat count invalid;
- expiry reached before or during the run;
- anti-recursion guard already active;
- unsupported source family or include scope;
- write-like/custody/reindex/purge term in the source family or include scope;
- runtime denial when `stop_on_denial=True`;
- runtime exception when `stop_on_error=True`.

## Receipt posture

Every receipt includes posture evidence that the runner itself performed none of the held actions:

- `service_started=false`
- `cron_or_startup_created=false`
- `runtime_registry_consumed=false`
- `global_config_mutation=false`
- `source_discovery_called=false`
- `credential_auth_env_keychain_authfile_reads=false`
- `file_stat_calls=0`
- `provider_prod_canary_authority=false`
- `write_custody_or_reindex=false`
- `atlas_gate_movement=false`

The receipt also carries `authority_note=readiness_only_not_unsupervised_or_recurring_unhold`.

## Future canary boundary

This issue does not authorize #108 or any canary tick. A future one-tick canary packet must still name exact scope, source family, subject, timeout, expiry, stop conditions, rollback, and the exact Jeremy approval phrase before any canary execution. Startup activation, broad recurring unsupervised reads, write/custody/reindex, provider/prod/canary authority beyond the one approved tick, repository visibility/package publication changes, and Atlas Gate movement remain held.

## Verification

Required gate for this packet:

```bash
pytest -q
python scripts/public_hygiene_scan.py
python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py
git diff --check
```
