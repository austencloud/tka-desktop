from typing import TYPE_CHECKING, Callable, Any
from PyQt6.QtWidgets import QWidget
from ..button_answers_renderer import ButtonAnswersRenderer
from ..pictograph_answers_renderer import PictographAnswersRenderer

if TYPE_CHECKING:
    from .lesson_widget import LessonWidget


class AnswersWidget(QWidget):
    """
    A dynamic answer widget that automatically chooses the correct answer renderer
    (buttons, pictographs, etc.), eliminating the need for separate Answer Widgets per lesson.
    """

    def __init__(
        self,
        lesson_widget: "LessonWidget",
        answer_format: str,
        columns: int = 2,
        spacing: int = 30,
    ):
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget
        self.main_widget = lesson_widget.main_widget
        self.answer_choices: dict[Any, QWidget] = {}

        # Dynamically select renderer
        self.renderer = self._select_renderer(answer_format, columns, spacing)
        self.renderer_container = self.renderer.get_layout()
        self.setLayout(self.renderer_container)

    def _select_renderer(
        self, answer_type: str, columns: int, spacing: int
    ) -> ButtonAnswersRenderer | PictographAnswersRenderer:
        """
        Determines which renderer to use based on answer_type.
        """
        if answer_type == "button":
            return ButtonAnswersRenderer()
        elif answer_type == "pictograph":
            return PictographAnswersRenderer(self.lesson_widget.lesson_type, columns=columns, spacing=spacing)
        else:
            raise ValueError(f"Unknown answer_type: {answer_type}")

    def create_answer_options(
        self,
        answers: list[Any],
        correct_answer: Any,
        check_callback: Callable[[Any, Any], None],
    ):
        self.answer_choices.clear()
        self.renderer.update_answer_options(
            answers, check_callback, correct_answer, self
        )

    def update_answer_options(
        self,
        answers: list[Any],
        correct_answer: Any,
        check_callback: Callable[[Any, Any], None],
    ):
        self.renderer.update_answer_options(
            answers, check_callback, correct_answer, self
        )

    def disable_answer(self, answer: Any):
        self.renderer.disable_answer_option(answer)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if isinstance(self.renderer, PictographAnswersRenderer):
            size = int(
                self.main_widget.height()
                // (4 if self.lesson_widget.lesson_type == "Lesson2" else 5)
            )
            for view in self.renderer.pictograph_views.values():
                view.setFixedSize(size, size)
