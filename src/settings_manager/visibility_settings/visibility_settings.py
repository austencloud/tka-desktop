from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class VisibilitySettings:
    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings
        # In-memory cache of real visibility states (not affected by dependencies)
        self._real_visibility_states = {}
        self._initialize_real_states()

    def _initialize_real_states(self) -> None:
        """Initialize the real visibility states from settings."""
        glyph_types = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]
        for glyph_type in glyph_types:
            self._real_visibility_states[glyph_type] = self.get_glyph_visibility(
                glyph_type
            )

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        default_visibility = glyph_type in ["TKA", "Reversals"]
        return self.settings.value(
            f"visibility/{glyph_type}", default_visibility, type=bool
        )

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        self.settings.setValue(f"visibility/{glyph_type}", visible)

    def get_real_glyph_visibility(self, glyph_type: str) -> bool:
        """Get the 'real' visibility state - what it would be if no dependencies affected it."""
        if glyph_type in self._real_visibility_states:
            return self._real_visibility_states[glyph_type]
        return self.get_glyph_visibility(glyph_type)

    def set_real_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        """Store the real visibility state without affecting the actual setting."""
        self._real_visibility_states[glyph_type] = visible

    def get_non_radial_visibility(self) -> bool:
        return self.settings.value("visibility/non_radial_points", False, type=bool)

    def set_non_radial_visibility(self, visible: bool):
        self.settings.setValue("visibility/non_radial_points", visible)

    def get_motion_visibility(self, color: str) -> bool:
        """Get visibility status for motions of a specific color."""
        return self.settings.value(f"visibility/{color}_motion", True, type=bool)

    def set_motion_visibility(self, color: str, visible: bool) -> None:
        """Set visibility status for motions of a specific color."""
        self.settings.setValue(f"visibility/{color}_motion", visible)

    def are_all_motions_visible(self) -> bool:
        """Check if all motions are visible."""
        return self.get_motion_visibility("red") and self.get_motion_visibility("blue")
