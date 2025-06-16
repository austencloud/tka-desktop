from typing import Callable, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager


class VisibilityStateManager:
    """
    Central manager for all visibility states that notifies observers when states change.
    Uses a simplified model without user intent concept.
    """

    def __init__(self, settings_manager: "LegacySettingsManager"):
        self.settings_manager = settings_manager
        self.settings = settings_manager.settings

        self._observers: Dict[str, List[Callable]] = {
            "glyph": [],
            "motion": [],
            "non_radial": [],
            "all": [],
            "buttons": [],  # Added category for button updates
        }

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

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        """Get the visibility of a glyph, considering any dependencies."""
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
        """Set the visibility of a glyph."""
        self.settings.setValue(f"visibility/{glyph_type}", visible)
        self._notify_observers(["glyph"])

    def get_motion_visibility(self, color: str) -> bool:
        """Get visibility for a specific motion color."""
        return self.settings.value(f"visibility/{color}_motion", True, type=bool)

    def set_motion_visibility(self, color: str, visible: bool) -> None:
        """
        Set visibility for a specific motion color and notify all observers.
        Ensures at least one motion remains visible at all times.
        """
        other_color = "blue" if color == "red" else "red"

        # Prevent turning off both colors
        if not visible and not self.get_motion_visibility(other_color):
            self.settings.setValue(f"visibility/{color}_motion", False)
            self.settings.setValue(f"visibility/{other_color}_motion", True)
            self._notify_observers(["motion", "glyph", "buttons"])
            return

        # Normal case
        self.settings.setValue(f"visibility/{color}_motion", visible)
        self._notify_observers(["motion", "glyph", "buttons"])

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
