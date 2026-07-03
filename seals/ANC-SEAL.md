---
id: seal-anc-moz
title: Seal — Mozambique ANC Dataset
isbrs: integrity
kind: seal
status: blind
date: 2026-07-03
updated: 2026-07-03
role: exam
tags: [isbrs/integrity]
---

# ANC-SEAL.md — Pin and Codebook for the Mozambique Dataset

**Status: sealed 2026-07-03. This file lives in ISM_LD_beta's repository.
The dataset it describes does not, and may not — see CONSTITUTION-LD.md,
L10.**

**Role: EXAM — BLIND.** (Roles, one-way transitions, and the general
procedure: SOP-DATA.md. This seal is that SOP's reference implementation.)

---

## 1. What this file is

The Mozambique trial is ISM_LD_beta's **held-out exam** (MAP.md §4, step 6).
The instrument's forensic axis learns what honest data texture looks like;
it must never learn that from the dataset that will one day examine it. So
the data stays outside the repository, behind Gate G3 — and this seal,
committed in advance, does two jobs:

1. **Tamper-evidence forward:** at Gate G3, the fetched dataset must match
   the hash below, byte for byte. The exam paper cannot be quietly swapped
   between now and then.
2. **Pre-commitment backward:** this seal proves the exam was fixed
   *before* the student was built. Nobody — including us — can later tune
   the choice of test data to flatter the instrument.

Schema is interface: required inside the repo (L11 union-compatibility).
Texture is the exam: sealed outside it.

---

## 2. The pin

- **Repository:** `https://github.com/ebergel/ANCMozambique` (public; MIT;
  ethics determination included in repo: `NHS Determination_STUDY00019267.pdf`)
- **Commit:** `d27ac5423b50ff32b8c47b5f18db6ffc6c38ce23`
- **Dataset file:** `appData.rds` — present at three paths in the repo
  (`data/`, `202407021245/`, `202407021245/www/`), all three
  **byte-identical**:
  - **SHA-256:** `c14523917354c11741a8f24d6192892665571bd6e26294fab68df9b0c37164aa`
  - **Size:** 815,503 bytes
  - **Dimensions:** 218,277 rows × 16 columns (one row per antenatal-care
    visit)

**Gate G3 verification procedure:** fetch the repo at the pinned commit,
`sha256sum` the dataset, compare against this seal. On mismatch: STOP —
the exam paper has changed, and nothing proceeds until EB resolves why.

---

## 3. The codebook (schema only — no values, no distributions)

This is L11's **seed schema**: beta's simulated-trial exports must be
union-compatible with it, so real and simulated data pour into the same
explorer. Meanings marked `[INFERRED]` were reconstructed from structure
and the trial's published design; EB ratifies or corrects.

| Column | Type | Levels / range | Meaning |
|---|---|---|---|
| `Clinics` | numeric | 1–10 | Cluster identifier: the health facility. |
| `Year` | numeric | 2014–2016 | Calendar year of visit. |
| `Month` | numeric | 1–12 | Calendar month of visit. |
| `Study Month` | string | — | Month index within the study. `[INFERRED]` |
| `Is Intervention Step` | string | — | Whether the visit occurred during the clinic's post-crossover (intervention) period. `[INFERRED]` |
| `Steps` | numeric | 1–11 | Stepped-wedge time period (11 steps). |
| `Is First Visit` | binary | No/Yes | First antenatal visit of the pregnancy. `[INFERRED]` |
| `Screening: High Blood Pressure` | binary | No/Yes | Screening performed at this visit. |
| `Screening: Proteinuria` | binary | No/Yes | Screening performed at this visit. |
| `Screening: Syphilis` | binary | No/Yes | Screening performed at this visit. |
| `Screening: HIV` | binary | No/Yes | Screening performed at this visit. |
| `Screening: Anemia` | binary | No/Yes | Screening performed at this visit. |
| `Treatment: Syphilis` | binary | No/Yes | Treatment given at this visit. `[INFERRED]` |
| `Treatment: HIV` | binary | No/Yes | Treatment given at this visit. `[INFERRED]` |
| `Treatment: Worms` | binary | No/Yes | Treatment given at this visit. `[INFERRED]` |
| `Treatment: Malaria` | binary | No/Yes | Treatment given at this visit. `[INFERRED]` |

Note for beta's export schema: the real table carries the *observed* wedge
(`Is Intervention Step`) but not, as a column, the *assigned* crossover
step per clinic. Beta's simulated exports must carry both assigned and
observed — the gap between them is where allocation lies live — plus
manifest keys (L11) and, for lie-injected runs, the confession-ledger join
keys.

---

## 4. What CCd receives, and what it does not

**Received (read-only reference, cloned beside — never inside — beta's
repo):**
- The Shiny app code (`ui.R`, `server.R`, `app.R`) — explorer prototype;
  pattern to imitate or reuse directly.
- The protocol PDFs (`ANCMozambiqueProtocol.pdf`,
  `SW Datasets Protocol 08Jan24 final.pdf`) — design input for the
  stepped-wedge capability (MAP.md §4, step 3).
- This codebook.

**Not received:** the rows. On cloning the reference, delete all three
copies of `appData.rds` locally (`find . -name "appData.rds" -delete`).
The seal makes deletion safe — the canonical copy lives in the public
repo and can always be re-fetched and verified at Gate G3. Physical
absence beats trusted restraint.

---

## 5. Exposure log (the audit trail of who has seen what)

| Date | Who | What was exposed | What was not |
|---|---|---|---|
| 2026-07-03 | Claude (conversation) | Schema, types, category levels, dimensions, file hashes; one screenshot of published-level pivot aggregates (proteinuria screening by clinic × step, first visits). | Microdata rows; distributions beyond the screenshot; any other outcome's texture. |
| 2026-07-03 | CCd | Nothing. | Everything. |

Every future exposure — including the Gate G3 events themselves — gets a
row here, before it happens where possible, immediately after where not.
An instrument that audits exposure must log its own.

---

*Sealed under CONSTITUTION-LD.md v0.5, L10–L11. The student never sees the
paper; the paper's fingerprint is on file.*
