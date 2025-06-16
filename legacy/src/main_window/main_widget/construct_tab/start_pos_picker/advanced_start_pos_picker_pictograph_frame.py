from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from typing import TYPE_CHECKING
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.advanced_start_pos_picker.advanced_start_pos_picker import (
        AdvancedStartPosPicker,
    )


class AdvancedStartPosPickerPictographFrame(QWidget):
    def __init__(self, advanced_start_pos_picker: "AdvancedStartPosPicker"):
        super().__init__(advanced_start_pos_picker)
        self.advanced_start_pos_picker = advanced_start_pos_picker
        self.clickable_option_handler = (
            self.advanced_start_pos_picker.construct_tab.click_handler
        )
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.pictographs_layout = QHBoxLayout()
        self.layout.addLayout(self.pictographs_layout)
        self.variation_buttons: dict[str, QPushButton] = {}
        self.start_positions: dict[str, LegacyPictograph] = {}
