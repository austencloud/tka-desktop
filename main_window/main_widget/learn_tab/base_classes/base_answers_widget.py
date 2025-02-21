# generic_answers_widget.py
from typing import TYPE_CHECKING, Callable, Any, List, Dict
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.learn_tab.base_classes.base_answers_renderer import (
    BaseAnswersRenderer,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )


class BaseAnswersWidget(QWidget):
    """
    A generic answer widget that uses a rendering strategy to display answer options.
    """

    def __init__(
        self, lesson_widget: "BaseLessonWidget", renderer: BaseAnswersRenderer
    ):
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget
        self.main_widget = lesson_widget.main_widget
        self.renderer = renderer
        self.renderer_container = renderer.get_layout()
        self.setLayout(self.renderer_container)
        # Store answer option widgets for future reference if needed.
        self.answer_widgets: Dict[Any, QWidget] = {}

    def create_answer_options(
        self,
        answers: List[Any],
        correct_answer: Any,
        check_callback: Callable[[Any, Any], None],
    ) -> None:
        self.answer_widgets.clear()
        self.renderer.update_answer_options(
            self, answers, check_callback, correct_answer
        )

    def update_answer_options(
        self,
        answers: List[Any],
        correct_answer: Any,
        check_callback: Callable[[Any, Any], None],
    ) -> None:
        self.renderer.update_answer_options(
            self, answers, check_callback, correct_answer
        )

    def disable_answer(self, answer: Any) -> None:
        self.renderer.disable_answer_option(answer)
