from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QWidget
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph

from PyQt6.QtCore import Qt

from base_widgets.pictograph.elements.views.lesson_pictograph_view import (
    LessonPictographView,
)


class PictographQuestionRenderer:
    """
    Renders a pictograph question.
    """

    def __init__(self, lesson_type: str):
        self.lesson_type = lesson_type
        self.widget = QWidget()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widget.setLayout(self.layout)

        self.pictograph = LegacyPictograph()
        self.view = LessonPictographView(self.pictograph)
        self.pictograph.elements.view = self.view
        self.pictograph.state.disable_gold_overlay = True
        self.pictograph.elements.view.setCursor(Qt.CursorShape.ArrowCursor)
        self.layout.addWidget(self.view)

    def get_widget(self):
        return self.widget

    def update_question(self, pictograph_data):
        """
        Updates the pictograph based on new question data.
        """
        self.pictograph.managers.updater.update_pictograph(pictograph_data)
        if self.lesson_type == "Lesson1":
            self.pictograph.state.hide_tka_glyph = True
        self.pictograph.elements.view.update_borders()
