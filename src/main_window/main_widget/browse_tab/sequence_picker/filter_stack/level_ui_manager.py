from functools import partial
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt

from styles.styled_button import StyledButton


if TYPE_CHECKING:
    from .filter_by_level_section import FilterByLevelSection
    from .level_data_manager import LevelDataManager
    from .level_image_handler import LevelImageHandler


class LevelUIManager:
    LEVEL_DESCRIPTIONS: dict[int, str] = {
        1: "Base letters with no turns.",
        2: "Turns added with only radial orientations.",
        3: "Non-radial orientations.",
    }
    AVAILABLE_LEVELS: list[int] = [1, 2, 3]

    def __init__(
        self,
        filter_section: "FilterByLevelSection",
        data_manager: "LevelDataManager",
        image_handler: "LevelImageHandler",
    ):
        self.filter_section = filter_section
        self.data_manager = data_manager
        self.image_handler = image_handler
        self.buttons: dict[int, StyledButton] = {}
        self.description_labels: dict[int, QLabel] = {}
        self.tally_labels: dict[int, QLabel] = {}

    def setup_ui(self) -> None:
        self.filter_section.go_back_button.show()
        self.filter_section.header_label.show()
        layout: QVBoxLayout = self.filter_section.layout()

        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.setHorizontalSpacing(50)
        grid_layout.setVerticalSpacing(30)

        for col, level in enumerate(self.AVAILABLE_LEVELS):
            level_vbox = self._create_level_vbox(level)
            grid_layout.addLayout(level_vbox, 0, col)

        layout.addLayout(grid_layout)
        layout.addStretch(1)

    def _create_level_vbox(self, level: int) -> QVBoxLayout:
        level_vbox = QVBoxLayout()
        level_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = self._create_level_button(level)
        description_label = self._create_description_label(level)
        image_placeholder = self.image_handler.create_image_placeholder(level)
        sequence_count_label = self._create_sequence_count_label(level)

        level_vbox.addWidget(button)
        level_vbox.addWidget(description_label)
        level_vbox.addItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )
        level_vbox.addWidget(image_placeholder)
        level_vbox.addWidget(sequence_count_label)

        return level_vbox

    def _create_level_button(self, level: int) -> StyledButton:
        button = StyledButton(f"Level {level}")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(partial(self.filter_section.handle_level_click, level))
        self.buttons[level] = button
        return button

    def _create_description_label(self, level: int) -> QLabel:
        description_label = QLabel(self.LEVEL_DESCRIPTIONS.get(level, ""))
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_labels[level] = description_label
        return description_label

    def _create_sequence_count_label(self, level: int) -> QLabel:
        count = self.data_manager.get_sequence_counts_per_level().get(level, 0)
        sequence_text = "sequence" if count == 1 else "sequences"
        label = QLabel(f"{count} {sequence_text}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tally_labels[level] = label
        return label
