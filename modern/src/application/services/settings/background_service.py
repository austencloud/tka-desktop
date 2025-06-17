"""
Background service for managing background settings.
"""

from typing import List
from src.core.interfaces.background_interfaces import IBackgroundService
from src.core.interfaces.core_services import IUIStateManagementService


class BackgroundService(IBackgroundService):
    """Service for managing background settings."""

    def __init__(self, ui_state_service: IUIStateManagementService):
        self.ui_state_service = ui_state_service
        self._available_backgrounds = [
            "Aurora",
            "AuroraBorealis",
            "Bubbles",
            "Snowfall",
            "Starfield",
        ]

    def get_available_backgrounds(self) -> List[str]:
        """Get list of available background types."""
        return self._available_backgrounds.copy()

    def get_current_background(self) -> str:
        """Get the currently selected background type."""
        return self.ui_state_service.get_setting("background_type", "Aurora")

    def set_background(self, background_type: str) -> bool:
        """Set the background type. Returns True if successful."""
        if not self.is_valid_background(background_type):
            return False

        self.ui_state_service.set_setting("background_type", background_type)
        return True

    def is_valid_background(self, background_type: str) -> bool:
        """Check if the background type is valid."""
        return background_type in self._available_backgrounds
