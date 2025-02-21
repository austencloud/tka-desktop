from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QWidget,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QRect, Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from main_window.settings_manager.settings_manager import SettingsManager


class StartupDialog(QDialog):
    def __init__(
        self, settings_manager: "SettingsManager", parent_window: "MainWidget"
    ) -> None:
        super().__init__(parent_window)
        self.setWindowTitle("Welcome to The Kinetic Constructor")
        self.settings_manager = settings_manager
        self.parent_window = parent_window

        layout = QVBoxLayout(self)

        # Image (Placeholder)
        label_image = QLabel(self)
        pixmap = QPixmap("path_to_maine_image.jpg")  # Replace with actual path
        label_image.setPixmap(pixmap)
        label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_image)

        # Welcome Message
        label_message = QLabel(
            "Thank you for using The Kinetic Constructor!\n"
            "This tool is still in development. Your support helps us grow!\n"
            "Explore the following resources to learn more."
        )
        label_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_message)

        # Links Section
        self.add_link(layout, "📖 Website: ", "https://thekineticalphabet.com")
        self.add_link(layout, "📂 GitHub: ", "https://github.com/thekineticalphabet")
        self.add_link(
            layout, "📷 Instagram: ", "https://instagram.com/thekineticalphabet"
        )
        self.add_link(layout, "💰 Donate: ", "https://paypal.me/thekineticalphabet")

        # Name Input Section
        self.label_name = QLabel("Enter your name (or stay Anonymous):", self)
        layout.addWidget(self.label_name)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        layout.addWidget(self.name_input)

        # "Don't Show Again" Checkbox
        self.checkbox = QCheckBox("Don't show this again", self)
        layout.addWidget(self.checkbox)

        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        self.anonymous_button = QPushButton("Use Anonymous")
        self.anonymous_button.clicked.connect(self.use_anonymous)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.anonymous_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.center_dialog(parent_window)

    def add_link(self, layout: QVBoxLayout, label_text: str, url: str) -> None:
        """Helper function to create clickable links."""
        label = QLabel(f'<a href="{url}">{label_text}{url}</a>', self)
        label.setOpenExternalLinks(True)
        layout.addWidget(label)

    def use_anonymous(self) -> None:
        self.name_input.setText("Anonymous")
        self.accept()

    def get_name(self) -> str:
        return self.name_input.text().strip()

    def center_dialog(self, parent_window: QWidget) -> None:
        """Centers the dialog relative to the given parent window."""
        parent_geometry: QRect = parent_window.geometry()
        dialog_width, dialog_height = 450, 400  # Expanded size for more content
        x = parent_geometry.x() + (parent_geometry.width() - dialog_width) // 2
        y = parent_geometry.y() + (parent_geometry.height() - dialog_height) // 2
        self.setGeometry(x, y, dialog_width, dialog_height)

    def accept(self) -> None:
        """Handle the 'Don't show again' checkbox on close."""
        if self.checkbox.isChecked():
            self.settings_manager.global_settings.set_show_welcome_screen(False)
        super().accept()
