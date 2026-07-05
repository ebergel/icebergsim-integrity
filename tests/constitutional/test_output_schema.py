"""Constitutional test — CONSTITUTION-LD.md L1 (two regimes, always labeled)
and L2 (no verdicts: mandatory payload on every anomaly output).

Red blocks merge.
"""
import dataclasses

import pytest

from icebergsim_integrity.schema import (
    AnomalyResult,
    FalseAlarmContext,
    ReferenceDistribution,
    Regime,
    Statistic,
)


def _minimal_result(**overrides):
    kwargs = dict(
        regime=Regime.VERIFICATION,
        statistic=Statistic(name="example_count", value=0),
        reference=ReferenceDistribution(name="degenerate-at-zero"),
        false_alarm=FalseAlarmContext(exact_by_construction=True),
    )
    kwargs.update(overrides)
    return AnomalyResult(**kwargs)


# --- L1: exactly two regimes, no third value, no absence ---

def test_regime_has_exactly_two_values():
    assert {r.value for r in Regime} == {"verification", "forensics"}
    assert len(Regime) == 2


def test_regime_rejects_third_value():
    with pytest.raises(ValueError):
        Regime("plausible")


@pytest.mark.parametrize("bad", [None, "verification", "forensics", 0, True])
def test_regime_field_accepts_only_regime_members(bad):
    # Raw strings are rejected too: the label must be the constrained type
    # itself, so no call site can smuggle in a third value.
    with pytest.raises(TypeError):
        _minimal_result(regime=bad)


def test_regime_cannot_be_absent():
    with pytest.raises(TypeError):
        AnomalyResult(  # type: ignore[call-arg]
            statistic=Statistic(name="example_count", value=0),
            reference=ReferenceDistribution(name="degenerate-at-zero"),
            false_alarm=FalseAlarmContext(exact_by_construction=True),
        )


# --- L2: mandatory payload — statistic, reference, false-alarm context ---

@pytest.mark.parametrize("field", ["statistic", "reference", "false_alarm"])
def test_payload_pieces_are_mandatory_and_typed(field):
    with pytest.raises(TypeError):
        _minimal_result(**{field: None})


def test_mandatory_payload_fields_exist():
    names = {f.name for f in dataclasses.fields(AnomalyResult)}
    assert {"regime", "statistic", "reference", "false_alarm"} <= names


# --- L2, structurally: nothing verdict-shaped ---

def test_no_boolean_fields_on_results():
    """A verdict most naturally hides in a bool. Results carry none."""
    for cls in (AnomalyResult, Statistic):
        for f in dataclasses.fields(cls):
            assert "bool" not in str(f.type), f"{cls.__name__}.{f.name} is boolean"


def test_statistic_value_rejects_bool():
    with pytest.raises(TypeError):
        Statistic(name="example", value=True)


# --- L2, at runtime: the string channels cannot carry judgment either ---
# (These constructions all passed before the Session Zero adversarial
# review; each one below is a pinned evasion.)

def test_statistic_name_rejects_verdict_vocabulary():
    with pytest.raises(ValueError):
        Statistic(name="fraud_probability", value=0.97)


def test_reference_name_rejects_verdict_vocabulary():
    with pytest.raises(ValueError):
        ReferenceDistribution(name="null_of_no_tampering")


def test_detail_keys_reject_verdict_vocabulary():
    with pytest.raises(ValueError):
        _minimal_result(details=(("fabrication_score", 1),))


def test_detail_string_values_reject_verdict_vocabulary():
    with pytest.raises(ValueError):
        _minimal_result(details=(("assessment", "likely fabricated"),))


def test_detail_values_reject_bool():
    with pytest.raises(TypeError):
        _minimal_result(details=(("seed_is_authentic", True),))


def test_detail_keys_cannot_shadow_schema_fields():
    with pytest.raises(ValueError):
        _minimal_result(details=(("regime", "screening"),))


@pytest.mark.parametrize(
    "bad",
    [
        ((("note",),),),               # not a pair
        ((("note", 1, 2),),),          # too long
        (((1, "x"),),),                # non-string key
        ((("note", object()),),),      # non-scalar value
        ([("note", 1)],),              # list, not tuple
    ],
)
def test_malformed_details_are_rejected(bad):
    with pytest.raises((TypeError, ValueError)):
        _minimal_result(details=bad[0])


def test_reference_parameters_validated_like_details():
    with pytest.raises(TypeError):
        ReferenceDistribution(
            name="permutation", parameters=(("data_ok", True),)
        )
    with pytest.raises(ValueError):
        ReferenceDistribution(
            name="permutation", parameters=(("regime", "third"),)
        )


# --- Frozen pure-core types (L12) ---

def test_results_are_frozen():
    result = _minimal_result()
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.regime = Regime.FORENSICS  # type: ignore[misc]


# --- L4 hook: false-alarm context states how far calibration reaches ---

def test_calibrated_context_requires_replicates_and_reach():
    with pytest.raises(ValueError):
        FalseAlarmContext(exact_by_construction=False)
    with pytest.raises(ValueError):
        FalseAlarmContext(
            exact_by_construction=False, null_replicates=0, reach=0.05
        )
    with pytest.raises(ValueError):
        FalseAlarmContext(
            exact_by_construction=False, null_replicates=1000, reach=0.0
        )
    FalseAlarmContext(exact_by_construction=False, null_replicates=1000, reach=0.01)


def test_exact_context_carries_no_simulated_calibration():
    with pytest.raises(ValueError):
        FalseAlarmContext(
            exact_by_construction=True, null_replicates=1000, reach=0.01
        )
