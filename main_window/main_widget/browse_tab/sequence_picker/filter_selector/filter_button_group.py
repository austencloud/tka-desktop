from typing import TYPE_CHECKING, Callable
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .initial_filter_choice_widget import InitialFilterChoiceWidget


class FilterButtonGroup(QWidget):
    """A group consisting of a button and its description label."""

    def __init__(
        self,
        label: str,
        description: str,
        handler: Callable,
        filter_choice_widget: "InitialFilterChoiceWidget",
    ):
        super().__init__()
        self.main_widget = filter_choice_widget.main_widget
        self.settings_manager = self.main_widget.settings_manager

        self.button = QPushButton(label)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(handler)

        self.description_label = QLabel(description)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Resize the button and description label dynamically."""
        button_font = QFont()
        button_font.setPointSize(self.main_widget.width() // 80)

        self.button.setFixedWidth(self.main_widget.width() // 7)
        self.button.setFixedHeight(self.main_widget.height() // 10)
        self.button.setFont(button_font)

        font_size = self.main_widget.width() // 150
        color = self.settings_manager.global_settings.get_current_font_color()
        self.description_label.setStyleSheet(
            f"font-size: {font_size}px; color: {color};"
        )
        super().resizeEvent(event)
