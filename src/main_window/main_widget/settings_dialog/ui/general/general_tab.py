# src/main_window/main_widget/settings_dialog/ui/general/general_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QSpinBox,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import Qt, pyqtSignal

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.modern_settings_dialog import (
        ModernSettingsDialog,
    )


class GeneralTab(QWidget):
    """General settings tab with cache configuration."""

    cache_settings_changed = pyqtSignal()

    def __init__(self, settings_dialog: "ModernSettingsDialog"):
        super().__init__()
        self.settings_dialog = settings_dialog
        self.settings_manager = settings_dialog.main_widget.settings_manager
        self.browse_settings = self.settings_manager.browse_tab_settings

        self._setup_ui()
        self._connect_signals()
        self._load_settings()

    def _setup_ui(self):
        """Set up the UI components with modern glassmorphism styling."""
        # Main layout with better spacing
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Create scroll area for better content management
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Content widget inside scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Cache Settings Group with modern styling
        cache_group = self._create_cache_settings_group()
        content_layout.addWidget(cache_group)

        # Add stretch to push content to top
        content_layout.addStretch()

        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

    def _create_cache_settings_group(self) -> QGroupBox:
        """Create simplified browse tab settings group."""
        group = QGroupBox("Browse Tab Settings")
        layout = QVBoxLayout(group)
        layout.setSpacing(15)

        # Simplified message
        info_label = QLabel(
            "Browse tab now uses simplified high-quality image rendering.\n"
            "All images are processed with maximum quality settings automatically."
        )
        info_label.setStyleSheet("QLabel { color: #666; font-style: italic; }")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        return group

    def _connect_signals(self):
        """Connect UI signals to handlers - simplified without cache."""
        pass  # No cache settings to connect

    def _load_settings(self):
        """Load current settings into UI - simplified without cache."""
        pass  # No cache settings to load

    def update_general_tab_from_settings(self):
        """Update the tab when it becomes active - simplified without cache."""
        self._load_settings()
