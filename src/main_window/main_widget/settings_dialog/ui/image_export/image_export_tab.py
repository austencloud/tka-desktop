from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QShowEvent
from main_window.main_widget.settings_dialog.ui.image_export.image_export_preview_panel import (
    ImageExportPreviewPanel,
)
from main_window.main_widget.settings_dialog.ui.image_export.image_export_control_panel import (
    ImageExportControlPanel,
)
from main_window.main_widget.settings_dialog.ui.image_export.loading_spinner import (
    WaitingSpinner,
)


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class ImageExportTab(QWidget):

    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self.settings_manager = self.main_widget.settings_manager

        self.control_panel = ImageExportControlPanel(self.settings_manager, self)
        self.preview_panel = ImageExportPreviewPanel(self)
        self.spinner = WaitingSpinner(self.preview_panel)

        self.control_panel.settingChanged.connect(self.update_preview)

        # CONNECT THE SEQUENCE UPDATE SIGNAL TO update_preview
        self.main_widget.sequence_workbench.beat_frame.updateImageExportPreview.connect(
            self.update_preview
        )

        self._setup_layout()
        self._connect_signals()

    def update_preview(self):
        """Automatically update the preview when beats are modified."""
        if not self.isVisible():
            return

        # check the length of the current sequence. if It's less than 3, we want to show a placeholder in place of the preview.
        sequence_length = len(self._get_current_sequence())
        if sequence_length < 2:
            self.preview_panel.preview_label.clear()
            return

        # In ImageExportTab.update_preview()
        options = self.settings_manager.image_export.get_all_image_export_options()
        options["user_name"] = self.control_panel.user_combo_box.currentText()
        options["notes"] = (
            self.control_panel.note_input.text()
        )  # Use text field instead of combo box
        options["export_date"] = datetime.now().strftime("%m-%d-%Y")

        sequence = self._get_current_sequence()

        pixmap = self.preview_panel.generate_preview_image(sequence, options)

        self.preview_panel.preview_label.setPixmap(pixmap)

    def _setup_layout(self):
        card = QWidget(self)
        layout = QVBoxLayout(card)
        layout.addWidget(self.control_panel, 1)
        layout.addWidget(self.preview_panel, 3)

        control_layout = QHBoxLayout(self)
        control_layout.addWidget(card)
        self.setLayout(control_layout)

        self.center_spinner()
        self.spinner.hide()

    def _connect_signals(self):
        self.control_panel.settingChanged.connect(self.update_preview)

    def center_spinner(self):
        vertical_offset = 10
        self.spinner.move(
            (self.preview_panel.width() - self.spinner.width()) // 2,
            (self.preview_panel.height() - self.spinner.height()) // 2
            - vertical_offset,
        )

    def _get_current_sequence(self):
        return (
            self.main_widget.sequence_workbench.beat_frame.json_manager.loader_saver.load_current_sequence()
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_preview()

    def update_image_export_tab_from_settings(self):
        for button_text, _ in self.control_panel.button_settings_keys.items():
            button = self.control_panel.buttons[button_text]
            button.update_is_toggled()
        self.control_panel._load_user_profiles()
        self.control_panel._load_saved_note()  # Load note instead of notes

    def showEvent(self, event: "QShowEvent"):
        self.update_image_export_tab_from_settings()
        self.update_preview()
        super().showEvent(event)
