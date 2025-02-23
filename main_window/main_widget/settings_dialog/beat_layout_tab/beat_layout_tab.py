from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .layout_controls_widget import LayoutControlsWidget
from .layout_beat_frame import LayoutBeatFrame

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class BeatLayoutTab(QWidget):
    num_beats: int = 16

    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self.sequence_workbench = self.main_widget.sequence_workbench
        self.layout_settings = self.main_widget.settings_manager.sequence_layout
        self.beat_frame = LayoutBeatFrame(self)
        self.controls = LayoutControlsWidget(self)
        self.beat_frame.update_preview()

        self.controls.layout_selected.connect(self._on_layout_selected)

        self._setup_layout()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.controls)
        layout.addWidget(self.beat_frame, stretch=1)
        self.setLayout(layout)

    def _on_layout_selected(self, layout_text: str):
        if layout_text:
            rows, cols = map(int, layout_text.split(" x "))
            self.beat_frame.current_layout = (rows, cols)
            self.beat_frame.update_preview()

