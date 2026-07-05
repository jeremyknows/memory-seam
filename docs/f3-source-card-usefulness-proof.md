# F3 source-card usefulness proof packet

This packet is the F3.02 source-card-first usefulness proof over committed synthetic fixtures only. It records whether a bounded context/recall answer is answerable from safe source cards, whether raw fallback was avoided, which report-safe source-card IDs contributed, and how degraded or unsafe outcomes are classified.

It is not activation authority. It does **not** grant service/listener startup, cron/startup injection, broad recall, live/private source reads, source discovery, Runtime Registry consumption, credentials/auth/keychain reads, writes, custody, reindexing, provider/prod/canary authority, repository visibility changes, package publication, or Gate movement.

## Fixture floor

- Harness: `examples/manual_pull_dogfood.py`
- Provider: `synthetic_safe_content_provider()`
- Source fixtures: committed synthetic source cards only
- Focused tests: `tests/test_source_card_usefulness_proof.py`
- Related runbook: `docs/f3-manual-pull-dogfood.md`

The proof uses report-safe card IDs and titles only. It does not include raw private source text, private absolute paths, raw platform IDs, raw query payloads, credentials, auth material, or private correlation references.

## PASS proof: source-card-first answerability

Expected PASS outcome for the committed synthetic manual-pull fixture:

```json
{
  "outcome": "PASS",
  "answerability": "answerable_from_safe_source_cards",
  "context_status_code": 200,
  "recall_status_code": 200,
  "context_receipt_verdict": "useful",
  "recall_receipt_verdict": "useful",
  "safe_detail_source_card_ids": [
    "source-card-project-boundary",
    "source-card-runtime-answer"
  ],
  "source_card_count": 2,
  "raw_fallback_used": false,
  "service_started": false,
  "runtime_registry_consumed": false,
  "write_custody_or_reindex": false,
  "read_backend_called": false
}
```

PASS means the source-card deck is sufficient for the bounded question and no fallback file, source discovery, service, Runtime Registry, or write/custody/reindex surface is used.

## HOLD proof: degraded but reportable-safe

Expected HOLD outcome for a truncated/redacted synthetic safe item:

```json
{
  "outcome": "HOLD",
  "answerability": "answerable_but_degraded",
  "reason_codes": [
    "redaction_survived",
    "safe_content_truncated"
  ],
  "raw_fallback_used": false,
  "service_started": false,
  "runtime_registry_consumed": false,
  "write_custody_or_reindex": false,
  "read_backend_called": false
}
```

HOLD means a reportable-safe answer may still be possible, but the operator should not treat it as a clean usefulness pass because redaction or truncation degraded the evidence. The safe response is to improve committed source-card fixtures or hold the rung, not to read private/live sources or use raw fallback.

## FAIL proof: degraded or unsafe evidence

Expected FAIL outcomes for unsafe or too-degraded synthetic evidence:

```json
{
  "outcome": "FAIL",
  "answerability": "not_answerable_from_safe_source_cards",
  "reason_codes_any_of": [
    "too_degraded",
    "unsafe_fragment_detected",
    "redaction_erased_answer"
  ],
  "raw_fallback_used": false,
  "service_started": false,
  "runtime_registry_consumed": false,
  "write_custody_or_reindex": false,
  "read_backend_called": false
}
```

FAIL means the packet must not be promoted as a usefulness proof. Unsafe/redacted content remains reportable-safe because the public artifact records only reason codes and synthetic IDs, not raw private text or raw paths.

## Denial-before-read and no-live posture

This issue does not add a new live denial path. The exercised path is the committed no-live provider/harness and the existing denial matrix remains the source for deny-before-read counters. For this proof packet, the equivalent no-live assertions are:

- `raw_fallback_used=false`
- `read_backend_called=false`
- `service_started=false`
- `runtime_registry_consumed=false`
- `write_custody_or_reindex=false`
- no source discovery, file/stat/backend counters, or live provider reads are introduced

If any future source-card usefulness proof requires a negative path, it must prove denial before source/provider/file/stat/backend reads with zero counters or monkeypatch/spy assertions before it can be recorded as PASS.

## Focused verification

```bash
PYTHONPATH=src python examples/manual_pull_dogfood.py
pytest -q tests/test_source_card_usefulness_proof.py
```

Repository-wide verification remains:

```bash
pytest -q
python scripts/public_hygiene_scan.py
python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py
git diff --check
```
