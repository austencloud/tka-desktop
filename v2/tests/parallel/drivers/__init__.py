"""
Application Drivers
==================

Version-specific application drivers for parallel testing.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: V1 deprecation complete
PURPOSE: Provide application control interfaces for V1/V2 parallel testing
"""

from .driver_base import (
    ApplicationState,
    ActionResult,
    IApplicationDriver,
    BaseApplicationDriver,
)

from .v1_driver import V1ApplicationDriver
from .v2_driver import V2ApplicationDriver

__all__ = [
    # Base interfaces and data structures
    "ApplicationState",
    "ActionResult", 
    "IApplicationDriver",
    "BaseApplicationDriver",
    
    # Version-specific drivers
    "V1ApplicationDriver",
    "V2ApplicationDriver",
]
