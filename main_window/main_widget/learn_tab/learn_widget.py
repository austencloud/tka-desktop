from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QStackedLayout,
)
from .lesson_1.lesson_1_widget import Lesson1Widget
from .lesson_2.lesson_2_widget import Lesson2Widget
from .lesson_3.lesson_3_widget import Lesson3Widget
from .lesson_selector import LessonSelector
from .codex.codex import Codex

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LearnTab(QWidget):
    """Widget for the learning module, managing lesson selection and individual lessons."""

    def __init__(self, main_widget: "MainWidget") -> None:
        """Initializes LearnTab with references to the main widget and settings."""
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.background_manager = None
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.lesson_selector = LessonSelector(self)
        self.lesson_1_widget = Lesson1Widget(self)
        self.lesson_2_widget = Lesson2Widget(self)
        self.lesson_3_widget = Lesson3Widget(self)
        self.codex = Codex(self)

    def _setup_layout(self) -> None:
        """Orchestrates creation of the main UI components and layout."""
        self._setup_stacked_layout()
        self._setup_right_side()
        self._setup_main_splitter()
        self._setup_main_layout()

    def _setup_stacked_layout(self) -> None:
        """Creates the QStackedLayout to hold the lesson selector and lesson widgets."""
        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(self.lesson_selector)
        self.stack_layout.addWidget(self.lesson_1_widget)
        self.stack_layout.addWidget(self.lesson_2_widget)
        self.stack_layout.addWidget(self.lesson_3_widget)
        self.stack_layout.setCurrentWidget(self.lesson_selector)

    def _setup_right_side(self) -> QWidget:
        """Creates the right-side widget, including the top bar and content frame."""
        self.right_side = QWidget()
        right_layout = QVBoxLayout(self.right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.codex.toggle_button)
        top_bar_layout.addStretch()
        right_layout.addLayout(top_bar_layout)

        content_frame = QFrame()
        content_frame.setLayout(self.stack_layout)
        right_layout.addWidget(content_frame)

    def _setup_main_splitter(self) -> None:
        """Sets up the main QSplitter, holding the Codex panel and right-side widget."""
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.codex, 1)
        self.main_layout.addWidget(self.right_side, 1)

    def _setup_main_layout(self) -> None:
        """Sets the final QVBoxLayout for the LearnTab."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.main_layout)
        self.setLayout(layout)
