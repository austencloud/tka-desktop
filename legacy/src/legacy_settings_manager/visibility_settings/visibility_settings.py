from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager


class VisibilitySettings:
    """
    Manages visibility settings with a simplified approach.

    Motion visibility affects dependent glyphs (TKA, VTG, Elemental, Positions).
    These dependent glyphs will only be visible when both motions are visible.
    """

    def __init__(self, settings_manager: "LegacySettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        """
        Get the visibility state of a glyph. For dependent glyphs, this also
        considers motion visibility.
        """
        default_visibility = glyph_type in ["TKA", "Reversals"]
        base_visibility = self.settings.value(
            f"visibility/{glyph_type}", default_visibility, type=bool
        )

        # For dependent glyphs, check if both motions are visible
        if glyph_type in ["TKA", "VTG", "Elemental", "Positions"]:
            return base_visibility and self.are_all_motions_visible()

        # For non-dependent glyphs, return direct visibility
        return base_visibility

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        """Set the visibility state of a glyph."""
        self.settings.setValue(f"visibility/{glyph_type}", visible)

    def get_non_radial_visibility(self) -> bool:
        """Get visibility status for non-radial points."""
        return self.settings.value("visibility/non_radial_points", False, type=bool)

    def set_non_radial_visibility(self, visible: bool):
        """Set visibility status for non-radial points."""
        self.settings.setValue("visibility/non_radial_points", visible)

    def get_motion_visibility(self, color: str) -> bool:
        """Get visibility status for motions of a specific color."""
        return self.settings.value(f"visibility/{color}_motion", True, type=bool)

    def set_motion_visibility(self, color: str, visible: bool) -> None:
        """
        Set visibility status for motions of a specific color.
        Ensures at least one motion remains visible at all times.
        """
        other_color = "blue" if color == "red" else "red"

        # Prevent turning off both colors
        if not visible and not self.get_motion_visibility(other_color):
            self.settings.setValue(f"visibility/{color}_motion", False)
            self.settings.setValue(f"visibility/{other_color}_motion", True)
            return

        # Normal case
        self.settings.setValue(f"visibility/{color}_motion", visible)

    def are_all_motions_visible(self) -> bool:
        """Check if all motions are visible."""
        return self.get_motion_visibility("red") and self.get_motion_visibility("blue")

    def is_any_motion_visible(self) -> bool:
        """Check if at least one motion is visible."""
        return self.get_motion_visibility("red") or self.get_motion_visibility("blue")
