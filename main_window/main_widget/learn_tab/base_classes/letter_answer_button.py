# button_answers_renderer.py
from typing import Any, List, Callable
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import Qt
from main_window.main_widget.learn_tab.base_classes.base_answers_renderer import (
    BaseAnswersRenderer,
)


class LetterAnswerButton(QPushButton):
    answer: Any

    def __init__(
        self,
        answer: Any,
        parent: QWidget,
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ):
        super().__init__(str(answer), parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.answer = answer
        self.clicked.connect(lambda _, a=answer: check_callback(a, correct_answer))

    def update_answer(
        self,
        answer: Any,
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ):
        self.setText(str(answer))
        self.answer = answer
        self.setEnabled(True)
        try:
            self.clicked.disconnect()
        except Exception:
            pass
        self.clicked.connect(lambda _, a=answer: check_callback(a, correct_answer))
