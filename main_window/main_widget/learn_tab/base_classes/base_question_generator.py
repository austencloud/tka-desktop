from typing import TYPE_CHECKING

from Enums.letters import Letter


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )


class BaseQuestionGenerator:
    not_implemented_message = "This function should be implemented by the subclass."

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        self.main_widget = lesson_widget.main_widget
        self.lesson_widget = lesson_widget

    def filter_pictograph_datas_by_grid_mode(self) -> dict[Letter, list[dict]]:
        """Filter pictograph dicts by grid mode."""
        valid_dicts: dict[Letter, list[dict]] = {}
        for letter in self.main_widget.pictograph_dataset:
            valid_dicts.setdefault(letter, [])
            for pictograph_data in self.main_widget.pictograph_dataset[letter]:
                if (
                    self.main_widget.grid_mode_checker.get_grid_mode(pictograph_data)
                    # == grid_mode
                ):
                    valid_dicts[letter].append(pictograph_data)
        return valid_dicts

    def start_new_question(self):
        widgets_to_fade = [
            self.lesson_widget.question_widget,
            self.lesson_widget.answers_widget,
        ]
        self.lesson_widget.fade_manager.widget_fader.fade_and_update(
            widgets_to_fade,
            callback=self.generate_question,
        )

    def generate_question(self):
        raise NotImplementedError(self.not_implemented_message)

    def generate_correct_answer(self):
        raise NotImplementedError(self.not_implemented_message)

    def generate_wrong_answers(self, correct_answer):
        raise NotImplementedError(self.not_implemented_message)

    def _get_random_correct_pictograph(self):
        raise NotImplementedError(self.not_implemented_message)
