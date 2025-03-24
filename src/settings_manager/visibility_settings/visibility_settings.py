from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class VisibilitySettings:
    """
    Manages visibility settings with two concepts:
    - User Intent: What the user has chosen for visibility (stored in _user_intent_states)
    - Effective Visibility: The actual visibility after applying dependencies (stored in settings)
    
    Dependent glyphs like TKA, VTG, Elemental need both motions visible to show,
    even if the user has set them to visible.
    """

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings
        # In-memory cache of user intent states (what user wants, regardless of dependencies)
        self._user_intent_states = {}
        self._initialize_user_intent_states()

    def _initialize_user_intent_states(self) -> None:
        """Initialize the user intent visibility states from effective settings."""
        glyph_types = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]
        for glyph_type in glyph_types:
            self._user_intent_states[glyph_type] = self.get_effective_visibility(
                glyph_type
            )

    def get_effective_visibility(self, glyph_type: str) -> bool:
        """
        Get the effective visibility state of a glyph (what's actually shown).
        This can be affected by dependencies like motion visibility.
        """
        default_visibility = glyph_type in ["TKA", "Reversals"]
        return self.settings.value(
            f"visibility/{glyph_type}", default_visibility, type=bool
        )

    def set_effective_visibility(self, glyph_type: str, visible: bool) -> None:
        """
        Set the effective visibility state of a glyph (what's actually shown).
        This applies the final visibility after considering all dependencies.
        """
        self.settings.setValue(f"visibility/{glyph_type}", visible)

    def get_user_intent_visibility(self, glyph_type: str) -> bool:
        """
        Get the user's intended visibility state for a glyph.
        This represents what the user wants, regardless of dependencies.
        """
        if glyph_type in self._user_intent_states:
            return self._user_intent_states[glyph_type]
        return self.get_effective_visibility(glyph_type)

    def set_user_intent_visibility(self, glyph_type: str, visible: bool) -> None:
        """
        Set the user's intended visibility state for a glyph.
        This stores what the user wants, even if it can't be applied due to dependencies.
        """
        self._user_intent_states[glyph_type] = visible

    # Backward compatibility methods
    def get_glyph_visibility(self, glyph_type: str) -> bool:
        """Legacy method - use get_effective_visibility instead."""
        return self.get_effective_visibility(glyph_type)

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        """Legacy method - use set_effective_visibility instead."""
        self.set_effective_visibility(glyph_type, visible)

    def get_real_glyph_visibility(self, glyph_type: str) -> bool:
        """Legacy method - use get_user_intent_visibility instead."""
        return self.get_user_intent_visibility(glyph_type)

    def set_real_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        """Legacy method - use set_user_intent_visibility instead."""
        self.set_user_intent_visibility(glyph_type, visible)

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