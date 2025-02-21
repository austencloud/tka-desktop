from typing import TYPE_CHECKING, Any, Callable
from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHBoxLayout

if TYPE_CHECKING:

    from main_window.main_widget.learn_tab.lesson_1.lesson_1_answers_widget import (
        Lesson1AnswersWidget,
    )
    from main_window.main_widget.learn_tab.base_classes.base_answers_widget import (
        BaseAnswersWidget,
    )


class LetterAnswerButton(QPushButton):
    answer: Any

    def __init__(
        self,
        answer: Any,
        answers_widget: "Lesson1AnswersWidget",
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ):
        super().__init__(str(answer), answers_widget)
        self.answer_widget = answers_widget
        self.answer = answer
        self.check_callback = check_callback
        self.correct_answer = correct_answer
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(lambda _, a=answer: check_callback(a, correct_answer))
        self.setStyleSheet("margin: 5px;")

    def resizeEvent(self, event):
        parent_width = self.answer_widget.lesson_widget.learn_tab.main_widget.width()
        size = parent_width // 16
        self.setFixedSize(size, size)
        font_size = parent_width // 50
        font = self.font()
        font.setFamily("Georgia")
        font.setPointSize(font_size)
        self.setFont(font)
        self.setStyleSheet(f"font-size: {font_size}px; margin: 5px;")
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
        self.setStyleSheet("margin: 5px;")
        try:
            self.clicked.disconnect()
        except Exception:
            pass
        self.clicked.connect(lambda _, a=answer: check_callback(a, correct_answer))

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(50, self.updateSize)

    def updateSize(self):
        parent_width = self.answer_widget.lesson_widget.learn_tab.main_widget.width()
        size = parent_width // 16
        self.setFixedSize(size, size)
        font_size = parent_width // 50
        font = self.font()
        font.setFamily("Georgia")
        font.setPointSize(font_size)
        self.setFont(font)
        self.setStyleSheet(f"font-size: {font_size}px; margin: 5px;")
