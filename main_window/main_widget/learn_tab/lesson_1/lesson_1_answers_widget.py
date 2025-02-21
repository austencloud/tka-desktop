from typing import TYPE_CHECKING
from main_window.main_widget.learn_tab.base_classes.base_answers_widget import (
    BaseAnswersWidget,
)
from main_window.main_widget.learn_tab.base_classes.button_answers_renderer import (
    ButtonAnswersRenderer,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )


class Lesson1AnswersWidget(BaseAnswersWidget):
    """Minimal Lesson 1 answers widget that directly uses the generic widget + button renderer."""

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        # Instantiate the button renderer
        self.renderer = ButtonAnswersRenderer()
        # Pass it to the generic widget constructor
        super().__init__(lesson_widget, self.renderer)

    def resizeEvent(self, event):
        """
        Override if you need to resize the buttons for Lesson 1 specifically.
        Otherwise, you can remove this method entirely.
        """
        super().resizeEvent(event)
        for button in self.renderer.buttons:
            size = self.main_widget.width() // 16
            button.setFixedSize(size, size)
            font_size = self.main_widget.width() // 40
            font = button.font()
            font.setFamily("Georgia")
            font.setPointSize(font_size)
            button.setFont(font)
            button.setStyleSheet(f"font-size: {font_size}px;")
