from typing import List
from src.core.interfaces.tab_settings_interfaces import IPropTypeService
from src.core.interfaces.core_services import IUIStateManagementService


class PropTypeService(IPropTypeService):
    """Service for managing prop type settings"""

    def __init__(self, ui_state_service: IUIStateManagementService):
        self.ui_state_service = ui_state_service
        self._available_prop_types = [
            "Staff",
            "Fans",
            "Buugeng",
            "Clubs",
            "Hands",
            "Bigballs",
            "Bigstaffs",
            "Fractals",
            "Triad",
            "Minihoop",
            "Sword",
            "Guitar",
            "Ukulele",
        ]

    def get_current_prop_type(self) -> str:
        """Get the currently selected prop type"""
        return self.ui_state_service.get_setting("prop_type", "Staff")

    def set_prop_type(self, prop_type: str) -> bool:
        """Set the current prop type"""
        if prop_type not in self._available_prop_types:
            return False

        self.ui_state_service.set_setting("prop_type", prop_type)
        return True

    def get_available_prop_types(self) -> List[str]:
        """Get all available prop types"""
        return self._available_prop_types.copy()

    def is_valid_prop_type(self, prop_type: str) -> bool:
        """Check if a prop type is valid"""
        return prop_type in self._available_prop_types

    def get_prop_setting(self, setting_key: str, default=None):
        """Get a prop-related setting"""
        return self.ui_state_service.get_setting(f"prop_{setting_key}", default)

    def set_prop_setting(self, setting_key: str, value) -> None:
        """Set a prop-related setting"""
        self.ui_state_service.set_setting(f"prop_{setting_key}", value)
