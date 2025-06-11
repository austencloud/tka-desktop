from typing import TYPE_CHECKING, Any, Callable
from PyQt6.QtCore import Qt

from styles.styled_button import StyledButton


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_widget.answers_widget import (
        AnswersWidget,
    )


class LetterAnswerButton(StyledButton):
    answer: Any

    def __init__(
        self,
        answer: Any,
        answers_widget: "AnswersWidget",
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ):
        super().__init__(str(answer))
        self.answer_widget = answers_widget
        self.answer = answer
        self.check_callback = check_callback
        self.correct_answer = correct_answer
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(lambda _, a=answer: check_callback(a, correct_answer))
        self._radius = 0

    def resizeEvent(self, event):
        self.main_widget = self.answer_widget.lesson_widget.learn_tab.main_widget
        parent_width = self.main_widget.width()
        size = parent_width // 16
        self.setFixedSize(size, size)
        font_size = parent_width // 50
        font = self.font()
        font.setFamily("Georgia")
        font.setPointSize(font_size)
        self.setFont(font)
        super().resizeEvent(event)

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
