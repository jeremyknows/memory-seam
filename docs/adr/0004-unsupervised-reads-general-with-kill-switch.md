# ADR 0004 — Unsupervised reads: general for contract adopters, governed by kill switch + telemetry

**Status:** Accepted (operator decision, 2026-06-09 grill session — "Yes B - I agree")
**Deciders:** project maintainers

## Context

Until now every seam read traced to a live interactive session; scheduled/unsupervised reads were a held boundary with per-tick approval-phrase ceremony (the L6-era canary discipline). Campaign rung W5 needed a standing policy: how autonomous may scheduled reading get? Alternatives: (A) narrow named jobs only, each individually approved; (B) any contract adopter may schedule recurring reads (crons/loops) without per-job approval, governed by a fire-tested global kill switch and weekly telemetry review; (C) speculative background pre-fetching.

## Decision

**(B) General scheduled reads for contract adopters.** Any agent that has completed the Fleet Adoption Contract checklist (identity packet, standing instruction, telemetry duty) may run recurring seam reads on schedules or loops without per-job approval. Governance is systemic, not per-job: the global kill switch (`memory_seam_disabled`) must be honored by all adopters and **fire-tested once as a W5 exit criterion**; per-family disable switches remain; weekly telemetry review is the detection surface for pathological patterns. (C) speculative pre-fetching is deferred — an optimization that must earn its way in with demand evidence.

## Consequences

- The L6-era per-tick approval-phrase ceremony is retired for reads (the fail-closed code paths remain; only the human ceremony goes).
- W5's exit criteria become: live scheduled canary read producing bus-visible receipts + one documented kill-switch drill.
- Read autonomy and write autonomy are now formally asymmetric by design: reads general-with-kill-switch (this ADR), writes class-laddered with per-class supervised graduation (ADR 0002).
- Scheduled-read telemetry joins the weekly rollup so volume/degradation trends are reviewed, not assumed.
