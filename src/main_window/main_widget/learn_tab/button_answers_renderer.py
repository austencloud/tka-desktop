# button_answers_renderer.py
from typing import TYPE_CHECKING, Any, List, Callable
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_widget.answers_widget import (
        AnswersWidget,
    )
from main_window.main_widget.learn_tab.letter_answer_button import (
    LetterAnswerButton,
)


class ButtonAnswersRenderer:
    def __init__(self):
        self.buttons: List[LetterAnswerButton] = []
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def get_layout(self):
        return self.layout

    def update_answer_options(
        self,
        answers: List[Any],
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
        answers_widget: "AnswersWidget",
    ) -> None:
        # If no buttons exist yet, create them.
        if not self.buttons:
            self.layout.setSpacing(
                answers_widget.lesson_widget.learn_tab.main_widget.width() // 80
            )
            for answer in answers:
                button = LetterAnswerButton(
                    answer, answers_widget, check_callback, correct_answer
                )

                self.layout.addWidget(button)
                self.buttons.append(button)
        else:
            # Otherwise, update the existing buttons.
            for i, answer in enumerate(answers):
                self.buttons[i].update_answer(answer, check_callback, correct_answer)
                self.buttons[i].show()  # ensure it's visible
        # In case the new answer list is shorter than before, hide extra buttons.
        for i in range(len(answers), len(self.buttons)):
            self.buttons[i].hide()

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
