from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
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
    from legacy.src.main_window.main_widget.settings_dialog.legacy_settings_dialog import (
        LegacySettingsDialog,
    )


class ImageExportTab(QWidget):

    def __init__(self, settings_dialog: "LegacySettingsDialog"):
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget

        # Get settings_manager from dependency injection system
        try:
            self.settings_manager = self.main_widget.app_context.settings_manager
        except AttributeError:
            # Fallback for cases where app_context is not available during initialization
            self.settings_manager = None
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "settings_manager not available during ImageExportTab initialization"
            )

        self.control_panel = ImageExportControlPanel(self.settings_manager, self)
        self.preview_panel = ImageExportPreviewPanel(self)
        self.spinner = WaitingSpinner(self.preview_panel)

        self.control_panel.settingChanged.connect(self.update_preview)

        # CONNECT THE SEQUENCE UPDATE SIGNAL TO update_preview
        try:
            sequence_workbench = self.main_widget.widget_manager.get_widget(
                "sequence_workbench"
            )
            if sequence_workbench and hasattr(sequence_workbench, "beat_frame"):
                sequence_workbench.beat_frame.updateImageExportPreview.connect(
                    self.update_preview
                )
        except AttributeError:
            # Fallback when sequence_workbench not available
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "sequence_workbench not available during ImageExportTab initialization"
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
        """Set up the layout with modern glassmorphism styling."""
        # Main layout with improved spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Control panel container with glassmorphism background
        control_container = QWidget()
        control_container.setObjectName("control_container")
        control_container.setStyleSheet(
            """
            QWidget#control_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(31, 41, 59, 0.1),
                    stop:1 rgba(55, 65, 81, 0.08));
                border: 1px solid rgba(75, 85, 99, 0.3);
                border-radius: 12px;
                padding: 16px;
            }
            """
        )

        control_layout = QVBoxLayout(control_container)
        control_layout.setContentsMargins(16, 16, 16, 16)
        control_layout.addWidget(self.control_panel)

        main_layout.addWidget(control_container)

        # Preview panel container with glassmorphism background
        preview_container = QWidget()
        preview_container.setObjectName("preview_container")
        preview_container.setStyleSheet(
            """
            QWidget#preview_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(31, 41, 59, 0.05),
                    stop:1 rgba(55, 65, 81, 0.03));
                border: 1px solid rgba(75, 85, 99, 0.15);
                border-radius: 16px;
                padding: 20px;
            }
            """
        )

        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        preview_layout.addWidget(self.preview_panel)

        main_layout.addWidget(preview_container, stretch=3)

        self.setLayout(main_layout)

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
        try:
            sequence_workbench = self.main_widget.widget_manager.get_widget(
                "sequence_workbench"
            )
            if sequence_workbench and hasattr(sequence_workbench, "beat_frame"):
                return (
                    sequence_workbench.beat_frame.json_manager.loader_saver.load_current_sequence()
                )
            else:
                # Fallback: return empty sequence
                return []
        except AttributeError:
            # Fallback when sequence_workbench not available
            return []

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_preview()

    def update_image_export_tab_from_settings(self):
        for button_text, _ in self.control_panel.button_settings_keys.items():
            button = self.control_panel.buttons[button_text]
            button.update_is_toggled()
        self.control_panel._load_user_profiles()
        self.control_panel._load_saved_note()  # Load note instead of notes
        self.control_panel._load_directory_preference()  # Load directory preference

    def showEvent(self, event: "QShowEvent"):
        self.update_image_export_tab_from_settings()
        self.update_preview()
        super().showEvent(event)
