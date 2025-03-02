from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.settings_dialog.ui.beat_layout.layout_controls.layout_controls import (
    LayoutControls,
)


from .layout_beat_frame.layout_beat_frame import LayoutBeatFrame

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class BeatLayoutTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self.layout_settings = self.main_widget.settings_manager.sequence_layout

        self.beat_frame = LayoutBeatFrame(self)
        self.controls = LayoutControls(self)
        self._connect_signals()
        self._setup_layout()

    def showEvent(self, a0):
        self.num_beats = (
            self.main_widget.sequence_workbench.sequence_beat_frame.get.beat_count()
        )
        default_layout = self.layout_settings.get_layout_setting(str(self.num_beats))
        self.beat_frame.current_layout = tuple(default_layout)
        self.controls.length_selector.num_beats_spinbox.setValue(self.num_beats)

        self.beat_frame.update_preview()
        return super().showEvent(a0)

    def _connect_signals(self):
        self.controls.layout_selected.connect(self._on_layout_selected)
        self.controls.sequence_length_changed.connect(self.on_sequence_length_changed)

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.controls)
        layout.addWidget(self.beat_frame, stretch=1)
        self.setLayout(layout)

    def _on_layout_selected(self, layout_text: str):
        if layout_text:
            rows, cols = map(int, layout_text.split(" x "))
            self.beat_frame.current_layout = (rows, cols)
            self.beat_frame.update_preview()

        # self.controls.default_layout_label.update_text(layout_text)

    def on_sequence_length_changed(self, new_length: int):
        self.controls = self.controls
        self.layout_dropdown = self.controls.layout_selector.layout_dropdown
        self.num_beats = new_length
        self.layout_dropdown.clear()
        layout_selector = self.controls.layout_selector
        layout_selector._update_valid_layouts(new_length)
        self.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in layout_selector.valid_layouts]
        )
        self.controls.layout_tab.beat_frame.current_layout = (
            self.layout_settings.get_layout_setting(str(self.num_beats))
        )
        layout_text = (
            f"{self.controls.layout_tab.beat_frame.current_layout[0]} x "
            f"{self.controls.layout_tab.beat_frame.current_layout[1]}"
        )
        self.layout_dropdown.setCurrentText(layout_text)

        self.controls.beat_frame.update_preview()
        self.controls.default_layout_label.setText(f"Default: {layout_text}")

    def update_beat_layout_tab(self):
        beat_count = (
            self.settings_dialog.main_widget.sequence_workbench.sequence_beat_frame.get.beat_count()
        )
        self.controls.layout_selector._update_valid_layouts(beat_count)
        self.controls.length_selector.num_beats_spinbox.setValue(beat_count)
