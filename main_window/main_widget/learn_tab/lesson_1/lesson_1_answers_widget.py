from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

from ..base_classes.base_answers_widget import BaseAnswersWidget


if TYPE_CHECKING:
    from ..learn_tab import LearnTab


class Lesson1AnswersWidget(BaseAnswersWidget):
    def __init__(self, learn_widget: "LearnTab"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.buttons: dict[str, QPushButton] = {}

    def create_answer_buttons(
        self, letters, correct_answer, check_answer_callback
    ) -> None:
        for letter in letters:
            button = QPushButton(letter)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda _, opt=letter: check_answer_callback(opt, correct_answer)
            )
            self.layout.addWidget(button)

    def update_answer_buttons(
        self, letters, correct_answer, check_answer_callback
    ) -> None:
        if len(self.buttons) != 4:
            self.buttons.clear()
            for letter in letters:
                button = QPushButton(letter)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                button.clicked.connect(
                    lambda _, opt=letter: check_answer_callback(opt, correct_answer)
                )
                self.layout.addWidget(button)
                self.buttons[letter] = button
        else:
            old_buttons = list(self.buttons.values())
            self.buttons.clear()
            for i, letter in enumerate(letters):
                button = old_buttons[i]
                button.setText(letter)
                button.setDisabled(False)
                try:
                    button.clicked.disconnect()
                except Exception:
                    pass
                button.clicked.connect(
                    lambda _, opt=letter: check_answer_callback(opt, correct_answer)
                )
                self.buttons[letter] = button

    def disable_answers(self, answer) -> None:
        button = self.buttons[answer]
        button.setDisabled(True)

    def resizeEvent(self, event) -> None:
        for button in self.buttons.values():
            size = self.main_widget.width() // 16
            button.setFixedSize(size, size)
            font_size = self.main_widget.width() // 40
            font = button.font()
            font.setFamily("Georgia")
            font.setPointSize(font_size)
            button.setFont(font)
            button.setStyleSheet(f"font-size: {font_size}px;")
