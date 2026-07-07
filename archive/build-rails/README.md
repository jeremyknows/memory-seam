# Build rails — historical process ledger (non-shipping)

This directory holds the L5/L6-series build-rail ledger: the receipted,
issue-bound decision packets, denial-before-callback scaffolding, and
their tests that Memory Seam's construction process produced between
roughly issue #130 and issue #370. It is **not part of the installable
package** and is excluded from both the sdist and the wheel — `pip
install memory-seam` never sees this directory.

## Why this exists

Memory Seam was built under a heavily-gated, multi-agent process: every
implementation slice required an explicit human approval packet, a
denial-before-callback proof, and a trust-boundary review before the next
slice could start. That discipline is real and it produced a fail-closed
core that a blind external review confirmed "coherent and actually
enforced, not just asserted." But the packets themselves — the
`l6aa`...`l6ar`, `l6x`/`l6y`/`l6z` chain and its ~130 companion docs and
~130 test files — are process exhaust from *how* the seam was built, not
part of *what* it does. A cold reader of the repo met roughly 10x more
rail-doc volume than functional payload.

Two independent blinded agent reviews (see [issue
#1](https://github.com/jeremyknows/memory-seam/issues/1)) confirmed this:
the functional core was rated genuinely good, but the rail corpus was
judged to be burying it. This directory is the response — the ledger is
preserved here for provenance and audit, out of the way of anyone trying
to evaluate or use the package.

## What's actually shipped

The write-custody model, positive-authorization receipts, custody
receipts, and the supervised source-card preflight gate are **not**
archived — they're real, tested, shipped modules
(`src/memory_seam/write_custody_*.py`,
`src/memory_seam/positive_authorization_receipt.py`,
`src/memory_seam/custody_receipts.py`,
`src/memory_seam/supervised_source_card_preflight.py`), gated
default-off pending a future human-approved unhold. Their docs
(`docs/l6-write-custody-*.md`, `docs/l6-write-intent-*.md`,
`docs/l6v01-supervised-source-card-preflight.md`) and tests stayed in
place. What moved here is everything else in the `l6*` chain: modules
that were never wired into the installed package (`src/memory_seam/__init__.py`
never imports them), plus their docs and tests.

## Layout

- `src/memory_seam/` — the 23 isolated `l6aa`...`l6ar`/`l6x`/`l6y`/`l6z`
  modules. None of them are imported by `src/memory_seam/__init__.py` or
  by any shipped module; they only import each other.
- `docs/` — the ~130 companion decision-packet, trust-boundary-review,
  and source-floor-reconciliation docs for that chain.
- `tests/` — the ~130 test files that exercised that chain (plus their
  one shared synthetic-harness helper and the one JSON fixture used only
  by an archived test). These are not part of the `pytest` run from the
  repo root's `tests/` directory anymore.

## Running these tests

They are **not** runnable in place: moving `src/memory_seam/l6*.py` out
of the installed package means `from memory_seam.l6aa_value_proof
import ...` (and its siblings) no longer resolves under a plain
`PYTHONPATH=src:archive/build-rails/src`, because `memory_seam` is
already a regular package rooted at `src/memory_seam` and Python does
not merge a second `memory_seam` directory into it. If you need to run
this suite, check out the commit immediately before the slimming pass
(the PR that moved this directory) and run `pytest` from the repo root
at that commit. This directory is a frozen historical record, not a
maintained standalone package — that's the point of moving it out of
the way.
