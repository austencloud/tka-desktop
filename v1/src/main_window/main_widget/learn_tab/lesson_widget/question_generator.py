import random
from typing import TYPE_CHECKING

from enums.letter.letter import Letter

from data.constants import END_POS, LETTER, START_POS
from main_window.main_widget.grid_mode_checker import GridModeChecker


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_widget.lesson_widget import (
        LessonWidget,
    )


class QuestionGenerator:
    """
    A single unified question generator that dynamically generates different types of questions
    based on lesson configuration.
    """

    def __init__(self, lesson_widget: "LessonWidget", quiz_description: str) -> None:
        super().__init__()
        self.lesson_widget = lesson_widget
        self.main_widget = lesson_widget.main_widget
        self.quiz_description = quiz_description
        self.previous_correct_letter = None
        self.previous_pictographs = set()

    def generate_question(self):
        """
        Dynamically determines how to generate a question based on question type.
        """
        self.lesson_widget.update_progress_label()

        if self.quiz_description == "pictograph_to_letter":
            self._generate_pictograph_to_letter()
        elif self.quiz_description == "letter_to_pictograph":
            self._generate_letter_to_pictograph()
        elif self.quiz_description == "valid_next_pictograph":
            self._generate_valid_next_pictograph()
        else:
            raise ValueError(f"Unknown question type: {self.quiz_description}")

    def _generate_pictograph_to_letter(self):
        """Generates a question where a pictograph is displayed, and the answer is a letter."""
        correct_answer = self._generate_correct_letter()
        self.previous_correct_letter = correct_answer
        pictograph_dataset = self.main_widget.pictograph_dataset

        correct_pictograph_data = random.choice(pictograph_dataset[correct_answer])
        self.lesson_widget.question_widget.renderer.update_question(
            correct_pictograph_data
        )

        wrong_answers = self._generate_wrong_letters(correct_answer)
        options = [correct_answer.value] + wrong_answers
        random.shuffle(options)

        self.lesson_widget.answers_widget.update_answer_options(
            options,
            correct_answer.value,
            self.lesson_widget.answer_checker.check_answer,
        )

    def _generate_letter_to_pictograph(self):
        """Generates a question where a letter is displayed, and the answer is a pictograph."""
        correct_letter, correct_pictograph = self._generate_correct_pictograph()

        self.lesson_widget.question_widget.renderer.update_question(
            correct_letter.value
        )

        pictographs = self._get_shuffled_pictographs(correct_pictograph)
        self.lesson_widget.answers_widget.update_answer_options(
            pictographs,
            correct_pictograph,
            self.lesson_widget.answer_checker.check_answer,
        )

    def _get_shuffled_pictographs(self, correct_pictograph):
        """Generate and shuffle the correct and wrong pictographs."""
        wrong_pictographs = self.generate_wrong_pictographs(correct_pictograph[LETTER])
        pictographs = [correct_pictograph] + wrong_pictographs
        random.shuffle(pictographs)

        return pictographs

    def _get_available_letters(self, correct_letter: str) -> list[str]:
        """Get the available letters excluding the correct letter."""
        return [
            letter
            for letter in self.main_widget.pictograph_dataset
            if letter != correct_letter
        ]

    def generate_wrong_pictographs(self, correct_letter: str) -> list[dict]:
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

    def _generate_valid_next_pictograph(self):
        """Generates a question where a pictograph is shown, and the answer is the valid next pictograph."""
        initial_pictograph = self._generate_initial_pictograph()
        self.previous_pictograph = initial_pictograph

        self.lesson_widget.question_widget.renderer.update_question(initial_pictograph)

        correct_pictograph = self._generate_correct_next_pictograph(initial_pictograph)
        wrong_pictographs = self._generate_wrong_pictographs(correct_pictograph)

        options = [correct_pictograph] + wrong_pictographs
        random.shuffle(options)

        self.lesson_widget.answers_widget.update_answer_options(
            options, correct_pictograph, self.lesson_widget.answer_checker.check_answer
        )

    def _generate_correct_letter(self) -> Letter:
        """Generates a correct letter, ensuring it is not the same as the previous one."""
        letters = list(self.main_widget.pictograph_dataset.keys())
        if self.previous_correct_letter:
            letters.remove(self.previous_correct_letter)
        return random.choice(letters)

    def _generate_correct_pictograph(self) -> tuple[Letter, dict]:
        """Retrieves a correct letter and its corresponding pictograph."""
        available_letters = list(self.main_widget.pictograph_dataset.keys())
        correct_letter = random.choice(available_letters)
        pictograph_datas = self.filter_pictograph_dataset_by_grid_mode()
        correct_pictograph = random.choice(pictograph_datas[correct_letter])
        return correct_letter, correct_pictograph

    def _generate_wrong_letters(self, correct_letter: Letter) -> list[str]:
        """Generates three incorrect letter answers."""
        return random.sample(
            [
                letter.value
                for letter in self.main_widget.pictograph_dataset
                if letter != correct_letter
            ],
            3,
        )

    def _generate_wrong_pictographs(self, correct_pictograph: dict) -> list[dict]:
        """Generates three incorrect pictographs."""
        wrong_pictographs = []
        while len(wrong_pictographs) < 3:
            random_pictograph = self._generate_random_pictograph()
            if random_pictograph[START_POS] != correct_pictograph[START_POS]:
                wrong_pictographs.append(random_pictograph)
        return wrong_pictographs

    def _generate_initial_pictograph(self) -> dict:
        """Generates an initial pictograph to display."""
        available_letters = list(self.main_widget.pictograph_dataset.keys())
        pictograph_datas = self.filter_pictograph_dataset_by_grid_mode()

        available_letters = [
            letter
            for letter in available_letters
            for pictograph in pictograph_datas[letter]
            if pictograph[START_POS] == pictograph[END_POS]
        ]
        letter = random.choice(available_letters)
        return random.choice(pictograph_datas[letter])

    def _generate_correct_next_pictograph(self, initial_pictograph: dict) -> dict:
        """Finds a valid pictograph that can follow the initial pictograph."""
        end_pos = initial_pictograph[END_POS]
        pictograph_datas = self.filter_pictograph_dataset_by_grid_mode()
        valid_pictographs = [
            pictograph
            for letter_pictographs in pictograph_datas.values()
            for pictograph in letter_pictographs
            if pictograph[START_POS] == end_pos
        ]

        correct_answer = random.choice(valid_pictographs)
        return correct_answer

    def _generate_random_pictograph(self) -> dict:
        """Selects a random pictograph."""
        pictograph_datas = self.filter_pictograph_dataset_by_grid_mode()
        while True:
            letter = random.choice(list(self.main_widget.pictograph_dataset.keys()))
            random_pictograph = random.choice(pictograph_datas[letter])
            if random_pictograph[START_POS] != random_pictograph[END_POS]:
                return random_pictograph

    def _get_random_pictograph(
        self, available_letters: list[str]
    ) -> tuple[Letter, dict]:
        """Choose a random letter and a corresponding pictograph."""
        letter = random.choice(available_letters)
        pictograph_datas = self.filter_pictograph_dataset_by_grid_mode()
        pictograph_data = random.choice(pictograph_datas[letter])
        return letter, pictograph_data

    def filter_pictograph_dataset_by_grid_mode(self) -> dict[Letter, list[dict]]:
        """Filter pictograph dicts by grid mode."""
        valid_dicts: dict[Letter, list[dict]] = {}
        for letter in self.main_widget.pictograph_dataset:
            valid_dicts.setdefault(letter, [])
            for pictograph_data in self.main_widget.pictograph_dataset[letter]:
                if (
                    GridModeChecker.get_grid_mode(pictograph_data)
                    # == grid_mode
                ):
                    valid_dicts[letter].append(pictograph_data)
        return valid_dicts

    def fade_to_new_question(self):

        widgets_to_fade = [
            self.lesson_widget.question_widget,
            self.lesson_widget.answers_widget,
        ]
        self.lesson_widget.fade_manager.widget_fader.fade_and_update(
            widgets_to_fade,
            callback=self.generate_question,
        )
