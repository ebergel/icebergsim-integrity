"""Exhaustive tests for the seed-verification kernel (L5).

The kernel is the floor: these tests pin its behavior bit-exactly (golden
vectors), exercise every declared failure mode, and enforce the
no-floating-point rule structurally on the module source.
"""
import ast
import inspect
from pathlib import Path

import pytest

import icebergsim_integrity.seedkernel as seedkernel_module
from icebergsim_integrity.schema import Regime
from icebergsim_integrity.seedkernel import (
    AllocationSpec,
    _fisher_yates,
    _randbelow,
    regenerate_allocation,
    verify_allocation,
)

COMPLETE = AllocationSpec(algorithm="complete", seed=1, arm_counts=(3, 3))
BLOCKED = AllocationSpec(
    algorithm="permuted_block", seed=42, block_ratio=(1, 1), n_participants=8
)


# --- Golden pins: bit-exact regeneration, frozen 2026-07-05 -----------------
# These guard against PCG64 raw-stream drift AND accidental kernel edits.
# If one of these moves, the floor moved: stop (L5, G1 once accepted).

GOLDEN = [
    (COMPLETE, (0, 0, 1, 1, 1, 0)),
    (
        AllocationSpec(algorithm="complete", seed=20260705, arm_counts=(5, 5)),
        (1, 0, 1, 1, 1, 0, 0, 0, 0, 1),
    ),
    (BLOCKED, (1, 0, 0, 1, 1, 0, 0, 1)),
    (
        AllocationSpec(
            algorithm="permuted_block", seed=7, block_ratio=(2, 1), n_participants=10
        ),
        (1, 0, 0, 0, 0, 1, 1, 0, 0, 0),
    ),
]


@pytest.mark.parametrize("spec,expected", GOLDEN)
def test_golden_regeneration(spec, expected):
    assert regenerate_allocation(spec) == expected


# --- Purity and determinism -------------------------------------------------

@pytest.mark.parametrize("spec", [COMPLETE, BLOCKED])
def test_regeneration_is_deterministic(spec):
    first = regenerate_allocation(spec)
    assert all(regenerate_allocation(spec) == first for _ in range(5))


def test_regeneration_returns_python_ints():
    for value in regenerate_allocation(COMPLETE):
        assert type(value) is int


def test_spec_is_frozen():
    import dataclasses

    with pytest.raises(dataclasses.FrozenInstanceError):
        COMPLETE.seed = 2  # type: ignore[misc]


# --- Round trip: what the seed produces, the seed verifies -------------------

SWEEP = [
    AllocationSpec(algorithm="complete", seed=s, arm_counts=counts)
    for s in range(10)
    for counts in [(4, 4), (5, 3), (2, 2, 2), (1, 7), (0, 3)]
] + [
    AllocationSpec(
        algorithm="permuted_block", seed=s, block_ratio=ratio, n_participants=n
    )
    for s in range(10)
    for ratio, n in [((1, 1), 8), ((1, 1), 7), ((2, 1), 12), ((2, 1), 10),
                     ((1, 1, 1), 9), ((3, 2), 11), ((1, 1), 1)]
]


@pytest.mark.parametrize("spec", SWEEP)
def test_round_trip_zero_discrepancies(spec):
    result = verify_allocation(spec, regenerate_allocation(spec))
    assert result.statistic.value == 0
    assert result.regime is Regime.VERIFICATION


# --- Design invariants across seeds ------------------------------------------

@pytest.mark.parametrize("seed", range(25))
def test_complete_preserves_arm_counts_exactly(seed):
    spec = AllocationSpec(algorithm="complete", seed=seed, arm_counts=(7, 5, 3))
    allocation = regenerate_allocation(spec)
    assert len(allocation) == 15
    assert tuple(allocation.count(code) for code in range(3)) == (7, 5, 3)


@pytest.mark.parametrize("seed", range(25))
def test_permuted_block_composition_exact_per_block(seed):
    spec = AllocationSpec(
        algorithm="permuted_block", seed=seed, block_ratio=(2, 1), n_participants=11
    )
    allocation = regenerate_allocation(spec)
    assert len(allocation) == 11
    for start in range(0, 9, 3):  # full blocks
        block = allocation[start : start + 3]
        assert sorted(block) == [0, 0, 1]
    tail = allocation[9:]  # truncated final block: never exceeds the ratio
    assert tail.count(0) <= 2 and tail.count(1) <= 1


# --- The verification result: shape and evidence ------------------------------

def test_result_payload_shape():
    result = verify_allocation(COMPLETE, regenerate_allocation(COMPLETE))
    assert result.statistic.name == "allocation_discrepancy_count"
    assert result.reference.name == "degenerate-at-zero"
    assert result.false_alarm.exact_by_construction
    details = dict(result.details)
    assert details["allocation_algorithm"] == "complete"
    assert details["committed_seed"] == 1
    assert details["rng_algorithm"] == "pcg64-raw"
    assert details["expected_length"] == 6
    assert details["reported_length"] == 6
    assert "first_discrepancy_index" not in details


def test_single_altered_position():
    reported = list(regenerate_allocation(COMPLETE))
    reported[3] = 1 - reported[3]
    result = verify_allocation(COMPLETE, reported)
    assert result.statistic.value == 1
    assert dict(result.details)["first_discrepancy_index"] == 3


def test_transposed_pair_counts_two():
    reported = list(regenerate_allocation(COMPLETE))
    i = reported.index(0)
    j = reported.index(1)
    reported[i], reported[j] = reported[j], reported[i]
    result = verify_allocation(COMPLETE, reported)
    assert result.statistic.value == 2
    assert dict(result.details)["first_discrepancy_index"] == min(i, j)


def test_every_position_altered():
    expected = regenerate_allocation(COMPLETE)
    reported = [1 - v for v in expected]
    assert verify_allocation(COMPLETE, reported).statistic.value == len(expected)


def test_truncated_report_counts_missing_positions():
    expected = regenerate_allocation(COMPLETE)
    result = verify_allocation(COMPLETE, expected[:4])
    assert result.statistic.value == 2
    details = dict(result.details)
    assert details["reported_length"] == 4
    assert details["first_discrepancy_index"] == 4


def test_padded_report_counts_extra_positions():
    expected = regenerate_allocation(COMPLETE)
    result = verify_allocation(COMPLETE, list(expected) + [0, 1, 0])
    assert result.statistic.value == 3
    assert dict(result.details)["first_discrepancy_index"] == len(expected)


def test_wrong_seed_does_not_regenerate():
    other = AllocationSpec(algorithm="complete", seed=2, arm_counts=(50, 50))
    mine = AllocationSpec(algorithm="complete", seed=1, arm_counts=(50, 50))
    reported = regenerate_allocation(other)
    assert verify_allocation(mine, reported).statistic.value > 0


def test_wrong_block_ratio_does_not_regenerate():
    declared = AllocationSpec(
        algorithm="permuted_block", seed=5, block_ratio=(1, 1), n_participants=60
    )
    actual = AllocationSpec(
        algorithm="permuted_block", seed=5, block_ratio=(2, 1), n_participants=60
    )
    reported = regenerate_allocation(actual)
    assert verify_allocation(declared, reported).statistic.value > 0


# --- Strict integer discipline ------------------------------------------------

@pytest.mark.parametrize("bad", [1.0, True, "1", None])
def test_reported_entries_must_be_python_ints(bad):
    reported = list(regenerate_allocation(COMPLETE))
    reported[0] = bad
    with pytest.raises(TypeError):
        verify_allocation(COMPLETE, reported)


def test_numpy_integers_are_rejected():
    import numpy as np

    reported = list(regenerate_allocation(COMPLETE))
    reported[0] = np.int64(reported[0])
    with pytest.raises(TypeError):
        verify_allocation(COMPLETE, reported)


@pytest.mark.parametrize("bad_seed", [1.0, True, "1", None])
def test_seed_must_be_python_int(bad_seed):
    with pytest.raises(TypeError):
        AllocationSpec(algorithm="complete", seed=bad_seed, arm_counts=(3, 3))


# --- Spec validation: every declared failure mode ------------------------------

@pytest.mark.parametrize(
    "kwargs",
    [
        dict(algorithm="complete", seed=-1, arm_counts=(3, 3)),
        dict(algorithm="complete", seed=1),
        dict(algorithm="complete", seed=1, arm_counts=(6,)),
        dict(algorithm="complete", seed=1, arm_counts=(-1, 4)),
        dict(algorithm="complete", seed=1, arm_counts=(0, 0)),
        dict(algorithm="complete", seed=1, arm_counts=(3, 3), n_participants=6),
        dict(algorithm="complete", seed=1, arm_counts=(3, 3), block_ratio=(1, 1)),
        dict(algorithm="permuted_block", seed=1, block_ratio=(1, 1)),
        dict(algorithm="permuted_block", seed=1, n_participants=8),
        dict(algorithm="permuted_block", seed=1, block_ratio=(1,), n_participants=8),
        dict(
            algorithm="permuted_block", seed=1, block_ratio=(0, 1), n_participants=8
        ),
        dict(
            algorithm="permuted_block", seed=1, block_ratio=(1, 1), n_participants=0
        ),
        dict(
            algorithm="permuted_block",
            seed=1,
            block_ratio=(1, 1),
            n_participants=8,
            arm_counts=(4, 4),
        ),
        dict(algorithm="urn", seed=1, arm_counts=(3, 3)),
    ],
)
def test_invalid_specs_are_rejected(kwargs):
    with pytest.raises((ValueError, TypeError)):
        AllocationSpec(**kwargs)


# --- The raw-stream primitives, pinned by hand ----------------------------------

def test_randbelow_rejection_branch():
    # bound 10: the largest multiple of 10 below 2**64 is 2**64 - 6, so
    # 2**64 - 1 must be rejected and the next draw used.
    draws = iter([2**64 - 1, 5])
    assert _randbelow(lambda: next(draws), 10) == 5


def test_randbelow_uses_modulo_reduction():
    draws = iter([23])
    assert _randbelow(lambda: next(draws), 10) == 3


def test_fisher_yates_known_draws():
    # n=4: i=3 swaps with j=1 -> [0,3,2,1]; i=2 swaps with j=0 -> [2,3,0,1];
    # i=1 swaps with j=1 (no-op).
    sequence = [0, 1, 2, 3]
    draws = iter([1, 0, 1])
    _fisher_yates(sequence, lambda: next(draws))
    assert sequence == [2, 3, 0, 1]


# --- No floating point in the kernel, enforced structurally ----------------------

def test_kernel_source_contains_no_floating_point():
    source = Path(inspect.getsourcefile(seedkernel_module)).read_text(
        encoding="utf-8"
    )
    tree = ast.parse(source)
    offences = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            offences.append(f"float literal {node.value!r} at line {node.lineno}")
        if isinstance(node, ast.Name) and node.id == "float":
            offences.append(f"'float' identifier at line {node.lineno}")
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            offences.append(f"true division at line {node.lineno}")
    assert not offences, "floating point in the kernel:\n" + "\n".join(offences)
