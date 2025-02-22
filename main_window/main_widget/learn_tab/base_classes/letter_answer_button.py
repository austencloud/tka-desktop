from typing import TYPE_CHECKING, Any, Callable
from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtGui import QFont, QResizeEvent


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.answers_widget import (
        AnswersWidget,
    )
    from main_window.main_widget.learn_tab.base_classes.base_answers_widget import (
        BaseAnswersWidget,
    )


class LetterAnswerButton(QPushButton):
    answer: Any

    def __init__(
        self,
        answer: Any,
        answers_widget: "AnswersWidget",
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
        self._radius = 0
        self._update_style()

    def _update_style(self):
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: lightgray;
                color: black;
                padding: 5px;
                border-radius: {self.width() // 2}px;
                margin: 5px;
                border: 3px solid black;
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(200, 200, 200, 1),
                    stop:1 rgba(150, 150, 150, 1)
                );
                border: 3px solid gold;
            }}
            QPushButton:pressed {{
                background-color: #d0d0d0;
            }}
            QPushButton:disabled {{
                color: gray;
            }}
        """
        )

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
