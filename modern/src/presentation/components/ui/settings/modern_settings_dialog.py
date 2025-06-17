from typing import Optional
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QWidget,
    QLabel,
    QPushButton,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.core.interfaces.core_services import IUIStateManagementService
from src.core.interfaces.tab_settings_interfaces import (
    IUserProfileService,
    IPropTypeService,
    IVisibilityService,
    IBeatLayoutService,
    IImageExportService,
)
from src.core.interfaces.background_interfaces import IBackgroundService

from .tabs.general_tab import GeneralTab
from .tabs.prop_type_tab import PropTypeTab
from .tabs.visibility_tab import VisibilityTab
from .tabs.beat_layout_tab import BeatLayoutTab
from .tabs.image_export_tab import ImageExportTab
from .tabs.background_tab import BackgroundTab


class ModernSettingsDialog(QDialog):
    settings_changed = pyqtSignal(str, object)

    def __init__(self, ui_state_service: IUIStateManagementService, parent=None):
        super().__init__(parent)
        self.ui_state_service = ui_state_service
        self._initialize_services()
        self._setup_dialog()
        self._create_ui()
        self._apply_styling()

    def _initialize_services(self):
        """Initialize all the tab-specific services"""
        from src.application.services.settings.user_profile_service import (
            UserProfileService,
        )
        from src.application.services.settings.prop_type_service import PropTypeService
        from src.application.services.settings.visibility_service import (
            VisibilityService,
        )
        from src.application.services.settings.beat_layout_service import (
            BeatLayoutService,
        )
        from src.application.services.settings.image_export_service import (
            ImageExportService,
        )
        from src.application.services.settings.background_service import (
            BackgroundService,
        )

        # All services use the UI state service directly
        self.user_service = UserProfileService(self.ui_state_service)
        self.prop_service = PropTypeService(self.ui_state_service)
        self.visibility_service = VisibilityService(self.ui_state_service)
        self.layout_service = BeatLayoutService(self.ui_state_service)
        self.export_service = ImageExportService(self.ui_state_service)
        self.background_service = BackgroundService(self.ui_state_service)

    def _setup_dialog(self):
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setFixedSize(1200, 800)

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _create_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QFrame()
        container.setObjectName("main_container")
        main_layout.addWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 30)

        # Header with title and close button
        header_layout = QHBoxLayout()
        title = QLabel("Settings")
        title.setObjectName("title")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        close_button = QPushButton("✕")
        close_button.setObjectName("close_button")
        close_button.setFixedSize(40, 40)
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.clicked.connect(self.close)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        container_layout.addLayout(header_layout)

        # Tab widget with all settings tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tab_widget")

        # Create all tabs
        self._create_tabs()

        container_layout.addWidget(self.tab_widget)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        reset_button = QPushButton("Reset to Defaults")
        reset_button.setObjectName("action_button")
        reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_button.clicked.connect(self._reset_settings)

        apply_button = QPushButton("Apply")
        apply_button.setObjectName("action_button")
        apply_button.setCursor(Qt.CursorShape.PointingHandCursor)
        apply_button.clicked.connect(self._apply_settings)

        ok_button = QPushButton("OK")
        ok_button.setObjectName("primary_button")
        ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_button.clicked.connect(self.accept)

        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)
        button_layout.addWidget(ok_button)
        container_layout.addLayout(button_layout)

    def _create_tabs(self):
        # General Tab
        general_tab = GeneralTab(self.user_service)
        general_tab.setting_changed.connect(self.settings_changed.emit)
        self.tab_widget.addTab(general_tab, "General")

        # Prop Type Tab
        prop_tab = PropTypeTab(self.prop_service)
        prop_tab.prop_type_changed.connect(
            lambda prop_type: self.settings_changed.emit("prop_type", prop_type)
        )
        self.tab_widget.addTab(prop_tab, "Prop Type")

        # Visibility Tab
        visibility_tab = VisibilityTab(self.visibility_service)
        visibility_tab.visibility_changed.connect(self.settings_changed.emit)
        self.tab_widget.addTab(visibility_tab, "Visibility")

        # Beat Layout Tab
        layout_tab = BeatLayoutTab(self.layout_service)
        layout_tab.layout_changed.connect(
            lambda length, rows, cols: self.settings_changed.emit(
                "beat_layout", {"length": length, "rows": rows, "cols": cols}
            )
        )
        self.tab_widget.addTab(layout_tab, "Beat Layout")

        # Image Export Tab
        export_tab = ImageExportTab(self.export_service)
        export_tab.export_option_changed.connect(self.settings_changed.emit)
        self.tab_widget.addTab(export_tab, "Image Export")

        # Background Tab
        background_tab = BackgroundTab(self.background_service)
        background_tab.background_changed.connect(self.settings_changed.emit)
        self.tab_widget.addTab(background_tab, "Background")

        # Advanced Tab (placeholder for future expansion)
        advanced_tab = self._create_advanced_tab()
        self.tab_widget.addTab(advanced_tab, "Advanced")

    def _create_advanced_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Advanced Settings")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        description = QLabel("Advanced configuration options and experimental features")
        description.setObjectName("description")
        layout.addWidget(description)

        # Placeholder content
        placeholder = QFrame()
        placeholder.setObjectName("settings_section")
        placeholder_layout = QVBoxLayout(placeholder)

        placeholder_title = QLabel("Coming Soon")
        placeholder_title.setObjectName("subsection_title")
        placeholder_layout.addWidget(placeholder_title)

        placeholder_text = QLabel(
            "Advanced features will be available in future updates"
        )
        placeholder_text.setObjectName("note")
        placeholder_layout.addWidget(placeholder_text)

        layout.addWidget(placeholder)
        layout.addStretch()

        return tab

    def _apply_styling(self):
        self.setStyleSheet(
            """
            QDialog {
                background: transparent;
            }
            
            QFrame#main_container {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 41, 59, 0.95),
                    stop:1 rgba(15, 23, 42, 0.95));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
            }
            
            QLabel#title {
                color: white;
                margin-bottom: 10px;
            }
            
            QLabel#section_title {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            QLabel#description {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin-bottom: 20px;
            }
            
            QLabel#subsection_title {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            
            QLabel#note {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                font-style: italic;
                margin-top: 15px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 6px;
                border-left: 3px solid rgba(59, 130, 246, 0.8);
            }
            
            QPushButton#close_button {
                background: rgba(220, 38, 38, 0.8);
                border: 2px solid rgba(220, 38, 38, 0.3);
                border-radius: 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            
            QPushButton#close_button:hover {
                background: rgba(220, 38, 38, 1.0);
            }
            
            QTabWidget {
                background: transparent;
                border: none;
            }
            
            QTabWidget::pane {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                margin-top: 5px;
            }
            
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                padding: 12px 20px;
                margin-right: 2px;
                color: white;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
            }
            
            QTabBar::tab:selected {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.4);
            }
            
            QTabBar::tab:hover {
                background: rgba(255, 255, 255, 0.15);
            }
            
            QFrame#settings_section {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
            }
            
            QPushButton#action_button {
                background: rgba(59, 130, 246, 0.8);
                border: 2px solid rgba(59, 130, 246, 0.3);
                border-radius: 8px;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                margin: 0 5px;
                font-size: 14px;
            }
            
            QPushButton#action_button:hover {
                background: rgba(59, 130, 246, 1.0);
            }
            
            QPushButton#primary_button {
                background: rgba(34, 197, 94, 0.8);
                border: 2px solid rgba(34, 197, 94, 0.3);
                border-radius: 8px;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                margin: 0 5px;
                font-size: 14px;
            }
            
            QPushButton#primary_button:hover {
                background: rgba(34, 197, 94, 1.0);
            }
        """
        )

    def _reset_settings(self):
        # Reset all settings to defaults
        pass

    def _apply_settings(self):
        # Save settings through the UI state service
        self.ui_state_service.save_state()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if (
            hasattr(self, "drag_position")
            and event.buttons() == Qt.MouseButton.LeftButton
        ):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
