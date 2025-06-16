"""
Enhanced General Tab with modern UI, thumbnail quality settings, and comprehensive configuration.
"""

from typing import Optional, Dict, Any
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QFrame,
    QLineEdit,
)
import logging

from ...core.modern_components import (
    SettingCard,
    ModernToggle,
    ModernButton,
    ModernSlider,
    ModernComboBox,
    StatusIndicator,
    HelpTooltip,
)
from ...core.glassmorphism_styler import GlassmorphismStyler


class EnhancedGeneralTab(QWidget):
    """
    Enhanced General Tab with modern glassmorphism UI and comprehensive settings.
    Includes cache settings, thumbnail quality, performance, and application behavior.
    """

    # Signals for settings changes
    setting_changed = pyqtSignal(str, object, object)  # key, old_value, new_value

    def __init__(self, settings_manager, state_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.state_manager = state_manager
        self._controls = {}  # Store references to controls for easy access
        self._setup_ui()
        self._load_current_settings()
        self._setup_connections()

    def _setup_ui(self):
        """Setup the enhanced general tab UI with compact layout."""
        # Main layout with compact spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        # Create a compact content widget (no scroll area needed)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)  # Much tighter spacing

        # Create setting sections
        self._create_user_profile_section(content_layout)

        self._create_application_behavior_section(content_layout)

        # Add stretch to push content to top
        content_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        # Add content widget directly to main layout
        main_layout.addWidget(content_widget)

        # Apply styling
        self._apply_styling()

    def _create_user_profile_section(self, parent_layout):
        """Create user profile settings section."""
        card = SettingCard(
            "User Profile",
            "Configure your user name that appears on exported sequences and shared content.",
        )

        # User Name Input
        user_name_layout = QVBoxLayout()
        user_name_label = QLabel("User Name (appears on exported sequences):")
        user_name_label.setFont(GlassmorphismStyler.get_font("body_medium"))
        user_name_label.setStyleSheet(
            f"color: {GlassmorphismStyler.get_color('text_primary')};"
        )
        user_name_layout.addWidget(user_name_label)

        # Create a modern styled line edit for user name
        user_name_input_layout = QHBoxLayout()
        self._controls["user_name"] = QLineEdit()
        self._controls["user_name"].setPlaceholderText("Enter your name...")
        self._controls["user_name"].setMaxLength(50)  # Reasonable limit

        # Apply modern styling to the line edit
        self._controls["user_name"].setStyleSheet(
            f"""
            QLineEdit {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GlassmorphismStyler.get_color('surface', 0.6)},
                    stop:1 {GlassmorphismStyler.get_color('surface_light', 0.4)});
                border: 1px solid {GlassmorphismStyler.get_color('border', 0.4)};
                border-radius: {GlassmorphismStyler.RADIUS['md']}px;
                padding: {GlassmorphismStyler.SPACING['sm']}px {GlassmorphismStyler.SPACING['md']}px;
                color: {GlassmorphismStyler.get_color('text_primary')};
                font-size: {GlassmorphismStyler.FONTS['body_medium']['size']}px;
                min-height: 32px;
                selection-background-color: {GlassmorphismStyler.get_color('primary', 0.3)};
            }}
            QLineEdit:focus {{
                border: 2px solid {GlassmorphismStyler.get_color('primary', 0.8)};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GlassmorphismStyler.get_color('surface_light', 0.7)},
                    stop:1 {GlassmorphismStyler.get_color('surface_lighter', 0.5)});
            }}
            QLineEdit:hover {{
                border-color: {GlassmorphismStyler.get_color('border_light', 0.6)};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GlassmorphismStyler.get_color('surface_light', 0.6)},
                    stop:1 {GlassmorphismStyler.get_color('surface_lighter', 0.4)});
            }}
            """
        )

        user_name_input_layout.addWidget(self._controls["user_name"])
        user_name_input_layout.addWidget(
            HelpTooltip(
                "This name will appear on exported sequence images and when sharing sequences. "
                "Choose a name that identifies you to other users."
            )
        )
        user_name_input_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

        user_name_layout.addLayout(user_name_input_layout)
        card.add_layout(user_name_layout)

        parent_layout.addWidget(card)

    def _create_application_behavior_section(self, parent_layout):
        """Create application behavior settings section."""
        card = SettingCard(
            "Application Behavior",
            "Configure startup preferences and automatic features.",
        )

        # Auto-save Settings
        autosave_layout = QHBoxLayout()
        self._controls["autosave"] = ModernToggle("Auto-save Settings")
        autosave_layout.addWidget(self._controls["autosave"])
        autosave_layout.addWidget(
            HelpTooltip(
                "Automatically saves settings changes without requiring manual confirmation. "
                "Recommended for most users."
            )
        )
        autosave_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        card.add_layout(autosave_layout)

        # Backup Frequency
        backup_layout = QVBoxLayout()
        backup_label = QLabel("Automatic Backup Frequency:")
        backup_label.setFont(GlassmorphismStyler.get_font("body_medium"))
        backup_label.setStyleSheet(
            f"color: {GlassmorphismStyler.get_color('text_primary')};"
        )
        backup_layout.addWidget(backup_label)

        backup_combo_layout = QHBoxLayout()
        self._controls["backup_frequency"] = ModernComboBox()
        self._controls["backup_frequency"].addItems(
            ["Never", "Daily", "Weekly", "Monthly"]
        )
        backup_combo_layout.addWidget(self._controls["backup_frequency"])
        backup_combo_layout.addWidget(
            HelpTooltip(
                "Automatically creates backups of your settings at the specified interval. "
                "Helps prevent data loss."
            )
        )
        backup_combo_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        backup_layout.addLayout(backup_combo_layout)
        card.add_layout(backup_layout)

        parent_layout.addWidget(card)

    def _apply_styling(self):
        """Apply glassmorphism styling to the tab."""
        style = GlassmorphismStyler.create_dialog_style()
        self.setStyleSheet(style)

    def _load_current_settings(self):
        """Load current settings into the controls."""
        try:
            # User profile settings
            current_user = self.settings_manager.users.get_current_user()
            self._controls["user_name"].setText(current_user or "")

            # Application behavior (use defaults for now)
            self._controls["autosave"].setChecked(True)
            self._controls["backup_frequency"].setCurrentIndex(2)  # Weekly

            logging.debug("Loaded current settings into Enhanced General Tab")

        except Exception as e:
            logging.error(f"Error loading settings in Enhanced General Tab: {e}")

    def _setup_connections(self):
        """Setup signal connections for all controls."""
        # User profile settings
        self._controls["user_name"].textChanged.connect(
            lambda text: self._on_user_name_changed(text)
        )

        # Application behavior settings
        self._controls["autosave"].toggled.connect(
            lambda checked: self._on_setting_changed("app/autosave", checked)
        )
        self._controls["backup_frequency"].currentTextChanged.connect(
            lambda text: self._on_setting_changed("app/backup_frequency", text.lower())
        )

    def _on_user_name_changed(self, text: str):
        """Handle user name change."""
        try:
            # Clean the text (remove extra whitespace)
            clean_text = text.strip()

            # Get old value
            old_value = self.settings_manager.users.get_current_user()

            # Update the user name directly in the settings
            self.settings_manager.users.set_current_user(clean_text)

            # Emit change signal
            self.setting_changed.emit(
                "user_profile/current_user", old_value, clean_text
            )
            logging.debug(f"User name changed: {clean_text}")

        except Exception as e:
            logging.error(f"Error handling user name change: {e}")

    def _on_setting_changed(self, setting_key: str, new_value):
        """Handle setting change."""
        try:
            # Get old value from state manager
            old_value = self.state_manager.get_setting(setting_key)

            # Update state manager
            if self.state_manager.set_setting(setting_key, new_value):
                # Emit change signal
                self.setting_changed.emit(setting_key, old_value, new_value)
                logging.debug(f"Setting changed: {setting_key} = {new_value}")
            else:
                logging.warning(f"Failed to set setting: {setting_key} = {new_value}")

        except Exception as e:
            logging.error(f"Error handling setting change for {setting_key}: {e}")

    def refresh_settings(self):
        """Refresh all settings from the current state."""
        self._load_current_settings()
