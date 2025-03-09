


# === turns_box/ui/dialogs/direct_set_turns_dialog.py ===
from typing import TYPE_CHECKING, Dict
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from data.constants import ANTI, BLUE, FLOAT, HEX_BLUE, HEX_RED, PRO
from ...domain.turns_value import TurnsValue

if TYPE_CHECKING:
    from ..turns_widget import TurnsWidget


class DirectSetTurnsButton(QPushButton):
    """Button for directly setting a specific turns value"""

    def __init__(self, value: str, direct_set_dialog: "DirectSetTurnsDialog") -> None:
        super().__init__(value)
        self.direct_set_dialog = direct_set_dialog
        self.turns_widget = direct_set_dialog.turns_widget
        self.turns_box = self.turns_widget.turns_box

        # Connect signals
        self.clicked.connect(self._on_clicked)

        # Setup
        self.setMouseTracking(True)

    def _on_clicked(self) -> None:
        """Handle button clicks"""
        value_text = self.text()

        # Convert value to appropriate type
        if value_text == "fl":
            turns_value = TurnsValue("fl")
        elif "." in value_text:
            turns_value = TurnsValue(float(value_text))
        else:
            turns_value = TurnsValue(int(value_text))

        # Apply the value
        self.turns_widget.adjustment_manager.direct_set(turns_value)

        # Close dialog
        self.direct_set_dialog.accept()

    def enterEvent(self, event) -> None:
        """Handle mouse enter events"""
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event) -> None:
        """Handle mouse leave events"""
        QApplication.restoreOverrideCursor()

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        super().resizeEvent(event)

        # Calculate sizes based on parent dimensions
        button_size = self.turns_box.height() // 2
        font_size = int(self.turns_box.adjustment_panel.graph_editor.height() / 6)

        # Get color based on turns box color
        color_hex = HEX_BLUE if self.turns_box.color == BLUE else HEX_RED

        # Apply styles
        self.setFixedSize(QSize(button_size, button_size))
        self.setFont(QFont("Arial", font_size, QFont.Weight.Bold))
        self.setStyleSheet(
            f"""
            QPushButton {{
                border: 4px solid {color_hex};
                border-radius: {button_size // 2}px;
                background-color: white;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
            """
        )


class DirectSetTurnsDialog(QDialog):
    """Dialog for directly setting turns to a specific value"""

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(
            turns_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.turns_display_frame = turns_widget.display_frame
        self.adjustment_manager = turns_widget.adjustment_manager
        self.buttons: Dict[str, DirectSetTurnsButton] = {}

        # Setup
        self._set_dialog_style()
        self._setup_buttons()
        self._setup_layout()

    def _set_dialog_style(self) -> None:
        """Set dialog appearance"""
        # Get color based on turns box color
        border_color = HEX_BLUE if self.turns_box.color == BLUE else HEX_RED

        # Apply styles
        self.setStyleSheet(
            f"""
            QDialog {{
                border: 2px solid {border_color};
                border-radius: 5px;
            }}
            """
        )

    def _setup_buttons(self) -> None:
        """Create value buttons"""
        # Define available turns values
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]

        # Add 'fl' for certain motion types
        motion = self.turns_box.matching_motion
        if motion and motion.state.motion_type in [PRO, ANTI, FLOAT]:
            turns_values.insert(0, "fl")

        # Create buttons
        for value in turns_values:
            button = DirectSetTurnsButton(value, self)
            self.buttons[value] = button

    def _setup_layout(self) -> None:
        """Set up dialog layout"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add buttons to layout
        for button in self.buttons.values():
            layout.addWidget(button)

        self.adjustSize()

    def show_direct_set_dialog(self) -> None:
        """Show the dialog at appropriate position"""
        # Resize buttons
        self.resize_direct_set_buttons()

        # Calculate position
        turns_label_rect = self.turns_display_frame.turns_label.geometry()
        global_turns_label_pos = self.turns_display_frame.turns_label.mapToGlobal(
            self.turns_display_frame.turns_label.pos()
        )
        turns_widget_pos = self.turns_widget.mapToGlobal(self.turns_widget.pos())

        # Position dialog under the turns label
        dialog_x = turns_widget_pos.x()
        dialog_y = global_turns_label_pos.y() + turns_label_rect.height()

        # Show dialog
        self.move(int(dialog_x), int(dialog_y))
        self.exec()

    def resize_direct_set_buttons(self) -> None:
        """Resize buttons to match current UI scale"""
        self.adjustSize()
        self.updateGeometry()
