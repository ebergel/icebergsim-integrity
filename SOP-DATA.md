---
id: sop-data
title: SOP — Sealing External Real Datasets
isbrs: program
kind: sop
status: draft
version: 0.1.1
date: 2026-07-03
updated: 2026-07-03
tags: [isbrs/program]
---

# SOP-DATA.md — Standard Operating Procedure: Sealing External Real Datasets

**Status: DRAFT v0.1. Referenced by CONSTITUTION-LD.md (L10, L13). Applies
to every real dataset — EB's own or third-party — that enters the program's
orbit, now or later.**

---

## 0. Why a procedure

Real datasets are the program's non-renewable resource. Each can serve as a
blind exam exactly once: the moment its texture is seen by anyone or
anything that shapes the detectors, it is spent as an exam forever. Storage
is cheap and hashes are cheap; blindness is not. This SOP exists to spend it
deliberately.

**What counts as texture (sealed for exams):** row-level values, joint
distributions, digit patterns, missingness patterns, cluster-level
heterogeneity — anything a forensic detector could learn from.
**What does not (always permitted):** schema (column names, types, levels,
ranges), dimensions, file hashes, and aggregates already published (papers,
public dashboards, repo screenshots).

---

## 1. Roles and transitions

- **EXAM (blind).** Held out for a future naked run. Nothing beyond schema,
  hashes, and already-published aggregates may be observed.
- **CALIBRATION (exposed).** Texture examinable under Gate G3: realism
  audits, planted-lie studies, tuning of the honest-trial generator.

Transitions are **one-way**: EXAM → CALIBRATION is a deliberate spend —
Gate G3, logged, dated. CALIBRATION → EXAM: never. A dataset with any
texture-exposure row in its log cannot hold or regain EXAM role.

**Portfolio rule:** at least one sealed EXAM stays blind at all times.
Prefer several. Do not spend the last one.

---

## 2. The sealing procedure (per dataset)

1. **Vault.** The canonical copy lives in a public GitHub repo.
   - Own data: publish ANCMozambique-style — data + protocol + ethics
     documentation + license in one repo. That is the house gold standard.
   - Third-party data: license permitting, **fork to `ebergel/…` as a
     frozen mirror and pin the fork.** Upstream repos can vanish or rewrite
     history; a seal pointing at unreachable bytes is dead.
2. **Pin.** Record: repo URL; commit hash (`git rev-parse HEAD`); for every
   data file, SHA-256 and byte size; dataset dimensions (rows × columns).
   Multiple copies inside the repo must be hashed individually and
   confirmed identical (or the canonical one designated).
3. **Codebook.** Extract schema only: column names, types, category levels,
   numeric ranges. No distributions, no unpublished aggregates. Tag
   inferred meanings `[INFERRED]` for EB to ratify. The extraction itself
   is a schema exposure — log it (step 6).
4. **Role.** Declare EXAM or CALIBRATION with one paragraph of rationale:
   what design type it exercises (individual / cluster / stepped-wedge /
   …), why this dataset, what it will someday test or teach.
5. **Mapping.** Note union-compatibility with beta's canonical export
   schema (L11): which columns map, which are missing (e.g., assigned vs.
   observed allocation), what the simulator must learn to emit to match.
6. **Exposure log.** Open the log with a first row recording what the
   sealing itself exposed, and to whom.
7. **Local hygiene.** Reference material (code, protocols, codebook) is
   cloned beside — never inside — beta's repository; all data files are
   deleted on arrival (`find . -name '<datafile>' -delete`). The seal makes
   deletion safe: the canonical bytes remain in the vault, re-fetchable and
   verifiable.
8. **Registry.** Add the dataset to the registry (§6).

---

## 3. Gate G3 verification (before any use, every time)

Fetch the vault at the pinned commit → hash the data file(s) → compare to
the seal.

- **Match:** proceed under the written, pre-committed interpretation rule
  (L10), with the exposure-log row written *before* the data is opened.
- **Mismatch:** STOP. The paper has changed; nothing proceeds until EB
  resolves why.

---

## 4. The exposure log (inside each seal file)

Columns: date | who (EB / Claude / CCd / detector component) | what was
exposed | what was not.

Rules: written before the exposure where possible, immediately after where
not; no exposure without a row; a dataset with any texture row is
permanently disqualified as an EXAM. An instrument that audits exposure
logs its own.

---

## 5. Seal file template

One file per dataset: `seals/SEAL-<HANDLE>.md`, inside beta's repository.

- Header: status, seal date, **ROLE**.
- §1 Purpose and role rationale.
- §2 The pin: repo, commit, per-file hashes and sizes, dimensions.
- §3 Codebook: schema only; `[INFERRED]` tags for EB to ratify.
- §4 Received / not received by CCd (local hygiene).
- §5 Exposure log.

ANC-SEAL.md is the reference implementation of this template.

---

## 6. Registry of sealed datasets

| Handle | Vault | Design | Role | Status | Sealed |
|---|---|---|---|---|---|
| ANC-MOZ | github.com/ebergel/ANCMozambique @ `d27ac54` | Stepped-wedge, 10 clusters × 11 steps, 218,277 visits | EXAM | BLIND (schema + published aggregates only) | 2026-07-03 |
| IST-1 | github.com/ebergel/ist-1-database @ [commit] | 2-arm factorial, aspirin/heparin, 19,435, acute ischaemic stroke | CALIBRATION | ACTIVE | 2026-07-05 |
*(New rows appended as datasets are sealed. CI may verify: every registry
row has a seal file, every seal hash is well-formed, and at least one EXAM
is BLIND.)*
