# L5.01 no-source-read idle tick contract

Issue #101 adds a deterministic in-process idle tick for Memory Seam. The tick is a wake/check posture report only; it does not perform a source read, provider/backend callback, file read, file stat, Runtime Registry lookup, service/listener activation, global config mutation, or write/custody/reindex action.

## Contract

Call `LocalReadOnlyRuntime().idle_tick()` or `runtime_idle_tick()` to receive metadata-only status:

- `read_backend_called: false`
- `source_read_called: false`
- `file_stat_called: false`
- `service_started: false`
- `runtime_registry_consumed: false`
- `global_config_mutation: false`
- `write_custody_or_reindex: false`
- `unsupervised_read_unheld: false`
- `write_custody_unheld: false`

The tick remains default-off/in-process. It does not install, schedule, start, or activate cron, a listener, a canary, a runner, or a service.

## Hold posture

This contract is intentionally boring. Passing L5.01 does **not** unhold unsupervised reads, recurring reads, source discovery, live/private source access, provider/prod/canary authority, Runtime Registry consumption, or any write/custody/reindex behavior. Later L5/L6 issues must satisfy their own gates before those surfaces can move.

## Proof

`tests/test_runtime.py::test_idle_tick_is_metadata_only_and_touches_no_source_surfaces` installs exploding spies for provider health/context/recall, read routing, file open, and file stat. The test asserts the idle tick returns the explicit false posture counters above and that every spy counter remains zero.
