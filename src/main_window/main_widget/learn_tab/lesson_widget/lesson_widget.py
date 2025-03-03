# learn_tab/base_classes/lesson_widget/lesson_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel

from .answers_widget import AnswersWidget
from .question_generator import QuestionGenerator
from .question_widget import QuestionWidget
from .lesson_layout_manager import LessonLayoutManager
from .lesson_answer_checker import LessonAnswerChecker
from .lesson_go_back_button import LessonGoBackButton
from .lesson_indicator_label import LessonIndicatorLabel
from .lesson_progress_label import LessonProgressLabel
from .lesson_quiz_timer_manager import QuizTimerManager


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.learn_tab import LearnTab


class LessonWidget(QWidget):
    """
    BaseLessonWidget is responsible for managing the lesson UI:
    it holds components such as the question widget, answers widget,
    progress indicator, timer, and go-back button.
    """

    question_generator: QuestionGenerator = None
    question_widget: QuestionWidget = None
    answers_widget: AnswersWidget = None
    total_questions = 20
    current_question = 1
    quiz_time = 120
    mode = "fixed_question"
    incorrect_guesses = 0

    def __init__(
        self,
        learn_tab: "LearnTab",
        lesson_type: str,
        question_format: str,
        answer_format: str,
        quiz_description: str,
        question_prompt: str,
    ):
        super().__init__(learn_tab)
        self.lesson_type = lesson_type
        self.learn_tab = learn_tab
        self.main_widget = learn_tab.main_widget
        self.fade_manager = self.main_widget.fade_manager

        # Initialize UI components
        self.timer_manager = QuizTimerManager(self)
        self.indicator_label = LessonIndicatorLabel(self)
        self.go_back_button = LessonGoBackButton(self)
        self.progress_label = LessonProgressLabel(self)
        self.answer_checker = LessonAnswerChecker(self)
        self.layout_manager = LessonLayoutManager(self)

        # Dynamically generate the correct question widget and generator
        self.question_widget = QuestionWidget(self, question_format=question_format)
        self.answers_widget = AnswersWidget(self, answer_format=answer_format)
        self.question_generator = QuestionGenerator(
            self, quiz_description=quiz_description
        )
        self.question_prompt = QLabel(question_prompt, self)

        self.layout_manager.setup_layout()

    def update_progress_label(self):
        if self.mode == "countdown":
            minutes, seconds = divmod(self.quiz_time, 60)
            self.progress_label.setText(f"Time Remaining: {minutes}:{seconds:02d}")
        else:
            self.progress_label.setText(
                f"{self.current_question}/{self.total_questions}"
            )

    def prepare_quiz_ui(self, mode: str, fade=True):
        """
        Prepares the quiz UI and generates the first question.
        """
        self.current_question = 1
        self.incorrect_guesses = 0
        self.update_progress_label()
        self.indicator_label.clear()
        self.mode = mode
        self.indicator_label.setGraphicsEffect(None)  # Reset effects
        self.indicator_label.setStyleSheet("opacity: 0.0")  # Ensure it's fully hidden

        if mode == "countdown":
            self.timer_manager.start_timer(120)
        else:
            self.timer_manager.stop_timer()

        widgets_to_fade = [
            self.question_widget,
            self.answers_widget,
            self.indicator_label,
        ]

        if fade:
            self.fade_manager.widget_fader.fade_and_update(
                widgets_to_fade,
                callback=self.question_generator.generate_question,
            )
        else:
            self.question_generator.generate_question()

    def resizeEvent(self, event):
        self._resize_question_prompt()
        self._resize_go_back_button()
        super().resizeEvent(event)

    def _resize_go_back_button(self):
        # set it to programatically resize the go back button
        go_back_width = self.main_widget.width() // 10
        go_back_height = self.main_widget.height() // 20
        self.go_back_button.setFixedSize(go_back_width, go_back_height)
        font = self.go_back_button.font()
        font.setFamily("Georgia")
        font.setPointSize(self.main_widget.width() // 80)
        self.go_back_button.setFont(font)

    def _resize_question_prompt(self) -> None:
        question_prompt_font_size = self.main_widget.width() // 65
        font = self.question_prompt.font()
        font.setFamily("Georgia")
        font.setPointSize(question_prompt_font_size)
        self.question_prompt.setFont(font)
        self.question_prompt.setStyleSheet(
            f"color: {self.main_widget.font_color_updater.get_font_color(
                self.main_widget.settings_manager.global_settings.get_background_type()
                )};"
        )
