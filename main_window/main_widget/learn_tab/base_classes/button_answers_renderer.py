# button_answers_renderer.py
from typing import Any, List, Callable
from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from main_window.main_widget.learn_tab.base_classes.base_answers_renderer import (
    BaseAnswersRenderer,
)
from main_window.main_widget.learn_tab.base_classes.letter_answer_button import (
    LetterAnswerButton,
)


class ButtonAnswersRenderer(BaseAnswersRenderer):
    def __init__(self):
        self.buttons: List[LetterAnswerButton] = []
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def get_layout(self):
        return self.layout

    def create_answer_options(
        self,
        parent: QWidget,
        answers: List[Any],
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ) -> None:
        self._clear_layout()
        self.buttons.clear()
        for answer in answers:
            button = LetterAnswerButton(answer, parent, check_callback, correct_answer)
            self.layout.addWidget(button)
            self.buttons.append(button)

    def update_answer_options(
        self,
        parent: QWidget,
        answers: List[Any],
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ) -> None:
        for button in self.buttons:
            button.hide()
        self.buttons.clear()
        for answer in answers:
            button = LetterAnswerButton(answer, parent, check_callback, correct_answer)
            self.layout.addWidget(button)
            self.buttons.append(button)
            button.show()

    def disable_answer_option(self, answer: Any) -> None:
        for button in self.buttons:
            if button.answer == answer:
                button.setDisabled(True)
                break

    def _clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
