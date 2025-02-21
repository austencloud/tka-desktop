# button_answers_renderer.py
from typing import Any, List, Callable
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import Qt
from main_window.main_widget.learn_tab.base_classes.base_answers_renderer import (
    BaseAnswersRenderer,
)


class ButtonAnswersRenderer(BaseAnswersRenderer):
    def __init__(self):
        self.buttons: List[QPushButton] = []
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
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.buttons.clear()
        for answer in answers:
            button = QPushButton(str(answer), parent)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            setattr(button, "answer", answer)
            button.clicked.connect(
                lambda _, a=answer: check_callback(a, correct_answer)
            )
            self.layout.addWidget(button)
            self.buttons.append(button)

    def update_answer_options(
        self,
        parent: QWidget,
        answers: List[Any],
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ) -> None:
        # Remove extra buttons if there are more than needed.
        while len(self.buttons) > len(answers):
            btn = self.buttons.pop()
            btn.deleteLater()
        # Update existing buttons and add new ones if necessary.
        for i, answer in enumerate(answers):
            if i < len(self.buttons):
                button = self.buttons[i]
                button.setText(str(answer))
                button.answer = answer
                try:
                    button.clicked.disconnect()
                except Exception:
                    pass
                button.clicked.connect(
                    lambda _, a=answer: check_callback(a, correct_answer)
                )
            else:
                button = QPushButton(str(answer), parent)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                button.answer = answer
                button.clicked.connect(
                    lambda _, a=answer: check_callback(a, correct_answer)
                )
                self.layout.addWidget(button)
                self.buttons.append(button)

    def disable_answer_option(self, answer: Any) -> None:
        # Disable the button whose stored answer matches.
        for button in self.buttons:
            if button.answer == answer:
                button.setDisabled(True)
                break
