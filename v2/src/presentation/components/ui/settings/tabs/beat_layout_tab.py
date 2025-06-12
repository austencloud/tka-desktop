from typing import Dict
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QComboBox,
    QFrame,
    QGridLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.core.interfaces.tab_settings_interfaces import IBeatLayoutService


class BeatLayoutTab(QWidget):
    layout_changed = pyqtSignal(int, int, int)  # length, rows, cols

    def __init__(self, layout_service: IBeatLayoutService, parent=None):
        super().__init__(parent)
        self.layout_service = layout_service
        self.layout_controls: Dict[int, tuple[QSpinBox, QSpinBox]] = {}
        self._setup_ui()
        self._load_settings()
        self._setup_connections()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title = QLabel("Beat Layout Configuration")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)

        description = QLabel("Configure grid layouts for different sequence lengths")
        description.setObjectName("description")
        main_layout.addWidget(description)

        # Layout configuration section
        config_section = self._create_layout_section()
        main_layout.addWidget(config_section)

        main_layout.addStretch()
        self._apply_styling()

    def _create_layout_section(self):
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("Layout Configurations")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Grid for layout controls
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(15)

        # Headers
        grid_layout.addWidget(QLabel("Sequence Length"), 0, 0)
        grid_layout.addWidget(QLabel("Rows"), 0, 1)
        grid_layout.addWidget(QLabel("Columns"), 0, 2)

        # Common sequence lengths
        lengths = [4, 8, 16, 32]

        for i, length in enumerate(lengths):
            row = i + 1

            # Length label
            length_label = QLabel(f"{length} beats")
            length_label.setObjectName("length_label")
            grid_layout.addWidget(length_label, row, 0)

            # Rows spinbox
            rows_spin = QSpinBox()
            rows_spin.setRange(1, 10)
            rows_spin.setObjectName("layout_spinbox")
            grid_layout.addWidget(rows_spin, row, 1)

            # Columns spinbox
            cols_spin = QSpinBox()
            cols_spin.setRange(1, 10)
            cols_spin.setObjectName("layout_spinbox")
            grid_layout.addWidget(cols_spin, row, 2)

            self.layout_controls[length] = (rows_spin, cols_spin)

        layout.addWidget(grid_widget)

        # Info note
        note = QLabel("Layouts determine how beats are arranged in the grid view")
        note.setObjectName("note")
        note.setWordWrap(True)
        layout.addWidget(note)

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
            
            QLabel#length_label {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
                padding: 8px;
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
            
            QFrame#settings_section {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin: 5px 0;
            }
            
            QSpinBox#layout_spinbox {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                padding: 6px;
                color: white;
                font-size: 14px;
                min-width: 60px;
            }
            
            QSpinBox#layout_spinbox:focus {
                border-color: rgba(59, 130, 246, 0.8);
            }
            
            QSpinBox#layout_spinbox::up-button, QSpinBox#layout_spinbox::down-button {
                background: rgba(255, 255, 255, 0.2);
                border: none;
                width: 20px;
            }
            
            QSpinBox#layout_spinbox::up-button:hover, QSpinBox#layout_spinbox::down-button:hover {
                background: rgba(255, 255, 255, 0.3);
            }
        """
        )

    def _load_settings(self):
        for length, (rows_spin, cols_spin) in self.layout_controls.items():
            rows, cols = self.layout_service.get_layout_for_length(length)
            rows_spin.setValue(rows)
            cols_spin.setValue(cols)

    def _setup_connections(self):
        for length, (rows_spin, cols_spin) in self.layout_controls.items():
            rows_spin.valueChanged.connect(
                lambda value, l=length: self._on_layout_changed(l)
            )
            cols_spin.valueChanged.connect(
                lambda value, l=length: self._on_layout_changed(l)
            )

    def _on_layout_changed(self, length: int):
        rows_spin, cols_spin = self.layout_controls[length]
        rows = rows_spin.value()
        cols = cols_spin.value()

        self.layout_service.set_layout_for_length(length, rows, cols)
        self.layout_changed.emit(length, rows, cols)
