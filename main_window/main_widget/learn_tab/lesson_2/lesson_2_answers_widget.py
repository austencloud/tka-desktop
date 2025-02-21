from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtCore import Qt
import logging

from base_widgets.pictograph.pictograph_scene import PictographScene
from main_window.main_widget.learn_tab.base_classes.base_answers_widget import (
    BaseAnswersWidget,
)
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_2.lesson_2_widget import Lesson2Widget

logger = logging.getLogger(__name__)


class Lesson2AnswersWidget(BaseAnswersWidget):
    columns = 2
    spacing = 30

    def __init__(self, lesson_2_widget: "Lesson2Widget"):
        super().__init__(lesson_2_widget)
        self.lesson_2_widget = lesson_2_widget
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
        self.clear()
        for i, data in enumerate(pictograph_data_list):
            key = self.key_generator.generate_pictograph_key(data)
            scene = PictographScene()
            view = LessonPictographView(scene)
            scene.elements.view = view
            scene.state.disable_gold_overlay = False
            scene.managers.updater.update_pictograph(data)
            scene.elements.view.update_borders()
            scene.state.quiz_mode = True
            scene.elements.tka_glyph.setVisible(False)
            view.mousePressEvent = (
                lambda event, opt=data: check_answer_callback(opt, correct_pictograph)
            )
            row, col = divmod(i, self.columns)
            self.layout.addWidget(view, row, col)
            self.pictograph_views.append(view)
            self.pictographs[key] = scene

    def update_answer_buttons(
        self,
        pictograph_data_list: List[dict],
        correct_pictograph: dict,
        check_answer_callback,
    ) -> None:
        if len(self.pictograph_views) != 4:
            self.create_answer_buttons(
                pictograph_data_list, correct_pictograph, check_answer_callback
            )
            return

        for view in self.pictograph_views:
            scene = view.scene()
            for item in scene.items():
                if item.data(0) == "overlay":
                    scene.removeItem(item)
            view.setEnabled(True)

        self.pictographs.clear()

        for i, data in enumerate(pictograph_data_list):
            key = self.key_generator.generate_pictograph_key(data)
            view = self.pictograph_views[i]
            scene = view.pictograph
            scene.state.disable_gold_overlay = False
            scene.managers.updater.update_pictograph(data)
            scene.elements.view.update_borders()
            scene.state.quiz_mode = True
            scene.elements.tka_glyph.setVisible(False)
            view.mousePressEvent = (
                lambda event, opt=data: check_answer_callback(opt, correct_pictograph)
            )
            self.pictographs[key] = scene

    def disable_answer(self, answer) -> None:
        key = self.key_generator.generate_pictograph_key(answer)
        if key in self.pictographs:
            view = self.pictographs[key].elements.view
            view.setEnabled(False)
            view.set_overlay_color("red")

    def clear(self) -> None:
        for view in self.pictograph_views:
            self.layout.removeWidget(view)
            view.deleteLater()
        self.pictograph_views.clear()
        self.pictographs.clear()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        size = int(self.main_widget.height() // 5)
        spacing = self.main_widget.width() // 100

        for view in self.pictograph_views:
            view.setFixedSize(size, size)
        self.layout.setSpacing(spacing)
