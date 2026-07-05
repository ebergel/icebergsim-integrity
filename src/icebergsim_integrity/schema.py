"""Anomaly-output schema — the mandatory shape of every result (L1, L2, L12).

Every result the instrument emits is an :class:`AnomalyResult`: a statistic,
its reference distribution, its calibrated false-alarm context, and its
regime label. Nothing here is verdict-shaped, and nothing here is optional.
A flag is a reason to look, never a finding.

Frozen dataclasses over plain data; no I/O, no hidden state (L12).
Constitutional tests: tests/constitutional/test_output_schema.py and
tests/constitutional/test_forbidden_vocabulary.py.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass


class Regime(enum.StrEnum):
    """The two regimes of L1. Exactly two; a third value is unconstitutional."""

    VERIFICATION = "verification"
    FORENSICS = "forensics"


@dataclass(frozen=True, slots=True)
class Statistic:
    """A named statistic value. Verification statistics are integer-exact."""

    name: str
    value: int | float

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("statistic must be named")
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
            raise TypeError("statistic value must be int or float, never bool")


@dataclass(frozen=True, slots=True)
class ReferenceDistribution:
    """What the statistic is compared against under the stated null.

    ``parameters`` is a flat tuple of (name, value) pairs so the whole
    object stays hashable and frozen.
    """

    name: str
    parameters: tuple[tuple[str, int | float | str], ...] = ()

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("reference distribution must be named")


@dataclass(frozen=True, slots=True)
class FalseAlarmContext:
    """How far calibration reaches for this statistic (L3, L4).

    Either the statistic is exact by construction, or it carries the size
    of its null calibration (``null_replicates``) and the smallest tail
    probability that calibration can support (``reach``). The reporting
    layer must refuse any p-value below ``reach`` (L4).
    """

    exact_by_construction: bool
    null_replicates: int | None = None
    reach: float | None = None

    def __post_init__(self) -> None:
        if self.exact_by_construction:
            if self.null_replicates is not None or self.reach is not None:
                raise ValueError(
                    "exact-by-construction carries no simulated calibration"
                )
            return
        if not isinstance(self.null_replicates, int) or self.null_replicates <= 0:
            raise ValueError("calibrated context requires positive null_replicates")
        if not isinstance(self.reach, float) or not 0.0 < self.reach <= 1.0:
            raise ValueError("calibrated context requires reach in (0, 1]")


@dataclass(frozen=True, slots=True)
class AnomalyResult:
    """The mandatory payload of every anomaly output (L1, L2).

    ``details`` carries structured, statistic-specific context as flat
    (name, value) pairs — never labels, never judgments.
    """

    regime: Regime
    statistic: Statistic
    reference: ReferenceDistribution
    false_alarm: FalseAlarmContext
    details: tuple[tuple[str, int | float | str], ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.regime, Regime):
            raise TypeError("regime must be a Regime member — no absence, no third value")
        if not isinstance(self.statistic, Statistic):
            raise TypeError("statistic is mandatory")
        if not isinstance(self.reference, ReferenceDistribution):
            raise TypeError("reference distribution is mandatory")
        if not isinstance(self.false_alarm, FalseAlarmContext):
            raise TypeError("false-alarm context is mandatory")
