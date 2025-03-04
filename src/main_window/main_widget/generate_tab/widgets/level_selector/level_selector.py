from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QToolButton, QLabel
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt, QSize
from typing import TYPE_CHECKING

from main_window.main_widget.generate_tab.widgets.level_selector.level_selector_difficulty_drawer import (
    LevelSelectorDifficultyDrawer,
)

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class LevelSelector(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__()
        self.generate_tab = generate_tab
        self.drawer = LevelSelectorDifficultyDrawer()
        self.buttons: list[QToolButton] = []
        self.info_labels: list[QLabel] = []
        self.current_level = self.generate_tab.settings.get_setting("level")
        self.default_icon_size = QSize(64, 64)
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.main_layout.addStretch(4)

        level_data = [
            ("No Turns", "Base motions only\nNo turns added"),
            ("Whole Turns", "Whole turns allowed\nRadial orientations only"),
            ("Half Turns", "Half turns allowed\nRadial/nonradial orientations"),
        ]

        for i, (label_text, info_text) in enumerate(level_data):
            vbox = QVBoxLayout()
            vbox.setSpacing(5)
            vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

            button = QToolButton()
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.setCheckable(True)
            button.setToolTip(info_text)
            button.clicked.connect(lambda _, idx=i: self.set_level(idx + 1))

            info_label = QLabel(label_text)
            info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            info_label.setStyleSheet("color: white; font-size: 12pt; font-weight: bold;")

            self.buttons.append(button)
            self.info_labels.append(info_label)

            vbox.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
            vbox.addWidget(info_label)

            self.main_layout.addLayout(vbox)
            self.main_layout.addStretch(1)

        self.main_layout.addStretch(3)
        self.setLayout(self.main_layout)

        self._update_icons()

    def _apply_styles(self):
        self.setStyleSheet(
            """
            QToolButton {
                background: transparent;
                border: none;
                margin: 0;
                padding: 0;
                outline: 0;
            }
            QToolButton:hover:!checked {
                background: rgba(200, 200, 200, 30);
                border-radius: 10px;
            }
            QToolButton:checked {
                background: rgba(255, 255, 255, 60);  /* Make checked buttons more visible */
                border: 2px solid rgba(255, 255, 255, 150);
                border-radius: 10px;
            }
            """
        )

    def set_level(self, level: int):
        """Sets the selected difficulty level and updates the UI."""
        self.current_level = level
        for i, btn in enumerate(self.buttons):
            btn.setChecked((i + 1) == level)
        self._update_icons()
        self._update_sequence_settings(level)

    def _update_icons(self):
        """Updates the icons based on the difficulty level using the drawer."""
        icon_size = self._desired_icon_size()
        for i, btn in enumerate(self.buttons):
            is_selected = (i + 1) == self.current_level
            pixmap = self.drawer.get_difficulty_level_pixmap(i + 1, icon_size.width())
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(icon_size)
            btn.setFixedSize(icon_size.width() + 10, icon_size.height() + 10)

    def _desired_icon_size(self) -> QSize:
        """Dynamically adjusts the icon size based on the UI's parent size."""
        parent_size = self.generate_tab.size()
        side = max(32, parent_size.width() // 10)
        return QSize(side, side)

    def resizeEvent(self, event):
        """Ensures icons update dynamically when the UI resizes."""
        super().resizeEvent(event)
        self._update_icons()

    def _update_sequence_settings(self, level: int):
        """Updates the selected level setting and modifies UI elements accordingly."""
        self.generate_tab.settings.set_setting("level", str(level))

        adjuster = self.generate_tab.turn_intensity
        adjuster.setVisible(level > 1)
        if level > 1:
            adjuster.adjust_values(level)
