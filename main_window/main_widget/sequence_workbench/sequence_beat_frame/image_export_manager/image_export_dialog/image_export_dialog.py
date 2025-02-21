from datetime import datetime
import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QSizePolicy,
    QCheckBox,
    QLabel,
    QComboBox,
    QLineEdit,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QResizeEvent

from main_window.settings_manager.global_settings.app_context import AppContext
from .export_dialog_control_panel import ExportDialogControlPanel
from .export_dialog_preview_panel import ExportDialogPreviewPanel
from sequence_sharer_dialog.sequence_sharer_dialog import SequenceSharerDialog

if TYPE_CHECKING:
    from ..image_export_manager import ImageExportManager


class ImageExportDialog(QDialog):
    def __init__(self, export_manager: "ImageExportManager", sequence: list[dict]):
        super().__init__(export_manager.main_widget)
        self.export_manager = export_manager
        self.sequence = sequence
        self.main_widget = export_manager.main_widget
        self.setWindowTitle("Save Image")
        self.setModal(True)

        self._setup_components()
        self._setup_layout()
        self._resize_image_export_dialog()

    def _setup_okay_cancel_buttons(self):
        """Setup Save, Cancel, and Share buttons with dynamic size."""
        self.ok_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)

        # connect the OK and cancel buttons to their respective functions
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # give them a pointed hand cursor
        self.ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Icon for the share button
        icon_path = os.path.join(
            "F:\\CODE\\tka-sequence-constructor\\images\\icons\\share.png"
        )
        self.share_button = QPushButton(QIcon(icon_path), "")
        self.share_button.setToolTip("Share this image")
        self.share_button.setIconSize(self.share_button.sizeHint())

        self.share_button.clicked.connect(self.open_sharer_dialog)
        self.share_button.setCursor(Qt.CursorShape.PointingHandCursor)

    def _setup_components(self):
        """Setup the components for the export dialog."""
        self.preview_panel = ExportDialogPreviewPanel(self)
        self.control_panel = ExportDialogControlPanel(self)
        self._setup_okay_cancel_buttons()

    def _setup_layout(self):
        """Setup the layout of the dialog with an HBox for control panel and preview panel."""
        # Horizontal layout for the control panel and preview panel
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.control_panel, 1)
        main_layout.addWidget(self.preview_panel, 3)

        # Button layout (Save, Cancel, Share) at the bottom
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        # button_layout.addWidget(self.share_button)

        # Main layout with buttons at the bottom
        layout = QVBoxLayout(self)
        layout.addLayout(main_layout, 1)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def open_sharer_dialog(self):
        """Open the SequenceSharerDialog to send the current preview image via email."""
        word = self.sequence[0]["word"]
        preview_image_path = f"{word}.png"
        pixmap = self.preview_panel.preview_image

        temp_image_path = os.path.join(os.getcwd(), f"{word}.png")

        if not pixmap.save(temp_image_path):
            QMessageBox.critical(
                self, "Save Error", "Failed to save the preview image."
            )
            return

        if not os.path.isfile(temp_image_path) or os.path.getsize(temp_image_path) == 0:
            QMessageBox.critical(self, "File Error", "File is invalid or empty.")
            return

        # Open the SequenceSharer dialog
        sharer_dialog = SequenceSharerDialog(self.main_widget, preview_image_path, word)
        sharer_dialog.exec()

        # Clean up the temporary image file after sending
        if os.path.exists(preview_image_path):
            os.remove(preview_image_path)

    def _resize_image_export_dialog(self):
        """Resize the dialog based on the parent window size."""
        main_width = self.main_widget.width()
        main_height = self.main_widget.height()
        self.resize(int(main_width // 1.5), int(main_height // 1.5))

    def update_export_setting_and_layout(self):
        """Update export settings and refresh the layout."""
        new_value = self.control_panel.include_start_pos_check.isChecked()
        self.export_manager.include_start_pos = new_value
        self.export_manager.settings_manager.image_export.set_image_export_setting(
            "include_start_position", new_value
        )
        # self.update_preview_based_on_options()

    def get_export_options(self):
        """Get the current export options."""
        current_date = datetime.now().strftime("%m-%d-%Y")
        current_date = "-".join([str(int(part)) for part in current_date.split("-")])
        return {
            "include_start_position": self.control_panel.include_start_pos_check.isChecked(),
            "add_info": self.control_panel.add_info_check.isChecked(),
            "add_word": self.control_panel.add_word_check.isChecked(),
            "user_name": self.control_panel.user_combo_box.currentText(),
            "export_date": current_date,
            "open_directory": self.control_panel.open_directory_check.isChecked(),
            "notes": self.control_panel.notes_combo_box.currentText(),
            "add_difficulty_level": self.control_panel.include_difficulty_level_check.isChecked(),
            "add_beat_numbers": self.control_panel.add_beat_numbers_check.isChecked(),
            "add_reversal_symbols": self.control_panel.add_reversal_symbols_check.isChecked(),
        }

    def showEvent(self, event):
        """Handle dialog show events."""
        super().showEvent(event)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self._resize_widgets()
        self.update_preview()
        self._resize_buttons()

    def _resize_widgets(self):
        font_size = int(self.height() * 0.025)
        for widget in self.control_panel.findChildren(QCheckBox):
            widget.setStyleSheet(f"font-size: {font_size}px;")
        for widget in self.control_panel.findChildren(QLabel):
            widget.setStyleSheet(f"font-size: {font_size}px;")
        for widget in self.control_panel.findChildren(QPushButton):
            widget.setStyleSheet(f"font-size: {font_size}px;")
        for widget in self.control_panel.findChildren(QComboBox):
            widget.setStyleSheet(f"font-size: {font_size}px;")
        for widget in self.preview_panel.findChildren(QLineEdit):
            widget.setStyleSheet(f"font-size: {font_size}px;")

    def update_preview(self):
        self.preview_panel.update_preview(
            self.control_panel.include_start_pos_check.isChecked(),
            self.control_panel.add_info_check.isChecked(),
            self.sequence,
            self.control_panel.add_word_check.isChecked(),
            self.control_panel.include_difficulty_level_check.isChecked(),
            self.control_panel.add_beat_numbers_check.isChecked(),
            self.control_panel.add_reversal_symbols_check.isChecked(),
        )

    def _resize_buttons(self):
        button_height = int(self.height() * 0.08)
        font_size = int(self.height() * 0.03)
        for button in [self.ok_button, self.cancel_button, self.share_button]:
            button.setFixedHeight(button_height)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            button.setStyleSheet(f"font-size: {font_size}px;")
