from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from .section_button import OptionPickerSectionButton
from .letter_types import LetterType


class OptionPickerSection(QWidget):
    def __init__(self, letter_type: str, parent=None):
        super().__init__(parent)
        self.letter_type = letter_type
        self.pictographs: List = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.header_button = OptionPickerSectionButton(self.letter_type)
        self.header_button.clicked.connect(self._toggle_section)
        layout.addWidget(self.header_button)

        self.pictograph_container = QWidget()
        self.pictograph_layout = QGridLayout(self.pictograph_container)
        self.pictograph_layout.setSpacing(8)
        self.pictograph_layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.pictograph_container)

        self.pictograph_container.setStyleSheet(
            """
            QWidget {
                background-color: rgba(248, 249, 250, 180);
                border: 1px solid rgba(222, 226, 230, 180);
                border-radius: 6px;
            }
        """
        )

    def _toggle_section(self):
        self.header_button.toggle_expansion()
        self.pictograph_container.setVisible(self.header_button.is_expanded)

    def add_pictograph(self, pictograph_frame):
        self.pictographs.append(pictograph_frame)
        self.update_layout()

    def clear_pictographs(self):
        for pictograph in self.pictographs:
            if pictograph is not None:
                pictograph.setParent(None)
        self.pictographs.clear()

    def update_layout(self):
        for i in reversed(range(self.pictograph_layout.count())):
            item = self.pictograph_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        columns = self._calculate_optimal_columns()
        for i, pictograph in enumerate(self.pictographs):
            row = i // columns
            col = i % columns
            self.pictograph_layout.addWidget(pictograph, row, col)

    def _calculate_optimal_columns(self) -> int:
        parent_widget = self.parent()
        total_width = 700

        if parent_widget and hasattr(parent_widget, "width"):
            try:
                total_width = parent_widget.width()
                available_width = (total_width // 2) - 80
            except (AttributeError, TypeError):
                available_width = 700
        else:
            available_width = 700

        pictograph_width = 160 + 8

        if self.letter_type == LetterType.TYPE1:
            max_columns = min(6, available_width // pictograph_width)
        elif self.letter_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
            max_columns = min(4, available_width // pictograph_width)
        else:
            max_columns = min(5, available_width // pictograph_width)

        return max(2, max_columns)
