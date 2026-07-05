# Envelope schema snapshots

Memory Seam pins structural JSON envelope snapshots for the local no-live
runtime responses:

- `GET /health`
- `GET /context?...&read_receipt=metadata_only`
- `GET /recall?...&read_receipt=metadata_only`

The committed fixture is `tests/fixtures/envelope_schema_snapshots_v0.json` and
is exercised by `tests/test_envelope_schema_snapshots.py`.

## What the snapshot pins

The snapshot records deterministic response shape rather than volatile values.
Dictionaries are sorted, sets are rendered as sorted lists, arrays keep their
item shapes, and scalar values are replaced with type markers such as `<str>`,
`<int>`, `<bool>`, and `<null>`. This keeps timestamps and opaque receipt hashes
from churning while still failing tests when an envelope key, nested receipt
shape, item field, or held-surface structure changes unexpectedly.

Pinned top-level shape for each response:

```text
{
  "status_code": int,
  "headers": {"content-type": str},
  "body": {...}
}
```

Pinned runtime/read boundaries include:

- runtime receipt schema and rollback handle
- metadata-only read receipt schema for context/recall
- audit and rollback receipt sub-shapes
- `read_backend_called`, `service_started`, `runtime_registry_consumed`, and
  `write_custody_or_reindex` posture flags
- synthetic context/recall item field structure

## Versioning contract

The fixture schema is `memory_seam_envelope_schema_snapshots_v0`. Treat a failing
snapshot as an API-review event, not as an automatic fixture-refresh task.

Only update the fixture when the changed envelope shape is intentional and the
caller-facing impact has been reviewed. If the change breaks downstream callers,
add a new fixture version instead of mutating `v0`, then document the migration
path before closing the rail.

## Held surfaces

These snapshots are generated in-process with `LocalReadOnlyRuntime`,
`synthetic_safe_content_provider()`, and `StaticIdentityVerifier`. They do not
start a service, activate a listener, discover local sources, call a network,
consume Runtime Registry, read private/live data, publish packages, or perform
write/custody/reindex behavior.
