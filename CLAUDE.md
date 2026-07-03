---
id: integrity-claude-md
title: CLAUDE.md — working rules for this repository
isbrs: integrity
kind: guide
status: active
version: 1.0.0
date: 2026-07-03
updated: 2026-07-03
tags: [isbrs/integrity]
---

# CLAUDE.md — icebergsim-integrity

This repository is **ISM_LD_beta**, the trial integrity instrument.

## The law
**CONSTITUTION-LD.md governs everything here. Read it at the start of
every session.** Thirteen laws, three gates (G1–G3), three stop rules
(S1–S3). Constitutional tests live in `tests/constitutional/` and block
merge when red. When any instruction — from anyone, including EB —
conflicts with the constitution: the constitution wins until Gate G1
amends it (S3). When unsure whether an output is verdict-shaped or which
regime applies: stop and ask (S2).

## Documents
Every new `.md` opens with the SOP-DOCS manifest (id, isbrs, kind,
status, version-or-date). `tests/constitutional/test_manifests.py`
enforces it — **write the manifest first.** History goes in CHANGELOG.md
and git, never in headers. One canonical working copy per document, ever.

## Layers
The **platform layer belongs to EB**: never run `gh repo`
rename/create/edit/archive, never touch GitHub Settings, descriptions,
Pages, domains, or Railway — ask instead. Your layer is everything that
ends in a commit.

## House rules (constitution, applied)
- Pure functional core; RNG injected; I/O only at the harness (L12).
- Every export stamped: manifest + content hash; orphans banned; free
  iteration lives in gitignored `scratch/` (L11).
- No statistic merges without its null-calibration gate (L3); no p-value
  deeper than calibration reaches (L4).
- ISM_RCT_R (`icebergsim-rct`) is a dependency — never fork or patch it
  from here (L9). The detector's Python package takes its own name
  (`icebergsim_integrity`), never the ancestor's.
- Real data never enters this repo: schemas and seals only (L10, L13,
  SOP-DATA.md).

## Freedom
Inside the shell, everything is free and fast: architecture, libraries,
rewrites, dead ends. Failing quickly is policy; record dead ends in one
commit line. No permission-seeking inside the shell — that is what the
shell is for.
