---
id: integrity-readme
title: README — IcebergSim Integrity
isbrs: integrity
kind: readme
status: active
date: 2026-07-03
updated: 2026-07-03
tags: [isbrs/integrity]
---

# IcebergSim Integrity

A trial integrity instrument, **in construction**: tools that examine a
randomized trial's data and weigh the evidence that it was — or was not —
produced the way its authors declare. It flags anomalies and attaches the
numbers; judgment stays with humans. It never delivers verdicts.

**Governed by [CONSTITUTION-LD.md](CONSTITUTION-LD.md)** — thirteen laws,
three human gates, three stop rules, enforced in CI
([`tests/constitutional/`](tests/constitutional/)). Real-world test data
is sealed by cryptographic hash before development may look at it
([`seals/`](seals/), [SOP-DATA.md](SOP-DATA.md)).

**The public promise:** no claim about what this instrument can detect
will be published before its false-alarm rate exists. Its subdomain
(`integrity.icebergsim.com`) stays empty until the first calibrated
number does.

Part of the [IcebergSim program](https://icebergsim.com) · program
handle: **ISM_LD_beta** ·
[program map](https://github.com/ebergel/icebergsim/blob/main/MAP.md)
