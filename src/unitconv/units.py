"""Unit tables.

For linear categories each unit stores a factor: how many base units
one such unit contains. The base unit is given in a comment.
Categories with non-linear conversion (temperature, fuel economy) use functions.
"""
from __future__ import annotations

import math

LENGTH = {  # base: metre
    "nm": 1e-9, "um": 1e-6, "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
    "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344,
    "nmi": 1852.0, "ly": 9.4607304725808e15,
}
WEIGHT = {  # base: kilogram
    "ug": 1e-9, "mg": 1e-6, "g": 0.001, "kg": 1.0, "t": 1000.0,
    "ct": 0.0002, "oz": 0.028349523125, "lb": 0.45359237, "st": 6.35029318,
}
AREA = {  # base: square metre
    "mm2": 1e-6, "cm2": 1e-4, "m2": 1.0, "km2": 1e6,
    "sot": 100.0, "ha": 10_000.0, "ac": 4046.8564224,
    "in2": 0.00064516, "ft2": 0.09290304, "yd2": 0.83612736, "mi2": 2589988.110336,
}
VOLUME = {  # base: litre (gallons etc. are US units)
    "ml": 0.001, "cm3": 0.001, "l": 1.0, "m3": 1000.0,
    "tsp": 0.00492892159375, "tbsp": 0.01478676478125, "floz": 0.0295735295625,
    "pt": 0.473176473, "qt": 0.946352946, "gal": 3.785411784, "bbl": 158.987294928,
}
SPEED = {  # base: metre per second
    "m/s": 1.0, "km/h": 1 / 3.6, "mph": 0.44704, "ft/s": 0.3048,
    "kn": 1852 / 3600, "mach": 340.29,  # Mach at sea level
}
TIME = {  # base: second
    "ns": 1e-9, "us": 1e-6, "ms": 0.001, "s": 1.0, "min": 60.0, "h": 3600.0,
    "d": 86400.0, "wk": 604800.0,
    "mo": 2_629_800.0,   # average month (30.4375 days)
    "yr": 31_557_600.0,  # Julian year (365.25 days)
}
DATA = {  # base: byte
    "bit": 0.125, "kbit": 125.0, "mbit": 125_000.0, "gbit": 125e6,
    "b": 1.0, "kb": 1e3, "mb": 1e6, "gb": 1e9, "tb": 1e12, "pb": 1e15,
    "kib": 1024.0, "mib": 1024.0**2, "gib": 1024.0**3, "tib": 1024.0**4,
    "pib": 1024.0**5,
}
PRESSURE = {  # base: pascal
    "pa": 1.0, "hpa": 100.0, "kpa": 1e3, "mpa": 1e6,
    "mbar": 100.0, "bar": 1e5, "atm": 101_325.0,
    "psi": 6894.757293168, "mmhg": 133.322387415, "torr": 101_325 / 760,
}
ENERGY = {  # base: joule
    "ev": 1.602176634e-19, "j": 1.0, "kj": 1e3, "mj": 1e6,
    "cal": 4.184, "kcal": 4184.0, "wh": 3600.0, "kwh": 3.6e6,
    "btu": 1055.05585262, "ftlb": 1.3558179483314004,
}
POWER = {  # base: watt
    "w": 1.0, "kw": 1e3,
    "hp": 745.69987158227,  # mechanical horsepower
    "ps": 735.49875,        # metric horsepower
    "btu/h": 0.29307107,
}
ANGLE = {  # base: degree
    "arcsec": 1 / 3600, "arcmin": 1 / 60, "deg": 1.0,
    "grad": 0.9, "rad": 180 / math.pi, "turn": 360.0,
}
FREQUENCY = {  # base: hertz
    "rpm": 1 / 60, "hz": 1.0, "khz": 1e3, "mhz": 1e6, "ghz": 1e9,
}
FORCE = {  # base: newton
    "dyn": 1e-5, "n": 1.0, "kgf": 9.80665, "lbf": 4.4482216152605,
}

CATEGORIES = {
    "length": LENGTH, "weight": WEIGHT, "area": AREA, "volume": VOLUME,
    "speed": SPEED, "time": TIME, "data": DATA, "pressure": PRESSURE,
    "energy": ENERGY, "power": POWER, "angle": ANGLE,
    "frequency": FREQUENCY, "force": FORCE,
}

# --- Non-linear categories: functions to and from the base unit ---

# Temperature (base: degree Celsius)
TO_CELSIUS = {
    "c": lambda x: x,
    "f": lambda x: (x - 32) * 5 / 9,
    "k": lambda x: x - 273.15,
}
FROM_CELSIUS = {
    "c": lambda x: x,
    "f": lambda x: x * 9 / 5 + 32,
    "k": lambda x: x + 273.15,
}

# Fuel economy (base: km per litre). L/100 km is inversely proportional.
_MPG = 1.609344 / 3.785411784  # miles per gallon -> km per litre
TO_KML = {
    "km/l": lambda x: x,
    "mpg": lambda x: x * _MPG,
    "l/100km": lambda x: 100 / x,
}
FROM_KML = {
    "km/l": lambda x: x,
    "mpg": lambda x: x / _MPG,
    "l/100km": lambda x: 100 / x,
}

NONLINEAR = {
    "temperature": (TO_CELSIUS, FROM_CELSIUS),
    "fuel": (TO_KML, FROM_KML),
}
TEMPERATURE = tuple(TO_CELSIUS)

# --- Aliases (Russian and English names; keys must be lowercase) ---
ALIASES = {
    # length
    "нм": "nm", "мкм": "um", "µm": "um", "мм": "mm", "см": "cm", "м": "m", "км": "km",
    "дюйм": "in", "фут": "ft", "ярд": "yd", "миля": "mi", "мили": "mi",
    "meter": "m", "metre": "m", "kilometer": "km", "kilometre": "km",
    "mile": "mi", "foot": "ft", "feet": "ft", "inch": "in", "yard": "yd",
    "световой год": "ly",
    # weight
    "мкг": "ug", "µg": "ug", "мг": "mg", "г": "g", "кг": "kg", "т": "t",
    "карат": "ct", "унция": "oz", "фунт": "lb", "стоун": "st",
    "gram": "g", "kilogram": "kg", "pound": "lb", "ounce": "oz", "tonne": "t",
    # area
    "мм2": "mm2", "см2": "cm2", "м2": "m2", "км2": "km2", "сотка": "sot",
    "га": "ha", "акр": "ac", "acre": "ac", "hectare": "ha",
    # volume
    "мл": "ml", "см3": "cm3", "л": "l", "м3": "m3", "галлон": "gal",
    "баррель": "bbl", "liter": "l", "litre": "l", "gallon": "gal",
    # speed
    "м/с": "m/s", "км/ч": "km/h", "кмч": "km/h", "kph": "km/h",
    "узел": "kn", "knot": "kn", "фут/с": "ft/s",
    # time
    "нс": "ns", "мкс": "us", "µs": "us", "мс": "ms", "с": "s", "сек": "s",
    "мин": "min", "ч": "h", "час": "h", "сут": "d", "день": "d", "нед": "wk",
    "мес": "mo", "год": "yr",
    "sec": "s", "second": "s", "minute": "min", "hour": "h", "day": "d",
    "week": "wk", "month": "mo", "year": "yr",
    # data
    "бит": "bit", "байт": "b", "кб": "kb", "мб": "mb", "гб": "gb", "тб": "tb",
    "пб": "pb", "кбит": "kbit", "мбит": "mbit", "гбит": "gbit",
    "кибб": "kib", "byte": "b",
    # pressure
    "па": "pa", "гпа": "hpa", "кпа": "kpa", "мпа": "mpa", "мбар": "mbar",
    "бар": "bar", "атм": "atm", "ммртст": "mmhg", "мм.рт.ст.": "mmhg",
    "мм рт. ст.": "mmhg", "мм рт.ст.": "mmhg",
    # energy
    "эв": "ev", "дж": "j", "кдж": "kj", "мдж": "mj", "кал": "cal",
    "ккал": "kcal", "втч": "wh", "квтч": "kwh", "квт·ч": "kwh", "квт*ч": "kwh",
    "joule": "j",
    # power
    "вт": "w", "квт": "kw", "лс": "ps", "л.с.": "ps", "watt": "w",
    "horsepower": "hp",
    # angle
    "°": "deg", "град": "deg", "градус": "deg", "рад": "rad",
    "оборот": "turn", "degree": "deg", "radian": "rad",
    # frequency
    "гц": "hz", "кгц": "khz", "мгц": "mhz", "ггц": "ghz", "об/мин": "rpm",
    # force
    "н": "n", "кгс": "kgf", "newton": "n", "дин": "dyn",
    # fuel economy
    "км/л": "km/l", "л/100км": "l/100km", "л/100 км": "l/100km",
    "l/100 km": "l/100km",
    # temperature
    "°c": "c", "°f": "f", "°k": "k", "°с": "c",
    "celsius": "c", "fahrenheit": "f", "kelvin": "k",
    "цельсий": "c", "фаренгейт": "f", "кельвин": "k",
}


def normalize(unit: str) -> str:
    """Return the canonical (lowercase, de-aliased) unit name."""
    unit = unit.strip().lower()
    return ALIASES.get(unit, unit)


def category_of(unit: str) -> str | None:
    """Return the unit's category name, or None if unknown."""
    unit = normalize(unit)
    for name, (to_base, _) in NONLINEAR.items():
        if unit in to_base:
            return name
    for name, table in CATEGORIES.items():
        if unit in table:
            return name
    return None


def all_units() -> dict[str, list[str]]:
    """All supported units grouped by category (currencies excluded)."""
    result = {name: list(table) for name, table in CATEGORIES.items()}
    for name, (to_base, _) in NONLINEAR.items():
        result[name] = list(to_base)
    return result
