"""
Turn Selection Dialog for Graph Editor

This dialog provides a modal interface for selecting turn values for arrows,
matching Legacy's turn selection behavior with 7 turn value options.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont


class TurnSelectionDialog(QDialog):
    """Modal dialog for selecting turn values, matching Legacy behavior."""

    turn_selected = pyqtSignal(float)  # Emitted when user selects a turn value

    def __init__(
        self, parent=None, current_turn: float = 0.0, arrow_color: str = "blue"
    ):
        super().__init__(parent)
        self._current_turn = current_turn
        self._arrow_color = arrow_color
        self._selected_turn: Optional[float] = None

        self._setup_ui()
        self._setup_styling()

    def _setup_ui(self):
        """Set up the dialog UI with turn value buttons."""
        self.setWindowTitle("Select Turn Value")
        self.setModal(True)
        self.setFixedSize(420, 120)

        # Remove window frame for custom styling
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header
        header = QLabel(f"Select Turn Value for {self._arrow_color.title()} Arrow")
        header.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: white; padding: 4px;")
        layout.addWidget(header)

        # Turn value buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(4)

        self._turn_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        self._turn_buttons = []

        for turn_value in self._turn_values:
            btn = QPushButton(str(turn_value))
            btn.setFixedSize(50, 40)
            btn.clicked.connect(
                lambda checked=False, val=turn_value: self._on_turn_selected(val)
            )

            # Highlight current turn value
            if abs(turn_value - self._current_turn) < 0.01:
                btn.setProperty("current", True)

            self._turn_buttons.append(btn)
            buttons_layout.addWidget(btn)

        layout.addLayout(buttons_layout)

        # Cancel button
        cancel_layout = QHBoxLayout()
        cancel_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(60, 30)
        cancel_btn.clicked.connect(self.reject)
        cancel_layout.addWidget(cancel_btn)

        layout.addLayout(cancel_layout)

    def _setup_styling(self):
        """Apply Legacy-matching styling to the dialog."""
        color_rgb = "100, 150, 255" if self._arrow_color == "blue" else "255, 100, 100"

        self.setStyleSheet(
            f"""
            TurnSelectionDialog {{
                background-color: rgba(30, 30, 30, 0.95);
                border: 2px solid rgba({color_rgb}, 0.6);
                border-radius: 8px;
            }}
            
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: rgba({color_rgb}, 0.3);
                border-color: rgba({color_rgb}, 0.6);
            }}
            
            QPushButton:pressed {{
                background-color: rgba({color_rgb}, 0.5);
            }}
            
            QPushButton[current="true"] {{
                background-color: rgba({color_rgb}, 0.4);
                border-color: rgba({color_rgb}, 0.8);
                border-width: 2px;
            }}
        """
        )

    def _on_turn_selected(self, turn_value: float):
        """Handle turn value selection."""
        self._selected_turn = turn_value
        self.turn_selected.emit(turn_value)
        self.accept()

    def get_selected_turn(self) -> Optional[float]:
        """Get the selected turn value."""
        return self._selected_turn

    @staticmethod
    def get_turn_value(
        parent=None, current_turn: float = 0.0, arrow_color: str = "blue", position=None
    ) -> Optional[float]:
        """
        Static method to show dialog and get turn value.

        Args:
            parent: Parent widget
            current_turn: Current turn value to highlight
            arrow_color: Arrow color for styling
            position: QPoint for dialog positioning (near clicked widget)

        Returns:
            Selected turn value or None if cancelled
        """
        dialog = TurnSelectionDialog(parent, current_turn, arrow_color)

        # Position dialog near the clicked widget if position provided
        if position:
            # Offset slightly so dialog doesn't cover the clicked widget
            x = position.x() - dialog.width() // 2
            y = position.y() - dialog.height() - 10  # 10px above the widget
            dialog.move(x, y)
        elif parent:
            # Fallback to centering on parent
            parent_rect = parent.geometry()
            dialog_rect = dialog.geometry()

            x = parent_rect.x() + (parent_rect.width() - dialog_rect.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - dialog_rect.height()) // 2

            dialog.move(x, y)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_selected_turn()
        return None

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        elif event.key() >= Qt.Key.Key_0 and event.key() <= Qt.Key.Key_3:
            # Quick selection with number keys
            index = event.key() - Qt.Key.Key_0
            if index < len(self._turn_values):
                self._on_turn_selected(self._turn_values[index])
        else:
            super().keyPressEvent(event)
