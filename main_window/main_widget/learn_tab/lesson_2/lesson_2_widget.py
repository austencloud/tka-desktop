from ..base_classes.base_lesson_widget.base_lesson_widget import BaseLessonWidget
from .lesson_2_question_widget import Lesson2QuestionWidget
from .lesson_2_question_generator import Lesson2QuestionGenerator
from PyQt6.QtWidgets import QLabel


class Lesson2Widget(BaseLessonWidget):
    """Lesson 2 widget for handling letter to pictograph matching and quiz logic."""

    def __init__(self, learn_tab):
        super().__init__(
            learn_tab,
            lesson_type="Lesson2",
            question_type="letter",
            answer_type="pictograph",
        )

        # self.question_widget = Lesson2QuestionWidget(self)
        self.question_generator = Lesson2QuestionGenerator(self)
        self.question_prompt = QLabel("Choose the pictograph for:")

        self.layout_manager.setup_layout()
