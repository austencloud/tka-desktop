from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class VisibilitySettings:
    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        default_visibility = glyph_type in ["TKA", "Reversals"]

        return self.settings.value(
            f"visibility/{glyph_type}", default_visibility, type=bool
        )

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        self.settings.setValue(f"visibility/{glyph_type}", visible)

    def get_non_radial_visibility(self) -> bool:
        return self.settings.value(f"visibility/non_radial_points", False, type=bool)

    def set_non_radial_visibility(self, visible: bool):
        self.settings.setValue(f"visibility/non_radial_points", visible)

    def get_motion_visibility(self, color: str) -> bool:
        """Get visibility status for props of a specific color."""
        return self.settings.value(f"visibility/{color}_motion", True, type=bool)

    def set_motion_visibility(self, color: str, visible: bool) -> None:
        """Set visibility status for props of a specific color."""
        self.settings.setValue(f"visibility/{color}_motion", visible)
