# Downstream integration smoke plan

This plan defines a no-mutation smoke for downstream consumers that import the standalone Memory Seam package. It is a planning and verification artifact only: it does not start services/listeners, mutate global Hermes/MCP/runtime configuration, read credentials/auth stores/keychains/secrets, discover private sources, perform live/private reads, consume Runtime Registry, publish packages, change repository visibility, or add write/custody/reindex behavior.

## Scope

Use this plan after a local package build, editable install, or private wheel install to prove a downstream checkout can import and exercise Memory Seam through synthetic/no-live surfaces.

Downstream examples:

- an Atlas Query adapter checkout;
- a Hermes consumer fixture;
- a temporary clean clone used only for import/smoke verification.

Do not run this plan against pinned production read-source clones as a write target. Use a clean dev worktree or disposable temporary checkout when the smoke needs files.

## Inputs

- Memory Seam checkout or local wheel artifact.
- Downstream checkout path represented as `<DOWNSTREAM_CHECKOUT>` in commands.
- Fresh virtual environment or isolated Python environment.
- No credentials or private source roots.

## Smoke A — package import from downstream checkout

Run from the downstream checkout after installing Memory Seam locally:

```bash
python - <<'PY'
from memory_seam import (
    CONTRACT_STATUS,
    NullMemorySeamProvider,
    provider_handlers,
    route_request,
    synthetic_safe_content_provider,
)

provider = synthetic_safe_content_provider()
handlers = provider_handlers(provider)
health = route_request('GET', '/health', **handlers)
context = route_request(
    'GET',
    '/context?include=project,memory&mode=downstream-smoke&agent=smoke&read_receipt=metadata_only',
    **handlers,
    token_subject='agent:smoke',
    allowed_scopes=['context:project', 'context:memory'],
)
recall = route_request(
    'GET',
    '/recall?query=runtime+identity+rollback&scope=wiki&n=2&read_receipt=metadata_only',
    **handlers,
    token_subject='agent:smoke',
    allowed_scopes=['wiki'],
)
null_health = NullMemorySeamProvider().health()
assert CONTRACT_STATUS in health['body']['contract_status']
assert context['status_code'] == 200
assert recall['status_code'] == 200
for body in (health['body'], context['body'], recall['body'], null_health):
    assert body['service_started'] is False
    assert body['runtime_registry_consumed'] is False
    assert body['write_custody_or_reindex'] is False
print('memory-seam downstream no-live smoke ok')
PY
```

Expected output:

```text
memory-seam downstream no-live smoke ok
```

## Smoke B — downstream adapter boundary check

If the downstream checkout has an adapter wrapper, inspect only committed source and run its local no-live tests. The wrapper should import Memory Seam package surfaces instead of copying core contracts.

Minimum checks:

```bash
python - <<'PY'
import importlib
for name in ['memory_seam', 'memory_seam.contracts', 'memory_seam.providers', 'memory_seam.router']:
    importlib.import_module(name)
print('memory-seam package imports ok')
PY
```

If the downstream repo has a focused no-live adapter test, run that test directly. Do not run broad commands that start services, mutate global config, or require credentials.

## Smoke C — rollback and cleanup

Rollback is local-only:

1. deactivate/remove the temporary virtual environment;
2. remove the disposable downstream checkout if one was created;
3. leave global Hermes/MCP/client configuration untouched;
4. do not delete or mutate pinned production read-source clones.

## Held authority boundaries

This plan keeps these surfaces held:

- service/listener activation;
- credential/auth/env/keychain reads;
- Runtime Registry runtime consumption;
- global client/runtime/MCP configuration mutation;
- live/private source reads and source discovery;
- unsupervised reads, cron/startup activation, or canaries;
- writes, custody, reindex, and thread-retirement behavior;
- provider/prod/Gate movement;
- package publication or repository visibility changes.

## Acceptance checklist

- Package imports succeed from the downstream checkout.
- Synthetic context and recall responses return status `200`.
- Safe posture fields remain false: service start, Runtime Registry consumption, write/custody/reindex.
- Any downstream adapter test is no-live/read-only and uses local committed fixtures.
- Rollback is limited to temporary environment/checkouts.
- No public artifact records credentials, raw private source text, platform IDs, private absolute paths, raw query payloads, or private correlation refs.
