from typing import Callable, Dict, List, Set, TYPE_CHECKING
from data.constants import RED, BLUE

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class VisibilityStateManager:
    """
    Central manager for all visibility states that notifies observers when states change.
    Acts as a single source of truth for visibility settings.
    """

    def __init__(self, settings_manager: "SettingsManager"):
        self.settings_manager = settings_manager
        self.settings = settings_manager.settings

        self._user_intent_states = {}

        self._initialize_from_settings()

        self._observers: Dict[str, List[Callable]] = {
            "glyph": [],
            "motion": [],
            "non_radial": [],
            "all": [],
        }

    def _initialize_from_settings(self):
        """Load initial states from settings."""
        glyph_types = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]
        for glyph_type in glyph_types:
            self._user_intent_states[glyph_type] = self.get_effective_visibility(
                glyph_type
            )

    def register_observer(self, callback: Callable, categories: List[str] = ["all"]):
        """Register a component to be notified when specific visibility states change."""
        for category in categories:
            if category in self._observers:
                self._observers[category].append(callback)

    def unregister_observer(self, callback: Callable):
        """Remove an observer."""
        for category in self._observers:
            if callback in self._observers[category]:
                self._observers[category].remove(callback)

    def _notify_observers(self, categories: List[str]):
        """Notify all relevant observers of state changes."""

        callbacks_to_notify = set()

        for category in categories:
            for callback in self._observers.get(category, []):
                callbacks_to_notify.add(callback)

        for callback in self._observers.get("all", []):
            callbacks_to_notify.add(callback)

        for callback in callbacks_to_notify:
            callback()

    def get_effective_visibility(self, glyph_type: str) -> bool:
        """Get the effective visibility of a glyph (what's actually shown)."""
        default_visibility = glyph_type in ["TKA", "Reversals"]
        return self.settings.value(
            f"visibility/{glyph_type}", default_visibility, type=bool
        )

    def set_effective_visibility(self, glyph_type: str, visible: bool) -> None:
        """Set the effective visibility of a glyph."""
        self.settings.setValue(f"visibility/{glyph_type}", visible)
        self._notify_observers(["glyph"])

    def get_user_intent_visibility(self, glyph_type: str) -> bool:
        """Get what the user intended for visibility, regardless of dependencies."""
        if glyph_type in self._user_intent_states:
            return self._user_intent_states[glyph_type]
        return self.get_effective_visibility(glyph_type)

    def set_user_intent_visibility(self, glyph_type: str, visible: bool) -> None:
        """Set the user's intent for visibility."""
        self._user_intent_states[glyph_type] = visible

        effective_visibility = visible
        if glyph_type in ["TKA", "VTG", "Elemental", "Positions"]:
            effective_visibility = visible and self.are_all_motions_visible()

        self.set_effective_visibility(glyph_type, effective_visibility)

    def get_motion_visibility(self, color: str) -> bool:
        """Get visibility for a specific motion color."""
        return self.settings.value(f"visibility/{color}_motion", True, type=bool)

    def set_motion_visibility(self, color: str, visible: bool) -> None:
        """Set visibility for a specific motion color and notify all observers."""
        other_color = "blue" if color == "red" else "red"
        
        # Prevent turning off both colors
        if visible == False and self.get_motion_visibility(other_color) == False:
            self.settings.setValue(f"visibility/{color}_motion", False)
            self.settings.setValue(f"visibility/{other_color}_motion", True)
            self._update_dependent_visibilities()
            self._notify_observers(["motion", "buttons"])  # Add buttons category
            return
            
        # Normal case
        self.settings.setValue(f"visibility/{color}_motion", visible)
        self._update_dependent_visibilities()
        self._notify_observers(["motion", "buttons"])  # Add buttons category

    def _update_dependent_visibilities(self):
        """Update visibility of glyphs that depend on motion visibility."""
        all_motions_visible = self.are_all_motions_visible()

        for glyph_type in ["TKA", "VTG", "Elemental", "Positions"]:
            user_intent = self.get_user_intent_visibility(glyph_type)
            effective_visibility = user_intent and all_motions_visible
            self.settings.setValue(f"visibility/{glyph_type}", effective_visibility)

    def get_non_radial_visibility(self) -> bool:
        """Get visibility status for non-radial points."""
        return self.settings.value("visibility/non_radial_points", False, type=bool)

    def set_non_radial_visibility(self, visible: bool) -> None:
        """Set visibility status for non-radial points."""
        self.settings.setValue("visibility/non_radial_points", visible)
        self._notify_observers(["non_radial"])

    def are_all_motions_visible(self) -> bool:
        """Check if all motions are visible."""
        return self.get_motion_visibility("red") and self.get_motion_visibility("blue")

    def is_any_motion_visible(self) -> bool:
        """Check if at least one motion is visible."""
        return self.get_motion_visibility("red") or self.get_motion_visibility("blue")
