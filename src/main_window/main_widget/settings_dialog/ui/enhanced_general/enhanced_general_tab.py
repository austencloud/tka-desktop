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
        self._create_thumbnail_quality_section(content_layout)
        self._create_cache_settings_section(content_layout)
        self._create_performance_section(content_layout)
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

    def _create_thumbnail_quality_section(self, parent_layout):
        """Create thumbnail quality settings section."""
        card = SettingCard(
            "Thumbnail Quality",
            "Configure high-quality thumbnail rendering and image enhancement settings.",
        )

        # Ultra Quality Mode
        ultra_quality_layout = QHBoxLayout()
        self._controls["ultra_quality"] = ModernToggle("Enable Ultra Quality Mode")
        ultra_quality_layout.addWidget(self._controls["ultra_quality"])
        ultra_quality_layout.addWidget(
            HelpTooltip(
                "Enables the highest quality thumbnail rendering with advanced scaling algorithms. "
                "May impact performance on slower systems."
            )
        )
        ultra_quality_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        card.add_layout(ultra_quality_layout)

        # Image Enhancement
        enhancement_layout = QHBoxLayout()
        self._controls["enhancement"] = ModernToggle("Enable Image Enhancement")
        enhancement_layout.addWidget(self._controls["enhancement"])
        enhancement_layout.addWidget(
            HelpTooltip(
                "Applies advanced image enhancement algorithms to improve thumbnail clarity and detail. "
                "Recommended for high-resolution displays."
            )
        )
        enhancement_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        card.add_layout(enhancement_layout)

        # Sharpening
        sharpening_layout = QHBoxLayout()
        self._controls["sharpening"] = ModernToggle("Enable Image Sharpening")
        sharpening_layout.addWidget(self._controls["sharpening"])
        sharpening_layout.addWidget(
            HelpTooltip(
                "Applies subtle sharpening to thumbnails for improved edge definition. "
                "Works best with ultra quality mode enabled."
            )
        )
        sharpening_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        card.add_layout(sharpening_layout)

        # Quality Priority
        quality_layout = QVBoxLayout()
        quality_label = QLabel("Quality Priority:")
        quality_label.setFont(GlassmorphismStyler.get_font("body_medium"))
        quality_label.setStyleSheet(
            f"color: {GlassmorphismStyler.get_color('text_primary')};"
        )
        quality_layout.addWidget(quality_label)

        quality_combo_layout = QHBoxLayout()
        self._controls["quality_priority"] = ModernComboBox()
        self._controls["quality_priority"].addItems(
            ["High Quality", "Balanced", "Fast"]
        )
        quality_combo_layout.addWidget(self._controls["quality_priority"])
        quality_combo_layout.addWidget(
            HelpTooltip(
                "High Quality: Maximum quality, slower rendering\n"
                "Balanced: Good quality with reasonable performance\n"
                "Fast: Prioritizes speed over quality"
            )
        )
        quality_combo_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        quality_layout.addLayout(quality_combo_layout)
        card.add_layout(quality_layout)

        parent_layout.addWidget(card)

    def _create_cache_settings_section(self, parent_layout):
        """Create cache settings section."""
        card = SettingCard(
            "Cache Settings",
            "Configure thumbnail caching for improved performance and storage management.",
        )

        # Enable Disk Cache
        cache_layout = QHBoxLayout()
        self._controls["enable_cache"] = ModernToggle("Enable Disk Cache")
        cache_layout.addWidget(self._controls["enable_cache"])
        cache_layout.addWidget(
            HelpTooltip(
                "Stores processed thumbnails on disk for faster loading. "
                "Recommended for better performance."
            )
        )
        cache_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        card.add_layout(cache_layout)

        # Cache Mode
        mode_layout = QVBoxLayout()
        mode_label = QLabel("Cache Mode:")
        mode_label.setFont(GlassmorphismStyler.get_font("body_medium"))
        mode_label.setStyleSheet(
            f"color: {GlassmorphismStyler.get_color('text_primary')};"
        )
        mode_layout.addWidget(mode_label)

        mode_combo_layout = QHBoxLayout()
        self._controls["cache_mode"] = ModernComboBox()
        self._controls["cache_mode"].addItems(["memory", "disk", "hybrid"])
        mode_combo_layout.addWidget(self._controls["cache_mode"])
        mode_combo_layout.addWidget(
            HelpTooltip(
                "Memory: Fast but limited by RAM\n"
                "Disk: Persistent but slower access\n"
                "Hybrid: Best of both worlds (recommended)"
            )
        )
        mode_combo_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        mode_layout.addLayout(mode_combo_layout)
        card.add_layout(mode_layout)

        # Cache Size
        size_layout = QVBoxLayout()
        size_label = QLabel("Maximum Cache Size:")
        size_label.setFont(GlassmorphismStyler.get_font("body_medium"))
        size_label.setStyleSheet(
            f"color: {GlassmorphismStyler.get_color('text_primary')};"
        )
        size_layout.addWidget(size_label)

        self._controls["cache_size"] = ModernSlider(50, 2000, 500, " MB")
        size_layout.addWidget(self._controls["cache_size"])
        card.add_layout(size_layout)

        # Preload Thumbnails
        preload_layout = QHBoxLayout()
        self._controls["preload_thumbnails"] = ModernToggle("Preload Thumbnails")
        preload_layout.addWidget(self._controls["preload_thumbnails"])
        preload_layout.addWidget(
            HelpTooltip(
                "Preloads thumbnails in the background for smoother browsing. "
                "Uses more memory but improves user experience."
            )
        )
        preload_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        card.add_layout(preload_layout)

        parent_layout.addWidget(card)

    def _create_performance_section(self, parent_layout):
        """Create performance settings section."""
        card = SettingCard(
            "Performance Settings",
            "Optimize application performance and resource usage.",
        )

        # UI Responsiveness
        responsiveness_layout = QVBoxLayout()
        responsiveness_label = QLabel("UI Responsiveness:")
        responsiveness_label.setFont(GlassmorphismStyler.get_font("body_medium"))
        responsiveness_label.setStyleSheet(
            f"color: {GlassmorphismStyler.get_color('text_primary')};"
        )
        responsiveness_layout.addWidget(responsiveness_label)

        self._controls["ui_responsiveness"] = ModernSlider(1, 10, 7, "")
        responsiveness_layout.addWidget(self._controls["ui_responsiveness"])
        card.add_layout(responsiveness_layout)

        # Animation Quality
        animation_layout = QVBoxLayout()
        animation_label = QLabel("Animation Quality:")
        animation_label.setFont(GlassmorphismStyler.get_font("body_medium"))
        animation_label.setStyleSheet(
            f"color: {GlassmorphismStyler.get_color('text_primary')};"
        )
        animation_layout.addWidget(animation_label)

        animation_combo_layout = QHBoxLayout()
        self._controls["animation_quality"] = ModernComboBox()
        self._controls["animation_quality"].addItems(
            ["High", "Medium", "Low", "Disabled"]
        )
        animation_combo_layout.addWidget(self._controls["animation_quality"])
        animation_combo_layout.addWidget(
            HelpTooltip(
                "Controls the quality and smoothness of UI animations. "
                "Lower settings improve performance on slower systems."
            )
        )
        animation_combo_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        animation_layout.addLayout(animation_combo_layout)
        card.add_layout(animation_layout)

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
            browse_settings = self.settings_manager.browse_tab_settings

            # User profile settings
            current_user = self.settings_manager.users.get_current_user()
            self._controls["user_name"].setText(current_user or "")

            # Thumbnail quality settings
            self._controls["ultra_quality"].setChecked(
                browse_settings.get_ultra_quality_enabled()
            )
            self._controls["enhancement"].setChecked(
                browse_settings.get_enhancement_enabled()
            )
            self._controls["sharpening"].setChecked(
                browse_settings.get_sharpening_enabled()
            )

            # Map quality priority
            quality_map = {"high": 0, "balanced": 1, "fast": 2}
            quality_priority = browse_settings.get_thumbnail_processing_settings().get(
                "quality_priority", "high"
            )
            self._controls["quality_priority"].setCurrentIndex(
                quality_map.get(quality_priority, 0)
            )

            # Cache settings
            self._controls["enable_cache"].setChecked(
                browse_settings.get_enable_disk_cache()
            )

            # Map cache mode
            mode_map = {"memory": 0, "disk": 1, "hybrid": 2}
            cache_mode = browse_settings.get_cache_mode()
            self._controls["cache_mode"].setCurrentIndex(mode_map.get(cache_mode, 2))

            self._controls["cache_size"].setValue(
                browse_settings.get_cache_max_size_mb()
            )
            self._controls["preload_thumbnails"].setChecked(
                browse_settings.get_preload_thumbnails()
            )

            # Performance settings (use defaults for now)
            self._controls["ui_responsiveness"].setValue(7)
            self._controls["animation_quality"].setCurrentIndex(0)  # High

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

        # Thumbnail quality settings
        self._controls["ultra_quality"].toggled.connect(
            lambda checked: self._on_setting_changed(
                "browse/ultra_quality_enabled", checked
            )
        )
        self._controls["enhancement"].toggled.connect(
            lambda checked: self._on_setting_changed(
                "browse/enhancement_enabled", checked
            )
        )
        self._controls["sharpening"].toggled.connect(
            lambda checked: self._on_setting_changed(
                "browse/sharpening_enabled", checked
            )
        )
        self._controls["quality_priority"].currentTextChanged.connect(
            lambda text: self._on_setting_changed(
                "browse/quality_priority", text.lower().replace(" ", "_")
            )
        )

        # Cache settings
        self._controls["enable_cache"].toggled.connect(
            lambda checked: self._on_setting_changed(
                "browse/enable_disk_cache", checked
            )
        )
        self._controls["cache_mode"].currentTextChanged.connect(
            lambda text: self._on_setting_changed("browse/cache_mode", text.lower())
        )
        self._controls["cache_size"].valueChanged.connect(
            lambda value: self._on_setting_changed("browse/cache_max_size_mb", value)
        )
        self._controls["preload_thumbnails"].toggled.connect(
            lambda checked: self._on_setting_changed(
                "browse/preload_thumbnails", checked
            )
        )

        # Performance settings (these would need to be added to settings manager)
        self._controls["ui_responsiveness"].valueChanged.connect(
            lambda value: self._on_setting_changed(
                "performance/ui_responsiveness", value
            )
        )
        self._controls["animation_quality"].currentTextChanged.connect(
            lambda text: self._on_setting_changed(
                "performance/animation_quality", text.lower()
            )
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
