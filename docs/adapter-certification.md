# Adapter certification

Adapter protocol version: `0.2`.

Every first-party or community adapter must pass the reusable pytest helper in
`tests/adapter_certification.py` before it is presented as compatible with
Memory Seam. The helper is intentionally local and no-network: it accepts a
`SourceAdapter` instance plus a fixture root and asserts the adapter can serve
report-safe items through the default-off runtime without widening authority.

## Certification bar

- **No writes** — certification must not create indexes, mutate source files,
  persist audit data, delete files, reindex, cache-purge, or perform write
  custody.
- **No network unless declared** — adapters must not call a network service
  during certification unless they expose an explicit capability field that says
  network access is required and the certifying test opts into that capability.
- **Read-only root policy** — item paths must be normalized root-relative paths:
  no leading slash, no `..`, no backslashes, no absolute paths, and no rendered
  fixture-root path in item dictionaries.
- **Symlink policy** — adapters must not follow symlinks outside the fixture
  root. Returned paths that resolve outside the root fail certification.
- **Redaction policy** — item payloads must not include raw private content,
  credentials, auth material, raw platform identifiers, raw backend responses,
  private correlation references, or private absolute paths. Use report-safe
  summaries, stable local labels, and explicit redaction labels.
- **Caps** — snippets must respect the configured snippet character cap, recall
  must respect `n`, file scans must have a bounded file/byte limit, and a
  zero-match query must return `[]` rather than raising.
- **Retrieval backend label** — every returned item must include
  `retrieval_backend`, and the value must be in the certification helper's
  allowed set or in a deliberately passed adapter-specific allowed set.
- **Receipt labels** — runtime output must keep posture flags fail-closed:
  `read_backend_called=false`, `service_started=false`,
  `runtime_registry_consumed=false`, `raw_fallback_used=false`, and
  `write_custody_or_reindex=false`. Runtime audit receipts must remain
  metadata-only and non-persistent.

## How to run

Create a fixture root with representative safe files, including one symlink that
points outside the root when the adapter supports filesystem traversal. Then call
the helper from a pytest file:

```python
from tests.adapter_certification import (
    AdapterCertificationConfig,
    assert_source_adapter_certified,
)


def test_my_adapter_is_certified(tmp_path):
    (tmp_path / "note.md").write_text("# Note\n\nsafe adapter recall", encoding="utf-8")
    adapter = MyAdapter(tmp_path)

    assert_source_adapter_certified(
        adapter,
        tmp_path,
        config=AdapterCertificationConfig(recall_query="adapter recall"),
    )
```

If your adapter uses a report-safe retrieval label that is not in the default
allowed set, pass an adapter-specific `allowed_retrieval_backends` set in the
config and document the label in the adapter README.

Certification is not authority to activate a service, consume Runtime Registry,
publish a package, run against production, or add write/custody behavior.
