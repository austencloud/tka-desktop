from typing import Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.core.interfaces.tab_settings_interfaces import IUserProfileService


class GeneralTab(QWidget):
    setting_changed = pyqtSignal(str, object)

    def __init__(self, user_service: IUserProfileService, parent=None):
        super().__init__(parent)
        self.user_service = user_service
        self._setup_ui()
        self._load_settings()
        self._setup_connections()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title = QLabel("General Settings")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # User Profile Section
        user_section = self._create_user_section()
        main_layout.addWidget(user_section)

        # Application Behavior Section
        behavior_section = self._create_behavior_section()
        main_layout.addWidget(behavior_section)

        main_layout.addStretch()
        self._apply_styling()

    def _create_user_section(self):
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("User Profile")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Current User
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Current User:"))
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your name")
        user_layout.addWidget(self.user_input)
        layout.addLayout(user_layout)

        return section

    def _create_behavior_section(self):
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("Application Behavior")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Enable fades
        self.enable_fades = QCheckBox("Enable smooth transitions")
        self.enable_fades.setToolTip("Enable smooth fade transitions between views")
        layout.addWidget(self.enable_fades)

        # Auto-save
        self.auto_save = QCheckBox("Auto-save changes")
        self.auto_save.setToolTip("Automatically save changes without prompting")
        layout.addWidget(self.auto_save)

        # Theme selection
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Auto"])
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        return section

    def _apply_styling(self):
        self.setStyleSheet(
            """
            QWidget {
                background: transparent;
                color: white;
            }
            
            QLabel#section_title {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            
            QLabel#subsection_title {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            QFrame#settings_section {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 15px;
                margin: 5px 0;
            }
            
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 8px;
                color: white;
                font-size: 12px;
            }
            
            QLineEdit:focus {
                border-color: rgba(59, 130, 246, 0.8);
            }
            
            QCheckBox {
                color: white;
                font-size: 12px;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.1);
            }
            
            QCheckBox::indicator:checked {
                background: rgba(34, 197, 94, 0.8);
                border-color: rgba(34, 197, 94, 1.0);
            }
            
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 8px;
                color: white;
                min-width: 120px;
            }
            
            QComboBox:focus {
                border-color: rgba(59, 130, 246, 0.8);
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid rgba(255, 255, 255, 0.7);
                margin-right: 5px;
            }
        """
        )

    def _load_settings(self):
        current_user = self.user_service.get_current_user()
        self.user_input.setText(current_user)

        # Load other settings with defaults
        self.enable_fades.setChecked(True)
        self.auto_save.setChecked(True)
        self.theme_combo.setCurrentText("Dark")

    def _setup_connections(self):
        self.user_input.textChanged.connect(self._on_user_changed)
        self.enable_fades.toggled.connect(
            lambda x: self.setting_changed.emit("enable_fades", x)
        )
        self.auto_save.toggled.connect(
            lambda x: self.setting_changed.emit("auto_save", x)
        )
        self.theme_combo.currentTextChanged.connect(
            lambda x: self.setting_changed.emit("theme", x)
        )

    def _on_user_changed(self, text: str):
        self.user_service.set_current_user(text.strip())
        self.setting_changed.emit("current_user", text.strip())
