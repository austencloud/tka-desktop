from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDialog,
    QDialogButtonBox,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from main_window.main_widget.settings_dialog.ui.user_profile.profile_picture_manager import (
    ProfilePictureManager,
)


class ImageCropDialog(QDialog):
    """Dialog for cropping an image to a square."""

    def __init__(self, pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crop Profile Picture")
        self.original_pixmap = pixmap
        self.cropped_pixmap = ProfilePictureManager.crop_to_square(pixmap)
        self.circular_preview = None

        self._setup_ui()

    def _setup_ui(self):
        """Sets up the dialog UI."""
        layout = QVBoxLayout(self)

        # Preview label
        preview_layout = QHBoxLayout()

        # Original image preview
        original_frame = QFrame()
        original_frame.setFrameShape(QFrame.Shape.StyledPanel)
        original_frame.setFixedSize(200, 200)
        original_layout = QVBoxLayout(original_frame)

        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setFixedSize(180, 180)
        original_layout.addWidget(self.original_label)

        # Cropped preview
        cropped_frame = QFrame()
        cropped_frame.setFrameShape(QFrame.Shape.StyledPanel)
        cropped_frame.setFixedSize(200, 200)
        cropped_layout = QVBoxLayout(cropped_frame)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFixedSize(180, 180)
        cropped_layout.addWidget(self.preview_label)

        preview_layout.addWidget(original_frame)
        preview_layout.addWidget(cropped_frame)

        # Labels
        label_layout = QHBoxLayout()
        label_layout.addWidget(QLabel("Original Image"))
        label_layout.addWidget(QLabel("Cropped Preview"))

        # Update previews
        self._update_previews()

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Add layouts to main layout
        layout.addLayout(label_layout)
        layout.addLayout(preview_layout)
        layout.addWidget(button_box)

        self.setMinimumWidth(450)

    def _update_previews(self):
        """Updates the preview images."""
        # Scale original for display
        scaled_original = self.original_pixmap.scaled(
            180,
            180,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.original_label.setPixmap(scaled_original)

        # Display cropped circular preview
        self.circular_preview = ProfilePictureManager.create_circular_pixmap(
            self.cropped_pixmap, 180
        )
        self.preview_label.setPixmap(self.circular_preview)

    def get_cropped_pixmap(self) -> QPixmap:
        """Returns the cropped square pixmap."""
        return self.cropped_pixmap
