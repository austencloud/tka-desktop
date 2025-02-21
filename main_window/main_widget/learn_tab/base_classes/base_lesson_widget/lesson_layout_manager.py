# learn_tab/base_classes/base_lesson_widget/lesson_layout_manager.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .base_lesson_widget import BaseLessonWidget


class LessonLayoutManager:
    """
    Manages the layout of a BaseLessonWidget.
    This class handles the creation, refresh, and resizing of UI components.
    """

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        """
        :param lesson_widget: An instance of BaseLessonWidget.
        """
        self.lesson_widget = lesson_widget
        self.central_layout = QVBoxLayout()
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setup_layout(self):
        """
        Creates and sets up the overall layout for the lesson widget.
        """
        self.back_layout = self._create_back_layout()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.addLayout(self.back_layout)
        self.main_layout.addLayout(self.central_layout)
        self.lesson_widget.setLayout(self.main_layout)

    def _create_back_layout(self):
        """
        Creates a horizontal layout for the go-back button.
        """
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        back_layout.addWidget(self.lesson_widget.go_back_button)
        return back_layout

    def refresh_central_layout(self):
        """
        Clears and rebuilds the central layout with the progress, question,
        answers, and indicator widgets.
        """
        self._clear_stretches(self.central_layout)
        widgets = [
            self.lesson_widget.progress_label,
            self.lesson_widget.question_widget,
            self.lesson_widget.answers_widget,
            self.lesson_widget.indicator_label,
        ]
        for widget in widgets:
            self.central_layout.addWidget(widget)
            # Add a stretch between widgets for spacing
            self.central_layout.addStretch(1)

    def _clear_stretches(self, layout: QVBoxLayout) -> None:
        """
        Remove all spacer items from the layout.
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.spacerItem():
                layout.takeAt(i)
