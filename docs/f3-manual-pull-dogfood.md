# F3 manual pull dogfood runbook

This runbook is the F3.01 supervised manual-pull path for proving that Memory Seam can answer a small context/recall question from committed synthetic source-card fixtures only.

It is not an activation runbook. It does **not** grant cron/startup injection, broad recall authority, service/listener startup, live or private source reads, Runtime Registry consumption, writes, custody, reindexing, provider/prod/canary authority, repository visibility changes, or package publication.

## Preconditions

- Work from a clean checkout of this repository.
- Install only the local package or run with `PYTHONPATH=src` from the checkout.
- Do not set credentials, auth files, keychain material, Runtime Registry endpoints, or live-source paths for this proof.
- Use only the committed synthetic fixtures exposed by `synthetic_safe_content_provider()`.

## Command

From the repository root:

```bash
PYTHONPATH=src python examples/manual_pull_dogfood.py
```

The command creates an in-process synthetic provider, routes one source-card-first `/context` request, routes one `/recall` request, and prints a compact report-safe JSON summary. It does not bind a port, start a daemon, discover local files, read private content, or perform writes.

## Expected output shape

The exact JSON is stable enough for operator comparison. Key fields should match this shape:

```json
{
  "context": {
    "item_titles": [
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
    "source_card_count": 2,
    "source_card_ids": [
      "source-card-project-boundary",
      "source-card-runtime-answer"
    ],
    "status_code": 200
  },
  "held_authority": [
    "no_cron_or_startup_injection",
    "no_service_or_listener",
    "no_broad_recall_authority",
    "no_live_or_private_source_reads",
    "no_runtime_registry_consumption",
    "no_write_custody_or_reindex"
  ],
  "recall": {
    "item_titles": [
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
  "status": "manual_pull_dogfood_no_live_pass"
}
```

## Acceptance readout

Treat the run as PASS only when all of the following are true:

1. `context.status_code` and `recall.status_code` are `200`.
2. `context.source_card_count` is at least `2`, with only report-safe synthetic source-card IDs.
3. Both receipt verdicts are `useful`.
4. Every `safe_posture` value is `false`.
5. The `held_authority` list is present and still names cron/startup, service/listener, broad recall, live/private reads, Runtime Registry, and write/custody/reindex as held.

If any field implies live source discovery, backend/file/stat reads, service startup, Runtime Registry use, raw fallback, broad recall, or write/custody/reindex behavior, stop and classify the proof as failed. Do not rerun with credentials, private paths, raw queries, platform IDs, or live provider configuration.

## Focused verification

```bash
PYTHONPATH=src python examples/manual_pull_dogfood.py
pytest -q tests/test_manual_pull_dogfood_runbook.py
```

The focused test checks the command, docs discoverability, expected safe output, and the no-authority boundary. The repository-wide gate remains:

```bash
pytest -q
python scripts/public_hygiene_scan.py
python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py
git diff --check
```
