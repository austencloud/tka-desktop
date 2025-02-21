from typing import TYPE_CHECKING
from main_window.main_widget.learn_tab.base_classes.base_answers_widget import (
    BaseAnswersWidget,
)
from main_window.main_widget.learn_tab.base_classes.pictograph_answers_renderer import (
    PictographAnswersRenderer,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )


class Lesson3AnswersWidget(BaseAnswersWidget):
    """Minimal Lesson 3 answers widget using the same pictograph renderer."""

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        self.renderer = PictographAnswersRenderer(columns=2, spacing=30)
        super().__init__(lesson_widget, self.renderer)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = int(self.main_widget.height() // 5)
        for view in self.renderer.pictograph_views.values():
            view.setFixedSize(size, size)
