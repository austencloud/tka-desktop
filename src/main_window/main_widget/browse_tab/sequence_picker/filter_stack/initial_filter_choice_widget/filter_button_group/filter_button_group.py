from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtCore import Qt

from main_window.main_widget.browse_tab.sequence_picker.filter_stack.initial_filter_choice_widget.filter_button_group.filter_button import (
    FilterButton,
)

if TYPE_CHECKING:
    from ..initial_filter_choice_widget import InitialFilterChoiceWidget


class FilterButtonGroup(QWidget):
    """A group consisting of a button and its description label."""

    def __init__(
        self,
        label: str,
        description: str,
        handler: callable,
        filter_choice_widget: "InitialFilterChoiceWidget",
    ):
        super().__init__()
        self.main_widget = filter_choice_widget.main_widget
        self.settings_manager = self.main_widget.settings_manager

        self.button = FilterButton(label)
        self.button.clicked.connect(handler)

        self.description_label = QLabel(description)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def resizeEvent(self, event: QResizeEvent) -> None:
        button_font = QFont()
        button_font.setPointSize(self.main_widget.width() // 80)

        button_width = self.main_widget.width() // 7
        button_height = self.main_widget.height() // 10
        # border_radius = min(button_width, button_height) // 4

        self.button.setFixedSize(button_width, button_height)
        self.button.setFont(button_font)
        # self.button.set_rounded_button_style(border_radius)

        font_size = self.main_widget.width() // 150
        color = self.settings_manager.global_settings.get_current_font_color()
        self.description_label.setStyleSheet(
            f"font-size: {font_size}px; color: {color};"
        )

        super().resizeEvent(event)
