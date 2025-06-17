"""
Beat Selection Manager

Manages beat selection state and visual feedback in the sequence workbench,
replacing Legacy's BeatSelectionOverlay with modern state management patterns.
"""

from typing import Optional, List, Callable
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent

from .beat_view import BeatView


class BeatSelectionManager(QObject):
    """
    Manages beat selection state and keyboard navigation.

    Replaces Legacy's BeatSelectionOverlay with:
    - Clean state management
    - Keyboard navigation support
    - Multi-selection capabilities (future)
    - Accessibility features
    """

    # Signals
    selection_changed = pyqtSignal(object)  # Optional[int] - beat index or None
    selection_cleared = pyqtSignal()
    multiple_selection_changed = pyqtSignal(list)  # List[int] - beat indices

    def __init__(self, parent_widget: QWidget):
        super().__init__(parent_widget)

        self._parent_widget = parent_widget
        self._beat_views: List[BeatView] = []
        self._selected_index: Optional[int] = None
        self._selected_indices: List[int] = []  # For future multi-selection
        self._multi_selection_enabled = False

        # Keyboard navigation
        self._keyboard_navigation_enabled = True
        self._parent_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._parent_widget.keyPressEvent = self._handle_key_press

    def register_beat_views(self, beat_views: List[BeatView]):
        """Register beat views for selection management"""
        self._beat_views = beat_views

        # Connect signals from beat views
        for i, beat_view in enumerate(beat_views):
            beat_view.beat_clicked.connect(lambda idx=i: self.select_beat(idx))

    def select_beat(self, beat_index: int):
        """Select a specific beat"""
        if not self._is_valid_index(beat_index):
            return

        # Clear previous selection
        self._clear_visual_selection()

        # Set new selection
        self._selected_index = beat_index
        self._selected_indices = [beat_index]

        # Update visual state
        self._update_visual_selection()

        # Emit signals
        self.selection_changed.emit(beat_index)

    def clear_selection(self):
        """Clear all selections"""
        self._clear_visual_selection()

        self._selected_index = None
        self._selected_indices = []

        self.selection_cleared.emit()
        self.selection_changed.emit(None)

    def get_selected_index(self) -> Optional[int]:
        """Get the currently selected beat index"""
        return self._selected_index

    def get_selected_indices(self) -> List[int]:
        """Get all selected beat indices (for multi-selection)"""
        return self._selected_indices.copy()

    def is_beat_selected(self, beat_index: int) -> bool:
        """Check if a specific beat is selected"""
        return beat_index in self._selected_indices

    def set_multi_selection_enabled(self, enabled: bool):
        """Enable or disable multi-selection mode"""
        self._multi_selection_enabled = enabled
        if not enabled and len(self._selected_indices) > 1:
            # Keep only the first selection
            if self._selected_indices:
                self.select_beat(self._selected_indices[0])
            else:
                self.clear_selection()

    def add_to_selection(self, beat_index: int):
        """Add a beat to the current selection (multi-selection mode)"""
        if not self._multi_selection_enabled or not self._is_valid_index(beat_index):
            return

        if beat_index not in self._selected_indices:
            self._selected_indices.append(beat_index)

            # Update visual state
            if beat_index < len(self._beat_views):
                self._beat_views[beat_index].set_selected(True)

            # Update primary selection if this is the first
            if self._selected_index is None:
                self._selected_index = beat_index

            self.multiple_selection_changed.emit(self._selected_indices)
            self.selection_changed.emit(self._selected_index)

    def remove_from_selection(self, beat_index: int):
        """Remove a beat from the current selection"""
        if beat_index in self._selected_indices:
            self._selected_indices.remove(beat_index)

            # Update visual state
            if beat_index < len(self._beat_views):
                self._beat_views[beat_index].set_selected(False)

            # Update primary selection
            if self._selected_index == beat_index:
                self._selected_index = (
                    self._selected_indices[0] if self._selected_indices else None
                )

            self.multiple_selection_changed.emit(self._selected_indices)
            self.selection_changed.emit(self._selected_index)

    def select_next_beat(self):
        """Select the next beat (keyboard navigation)"""
        if not self._keyboard_navigation_enabled:
            return

        if self._selected_index is None:
            # Select first beat
            if self._beat_views:
                self.select_beat(0)
        else:
            # Select next beat
            next_index = self._selected_index + 1
            if next_index < len(self._beat_views):
                self.select_beat(next_index)

    def select_previous_beat(self):
        """Select the previous beat (keyboard navigation)"""
        if not self._keyboard_navigation_enabled:
            return

        if self._selected_index is None:
            # Select last beat
            if self._beat_views:
                self.select_beat(len(self._beat_views) - 1)
        else:
            # Select previous beat
            prev_index = self._selected_index - 1
            if prev_index >= 0:
                self.select_beat(prev_index)

    def select_beat_in_direction(self, direction: str, layout_columns: int):
        """Select beat in a specific direction (up, down, left, right)"""
        if not self._keyboard_navigation_enabled or self._selected_index is None:
            return

        current_row = self._selected_index // layout_columns
        current_col = self._selected_index % layout_columns

        new_row, new_col = current_row, current_col

        if direction == "up":
            new_row = max(0, current_row - 1)
        elif direction == "down":
            new_row = current_row + 1
        elif direction == "left":
            new_col = max(0, current_col - 1)
        elif direction == "right":
            new_col = current_col + 1

        new_index = new_row * layout_columns + new_col

        if self._is_valid_index(new_index):
            self.select_beat(new_index)

    def set_keyboard_navigation_enabled(self, enabled: bool):
        """Enable or disable keyboard navigation"""
        self._keyboard_navigation_enabled = enabled

    def focus_selected_beat(self):
        """Set focus to the currently selected beat"""
        if self._selected_index is not None and self._selected_index < len(
            self._beat_views
        ):
            self._beat_views[self._selected_index].setFocus()

    # Private methods
    def _is_valid_index(self, beat_index: int) -> bool:
        """Check if beat index is valid"""
        return 0 <= beat_index < len(self._beat_views)

    def _clear_visual_selection(self):
        """Clear visual selection from all beat views"""
        for beat_view in self._beat_views:
            beat_view.set_selected(False)

    def _update_visual_selection(self):
        """Update visual selection state"""
        for i, beat_view in enumerate(self._beat_views):
            beat_view.set_selected(i in self._selected_indices)

    def _handle_key_press(self, event: QKeyEvent):
        """Handle keyboard events for navigation"""
        if not self._keyboard_navigation_enabled:
            return

        key = event.key()
        modifiers = event.modifiers()

        # Basic navigation
        if key == Qt.Key.Key_Right:
            self.select_next_beat()
            event.accept()
        elif key == Qt.Key.Key_Left:
            self.select_previous_beat()
            event.accept()
        elif key == Qt.Key.Key_Up:
            # Need layout info for up/down navigation
            # This would be provided by the beat frame
            pass
        elif key == Qt.Key.Key_Down:
            # Need layout info for up/down navigation
            pass
        elif key == Qt.Key.Key_Home:
            if self._beat_views:
                self.select_beat(0)
            event.accept()
        elif key == Qt.Key.Key_End:
            if self._beat_views:
                self.select_beat(len(self._beat_views) - 1)
            event.accept()
        elif key == Qt.Key.Key_Escape:
            self.clear_selection()
            event.accept()

        # Multi-selection with Ctrl
        elif modifiers & Qt.KeyboardModifier.ControlModifier:
            if key == Qt.Key.Key_A:
                # Select all (if multi-selection enabled)
                if self._multi_selection_enabled:
                    self._select_all_beats()
                event.accept()

    def _select_all_beats(self):
        """Select all beats (multi-selection mode)"""
        if not self._multi_selection_enabled:
            return

        self._selected_indices = list(range(len(self._beat_views)))
        self._selected_index = 0 if self._beat_views else None

        self._update_visual_selection()

        self.multiple_selection_changed.emit(self._selected_indices)
        self.selection_changed.emit(self._selected_index)

    # Accessibility support
    def announce_selection(self, beat_index: int):
        """Announce selection change for screen readers"""
        if beat_index < len(self._beat_views):
            beat_view = self._beat_views[beat_index]
            beat_data = beat_view.get_beat_data()

            if beat_data:
                announcement = f"Selected beat {beat_view.get_beat_number()}, letter {beat_data.letter}"
            else:
                announcement = f"Selected empty beat slot {beat_view.get_beat_number()}"

            # TODO: Integrate with accessibility service for screen reader announcements
            print(f"Accessibility: {announcement}")  # Placeholder

    def get_selection_summary(self) -> str:
        """Get a summary of current selection for accessibility"""
        if not self._selected_indices:
            return "No beats selected"
        elif len(self._selected_indices) == 1:
            beat_num = self._selected_indices[0] + 1
            return f"Beat {beat_num} selected"
        else:
            return f"{len(self._selected_indices)} beats selected"
