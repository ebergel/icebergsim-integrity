---
id: seal-ist-1
title: Seal — International Stroke Trial (IST-1) database
isbrs: integrity
kind: seal
status: pending
role: calibration
date: 2026-07-04
updated: 2026-07-04
tags: [isbrs/integrity]
---

# SEAL-IST.md — International Stroke Trial (IST-1), version 2

**Status: PENDING — this seal is a draft. It becomes active when EB forks
the dataset to a public `ebergel/` mirror, records the hash of the actual
downloaded file(s), and confirms the dataset-record license. Roles,
transitions, and procedure: SOP-DATA.md. Template: this file follows the
SOP-DATA §5 seal template; ANC-SEAL.md is the reference implementation.**

**Role: CALIBRATION.** This dataset is a **generator template**, not a
blind exam. Its texture — baseline covariate marginals and their
correlation structure — will be estimated to seed the plasmode honest-trial
generator (B6, layer 1). Under SOP-DATA §1, using a real Table 1 as a
generator template is a deliberate texture exposure; CALIBRATION role
makes that lawful. One-way rule (SOP-DATA §1): a CALIBRATION dataset can
never later serve as a blind exam. IST is therefore permanently disjoint
from the exam set — which is correct: it is meant to be *seen*.

---

## 1. Why this dataset, and why CALIBRATION

The honest-trial generator must learn realistic baseline structure from
real trials, not from priors. IST-1 is chosen as the first template
because:

- **Redistribution is lawful.** The database paper (Sandercock, Niewada,
  Członkowska, *Trials* 2011, 12:101) is CC-BY — unrestricted use,
  distribution, and reproduction with attribution. A public frozen mirror
  under `ebergel/` is permitted, which a seal requires. *(Dataset-record
  license to be confirmed at fork — see §6.)*
- **The shape is right.** Per-participant: baseline covariates assessed at
  randomisation (Table 1 structure), plus outcomes at two timepoints
  (14-day and 6-month) — the covariates-plus-multi-outcome shape B6 needs,
  in one real dataset.
- **The population generalizes away from the exam.** Elderly acute
  ischaemic stroke (>26% aged over 80), cardiovascular covariate
  structure — deliberately unlike the Mozambique antenatal population
  (ANC-SEAL, the blind exam). Training the generator here and examining on
  Mozambique tests generalization, not memorization.
- **Scale and completeness.** 19,435 randomised patients, ~99% follow-up.

**Hard boundary:** the Mozambique ANC dataset (ANC-SEAL, role EXAM, BLIND)
must NEVER become a generator template. If the generator learns texture
from the exam's own population, the naked run is graded against a student
trained on the exam. IST exists so honest texture is learned from
*elsewhere*.

---

## 2. The pin

- **Trial:** International Stroke Trial (IST-1) — RCT of aspirin,
  subcutaneous heparin, both, or neither in 19,435 patients with acute
  ischaemic stroke. Primary report: *Lancet* 1997;349:1569–81.
- **Dataset:** International Stroke Trial database (version 2), University
  of Edinburgh, Department of Clinical Neurosciences.
  - **DOI:** 10.7488/ds/104
  - **Source page:** Edinburgh DataShare, handle 10283/124
  - **Registry:** (IST-1 predates ISRCTN; cite the Lancet 1997 report)
- **Mirror:** github.com/ebergel/ist-1-database (public; ODC-By;
  README + LICENSE + NOTICE present)
- **Commit:** [FILL: run `git rev-parse HEAD` in the mirror, or copy the
  latest commit hash from the repo's commit list]
- **Data file:** data/IST_corrected.csv (the corrected version
  incorporating the 2012 erratum — authoritative)
  - **SHA-256:** a350aed2329bbcde23c05caaa96b9275b44b017adecc2fd02231d590454695d5
  - **Size:** 4,798,288 bytes
  - **Dimensions:** 19,435 rows × 112 columns (one row per randomised patient)
- **Source of truth:** University of Edinburgh, DOI 10.7488/ds/104

**Gate G3 verification procedure (every use):** fetch the mirror at the
pinned commit → `sha256sum` the data file(s) → compare to this seal. On
mismatch: STOP.

---

## 3. The codebook (schema only — to be extracted at fork)

`[FILL AT FORK]` — column names, types, category levels, numeric ranges,
extracted from the dataset's own documentation (IST publishes a variable
dictionary). No distributions beyond the already-published Table 1
aggregates in the 1997 Lancet paper and the 2011 database paper. Tag
inferred meanings `[INFERRED]` for EB to ratify.

Note for B6 (the generator): the columns needed are the **baseline**
covariates (randomisation-time), for estimating the Table 1 joint
structure. The outcome and follow-up columns are not part of the covariate
template — they inform the multi-outcome layer separately. The seal
records the full schema; the generator consumes only the baseline block.

---

## 4. What CCd receives, and what it does not

**Received (read-only reference, cloned beside — never inside — beta's
repo):** the dataset documentation / variable dictionary, this seal, the
codebook.

**Not received into `icebergsim-integrity`:** the rows. Real data lives
only in its own public mirror (L10). The generator reads the mirror under
Gate G3, estimates the covariate joint distribution, and what enters the
integrity repo is the **estimated generator parameters** (marginals,
correlation matrix / copula) — a derived statistical summary, not the
microdata. Whether even those parameters count as texture-that-must-stay-
local is a G3 question for EB at B6 time.

---

## 5. Exposure log

| Date | Who | What was exposed | What was not |
|---|---|---|---|
| 2026-07-04 | Claude (conversation) | Trial metadata, license, dataset DOI, published Table 1 aggregates (age >80 share, N, follow-up %), dataset shape. | Microdata rows; the variable-level joint distribution; anything beyond the 1997/2011 published aggregates. |
| — | CCd | Nothing yet. | Everything. |

Every future exposure — including the fork, the codebook extraction, and
each Gate G3 estimation run — gets a row here, before it happens where
possible.

---

## 6. Open items before this seal goes active

1. `[VERIFY AT FORK]` **Dataset-record license.** CC-BY is confirmed for
   the *database paper*. Edinburgh DataShare dataset records can carry
   their own license terms; confirm the dataset record (handle 10283/124)
   permits redistribution before creating the public mirror. If the
   dataset record is more restrictive than the paper, STOP and reassess —
   do not mirror.
2. `[FILL]` Fork to `ebergel/ist-1-database`, add NOTICE (citation + DOI +
   license), record commit.
3. `[FILL]` Download the data file(s), record SHA-256, size, exact
   dimensions.
4. `[FILL]` Extract the codebook (§3) from the IST variable dictionary.
5. Flip `status: pending → active` and add the registry row to
   SOP-DATA.md §6:
   `IST-1 | github.com/ebergel/ist-1-database @ [commit] | 2-arm factorial, 19,435, acute stroke | CALIBRATION | ACTIVE | [date]`

*Drafted 2026-07-04. Licence of the database paper confirmed CC-BY via the
Trials 2011 open-access record; dataset-record licence pending
confirmation at fork.*
