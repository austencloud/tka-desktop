from typing import Dict, Union
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QFrame,
    QGridLayout,
    QPushButton,
    QLineEdit,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.core.interfaces.tab_settings_interfaces import IImageExportService


class ExportToggle(QCheckBox):
    def __init__(self, label: str, tooltip: Union[str, None] = None, parent=None):
        super().__init__(label, parent)
        if tooltip:
            self.setToolTip(tooltip)
        self._apply_styling()

    def _apply_styling(self):
        self.setStyleSheet(
            """
            QCheckBox {
                color: white;
                font-size: 14px;
                font-weight: 500;
                spacing: 10px;
                padding: 10px;
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.05);
            }
            
            QCheckBox:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.1);
            }
            
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(59, 130, 246, 0.9),
                    stop:1 rgba(59, 130, 246, 0.7));
                border-color: rgba(59, 130, 246, 1.0);
            }
        """
        )


class ImageExportTab(QWidget):
    export_option_changed = pyqtSignal(str, object)

    def __init__(self, export_service: IImageExportService, parent=None):
        super().__init__(parent)
        self.export_service = export_service
        self.option_toggles: Dict[str, ExportToggle] = {}
        self._setup_ui()
        self._load_settings()
        self._setup_connections()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title = QLabel("Image Export Settings")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)

        description = QLabel("Configure options for exporting sequence images")
        description.setObjectName("description")
        main_layout.addWidget(description)

        # Main content layout
        content_layout = QHBoxLayout()

        # Left column - Export options
        options_section = self._create_options_section()
        content_layout.addWidget(options_section)

        # Right column - Settings and actions
        settings_section = self._create_settings_section()
        content_layout.addWidget(settings_section)

        main_layout.addLayout(content_layout)
        main_layout.addStretch()
        self._apply_styling()

    def _create_options_section(self):
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("Export Options")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Export options with descriptions
        export_options = [
            (
                "include_start_position",
                "Include Start Position",
                "Show the starting position in exports",
            ),
            ("add_beat_numbers", "Beat Numbers", "Add numbers to each beat"),
            ("add_reversal_symbols", "Reversal Symbols", "Show reversal indicators"),
            ("add_user_info", "User Information", "Include user name in export"),
            ("add_word", "Word Labels", "Add word descriptions"),
            ("add_difficulty_level", "Difficulty Level", "Show difficulty rating"),
            ("combined_grids", "Combined Grids", "Use combined grid layouts"),
        ]

        for option_key, label, tooltip in export_options:
            toggle = ExportToggle(label, tooltip)
            self.option_toggles[option_key] = toggle
            layout.addWidget(toggle)

        return section

    def _create_settings_section(self):
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("Export Settings")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Directory preference
        self.remember_dir_toggle = ExportToggle(
            "Remember Last Directory", "Remember the last directory used for saving"
        )
        layout.addWidget(self.remember_dir_toggle)

        # User name input
        user_layout = QVBoxLayout()
        user_label = QLabel("User Name:")
        user_label.setObjectName("input_label")
        user_layout.addWidget(user_label)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your name for exports")
        self.user_input.setObjectName("export_input")
        user_layout.addWidget(self.user_input)

        layout.addLayout(user_layout)

        # Custom note input
        note_layout = QVBoxLayout()
        note_label = QLabel("Custom Note:")
        note_label.setObjectName("input_label")
        note_layout.addWidget(note_label)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Add a custom note to exports")
        self.note_input.setObjectName("export_input")
        note_layout.addWidget(self.note_input)

        layout.addLayout(note_layout)

        # Export actions
        actions_layout = QVBoxLayout()
        actions_label = QLabel("Quick Actions:")
        actions_label.setObjectName("input_label")
        actions_layout.addWidget(actions_label)

        self.export_current_btn = QPushButton("Export Current")
        self.export_current_btn.setObjectName("action_button")
        actions_layout.addWidget(self.export_current_btn)

        self.export_all_btn = QPushButton("Export All")
        self.export_all_btn.setObjectName("action_button")
        actions_layout.addWidget(self.export_all_btn)

        layout.addLayout(actions_layout)

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
            
            QLabel#input_label {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 5px;
                margin-top: 10px;
            }
            
            QFrame#settings_section {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin: 5px;
                min-width: 300px;
            }
            
            QLineEdit#export_input {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 14px;
                margin-bottom: 10px;
            }
            
            QLineEdit#export_input:focus {
                border-color: rgba(59, 130, 246, 0.8);
            }
            
            QPushButton#action_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(59, 130, 246, 0.8),
                    stop:1 rgba(59, 130, 246, 0.6));
                border: 2px solid rgba(59, 130, 246, 0.3);
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                margin: 5px 0;
            }
            
            QPushButton#action_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(59, 130, 246, 1.0),
                    stop:1 rgba(59, 130, 246, 0.8));
                border-color: rgba(59, 130, 246, 0.8);
            }
            
            QPushButton#action_button:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(59, 130, 246, 0.6),
                    stop:1 rgba(59, 130, 246, 0.4));
            }
        """
        )

    def _load_settings(self):
        # Load export options
        for option_key, toggle in self.option_toggles.items():
            value = self.export_service.get_export_option(option_key)
            toggle.setChecked(bool(value))

        # Load directory preference
        remember_dir = self.export_service.get_export_option("use_last_save_directory")
        self.remember_dir_toggle.setChecked(bool(remember_dir))

        # Load user inputs with defaults
        self.user_input.setText("Default User")
        self.note_input.setText("")

    def _setup_connections(self):
        # Connect export option toggles
        for option_key, toggle in self.option_toggles.items():
            toggle.toggled.connect(
                lambda checked, key=option_key: self._on_option_changed(key, checked)
            )

        # Connect other controls
        self.remember_dir_toggle.toggled.connect(
            lambda checked: self._on_option_changed("use_last_save_directory", checked)
        )

        self.user_input.textChanged.connect(
            lambda text: self.export_option_changed.emit("user_name", text)
        )

        self.note_input.textChanged.connect(
            lambda text: self.export_option_changed.emit("custom_note", text)
        )

        # Connect action buttons (placeholder functionality)
        self.export_current_btn.clicked.connect(self._export_current)
        self.export_all_btn.clicked.connect(self._export_all)

    def _on_option_changed(self, option_key: str, value: bool):
        self.export_service.set_export_option(option_key, value)
        self.export_option_changed.emit(option_key, value)

    def _export_current(self):
        # Placeholder for export current functionality
        self.export_option_changed.emit("action", "export_current")

    def _export_all(self):
        # Placeholder for export all functionality
        self.export_option_changed.emit("action", "export_all")
