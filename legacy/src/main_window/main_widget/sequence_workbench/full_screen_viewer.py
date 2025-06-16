from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox

from main_window.main_widget.full_screen_image_overlay import (
    FullScreenImageOverlay,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_data_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class FullScreenViewer:
    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        self.sequence_workbench = sequence_workbench
        self.main_widget = sequence_workbench.main_widget
        self.beat_frame = sequence_workbench.beat_frame
        self.indicator_label = sequence_workbench.indicator_label
        self.json_loader = AppContext.json_manager().loader_saver

        self.full_screen_overlay = None

    def view_full_screen(self):
        """Display the current image in full screen mode."""
        mw = self.main_widget
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Get sequence length from UI state instead of JSON to ensure accuracy
        current_sequence = self._get_current_sequence_from_ui()
        sequence_length = len(current_sequence)

        if sequence_length <= 2:
            self.indicator_label.show_message("Please build a sequence first.")
            QApplication.restoreOverrideCursor()
            return
        else:
            current_thumbnail = self.create_thumbnail()
            if current_thumbnail:
                pixmap = QPixmap(current_thumbnail)

                # Use MainWidgetCoordinator pattern for widget access
                full_screen_overlay = None
                try:
                    # Try to get existing overlay using widget manager
                    if hasattr(mw, "get_widget"):
                        full_screen_overlay = mw.get_widget("full_screen_overlay")
                except (AttributeError, KeyError):
                    # Widget manager not available or overlay not found
                    pass

                if not full_screen_overlay:
                    # Create overlay if it doesn't exist
                    full_screen_overlay = FullScreenImageOverlay(mw)
                    # Store it for future use if the widget manager supports it
                    try:
                        if hasattr(mw, "widget_manager") and hasattr(
                            mw.widget_manager, "_widgets"
                        ):
                            mw.widget_manager._widgets["full_screen_overlay"] = (
                                full_screen_overlay
                            )
                    except (AttributeError, TypeError):
                        # Widget manager not available - overlay will still work
                        pass

                full_screen_overlay.show(pixmap)
                QApplication.restoreOverrideCursor()
            else:
                QMessageBox.warning(None, "No Image", "Please select an image first.")
                QApplication.restoreOverrideCursor()

    def create_thumbnail(self):
        self.thumbnail_generator = (
            self.sequence_workbench.dictionary_service.thumbnail_generator
        )
        # Get the current sequence from the UI state instead of the JSON file
        # This ensures we're showing what's currently displayed in the beat frame
        current_sequence = self._get_current_sequence_from_ui()
        temp_path = get_data_path("temp")
        image_path = self.thumbnail_generator.generate_and_save_thumbnail(
            current_sequence, 0, temp_path, fullscreen_preview=True
        )
        return image_path

    def _get_current_sequence_from_ui(self) -> list[dict]:
        """
        Get the current sequence from the beat frame UI state.

        This ensures the full-screen viewer shows exactly what's displayed
        in the beat frame, not what's saved in the JSON file.
        """
        try:
            # Get the sequence from the beat frame's current state
            beat_frame = self.beat_frame
            if not beat_frame:
                # Fallback to JSON if beat frame not available
                return self.json_loader.load_current_sequence()

            # Build sequence from current UI state
            sequence = []

            # Add the word entry (first entry) - get current word from beat frame
            current_word = ""
            if hasattr(beat_frame, "get") and hasattr(beat_frame.get, "current_word"):
                current_word = beat_frame.get.current_word()
            elif hasattr(self.sequence_workbench, "current_word_label") and hasattr(
                self.sequence_workbench.current_word_label, "current_word"
            ):
                current_word = (
                    self.sequence_workbench.current_word_label.current_word or ""
                )

            word_entry = {"word": current_word}
            sequence.append(word_entry)

            # Add start position if available
            if (
                hasattr(beat_frame, "start_pos_view")
                and beat_frame.start_pos_view
                and beat_frame.start_pos_view.is_filled
            ):
                start_pos = beat_frame.start_pos_view.start_pos
                if (
                    start_pos
                    and hasattr(start_pos, "state")
                    and hasattr(start_pos.state, "pictograph_data")
                ):
                    # Get the pictograph data from the start position beat
                    start_pos_data = start_pos.state.pictograph_data.copy()
                    # Ensure it's marked as a start position
                    start_pos_data["sequence_start_position"] = True
                    sequence.append(start_pos_data)

            # Add all filled beats from the UI
            if hasattr(beat_frame, "beat_views"):
                for beat_view in beat_frame.beat_views:
                    if beat_view and beat_view.is_filled and hasattr(beat_view, "beat"):
                        beat = beat_view.beat
                        if hasattr(beat, "state") and hasattr(
                            beat.state, "pictograph_data"
                        ):
                            # Get the pictograph data from the beat
                            beat_data = beat.state.pictograph_data.copy()
                            sequence.append(beat_data)

            return sequence

        except Exception as e:
            # Fallback to JSON if there's any error reading from UI
            print(
                f"Warning: Failed to read sequence from UI, falling back to JSON: {e}"
            )
            return self.json_loader.load_current_sequence()
