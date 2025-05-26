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
        """Create the cache settings group box."""
        group = QGroupBox("Browse Tab Cache Settings")
        layout = QVBoxLayout(group)
        layout.setSpacing(15)

        # Enable cache checkbox
        self.enable_cache_checkbox = QCheckBox("Enable disk caching for thumbnails")
        self.enable_cache_checkbox.setToolTip(
            "Enable persistent disk caching to improve thumbnail loading performance"
        )
        layout.addWidget(self.enable_cache_checkbox)

        # Cache mode selection
        cache_mode_layout = QHBoxLayout()
        cache_mode_layout.addWidget(QLabel("Cache Mode:"))

        self.cache_mode_combo = QComboBox()
        self.cache_mode_combo.addItems(
            ["High Performance (1GB)", "Balanced (500MB)", "Storage Efficient (100MB)"]
        )
        self.cache_mode_combo.setToolTip(
            "High Performance: Faster loading, more disk space\n"
            "Balanced: Good balance of speed and storage\n"
            "Storage Efficient: Minimal disk usage"
        )
        cache_mode_layout.addWidget(self.cache_mode_combo)
        cache_mode_layout.addStretch()
        layout.addLayout(cache_mode_layout)

        # Cache size display and manual override
        cache_size_layout = QHBoxLayout()
        cache_size_layout.addWidget(QLabel("Max Cache Size (MB):"))

        self.cache_size_spinbox = QSpinBox()
        self.cache_size_spinbox.setRange(50, 5000)
        self.cache_size_spinbox.setSuffix(" MB")
        self.cache_size_spinbox.setToolTip("Maximum cache size in megabytes")
        cache_size_layout.addWidget(self.cache_size_spinbox)
        cache_size_layout.addStretch()
        layout.addLayout(cache_size_layout)

        # Cache location
        cache_location_layout = QHBoxLayout()
        cache_location_layout.addWidget(QLabel("Cache Location:"))

        self.cache_location_label = QLabel("Default (AppData)")
        self.cache_location_label.setStyleSheet("QLabel { color: #666; }")
        cache_location_layout.addWidget(self.cache_location_label)

        self.browse_cache_button = QPushButton("Browse...")
        self.browse_cache_button.setMaximumWidth(100)
        cache_location_layout.addWidget(self.browse_cache_button)
        cache_location_layout.addStretch()
        layout.addLayout(cache_location_layout)

        # Quality mode selection
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Image Quality:"))

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(
            ["Two-Stage (Fast + High Quality)", "Fast Only", "High Quality Only"]
        )
        self.quality_combo.setToolTip(
            "Two-Stage: Fast display then quality enhancement\n"
            "Fast Only: Quick loading, lower quality\n"
            "High Quality Only: Best quality, may be slower"
        )
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        layout.addLayout(quality_layout)

        # Preload thumbnails checkbox
        self.preload_checkbox = QCheckBox("Preload thumbnails on startup")
        self.preload_checkbox.setToolTip(
            "Automatically load visible thumbnails when browse tab opens"
        )
        layout.addWidget(self.preload_checkbox)

        # Cache statistics and management
        stats_layout = QHBoxLayout()

        self.cache_stats_label = QLabel("Cache: 0 items, 0 MB")
        self.cache_stats_label.setStyleSheet("QLabel { color: #666; }")
        stats_layout.addWidget(self.cache_stats_label)

        self.clear_cache_button = QPushButton("Clear Cache")
        self.clear_cache_button.setMaximumWidth(100)
        stats_layout.addWidget(self.clear_cache_button)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        return group

    def _connect_signals(self):
        """Connect UI signals to handlers."""
        self.enable_cache_checkbox.stateChanged.connect(self._on_enable_cache_changed)
        self.cache_mode_combo.currentTextChanged.connect(self._on_cache_mode_changed)
        self.cache_size_spinbox.valueChanged.connect(self._on_cache_size_changed)
        self.browse_cache_button.clicked.connect(self._on_browse_cache_location)
        self.quality_combo.currentTextChanged.connect(self._on_quality_mode_changed)
        self.preload_checkbox.stateChanged.connect(self._on_preload_changed)
        self.clear_cache_button.clicked.connect(self._on_clear_cache)

    def _load_settings(self):
        """Load current settings into UI."""
        # Enable cache
        self.enable_cache_checkbox.setChecked(
            self.browse_settings.get_enable_disk_cache()
        )

        # Cache mode
        cache_mode = self.browse_settings.get_cache_mode()
        mode_map = {"High Performance": 0, "Balanced": 1, "Storage Efficient": 2}
        self.cache_mode_combo.setCurrentIndex(mode_map.get(cache_mode, 1))

        # Cache size
        self.cache_size_spinbox.setValue(self.browse_settings.get_cache_max_size_mb())

        # Cache location
        location = self.browse_settings.get_cache_location()
        if location:
            self.cache_location_label.setText(location)
        else:
            self.cache_location_label.setText("Default (AppData)")

        # Quality mode
        quality_mode = self.browse_settings.get_cache_quality_mode()
        quality_map = {"two_stage": 0, "fast_only": 1, "smooth_only": 2}
        self.quality_combo.setCurrentIndex(quality_map.get(quality_mode, 0))

        # Preload thumbnails
        self.preload_checkbox.setChecked(self.browse_settings.get_preload_thumbnails())

        # Update cache stats
        self._update_cache_stats()

    def _on_enable_cache_changed(self, state):
        """Handle enable cache checkbox change."""
        enabled = bool(state)
        self.browse_settings.set_enable_disk_cache(enabled)

        # Enable/disable other cache controls
        self.cache_mode_combo.setEnabled(enabled)
        self.cache_size_spinbox.setEnabled(enabled)
        self.browse_cache_button.setEnabled(enabled)
        self.quality_combo.setEnabled(enabled)
        self.clear_cache_button.setEnabled(enabled)

        self.cache_settings_changed.emit()

    def _on_cache_mode_changed(self, text):
        """Handle cache mode change."""
        mode_map = {
            "High Performance (1GB)": "High Performance",
            "Balanced (500MB)": "Balanced",
            "Storage Efficient (100MB)": "Storage Efficient",
        }
        mode = mode_map.get(text, "Balanced")
        self.browse_settings.set_cache_mode(mode)

        # Update cache size spinbox to match mode
        self.cache_size_spinbox.setValue(self.browse_settings.get_cache_max_size_mb())

        self.cache_settings_changed.emit()

    def _on_cache_size_changed(self, value):
        """Handle cache size change."""
        self.browse_settings.set_cache_max_size_mb(value)
        self.cache_settings_changed.emit()

    def _on_browse_cache_location(self):
        """Handle browse cache location button click."""
        current_location = self.browse_settings.get_cache_location()
        if not current_location:
            # Use default location as starting point
            try:
                from utils.path_helpers import get_user_editable_resource_path

                current_location = get_user_editable_resource_path("")
            except:
                current_location = ""

        directory = QFileDialog.getExistingDirectory(
            self, "Select Cache Directory", current_location
        )

        if directory:
            self.browse_settings.set_cache_location(directory)
            self.cache_location_label.setText(directory)
            self.cache_settings_changed.emit()

    def _on_quality_mode_changed(self, text):
        """Handle quality mode change."""
        mode_map = {
            "Two-Stage (Fast + High Quality)": "two_stage",
            "Fast Only": "fast_only",
            "High Quality Only": "smooth_only",
        }
        mode = mode_map.get(text, "two_stage")
        self.browse_settings.set_cache_quality_mode(mode)
        self.cache_settings_changed.emit()

    def _on_preload_changed(self, state):
        """Handle preload thumbnails checkbox change."""
        self.browse_settings.set_preload_thumbnails(bool(state))
        self.cache_settings_changed.emit()

    def _on_clear_cache(self):
        """Handle clear cache button click."""
        try:
            # Try to get cache instance from browse tab if available
            browse_tab = getattr(self.settings_dialog.main_widget, "browse_tab", None)
            if browse_tab:
                # Clear cache through browse tab's cache system
                # This would need to be implemented in the browse tab
                pass

            # Update stats display
            self._update_cache_stats()

        except Exception as e:
            import logging

            logging.debug(f"Error clearing cache: {e}")

    def _update_cache_stats(self):
        """Update cache statistics display."""
        try:
            # Try to get cache stats from browse tab if available
            browse_tab = getattr(self.settings_dialog.main_widget, "browse_tab", None)
            if browse_tab:
                # Get cache stats - this would need to be implemented
                self.cache_stats_label.setText("Cache: 0 items, 0 MB")
            else:
                self.cache_stats_label.setText("Cache: Not available")
        except Exception:
            self.cache_stats_label.setText("Cache: Error reading stats")

    def update_general_tab_from_settings(self):
        """Update the tab when it becomes active."""
        self._load_settings()
