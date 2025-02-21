import random
from typing import TYPE_CHECKING
from Enums.letters import Letter
from main_window.main_widget.learn_tab.base_classes.base_question_generator import (
    BaseQuestionGenerator,
)


if TYPE_CHECKING:
    from .lesson_1_widget import Lesson1Widget


class Lesson1QuestionGenerator(BaseQuestionGenerator):
    """Generates questions for Lesson 1 (pictograph to letter matching)."""

    def __init__(self, lesson_1_widget: "Lesson1Widget") -> None:
        super().__init__(lesson_1_widget)
        self.lesson_1_widget = lesson_1_widget
        self.previous_correct_letter: Letter = None

    def generate_question(self):
        """Generate a question for Lesson 1."""
        self.lesson_1_widget.update_progress_label()

        correct_answer = self.generate_correct_answer()
        self.previous_correct_letter = correct_answer
        pictograph_dataset = self.main_widget.pictograph_dataset

        correct_pictograph_data = random.choice(pictograph_dataset[correct_answer])
        self.lesson_1_widget.question_widget.update_pictograph(correct_pictograph_data)
        wrong_answers = self.generate_wrong_answers(correct_answer)
        letters = [correct_answer.value] + wrong_answers
        random.shuffle(letters)
        self.lesson_1_widget.answers_widget.update_answer_options(
            letters,
            correct_answer.value,
            self.lesson_1_widget.answer_checker.check_answer,
        )

    def generate_correct_answer(self) -> Letter:
        """Generate a new correct letter that is different from the previous one."""
        letters = list(self.main_widget.pictograph_dataset.keys())
        if self.previous_correct_letter:
            letters.remove(self.previous_correct_letter)
        return random.choice(letters)

    def generate_wrong_answers(self, correct_answer) -> list[str]:
        """Generate three random wrong letter answers."""
        wrong_answers = random.sample(
            [
                letter.value
                for letter in self.main_widget.pictograph_dataset
                if letter != correct_answer
            ],
            3,
        )
        return wrong_answers
