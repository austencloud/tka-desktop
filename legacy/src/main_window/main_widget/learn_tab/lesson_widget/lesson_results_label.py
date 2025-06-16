from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_widget.lesson_results_widget import (
        LessonResultsWidget,
    )


class LessonResultLabel(QLabel):
    def __init__(self, results_widget: "LessonResultsWidget"):
        super().__init__(results_widget)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_widget = results_widget
        self.lesson_widget = results_widget.learn_tab

    def resizeEvent(self, event):
        font_size = self.lesson_widget.main_widget.width() // 60
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)
