from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt
from ..base_classes.base_question_widget import BaseQuestionWidget

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.learn_tab import LearnTab


class Lesson3QuestionWidget(BaseQuestionWidget):
    """Widget for displaying the initial pictograph in Lesson 3."""

    def __init__(self, learn_widget: "LearnTab"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.pictograph = None
        self.question_label = QLabel("Choose the pictograph that can follow:")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._setup_layout()

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
            self.pictograph.elements.tka_glyph.setVisible(True)

    def clear(self) -> None:
        """Clear the current pictograph."""
        if self.pictograph:
            self.layout.removeWidget(self.pictograph.elements.view)
            self.pictograph.elements.view.deleteLater()
            self.pictograph = None

    def resizeEvent(self, event) -> None:
        self._resize_question_label()
        self._resize_pictograph()
        self._resize_spacer()

    def _resize_pictograph(self) -> None:
        if self.pictograph:
            size = int(self.main_widget.height() // 5)
            self.pictograph.elements.view.setFixedSize(size, size)
