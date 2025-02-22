from typing import TYPE_CHECKING, Any
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from main_window.main_widget.learn_tab.base_classes.pictograph_question_renderer import (
    PictographQuestionRenderer,
)
from main_window.main_widget.learn_tab.base_classes.text_question_renderer import (
    TextQuestionRenderer,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )


class QuestionWidget(QWidget):
    """
    A unified Question Widget that dynamically selects the appropriate renderer
    (text, pictograph, etc.), eliminating the need for separate question widgets per lesson.
    """

    def __init__(self, lesson_widget: "BaseLessonWidget", question_type: str):
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget
        self.main_widget = lesson_widget.main_widget

        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        # Choose renderer based on question type
        self.renderer = self.select_renderer(question_type)

        # Add the rendered question to the layout
        self.layout.addWidget(self.renderer.get_widget())

    def select_renderer(
        self, question_type: str
    ) -> PictographQuestionRenderer | TextQuestionRenderer:
        """
        Selects and returns the appropriate question renderer based on type.
        """
        self.question_type = question_type
        if self.question_type == "pictograph":
            return PictographQuestionRenderer(self.lesson_widget.lesson_type)
        elif self.question_type == "letter":
            return TextQuestionRenderer()
        else:
            raise ValueError(f"Unknown question type: {self.question_type}")

    def update_question(self, question_data: Any):
        """
        Updates the question based on new question data.
        """
        self.renderer.update_question(question_data)

    def resizeEvent(self, event) -> None:
        """Resize the question labels based on window size."""
        super().resizeEvent(event)
        if isinstance(self.renderer, TextQuestionRenderer):
            letter_label_font_size = self.main_widget.width() // 40
            letter_label_font = self.renderer.letter_label.font()
            letter_label_font.setFamily("Georgia")
            letter_label_font.setPointSize(letter_label_font_size)
            self.renderer.letter_label.setFont(letter_label_font)

        elif isinstance(self.renderer, PictographQuestionRenderer):
            if self.lesson_widget.lesson_type == "Lesson1":
                self.renderer.pictograph.elements.view.setFixedSize(
                    self.main_widget.height() // 3, self.main_widget.height() // 3
                )
            elif self.lesson_widget.lesson_type == "Lesson3":
                self.renderer.pictograph.elements.view.setFixedSize(
                    self.main_widget.height() // 5, self.main_widget.height() // 5
                )
