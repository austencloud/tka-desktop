"""
Start Text Widget Overlay Component for Modern Start Position Views

This component adds "Start" text overlays directly to start position view widgets,
using the widget overlay approach that provides reliable visibility and
natural scene integration without visual styling artifacts.

Based on successful testing, this approach provides better compatibility
with Modern's architecture than scene-based text overlays.
"""

from typing import Optional
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class StartTextWidgetOverlay(QLabel):
    """
    Start text overlay widget that displays "Start" text on start position views.

    Uses transparent widget overlay approach for reliable visibility
    and natural integration with the start position appearance.
    """

    def __init__(self, parent_widget: Optional[QWidget] = None):
        super().__init__("Start", parent_widget)  # Use "Start" not "START" like Legacy

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
        # Position: (10, 2), Size: 60x30
        self.setGeometry(10, 2, 60, 30)

    def show_start_text(self):
        """Show the start text overlay"""
        self.show()
        self.raise_()  # Bring to front to ensure visibility

    def hide_start_text(self):
        """Hide the start text overlay"""
        self.hide()

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


def add_start_text_to_view(
    start_position_view: QWidget,
) -> Optional[StartTextWidgetOverlay]:
    """
    Add start text overlay to a start position view widget.

    Args:
        start_position_view: StartPositionView widget instance

    Returns:
        StartTextWidgetOverlay instance if successful, None otherwise
    """
    if not start_position_view:
        return None

    try:
        # Create the start text overlay
        start_text_overlay = StartTextWidgetOverlay(start_position_view)
        start_text_overlay.show_start_text()

        # Store reference on the start position view to prevent garbage collection
        if not hasattr(start_position_view, "_text_overlays"):
            start_position_view._text_overlays = []
        start_position_view._text_overlays.append(start_text_overlay)

        return start_text_overlay

    except Exception as e:
        print(f"Failed to add start text overlay: {e}")
        return None


def remove_start_text_from_view(
    start_position_view: QWidget, start_text_overlay: StartTextWidgetOverlay
):
    """
    Remove start text overlay from a start position view widget.

    Args:
        start_position_view: StartPositionView widget instance
        start_text_overlay: StartTextWidgetOverlay instance to remove
    """
    if not start_text_overlay:
        return

    try:
        # Remove from start position view's overlay list
        if (
            hasattr(start_position_view, "_text_overlays")
            and start_text_overlay in start_position_view._text_overlays
        ):
            start_position_view._text_overlays.remove(start_text_overlay)

        # Hide and delete the overlay
        start_text_overlay.hide_start_text()
        start_text_overlay.deleteLater()

    except Exception as e:
        print(f"Failed to remove start text overlay: {e}")


def clear_all_start_text_from_view(start_position_view: QWidget):
    """
    Clear all start text overlays from a start position view widget.

    Args:
        start_position_view: StartPositionView widget instance
    """
    if not hasattr(start_position_view, "_text_overlays"):
        return

    try:
        # Remove all start text overlays
        for overlay in start_position_view._text_overlays[
            :
        ]:  # Copy list to avoid modification during iteration
            if isinstance(overlay, StartTextWidgetOverlay):
                remove_start_text_from_view(start_position_view, overlay)

    except Exception as e:
        print(f"Failed to clear start text overlays: {e}")
