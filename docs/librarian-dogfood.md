# Librarian dogfood runner

`memory-seam librarian dogfood <workspace> [--notes <root>] [--now <iso>] [--json]`
runs the v0.2 memory-librarian template-package proof in-process. It uses the
same local read-only runtime wiring as the CLI, so no MCP client, listener,
daemon, Runtime Registry, credential read, global config mutation, or
write/custody/reindex surface is required.

## What it proves

The runner checks a generated librarian workspace end to end:

1. Runs `memory-seam librarian doctor <workspace>` and stops immediately if the
   workspace posture fails.
2. Copies the configured notes root into a temporary sandbox under the
   workspace, then runs health and context through the local markdown runtime.
3. Derives five recall questions from real note titles/content and requires each
   recall envelope to return a receipt verdict, computed posture verdict, and
   root-relative cited paths.
4. Adds a hostile note fixture only inside the sandbox copy and verifies recall
   returns the fixture as data while the runner keeps fail-closed posture.
5. Writes `memory/dogfood-draft-note.md` in the librarian workspace memory
   folder, then proves that draft is not in the notes root and is not returned
   by recall over the sandbox notes copy.
6. Writes `memory/dogfood-report.json` with every step, receipt summaries, the
   evaluated pass-criteria checklist, and the deterministic timestamp supplied
   by `--now` or the default string `unset`.

## Example

```bash
memory-seam librarian init ./tmp-lib --notes ./notes --mode supervised-request
memory-seam librarian dogfood ./tmp-lib --notes ./notes --now 2026-07-05T00:00:00Z
```

Human output is one `PASS` or `FAIL` line per step, followed by the final
verdict and report path. `--json` prints the same report JSON that is written to
`memory/dogfood-report.json`. Exit code is `0` only when every step and every
pass criterion passes.

## Report posture

The report intentionally stores metadata and root-relative citations only. It
does not include raw note snippets, absolute local paths, credential values,
source URIs, backend payloads, or copied workspace paths. The timestamp is not
read from the wall clock; callers pass `--now` when they need a concrete ISO
value.

## Verification

```bash
python3 -m pytest -q tests/test_librarian_cli.py
python3 -m pytest -q
python3 scripts/public_hygiene_scan.py
git diff --check
```
