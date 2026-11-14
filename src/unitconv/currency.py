"""Currency conversion using exchange rates from an open API (with caching)."""
from __future__ import annotations

import json
import time
import urllib.request

API_URL = "https://open.er-api.com/v6/latest/USD"

_cache: dict = {"time": 0.0, "rates": {}}


class CurrencyError(ValueError):
    """Raised when rates cannot be fetched or a currency is unknown."""


def set_rates(rates: dict[str, float]) -> None:
    """Set exchange rates manually (relative to USD). Useful offline and in tests."""
    _cache.update(time=time.time(), rates={k.upper(): float(v) for k, v in rates.items()})


def get_rates(ttl: int = 3600) -> dict[str, float]:
    """Get exchange rates, cached for ``ttl`` seconds."""
    if not _cache["rates"] or time.time() - _cache["time"] > ttl:
        try:
            with urllib.request.urlopen(API_URL, timeout=10) as resp:  # noqa: S310
                data = json.load(resp)
            _cache.update(time=time.time(), rates=data["rates"])
        except Exception as exc:
            if _cache["rates"]:  # fall back to stale data if available
                return _cache["rates"]
            raise CurrencyError(f"Could not fetch exchange rates: {exc}") from exc
    return _cache["rates"]


def convert_currency(value: float, src: str, dst: str) -> float:
    rates = get_rates()
    src, dst = src.upper(), dst.upper()
    for code in (src, dst):
        if code not in rates:
            raise CurrencyError(f"Unknown currency: {code}")
    return value / rates[src] * rates[dst]


def is_currency(code: str) -> bool:
    """Whether ``code`` looks like a currency code (3 Latin letters)."""
    return len(code) == 3 and code.isalpha() and code.isascii()
