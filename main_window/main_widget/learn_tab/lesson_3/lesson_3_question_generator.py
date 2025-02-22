import random
from typing import TYPE_CHECKING
from base_widgets.pictograph.pictograph import Pictograph
from main_window.main_widget.learn_tab.base_classes.base_question_generator import (
    BaseQuestionGenerator,
)

if TYPE_CHECKING:
    from .lesson_3_widget import Lesson3Widget


class Lesson3QuestionGenerator(BaseQuestionGenerator):
    """Generates questions for Lesson 3 (valid next pictograph matching)."""

    def __init__(self, lesson_3_widget: "Lesson3Widget"):
        super().__init__(lesson_3_widget)
        self.lesson_widget = lesson_3_widget
        self.previous_pictograph = None

    def generate_question(self):
        """Generate a question for Lesson 3."""
        self.lesson_widget.update_progress_label()

        initial_pictograph = self.generate_initial_pictograph()
        self.previous_pictograph = initial_pictograph

        self.lesson_widget.question_widget.renderer.update_question(initial_pictograph)
        correct_pictograph = self.generate_correct_answer(initial_pictograph)
        wrong_pictographs = self.generate_wrong_answers(correct_pictograph)
        pictographs: list["Pictograph"] = [correct_pictograph] + wrong_pictographs
        random.shuffle(pictographs)
        self.lesson_widget.answers_widget.update_answer_options(
            pictographs,
            correct_pictograph,
            self.lesson_widget.answer_checker.check_answer,
        )

    def generate_initial_pictograph(self) -> dict:
        """Generate an initial pictograph randomly to display."""
        available_letters = list(self.main_widget.pictograph_dataset.keys())
        pictograph_datas = self.filter_pictograph_datas_by_grid_mode()

        available_letters = [
            letter
            for letter in available_letters
            for pictograph in pictograph_datas[letter]
            if pictograph["start_pos"] == pictograph["end_pos"]
        ]
        letter = random.choice(available_letters)
        return random.choice(pictograph_datas[letter])

    def generate_correct_answer(self, initial_pictograph: dict) -> dict:
        """Generate a valid pictograph that can follow the initial pictograph."""
        end_pos = initial_pictograph["end_pos"]
        pictograph_datas = self.filter_pictograph_datas_by_grid_mode()
        valid_pictographs = [
            pictograph
            for letter_pictographs in pictograph_datas.values()
            for pictograph in letter_pictographs
            if pictograph["start_pos"] == end_pos
        ]

        valid_pictographs = [
            pictograph
            for pictograph in valid_pictographs
            if pictograph["start_pos"] != pictograph["end_pos"]
        ]

        correct_answer = random.choice(valid_pictographs)
        self._update_orientations(initial_pictograph, correct_answer)

        return correct_answer

    def _update_orientations(self, initial_pictograph, correct_answer):
        correct_answer["blue_attributes"]["start_ori"] = initial_pictograph[
            "blue_attributes"
        ]["end_ori"]
        correct_answer["blue_attributes"]["end_ori"] = (
            self.main_widget.json_manager.ori_calculator.calculate_end_ori(
                correct_answer, "blue"
            )
        )

        correct_answer["red_attributes"]["start_ori"] = initial_pictograph[
            "red_attributes"
        ]["end_ori"]
        correct_answer["red_attributes"]["end_ori"] = (
            self.main_widget.json_manager.ori_calculator.calculate_end_ori(
                correct_answer, "red"
            )
        )

    def generate_random_pictograph(self) -> dict:
        pictograph_datas = self.filter_pictograph_datas_by_grid_mode()
        while True:
            letter = random.choice(list(self.main_widget.pictograph_dataset.keys()))
            random_pictograph = random.choice(pictograph_datas[letter])
            if random_pictograph["start_pos"] != random_pictograph["end_pos"]:
                return random_pictograph

    def generate_wrong_answers(self, correct_pictograph: dict) -> list[dict]:
        """Generate three random wrong pictographs that don't match the correct condition."""
        correct_start_pos = correct_pictograph["start_pos"]

        wrong_pictographs = []
        while len(wrong_pictographs) < 3:
            random_pictograph = self.generate_random_pictograph()
            if random_pictograph["start_pos"] != correct_start_pos:
                wrong_pictographs.append(random_pictograph)
        return wrong_pictographs
