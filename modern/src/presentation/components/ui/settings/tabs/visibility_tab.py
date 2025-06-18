from typing import Dict, Union
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QFrame,
    QGridLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.core.interfaces.tab_settings_interfaces import IVisibilityService


class VisibilityToggle(QCheckBox):
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
                padding: 8px;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.1);
            }
            
            QCheckBox::indicator:hover {
                border-color: rgba(255, 255, 255, 0.6);
                background: rgba(255, 255, 255, 0.15);
            }
            
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(34, 197, 94, 0.9),
                    stop:1 rgba(34, 197, 94, 0.7));
                border-color: rgba(34, 197, 94, 1.0);
            }
            
            QCheckBox::indicator:checked:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(34, 197, 94, 1.0),
                    stop:1 rgba(34, 197, 94, 0.8));
            }
        """
        )


class VisibilityTab(QWidget):
    visibility_changed = pyqtSignal(str, bool)

    def __init__(self, visibility_service: IVisibilityService, parent=None):
        super().__init__(parent)
        self.visibility_service = visibility_service
        self.glyph_toggles: Dict[str, VisibilityToggle] = {}
        self.motion_toggles: Dict[str, VisibilityToggle] = {}
        self._setup_ui()
        self._load_settings()
        self._setup_connections()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title = QLabel("Visibility Settings")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)

        description = QLabel("Control which elements are visible in pictographs")
        description.setObjectName("description")
        main_layout.addWidget(description)

        # Create sections
        layout = QHBoxLayout()

        # Left column - Glyph elements
        glyph_section = self._create_glyph_section()
        layout.addWidget(glyph_section)

        # Right column - Motion elements
        motion_section = self._create_motion_section()
        layout.addWidget(motion_section)

        main_layout.addLayout(layout)
        main_layout.addStretch()
        self._apply_styling()

    def _create_glyph_section(self):
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("Glyph Elements")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Glyph visibility toggles
        glyph_elements = [
            ("TKA", "Show TKA (The Kinetic Alphabet) symbols"),
            ("Reversals", "Show reversal indicators"),
            ("VTG", "Show VTG (Vertical/Twist/Gyre) symbols"),
            ("Elemental", "Show elemental symbols"),
            ("Positions", "Show position indicators"),
            ("Non-radial_points", "Show non-radial point indicators"),
        ]

        for name, tooltip in glyph_elements:
            toggle = VisibilityToggle(name.replace("_", " ").replace("-", " "), tooltip)
            self.glyph_toggles[name] = toggle
            layout.addWidget(toggle)

        return section

    def _create_motion_section(self):
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("Motion Elements")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Motion visibility toggles
        motion_elements = [
            ("red", "Show red motion props and arrows"),
            ("blue", "Show blue motion props and arrows"),
        ]

        for color, tooltip in motion_elements:
            toggle = VisibilityToggle(f"{color.title()} Motion", tooltip)
            self.motion_toggles[color] = toggle
            layout.addWidget(toggle)

        # Note about motion visibility
        note = QLabel("Note: At least one motion type must remain visible")
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
            
            QLabel#note {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                font-style: italic;
                margin-top: 15px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 6px;
                border-left: 3px solid rgba(255, 193, 7, 0.8);
            }
            
            QFrame#settings_section {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin: 5px;
                min-width: 300px;
            }
        """
        )

    def _load_settings(self):
        # Load glyph visibility settings
        for name, toggle in self.glyph_toggles.items():
            visible = self.visibility_service.get_glyph_visibility(name)
            # Ensure we have a boolean value
            if isinstance(visible, str):
                visible = visible.lower() == "true"
            toggle.setChecked(bool(visible))

        # Load motion visibility settings
        for color, toggle in self.motion_toggles.items():
            visible = self.visibility_service.get_motion_visibility(color)
            # Ensure we have a boolean value
            if isinstance(visible, str):
                visible = visible.lower() == "true"
            toggle.setChecked(bool(visible))

    def _setup_connections(self):
        # Connect glyph toggles
        for name, toggle in self.glyph_toggles.items():
            toggle.toggled.connect(
                lambda checked, n=name: self._on_glyph_visibility_changed(n, checked)
            )

        # Connect motion toggles with validation
        for color, toggle in self.motion_toggles.items():
            toggle.toggled.connect(
                lambda checked, c=color: self._on_motion_visibility_changed(c, checked)
            )

    def _on_glyph_visibility_changed(self, name: str, visible: bool):
        self.visibility_service.set_glyph_visibility(name, visible)
        self.visibility_changed.emit(f"glyph_{name}", visible)

    def _on_motion_visibility_changed(self, color: str, visible: bool):
        # Ensure at least one motion type remains visible
        if not visible:
            other_color = "blue" if color == "red" else "red"
            other_visible = self.visibility_service.get_motion_visibility(other_color)

            if not other_visible:
                # Don't allow turning off the last motion type
                self.motion_toggles[color].setChecked(True)
                return

        self.visibility_service.set_motion_visibility(color, visible)
        self.visibility_changed.emit(f"motion_{color}", visible)
