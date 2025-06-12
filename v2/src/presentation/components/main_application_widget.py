from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ...core.dependency_injection.simple_container import get_container
from ...core.interfaces.settings_interfaces import (
    ISettingsService,
    ISettingsDialogService,
)
from ...application.services.settings_service import SettingsService
from ...application.services.settings_dialog_service import SettingsDialogService
from ..components.ui.settings.settings_button import SettingsButton


class MainApplicationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_dependency_injection()
        self._setup_ui()
        self._apply_styling()

    def _setup_dependency_injection(self):
        """Setup dependency injection container with services"""
        container = get_container()

        # Register services
        container.register_singleton(ISettingsService, SettingsService)
        container.register_transient(ISettingsDialogService, SettingsDialogService)

        # Resolve services
        self.settings_service = container.resolve(ISettingsService)
        self.settings_dialog_service = SettingsDialogService(
            self.settings_service, self
        )

    def _setup_ui(self):
        """Setup the main UI layout"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Top bar with title and settings button (mimicking v1 structure)
        top_bar = QHBoxLayout()

        # Title
        title = QLabel("Kinetic Constructor v2")
        title.setObjectName("main_title")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))

        # Settings button positioned like in v1 (top-right)
        self.settings_button = SettingsButton()
        self.settings_button.settings_requested.connect(self._show_settings)

        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addWidget(self.settings_button)

        main_layout.addLayout(top_bar)

        # Main content area
        content_area = QWidget()
        content_area.setObjectName("content_area")
        content_layout = QVBoxLayout(content_area)

        welcome_label = QLabel("Welcome to the modern v2 architecture!")
        welcome_label.setObjectName("welcome_label")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setFont(QFont("Arial", 16))

        content_layout.addWidget(welcome_label)
        content_layout.addStretch()

        main_layout.addWidget(content_area, stretch=1)

    def _apply_styling(self):
        """Apply modern glassmorphism styling"""
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 23, 42, 0.95),
                    stop:0.5 rgba(30, 41, 59, 0.95),
                    stop:1 rgba(51, 65, 85, 0.95));
            }
            
            QLabel#main_title {
                color: white;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            
            QWidget#content_area {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                margin: 20px 0;
            }
            
            QLabel#welcome_label {
                color: rgba(255, 255, 255, 0.9);
                padding: 40px;
            }
        """
        )

    def _show_settings(self):
        """Show the settings dialog"""
        self.settings_dialog_service.show_settings_dialog()

    def closeEvent(self, event):
        """Handle application close"""
        self.settings_service.save_settings()
        super().closeEvent(event)
