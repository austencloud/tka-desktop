from ..base_classes.base_lesson_widget.base_lesson_widget import BaseLessonWidget
from .lesson_1_question_widget import Lesson1QuestionWidget
from .lesson_1_question_generator import Lesson1QuestionGenerator
from PyQt6.QtWidgets import QLabel


class Lesson1Widget(BaseLessonWidget):
    """Lesson 1 widget for handling letter to pictograph matching and quiz logic."""

    def __init__(self, learn_tab):
        super().__init__(
            learn_tab,
            lesson_type="Lesson1",
            question_type="pictograph",
            answer_type="button",
        )
        # self.question_widget = Lesson1QuestionWidget(self)
        self.question_generator = Lesson1QuestionGenerator(self)
        self.question_prompt = QLabel("Choose the letter for:")
        self.layout_manager.setup_layout()
