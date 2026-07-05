# Public hygiene scan

`scripts/public_hygiene_scan.py` is a conservative public-source guard for the
release checkout. It scans repository text files for content that should
not ship in a public package or source distribution:

- host-private path variants such as macOS, Linux, Windows user directories, and
  Darwin temporary folder paths;
- raw platform identifiers, including Discord snowflakes and Slack-style IDs;
- token-like strings, including GitHub, OpenAI-style, Slack bot/app/user token
  prefixes, and AWS access-key IDs;
- adapter/source-floor provenance strings and removed internal-doc references;
- GitHub issue-comment URLs;
- internal operator/provenance labels currently blocked by the scanner:
  example agents, `operator directive`, `stewardship-transition`, and
  `Example-stewardship`.

## Documented exceptions

Private provenance has no public-tree quarantine. Internal planning and
provenance documents are maintained privately and omitted from this repository.

Generated cache paths and build-output paths are skipped rather than scanned. This
keeps the guard focused on source artifacts and avoids failing on disposable tool
state such as `.pytest_cache/`, `.mypy_cache/`, `__pycache__/`, `.tox/`, `.venv/`,
`build/`, `dist/`, `site-packages/`, and package metadata cache directories such
as `*.egg-info` or `*.dist-info`.

The same disposable paths are expected to stay out of git entirely. `.gitignore`
covers Python bytecode, pytest/mypy/ruff/tox caches, local virtualenv and coverage
output, build artifacts, and package metadata. The regression suite checks both
that those ignore rules exist and that the tracked source tree does not already
contain generated cache artifacts.

The scanner also permits its own pattern definitions in
`scripts/public_hygiene_scan.py`; tests cover the denied forms in temporary
fixtures so the real checkout does not need to carry unsafe literals outside the
scanner implementation itself.

## L6V supervised source-card proof ratchet

The public hygiene scan also ratchets reportable L6V supervised source-card proof
artifacts. It fails JSON/YAML/text output artifacts that would
make a proof unsafe to report, including:

- `allowed=true`, non-zero `allowed_result_count`, live-adapter/callback flags,
  mutation, or persistence flags;
- raw approval text, raw actor IDs, raw source-content flags, private-path flags,
  credential/auth-material flags, source-URI flags, raw platform-ID flags, raw
  prompt/query flags, raw payload/backend-response flags, or private correlation
  flags;
- unsafe descriptor/source-card refs that do not use the committed synthetic
  report-safe `l6v-report-safe-*` prefixes;
- raw source content, source identifiers, source URIs, private paths, token/auth
  material, raw prompt/query text, raw payload/backend responses, raw platform
  IDs, or private correlation refs.

The ratchet is scanner/test/docs-only. It performs no live/private reads, source
discovery, credential reads, callbacks, persistence, mutation, activation,
publication, provider/prod/canary movement, or Atlas Gate movement.
