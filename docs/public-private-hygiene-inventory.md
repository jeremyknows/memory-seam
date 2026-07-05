# Public/private hygiene inventory

## Verdict

**Inventory PASS — public/package-facing surfaces have named hygiene classes, scanner coverage, and safe exceptions for the v0.1.0 public source release.**

This inventory is documentation and test guidance only. It does not authorize package publication automation, service/listener activation, credential/auth/env/keychain reads, Runtime Registry consumption, live/private source reads, source discovery, unsupervised reads, writes/custody/reindex behavior, provider/prod/canary authority, or production authority changes.

## Source floor and scope

- Repository: public Memory Seam source package.
- L4 closure floor: `8e23e9f Add final L4 closure review packet (#70)` or later.
- F4 verifier floor: `6bf7a2e Add F4 no-service identity verifier packet`.
- Current selected issue: public/private hygiene inventory.
- Earlier F2/F3/F4 verifier packets are closed/PASS; runtime/write authority remains held unless explicitly approved by a maintainer.

The inventory covers committed public/package-facing text surfaces: root package docs, docs index, contract/runtime docs, examples, tests, scripts, and package metadata. It does not inspect private operator worktrees, live sources, credentials, auth files, keychains, env secrets, Runtime Registry entries, provider backends, or service listeners.

## Public/package-facing surfaces

| Surface | Examples | Public-safe evidence allowed | Private-risk classes to reject |
| --- | --- | --- | --- |
| Root/package docs | `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, package metadata | Scope statements, no-live boundaries, command names, issue/PR numbers, sanitized source-floor labels, aggregate counts | Private absolute paths, raw private source text, credentials, auth/env/keychain material, token-shaped strings, raw platform IDs, raw query payloads, private correlation refs |
| Documentation index and hygiene docs | `docs/README.md`, `docs/public-hygiene.md`, `docs/public-private-hygiene-inventory.md` | Taxonomy, omitted-material policy, scanner command and PASS/FAIL status | Package-publish instructions, service activation, live-source instructions, raw private identifiers |
| Runtime/contracts notes | `docs/default-off-runtime.md`, `docs/schema-contracts.md`, `docs/policy-semantics-decision-note.md`, verifier packets | Metadata-only receipts, denial reason codes, posture booleans, zero-read assertions, safe summaries | Source dumps, raw local roots, credential or provider details, raw request/query payloads, production-authoritative claims |
| Tests/scripts/examples | `tests/`, `scripts/public_hygiene_scan.py`, `examples/` | Synthetic fixtures, test names, command invocations, monkeypatch/spy assertions, generated-cache rules | Live/private source discovery, network/provider calls, credential reads, untracked cache artifacts, raw platform IDs or token-like literals outside split test construction |
| Omitted internal material | no public manifest | Generic omission note only | Private source notes, package-use requirements, host-private paths, raw platform IDs, issue-comment URLs |

## Scanner coverage and safe exceptions

`python scripts/public_hygiene_scan.py` is the committed public-readiness gate. It currently scans text-like repository files while skipping generated/dependency cache directories. Its target hygiene classes are:

1. **Host-private paths** — local user homes and platform temp roots.
2. **Raw platform identifiers** — long snowflake-like IDs and common channel/team token shapes.
3. **Token-like strings** — common GitHub, OpenAI-style, Slack, and AWS credential shapes.
4. **Adapter/source-floor provenance labels and removed-doc references** — private source-floor handles and removed private doc paths must not leak into public/package-facing docs.
5. **GitHub issue-comment URLs** — use neutral fixture IDs or design-note references instead.
6. **Internal operator/provenance terms** — the scanner blocks selected private labels listed in `scripts/public_hygiene_scan.py`.

Safe exceptions are intentionally narrow:

- Private provenance has no public-tree quarantine; internal planning and provenance documents are maintained privately and omitted from this repository.
- Token-like strings are never allowed.
- Generated caches and dependency/build artifacts are skipped by the scanner and must stay ignored and untracked.
- `scripts/public_hygiene_scan.py` may include its own pattern examples so the scanner can test what it rejects. Stated without markup: scripts/public_hygiene_scan.py may include its own pattern examples.

## Trust-boundary evidence

This issue is inventory/scanner documentation only. It does not add a denial path that can materialize source/provider/file/stat/backend reads. Existing trust-boundary proof remains the F2/F3/F4 test evidence: denial and identity negative paths assert zero provider/backend/read/stat calls or equivalent monkeypatch/spy evidence before any materialization. Public artifacts for this inventory contain only issue/PR numbers, command names, file names, booleans, safe class names, and aggregate policy statements.

## Focused verifier

Focused command for this issue:

```bash
pytest -q tests/test_public_private_hygiene_inventory.py tests/test_public_hygiene_scan.py
```

Required full gate before merge:

```bash
pytest -q
python scripts/public_hygiene_scan.py
python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py
git diff --check
```

## Residual runtime hold

This inventory names the public/private hygiene surfaces only. It does not decide package upload, service activation, live adapter authority, or provider/prod/canary authority. Those decisions remain held for explicit maintainer approval.

## Next issue pointer

After this inventory lands and passes local verification, remaining runtime/write authority changes still require explicit maintainer review.
