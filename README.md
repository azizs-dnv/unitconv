# unitconv

[![CI](https://github.com/YOUR_USERNAME/unitconv/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/unitconv/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A dependency-free Python library for converting units and currencies, with a command-line tool and a `Quantity` class that supports arithmetic.

## Installation

```bash
pip install unitconv-azizs        # once published to PyPI
# or from source:
git clone https://github.com/azizs-dnv/unitconv.git
cd unitconv
pip install -e ".[dev]"
```

## Quick start

```python
from unitconv import convert, Quantity

convert(5, "km", "mi")        # 3.1068...
convert(100, "c", "f")        # 212.0
convert(2, "kg", "lb")        # 4.409...
convert(1, "atm", "psi")      # 14.69...
convert(7, "l/100km", "mpg")  # 33.6...
convert(10, "usd", "tjs")     # at the current exchange rate

# Quantities with units
d = Quantity(5, "km") + Quantity(500, "m")   # Quantity(5.5, 'km')
d.to("mi")
Quantity(1, "km") > Quantity(500, "m")       # True
```

### Command line

```bash
unitconv 5 km mi
unitconv 100 c f
unitconv 2500 kcal kj
unitconv 10 usd eur -p 2
unitconv --list
python -m unitconv 1 gb mib
```

## Supported categories

| Category | Units |
|---|---|
| Length | nm, um, mm, cm, m, km, in, ft, yd, mi, nmi, ly |
| Weight | ug, mg, g, kg, t, ct, oz, lb, st |
| Area | mm2, cm2, m2, km2, sot, ha, ac, in2, ft2, yd2, mi2 |
| Volume | ml, cm3, l, m3, tsp, tbsp, floz, pt, qt, gal, bbl |
| Speed | m/s, km/h, mph, ft/s, kn, mach |
| Time | ns, us, ms, s, min, h, d, wk, mo, yr |
| Data | bit, kbit, mbit, gbit, b, kb, mb, gb, tb, pb, kib, mib, gib, tib, pib |
| Pressure | pa, hpa, kpa, mpa, mbar, bar, atm, psi, mmhg, torr |
| Energy | ev, j, kj, mj, cal, kcal, wh, kwh, btu, ftlb |
| Power | w, kw, hp, ps, btu/h |
| Angle | arcsec, arcmin, deg, grad, rad, turn |
| Frequency | rpm, hz, khz, mhz, ghz |
| Force | dyn, n, kgf, lbf |
| Temperature | c, f, k |
| Fuel economy | km/l, mpg, l/100km |
| Currencies | ISO 4217 codes (USD, EUR, TJS, ...) |

Unit names are case-insensitive. English names (`kilometer`, `pound`, `knot`) and Russian names (`км`, `кг`, `ккал`, `л.с.`, `мм рт. ст.`) are accepted as aliases. Gallons, pints and barrels are US units. Mach, month and year are approximations (see comments in `units.py`).

## Currencies

Exchange rates come from an open API ([open.er-api.com](https://www.exchangerate-api.com/docs/free)) and are cached for one hour. Please check the service's terms of use. For offline use and tests, set rates manually:

```python
from unitconv import set_rates
set_rates({"USD": 1, "EUR": 0.92, "TJS": 10.7})
```

## Errors

All conversion errors raise `UnitError`:

```python
from unitconv import convert, UnitError

try:
    convert(1, "km", "kg")
except UnitError as e:
    print(e)   # Incompatible units: 'km' (length) and 'kg' (weight)
```

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for details and [CHANGELOG.md](CHANGELOG.md) for release history.

## License

MIT, see [LICENSE](LICENSE).
