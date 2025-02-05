from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import (
    QGridLayout,
)
from PyQt6.QtCore import Qt
import logging

from base_widgets.base_pictograph.pictograph import Pictograph
from main_window.main_widget.learn_tab.base_classes.base_answers_widget import (
    BaseAnswersWidget,
)
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_2.lesson_2_widget import (
        Lesson2Widget,
    )

logger = logging.getLogger(__name__)


class Lesson2AnswersWidget(BaseAnswersWidget):
    """Widget responsible for displaying the pictograph answers in a grid layout."""

    columns = 2
    spacing = 30
    pictographs: dict[str, Pictograph]

    def __init__(self, lesson_2_widget: "Lesson2Widget"):
        super().__init__(lesson_2_widget)
        self.lesson_2_widget = lesson_2_widget
        self.key_generator = self.main_widget.pictograph_key_generator

        self.layout: QGridLayout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.pictograph_views: List[LessonPictographView] = []
        self.pictographs: dict[str, Pictograph] = {}

        self.layout.setSpacing(self.spacing)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def display_answers(
        self, pictographs: List[dict], correct_pictograph: dict, check_answer_callback
    ):
        """Display the pictographs as answer options in a grid layout."""
        self.clear()

        num_pictographs = len(pictographs)
        rows = (num_pictographs + self.columns - 1) // self.columns  # Ceiling division

        for index, pictograph_data in enumerate(pictographs):
            key = self.key_generator.generate_pictograph_key(pictograph_data)
            pictograph = Pictograph(self.lesson_2_widget.main_widget)
            view = LessonPictographView(pictograph)
            pictograph.view = view
            pictograph.disable_gold_overlay = False
            pictograph.updater.update_pictograph(pictograph_data)
            pictograph.view.update_borders()
            self.pictographs[key] = pictograph
            pictograph.quiz_mode = True
            pictograph.tka_glyph.setVisible(False)

            view.mousePressEvent = (
                lambda event, opt=pictograph_data: check_answer_callback(
                    opt, correct_pictograph
                )
            )
            row = index // self.columns
            col = index % self.columns
            self.layout.addWidget(view, row, col)

            self.pictograph_views.append(view)

    def disable_answers(self, answer):
        """Disable a specific pictograph answer."""
        pictograph_key = self.key_generator.generate_pictograph_key(answer)
        wrong_answer = self.pictographs[pictograph_key]
        wrong_answer.view.setEnabled(False)
        wrong_answer.view.set_overlay_color("red")

    def clear(self):
        """Clear all the displayed pictographs."""
        for view in self.pictograph_views:
            self.layout.removeWidget(view)
            view.deleteLater()
            logger.debug("Removed and deleted a pictograph view from the grid.")
        self.pictograph_views.clear()
        self.pictographs.clear()

    def resizeEvent(self, event):
        """Resize the pictograph views based on window size."""
        super().resizeEvent(event)
        for view in self.pictograph_views:
            size = int(self.main_widget.height() // 5)
            view.setFixedSize(size, size)
        spacing = self.main_widget.width() // 100
        self.layout.setSpacing(spacing)
