from typing import Dict, Any
from src.core.interfaces.tab_settings_interfaces import IVisibilityService
from src.core.interfaces.core_services import IUIStateManagementService


class VisibilityService(IVisibilityService):
    """Service for managing visibility settings for glyphs and UI elements"""

    def __init__(self, ui_state_service: IUIStateManagementService):
        self.ui_state_service = ui_state_service
        self._glyph_types = [
            "TKA",
            "Reversals",
            "VTG",
            "Elemental",
            "Positions",
            "Red Motion",
            "Blue Motion",
        ]

    def get_glyph_visibility(self, glyph_name: str) -> bool:
        """Get visibility state for a specific glyph type"""
        default_visibility = {
            "TKA": True,
            "Reversals": True,
            "VTG": True,
            "Elemental": True,
            "Positions": True,
            "Red Motion": True,
            "Blue Motion": True,
        }

        return self.ui_state_service.get_setting(
            f"visibility_{glyph_name.lower().replace(' ', '_')}",
            default_visibility.get(glyph_name, True),
        )

    def set_glyph_visibility(self, glyph_name: str, visible: bool) -> None:
        """Set visibility state for a specific glyph type"""
        self.ui_state_service.set_setting(
            f"visibility_{glyph_name.lower().replace(' ', '_')}", visible
        )

    def get_motion_visibility(self, motion_color: str) -> bool:
        """Get visibility for motion arrows (red/blue)"""
        return self.get_glyph_visibility(f"{motion_color.title()} Motion")

    def set_motion_visibility(self, motion_color: str, visible: bool) -> None:
        """Set visibility for motion arrows (red/blue)"""
        self.set_glyph_visibility(f"{motion_color.title()} Motion", visible)

    def get_non_radial_visibility(self) -> bool:
        """Get visibility state for non-radial points"""
        return self.ui_state_service.get_setting("visibility_non_radial", True)

    def set_non_radial_visibility(self, visible: bool) -> None:
        """Set visibility state for non-radial points"""
        self.ui_state_service.set_setting("visibility_non_radial", visible)

    def get_all_visibility_settings(self) -> Dict[str, bool]:
        """Get all visibility settings as a dictionary"""
        settings = {}

        for glyph in self._glyph_types:
            settings[glyph] = self.get_glyph_visibility(glyph)

        settings["Non-radial"] = self.get_non_radial_visibility()

        return settings

    def reset_to_defaults(self) -> None:
        """Reset all visibility settings to defaults"""
        for glyph in self._glyph_types:
            self.set_glyph_visibility(glyph, True)

        self.set_non_radial_visibility(True)

    def get_grid_visibility(self) -> bool:
        """Get grid visibility setting"""
        return self.ui_state_service.get_setting("show_grid", True)

    def set_grid_visibility(self, visible: bool) -> None:
        """Set grid visibility setting"""
        self.ui_state_service.set_setting("show_grid", visible)
