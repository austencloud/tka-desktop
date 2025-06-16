# ori_picker_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import TYPE_CHECKING
from data.constants import IN, COUNTER, OUT, CLOCK
from src.legacy_settings_manager.global_settings.app_context import AppContext
from .ori_setter import OrientationSetter
from .ori_text_label import OrientationTextLabel
from .clickable_ori_label import ClickableOriLabel
from .rotate_buttons_widget import RotateButtonsWidget

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.widgets.option_picker_widget import (
        OptionPickerWidget,
    )
    from ..ori_picker_box import OriPickerBox


class OriPickerWidget(QWidget):
    """Minimalist widget that displays the orientation controls."""

    ori_adjusted = pyqtSignal(str)
    current_orientation_index = 0
    orientations = [IN, COUNTER, OUT, CLOCK]
    option_picker: "OptionPickerWidget" = None

    def __init__(self, ori_picker_box: "OriPickerBox") -> None:
        super().__init__(ori_picker_box)
        self.ori_picker_box = ori_picker_box
        self.color = self.ori_picker_box.color

        self.json_manager = AppContext.json_manager()
        self.json_validation_engine = self.json_manager.ori_validation_engine
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_workbench.beat_frame

        self.orientation_text_label = OrientationTextLabel(self)
        self.clickable_ori_label = ClickableOriLabel(self)
        self.rotate_buttons_widget = RotateButtonsWidget(self)
        self.ori_setter = OrientationSetter(self)

        self._setup_layout()

    def _setup_layout(self):
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        widgets = [
            self.orientation_text_label,
            self.clickable_ori_label,
            self.rotate_buttons_widget,
        ]

        for widget in widgets:
            layout.addStretch(1)
            layout.addWidget(widget)
        layout.addStretch(1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.orientation_text_label.resizeEvent(event)
        self.clickable_ori_label.resizeEvent(event)
