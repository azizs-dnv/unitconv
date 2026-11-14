from __future__ import annotations

from .currency import CurrencyError, convert_currency, is_currency
from .units import CATEGORIES, NONLINEAR, all_units, category_of, normalize


class UnitError(ValueError):
    """Raised when a conversion is impossible."""


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert ``value`` from ``from_unit`` to ``to_unit``.

    >>> convert(1, "km", "m")
    1000.0
    >>> convert(0, "c", "f")
    32.0
    """
    src, dst = normalize(from_unit), normalize(to_unit)

    # Non-linear categories (temperature, fuel economy)
    for to_base, from_base in NONLINEAR.values():
        if src in to_base and dst in from_base:
            try:
                return float(from_base[dst](to_base[src](value)))
            except ZeroDivisionError:
                raise UnitError("Division by zero during conversion") from None

    # Linear categories
    for table in CATEGORIES.values():
        if src in table and dst in table:
            return value * table[src] / table[dst]

    cat_src, cat_dst = category_of(src), category_of(dst)
    if cat_src and cat_dst and cat_src != cat_dst:
        raise UnitError(
            f"Incompatible units: '{from_unit}' ({cat_src}) and '{to_unit}' ({cat_dst})"
        )

    # Currencies
    if cat_src is None and cat_dst is None and is_currency(src) and is_currency(dst):
        try:
            return convert_currency(value, src, dst)
        except CurrencyError as exc:
            raise UnitError(str(exc)) from exc

    raise UnitError(f"Cannot convert '{from_unit}' to '{to_unit}'")


def supported_units() -> dict[str, list[str]]:
    """All supported units grouped by category (currencies excluded)."""
    return all_units()
