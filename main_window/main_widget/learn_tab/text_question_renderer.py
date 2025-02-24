from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt


class TextQuestionRenderer:
    """
    Renders a simple text-based question.
    """

    def __init__(self):
        self.widget = QWidget()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.widget.setLayout(self.layout)

        self.letter_label = QLabel()
        self.letter_label.setWordWrap(True)
        self.layout.addWidget(self.letter_label)

    def get_widget(self):
        return self.widget

    def update_question(self, question_text):
        """
        Updates the question label.
        """
        self.letter_label.setText(question_text)
