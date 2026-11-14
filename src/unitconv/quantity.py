from __future__ import annotations

import math

from .core import UnitError, convert
from .currency import is_currency
from .units import category_of, normalize


class Quantity:
    """A value with a unit of measurement.

    >>> Quantity(5, "km") + Quantity(500, "m")
    Quantity(5.5, 'km')
    >>> Quantity(1, "km").to("m")
    Quantity(1000.0, 'm')
    """

    __slots__ = ("value", "unit")

    def __init__(self, value: float, unit: str):
        self.value = value
        canonical = normalize(unit)
        if category_of(canonical) is None and is_currency(canonical):
            canonical = canonical.upper()  # currency codes are stored uppercase
        self.unit = canonical

    def to(self, unit: str) -> Quantity:
        return Quantity(convert(self.value, self.unit, unit), unit)

    def _other(self, other: Quantity) -> float:
        if not isinstance(other, Quantity):
            raise TypeError("Operation is only supported between Quantity objects")
        return convert(other.value, other.unit, self.unit)

    def __add__(self, other):
        return Quantity(self.value + self._other(other), self.unit)

    def __sub__(self, other):
        return Quantity(self.value - self._other(other), self.unit)

    def __mul__(self, k):
        if isinstance(k, Quantity):
            return NotImplemented
        return Quantity(self.value * k, self.unit)

    __rmul__ = __mul__

    def __truediv__(self, k):
        if isinstance(k, Quantity):
            return self.value / self._other(k)  # ratio of quantities
        return Quantity(self.value / k, self.unit)

    def __neg__(self):
        return Quantity(-self.value, self.unit)

    def __eq__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        try:
            return math.isclose(self.value, self._other(other), rel_tol=1e-9)
        except UnitError:
            return False

    def __lt__(self, other):
        return self.value < self._other(other)

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return self.value > self._other(other)

    def __ge__(self, other):
        return self == other or self > other

    def __repr__(self):
        return f"Quantity({self.value!r}, {self.unit!r})"

    def __str__(self):
        return f"{self.value:g} {self.unit}"
