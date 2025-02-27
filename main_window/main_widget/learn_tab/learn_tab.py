from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QStackedLayout

from data.constants import LETTER
from main_window.main_widget.learn_tab.lesson_selector.lesson_selector import (
    LessonSelector,
)
from main_window.main_widget.learn_tab.lesson_widget.lesson_results_widget import (
    LessonResultsWidget,
)
from main_window.main_widget.learn_tab.lesson_widget.lesson_widget import (
    LessonWidget,
)


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LearnTab(QWidget):
    """Widget for the learning module, managing lesson selection and individual lessons."""

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_widget.splash.updater.update_progress("LearnTab")

        self.stack = QStackedLayout()
        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.lesson_selector = LessonSelector(self)
        self.lesson_1_widget = LessonWidget(
            self,
            lesson_type="Lesson1",
            question_format="pictograph",
            answer_format="button",
            quiz_description="pictograph_to_letter",
            question_prompt="Choose the letter for:",
        )
        self.lesson_2_widget = LessonWidget(
            self,
            lesson_type="Lesson2",
            question_format=LETTER,
            answer_format="pictograph",
            quiz_description="letter_to_pictograph",
            question_prompt="Choose the pictograph for:",
        )

        self.lesson_3_widget = LessonWidget(
            self,
            lesson_type="Lesson3",
            question_format="pictograph",
            answer_format="pictograph",
            quiz_description="valid_next_pictograph",
            question_prompt="Which pictograph can follow?",
        )

        self.results_widget = LessonResultsWidget(self)

    def _setup_layout(self) -> None:
        self.stack.addWidget(self.lesson_selector)
        self.stack.addWidget(self.lesson_1_widget)
        self.stack.addWidget(self.lesson_2_widget)
        self.stack.addWidget(self.lesson_3_widget)
        self.stack.setCurrentWidget(self.lesson_selector)
        self.stack.addWidget(self.results_widget)
        self.setLayout(self.stack)
