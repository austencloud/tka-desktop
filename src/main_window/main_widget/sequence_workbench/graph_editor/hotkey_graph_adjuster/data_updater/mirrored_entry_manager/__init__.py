"""
Mirrored Entry Management System
-------------------------------

This module provides functionality for managing mirrored entries in special placements.
It is designed to be a clean replacement for the old mirrored entry system.

Main Components:
- MirroredEntryService: Main entry point for all mirrored entry operations
- MirroredEntryFactory: Factory for creating and configuring mirrored entry components
- MirroredEntryAdapter: Adapter for integrating with existing code
"""

from .mirrored_entry_service import MirroredEntryService
from .mirrored_entry_factory import MirroredEntryFactory
from .mirrored_entry_adapter import MirroredEntryAdapter
from .mirrored_entry_utils import MirroredEntryUtils

# Export the main components
__all__ = [
    'MirroredEntryService',
    'MirroredEntryFactory',
    'MirroredEntryAdapter',
    'MirroredEntryUtils',
]
