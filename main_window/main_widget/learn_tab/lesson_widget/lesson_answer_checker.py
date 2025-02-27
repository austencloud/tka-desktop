from typing import TYPE_CHECKING

from data.constants import RED

if TYPE_CHECKING:
    from .lesson_widget import LessonWidget


class LessonAnswerChecker:
    """Class to check answers and update the UI accordingly."""

    def __init__(self, lesson_widget: "LessonWidget"):
        self.lesson = lesson_widget

    def _update_indicator_style(self, color: str, message: str):
        self.lesson.indicator_label.show_message(message)
        border_radius = (
            min(
                self.lesson.indicator_label.width(),
                self.lesson.indicator_label.height(),
            )
            // 2
        )
        self.lesson.indicator_label.setStyleSheet(
            f"LessonIndicatorLabel {{"
            f" background-color: rgba(255, 255, 255, 128);"
            f" border-radius: {border_radius}px;"
            f" color: {color};"
            f"}}"
        )

    def check_answer(self, selected_answer, correct_answer):
        if selected_answer == correct_answer:
            self._update_indicator_style("green", "Correct! Well done.")
            self.lesson.current_question += 1

            if self.lesson.mode == "fixed_question":
                if self.lesson.current_question <= self.lesson.total_questions:
                    self.lesson.question_generator.fade_to_new_question()
                else:
                    self.lesson.learn_tab.results_widget.show_results(
                        self.lesson, self.lesson.incorrect_guesses
                    )
            elif self.lesson.mode == "countdown":
                self.lesson.question_generator.fade_to_new_question()
        else:
            self._update_indicator_style(RED, "Wrong! Try again.")
            self.lesson.answers_widget.disable_answer(selected_answer)
            self.lesson.incorrect_guesses += 1
