# Changelog

Memory Seam uses this changelog as the stability ledger for public API, schema,
contract, and operator-facing behavior changes for the public Apache-2.0 source
package. The format follows Keep a Changelog: every PR updates `[Unreleased]`
before merge, and each entry is tagged **Breaking**, **Non-breaking**, or
**Documentation-only**.

This file does not authorize service/listener activation, live source reads,
Runtime Registry consumption, provider/prod/canary authority changes, package
publication, or write/custody/reindex work.

## [Unreleased]

### Added

- **Non-breaking** — Added `memory-seam librarian init` and
  `memory-seam librarian doctor` for creating and posture-checking the
  memory-librarian template package workspace.
  - Surface: CLI, packaged resources, and subprocess tests.
  - Migration: none; init writes only inside the chosen destination and emits
    MCP client snippets without mutating client config.
  - Rollback: remove `src/memory_seam/librarian.py`, the librarian CLI
    subcommands, and related tests/resources.
- **Non-breaking** — Added the packaged
  `memory_seam.agent_packages.memory_librarian` template package/starter with
  schema-versioned role-card/config templates, receipt inspection posture,
  held-surface denials, and importlib resource snapshot coverage.
  - Surface: packaged resources and tests.
  - Migration: none; no runtime, service, config-write, custody, or reindex
    authority is introduced.
  - Rollback: remove the agent package resource tree and its snapshot tests.
- **Non-breaking** — Extended the public hygiene scanner to cover `.template`
  files, packaged template trees, placeholder discipline, real-operator
  defaults, authority phrases, and stdio-only MCP example posture.
  - Surface: public hygiene scanner and scanner tests.
  - Migration: template authors must use the approved placeholder set and keep
    MCP examples snippet-only and stdio-only.
  - Rollback: revert the scanner rule additions and related tests.
- **Non-breaking** — Added
  `memory_seam.local_adapters.sqlite_notes.LocalSqliteAdapter`, a read-only
  local SQLite notes adapter with explicit table/column mapping, app-cache path
  blocking, row caps, statement progress limits, and schema-only table
  inspection for copied databases.
  - Surface: packaged adapter API and adapter test coverage.
  - Migration: import `LocalSqliteAdapter` from
    `memory_seam.local_adapters.sqlite_notes` for deliberately copied SQLite
    notes databases.
  - Rollback: remove the adapter module and its tests if the local adapter
    campaign changes direction.
- **Non-breaking** — Added
  `memory_seam.local_adapters.git_tree.LocalGitTreeAdapter`, a read-only local
  Git current-tree adapter that enumerates tracked files only with
  `git ls-files -z`, rejects history access, skips binary/large/non-regular
  files and submodule gitlinks, and returns friendly structured reasons when
  Git is unavailable or the root is not a repository.
  - Surface: packaged adapter API and adapter test coverage.
  - Migration: import `LocalGitTreeAdapter` from
    `memory_seam.local_adapters.git_tree` for tracked current-tree recall.
  - Rollback: remove the adapter module and its tests if the local adapter
    campaign changes direction.
- **Non-breaking** — Added
  `memory_seam.local_adapters.jsonl_export.LocalJsonlExportAdapter`, a read-only
  local JSONL/JSON export adapter with explicit field mapping, safe common-field
  autodetection, malformed-row scan accounting, and per-file record caps.
  - Surface: packaged adapter API and adapter test coverage.
  - Migration: import `LocalJsonlExportAdapter` from
    `memory_seam.local_adapters.jsonl_export` for local `.jsonl` and `.json`
    export recall.
  - Rollback: remove the adapter module and its tests if the local adapter
    campaign changes direction.
- **Non-breaking** — Added stdlib-only CLI polish for local markdown
  recall/context: the Gate Wordmark startup/version banner, TTY-aware ANSI
  styling for human output, colored receipt verdict lines, a TTY-only scan
  status line that resolves into the run summary, and tests preserving
  byte-stable `--json` output.
  - Surface: CLI human output and CLI tests.
  - Migration: none; JSON envelopes are unchanged.
  - Rollback: revert `src/memory_seam/_style.py` and the CLI display-layer
    styling if terminal output needs to return to plain text.
- **Non-breaking** — Added
  `memory_seam.local_adapters.plaintext.LocalPlainTextAdapter`, a read-only
  local plain-text folder adapter with configurable extension allowlist,
  null-byte binary skip accounting, scan caps, and certification tests.
  - Surface: packaged adapter API and adapter test coverage.
  - Migration: import `LocalPlainTextAdapter` from
    `memory_seam.local_adapters.plaintext` for `.txt`, `.md`, `.rst`, and `.log`
    folder recall.
  - Rollback: remove the adapter module and its tests if the local adapter
    campaign changes direction.
- **Non-breaking** — Added `memory_seam.__version__` to the public API surface.
  - Surface: exported API.
  - Migration: none.
  - Rollback: revert the version export if package metadata handling changes.
- **Non-breaking** — Added a local markdown-folder provider example plus the
  "Use Your Own Notes" demo for read-only local notes recall.
  - Surface: examples and README operator workflow.
  - Migration: none.
  - Rollback: remove the example/demo files if the adapter contract changes.
- **Non-breaking** — Added adapter protocol version `0.2` as
  `ADAPTER_PROTOCOL_VERSION`, exported from `memory_seam`.
  - Surface: exported API and adapter contract.
  - Migration: adapters may pin or assert the protocol version before claiming
    compatibility.
  - Rollback: revert the constant/export before a tagged release if the protocol
    shape changes again.
- **Non-breaking** — Added `tests/adapter_certification.py`, a reusable pytest
  certification helper for any `SourceAdapter`, covering root-relative paths,
  absolute-path rejection, symlink escape rejection, snippet caps, zero-match
  empty results, runtime posture flags, and allowed `retrieval_backend` labels.
  - Surface: downstream fixture/certification helper.
  - Migration: adapter authors should run the helper against their adapter.
  - Rollback: revert helper and docs if the protocol moves to a packaged helper.
- **Non-breaking** — Promoted the local markdown-folder example into the
  first-party `memory_seam.local_adapters.markdown.LocalMarkdownAdapter`.
  - Surface: packaged adapter API, examples, and adapter runtime envelopes.
  - Migration: import `LocalMarkdownAdapter` from `memory_seam.local_adapters.markdown`;
    `examples.local_markdown_provider.LocalMarkdownProvider` remains a shim.
  - Rollback: revert the packaged adapter and keep the example shim pointing to
    the prior example implementation.
- **Non-breaking** — Added the user-facing CLI front door for local markdown
  adapter recall/context via `memory-seam recall <root> "<query>"` and
  `memory-seam context <root>`.
  - Surface: CLI, README operator workflow, and subprocess tests.
  - Migration: none; rootless CLI commands keep the prior synthetic no-live
    smoke behavior.
  - Rollback: revert the CLI local markdown branch and README onboarding update.

### Changed

- **Documentation-only** — Rewrote the README for a user-first quickstart and
  clearer package scope.
  - Surface: README.
  - Migration: none.
  - Rollback: revert README wording.
- **Documentation-only** — Added agent-first onboarding with an install line and
  copy-paste template prompt for CLI-based notes recall.
  - Surface: README.
  - Migration: none.
  - Rollback: revert README wording.
- **Documentation-only** — Clarified adapter import-boundary wording from "no
  adapters in package" to "core imports no adapter implementations"; in-package
  adapter modules may exist when core does not import them.
  - Surface: docs and AST import-boundary tests.
  - Migration: keep adapter implementation dependencies pointed into core, not
    from core into adapter implementations.
  - Rollback: revert docs/tests wording.

### Breaking

- No breaking changes in `[Unreleased]`.

## [0.1.0]

### Initial public release baseline

- **Non-breaking** — Initial no-live core package surface: contracts, policy,
  descriptors, provider protocols/null provider, receipts, router, testing
  helpers, and package import boundary.
- **Non-breaking** — Atlas Query bridge helper and versioned standalone fixture
  for downstream adapter migration without duplicating core contracts.
- **Non-breaking** — Default-off read-only runtime skeleton for synthetic
  `/health`, `/context`, and `/recall` envelopes, including denial-before-read
  behavior, metadata-only receipts, kill-switch/rollback contract tests, and
  safe source-card adapter interfaces.
- **Non-breaking** — Local packaging metadata, local wheel/install smoke, null
  and deterministic fake provider examples, and minimal no-live CLI smoke.
- **Documentation-only** — Public hygiene, docs taxonomy, release decision
  checklist, issue-railed autopilot template, Atlas Query migration guide, and
  private provenance quarantine guidance.
- **Documentation-only** — F10 package boundary and release-authority docs
  cleanup aligning README/docs/changelog/packaging on public v0.1.0 posture,
  no-live examples, downstream adapter ownership, and held runtime/write
  authority.
- **Documentation-only** — package boundary and release-authority docs cleanup
  captured in `docs/package-boundary.md`.

## Stability Policy

- Public API changes include exported modules under `memory_seam`, documented
  contract dataclasses/protocols, CLI no-live smoke behavior, envelope schema
  snapshots, receipt fields, provider interfaces, and bridge fixture versions.
- **Breaking** changes must include the affected surface, migration note,
  rollback note, and the issue/PR that introduced the change.
- **Non-breaking** changes should include the affected surface and the issue/PR
  that introduced the change when available.
- **Documentation-only** changes should call out when they do not alter package
  behavior or schema shape.

### Entry Template

```markdown
- **Breaking|Non-breaking|Documentation-only** — Short summary.
  - Surface: exported API, schema snapshot, CLI, docs, packaging, or downstream fixture.
  - Migration: required downstream action, or `none`.
  - Rollback: safe rollback route, or `revert PR` when sufficient.
  - Evidence: issue #NN / PR #NN plus local and CI checks.
```

## Runtime Boundary

This changelog records source package changes only. It does not authorize
service/listener activation, live source reads, Runtime Registry consumption,
provider/prod/canary authority changes, package publication, or
write/custody/reindex work.
