"""
Beat Number Overlay Component for Modern Beat Views

This component adds beat number text overlays directly to beat view widgets,
using the widget overlay approach that provides reliable visibility and
natural scene integration without visual styling artifacts.

Based on successful testing, this approach provides better compatibility
with Modern's architecture than scene-based text overlays.
"""

from typing import Optional
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class BeatNumberOverlay(QLabel):
    """
    Beat number overlay widget that displays beat numbers on beat views.

    Uses transparent widget overlay approach for reliable visibility
    and natural integration with the beat frame appearance.
    """

    def __init__(self, beat_number: int, parent_widget: Optional[QWidget] = None):
        super().__init__(str(beat_number), parent_widget)

        self.beat_number = beat_number
        self._setup_styling()
        self._setup_positioning()

        # Initially hidden until explicitly shown
        self.hide()

    def _setup_styling(self):
        """Setup the text styling to match Legacy's appearance exactly"""
        # Use the exact settings determined from successful testing
        self.setFont(QFont("Georgia", 10, QFont.Weight.DemiBold))

        # Transparent styling for natural scene integration
        self.setStyleSheet(
            """
            QLabel {
                color: black;
                background: transparent;
                border: none;
                padding: 0px;
            }
        """
        )

        # Ensure text alignment
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def _setup_positioning(self):
        """Setup the positioning and sizing based on successful test results"""
        # Use the exact dimensions determined from testing
        # Position: (10, 2), Size: 25x25
        self.setGeometry(10, 2, 25, 25)

    def show_beat_number(self):
        """Show the beat number overlay"""
        self.show()
        self.raise_()  # Bring to front to ensure visibility

    def hide_beat_number(self):
        """Hide the beat number overlay"""
        self.hide()

    def update_beat_number(self, new_number: int):
        """Update the displayed beat number"""
        self.beat_number = new_number
        self.setText(str(new_number))

    def update_position(self, x: int, y: int):
        """Update the overlay position"""
        current_geometry = self.geometry()
        self.setGeometry(x, y, current_geometry.width(), current_geometry.height())

    def update_size(self, width: int, height: int):
        """Update the overlay size"""
        current_geometry = self.geometry()
        self.setGeometry(current_geometry.x(), current_geometry.y(), width, height)

    def update_font_size(self, font_size: int):
        """Update the font size"""
        current_font = self.font()
        current_font.setPointSize(font_size)
        self.setFont(current_font)


def add_beat_number_to_view(
    beat_view: QWidget, beat_number: int
) -> Optional[BeatNumberOverlay]:
    """
    Add beat number overlay to a beat view widget.

    Args:
        beat_view: BeatView widget instance
        beat_number: The beat number to display (1, 2, 3, etc.)

    Returns:
        BeatNumberOverlay instance if successful, None otherwise
    """
    if not beat_view:
        return None

    try:
        # Create the beat number overlay
        beat_number_overlay = BeatNumberOverlay(beat_number, beat_view)
        beat_number_overlay.show_beat_number()

        # Store reference on the beat view to prevent garbage collection
        if not hasattr(beat_view, "_text_overlays"):
            beat_view._text_overlays = []
        beat_view._text_overlays.append(beat_number_overlay)

        return beat_number_overlay

    except Exception as e:
        print(f"Failed to add beat number overlay: {e}")
        return None


def remove_beat_number_from_view(
    beat_view: QWidget, beat_number_overlay: BeatNumberOverlay
):
    """
    Remove beat number overlay from a beat view widget.

    Args:
        beat_view: BeatView widget instance
        beat_number_overlay: BeatNumberOverlay instance to remove
    """
    if not beat_number_overlay:
        return

    try:
        # Remove from beat view's overlay list
        if (
            hasattr(beat_view, "_text_overlays")
            and beat_number_overlay in beat_view._text_overlays
        ):
            beat_view._text_overlays.remove(beat_number_overlay)

        # Hide and delete the overlay
        beat_number_overlay.hide_beat_number()
        beat_number_overlay.deleteLater()

    except Exception as e:
        print(f"Failed to remove beat number overlay: {e}")


def clear_all_beat_numbers_from_view(beat_view: QWidget):
    """
    Clear all beat number overlays from a beat view widget.

    Args:
        beat_view: BeatView widget instance
    """
    if not hasattr(beat_view, "_text_overlays"):
        return

    try:
        # Remove all beat number overlays
        for overlay in beat_view._text_overlays[
            :
        ]:  # Copy list to avoid modification during iteration
            if isinstance(overlay, BeatNumberOverlay):
                remove_beat_number_from_view(beat_view, overlay)

    except Exception as e:
        print(f"Failed to clear beat number overlays: {e}")
