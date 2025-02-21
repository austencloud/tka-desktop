from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

from main_window.main_widget.learn_tab.base_classes.button_answers_renderer import (
    ButtonAnswersRenderer,
)
from main_window.main_widget.learn_tab.base_classes.generic_answers_widget import (
    GenericAnswersWidget,
)

from ..base_classes.base_answers_widget import BaseAnswersWidget


if TYPE_CHECKING:
    from ..learn_tab import LearnTab


class Lesson1AnswersWidget(BaseAnswersWidget):
    def __init__(self, learn_widget):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget

        self.buttons: dict[str, QPushButton] = {}
        self.renderer = ButtonAnswersRenderer()
        self.generic_widget = GenericAnswersWidget(
            learn_widget, self.renderer
        )
        self.setLayout(self.generic_widget.layout())

    def create_answer_buttons(
        self, answers, correct_answer, check_answer_callback
    ) -> None:
        self.generic_widget.create_answer_options(
            answers, correct_answer, check_answer_callback
        )

    def update_answer_buttons(
        self, answers, correct_answer, check_answer_callback
    ) -> None:
        self.generic_widget.update_answer_options(
            answers, correct_answer, check_answer_callback
        )

    def disable_answer(self, answer) -> None:
        self.generic_widget.disable_answer(answer)

    def resizeEvent(self, event) -> None:
        for button in self.renderer.buttons:
            size = self.main_widget.width() // 16
            button.setFixedSize(size, size)
            font_size = self.main_widget.width() // 40
            font = button.font()
            font.setFamily("Georgia")
            font.setPointSize(font_size)
            button.setFont(font)
            button.setStyleSheet(f"font-size: {font_size}px;")
