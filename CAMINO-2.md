---
id: camino-2
title: CAMINO II — From Signed Constitution to First Number
isbrs: program
kind: guide
status: active
version: 1.0.0
date: 2026-07-04
updated: 2026-07-04
tags: [isbrs/program]
---

# CAMINO II — The Walking Order, Phase B onward

**Status: v1.0, 2026-07-04.** Picks up where CAMINO.md ended: the
constitution is signed (v1.0.0, tag `constitution-1.0.0`), Phase A
complete, B1 complete. This is the road from a governed-but-empty repo to
the north star — the first honest false-alarm rate.

**The north star, restated:** one sentence — *"on N messy-but-honest
simulated trials, the instrument flags X%."* Everything below is on the
critical path to that sentence or it is ceremony. Steps marked 🖥️ need the
Mac Studio (alfa lives there); the rest run from any machine. Steps marked
⚠️ cross a gate or a one-way door.

---

## Where we are (the board)

- **Constitution:** signed, v1.0.0. Governance now only via Gate G1.
- **Seed exam:** Mozambique / ANC-SEAL — sealed, role EXAM, BLIND.
- **First calibration template:** IST-1 / SEAL-IST — drafted, role
  CALIBRATION, status `pending` (awaiting fork + license confirmation).
- **Code:** none yet. That starts now.

---

## STEP B5 — Session Zero: enforcement + the umbilical spike
*(any machine; the first coding session)*

Launch CCd in the `icebergsim-integrity` clone with the B5 packet. It does,
in order:

1. **The umbilical spike (reports before building on it).** Install
   `icebergsim-rct` as a dependency; simulate one honest trial; try to
   extract participant-level rows. Report one of four verdicts:
   (a) rows exposed; (b) computed-but-not-exposed → draft an upstream
   feature request, don't implement; (c) no row-level form; (d) rows
   exposed but **dimensionally insufficient** (one outcome, no covariate
   structure — the expected verdict, per our B6 discussion). The verdict
   is an inventory of what RCT_R provides vs. what B6 must build fresh, not
   a blocker.
2. **Package skeleton** — `pyproject.toml`, `src/icebergsim_integrity/`
   (that name; never the ancestor's — L9), pytest wiring so
   `tests/constitutional/` runs and passes locally.
3. **CI** — GitHub Actions; the constitutional job is required; red blocks
   merge. The moment "laws are tests" becomes a locked door.
4. **The anomaly-output schema** + its constitutional tests — regime field
   (two values only), mandatory payload (statistic, reference
   distribution, false-alarm context), forbidden-vocabulary test. Frozen,
   pure-core (L1, L2, L12).
5. **The seed-verification kernel, v1** — regenerate allocation from
   committed seed → integer-exact compare → report; regime `verification`;
   no floats in the comparison path; exhaustive tests (L5). Built freely,
   then **handed to EB** — do not build past the handoff this session.

**Your closing act ⚠️ (L5, as amended):** review the seed kernel (or bring
it here and we review together) and **accept it**. Your yes starts the
freeze — from that moment, changes to the kernel cross Gate G1. The law's
first enforcement is executing its own first amendment.

**Exit:** CI green on `main`; schema + kernel committed; kernel accepted.
Bring the spike verdict back — it shapes everything downstream.

---

## STEP B4 — The quarry from alfa  🖥️
*(needs the Mac Studio; can run any time after B5, or before if at home)*

Launch CCd with the B4 packet, pointed at both alfa (read-only,
`cf694b1`) and the integrity clone. It:

1. Verifies the specimen: alfa at `cf694b1`, 101 tests green, env pinned.
   (Any deviation → STOP.)
2. Writes `quarry/BENCHMARK-LIE.md` — the exact recipe + seed + bit-exact
   p of the planted-subversion catch. This is alfa's DNA transfer and
   doubles as alfa's seal. (0.0006 is alfa's number, never beta's target;
   beta inherits the *lie*.)
3. Writes `quarry/TEST-IDEAS.md` — the 101 tests skimmed as ideas, never
   code.
4. Tags alfa `alfa-sealed-cf694b1` (the museum plaque) — the one allowed
   write, a ref not source.

**Optional, any time:** publish alfa as `icebergsim-integrity-alfa` and
GitHub-Archive it (read-only museum). Low priority, your call.

**Exit:** the quarry lives in `main`; alfa is read-only forever.

---

## STEP F1 — The IST fork ⚠️  (the first CALIBRATION seal ceremony)
*(any machine with a browser + git; low-stakes, satisfying)*

Complete SEAL-IST. In order:

1. ⚠️ **Confirm the dataset-record license.** CC-BY is confirmed for the
   database paper; check the Edinburgh DataShare record itself (handle
   10283/124) permits redistribution. If more restrictive → STOP, don't
   mirror, reassess.
2. Download the data file(s) + variable dictionary from DataShare.
3. Fork/mirror to public `ebergel/ist-1-database` with a NOTICE file
   (full citation + DOI 10.7488/ds/104 + CC-BY — attribution is a
   redistribution condition, not a courtesy).
4. Record in SEAL-IST: commit hash, filename(s), SHA-256, size, exact
   dimensions; extract the codebook from the variable dictionary.
5. Flip SEAL-IST `status: pending → active`; add the registry row to
   SOP-DATA §6.

**Exit:** the teaching hospital has its first real skeleton, lawfully
vaulted and hash-pinned. (Parallel, later: audit the 50-trial benchmark
for a CC0/CC-BY subset — the eventual portfolio of templates.)

---

## STEP B6 — The honest-trial generator  (integrity's own module)
*(the biggest build; starts after B5; needs F1's seal for real texture)*

The generator that makes realistic honest trials — integrity's, not
RCT_R's (that boundary is settled: RCT_R plans trials; integrity audits
them). Three layers, in order:

1. **Table 1 layer** — plasmode covariates: estimate the joint structure
   (marginals + correlation matrix / copula) from IST-1 under Gate G3,
   sample synthetic patients fresh. Real structure, synthetic people.
2. **Outcome layer** — multiple endpoints per participant, correlated with
   each other and with baseline, via explicit seeded mechanisms. This is
   what gives the strong null its teeth and the future MAX-delta a vector
   to range over.
3. **Mess layer** — RCT_R's pragmatic imperfections on top, now
   covariate-aware (dropout depending on age, noncompliance clustering by
   site) — because honest mess correlated with baseline is what mimics
   fraud (L8's "messy-honest").

Pure-core (L12), every output through the harness (L11). It is calibration
infrastructure, so it needs no L3 gate itself — but everything downstream
of it does.

**Exit:** the generator emits stamped, tidy, multi-outcome,
covariate-rich honest trials on demand — the fuel for the first
calibration.

---

## STEP B7 — The first detector + its calibration gate  ⚠️(G2 territory ahead)
*(the north star lands here)*

1. Build the **first forensic statistic** (Discriminator B, simplest
   useful version) over the generator's output.
2. Build its **null-calibration gate** (L3): run it over thousands of
   messy-honest generated trials; measure empirical Type I error at every
   alpha; it merges only if calibrated. No p quoted deeper than
   calibration reaches (L4).
3. **The first number exists:** the false-alarm rate. Report it — with its
   reference distribution and regime label, in the schema's shape, never as
   a verdict.

⚠️ Any claim about this number leaving the repo crosses **Gate G2** — and
G2 requires the false-alarm rate to already exist, which after this step it
does. First eligible G2 moment in the program's life.

**Exit — the north star:** *"on N messy-but-honest simulated trials, the
instrument flags X%."* When it exists, `integrity.icebergsim.com` gets its
first content: that number and the tables behind it. Not before.

---

## After the north star (the map's roadmap, in brief)

Sequenced in MAP.md §4: the invisibility frontier (which lies, at what
size, are catchable) → teach both instruments stepped-wedge → the adaptive
adversary → external fire (blinded challenge) → and only then the naked run
on Mozambique, interpretation rule pre-committed in writing before any
output is seen (L10).

---

## Decisions parked for EB (no rush)

1. Alfa public museum: publish-and-archive, or local seal only (B4).
2. The 50-trial benchmark portfolio: which CC0/CC-BY subset to seal, after
   IST proves the ceremony (F1).
3. Where B6 eventually lives long-term: stays integrity's, or upstreams to
   RCT_R once stable (leaning: stays integrity's; revisit at maturity).

*Caminante: the constitution is signed. Now the instrument gets built —
inside a system where cheating is harder than doing it right.*
