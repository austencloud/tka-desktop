from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtCore import Qt
import logging

from base_widgets.pictograph.pictograph_scene import PictographScene
from main_window.main_widget.learn_tab.base_classes.base_answers_widget import BaseAnswersWidget
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_3.lesson_3_widget import Lesson3Widget

logger = logging.getLogger(__name__)


class Lesson3AnswersWidget(BaseAnswersWidget):
    """Widget responsible for displaying pictograph answers in Lesson 3."""
    columns = 2
    spacing = 30
    pictographs: dict[str, PictographScene]

    def __init__(self, lesson_3_widget: "Lesson3Widget"):
        super().__init__(lesson_3_widget)
        self.lesson_3_widget = lesson_3_widget
        self.key_generator = self.main_widget.pictograph_key_generator
        self.layout: QGridLayout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.pictograph_views: List[LessonPictographView] = []
        self.pictographs: dict[str, PictographScene] = {}
        self.layout.setSpacing(self.spacing)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def create_answer_buttons(
        self,
        pictograph_data_list: List[dict],
        correct_pictograph: dict,
        check_answer_callback,
    ) -> None:
        """Initial creation of answer buttons."""
        self.clear()
        for index, pictograph_data in enumerate(pictograph_data_list):
            key = self.key_generator.generate_pictograph_key(pictograph_data)
            scene = PictographScene()
            view = LessonPictographView(scene)
            scene.elements.view = view
            scene.state.disable_gold_overlay = False
            scene.managers.updater.update_pictograph(pictograph_data)
            scene.elements.view.update_borders()
            scene.state.quiz_mode = True
            scene.elements.tka_glyph.setVisible(False)
            # Tag overlay items when created in set_overlay_color
            view.mousePressEvent = (
                lambda event, opt=pictograph_data: check_answer_callback(opt, correct_pictograph)
            )
            row = index // self.columns
            col = index % self.columns
            self.layout.addWidget(view, row, col)
            self.pictograph_views.append(view)
            self.pictographs[key] = scene

    def update_answer_buttons(
        self,
        pictograph_data_list: List[dict],
        correct_pictograph: dict,
        check_answer_callback,
    ) -> None:
        """
        Update the existing answer views with new pictograph data.
        This method reuses the existing four views instead of recreating them.
        """
        # If we don't yet have exactly 4 views, create them from scratch.
        if len(self.pictograph_views) != 4:
            self.create_answer_buttons(pictograph_data_list, correct_pictograph, check_answer_callback)
            return

        # First, remove any overlay items from each view's scene.
        for view in self.pictograph_views:
            scene = view.scene()
            for item in scene.items():
                if item.data(0) == "overlay":
                    scene.removeItem(item)
            view.setEnabled(True)

        # Clear out our dictionary so we can rebuild it.
        self.pictographs.clear()

        # Now update each view in place.
        for i, pictograph_data in enumerate(pictograph_data_list):
            key = self.key_generator.generate_pictograph_key(pictograph_data)
            view = self.pictograph_views[i]
            scene = view.pictograph  # Our persistent PictographScene attached to the view
            scene.state.disable_gold_overlay = False
            scene.managers.updater.update_pictograph(pictograph_data)
            scene.elements.view.update_borders()
            scene.state.quiz_mode = True
            scene.elements.tka_glyph.setVisible(False)
            view.mousePressEvent = (
                lambda event, opt=pictograph_data: check_answer_callback(opt, correct_pictograph)
            )
            self.pictographs[key] = scene

    def disable_answer(self, answer) -> None:
        """Disable a specific pictograph answer by setting its overlay to red."""
        pictograph_key = self.key_generator.generate_pictograph_key(answer)
        if pictograph_key in self.pictographs:
            scene = self.pictographs[pictograph_key]
            scene.elements.view.setEnabled(False)
            scene.elements.view.set_overlay_color("red")

    def clear(self) -> None:
        """Clear all the answer views."""
        for view in self.pictograph_views:
            self.layout.removeWidget(view)
            view.deleteLater()
        self.pictograph_views.clear()
        self.pictographs.clear()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        for view in self.pictograph_views:
            size = int(self.main_widget.height() // 5)
            view.setFixedSize(size, size)
        spacing = self.main_widget.width() // 100
        self.layout.setSpacing(spacing)
