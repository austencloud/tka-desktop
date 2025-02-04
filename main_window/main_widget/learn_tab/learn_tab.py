from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QStackedLayout
from .lesson_selector import LessonSelector
from .lesson_1.lesson_1_widget import Lesson1Widget
from .lesson_2.lesson_2_widget import Lesson2Widget
from .lesson_3.lesson_3_widget import Lesson3Widget
from .codex.codex import Codex

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LearnTab(QWidget):
    """Widget for the learning module, managing lesson selection and individual lessons."""

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.lesson_selector = LessonSelector(self)
        self.lesson_1_widget = Lesson1Widget(self)
        self.lesson_2_widget = Lesson2Widget(self)
        self.lesson_3_widget = Lesson3Widget(self)
        self.codex = Codex(self)
        
    def _setup_layout(self) -> None:
        self.stack = QStackedLayout()
        self.stack.addWidget(self.lesson_selector)
        self.stack.addWidget(self.lesson_1_widget)
        self.stack.addWidget(self.lesson_2_widget)
        self.stack.addWidget(self.lesson_3_widget)
        self.stack.setCurrentWidget(self.lesson_selector)
        self.setLayout(self.stack)
