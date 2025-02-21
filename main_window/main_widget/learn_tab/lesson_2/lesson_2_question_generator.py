import random
from typing import TYPE_CHECKING

from Enums.letters import Letter
from main_window.main_widget.learn_tab.base_classes.base_question_generator import (
    BaseQuestionGenerator,
)

if TYPE_CHECKING:
    from .lesson_2_widget import Lesson2Widget


class Lesson2QuestionGenerator(BaseQuestionGenerator):
    """Generates questions for Lesson 2 (letter to pictograph matching)."""

    def __init__(self, lesson_2_widget: "Lesson2Widget") -> None:
        self.lesson_widget = lesson_2_widget
        self.main_widget = lesson_2_widget.main_widget
        self.previous_pictographs = set()
        self.previous_letter = None  # Track the previously used letter

    def generate_question(self):
        """Generate a question and update the question and answer widgets."""
        self.lesson_widget.update_progress_label()

        correct_letter, correct_pictograph = self.generate_correct_answer()

        self.lesson_widget.question_widget._update_letter_label(correct_letter.value)

        pictographs = self._get_shuffled_pictographs(correct_pictograph)
        self.lesson_widget.answers_widget.update_answer_options(
            pictographs,
            correct_pictograph,
            self.lesson_widget.answer_checker.check_answer,
        )

    def generate_correct_answer(self) -> tuple[Letter, dict]:
        """Retrieve a random correct letter and its corresponding pictograph, avoiding repetition."""
        # Get a list of available letters excluding the previous one
        available_letters = [
            letter
            for letter in self.main_widget.pictograph_dataset.keys()
            if letter != self.previous_letter
        ]

        correct_letter = random.choice(available_letters)
        pictograph_datas = self.filter_pictograph_datas_by_grid_mode()
        correct_pictograph = random.choice(pictograph_datas[correct_letter])

        # Update the previous letter to the current one
        self.previous_letter = correct_letter
        return correct_letter, correct_pictograph

    def _get_shuffled_pictographs(self, correct_pictograph):
        """Generate and shuffle the correct and wrong pictographs."""
        wrong_pictographs = self.generate_wrong_answers(correct_pictograph["letter"])
        pictographs = [correct_pictograph] + wrong_pictographs
        random.shuffle(pictographs)

        return pictographs

    def generate_wrong_answers(self, correct_letter: str) -> list[dict]:
        """Generate three random wrong pictographs, ensuring each has a different letter."""
        available_letters = self._get_available_letters(correct_letter)
        wrong_pictographs = []

        while len(wrong_pictographs) < 3:
            # Ensure the letter hasn't been used before and does not match the correct letter
            letter, pictograph_data = self._get_random_pictograph(available_letters)

            if letter.value != correct_letter:
                wrong_pictographs.append(pictograph_data)
                available_letters.remove(letter)

        return wrong_pictographs

    def _get_available_letters(self, correct_letter: str) -> list[str]:
        """Get the available letters excluding the correct letter."""
        return [
            letter
            for letter in self.main_widget.pictograph_dataset
            if letter != correct_letter
        ]

    def _get_random_pictograph(
        self, available_letters: list[str]
    ) -> tuple[Letter, dict]:
        """Choose a random letter and a corresponding pictograph."""
        letter = random.choice(available_letters)
        pictograph_datas = self.filter_pictograph_datas_by_grid_mode()
        pictograph_data = random.choice(pictograph_datas[letter])
        return letter, pictograph_data

    def _is_duplicate_pictograph(self, letter: str, pictograph_data: dict) -> bool:
        """Check if a pictograph has already been used."""
        pictograph_key = (
            self.main_widget.pictograph_key_generator.generate_pictograph_key(
                pictograph_data
            )
        )
        if pictograph_key in self.previous_pictographs:
            return True

        self.previous_pictographs.add(pictograph_key)
        return False
