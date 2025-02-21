from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from base_widgets.pictograph.pictograph_scene import PictographScene
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)
from main_window.main_widget.learn_tab.base_classes.base_question_widget import (
    BaseQuestionWidget,
)


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_1.lesson_1_widget import (
        Lesson1Widget,
    )


class Lesson1QuestionWidget(BaseQuestionWidget):
    """Widget for displaying the pictograph and managing its size and alignment."""

    def __init__(self, lesson_1_widget: "Lesson1Widget"):
        super().__init__(lesson_1_widget)
        self.lesson_1_widget = lesson_1_widget
        self.main_widget = lesson_1_widget.main_widget
        self.pictograph = None
        self._setup_label()
        self._setup_layout()

        # Animation-related properties
        self.fade_out_animation = None
        self.fade_in_animation = None

    def _setup_label(self):
        self.question_label = QLabel("What letter matches the pictograph?")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.question_label)

        self.spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.layout.addItem(self.spacer)

        self.setLayout(self.layout)

    def update_pictograph(self, pictograph_data) -> None:
        """Load and display the pictograph."""
        super().update_pictograph(pictograph_data)
        if self.pictograph:
            self.pictograph.elements.tka_glyph.setVisible(False)

    def clear(self) -> None:
        """Remove the current pictograph view."""
        if self.pictograph:
            self.layout.removeWidget(self.pictograph.elements.view)
            self.pictograph.elements.view.deleteLater()
            self.pictograph = None

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._resize_question_label()
        self._resize_pictograph()
        self._resize_spacer()

    def _resize_pictograph(self) -> None:
        if self.pictograph:
            self.pictograph.elements.view.setFixedSize(
                self.main_widget.height() // 3, self.main_widget.height() // 3
            )
