from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .initial_filter_choice_widget.initial_filter_choice_widget import InitialFilterChoiceWidget


class ChooseFilterLabel(QLabel):
    """Header label for the filter choice widget with automatic resize handling."""

    def __init__(self, filter_choice_widget: "InitialFilterChoiceWidget"):
        super().__init__("Choose a filter:")
        self.main_widget = filter_choice_widget.main_widget
        self.filter_choice_widget = filter_choice_widget
        self.settings_manager = self.main_widget.settings_manager
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Resize the header label's font dynamically."""
        font_size = self.main_widget.width() // 30
        font_family = "Monotype Corsiva"
        color = self.settings_manager.global_settings.get_current_font_color()

        self.setStyleSheet(
            f"font-size: {font_size}px; font-family: {font_family}; color: {color};"
        )
        super().resizeEvent(event)
