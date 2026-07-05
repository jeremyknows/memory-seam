# ADR 0002 — Write-autonomy ceiling: every class may earn it, dangerous domains never

**Status:** Accepted (operator decision, 2026-06-09 grill session)
**Deciders:** project maintainers

## Context

The write/custody companion (seam Phase 7 / campaign rung W6) needs a declared autonomy ceiling before design: which write classes may ever operate without per-item human review, and which never may. Write classes in rising stakes: ① `draft_submit` (file a draft for review), ② `live_correction` (small evidenced fixes to existing articles), ③ `net_new_publish` (new articles live without review), ④ `curation` (merge/retire/supersession repoints), ⑤ plumbing (`reindex`, custody transfers). The alternative considered was a permanently lower ceiling (e.g., ③ net-new always human).

## Decision

**All content classes ①–④ are ELIGIBLE to earn autonomy — one class at a time, each through its own supervised pilot (≥10 operations, 0 false-promotes, 0 incorrect-halts) before graduating.** No class starts autonomous; graduation is evidence-earned and operator-ratified per class. Class ⑤: `reindex` may run autonomous **with a fire-tested kill switch**; custody transfers always notify the operator. **Permanent carve-out regardless of class: content touching security configuration, credential documentation, runbooks, or auth flows is human-reviewed forever** — wrongness in those domains is dangerous, not merely inaccurate. (Operator: "Path A — your recommendation on write-side is spot on.")

## Consequences

- W6's architecture is a **class ladder with per-class gates**, not a single autonomy switch; the Arc-A Phase-5 Resolver's `ENABLED_CLASSES` mechanism generalizes to carry it.
- ③ `net_new_publish` remains separately held behind consolidation/dedup proof (existing condition) *and* its own supervised pilot — eligibility is not activation.
- The dangerous-domain carve-out must be enforced **by classifier/path rules in the gate**, not by author judgment, and is not relitigable without a new operator ADR.
- Custody-transfer notifications become a required receipt consumer (operator-facing), shaping W6's provenance design.
