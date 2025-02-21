from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_lesson_widget import BaseLessonWidget


class LessonAnswerChecker:
    """Class to check answers and update the UI accordingly."""

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        self.lesson = lesson_widget

    def check_answer(self, selected_answer, correct_answer):
        if selected_answer == correct_answer:
            self.lesson.indicator_label.show_message("Correct! Well done.")
            self.lesson.indicator_label.setStyleSheet("color: green;")
            self.lesson.current_question += 1

            if self.lesson.mode == "fixed_question":
                self.lesson.update_progress_label()
                if self.lesson.current_question <= self.lesson.total_questions:
                    self.lesson.question_generator.fade_to_new_question()
                else:
                    self.lesson.learn_tab.results_widget.show_results(
                        self.lesson, self.lesson.incorrect_guesses
                    )
            elif self.lesson.mode == "countdown":
                self.lesson.question_generator.fade_to_new_question()
        else:
            self.lesson.indicator_label.show_message("Wrong! Try again.")
            self.lesson.indicator_label.setStyleSheet("color: red;")
            self.lesson.answers_widget.disable_answers(selected_answer)
            self.lesson.incorrect_guesses += 1
