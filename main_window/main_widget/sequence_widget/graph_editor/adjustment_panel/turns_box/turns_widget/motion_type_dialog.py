from PyQt6.QtWidgets import QDialog, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING
from data.constants import ANTI, BLUE, FLOAT, HEX_BLUE, HEX_RED, PRO

if TYPE_CHECKING:
    from .motion_type_label_widget import MotionTypeLabelWidget


class MotionTypeDialog(QDialog):
    def __init__(self, label_widget: "MotionTypeLabelWidget") -> None:
        super().__init__(
            label_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.label_widget = label_widget
        self.turns_box = label_widget.turns_widget.turns_box
        self._set_dialog_style()

    def _set_dialog_style(self):
        """Apply consistent styling to the dialog."""
        self.setStyleSheet(
            f"""
            QDialog {{
                border: 2px solid {HEX_BLUE if self.turns_box.color == BLUE else HEX_RED};
                border-radius: 5px;
                background-color: white;
            }}
        """
        )

    def _setup_buttons(self):
        """Create and style the motion type buttons."""
        motion_types = [PRO, FLOAT, ANTI]
        layout = QHBoxLayout(self)

        for motion_type in motion_types:
            button = QPushButton(motion_type.capitalize(), self)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, mt=motion_type: self.set_motion_type(mt))
            layout.addWidget(button)

        self.setLayout(layout)
        self.adjust_button_styles()

    def adjust_button_styles(self):
        """Adjust the button styles based on the dialog size."""
        label_widget_height = self.label_widget.height()
        font_size = (
            label_widget_height
            // 2  # Adjust the font size relative to the dialog height
        )
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        border_size = label_widget_height // 20
        border_radius = border_size * 4
        for button in self.findChildren(QPushButton):
            button.setStyleSheet(
                f"""
                QPushButton {{
                    padding: 10px 20px;
                    border: {border_size}px solid {HEX_BLUE if self.turns_box.color == BLUE else HEX_RED};
                    border-radius: {border_radius}px;
                    background-color: #f8f8f8;
                }}
                QPushButton:hover {{
                    background-color: #e0e0e0;
                }}
            """
            )
            button.setFont(font)

    def set_motion_type(self, motion_type: str) -> None:
        """Set the selected motion type and close the dialog."""
        self.label_widget.set_motion_type(motion_type)
        self.accept()

    def show_motion_type_dialog(self) -> None:
        """Display the motion type dialog and position it above the label."""
        self._setup_buttons()
        self.adjustSize()

        # Positioning logic to show the dialog above the label
        label_rect = self.label_widget.label.geometry()
        global_label_pos = self.label_widget.label.mapToGlobal(
            self.label_widget.label.pos()
        )
        dialog_width = self.width()
        dialog_height = self.height()
        dialog_x = global_label_pos.x() + (label_rect.width() - dialog_width) / 2
        dialog_y = global_label_pos.y() - dialog_height
        self.move(int(dialog_x), int(dialog_y))

        self.exec()
