from typing import List
from src.core.interfaces.tab_settings_interfaces import IPropTypeService, PropType
from src.core.interfaces.core_services import IUIStateManagementService


class PropTypeService(IPropTypeService):
    """Service for managing prop type settings"""

    def __init__(self, ui_state_service: IUIStateManagementService):
        self.ui_state_service = ui_state_service
        # Use the actual PropType enum values
        self._available_prop_types = [
            PropType.STAFF,
            PropType.FAN,
            PropType.BUUGENG,
            PropType.CLUB,
            PropType.SWORD,
            PropType.GUITAR,
            PropType.UKULELE,
        ]

    def get_current_prop_type(self) -> PropType:
        """Get the currently selected prop type"""
        prop_str = self.ui_state_service.get_setting("prop_type", "Staff")
        # Convert string to PropType enum
        try:
            return PropType(prop_str)
        except ValueError:
            return PropType.STAFF  # Default fallback

    def set_prop_type(self, prop_type: PropType) -> None:
        """Set the current prop type"""
        self.ui_state_service.set_setting("prop_type", prop_type.value)

    def get_available_prop_types(self) -> List[PropType]:
        """Get all available prop types"""
        return self._available_prop_types.copy()

    def is_valid_prop_type(self, prop_type: PropType) -> bool:
        """Check if a prop type is valid"""
        return prop_type in self._available_prop_types

    def get_prop_setting(self, setting_key: str, default=None):
        """Get a prop-related setting"""
        return self.ui_state_service.get_setting(f"prop_{setting_key}", default)

    def set_prop_setting(self, setting_key: str, value) -> None:
        """Set a prop-related setting"""
        self.ui_state_service.set_setting(f"prop_{setting_key}", value)
