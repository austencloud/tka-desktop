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
    def __init__(self, lesson_widget: "BaseLessonWidget"):
        self.renderer = ButtonAnswersRenderer()
        super().__init__(lesson_widget, self.renderer)

