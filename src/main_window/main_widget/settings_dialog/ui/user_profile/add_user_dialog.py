from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QDialog,
    QLineEdit,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from main_window.main_widget.settings_dialog.ui.user_profile.image_crop_dialog import (
    ImageCropDialog,
)
from main_window.main_widget.settings_dialog.ui.user_profile.profile_picture_manager import (
    ProfilePictureManager,
)


class AddUserDialog(QDialog):
    """Dialog for adding a new user with profile picture support."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New User")
        self.profile_pixmap = None
        self._setup_ui()

    def _setup_ui(self):
        """Sets up the user interface layout."""
        layout = QVBoxLayout(self)

        # User name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter user name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Profile picture selection
        pic_layout = QHBoxLayout()
        pic_label = QLabel("Profile Picture:")
        self.pic_button = QPushButton("Choose Image...")
        self.pic_button.clicked.connect(self._select_image)
        pic_layout.addWidget(pic_label)
        pic_layout.addWidget(self.pic_button)
        layout.addLayout(pic_layout)

        # Image preview
        self.preview_frame = QFrame()
        self.preview_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.preview_frame.setFixedSize(150, 150)
        preview_layout = QVBoxLayout(self.preview_frame)

        self.preview_label = QLabel("No image selected")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setWordWrap(True)
        preview_layout.addWidget(self.preview_label)

        layout.addWidget(self.preview_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setMinimumWidth(350)

    def _select_image(self):
        """Opens file dialog to select a profile picture."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Profile Picture",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
        )

        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Show crop dialog
                crop_dialog = ImageCropDialog(pixmap, self)
                if crop_dialog.exec() == QDialog.DialogCode.Accepted:
                    self.profile_pixmap = crop_dialog.get_cropped_pixmap()
                    self._update_preview()

    def _update_preview(self):
        """Updates the profile picture preview."""
        if self.profile_pixmap and not self.profile_pixmap.isNull():
            # Create circular preview
            circular_pixmap = ProfilePictureManager.create_circular_pixmap(
                self.profile_pixmap, 140
            )
            self.preview_label.setPixmap(circular_pixmap)
            self.preview_label.setText("")
        else:
            self.preview_label.setText("No image selected")
            self.preview_label.setPixmap(QPixmap())

    def get_user_info(self):
        """Returns the user name and profile picture."""
        return self.name_input.text().strip(), self.profile_pixmap
