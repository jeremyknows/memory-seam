# L5.06 post-read usefulness and redaction verifier

Issue #106 adds a no-live verifier for the L5.05 supervised one-read receipt. The verifier consumes the already-committed report-safe receipt artifact and performs no additional live/private source read.

## Scope

- Input artifact: `docs/l5-supervised-one-read-receipt.md` or an equivalent in-memory receipt dictionary.
- Output schema: `memory_seam_l5_post_read_verifier_v0`.
- Allowed outcomes: `useful`, `too_redacted`, `denied_before_read`, and `degraded_backend_error`.
- Default command:

```bash
python scripts/l5_post_read_verifier.py --receipt docs/l5-supervised-one-read-receipt.md
```

## Classification contract

| Outcome | Meaning |
| --- | --- |
| `useful` | The receipt says the task was answerable from safe metadata and the posture/hygiene checks pass. |
| `too_redacted` | The receipt is public-safe but insufficient, or the verifier fails closed on public/private hygiene findings. |
| `denied_before_read` | The receipt records denial before read, with zero source-discovery/stat/backend/provider counters. |
| `degraded_backend_error` | The receipt records backend/adapter degradation, is missing required fields, or violates held posture counters. |

## Safety checks

The verifier fails closed if the public artifact contains sensitive-looking private paths, token shapes, raw platform identifiers, or raw query-payload labels. It also requires the held posture counters to preserve:

- zero source discovery, raw content, credential/auth/env/keychain/OAuth/auth-file, file-stat, read-backend, and provider calls;
- no Runtime Registry consumption;
- no service/listener/cron/startup activation;
- no global configuration mutation;
- no recurring runner activation;
- no provider/prod/canary authority;
- no write/custody/reindex behavior;
- no repository visibility or package publication change;
- no Atlas Gate movement.

## Boundary

This verifier is docs/tests/package-local code only. It does not discover sources, read raw/private source text, inspect credentials or auth material, consume Runtime Registry, start services, mutate global config, activate cron/startup/canary behavior, write custody records, reindex, publish packages, change repository visibility, or move Atlas Gate authority.
