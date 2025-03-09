from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..domain.turns_value import TurnsValue
from ..managers.turns_adjustment_manager import TurnsAdjustmentManager
from .turns_display_frame import TurnsDisplayFrame
from .dialogs.direct_set_turns_dialog import DirectSetTurnsDialog

if TYPE_CHECKING:
    from .turns_box import TurnsBox


class MotionTypeLabel(QLabel):
    """Label displaying the current motion type"""

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__("", turns_widget)
        self.turns_widget = turns_widget
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_display(self, motion_type: str) -> None:
        """Update the display with new motion type"""
        self.setText(motion_type.capitalize())

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        # Update font size based on parent dimensions
        font_size = self.turns_widget.turns_box.graph_editor.width() // 40
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        self.setFont(font)


class TurnsTextLabel(QLabel):
    """Label for the "Turns" heading"""

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__("Turns", turns_widget)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_widget = turns_widget

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        # Update font size based on parent dimensions
        font_size = self.turns_widget.turns_box.graph_editor.width() // 50
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.setFont(font)
        super().resizeEvent(event)


class TurnsWidget(QWidget):
    """Widget containing turns adjustment controls and displays"""

    turns_adjusted = pyqtSignal()

    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box

        # Setup
        self._setup_components()
        self._setup_layout()
        self._connect_signals()

    def _setup_components(self) -> None:
        """Initialize components"""
        # Create turns adjustment manager
        self.adjustment_manager = TurnsAdjustmentManager(self, self.turns_box.color)

        # Create turns display frame
        self.display_frame = TurnsDisplayFrame(self)

        # Create labels
        self.turns_text = TurnsTextLabel(self)
        self.motion_type_label = MotionTypeLabel(self)

        # Create direct set dialog
        self.direct_set_dialog = DirectSetTurnsDialog(self)

        # Initialize with current motion
        current_motion = self._get_current_motion()
        if current_motion:
            self.adjustment_manager.set_current_motion(current_motion)

            # Connect to pictograph selection signal
            self.turns_box.graph_editor.pictograph_selected.connect(
                self._on_pictograph_selected
            )

    def _setup_layout(self) -> None:
        """Set up widget layout"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.turns_text, 1)
        layout.addWidget(self.display_frame, 3)
        layout.addWidget(self.motion_type_label, 1)
        layout.setContentsMargins(5, 5, 5, 5)

    def _connect_signals(self) -> None:
        """Connect signals to slots"""
        self.adjustment_manager.turns_changed.connect(self._on_turns_changed)

    def _on_turns_changed(self, turns_value: TurnsValue) -> None:
        """Handle turns value changes"""
        # Notify external components
        self.turns_adjusted.emit()

        # Update image export preview if available
        settings_dialog = (
            self.turns_box.adjustment_panel.graph_editor.main_widget.settings_dialog
        )
        if hasattr(settings_dialog, "ui") and hasattr(
            settings_dialog.ui, "image_export_tab"
        ):
            settings_dialog.ui.image_export_tab.update_preview()

    def _on_pictograph_selected(self) -> None:
        """Handle pictograph selection"""
        current_motion = self._get_current_motion()
        if current_motion:
            self.adjustment_manager.set_current_motion(current_motion)

    def _get_current_motion(self):
        """Get current motion based on selected pictograph"""
        try:
            current_beat = (
                self.turns_box.graph_editor.pictograph_container.GE_view.pictograph
            )
            return current_beat.elements.motion_set[self.turns_box.color]
        except (AttributeError, KeyError) as e:
            print(f"Error getting current motion: {e}")
            return None

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        # Propagate resize event
        self.display_frame.resizeEvent(event)
        self.turns_text.resizeEvent(event)
        self.motion_type_label.resizeEvent(event)
        super().resizeEvent(event)
