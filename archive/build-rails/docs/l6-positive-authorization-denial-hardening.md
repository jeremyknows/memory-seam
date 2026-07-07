# L6P.02 positive-authorization stale/variant denial hardening

Issue: #164
Parent: #6
Prerequisite: #163 closed/PASS
Implementation evidence: `src/memory_seam/positive_authorization_receipt.py`; `tests/test_l6p02_positive_authorization_denial_hardening.py`

This slice hardens the L6P.01 synthetic/no-production positive-authorization receipt skeleton against stale, copied, variant, mismatched, broadened, and explicitly unsafe requests. It does not add an `allowed=true` path and does not execute, simulate, or enable mutation.

## Negative matrix

The test matrix proves denial before receipt recognition and before callbacks for:

- stale approval windows;
- copied #137 approval references;
- copied L6I.13-style template references without the fresh #163 event;
- issue mismatch;
- actor-role mismatch;
- subject mismatch;
- owner-scope mismatch;
- expiry at or after the exact 24-hour limit;
- operation count over the max-one limit;
- missing operation class;
- storage, receipt, and audit persistence requests;
- provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callback requests;
- live/private read and source-discovery requests;
- Runtime Registry consumption and global configuration mutation requests;
- service/listener/startup/cron activation, publication, repository visibility change, provider/prod/canary authority, and Atlas Gate movement requests.

## Guarded result invariants

Every negative path preserves:

- `recognized_positive_authorization=false`;
- `allowed=false` and `allowed_result_count=0`;
- `mutation_attempted=false`;
- `mutation_supported=false`;
- `denied_before_callback=true`;
- `callbacks_invoked=false`;
- `fixture_is_persistent=false`;
- no positive receipt metadata;
- all guarded provider/backend/source/mutation/persistence/cache counters at zero.

## Public/report hygiene

Denial reports are report-safe: they expose denial codes, public-shaped references, booleans, and zero counters only. They continue to exclude raw approval text, credentials, private source text, raw platform IDs, private paths, raw payloads, and private correlation refs.
