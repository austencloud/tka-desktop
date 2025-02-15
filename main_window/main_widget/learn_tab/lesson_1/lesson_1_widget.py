from ..base_classes.base_lesson_widget.base_lesson_widget import BaseLessonWidget
from .lesson_1_question_widget import Lesson1QuestionWidget
from .lesson_1_answers_widget import Lesson1AnswersWidget
from .lesson_1_question_generator import Lesson1QuestionGenerator


class Lesson1Widget(BaseLessonWidget):
    """Lesson 1 widget for handling letter to pictograph matching and quiz logic."""

    def __init__(self, learn_widget):
        super().__init__(learn_widget)
        self.question_widget = Lesson1QuestionWidget(self)
        self.answers_widget = Lesson1AnswersWidget(self)
        self.question_generator = Lesson1QuestionGenerator(self)
        # self.prepare_quiz_ui()
