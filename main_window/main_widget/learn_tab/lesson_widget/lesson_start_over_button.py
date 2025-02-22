from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt



if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_widget.lesson_results_widget import LessonResultsWidget

class LessonStartOverButton(QPushButton):
    """Custom Start Over button with resize functionality."""

    def __init__(self, results_widget: "LessonResultsWidget"):
        super().__init__("Start Over")
        self.results_widget = results_widget
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def resizeEvent(self, event):
        font_size = self.results_widget.main_widget.width() // 60
        self.setStyleSheet(f"font-size: {font_size}px;")
        self.setFixedSize(
            self.results_widget.main_widget.width() // 8,
            self.results_widget.main_widget.height() // 12,
        )
