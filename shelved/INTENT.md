---
id: intent-ld
title: INTENT — Constitutional Intent (Stage 1 Port)
isbrs: integrity
kind: guide
status: shelved
version: 0.1.1
date: 2026-07-02
updated: 2026-07-03
tags: [isbrs/integrity]
---

# INTENT.md — Constitutional Intent for the ICEBERGSIM Lie Detector
## Stage 1 Phoenix Port

**Status: DRAFT v0.1 — work in progress. Binds nothing until ratified.**

Compressed from the Bergel–Claude design record, 2026-07-02.
Author of record: Eduardo Bergel. Compressor: Claude (Fable 5).
Ratification protocol: §14. Open questions: §12.
Version handles (defined in MAP.md): the Stage 1 specimen = **ISM_LD_alfa**;
its Phoenix resurrection = **ISM_LD_PNX**; ICEBERGSIM v2 = **ISM_RCT_R**.

---

## 0. What this document is, and what it is not

The Phoenix method separates source from render: specification is source, code
is translation. But a specification distilled from code alone captures **what**
the code does and loses **why** it does it. For ICEBERGSIM v2 that loss was
acceptable — the ancestor carried decades of earned trust. Stage 1 of the lie
detector is young and unaudited. Its code is **evidence of intent, not
constitution**. Where code and intent diverge, that divergence is called
**drift**, and drift must surface as a decision for the author — never be
silently canonized into the spec, never be silently "fixed" by an agent.

This document is the intent side of that collision. It states the invariants
the instrument was designed to enforce and the reasons behind them, so that
the Phoenix port has a constitution to check behavior against.

**Epistemic honesty clause.** This document is itself a render — compressed
from a design record, not quoted from transcripts. The compressor is a lossy
channel. Therefore every claim below carries a provenance tag, and the only
non-lossy store of intent — Eduardo — must ratify before any clause binds.

**Provenance tags:**

- `[ANCHORED]` — pinned by the explicit design record. High confidence.
- `[INFERRED]` — reconstructed from design logic; coherent with the record
  but not verbatim in it. Requires ratification.
- `[OPEN]` — unknown to this document. Must be answered by Eduardo or by
  the code itself (and if only by the code, the answer is *behavior*, not
  intent, and should be ratified explicitly).

---

## 1. Purpose axiom — what the instrument is

`[ANCHORED]` The lie detector manufactures a **frequency-independent
verifier for trial integrity**. Code and mathematics have such verifiers for
free (the test passes or fails; the proof holds or breaks). Trial integrity
has none: whether a randomized trial was conducted as claimed is ordinarily
adjudicated by consensus, reputation, and post-hoc forensics — all
frequency-dependent, all flatterable. This instrument exists to make a class
of integrity claims **verifiable or statistically boundable**, independent of
who asserts them.

`[ANCHORED]` It is a detector of **anomalies relative to a declared design**,
not a fraud oracle. See §6.

`[INFERRED]` Scope of the integrity claims, Stage 1: subversion of the
randomization/allocation process and data-level manipulation of a completed
two-arm trial dataset. Broader claims (site-level fabrication networks,
multi-trial forensics) are future stages, not Stage 1 intent.

---

## 2. Two-regime axiom — verification above the floor, forensics below

`[ANCHORED]` The instrument's foundation is a **pre-committed random seed**
as the incorruptible floor.

- **With** a public, pre-committed seed: allocation subversion is detectable
  with **certainty**. The claimed allocation either regenerates from the seed
  or it does not. This is *verification* — deterministic, binary, not
  statistical.
- **Without** the seed floor: only **distributional forensics** remain —
  statistical evidence, never certainty.

`[ANCHORED]` The instrument MUST never blur which regime a claim comes from.
Every output that asserts or suggests anomaly MUST be labeled as
*verification* (floor) or *forensics* (statistics). Conflating the two is a
constitutional violation, not a style error.

`[ANCHORED]` Policy intent behind the floor: seed pre-commitment is cheap,
implementable trial infrastructure. The instrument is also an argument — a
demonstration that a mandatory committed-seed ledger would convert an entire
class of fraud from "statistically arguable" to "mechanically impossible to
hide." The design should keep this demonstration crisp.

`[INFERRED]` The floor is out of bounds for the adversary **by
construction**: the Lie Generator may manipulate anything except the
committed seed and its published hash. A lie that requires corrupting the
floor is defined out of the game, because in deployment it is defined out by
cryptography and publication, not by trust.

---

## 3. Orthogonality axiom — two detectors, two axes, by construction

`[ANCHORED]` There are two detection instruments, and their separation is
architectural, not accidental:

- **Detector A — the causal axis.** Operates on the randomization/design
  structure: what the declared design implies must be true of the data as a
  consequence of how assignment was generated.
- **Discriminator B — the forensic axis.** Operates on distributional
  texture: what honest data-generating processes look like, independent of
  the causal design.

`[ANCHORED]` **Why orthogonality:** a lie must evade both axes
simultaneously. Two correlated detectors are one detector wearing two badges
— double confidence, no additional constraint. Orthogonality is what makes
the pair stronger than either alone.

`[INFERRED]` Secondary reason: regime hygiene (§2). A must remain exact where
the floor makes exactness possible; B is irreducibly statistical. Keeping
them orthogonal prevents B's calibration uncertainty from contaminating A's
verification claims.

`[OPEN]` The precise statistics implemented in A and B at `cf694b1` — which
test statistics, which features, which reference distributions. The port
must extract these from the code and record them in SPEC; Eduardo ratifies
whether the implemented statistics match intent or are Stage-1 placeholders.

---

## 4. Adversarial axiom — the generator sharpens, it never certifies

`[ANCHORED]` The **Lie Generator is causal**: it produces lies by
*intervening on the data-generating process* (subverting allocation,
selectively excluding, reclassifying outcomes, fabricating records), not by
painting statistical artifacts onto finished outputs. Lies are grown, not
photoshopped — because only grown lies have the propagating consequences
that a causal detector can catch.

`[ANCHORED]` The adversarial game (generator vs. detectors) exists to
**sharpen** the detectors. It can never **certify** them: self-play is
self-graded homework. Certification requires external fire — blinded
challenges by adversaries who are not the authors, and ultimately real data.

`[INFERRED]` The generator operates under a **plausibility budget**: it must
produce datasets an honest-looking trial could have produced, not arbitrary
noise. An unconstrained generator proves nothing when caught.

`[OPEN]` Which lie types are implemented at `cf694b1`, and whether the
planted subversion behind the anchor catch (§11) is allocation subversion
specifically. Believed yes; the code must confirm.

---

## 5. Calibration-before-accusation axiom

`[ANCHORED]` **No sensitivity claim before a specificity measurement.** The
detector's false-flag rate must be measured on **honest-messy** trials —
trials with the pragmatic imperfections of real research (differential loss
to follow-up, noncompliance, crossover, imperfect ascertainment) — not on
clean nulls. Honest mess mimics fraud signatures; a detector calibrated on
clean nulls will convict honest trialists.

`[ANCHORED]` The detector's operating threshold (alpha) is set on the
honest-messy reference distribution. ICEBERGSIM v2 is the designated
honest-trial generator for this calibration.

`[ANCHORED]` **Ethical grounding:** an uncalibrated fraud detector is an
accusation machine, and its Type I error is denominated in reputations.
This axiom is not a statistical preference; it is the instrument's ethics.

`[INFERRED]` Stage 1 as built likely calibrates against cleaner nulls than
this axiom demands (v2's pragmatic-imperfection engine post-dates Stage 1's
construction). If so, that is not drift to be "fixed" during the port — it
is a recorded limitation, and closing it is roadmap work (the port freezes
behavior; see §9).

---

## 6. Anomaly-not-verdict axiom — output humility, sharpened

`[ANCHORED]` Inherited from ICEBERGSIM v2's output-humility axiom and
sharpened for this instrument: outputs MUST NOT label any trial or dataset
"fraudulent," "honest," "fabricated," or any synonym of verdict. Outputs
report **anomaly statistics relative to a declared design**, each with its
regime label (§2) and its calibrated reference distribution (§5) attached.

`[ANCHORED]` A flag is a reason to look, never a finding. Judgment belongs
to humans and institutions — investigators, editors, regulators, courts.

`[INFERRED]` Structural enforcement is intended, not just tonal: output
schemas should make it **hard to launder a flag into an accusation** — no
verdict-shaped fields, reference distribution and false-flag rate travel
with every flag, regime label mandatory.

---

## 7. Transparency and reproducibility axiom (inherited)

`[ANCHORED]` Full inheritance of v2's transparency axiom: no output depends
on hidden state. Every result reproducible from the input definition, the
spec/software version, the seed, the RNG algorithm name, and the analysis
method. Every result carries a reproducibility manifest.

`[INFERRED]` For this instrument the axiom is doubled: a **detector of
integrity violations must be beyond reproach on its own integrity**. Its
claims must be independently regenerable, or it becomes the thing it hunts.

---

## 8. Lineage axiom — downstream symbiont, ancestor pristine

`[ANCHORED]` The detector lives **downstream** of ICEBERGSIM v2 (ISM_RCT_R): separate
repository, v2 consumed as a dependency, v2's core never forked or modified
for the detector's convenience. The classical instrument stays pristine; the
mutation lives in the descendant. (Asymmetric symbiont, applied to
repositories.)

`[INFERRED]` **Sequencing consequence for the port:** Stage 1 predates v2's
Phoenix release and likely embeds its own simulation machinery. The port
does NOT rewire Stage 1 to consume v2 — that is a behavior-affecting
migration. Order of operations: **port first** (behavior frozen, spec
distilled, regeneration green), **migrate second** (behavior-preserving
refactor onto v2 as dependency, adjudicated by the canonical tests). The
port must *inventory* embedded machinery that duplicates v2 and log it as
LINEAGE items for the migration; it must not perform the migration.

---

## 9. Scope axiom — spec the organism that exists

`[ANCHORED]` Stage 1 = Steps 1–6, complete at commit `cf694b1`, 101 tests
passing. Steps 7–12 are designed but unbuilt.

`[ANCHORED]` The port specs **only what exists**. Steps 7–12 are design
intentions, not behavior; they MUST NOT be specced as if implemented. Where
the code contains stubs or reservations for them, the spec records them as
RESERVED with structured errors (v2's pattern: explicitly rejected, never
silent).

`[ANCHORED]` The port adds no features, performs no refactors, "improves"
nothing. A bug discovered during the port is a DRIFT item (§13) — a decision
for Eduardo — never a silent fix. The Phoenix resurrects; it does not edit
the genome mid-resurrection.

---

## 10. Interpretation pre-commitment axiom (standing principle)

`[ANCHORED]` Before this instrument is ever run against real trial data —
including and especially the author's own — the **interpretation rule must
be pre-committed in writing**: what will be done with each class of flag,
decided before any output is seen. An integrity instrument whose outputs are
interpreted post hoc by an interested party is theater. Pre-registration
discipline, applied to ourselves first.

`[INFERRED]` This axiom has no code counterpart in Stage 1 and needs none
yet; it binds *use*, not implementation. It is recorded here so the
constitution carries it forward before Mozambique.

---

## 11. Stage 1 anchors — the facts the port is pinned to

`[ANCHORED]` Commit: `cf694b1` — the artifact ISM_LD_alfa — on Eduardo's machine (Mac Studio M3 Ultra;
Python / NumPy / SciPy stack). **101 tests passing** at that commit.

`[ANCHORED]` **The anchor catch:** a planted synthetic subversion detected
at **p ≈ 0.0006**. This is the golden case — *anchor case zero* of the
canonical test set.

`[ANCHORED]` Precision discipline: "≈ 0.0006" is the design record's
approximation. The **bit-exact** value, with the exact seed and
configuration that produce it, must be extracted from the artifact itself
during the port (Loop Phase 1) and frozen. If the artifact cannot reproduce
the catch, the port STOPS and reports — the record yields to the artifact,
never the reverse.

`[OPEN]` Exact contents of Steps 1–6 vs. 7–12 — the step boundary as
implemented. The port extracts this from code and design docs in the repo;
Eduardo ratifies the boundary.

---

## 12. OPEN register — what this document does not know

1. `[OPEN]` The implemented statistics of Detector A and Discriminator B
   (§3).
2. `[OPEN]` The implemented lie types in the Generator; the lie type of the
   anchor catch (§4).
3. `[OPEN]` The exact seed + configuration of anchor case zero (§11).
4. `[OPEN]` The Step 1–6 / 7–12 boundary as implemented (§11).
5. `[OPEN]` Which of the 101 tests are **constitutional** (pin invariants),
   which are **behavioral** (pin correct-but-contingent choices), and which
   are **scaffolding** (development artifacts). The loop proposes a
   classification; Eduardo ratifies. Scaffolding may be excluded from the
   canonical set but must be recorded in traceability.
6. `[OPEN]` Whether any machinery is shared with the **unified-asymmetry
   randomization test** (the MAX-delta / strong-null-first mutation). That
   is a *separate branch* of the ICEBERGSIM program. Intent here: do not
   conflate the branches; if shared machinery exists in code, log it as a
   LINEAGE item, do not spec it into the detector's constitution.
7. `[OPEN]` Stepped-wedge readiness. Believed **absent** (v2's ceiling is
   cluster pre/post; Stage 1 predates even that). If confirmed absent,
   record as RESERVED — it is on the Mozambique critical path but out of
   port scope.
8. `[OPEN]` Naming: spec identifier and version for the detector (proposal:
   `LIESPEC 0.1.0-alpha.1`; Eduardo may rename the instrument and the spec
   line entirely).
9. `[OPEN]` Environment pins at `cf694b1` (exact Python/NumPy/SciPy
   versions) — required for the bit-exactness policy (see loop prompt,
   Tolerance Policy).

---

## 13. DRIFT protocol — definition

A **DRIFT item** is any point where observed Stage 1 behavior contradicts a
clause of this document, once ratified.

- Each item is numbered (`DRIFT-001`, …) and records: the behavior (file,
  line, test), the intent clause violated, the contradiction in one
  sentence, and the available resolutions.
- The loop **never resolves drift silently in either direction**: it neither
  "fixes" code to match intent nor canonizes code against intent. The spec
  records observed behavior tagged with the DRIFT id; the decision lands on
  Eduardo's desk.
- The complement is an **INTENT-GAP item**: code behavior that this document
  simply does not cover. Same discipline — numbered, logged, surfaced.
- The DRIFT/INTENT-GAP report is a first-class deliverable of the port. It
  is the only audit that shows where Stage 1 diverged from its designers.

---

## 14. Ratification and revision protocol

1. Eduardo reads this draft and, per clause: **ratifies**, **amends**, or
   **strikes**. `[INFERRED]` clauses especially — they are the compressor's
   reconstruction, and the compressor is lossy.
2. Items in the OPEN register are answered by Eduardo where he holds the
   answer, and left to Phase-extraction where only the artifact does.
3. On ratification the document becomes `v1.0 — RATIFIED` and binds the
   port. Until then it binds nothing.
4. Amendment after ratification follows the same rule as everything else in
   this program: explicit, versioned, and logged. No silent edits to a
   constitution.

*I might be wrong but I'm not lying: every uncertain clause above is tagged
as uncertain. — the compressor*
