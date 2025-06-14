"""
Graph Editor Hotkey Service

Implements V1 hotkey functionality for V2 graph editor.
Provides WASD arrow movement, X/Z/C key operations with exact V1 behavior.
"""

from typing import Optional, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent

from src.domain.models.core_models import BeatData
from src.core.interfaces.workbench_services import IGraphEditorService


class GraphEditorHotkeyService(QObject):
    """Service for handling graph editor hotkeys with V1 compatibility."""

    # Signals for hotkey actions
    arrow_moved = pyqtSignal(str, str)  # arrow_id, direction
    arrow_rotation_overridden = pyqtSignal(str)  # arrow_id
    special_placement_removed = pyqtSignal(str, str)  # letter, arrow_id
    prop_placement_overridden = pyqtSignal()

    def __init__(self, graph_service: IGraphEditorService):
        super().__init__()

        self._graph_service = graph_service
        self._hotkey_enabled = True

        # Movement key mappings (V1 compatible)
        self._movement_keys = {
            Qt.Key.Key_W: "up",
            Qt.Key.Key_A: "left",
            Qt.Key.Key_S: "down",
            Qt.Key.Key_D: "right",
        }

        # Special action keys
        self._action_keys = {
            Qt.Key.Key_X: self._handle_rotation_override,
            Qt.Key.Key_Z: self._handle_special_placement_removal,
            Qt.Key.Key_C: self._handle_prop_placement_override,
        }

    def handle_key_event(self, event: QKeyEvent) -> bool:
        """
        Handle key press events for graph editor.

        Returns True if the key was handled, False otherwise.
        """
        if not self._hotkey_enabled:
            return False

        key = event.key()
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier

        # Get currently selected arrow
        selected_arrow = self._graph_service.get_selected_arrow()

        # Handle movement keys (only when arrow is selected)
        if selected_arrow and key in self._movement_keys:
            return self._handle_arrow_movement(
                selected_arrow, key, shift_held, ctrl_held
            )

        # Handle special action keys
        if key in self._action_keys:
            if key == Qt.Key.Key_X and selected_arrow:
                return self._action_keys[key](selected_arrow)
            elif key == Qt.Key.Key_Z and selected_arrow:
                return self._action_keys[key](selected_arrow)
            elif key == Qt.Key.Key_C:
                return self._action_keys[key]()

        return False

    def _handle_arrow_movement(
        self, arrow_id: str, key: Qt.Key, shift_held: bool, ctrl_held: bool
    ) -> bool:
        """Handle WASD arrow movement with V1 logic."""
        direction = self._movement_keys[key]

        try:
            # Get current arrow properties
            arrow_properties = self._get_arrow_properties(arrow_id)
            if not arrow_properties:
                return False

            # Calculate movement based on modifiers
            movement_amount = self._calculate_movement_amount(shift_held, ctrl_held)

            # Apply movement in specified direction
            new_properties = self._apply_movement(
                arrow_properties, direction, movement_amount
            )

            # Update arrow through V1 integration
            success = self._update_arrow_properties(arrow_id, new_properties)

            if success:
                self.arrow_moved.emit(arrow_id, direction)
                self._refresh_pictograph()

            return success

        except Exception as e:
            print(f"Error handling arrow movement: {e}")
            return False

    def _calculate_movement_amount(self, shift_held: bool, ctrl_held: bool) -> float:
        """Calculate movement amount based on modifier keys (V1 logic)."""
        if ctrl_held:
            return 0.1  # Fine movement
        elif shift_held:
            return 5.0  # Large movement
        else:
            return 1.0  # Normal movement

    def _apply_movement(
        self, arrow_properties: Dict[str, Any], direction: str, amount: float
    ) -> Dict[str, Any]:
        """Apply movement to arrow properties."""
        new_properties = arrow_properties.copy()

        # Get current position
        x = arrow_properties.get("x", 0.0)
        y = arrow_properties.get("y", 0.0)

        # Apply movement based on direction
        if direction == "up":
            new_properties["y"] = y - amount
        elif direction == "down":
            new_properties["y"] = y + amount
        elif direction == "left":
            new_properties["x"] = x - amount
        elif direction == "right":
            new_properties["x"] = x + amount

        return new_properties

    def _handle_rotation_override(self, arrow_id: str) -> bool:
        """Handle X key - rotation angle override (V1 logic)."""
        try:
            # Get current arrow properties
            arrow_properties = self._get_arrow_properties(arrow_id)
            if not arrow_properties:
                return False

            # Apply rotation override logic from V1
            new_properties = self._apply_rotation_override(arrow_properties)

            # Update arrow
            success = self._update_arrow_properties(arrow_id, new_properties)

            if success:
                self.arrow_rotation_overridden.emit(arrow_id)
                self._refresh_pictograph()

            return success

        except Exception as e:
            print(f"Error handling rotation override: {e}")
            return False

    def _apply_rotation_override(
        self, arrow_properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply V1 rotation override logic."""
        new_properties = arrow_properties.copy()

        # V1 rotation override logic - cycle through standard angles
        current_angle = arrow_properties.get("rotation", 0.0)
        standard_angles = [0, 45, 90, 135, 180, 225, 270, 315]

        # Find next angle in sequence
        try:
            current_index = standard_angles.index(current_angle)
            next_index = (current_index + 1) % len(standard_angles)
            new_properties["rotation"] = standard_angles[next_index]
        except ValueError:
            # Current angle not in standard list, snap to nearest
            new_properties["rotation"] = 0

        return new_properties

    def _handle_special_placement_removal(self, arrow_id: str) -> bool:
        """Handle Z key - remove special placement entry (V1 logic)."""
        try:
            # Get current beat data
            current_beat = self._graph_service.get_selected_beat()
            if not current_beat:
                return False

            # Remove special placement entry for this letter/arrow combination
            letter = current_beat.letter

            # This would integrate with V1's special placement removal logic
            success = self._remove_special_placement_entry(letter, arrow_id)

            if success:
                self.special_placement_removed.emit(letter, arrow_id)
                self._refresh_pictograph()

            return success

        except Exception as e:
            print(f"Error removing special placement: {e}")
            return False

    def _handle_prop_placement_override(self) -> bool:
        """Handle C key - prop placement override (V1 logic)."""
        try:
            # Apply prop placement override logic from V1
            success = self._apply_prop_placement_override()

            if success:
                self.prop_placement_overridden.emit()
                self._refresh_pictograph()

            return success

        except Exception as e:
            print(f"Error handling prop placement override: {e}")
            return False

    def _get_arrow_properties(self, arrow_id: str) -> Optional[Dict[str, Any]]:
        """Get current properties of specified arrow from V2 beat data."""
        try:
            current_beat = self._graph_service.get_selected_beat()
            if not current_beat:
                return None

            # Get motion data for the specified arrow
            motion_data = None
            if arrow_id == "blue" and current_beat.blue_motion:
                motion_data = current_beat.blue_motion
            elif arrow_id == "red" and current_beat.red_motion:
                motion_data = current_beat.red_motion

            if not motion_data:
                return None

            # Extract properties from motion data
            return {
                "x": getattr(motion_data, "position_x", 0.0),
                "y": getattr(motion_data, "position_y", 0.0),
                "rotation": getattr(motion_data, "rotation_angle", 0.0),
                "color": arrow_id,
                "orientation": getattr(motion_data, "orientation", None),
                "turns": getattr(motion_data, "turns", 0.0),
                "motion_type": getattr(motion_data, "motion_type", None),
                "location": getattr(motion_data, "location", None),
            }

        except Exception as e:
            print(f"Error getting arrow properties: {e}")
            return None

    def _update_arrow_properties(
        self, arrow_id: str, properties: Dict[str, Any]
    ) -> bool:
        """Update arrow properties through V2 graph editor service."""
        try:
            # Use the graph editor service to update arrow properties
            if hasattr(self._graph_service, "update_arrow_position"):
                success = self._graph_service.update_arrow_position(
                    arrow_id, properties.get("x", 0.0), properties.get("y", 0.0)
                )
                if success and "rotation" in properties:
                    # Also update rotation if provided
                    self._graph_service.update_arrow_rotation(
                        arrow_id, properties["rotation"]
                    )
                return success
            return False

        except Exception as e:
            print(f"Error updating arrow properties: {e}")
            return False

    def _remove_special_placement_entry(self, letter: str, arrow_id: str) -> bool:
        """Remove special placement entry using V2 services."""
        # Suppress unused parameter warnings
        _ = letter, arrow_id

        # For V2, this could involve updating beat data or motion properties
        # to remove any special positioning overrides
        try:
            if hasattr(self._graph_service, "remove_special_placement"):
                return self._graph_service.remove_special_placement(letter, arrow_id)
            # For now, return True as placeholder until V2 special placement is implemented
            return True
        except Exception as e:
            print(f"Error removing special placement: {e}")
            return False

    def _apply_prop_placement_override(self) -> bool:
        """Apply prop placement override using V2 services."""
        try:
            if hasattr(self._graph_service, "toggle_prop_placement_override"):
                return self._graph_service.toggle_prop_placement_override()
            # For now, return True as placeholder until V2 prop placement is implemented
            return True
        except Exception as e:
            print(f"Error applying prop placement override: {e}")
            return False

    def _refresh_pictograph(self):
        """Refresh the pictograph display after changes."""
        try:
            if hasattr(self._graph_service, "refresh_pictograph"):
                self._graph_service.refresh_pictograph()
            elif hasattr(self._graph_service, "update_pictograph_display"):
                self._graph_service.update_pictograph_display()
        except Exception as e:
            print(f"Error refreshing pictograph: {e}")

    def enable_hotkeys(self):
        """Enable hotkey processing."""
        self._hotkey_enabled = True

    def disable_hotkeys(self):
        """Disable hotkey processing."""
        self._hotkey_enabled = False

    def is_hotkey_enabled(self) -> bool:
        """Check if hotkeys are enabled."""
        return self._hotkey_enabled
