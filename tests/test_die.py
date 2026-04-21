from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from uuid import UUID, uuid4

import pytest


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "die_and_die_again" / "core" / "die.py"
)
SPEC = spec_from_file_location("die_module", MODULE_PATH)
die_module = module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(die_module)

Die = die_module.Die
DieType = die_module.DieType


@pytest.mark.parametrize(
    ("sides", "expected"),
    [
        (3, DieType.D3),
        (4, DieType.D4),
        (6, DieType.D6),
        (8, DieType.D8),
        (10, DieType.D10),
        (12, DieType.D12),
        (20, DieType.D20),
    ],
)
def test_die_type_from_sides_returns_matching_enum(sides, expected):
    assert DieType.from_sides(sides) is expected


def test_die_type_from_sides_rejects_too_few_sides():
    with pytest.raises(DieType.InvalidSides, match=r"Too few sides\(2\)"):
        DieType.from_sides(2)


def test_die_type_from_sides_rejects_unknown_side_count():
    with pytest.raises(DieType.InvalidSides, match=r"invalid #sides\(5\)"):
        DieType.from_sides(5)


def test_die_type_string_and_sides_properties():
    assert str(DieType.D12) == "D12"
    assert DieType.D12.sides == 12


def test_die_defaults_to_fair_d6():
    die = Die()

    assert isinstance(die.unique_id, UUID)
    assert die.sides == 6
    assert die.values == [1, 2, 3, 4, 5, 6]
    assert die.weights == pytest.approx([1 / 6] * 6)
    assert die.roll_count == 0
    assert str(die) == "D6"


def test_die_rejects_too_few_sides():
    with pytest.raises(ValueError, match="Min sides is 2, got 1"):
        Die(1)


def test_die_rejects_mismatched_weights():
    with pytest.raises(ValueError, match="Weight count mismatch. expected 6 got 2"):
        Die(6, weights=[0.5, 0.5])


def test_die_uses_given_unique_id():
    unique_id = uuid4()

    die = Die(unique_id=unique_id)

    assert die.unique_id == unique_id


def test_die_generates_unique_ids_per_instance():
    die_a = Die()
    die_b = Die()

    assert die_a.unique_id != die_b.unique_id


def test_change_weighting_updates_selected_value_only():
    die = Die(4)

    die.change_weighting(3, 50)

    assert die.weights == pytest.approx([0.25, 0.25, 0.375, 0.25])


def test_change_weighting_rejects_invalid_value():
    die = Die(4)

    with pytest.raises(ValueError, match=r"Value must be in \[1, 2, 3, 4\], got 5"):
        die.change_weighting(5, 10)


def test_normalize_weights_rescales_total_to_one():
    die = Die(4)
    die.change_weighting(2, 100)

    die.normalize_weights()

    assert sum(die.weights) == pytest.approx(1.0)
    assert die.weights == pytest.approx([0.2, 0.4, 0.2, 0.2])


def test_reset_weights_restores_fair_distribution():
    die = Die(4)
    die.change_weighting(2, 100)
    die.normalize_weights()

    die.reset_weights()

    assert die.weights == pytest.approx([0.25, 0.25, 0.25, 0.25])


def test_weighting_str_formats_values_and_weights():
    die = Die(3)

    assert die.weighting_str() == "[ 1:0.33,  2:0.33,  3:0.33]"


def test_roll_uses_random_choices_result(monkeypatch):
    die = Die(6)

    def fake_choices(values, weights, k):
        assert values == die.values
        assert weights == die.weights
        assert k == 1
        return [4]

    monkeypatch.setattr(die_module, "choices", fake_choices)

    assert die.roll() == 4
    assert die.roll_count == 1


def test_roll_count_accumulates_across_multiple_rolls(monkeypatch):
    die = Die(6)
    results = iter([3, 5, 2])

    monkeypatch.setattr(
        die_module, "choices", lambda values, weights, k: [next(results)]
    )

    assert die.multiple_roll(3) == [3, 5, 2]
    assert die.roll_count == 3


def test_multiple_roll_returns_requested_number_of_results(monkeypatch):
    die = Die(6)
    results = iter([2, 5, 1])

    monkeypatch.setattr(die, "roll", lambda: next(results))

    assert die.multiple_roll(3) == [2, 5, 1]


def test_multiple_roll_rejects_non_positive_count():
    die = Die(6)

    with pytest.raises(ValueError, match="Min rolls is 1, got 0"):
        die.multiple_roll(0)
