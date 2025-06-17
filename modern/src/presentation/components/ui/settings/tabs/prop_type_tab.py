from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QIcon, QCursor

from core.interfaces.tab_settings_interfaces import IPropTypeService, PropType


class PropButton(QPushButton):
    def __init__(self, prop_type: PropType, parent=None):
        super().__init__(prop_type.value, parent)
        self.prop_type = prop_type
        self.setFixedSize(QSize(120, 120))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._is_active = False
        self._apply_styling()

    def set_active(self, active: bool):
        self._is_active = active
        self._apply_styling()

    def _apply_styling(self):
        base_style = """
            QPushButton {
                border: 3px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.05));
                color: white;
                font-size: 12px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                border-color: rgba(255, 255, 255, 0.5);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.25),
                    stop:1 rgba(255, 255, 255, 0.15));
            }
        """

        if self._is_active:
            active_style = """
                QPushButton {
                    border: 3px solid rgba(34, 197, 94, 0.8);
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(34, 197, 94, 0.3),
                        stop:1 rgba(34, 197, 94, 0.1));
                    color: rgba(34, 197, 94, 1.0);
                }
                QPushButton:hover {
                    border-color: rgba(34, 197, 94, 1.0);
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(34, 197, 94, 0.4),
                        stop:1 rgba(34, 197, 94, 0.2));
                }
            """
            self.setStyleSheet(active_style)
        else:
            self.setStyleSheet(base_style)


class PropTypeTab(QWidget):
    prop_type_changed = pyqtSignal(PropType)

    def __init__(self, prop_service: IPropTypeService, parent=None):
        super().__init__(parent)
        self.prop_service = prop_service
        self.buttons = {}
        self._setup_ui()
        self._load_current_prop()
        self._setup_connections()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title = QLabel("Prop Type Selection")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        description = QLabel("Choose the prop type for your sequences")
        description.setObjectName("description")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(description)

        # Props grid
        props_widget = QWidget()
        props_layout = QGridLayout(props_widget)
        props_layout.setSpacing(15)
        props_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        available_props = self.prop_service.get_available_prop_types()

        for i, prop_type in enumerate(available_props):
            row = i // 3
            col = i % 3

            button = PropButton(prop_type)
            button.clicked.connect(
                lambda checked, pt=prop_type: self._on_prop_selected(pt)
            )
            self.buttons[prop_type] = button
            props_layout.addWidget(button, row, col)

        main_layout.addWidget(props_widget)
        main_layout.addStretch()
        self._apply_styling()

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
        """
        )

    def _load_current_prop(self):
        current_prop = self.prop_service.get_current_prop_type()
        if current_prop in self.buttons:
            self._set_active_button(current_prop)

    def _setup_connections(self):
        pass  # Connections set up in _setup_ui

    def _on_prop_selected(self, prop_type: PropType):
        self.prop_service.set_prop_type(prop_type)
        self._set_active_button(prop_type)
        self.prop_type_changed.emit(prop_type)

    def _set_active_button(self, active_prop: PropType):
        for prop_type, button in self.buttons.items():
            button.set_active(prop_type == active_prop)
