from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from main_window.main_widget.sequence_workbench.legacy_beat_frame.image_export_manager.image_export_manager import (
    ImageExportManager,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class ImageExportPreviewPanel(QFrame):
    def __init__(self, tab: "ImageExportTab"):
        super().__init__(tab)
        self.tab = tab
        self._setup_ui()

    def _setup_ui(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.preview_label, stretch=1)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def generate_preview_image(
        self, sequence: list[dict], options: dict[str, any]
    ) -> QPixmap:
        """Generate and properly scale the preview image while maintaining aspect ratio."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.image_export_manager: "ImageExportManager" = (
            self.tab.main_widget.sequence_workbench.beat_frame.image_export_manager
        )

        # Generate the image directly
        image = self.image_export_manager.image_creator.create_sequence_image(
            sequence, options
        )
        pixmap = QPixmap.fromImage(image)

        # Get the maximum allocated width and height for the preview panel
        max_width = self.width() * 0.95
        max_height = self.height() * 0.95

        # Determine the best size while keeping the aspect ratio
        scaled_pixmap = pixmap.scaled(
            int(max_width),
            int(max_height),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        QApplication.restoreOverrideCursor()
        return scaled_pixmap
