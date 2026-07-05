---
id: spike-b5-umbilical
title: Session 0 — umbilical spike verdict (B5)
isbrs: integrity
kind: session
status: decided
date: 2026-07-05
updated: 2026-07-05
tags: [isbrs/integrity]
---

# SESSION-0-SPIKE-B5.md — The Umbilical Spike

**Question.** The roadmap assumes icebergsim-rct (ISM_RCT_R, package
`icebergsim`) feeds this instrument participant-level rows — forensic
texture lives in individual rows, not summaries. True?

**Verdict: (c) — NO ROW-LEVEL FORM.** Participant rows are not exposed by
the public API, and they do not exist internally either: nothing to expose,
nothing to request upstream as a small change.

## Evidence

- Dependency: `icebergsim` 2.0.0a1, consumed from
  `github.com/ebergel/icebergsim-rct`, pinned in `uv.lock` at `5d439b2a`
  (L9: dependency, never vendored or forked).
- Public entry point: `simulate_trial(validated) -> SimulationResult`
  (`src/icebergsim/simulate.py`). The result tree bottoms out at:
  - `SimulatedTables` — four int64 arrays of shape `(n_simulations,)`:
    per-**replicate** 2×2 counts, not per-participant anything;
  - `AnalysisBatch` — per-replicate CER/EER/ARR/RR/RRR/p-value arrays;
  - `SimulationSummary` — scalars.
- Why rows never exist: `simulate_arm_counts()` (`simulate.py`, §6.3
  docstring) implements SPEC §6.2's per-participant model by **exact
  analytic collapse** — participants are i.i.d., so behavior × loss cells
  are drawn as `rng.multinomial(n, cell_probs, size=n_sims)` (six cells)
  and observed events as binomials per cell. No participant array is ever
  materialized, internally or otherwise.
- Empirical check (reproducible): one honest `individual_binary` trial,
  `total_n=400`, `intervention_fraction=0.5`, CER 0.30 / EER 0.20, seed
  `20260705` → result contains no array of size > n_simulations; deepest
  granularity is the single 2×2 table (50/200 vs 37/200). Runner:
  `scratch/spike_umbilical2.py` (scratch; the evidence above is
  re-derivable from the pinned dependency alone).
- Allocation is not a sequence: `Allocation(total_n, intervention_fraction)`
  fixes arm **sizes** deterministically. The package generates no
  per-participant randomization sequence at all.

## Inventory for B6 (the honest-trial generator)

What icebergsim-rct **provides** (consume, don't rebuild):

- Trial designs: `individual_binary`, `cluster_post`, `cluster_pre_post`.
- The pragmatic-imperfection engine (L8's "messy honesty"), per arm:
  loss, lost-event risk ratio, noncompliance, crossover, two-sided
  ascertainment error — with crossover-precedence semantics (AXIOMS §9).
- Analysis of 2×2 tables (several p-value methods), sample-size and
  power machinery, subgroups, stopping rules.
- RNG discipline: seeded PCG64, named streams; every result carries a
  reproducibility manifest (`input_hash`, seed, rng algorithm, spec
  version) — precedent for beta's own L6 manifests.

What B6 must **build fresh** (nothing upstream to unlock):

- Participant-level materialization itself: assignment vector + outcome
  vector, one row per participant (per-visit later, per the ANC seed
  schema).
- Baseline covariates with real joint structure.
- Correlated multiple outcomes.
- Allocation **sequences** (simple, permuted-block, …) — needed by the
  seed kernel's verification regime too; rct only fixes arm sizes.

**Load-bearing consequence.** L8's second clause — "or by generators
validated against it" — becomes the operative path: B6 materializes rows
itself and validates its aggregate behavior against icebergsim-rct's
exact-collapsed counts (same seeds' marginals, same 2×2 laws). The
umbilical feeds validation targets and imperfection semantics, not rows.

**No upstream feature request drafted** — that remedy belongs to verdict
(b). Exposing rows upstream would mean abandoning §6.3's exact
vectorization for a materializing sampler: a redesign of the ancestor for
the descendant's convenience, which is the thing L9 exists to prevent. If
B6 later wants an upstream row-mode anyway, that is a design decision to
put through icebergsim-rct's own spec process, with this document as the
evidence.
