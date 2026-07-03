---
id: phoenix-port-prompt
title: Phoenix Port Prompt (Stage 1 → PNX kit)
isbrs: integrity
kind: guide
status: shelved
version: 0.1.1
date: 2026-07-02
updated: 2026-07-03
tags: [isbrs/integrity]
---

# PHOENIX-PORT-PROMPT.md — Loop Prompt for Claude Code
## Port the ICEBERGSIM Lie Detector, Stage 1, through the Phoenix

**Status: DRAFT v0.1 — work in progress.** Placeholders in `{braces}` must be
filled by Eduardo before launch. Numbers marked *(adjustable)* are proposals.

Version handles (defined in MAP.md): specimen = **ISM_LD_alfa**; regenerated
lineage = **ISM_LD_PNX**; ICEBERGSIM v2 = **ISM_RCT_R**.

**How to use:** place this file and the ratified `INTENT.md` in the working
directory, point Claude Code at them, and instruct: *"Execute
PHOENIX-PORT-PROMPT.md. INTENT.md is constitutional. Do not deviate from the
rails."*

---

## MISSION

Distill a complete, implementation-independent Phoenix specification from the
Stage 1 lie-detector codebase (ISM_LD_alfa, commit `cf694b1`), under the
constitutional constraint of `INTENT.md`; then prove the spec by regenerating
a fresh implementation (ISM_LD_PNX) from the spec alone and driving it to green against the
canonical tests — without consulting the original code.

You are porting an organism, not improving one. Fidelity is the only virtue.

**Division of labor (do not renegotiate it):** the tests adjudicate you; you
adjudicate behavior; Eduardo adjudicates intent. Where behavior and intent
collide, you file the collision (DRIFT protocol) and move on. You never
resolve constitutional questions yourself.

---

## INPUTS

- `{PATH_TO_STAGE1}` — Stage 1 repository (ISM_LD_alfa) at commit `cf694b1`.
  **READ-ONLY.**
- `INTENT.md` — ratified constitutional intent. **READ-ONLY.**
- `{PATH_TO_V2}` — ICEBERGSIM v2 (ISM_RCT_R) repository. **READ-ONLY.** Style reference
  only: its `spec/` directory (AXIOMS.md, SPEC.md, ARCHITECTURE.md,
  tests.yaml, INSTALL.md, traceability/) is the house style this port must
  match — MUST/MUST-NOT language, structured errors as data, reproducibility
  manifests, RESERVED-with-structured-errors for out-of-scope behavior,
  canonical tests parsed from tests.yaml as first-class pytest cases.
- Working directory: `{PATH_TO_WORKDIR}` — all new files live here.

---

## HARD RAILS — non-negotiable

**R1. Quarantine.** The Stage 1 source is a read-only reference specimen.
Never modify it. Never copy files from it into the regenerated
implementation. The regenerated implementation must not import from, link
to, or read the quarantined tree — enforce by path discipline during Phase 5
and verify by audit (grep the regenerated tree for any reference to the
quarantine path; zero hits required).

**R2. Verify before distilling.** Before writing one line of spec: run the
existing test suite in the Stage 1 repo. Record the environment (Python,
NumPy, SciPy exact versions; platform). Expected: **101 passing** at
`cf694b1`. If the count differs or any test fails: **STOP. Report. Do not
spec against unverified behavior.** The record yields to the artifact; but a
red artifact yields to Eduardo.

**R3. Anchor case zero, pre-committed.** Before general distillation:
locate and run the planted-subversion catch (design record: p ≈ 0.0006).
Extract the exact configuration and seed; record the **bit-exact** p-value
and every intermediate the manifest requires. Freeze this as `tests.yaml`
**case 0**. If the catch cannot be reproduced from the artifact: **STOP.
Report.**

**R4. DRIFT protocol (from INTENT.md §13).** Wherever observed behavior
contradicts a ratified INTENT clause: log `DRIFT-NNN` (behavior: file/line/
test; intent clause; one-sentence contradiction; available resolutions).
Where behavior falls outside INTENT's coverage: log `INTENT-GAP-NNN`. In
both cases the spec records **observed behavior**, tagged with the item id.
**Never** fix code to match intent. **Never** canonize a contradiction
without its tag. Bugs are DRIFT items, not fixes.

**R5. Scope fence (INTENT.md §9).** Spec Steps 1–6 only — the organism that
exists. Stubs or reservations for Steps 7–12 are specced as RESERVED with
structured errors, v2-style: explicitly rejected, never silent. No feature
additions. No refactors. No API "cleanups." No performance improvements.

**R6. Lineage fence (INTENT.md §8).** Do not rewire Stage 1 or its
regeneration to depend on ICEBERGSIM v2. Inventory embedded machinery that
duplicates v2 functionality and log each as `LINEAGE-NNN` for the future
behavior-preserving migration. Port first; migrate never — that is a
separate, later task.

**R7. Full Phoenix cycle.** The port is not spec-writing. It is spec →
quarantine → regenerate from spec alone → canonical tests → iterate to
green. A spec that has not survived its own resurrection is a hypothesis,
not a specification.

**R8. Tolerance policy — explicit, per test, never implicit.** Canonical
expected values are recorded bit-exact under the pinned environment
(recorded in INSTALL-LIE.md). For each canonical case, state the comparison
policy: `exact` (bitwise), or `rtol/atol` with justification (floating-point
reductions whose order is not pinned by the spec). Anchor case zero is
`exact` under the pinned environment. Any case downgraded from `exact` must
say why in one sentence.

**R9. Session budget and checkpoints** *(adjustable)*. Commit a checkpoint
at the end of every phase, message prefixed `PHOENIX-PORT:`. If context
grows stale, re-read INTENT.md and this file before proceeding — the rails
outrank your momentum.

**R10. STOP conditions.** Halt and produce a report for Eduardo if any of:
- R2 or R3 fails (suite not green; anchor not reproducible).
- DRIFT + INTENT-GAP count exceeds **15** *(adjustable)* — that is
  structural divergence between artifact and intent, and porting must pause
  for constitutional review.
- Regeneration (Phase 6) is not green after **3** *(adjustable)* full
  iterations — the spec is under-determined; report which behaviors resisted
  specification instead of brute-forcing a fourth pass.
- Any instruction here conflicts with INTENT.md — INTENT wins; report the
  conflict.

---

## PHASES — each with an exit criterion

**Phase 0 — Verify the specimen.**
Run the Stage 1 suite (R2). Deliver: `PORT-LOG.md` §0 with environment pins,
test count, wall time.
*Exit: 101 green, environment recorded.*

**Phase 1 — Freeze the anchor.**
Reproduce the planted-subversion catch (R3). Deliver: `tests.yaml` case 0
(config, seed, bit-exact expected values, `exact` policy) + PORT-LOG §1.
*Exit: case 0 reproduces twice consecutively, bit-identical.*

**Phase 2 — Inventory and classify.**
Map the repo: modules, entry points, the Step 1–6 boundary as implemented,
Step 7–12 stubs, embedded v2-duplicate machinery (`LINEAGE-NNN`). Classify
all 101 tests: **constitutional** / **behavioral** / **scaffolding** —
as a *proposal* for Eduardo (INTENT.md OPEN §12.5), with one-line rationale
each. Deliver: `TRACEABILITY.md` (test → behavior → spec-section map,
classification column) + PORT-LOG §2.
*Exit: every test classified; step boundary documented; LINEAGE register
opened.*

**Phase 3 — Distill the constitution and the spec.**
Write, in v2 house style:
- `AXIOMS-LIE.md` — the invariants the code **actually enforces**, audited
  clause-by-clause against INTENT.md. Every mismatch → DRIFT/INTENT-GAP
  (R4). Every axiom cites the evidence (module/test) that enforces it.
- `SPEC-LIE.md` — complete behavioral specification: data model; the Lie
  Generator's implemented lie types and parameters; Detector A's statistic
  and reference distribution; Discriminator B's features and calibration;
  the p-value machinery; regime labeling (verification vs. forensics,
  INTENT §2); output schema incl. reproducibility manifest; validation and
  structured errors; RESERVED behaviors.
- `ARCHITECTURE-LIE.md` — design rules (pure functions over frozen data,
  RNG always injected, validation as data, I/O at edges — confirm against
  the artifact, drift-log deviations).
Deliver: the three documents + updated DRIFT/INTENT-GAP registers.
*Exit: a competent implementer could, in principle, rebuild from these three
files plus tests.yaml without seeing the code.*

**Phase 4 — Translate the tests.**
Translate every **constitutional** and **behavioral** test into
language-agnostic canonical cases in `tests.yaml` (inputs as data, expected
outputs as data, tolerance policy per R8). Scaffolding tests: excluded from
canonical set, recorded in TRACEABILITY with reason. Write the pytest bridge
that runs tests.yaml as first-class cases (v2 pattern). Deliver: complete
`tests.yaml` + bridge + PORT-LOG §4.
*Exit: canonical suite runs green against the ORIGINAL Stage 1 code — the
tests are proven faithful before the code is deleted from view.*

**Phase 5 — Quarantine.**
Seal the original: no path from the regeneration workspace to
`{PATH_TO_STAGE1}`. Fresh directory, spec files + tests.yaml + INSTALL-LIE
only.
*Exit: audit shows zero references to the quarantine path.*

**Phase 6 — Regenerate and iterate.**
Implement from `spec/` alone. Run canonical tests. Iterate to green (≤ 3
full iterations, R10). Where a test fails because the spec under-determined
behavior: amend the spec (that is the spec failing, not the code), log the
amendment in PORT-LOG, re-run.
*Exit: full canonical suite green, including case 0 bit-exact.*

**Phase 7 — Report.**
Assemble `spec/` (AXIOMS-LIE.md, SPEC-LIE.md, ARCHITECTURE-LIE.md,
tests.yaml, INSTALL-LIE.md with environment pins, traceability/), final
DRIFT/INTENT-GAP/LINEAGE registers, PORT-LOG, and a one-page summary for
Eduardo: what ported cleanly, what drifted, what needs his ruling.
*Exit: Eduardo can adjudicate every open item from the report alone.*

---

## ACCEPTANCE CRITERION — pre-committed, not negotiable after the fact

The port is **done** when a fresh implementation (ISM_LD_PNX), regenerated
from `spec/` alone, reproduces anchor case zero — same seed, same configuration, same
p-value, bit-exact under the pinned environment — and passes the full
canonical suite, **without consulting the quarantined code**.

Anything less is a hypothesis with good posture.

---

## DELIVERABLES CHECKLIST

- [ ] `spec/AXIOMS-LIE.md`
- [ ] `spec/SPEC-LIE.md` (id proposal: `LIESPEC 0.1.0-alpha.1` — Eduardo may
      rename, INTENT OPEN §12.8)
- [ ] `spec/ARCHITECTURE-LIE.md`
- [ ] `spec/tests.yaml` (case 0 = the anchor catch, `exact`)
- [ ] `spec/INSTALL-LIE.md` (environment pins from Phase 0)
- [ ] `spec/traceability/TRACEABILITY.md` (101 tests mapped + classified)
- [ ] `DRIFT.md` (DRIFT + INTENT-GAP + LINEAGE registers)
- [ ] `PORT-LOG.md` (per-phase record)
- [ ] Regenerated implementation, canonical-green, quarantine-clean
- [ ] One-page adjudication summary for Eduardo

---

## PLACEHOLDERS TO FILL BEFORE LAUNCH

- `{PATH_TO_STAGE1}` = ______ (must be at commit `cf694b1`; verify with
  `git rev-parse HEAD`)
- `{PATH_TO_V2}` = ______
- `{PATH_TO_WORKDIR}` = ______
- Confirm/adjust: DRIFT cap (15), regeneration iterations (3)
- Attach: **ratified** INTENT.md (v1.0). A draft INTENT binds nothing, and
  a loop with a non-binding constitution is a loop with no constitution.
