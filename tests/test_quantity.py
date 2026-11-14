import pytest

from unitconv import Quantity, UnitError, set_rates


def test_add_sub():
    assert Quantity(5, "km") + Quantity(500, "m") == Quantity(5.5, "km")
    assert Quantity(1, "km") - Quantity(500, "m") == Quantity(0.5, "km")


def test_to_and_eq():
    assert Quantity(1, "km").to("m") == Quantity(1000, "m")
    assert Quantity(1, "km") == Quantity(1000, "m")


def test_scalar_ops():
    assert Quantity(2, "kg") * 3 == Quantity(6, "kg")
    assert 3 * Quantity(2, "kg") == Quantity(6, "kg")
    assert Quantity(6, "kg") / 3 == Quantity(2, "kg")
    assert Quantity(1, "km") / Quantity(500, "m") == pytest.approx(2)
    assert -Quantity(1, "m") == Quantity(-1, "m")


def test_compare():
    assert Quantity(1, "km") > Quantity(500, "m")
    assert Quantity(1, "m") < Quantity(1, "ft") * 4
    assert Quantity(1, "km") >= Quantity(1000, "m")
    assert Quantity(1, "m") <= Quantity(1000, "mm")


def test_incompatible():
    with pytest.raises(UnitError):
        Quantity(1, "km") + Quantity(1, "kg")
    assert Quantity(1, "km") != Quantity(1, "kg")


def test_str_repr():
    assert str(Quantity(5, "km")) == "5 km"
    assert repr(Quantity(5, "Км")) == "Quantity(5, 'km')"


def test_currency_quantity():
    set_rates({"USD": 1, "EUR": 0.5})
    q = Quantity(10, "usd")
    assert q.unit == "USD"
    assert q.to("eur") == Quantity(5, "EUR")
