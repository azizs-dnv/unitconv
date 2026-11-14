from __future__ import annotations

import argparse
import sys

from . import __version__
from .core import UnitError, convert, supported_units


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="unitconv",
        description="Unit and currency converter.",
        epilog="Examples: unitconv 5 km mi | unitconv 100 c f | unitconv 10 usd eur",
    )
    p.add_argument("value", nargs="?", type=float, help="number to convert")
    p.add_argument("from_unit", nargs="?", help="source unit")
    p.add_argument("to_unit", nargs="?", help="target unit")
    p.add_argument("-p", "--precision", type=int, default=6,
                   help="decimal places (default: 6)")
    p.add_argument("-l", "--list", action="store_true",
                   help="list supported units")
    p.add_argument("-V", "--version", action="version", version=__version__)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        for category, units in supported_units().items():
            print(f"{category}: {', '.join(units)}")
        print("currency: ISO 4217 codes (USD, EUR, TJS, ...)")
        return 0

    if args.value is None or not args.from_unit or not args.to_unit:
        parser.print_usage(sys.stderr)
        return 2

    try:
        result = convert(args.value, args.from_unit, args.to_unit)
    except UnitError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"{args.value:g} {args.from_unit} = {round(result, args.precision):g} {args.to_unit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
