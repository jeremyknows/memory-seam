# Memory Seam

Memory Seam is a portable, receipt-first boundary layer that sits between AI agents and their memory backends: agents ask through the seam, and the seam enforces authority, scoping, and receipts before anything can be returned. It is for engineers building agent memory, RAG, personal knowledge, or internal assistant systems who need a small Python core that makes memory access auditable and fail-closed instead of letting every agent read directly from every backend.

## Why This Exists

When agents read memory directly, you usually lose the record of what was requested, why it was allowed, and which authority boundary was supposed to apply. That makes debugging hard and security reviews worse. Memory Seam moves that decision into one narrow layer: route the request, verify identity/scope, return metadata-only receipts, and deny before read when authority is missing. The current package is intentionally no-live and read-only so the contracts can be tested without connecting to private systems.

## Install (Verified E2E)

Requires Python >=3.10.

```bash
pip install "git+https://github.com/jeremyknows/memory-seam.git"
```

Clone and local-source alternative:

```bash
git clone https://github.com/jeremyknows/memory-seam.git
cd memory-seam
PYTHONPATH=src python3 examples/quickstart_smoke.py
```

## For Agents

Install line:

```bash
pip install "git+https://github.com/jeremyknows/memory-seam.git"
```

Copy-paste template prompt for a human to give their agent:

```text
Install memory-seam (pip install "git+https://github.com/jeremyknows/memory-seam.git"), then use `memory-seam recall <notes-root> "<question>" --json` to answer my questions from my notes. Always check the receipt_verdict (`read_receipt.usefulness_shape.verdict`) and safe_posture (`service_started`, `runtime_registry_consumed`, `raw_fallback_used`, `write_custody_or_reindex`) before trusting the output.
```

## Claude Code Plugin

Memory Seam ships one repo with three installable surfaces:

- Core: the `memory-seam` Python package from the repo root.
- Bridge: the `memory-seam-mcp` MCP stdio package from [`bridge`](bridge/README.md).
- Plugin: the Claude Code plugin shell at [`integrations/claude-plugin`](integrations/claude-plugin/README.md).

Install the plugin from a clone with:

```bash
claude --plugin-dir ./memory-seam/integrations/claude-plugin
```

The plugin exposes the canonical librarian skills as `/memory-seam:seam-recall`, `/memory-seam:seam-filing`, `/memory-seam:seam-curation`, and `/memory-seam:seam-ops`, paired with a local `memory-seam-mcp` bridge config.

Install the paired bridge where Claude Code can find it:

```bash
pip install "git+https://github.com/jeremyknows/memory-seam.git#subdirectory=bridge"
```

## MCP Bridge

The bridge lives in [`bridge`](bridge/README.md) as its own Python package named `memory-seam-mcp`. It installs the `memory-seam-mcp` executable used by MCP clients and by the plugin `.mcp.json` config:

```bash
pip install "git+https://github.com/jeremyknows/memory-seam.git#subdirectory=bridge"
memory-seam-mcp --help
```

For in-repo development, `bridge/scripts/verify.sh` installs the root core package from this checkout, then installs and tests the bridge package.

## 60-Second Quickstart

```bash
git clone https://github.com/jeremyknows/memory-seam.git
cd memory-seam
PYTHONPATH=src python3 examples/quickstart_smoke.py
```

Expected output shape, trimmed from a real run:

```json
{
  "context": {
    "endpoint": "context",
    "items": [
      "Memory Seam project boundary",
      "Default-off runtime answer"
    ],
    "receipt_verdict": "useful",
    "safe_posture": {
      "raw_fallback_used": false,
      "read_backend_called": false,
      "runtime_registry_consumed": false,
      "service_started": false,
      "write_custody_or_reindex": false
    },
    "status_code": 200
  },
  "recall": {
    "endpoint": "recall",
    "items": [
      "Default-off runtime answer"
    ],
    "receipt_verdict": "useful",
    "safe_posture": {
      "raw_fallback_used": false,
      "read_backend_called": false,
      "runtime_registry_consumed": false,
      "service_started": false,
      "write_custody_or_reindex": false
    },
    "status_code": 200
  }
}
```

This proves the seam can answer a context request and a recall request through the local runtime using committed synthetic fixtures only. The receipts are metadata-only, there are no live reads or raw fallbacks, and the posture flags stay fail-closed for service startup, Runtime Registry consumption, backend reads, and write/custody/reindex behavior.

## Use Your Own Notes (2 minutes)

After installing, point the CLI at any supported local source. Markdown is the default:

```bash
memory-seam recall ./docs "runtime boundary" --n 3
```

For a full machine-readable envelope:

```bash
memory-seam recall ./docs "runtime boundary" --json
```

Human output shows title, root-relative path, snippet, and one receipt line:

```text
1. Default-off runtime
   default-off-runtime.md
   The L3 runtime is an in-process skeleton...
Receipt: verdict=useful; reason=safe_context_sufficient; safe_posture=read_backend_called=false, service_started=false, runtime_registry_consumed=false, raw_fallback_used=false, write_custody_or_reindex=false
```

Use `context` to scan the same markdown root without a query:

```bash
memory-seam context ./docs/patterns --json
```

The receipt proves the runtime authorized the request before the folder scan, the returned evidence is report-safe with root-relative paths, and the held surfaces stayed closed: no service startup, no Runtime Registry consumption, no raw fallback, and no write/custody/reindex behavior.

Adapter alternates:

```bash
memory-seam recall ./notes-markdown "launch plan" --adapter markdown --n 1
memory-seam recall ./notes-text "receipt" --adapter plaintext --n 1
memory-seam recall ./notes-export "customer signal" --adapter jsonl --n 1
memory-seam recall . "adapter factory" --adapter git-tree --n 1
memory-seam recall ./notes.db "retrospective" --adapter sqlite --db-table notes --title-column title --body-column body --n 1
```

`sqlite` is for deliberately copied databases and requires explicit table/title/body mapping; it does not autodetect schema.

Python alternative, using the same adapter/runtime shape:

```bash
python3 examples/my_notes_quickstart.py
python3 examples/my_notes_quickstart.py ~/path/to/notes
```

This is the reference path for local files and copied exports; production backends stay outside the core package and arrive through adapters.

## Build Your Own Provider

```python
from dataclasses import dataclass
from memory_seam import (
    AdapterMemorySeamProvider, LocalReadOnlyRuntime, ReadOnlyRuntimeConfig,
    RuntimeRequest, StaticIdentityVerifier,
)

@dataclass(frozen=True)
class MyAdapter:
    adapter_name: str = "my-fixture"

    def context_items(self, *, include, token_subject):
        return [{
            "id": "hello", "scope": "context", "include_family": "project",
            "source_tier": "fixture", "backend": "local",
            "retrieval_backend": "metadata_only", "canonicality": "example",
            "private_class": "reportable_synthetic", "title": "Hello seam",
            "snippet": "This came through a provider, not a raw backend read.",
        }]

    def recall_items(self, query, *, scope, token_subject, n):
        return self.context_items(include=["project"], token_subject=token_subject)[:n]

runtime = LocalReadOnlyRuntime(
    ReadOnlyRuntimeConfig(enabled=True, provider_name="my-fixture"),
    AdapterMemorySeamProvider(MyAdapter()),
    StaticIdentityVerifier("agent:demo", frozenset({"context", "wiki"})),
)
print(runtime.handle(RuntimeRequest("GET", "/context?include=project"))["body"]["items"][0]["title"])
```

Provider protocols are deliberately small: implement health/context/recall directly with `MemorySeamProvider`, or wrap a read-only adapter with `AdapterMemorySeamProvider` as shown above.

## Capabilities And Non-Goals

| Area | What it does | What it deliberately does NOT do |
| --- | --- | --- |
| Core runtime | In-process, read-only routing for health/context/recall | Start a live service, listener, daemon, or network server |
| Authority | Static/demo identity verification, scope checks, deny-before-read paths | Trust query strings as authority or silently widen access |
| Receipts | Metadata-only read receipts and runtime posture flags | Persist audit logs or expose raw/private source content |
| Providers | Protocols, null provider, synthetic fixtures, adapter wrapper | Ship a production memory backend or call one by default |
| Local adapters | Markdown, plaintext, JSONL/JSON export, Git current-tree, and explicitly mapped copied SQLite recall/context | Follow symlinks, read Git history, autodetect private app databases, start services, or mutate sources |
| Policy/descriptors | Safe contracts for scoped source metadata and grants | Discover local sources or consume Runtime Registry state |
| Writes | Explicit write-like route/payload denial | Write memory, custody records, delete, reindex, rollback, or purge |
| Network | Installable Python package with local examples | Make runtime network calls from the core package |

## Architecture In 6 Lines

1. Agents call Memory Seam routes such as `/context` and `/recall`.
2. The local runtime verifies identity/scope before provider callbacks run.
3. Providers return report-safe items and posture flags through a narrow protocol.
4. Receipts describe what happened without exposing raw source content.
5. Core owns contracts, routing, policy, descriptors, receipts, and no-live examples.
6. Adapters own backend-specific reads outside core; see [adapter import boundary](docs/adapter-import-boundary.md) and [package boundary](docs/package-boundary.md).

Deep docs live in [docs/README.md](docs/README.md).

## Documentation

Start with `docs/README.md` for the documentation taxonomy across public package docs, runtime/contracts notes, downstream adapter notes, and examples. See `CHANGELOG.md` for the API/schema stability ledger.

Public v0.1.0 source package under Apache-2.0 is packaged as a no-live/read-only core. It does not include live adapter implementation, service/listener activation, credentials, runtime registry consumption, unsupervised reads, writes/custody/reindex, provider/prod/canary authority, or package publication automation.

- `docs/atlas-query-migration.md` — migration guide for downstream Atlas Query adapters, package dependency shape, rollback, and no-submodule boundary.
- `docs/f2-verifier-packet.md` — F2 verifier packet for policy semantics, denial-before-read evidence, CI/local checks, and residual no-live holds.
- `docs/f3-manual-pull-dogfood.md` — supervised manual-pull dogfood runbook using committed synthetic source-card fixtures only.
- `docs/f3-source-card-usefulness-proof.md` — source-card usefulness proof with PASS/HOLD/FAIL outcomes and no raw fallback.
- `docs/f3-verifier-packet.md` — F3 verifier packet for manual-pull/source-card evidence and the bounded F4 identity unlock.
- `docs/no-service-identity-semantics.md` — no-service identity semantics for subject, acting-for, audience/scope, query/body mismatch, and held service/live/write authority.
- `docs/f4-verifier-packet.md` — F4 verifier packet for no-service identity negative matrix evidence and F10 hygiene-prep unlock.
- `docs/policy-semantics-decision-note.md` — policy semantics decision note for descriptor/grant intersection, denial reasons, and held surfaces.
- `docs/public-private-hygiene-inventory.md` — public/private hygiene inventory covering public surfaces, scanner target classes, safe exceptions, and omitted private planning material.
- `docs/contract-test-inventory.md` — map from committed tests to the discoverability and safety invariants they protect.

## Project Status

Memory Seam is v0.1.0 public source. The API may evolve while the package boundary is still hardening. Current scope is no-live/read-only core behavior, examples, contracts, and tests.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Before proposing a change, run:

```bash
python3 -m pytest -q
python3 scripts/public_hygiene_scan.py
```

Keep contributions inside the portable package boundary: no credentials, no private paths, no service activation, no live/private reads, and no write/custody/reindex behavior.

## Security

Report vulnerabilities through GitHub Security Advisories for this repo. See [SECURITY.md](SECURITY.md) for supported surfaces and the current no-live security boundary.

## License

Apache-2.0. See [LICENSE](LICENSE).
