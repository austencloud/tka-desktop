from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QCheckBox
from PyQt6.QtGui import QPixmap, QGuiApplication
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_window import MainWindow
    from main_window.settings_manager.settings_manager import SettingsManager


class WelcomeDialog(QDialog):
    def __init__(
        self,
        settings_manager: "SettingsManager",
        main_window: "MainWindow",
        parent=None,
    ):
        super().__init__(parent)

        self.settings_manager = settings_manager
        self.main_window = main_window
        self.setWindowTitle("Welcome to the Beta")

        # Layout
        layout = QVBoxLayout(self)

        # Image (Placeholder for the image of Maine)
        label_image = QLabel(self)
        pixmap = QPixmap("path_to_maine_image.jpg")  # Replace with actual path to image
        label_image.setPixmap(pixmap)
        label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_image)

        # Beta message
        label_message = QLabel(
            "Thank you for using The Kinetic Constructor Beta!\n"
            "This product is still in development, and your feedback is valuable.\n"
            "Please consider providing feedback and supporting the project with a donation.",
            self,
        )
        label_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_message)

        # Checkbox to not show again
        # self.checkbox = QCheckBox("Don't show this again", self)
        # layout.addWidget(self.checkbox)

        # Donation button
        btn_donate = QPushButton("Donate", self)
        btn_donate.clicked.connect(self.on_donate)
        layout.addWidget(btn_donate)

        # Close button
        btn_close = QPushButton("Close", self)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

        self.setLayout(layout)

        # Ensure the dialog is shown on the same screen as the main window
        self.position_on_main_window_screen()

    def position_on_main_window_screen(self):
        """Position the dialog on the same screen as the main window."""
        window_geometry = self.main_window.geometry()
        screen = QGuiApplication.screenAt(window_geometry.center())
        if screen:
            available_geometry = screen.availableGeometry()
            self.setGeometry(
                available_geometry.x()
                + (available_geometry.width() - self.width()) // 2,
                available_geometry.y()
                + (available_geometry.height() - self.height()) // 2,
                self.width(),
                self.height(),
            )

    def accept(self):
        """Handle the 'Don't show again' checkbox on close."""
        # if self.checkbox.isChecked():
        #     self.settings_manager.global_settings.set_show_welcome_screen(False)
        super().accept()

    def on_donate(self):
        """Open the donation page or show donation options."""
        print("Opening donation page...")
