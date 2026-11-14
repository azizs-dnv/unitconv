"""Integrity checks for the unit tables."""
import itertools

import pytest

from unitconv import convert
from unitconv.units import ALIASES, CATEGORIES, NONLINEAR, all_units, normalize


def test_unit_names_unique_across_categories():
    seen = {}
    for category, units in all_units().items():
        for unit in units:
            assert unit not in seen, f"{unit!r} appears in both {seen[unit]} and {category}"
            seen[unit] = category


def test_aliases_point_to_existing_units():
    known = {u for units in all_units().values() for u in units}
    for alias, target in ALIASES.items():
        assert target in known, f"alias {alias!r} -> unknown unit {target!r}"


def test_aliases_are_lowercase():
    for alias in ALIASES:
        assert alias == alias.lower(), alias


def test_normalize():
    assert normalize("  КМ ") == "km"
    assert normalize("Kilometer") == "km"


@pytest.mark.parametrize("category", list(CATEGORIES))
def test_linear_roundtrip(category):
    for a, b in itertools.permutations(CATEGORIES[category], 2):
        back = convert(convert(12.5, a, b), b, a)
        assert back == pytest.approx(12.5, rel=1e-9), (a, b)


@pytest.mark.parametrize("category", list(NONLINEAR))
def test_nonlinear_roundtrip(category):
    to_base, _ = NONLINEAR[category]
    for a, b in itertools.permutations(to_base, 2):
        back = convert(convert(12.5, a, b), b, a)
        assert back == pytest.approx(12.5, rel=1e-9), (a, b)
