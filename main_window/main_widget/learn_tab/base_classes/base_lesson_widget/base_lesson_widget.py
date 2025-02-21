# learn_tab/base_classes/base_lesson_widget/base_lesson_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from .lesson_layout_manager import LessonLayoutManager
from .lesson_answer_checker import LessonAnswerChecker
from .lesson_go_back_button import LessonGoBackButton
from .lesson_indicator_label import LessonIndicatorLabel
from .lesson_progress_label import LessonProgressLabel
from .lesson_quiz_timer_manager import QuizTimerManager

from ..base_answers_widget import BaseAnswersWidget
from ..base_question_generator import BaseQuestionGenerator
from ..base_question_widget import BaseQuestionWidget

if TYPE_CHECKING:
    from ...learn_tab import LearnTab


class BaseLessonWidget(QWidget):
    """
    BaseLessonWidget is responsible for managing the lesson UI:
    it holds components such as the question widget, answers widget,
    progress indicator, timer, and go-back button.
    """

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

        # Initialize UI components
        self.timer_manager = QuizTimerManager(self)
        self.indicator_label = LessonIndicatorLabel(self)
        self.go_back_button = LessonGoBackButton(self)
        self.progress_label = LessonProgressLabel(self)
        self.answer_checker = LessonAnswerChecker(self)

        # Delegate layout management to LessonLayoutManager
        self.layout_manager = LessonLayoutManager(self)

    def update_progress_label(self):
        self.progress_label.setText(f"{self.current_question}/{self.total_questions}")

    def prepare_quiz_ui(self):
        self.current_question = 1
        self.incorrect_guesses = 0
        self.update_progress_label()
        self.indicator_label.clear()
        widgets_to_fade = [
            self.question_widget,
            self.answers_widget,
            self.indicator_label,
            self.progress_label,
        ]
        indicator_label = self.indicator_label
        indicator_label.setStyleSheet(
            f"LessonIndicatorLabel {{"
            f" background-color: transparent;"
            f"}}"
        )
        self.fade_manager.widget_fader.fade_and_update(
            widgets_to_fade,
            callback=self.question_generator.generate_question,  # Now update content in-place
        )
