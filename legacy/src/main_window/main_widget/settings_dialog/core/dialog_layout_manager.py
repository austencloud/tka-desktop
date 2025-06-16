"""
Dialog layout manager for the modern settings dialog.

Handles UI layout creation and management.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QStackedWidget, 
    QWidget, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
import logging

if TYPE_CHECKING:
    from src.core.application_context import ApplicationContext
    from ..ui.settings_dialog_sidebar import SettingsDialogSidebar
    from ..components.modern_action_buttons import ModernActionButtons

logger = logging.getLogger(__name__)


class DialogLayoutManager:
    """
    Manages dialog layout creation and organization.
    
    Responsibilities:
    - Create main layout structure
    - Setup header with title and close button
    - Create content area (sidebar + tabs)
    - Organize layout hierarchy
    """

    def __init__(self, dialog: QDialog, app_context: "ApplicationContext" = None):
        self.dialog = dialog
        self.app_context = app_context
        
        # Layout components
        self.main_container: QWidget = None
        self.sidebar: "SettingsDialogSidebar" = None
        self.content_area: QStackedWidget = None
        self.action_buttons: "ModernActionButtons" = None
        self.close_button: QPushButton = None

    def setup_layout(self) -> dict:
        """
        Setup the complete dialog layout.
        
        Returns:
            Dictionary containing layout components for coordinator access
        """
        logger.debug("Setting up modern UI layout...")

        # Main layout with no margins for frameless design
        main_layout = QVBoxLayout(self.dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create main container with glassmorphism background
        self.main_container = QWidget()
        self.main_container.setObjectName("main_container")
        container_layout = QVBoxLayout(self.main_container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(20)

        # Create header
        header_layout = self._create_header()
        container_layout.addLayout(header_layout)

        # Create content area
        content_layout = self._create_content_area()
        container_layout.addLayout(content_layout, stretch=1)

        # Create action buttons
        self._create_action_buttons()
        container_layout.addWidget(self.action_buttons)

        # Add container to main layout
        main_layout.addWidget(self.main_container)

        logger.debug("Modern UI layout setup complete")

        # Return components for coordinator access
        return {
            'main_container': self.main_container,
            'sidebar': self.sidebar,
            'content_area': self.content_area,
            'action_buttons': self.action_buttons,
            'close_button': self.close_button
        }

    def _create_header(self) -> QHBoxLayout:
        """Create the dialog header with title and close button."""
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title_label = QLabel("Settings")
        title_label.setObjectName("dialog_title")
        title_label.setStyleSheet(
            """
            QLabel#dialog_title {
                font-size: 24px;
                font-weight: 700;
                color: rgba(255, 255, 255, 0.95);
                margin: 0px;
                padding: 0px;
            }
        """
        )
        header_layout.addWidget(title_label)

        # Spacer
        header_layout.addStretch()

        # Custom close button
        self.close_button = self._create_close_button()
        header_layout.addWidget(self.close_button)

        return header_layout

    def _create_close_button(self) -> QPushButton:
        """Create the custom close button."""
        close_button = QPushButton("✕")
        close_button.setObjectName("close_button")
        close_button.setFixedSize(32, 32)
        close_button.setStyleSheet(
            """
            QPushButton#close_button {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#close_button:hover {
                background: rgba(239, 68, 68, 0.8);
                border: 1px solid rgba(239, 68, 68, 0.9);
                color: rgba(255, 255, 255, 1.0);
            }
            QPushButton#close_button:pressed {
                background: rgba(220, 38, 38, 0.9);
            }
        """
        )
        return close_button

    def _create_content_area(self) -> QHBoxLayout:
        """Create the content area with sidebar and tab content."""
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Create sidebar (will be populated by tab manager)
        self._create_sidebar()
        content_layout.addWidget(self.sidebar)

        # Create stacked widget for tab content
        self.content_area = QStackedWidget()
        self.content_area.setMinimumWidth(500)
        content_layout.addWidget(self.content_area, stretch=1)

        return content_layout

    def _create_sidebar(self):
        """Create the settings dialog sidebar."""
        # Import here to avoid circular imports
        try:
            from ..ui.settings_dialog_sidebar import SettingsDialogSidebar
            self.sidebar = SettingsDialogSidebar(self.dialog)
        except ImportError:
            # Fallback to simple list widget
            from PyQt6.QtWidgets import QListWidget
            self.sidebar = QListWidget(self.dialog)
            logger.warning("Using fallback sidebar implementation")

        self.sidebar.setMinimumWidth(240)
        self.sidebar.setMaximumWidth(280)
        self.sidebar.setFixedWidth(260)  # Fixed width for consistent layout

    def _create_action_buttons(self):
        """Create the action buttons."""
        from ..components.modern_action_buttons import ModernActionButtons
        self.action_buttons = ModernActionButtons(self.app_context)
