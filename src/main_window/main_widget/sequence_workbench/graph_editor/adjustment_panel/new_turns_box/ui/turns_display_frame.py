# === turns_box/ui/turns_display_frame.py ===
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from data.constants import ANTI, FLOAT, PRO, BLUE, RED
from objects.motion.motion import Motion
from .buttons.adjust_turns_button import AdjustTurnsButton
from utils.path_helpers import get_image_path

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget


class TurnsLabel(QLabel):
    """Label displaying the current turns value"""

    clicked = pyqtSignal()

    def __init__(self, turns_display_frame: "TurnsDisplayFrame") -> None:
        super().__init__()
        self.turns_display_frame = turns_display_frame
        self.turns_box = turns_display_frame.turns_box

        # Setup
        self.turns_display_font_size = 20
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event) -> None:
        """Handle mouse press events"""
        super().mousePressEvent(event)
        self.clicked.emit()

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        # Update font size based on parent dimensions
        self.turns_display_font_size = int(
            (self.turns_box.adjustment_panel.graph_editor.width() / 22)
        )
        self.setFont(QFont("Arial", self.turns_display_font_size, QFont.Weight.Bold))

        # Set maximum dimensions
        self.setMaximumWidth(
            int(self.turns_box.adjustment_panel.graph_editor.width() / 9)
        )
        self.setMaximumHeight(
            int(self.turns_box.adjustment_panel.graph_editor.height() / 4)
        )

        # Calculate styles
        border_radius = self.width() // 4
        turn_display_border = int(self.width() / 20)

        # Get color based on turns box color
        turns_box_color = self.turns_box.color
        border_color = (
            "#ED1C24"
            if turns_box_color == RED
            else "#2E3192" if turns_box_color == BLUE else "black"
        )

        # Apply styles
        self.setStyleSheet(
            f"""
            QLabel {{
                border: {turn_display_border}px solid {border_color};
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px;
                padding-right: 2px;
            }}
            """
        )

        super().resizeEvent(event)


class TurnsDisplayFrame(QFrame):
    """Frame containing turns display and adjustment buttons"""

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.adjustment_manager = turns_widget.adjustment_manager

        # Setup
        self._setup_components()
        self._attach_listeners()
        self._setup_layout()

    def _setup_components(self) -> None:
        """Initialize components"""
        # Create adjustment buttons
        plus_path = get_image_path("icons/plus.svg")
        minus_path = get_image_path("icons/minus.svg")
        self.increment_button = AdjustTurnsButton(plus_path, self.turns_widget)
        self.decrement_button = AdjustTurnsButton(minus_path, self.turns_widget)

        # Create turns label
        self.turns_label = TurnsLabel(self)

    def _setup_layout(self) -> None:
        """Set up widget layout"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.decrement_button, 1)
        layout.addWidget(self.turns_label, 2)
        layout.addWidget(self.increment_button, 1)

    def _attach_listeners(self) -> None:
        """Connect signals to slots"""
        # Connect adjustment buttons
        self.increment_button.clicked.connect(lambda: self.adjustment_manager.adjust(1))
        self.decrement_button.clicked.connect(
            lambda: self.adjustment_manager.adjust(-1)
        )

        # Connect context menu for half-turn adjustments
        self.decrement_button.customContextMenuRequested.connect(
            lambda: self.adjustment_manager.adjust(-0.5)
        )
        self.increment_button.customContextMenuRequested.connect(
            lambda: self.adjustment_manager.adjust(0.5)
        )

        # Connect turns label
        self.turns_label.clicked.connect(self._on_turns_label_clicked)

    def _on_turns_label_clicked(self) -> None:
        """Handle turns label clicks"""
        self.turns_widget.direct_set_dialog.show_direct_set_dialog()

    def update_turns_display(self, motion: "Motion", display_value: str) -> None:
        """Update the display with new turns value"""
        # Update motion reference
        self.turns_box.matching_motion = motion

        # Update label text
        self.turns_label.setText(str(display_value))

        # Update button states
        is_float_or_zero = display_value == "fl" or display_value == "0"

        # Disable decrement if at minimum or special case
        if motion.state.motion_type in [PRO, ANTI, FLOAT]:
            self.decrement_button.setEnabled(display_value != "fl")
        else:
            self.decrement_button.setEnabled(display_value != "0")

        # Disable increment if at maximum
        self.increment_button.setEnabled(display_value != "3")

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        # Propagate resize event
        self.turns_label.resizeEvent(event)
        self.increment_button.resizeEvent(event)
        self.decrement_button.resizeEvent(event)
        return super().resizeEvent(event)
