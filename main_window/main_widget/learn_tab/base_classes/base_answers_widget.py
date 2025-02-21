from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget


if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_scene import PictographScene
    from .base_lesson_widget.base_lesson_widget import BaseLessonWidget


class BaseAnswersWidget(QWidget):
    pictographs: dict[str, "PictographScene"]

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        super().__init__(lesson_widget)
        self.main_widget = lesson_widget.main_widget

    def clear(self) -> None:
        raise NotImplementedError(
            "This function should be implemented by the subclass."
        )

    def resize_answers_widget(self) -> None:
        raise NotImplementedError(
            "This function should be implemented by the subclass."
        )

    def display_answers(self, answers) -> None:
        raise NotImplementedError(
            "This function should be implemented by the subclass."
        )

    def disable_answers(self, answer) -> None:
        raise NotImplementedError(
            "This function should be implemented by the subclass."
        )
