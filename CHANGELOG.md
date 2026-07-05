---
id: changelog-integrity
title: Changelog — icebergsim-integrity
isbrs: integrity
kind: changelog
status: active
date: 2026-07-03
updated: 2026-07-03
tags: [isbrs/integrity]
---

# CHANGELOG — icebergsim-integrity

Newest first. One line per version per document (SOP-DOCS.md §4).

## 2026-07-05 — session zero (B5)
- seed kernel **0.1.0** — **ACCEPTED by EB**; the freeze begins (L5).
  From now on any change to seedkernel.py crosses Gate G1. Enforced
  executably: tests/constitutional/test_seed_kernel_freeze.py pins the
  module's content hash
  (`b01a1fcf533b13a5b6e79e68f4ddc14d37adf0cad735d9ed1cc62d0b8cd2e61d`).
- anomaly-output schema **0.2.0** — hardened after the in-session
  adversarial review (21 agents, 5 lenses; 12 findings confirmed, 4
  refuted; kernel math lens: zero findings): banned vocabulary moved to
  a shared module enforced at runtime on every string channel (statistic
  names, reference names, detail/parameter keys and values) and by the
  constitutional scan over identifiers, non-docstring string constants
  and module filenames; details/parameters shape-validated; reserved
  keys cannot shadow schema fields; ban list pinned in both directions.
- seed kernel hardening (still 0.1.0, pre-acceptance) — out-of-range
  reported arm codes now raise instead of inflating the count; golden
  pins widened (n=20, three arms, block ratio 2:2:1, 128-bit seed);
  empty report, truncation+alteration additivity, spec-entry type
  strictness and kernel_version manifest all pinned. CI: interpreter
  pinned via .python-version.
- icebergsim-integrity **0.1.0** — package born: pyproject, src layout,
  pytest wired; icebergsim-rct consumed as a git dependency, pinned in
  uv.lock at `5d439b2a` (L9).
- seed kernel **0.1.0** — **PENDING EB ACCEPTANCE** (L5: freeze begins at
  his yes). Regenerates allocation from the committed seed over PCG64's
  raw stream with the kernel's own integer algorithms (rejection-sampled
  bounds, Fisher–Yates); complete + permuted-block; integer-exact
  comparison; result = discrepancy count, regime verification, exact by
  construction. No floating point in the module, enforced by test.
  Golden vectors pinned. tests/kernel/: exhaustive suite.
- anomaly-output schema **0.1.0** — frozen pure-core types (L1, L2, L12):
  Regime with exactly two values; mandatory statistic + reference
  distribution + false-alarm context; no booleans on results; verdict
  vocabulary banned from output identifiers. Constitutional tests:
  test_output_schema.py, test_forbidden_vocabulary.py.
- CI live — `.github/workflows/constitutional.yml`: constitutional tests
  on every push and PR (plus ruff, mypy). Marking the job *required* is
  branch protection — EB's platform layer, flagged in the workflow header.
- integrity-readme **1.0.0** — manifest gains `version`: the constitutional
  suite's first real run flagged it (readme is a versioned kind).
- spike-b5-umbilical — umbilical spike verdict **(c)**: icebergsim-rct
  has no row-level form, internal or exposed (exact multinomial collapse,
  SPEC §6.3); inventory for B6 recorded in sessions/SESSION-0-SPIKE-B5.md.

## 2026-07-04 — signed
- constitution-ld **1.0.0** — SIGNED by EB. Table-read passed by a
  fresh reader on 2026-07-04; the law reads as written.
- constitution-ld 0.9.1 — L5 clarified (creation free; freeze at EB's
  acceptance) — found by the table-read.
## 2026-07-03 — the founding day
- sop-docs **0.2.1** — clarified: the root `#isbrs` is implicit via tag
  nesting; never written explicitly; the `isbrs:` field is the canonical
  membership signal.
- sop-docs **0.2.0** — +§6 Enforcement: constitutional test
  (test_manifests.py, id uniqueness), CLAUDE.md line, vault rails,
  Claude memory instruction.
- constitution-ld **0.8.0** — L11: documents are exports too (frontmatter
  manifests, SOP-DOCS); manifest retrofit; history migrated here.
- constitution-ld 0.7.0 — L11: gitignored `scratch/` exempted; decisions
  only from stamped tables.
- constitution-ld 0.6.0 — +L13 exposure is irreversible; sealing
  generalized to SOP-DATA.md.
- constitution-ld 0.5.0 — L10: real data outside the repo; the exam stays
  blind.
- constitution-ld 0.4.0 — L11: content hash in manifests; exports
  tamper-evident.
- constitution-ld 0.3.0 — L11: harness-only exports; provenance mandatory;
  orphans banned.
- constitution-ld 0.2.0 — +L11 glass box; +L12 pure core.
- constitution-ld 0.1.0 — born: ten laws, three gates, three stop rules,
  the freedoms, the north star.
- sop-data 0.1.1 — manifest retrofit. 0.1.0 — born: roles, one-way
  transitions, sealing procedure, registry (ANC-MOZ, EXAM, BLIND).
- seal-anc-moz — sealed: commit `d27ac54`, SHA-256 `c1452391…64aa`,
  218,277 × 16, role EXAM, status BLIND. Dated, never versioned.
