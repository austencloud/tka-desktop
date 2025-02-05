from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .lesson_answer_checker import LessonAnswerChecker
from .lesson_go_back_button import LessonGoBackButton
from .lesson_progress_label import LessonProgressLabel
from .lesson_indicator_label import LessonIndicatorLabel
from ..base_answers_widget import BaseAnswersWidget
from .lesson_quiz_timer_manager import QuizTimerManager
from ..base_question_generator import BaseQuestionGenerator
from ..base_question_widget import BaseQuestionWidget

if TYPE_CHECKING:
    from ...learn_tab import LearnTab


class BaseLessonWidget(QWidget):

    question_generator: BaseQuestionGenerator = None
    question_widget: BaseQuestionWidget = None
    answers_widget: BaseAnswersWidget = None
    total_questions = 30
    current_question = 1
    quiz_time = 120
    mode = "fixed_question"
    incorrect_guesses = 0

    def __init__(self, learn_tab: "LearnTab"):
        super().__init__(learn_tab)
        self.learn_tab = learn_tab
        self.main_widget = learn_tab.main_widget
        self.fade_manager = self.main_widget.fade_manager

        self.timer_manager = QuizTimerManager(self)
        self.indicator_label = LessonIndicatorLabel(self)
        self.go_back_button = LessonGoBackButton(self)
        self.progress_label = LessonProgressLabel(self)
        self.answer_checker = LessonAnswerChecker(self)

        self._setup_layout()

    def _setup_layout(self):
        self.central_layout = QVBoxLayout()

        self.back_layout = QHBoxLayout()
        self.back_layout.addWidget(self.go_back_button)
        self.back_layout.addStretch(1)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.back_layout, 0)
        self.main_layout.addLayout(self.central_layout)

        self.setLayout(self.main_layout)

    def update_progress_label(self):
        self.progress_label.setText(f"{self.current_question}/{self.total_questions}")

    def prepare_quiz_ui(self):
        self.current_question = 1
        self.incorrect_guesses = 0
        self.update_progress_label()
        self.indicator_label.clear()
        # self.clear_layout(self.central_layout)
        self.question_generator.start_new_question()
        self._refresh_layout()
        # self.learn_tab.stack.setCurrentWidget(self)

    def _refresh_layout(self):
        # first remove all the stretches
        self.clear_stretches(self.central_layout)
        layout = self.central_layout
        widgets = [
            self.progress_label,
            self.question_widget,
            self.answers_widget,
            self.indicator_label,
        ]
        for widget in widgets:
            layout.addWidget(widget)
            layout.addStretch(1)

    def clear_stretches(self, layout: QVBoxLayout):
        # specifically target the stretch poilcys, don't go for all the items
        for i in reversed(range(layout.count())):
            if layout.itemAt(i).widget() is None:
                layout.takeAt(i)

    def clear_current_question(self):
        self.question_widget.clear()
        self.answers_widget.clear()
