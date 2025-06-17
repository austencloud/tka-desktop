"""
Background service interfaces for dependency injection.
"""

from abc import ABC, abstractmethod
from typing import List


class IBackgroundService(ABC):
    """Interface for background management service."""

    @abstractmethod
    def get_available_backgrounds(self) -> List[str]:
        """Get list of available background types."""
        pass

    @abstractmethod
    def get_current_background(self) -> str:
        """Get the currently selected background type."""
        pass

    @abstractmethod
    def set_background(self, background_type: str) -> bool:
        """Set the background type. Returns True if successful."""
        pass

    @abstractmethod
    def is_valid_background(self, background_type: str) -> bool:
        """Check if the background type is valid."""
        pass
