import pytest

from unitconv import UnitError, convert, set_rates, supported_units


@pytest.mark.parametrize("v,a,b,expected", [
    (1, "km", "m", 1000),
    (1, "mi", "km", 1.609344),
    (1, "nmi", "km", 1.852),
    (2, "кг", "lb", 4.409245),
    (1, "st", "kg", 6.35029318),
    (1, "h", "min", 60),
    (1, "yr", "d", 365.25),
    (1, "gib", "mib", 1024),
    (8, "bit", "b", 1),
    (1, "gb", "mb", 1000),
    (36, "km/h", "m/s", 10),
    (1, "ha", "m2", 10000),
    (10, "сотка", "m2", 1000),
    (1, "gal", "l", 3.785411784),
    (1, "atm", "pa", 101325),
    (1, "bar", "kpa", 100),
    (14.5038, "psi", "bar", 1.0),
    (1, "kwh", "kj", 3600),
    (1, "kcal", "cal", 1000),
    (1, "hp", "kw", 0.745699872),
    (180, "deg", "rad", 3.141592653589793),
    (1, "turn", "deg", 360),
    (60, "rpm", "hz", 1),
    (1, "kgf", "n", 9.80665),
])
def test_conversions(v, a, b, expected):
    assert convert(v, a, b) == pytest.approx(expected, rel=1e-4)


@pytest.mark.parametrize("v,a,b,expected", [
    (0, "c", "f", 32), (100, "c", "f", 212),
    (0, "c", "k", 273.15), (32, "f", "c", 0), (-40, "c", "f", -40),
    (5, "l/100km", "km/l", 20),
    (10, "l/100km", "l/100km", 10),
    (1, "km/l", "mpg", 2.352146),
])
def test_nonlinear(v, a, b, expected):
    assert convert(v, a, b) == pytest.approx(expected, rel=1e-4)


def test_fuel_zero():
    with pytest.raises(UnitError):
        convert(0, "l/100km", "mpg")


def test_incompatible():
    with pytest.raises(UnitError):
        convert(1, "km", "kg")
    with pytest.raises(UnitError):
        convert(1, "c", "km")


def test_unknown():
    with pytest.raises(UnitError):
        convert(1, "foo", "bar")


def test_currency():
    set_rates({"USD": 1, "EUR": 0.5, "TJS": 10})
    assert convert(10, "usd", "eur") == pytest.approx(5)
    assert convert(10, "eur", "tjs") == pytest.approx(200)


def test_unknown_currency():
    set_rates({"USD": 1})
    with pytest.raises(UnitError):
        convert(1, "usd", "xyz")


def test_supported_units():
    units = supported_units()
    assert "km" in units["length"]
    assert "c" in units["temperature"]
    assert "pressure" in units and "energy" in units
