"""unitconv: a simple unit and currency converter."""
from .core import UnitError, convert, supported_units
from .currency import CurrencyError, set_rates
from .quantity import Quantity

__all__ = ["convert", "Quantity", "UnitError", "CurrencyError",
           "set_rates", "supported_units"]
__version__ = "0.3.0"
