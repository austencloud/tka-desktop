from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

from main_window.main_widget.learn_tab.base_classes.base_question_widget import (
    BaseQuestionWidget,
)

if TYPE_CHECKING:
    from .lesson_2_widget import Lesson2Widget


class Lesson2QuestionWidget(BaseQuestionWidget):
    """Widget responsible for displaying the question in Lesson 2."""

    def __init__(self, lesson_2_widget: "Lesson2Widget") -> None:
        super().__init__(lesson_2_widget)
        self.lesson_widget = lesson_2_widget
        self.main_widget = lesson_2_widget.main_widget
        self._setup_labels()
        self._setup_layout()

    def _setup_labels(self) -> None:

        self.letter_label = QLabel()
        self.letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.layout.addItem(self.spacer)
        self.layout.addWidget(self.letter_label)

    def _update_letter_label(self, letter: str) -> None:
        """Display the question prompt and the letter to be matched."""
        self.letter_label.setText(letter)

    def clear(self) -> None:
        """Clear the question display."""
        self.letter_label.clear()

    def resizeEvent(self, event) -> None:
        """Resize the question labels based on window size."""
        super().resizeEvent(event)
        self._resize_letter_label()
        self._resize_spacer()

    def _resize_letter_label(self):
        letter_label_font_size = self.main_widget.width() // 40
        letter_label_font = self.letter_label.font()
        letter_label_font.setFamily("Georgia")
        letter_label_font.setPointSize(letter_label_font_size)
        self.letter_label.setFont(letter_label_font)
