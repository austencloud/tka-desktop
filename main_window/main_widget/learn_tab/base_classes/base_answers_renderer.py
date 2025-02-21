# generic_answers_widget.py
from typing import Callable, Any, List
from PyQt6.QtWidgets import QWidget, QLayout


class BaseAnswersRenderer:
    """
    A strategy interface that knows how to create, update, and disable answer options.
    """

    def create_answer_options(
        self,
        parent: QWidget,
        answers: List[Any],
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ) -> None:
        raise NotImplementedError()

    def update_answer_options(
        self,
        parent: QWidget,
        answers: List[Any],
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ) -> None:
        raise NotImplementedError()

    def disable_answer_option(self, answer: Any) -> None:
        raise NotImplementedError()

    def get_layout(self) -> QLayout:
        raise NotImplementedError()
