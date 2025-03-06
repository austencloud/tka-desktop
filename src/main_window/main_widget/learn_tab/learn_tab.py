from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QStackedLayout
from main_window.main_widget.learn_tab.lesson_configs import LESSON_CONFIGS
from .lesson_selector.lesson_selector import LessonSelector
from .lesson_widget.lesson_results_widget import LessonResultsWidget
from .lesson_widget.lesson_widget import LessonWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LearnTab(QWidget):
    """Widget for the learning module, managing lesson selection and individual lessons."""

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_widget.splash.updater.update_progress("LearnTab")
        self.lessons: dict[str, LessonWidget] = {}
        self.stack = QStackedLayout()
        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.lesson_selector = LessonSelector(self)
        self.results_widget = LessonResultsWidget(self)

        for lesson_type, config in LESSON_CONFIGS.items():
            self.lessons[lesson_type] = LessonWidget(
                self, lesson_type=lesson_type, **config
            )

    def _setup_layout(self) -> None:
        self.stack.addWidget(self.lesson_selector)
        for lesson in self.lessons.values():
            self.stack.addWidget(lesson)
        self.stack.addWidget(self.results_widget)
        self.stack.setCurrentWidget(self.lesson_selector)
        self.setLayout(self.stack)
