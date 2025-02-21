from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from base_widgets.pictograph.pictograph_scene import PictographScene
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)

if TYPE_CHECKING:
    from .base_lesson_widget.base_lesson_widget import BaseLessonWidget


class BaseQuestionWidget(QWidget):
    letter_label: QLabel = None
    pictograph: PictographScene = None

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget
        self.main_widget = lesson_widget.main_widget
        self.layout: QVBoxLayout = None
        self.spacer: QSpacerItem = None


    def _resize_question_widget(self) -> None:
        raise NotImplementedError(
            "This function should be implemented by the subclass."
        )

    def _update_letter_label(self, letter: str) -> None:
        raise NotImplementedError(
            "This function should be implemented by the subclass."
        )

    def update_pictograph(self, pictograph_data) -> None:
        """
        Update the existing pictograph view with new data.
        If no view exists yet, create one.
        """
        if self.pictograph is None:
            self.pictograph = PictographScene()
            self.pictograph.elements.view = LessonPictographView(self.pictograph)
            self.layout.addWidget(
                self.pictograph.elements.view, alignment=Qt.AlignmentFlag.AlignCenter
            )
        self.pictograph.state.disable_gold_overlay = True
        self.pictograph.managers.updater.update_pictograph(pictograph_data)
        self.pictograph.elements.view.update_borders()
        self.pictograph.elements.tka_glyph.setVisible(False)


    def _resize_spacer(self) -> None:
        self.spacer.changeSize(
            20,
            self.main_widget.height() // 20,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )
