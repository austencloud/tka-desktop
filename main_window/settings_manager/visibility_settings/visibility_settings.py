from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class VisibilitySettings:
    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        return self.settings.value(
            f"visibility/glyph_visibility/{glyph_type}",
            False,
            type=bool,
        )

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        self.settings.setValue(f"visibility/glyph_visibility/{glyph_type}", visible)

    def get_non_radial_visibility(self) -> bool:
        return self.settings.value(
            f"visibility/grid_visibility/non_radial_points", True, type=bool
        )

    def set_non_radial_visibility(self, visible: bool):
        self.settings.setValue(f"visibility/grid_visibility/non_radial_points", visible)
