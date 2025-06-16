import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

from src.legacy_settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_data_path

from .layout_dropdown import LayoutDropdown
from .select_layout_label import SelectLayoutLabel

if TYPE_CHECKING:
    from ..layout_controls import LayoutControls

BEAT_FRAME_LAYOUT_OPTIONS_PATH = get_data_path(
    "beat_frame_layout_options.json"
)


class LayoutSelector(QFrame):
    layout_selected = pyqtSignal(str)  # Changed from list to str

    def __init__(self, controls_widget: "LayoutControls"):
        super().__init__(controls_widget)
        self.controls_widget = controls_widget
        self.layout_tab = controls_widget.layout_tab
        self.select_layout_label = SelectLayoutLabel(self)
        self.layout_dropdown = LayoutDropdown(self)
        self._setup_layout()
        self._connect_signals()

    def showEvent(self, event):
        num_beats = int(AppContext.settings_manager().sequence_layout.get_num_beats())
        self._update_valid_layouts(num_beats)
        self.layout_dropdown._populate_dropdown()
        super().showEvent(event)

    def _update_valid_layouts(self, num_beats: int):
        beat_frame_layout_options = self.load_beat_frame_layout_options(
            BEAT_FRAME_LAYOUT_OPTIONS_PATH
        )
        self.valid_layouts = beat_frame_layout_options.get(num_beats, [(1, 1)])

    def load_beat_frame_layout_options(
        self, file_path: str
    ) -> dict[int, list[list[int]]]:

        try:
            with open(file_path, "r") as f:
                return {int(key): value for key, value in json.load(f).items()}
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Beat frame layout options file not found at {file_path}"
            )
            return {}

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.select_layout_label)
        self.layout.addWidget(self.layout_dropdown)

    def _connect_signals(self):
        self.layout_dropdown.current_layout_changed.connect(self.layout_selected.emit)

    def resizeEvent(self, event):
        self.layout.setSpacing(self.controls_widget.width() // 20)
        base_size = int(self.controls_widget.width() // 30)
        padding = int(base_size / 5)
        self.select_layout_label.setStyleSheet(
            f"""
            QLabel {{
                padding: {padding}px;
                font-size: {base_size}px;
            }}
            """
        )
        self.layout_dropdown.setStyleSheet(
            f"""
            QComboBox {{
                padding: {padding}px;
                min-width: {base_size * 3}px;
                font-size: {base_size}px;
            }}
            """
        )

    def current_layout(self):
        return self.layout_dropdown.currentText()
