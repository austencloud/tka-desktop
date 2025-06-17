"""
Application Drivers
==================

Version-specific application drivers for parallel testing.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Provide application control interfaces for Legacy/Modern parallel testing
"""

from .driver_base import (
    ApplicationState,
    ActionResult,
    IApplicationDriver,
    BaseApplicationDriver,
)

from .legacy_driver import LegacyApplicationDriver
from .modern_driver import ModernApplicationDriver

__all__ = [
    # Base interfaces and data structures
    "ApplicationState",
    "ActionResult",
    "IApplicationDriver",
    "BaseApplicationDriver",
    # Version-specific drivers
    "LegacyApplicationDriver",
    "ModernApplicationDriver",
]
