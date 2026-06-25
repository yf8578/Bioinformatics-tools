"""TANGO package for adaptive network-informed trans-QTL module tests."""

from .core import TangoResult, tango_test, scan_modules
from .covariance import shrink_correlation, estimate_null_correlation
from .simulation import simulate_z_scores

__version__ = "0.1.0"

__all__ = [
    "TangoResult",
    "tango_test",
    "scan_modules",
    "shrink_correlation",
    "estimate_null_correlation",
    "simulate_z_scores",
]
