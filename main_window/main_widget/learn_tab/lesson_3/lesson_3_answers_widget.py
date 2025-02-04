import logging
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.learn_tab.base_classes.base_answers_widget import (
    BaseAnswersWidget,
)
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_3.lesson_3_widget import (
        Lesson3Widget,
    )
logger = logging.getLogger(__name__)


class Lesson3AnswersWidget(BaseAnswersWidget):
    """Widget responsible for displaying pictograph answers in Lesson 3."""

    def __init__(self, lesson_3_widget: "Lesson3Widget"):
        super().__init__(lesson_3_widget)
        self.lesson_3_widget = lesson_3_widget
        self.key_generator = self.main_widget.pictograph_key_generator

        self.layout: QGridLayout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.pictograph_views: list[QWidget] = []
        self.pictographs: dict[str, BasePictograph] = {}
        # Define grid parameters
        self.columns = 2  # Number of columns in the grid
        self.spacing = 30  # Spacing between widgets

        self.layout.setSpacing(self.spacing)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def display_answers(
        self, pictographs: list[dict], correct_pictograph: dict, check_answer_callback
    ):
        """Display the pictographs as answer options in a grid layout."""
        self.clear()

        num_pictographs = len(pictographs)
        rows = (num_pictographs + self.columns - 1) // self.columns  # Ceiling division

        for index, pictograph_dict in enumerate(pictographs):
            key = self.key_generator.generate_pictograph_key(pictograph_dict)
            pictograph = BasePictograph(self.lesson_3_widget.main_widget)
            view = LessonPictographView(pictograph)
            pictograph.view = view
            pictograph.disable_gold_overlay = False
            pictograph.updater.update_pictograph(pictograph_dict)
            pictograph.view.update_borders()
            self.pictographs[key] = pictograph
            # Configure view properties
            view.setCursor(Qt.CursorShape.PointingHandCursor)
            pictograph.quiz_mode = True
            pictograph.tka_glyph.setVisible(False)

            # Connect click event
            # Use lambda with default arguments to capture current pictograph_dict and correct_pictograph
            view.mousePressEvent = (
                lambda event, opt=pictograph_dict: check_answer_callback(
                    opt, correct_pictograph
                )
            )

            # Add to the grid layout
            row = index // self.columns
            col = index % self.columns
            self.layout.addWidget(view, row, col)

            self.pictograph_views.append(view)


    def clear(self):
        """Clear all the displayed pictographs."""
        for view in self.pictograph_views:
            self.layout.removeWidget(view)
            view.deleteLater()
        self.pictograph_views.clear()
        self.pictographs.clear()


    def disable_answers(self, answer):
        """Disable a specific pictograph answer."""
        pictograph_key = self.key_generator.generate_pictograph_key(answer)
        wrong_answer = self.pictographs[pictograph_key]
        wrong_answer.view.setEnabled(False)
        wrong_answer.view.set_overlay_color("red")

    def resizeEvent(self,event):
        """Resize the pictograph views based on window size."""
        super().resizeEvent(event)
        for view in self.pictograph_views:
            size = int(self.main_widget.height() // 5)
            view.setFixedSize(size, size)
        spacing = self.main_widget.width() // 100
        self.layout.setSpacing(spacing)
