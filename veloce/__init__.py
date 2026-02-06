"""
Veloce API - Python client library for Veloce VPN Panel

Copyright (c) 2026 Veloce VPN Panel
Licensed under the MIT License
"""

from .client import VeloceClient
from .exceptions import (
    VeloceAPIError,
    VeloceAuthError,
    VeloceNotFoundError,
    VeloceValidationError,
    VeloceConflictError,
    VeloceServerError
)
from .utils import setup_logging

__version__ = "1.2.0"
__author__ = "Veloce Team"
__license__ = "MIT"

__all__ = [
    "VeloceClient",
    "VeloceAPIError",
    "VeloceAuthError",
    "VeloceNotFoundError",
    "VeloceValidationError",
    "VeloceConflictError",
    "VeloceServerError",
    "setup_logging",
]
