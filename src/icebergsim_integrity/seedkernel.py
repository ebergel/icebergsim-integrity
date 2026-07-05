"""Seed-verification kernel — the floor everything else stands on (L5).

Given a trial's pre-committed seed and its declared allocation procedure,
regenerate the allocation sequence and compare it INTEGER-EXACTLY to the
reported allocation. The allocation regenerates from the seed or it does
not: the result is a discrepancy count of zero or not, regime
``verification``, exact by construction. No verdict — a mismatch says the
reported allocation is not what the committed seed produces, and nothing
more.

Determinism contract (the full method manifest, L5/L6):

- Randomness source: the raw 64-bit output stream of NumPy's PCG64 bit
  generator seeded with the committed seed. NumPy guarantees BitGenerator
  stream stability across versions; ``Generator`` convenience methods
  carry no such guarantee, so this module never uses them.
- Bounded draws: unbiased rejection sampling on the raw stream — draw a
  64-bit integer, reject values at or above the largest multiple of the
  bound, reduce modulo the bound.
- Shuffles: Fisher–Yates, iterating i from n-1 down to 1, swapping i with
  a rejection-sampled j uniform on [0, i].
- ``complete``: one sequence holding each arm code ``a`` exactly
  ``arm_counts[a]`` times, in ascending code order, shuffled once.
- ``permuted_block``: blocks holding each arm code ``a`` exactly
  ``block_ratio[a]`` times in ascending code order, each block shuffled
  with the same stream in enrollment order, concatenated, truncated to
  ``n_participants`` (final partial block allowed).

Everything downstream of the raw draws is Python ``int``. No floating
point exists in this module, on the generation path or the comparison
path. Strictest standard in the codebase: exhaustive tests in
tests/kernel/, golden pins against stream drift.

L5 (as amended): this first version is free creation inside the shell;
the freeze begins when EB accepts it. From that moment, any change here
crosses Gate G1.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

import numpy as np

from icebergsim_integrity.schema import (
    AnomalyResult,
    FalseAlarmContext,
    ReferenceDistribution,
    Regime,
    Statistic,
)

KERNEL_VERSION = "0.1.0"
RNG_ALGORITHM = "pcg64-raw"

_UINT64_SPAN = 2**64


def _require_int(value: object, name: str) -> int:
    """Strict integer: bool is a subclass of int and is rejected."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be a Python int, got {type(value).__name__}")
    return value


@dataclass(frozen=True, slots=True)
class AllocationSpec:
    """A trial's declared allocation procedure plus its committed seed.

    ``complete``       — requires ``arm_counts``: participants per arm code.
    ``permuted_block`` — requires ``block_ratio`` (arm multiplicities per
                         block) and ``n_participants``.
    """

    algorithm: Literal["complete", "permuted_block"]
    seed: int
    arm_counts: tuple[int, ...] | None = None
    block_ratio: tuple[int, ...] | None = None
    n_participants: int | None = None

    def __post_init__(self) -> None:
        if _require_int(self.seed, "seed") < 0:
            raise ValueError("seed must be non-negative")
        if self.algorithm == "complete":
            if self.arm_counts is None:
                raise ValueError("complete allocation requires arm_counts")
            if self.block_ratio is not None or self.n_participants is not None:
                raise ValueError("complete allocation takes no block fields")
            counts = tuple(
                _require_int(c, "arm_counts entry") for c in self.arm_counts
            )
            if len(counts) < 2:
                raise ValueError("allocation needs at least two arms")
            if any(c < 0 for c in counts) or sum(counts) < 1:
                raise ValueError("arm_counts must be non-negative and sum to >= 1")
        elif self.algorithm == "permuted_block":
            if self.block_ratio is None or self.n_participants is None:
                raise ValueError(
                    "permuted_block requires block_ratio and n_participants"
                )
            if self.arm_counts is not None:
                raise ValueError("permuted_block takes no arm_counts")
            ratio = tuple(
                _require_int(m, "block_ratio entry") for m in self.block_ratio
            )
            if len(ratio) < 2:
                raise ValueError("allocation needs at least two arms")
            if any(m < 1 for m in ratio):
                raise ValueError("block_ratio multiplicities must be >= 1")
            if _require_int(self.n_participants, "n_participants") < 1:
                raise ValueError("n_participants must be >= 1")
        else:
            raise ValueError(f"unknown allocation algorithm: {self.algorithm!r}")


def _raw_stream(seed: int) -> Callable[[], int]:
    """The committed seed's raw 64-bit stream, one Python int per call."""
    bit_generator = np.random.PCG64(seed)
    raw = bit_generator.random_raw

    def draw() -> int:
        return int(raw())

    return draw


def _randbelow(draw: Callable[[], int], bound: int) -> int:
    """Uniform integer on [0, bound), unbiased by rejection sampling."""
    limit = (_UINT64_SPAN // bound) * bound
    while True:
        value = draw()
        if value < limit:
            return value % bound


def _fisher_yates(sequence: list[int], draw: Callable[[], int]) -> None:
    """In-place Fisher–Yates shuffle driven by the raw stream."""
    for i in range(len(sequence) - 1, 0, -1):
        j = _randbelow(draw, i + 1)
        sequence[i], sequence[j] = sequence[j], sequence[i]


def regenerate_allocation(spec: AllocationSpec) -> tuple[int, ...]:
    """Regenerate the allocation sequence a committed seed produces.

    Pure: same spec, same tuple, always. Arm codes are 0..k-1 in the order
    the spec declares them.
    """
    draw = _raw_stream(spec.seed)
    if spec.algorithm == "complete":
        assert spec.arm_counts is not None  # __post_init__ guarantees
        sequence = [
            code for code, count in enumerate(spec.arm_counts) for _ in range(count)
        ]
        _fisher_yates(sequence, draw)
        return tuple(sequence)
    assert spec.block_ratio is not None and spec.n_participants is not None
    pattern = [
        code for code, mult in enumerate(spec.block_ratio) for _ in range(mult)
    ]
    sequence = []
    while len(sequence) < spec.n_participants:
        block = list(pattern)
        _fisher_yates(block, draw)
        sequence.extend(block)
    return tuple(sequence[: spec.n_participants])


def verify_allocation(
    spec: AllocationSpec, reported: Sequence[int]
) -> AnomalyResult:
    """Compare a reported allocation against its committed seed, exactly.

    The comparison path is Python-int equality only. The statistic is the
    number of discrepant positions; length differences count position by
    position. Zero means the reported allocation regenerates from the
    committed seed; anything else means it does not.
    """
    checked = tuple(_require_int(v, "reported allocation entry") for v in reported)
    expected = regenerate_allocation(spec)
    overlap = min(len(expected), len(checked))
    discrepant = [i for i in range(overlap) if expected[i] != checked[i]]
    count = len(discrepant) + abs(len(expected) - len(checked))
    details: list[tuple[str, int | str]] = [
        ("allocation_algorithm", spec.algorithm),
        ("committed_seed", spec.seed),
        ("rng_algorithm", RNG_ALGORITHM),
        ("kernel_version", KERNEL_VERSION),
        ("expected_length", len(expected)),
        ("reported_length", len(checked)),
    ]
    if discrepant:
        details.append(("first_discrepancy_index", discrepant[0]))
    elif len(expected) != len(checked):
        details.append(("first_discrepancy_index", overlap))
    return AnomalyResult(
        regime=Regime.VERIFICATION,
        statistic=Statistic(name="allocation_discrepancy_count", value=count),
        reference=ReferenceDistribution(
            name="degenerate-at-zero",
            parameters=(("under", "committed seed and declared procedure"),),
        ),
        false_alarm=FalseAlarmContext(exact_by_construction=True),
        details=tuple(details),
    )
