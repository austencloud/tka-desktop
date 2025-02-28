from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from main_window.main_widget.settings_dialog.card_frame import CardFrame
from main_window.main_widget.settings_dialog.ui.image_export.image_export_control_panel import (
    ImageExportControlPanel,
)
from main_window.main_widget.settings_dialog.ui.image_export.image_export_preview_panel import (
    ImageExportPreviewPanel,
)


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class ImageExportTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self.settings_manager = self.main_widget.settings_manager

        self.control_panel = ImageExportControlPanel(self)
        self.preview_panel = ImageExportPreviewPanel(self)

        self._setup_layout()
        self._connect_signals()

    def _setup_layout(self):
        card = CardFrame(self)
        layout = QHBoxLayout(card)
        layout.addWidget(self.control_panel, 1)
        layout.addWidget(self.preview_panel, 3)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(card)
        self.setLayout(main_layout)

    def _connect_signals(self):
        self.control_panel.settingChanged.connect(self._update_preview)

    def _update_preview(self):
        sequence = self._get_current_sequence()
        if sequence:
            options = self.settings_manager.image_export.get_all_settings()
            self.preview_panel.update_preview(
                include_start_pos=options.get("include_start_position", True),
                add_info=options.get("add_info", False),
                sequence=sequence,
                add_word=options.get("add_word", False),
                include_difficulty_level=options.get("add_difficulty_level", False),
                add_beat_numbers=options.get("add_beat_numbers", True),
                add_reversal_symbols=options.get("add_reversal_symbols", True),
            )

    def _get_current_sequence(self):
        return (
            self.main_widget.sequence_workbench.sequence_beat_frame.json_manager.load_current_sequence()
        )
