# Deployment pattern: `sensitive_pointer` source family

**Status:** documented pattern only — not shipped in core
**Related ADR:** [0003 — Credentials: permanent values ban; pointer custody is a deployment pattern](../adr/0003-credentials-values-ban-pointer-as-pattern.md)

## What this pattern is

In a multi-user or multi-host deployment, some agents may need to locate a
credential or service account — where it lives in a vault, which wrapper script
to call — without needing the value itself.  The `sensitive_pointer` source
family is the recommended way to serve that pointer content through the seam
using only the machinery already present in the core: source families, the
descriptor registry, the grant matrix, `private_class` labeling, and read
receipts.

The core ships **no such family by default.**  Adding one is a deployment
decision, not a feature of the portable package.

## What it serves — and what it never serves

| Allowed through this family | Permanently banned at every layer |
|---|---|
| Vault item names (e.g. `discord-builder-token`) | Credential values, tokens, secrets |
| Wrapper script names / access patterns | Raw `.env` content, auth JSON |
| Human-readable "how to access" prose | OAuth payloads, keychain entries |

The "never serves values" guarantee is not advisory — it is enforced
structurally.  `PROTECTED_CONTEXT_PATH_FRAGMENTS` (contracts.py) pre-emptively
denies any source whose resolved path touches `/keychain/`, `/oauth/`,
`/gateway/`, `/sessions/`, or `/logs/`.  `PROTECTED_CONTEXT_PATH_NAMES` denies
`.env`, `auth.json`, and `state.db` by name.  These denials fire before the
grant matrix is consulted; a misconfigured descriptor pointing at a protected
path is rejected at registration, not at read time.

## When to use it

Use this family when **all** of the following are true:

1. The deployment has multiple users or multiple hosts where OS-level isolation
   is real.  The grant matrix can then enforce per-agent walls that matter — a
   grant absence produces `source_grant_missing` denial before any read reaches
   the filesystem.
2. Agents repeatedly fail tasks because they cannot locate the right vault item
   or wrapper script.  Observed demand, not speculation.
3. The pointer content is genuinely distinct from the credential value (vault
   item name, not the item).

## When NOT to use it

Do not create a `sensitive_pointer` family on a single-user, single-host
deployment.  On such a machine all agents share one OS user identity, so a
grant-matrix wall is decorative: any process that could abuse the seam could
also read the pointer source file directly.  Worse, registering a
machine-readable index of secret locations creates a recon artifact — a single
source that maps every credential to its vault path — where none existed before.
ADR 0003 names this trade-off explicitly: the pointer need is better served by
keeping a complete wiki article (readable through the normal receipted read path)
than by building dedicated machinery whose security guarantees are illusory at
that deployment scale.

## Extension points in the core

To add this family to a deployment, a maintainer touches exactly four places:

### 1. `VALID_CONTEXT_INCLUDES` (contracts.py)

```python
VALID_CONTEXT_INCLUDES = {"user", "memory", "soul", "project", "last_session",
                          "sensitive_pointer"}   # deployment extension
```

`ContextSourceDescriptor.__post_init__` validates `include_family` against this
set at construction time, so extending the constant is the registration gate.

### 2. `ContextSourceDescriptor` rows (descriptors.py)

Each pointer document gets one descriptor:

```python
ContextSourceDescriptor(
    subject="agent-x",
    include_family="sensitive_pointer",
    root_ref="vault-pointers-root",    # opaque label; path injected by operator
    relative_path="agent-x/access-map.md",
    source_tier="operator_managed",
    private_class="sensitive_pointer",  # propagates to every receipt
    canonicality="deployment_specific",
    enabled=False,                      # deny-first; operator flips per grant
    reportable=False,
)
```

Setting `enabled=False` means the descriptor exists in the registry but
`ContextSourceDescriptorRegistry.to_allowlist()` places it in `policy_denials`
with reason `"descriptor_disabled"` before any grant check.  An operator can
then enable individual descriptors while leaving the family disabled by default
at the family level.

### 3. `ContextSourceGrant` rows and `ContextSourceGrantMatrix` (descriptors.py)

Grant rows are tiny — they reference an `(subject, include_family)` key and
flip `enabled`.  Unlisted agents are denied with reason `source_grant_missing`:

```python
ContextSourceGrant(
    subject="agent-x",
    include_family="sensitive_pointer",
    enabled=True,
    reason="operator_approved",   # must be in VALID_CONTEXT_GRANT_REASONS
)
```

Build the matrix with `ContextSourceGrantMatrix.from_grants([...])`.
`assert_descriptors_exist()` fires at matrix construction if a grant references
a descriptor key that has not been registered, preventing silent misconfiguration.

### 4. Scope guard in `policy.py`

`scope_allowed()` checks the caller's `SubjectPolicy.allowed_scopes` before the
grant matrix is consulted.  A deployer should add `"context:sensitive_pointer"`
to the scope issued to agents that are permitted to request pointer content, and
keep it absent from the default scope set.  The default `policy()` helper
(policy.py) issues `{"wiki", "diary", "context"}` to authenticated callers;
the deployer narrows this for most agents by omitting `context` or by using the
`context:sensitive_pointer` scoped form.

## Receipt behavior

Every approved read through this family produces a receipt carrying
`private_class="sensitive_pointer"` in the source metadata.  That label flows
through `ContextSource` into the audit log, making it straightforward to query
for all pointer reads in a telemetry review.

Write-path receipts (when W6 write-custody ships) will inherit the same
`private_class` label, keeping pointer-touching writes auditable alongside reads.

## Summary

| Property | Value |
|---|---|
| Values ever served | Never — protected-path denials are structural |
| Default posture | Deny-first (`descriptor.enabled=False`; no default grants) |
| Real wall? | Only in multi-user/multi-host deployments |
| Core ships this family | No — deployment decision only |
| Revisit triggers | Multi-user fleet, or telemetry showing repeated access failures |
