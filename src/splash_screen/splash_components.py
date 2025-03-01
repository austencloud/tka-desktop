from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from main_window.main_widget.rainbow_progress_bar import (
    RainbowProgressBar,
)
from utils.path_helpers import get_data_path, get_image_path

if TYPE_CHECKING:
    from .splash_screen import SplashScreen


class SplashComponents:
    """Creates and initializes the main components for the splash screen."""

    def __init__(self, splash_screen: "SplashScreen"):
        self.splash_screen = splash_screen
        self.splash_screen.title_label = self._create_title_label()
        self.splash_screen.currently_loading_label = self._create_label(
            "Importing modules..."
        )
        self.splash_screen.created_by_label = self._create_label(
            "Created by Austen Cloud", bold=True
        )
        self.splash_screen.progress_bar = self._create_progress_bar()
        self.splash_screen.logo_label = self._setup_logo()

    def _create_title_label(self) -> QLabel:
        title_font = QFont("Monotype Corsiva", self.splash_screen.height() // 10)
        title_label = QLabel("The\nKinetic\nConstructor")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(title_font)
        return title_label

    def _create_label(self, text: str, bold: bool = False) -> QLabel:
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Georgia", self.splash_screen.height() // 40)
        font.setBold(bold)
        label.setFont(font)
        return label

    def _create_progress_bar(self) -> RainbowProgressBar:
        progress_bar = RainbowProgressBar(self.splash_screen)
        progress_bar.progress_bar.setMaximum(100)
        progress_bar.set_value(0)
        font = QFont("Monotype Corsiva")
        font.setPointSize(self.splash_screen.width() // 40)
        progress_bar.percentage_label.setFont(font)
        return progress_bar

    def _setup_logo(self) -> QLabel:
        splash_pix = QPixmap(get_image_path("splash_screen.png"))
        available_width = self.splash_screen.width() // 2
        available_height = self.splash_screen.height()
        scaled_splash_pix = splash_pix.scaled(
            available_width, available_height, Qt.AspectRatioMode.KeepAspectRatio
        )

        logo_label = QLabel()
        logo_label.setPixmap(scaled_splash_pix)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setMaximumSize(available_width, available_height)
        return logo_label
