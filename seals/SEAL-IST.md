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
- **Commit:** 24584c68d54e8f15c6fa71bd508483b6205ff832
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

## 3. The codebook (schema — from IST_variables.csv, ratified against data)

**Note on dimensions:** the variable dictionary documents **119 variables**; the data file `IST_corrected.csv` has **112 columns**. This 7-column discrepancy is recorded, not hidden — some documented derived variables may be absent, renamed, or reordered in the corrected version. The generator (B6) reconciles against the **actual 112 headers**, not the dictionary. Header order in the data begins: `HOSPNUM, RDELAY, RCONSC, SEX, AGE, RSLEEP, RATRIAL, RCT, RVISINF, RHEP24, RASP3, RSBP, RDEF1…RDEF8, …`.

**For the generator, the baseline (randomisation-time) block is the covariate template.** Outcome and follow-up columns inform the multi-outcome layer separately; derived/prognostic columns (EXPD*) are a bonus sealed prognostic score. Values `9`/`8` are missing codes in several fields (see OCCODE, SET14D). No distributions recorded here beyond published aggregates.

### Randomisation data (baseline — the Table 1 covariate template)

|Variable|Meaning|
|---|---|
|`HOSPNUM`|Hospital number|
|`RDELAY`|Delay between stroke and randomisation (hours)|
|`RCONSC`|Conscious state (F=fully alert, D=drowsy, U=unconscious)|
|`SEX`|M=male; F=female|
|`AGE`|Age (years)|
|`RSLEEP`|Symptoms noted on waking (Y/N)|
|`RATRIAL`|Atrial fibrillation (Y/N); not coded for pilot (984 pts)|
|`RCT`|CT before randomisation (Y/N)|
|`RVISINF`|Infarct visible on CT (Y/N)|
|`RHEP24`|Heparin within 24h prior (Y/N)|
|`RASP3`|Aspirin within 3 days prior (Y/N)|
|`RSBP`|Systolic BP at randomisation (mmHg)|
|`RDEF1`–`RDEF8`|Deficits: face, arm/hand, leg/foot, dysphasia, hemianopia, visuospatial, brainstem/cerebellar, other (Y/N/C=can't assess)|
|`STYPE`|Stroke subtype (TACS/PACS/POCS/LACS/other)|
|`RDATE`,`RTIME`,`HOURLOCAL`,`MINLOCAL`,`DAYLOCAL`|Randomisation date/time fields|
|`RXASP`|Trial aspirin allocated (Y/N) — **allocation**|
|`RXHEP`|Trial heparin allocated (M/L/N) — **allocation**|

### 14-day / discharge treatments and events

`DASP14, DASPLT, DLH14, DMH14, DHH14, ONDRUG, DSCH, DIVH, DAP, DOAC, DGORM, DSTER, DCAA, DHAEMD, DCAREND, DTHROMB` (treatments given); `DMAJNCH(+D/X), DSIDE(+D/X)` (adverse events).

### Final diagnosis of initial event

`DDIAGISC, DDIAGHA, DDIAGUN, DNOSTRK, DNOSTRKX`.

### Recurrent stroke / other events within 14 days

`DRSISC(+D), DRSH(+D), DRSUNK(+D)`; `DPE(+D), DALIVE(+D), DPLACE, DDEAD(+D/C/X)`.

### 6-month follow-up

`FMETHOD, FSOURCE, FDEAD, FLASTD, FDEADD, FDEADC, FDEADX, FRECOVER, FDENNIS, FPLACE, FAP, FOAC`.

### Outcomes and derived variables (the multi-outcome layer)

|Variable|Meaning|
|---|---|
|`ID`,`TD`|Death indicator (1/0), time to death/censoring (days)|
|`ID14`|Death within 14 days (indicator)|
|`SET14D`|Known dead/alive at 14 days (1/0)|
|`OCCODE`|Six-month outcome (1=dead, 2=dependent, 3=not recovered, 4=recovered, 8/9=missing)|
|`STR14`,`ISC14`,`NK14`,`H14`|Any / ischaemic / indeterminate / haemorrhagic stroke within 14 days|
|`MI14`,`PE14`,`DVT14`,`HTI14`|MI, PE, DVT, haemorrhagic transformation within 14 days|
|`NCB14`,`TRAN14`|Any / major non-cerebral bleed within 14 days|
|`EXPD14`,`EXPD6`,`EXPDD`|**Published predicted probabilities** (death@14d, death@6m, death-or-dependency@6m) — a ready-made sealed prognostic score|
|`DEAD1`–`DEAD8`|Cause-of-death indicators|
|`TICH`,`TMAJH`|Time to cerebral bleed / major non-cerebral bleed|
|`CMPLASP`,`CMPLHEP`,`NCCODE`|Compliance (aspirin/heparin)|
|`COUNTRY`,`CNTRYNUM`|Country code|

_Full per-variable dictionary: `docs/IST_variables.csv` / `docs/IST_variables.pdf` in the mirror. Inferred groupings above are Claude's; EB ratifies. `[INFERRED]` groupings, not license-bearing._

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
