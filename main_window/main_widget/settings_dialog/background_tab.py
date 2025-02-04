from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog

class BackgroundTab(QWidget):
    buttons: list[QPushButton] = []
    
    def __init__(self, dialog: "SettingsDialog"):
        super().__init__()
        self.dialog = dialog
        self.main_widget = dialog.main_widget
        self._setup_ui()
        
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.title = QLabel("Background Settings")
        layout.addWidget(self.title)

        # Available background options
        backgrounds = ["Starfield", "Aurora", "Snowfall", "Bubbles"]

        for background in backgrounds:
            button = QPushButton(background)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet("margin: 5px;")
            button.clicked.connect(lambda _, b=background: self._set_background(b))
            self.buttons.append(button)
            layout.addWidget(button)

        layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )
        self.setLayout(layout)

    def _set_background(self, background: str):
        settings_manager = self.main_widget.settings_manager
        settings_manager.global_settings.set_background_type(background)
        self.main_widget.background_widget.apply_background()

    def _get_title_font(self):
        font = QFont()
        font.setPointSize(self.dialog.calculate_font_size())
        font.setBold(True)
        return font

    def resizeEvent(self, event):
        self.title.setFont(self._get_title_font())
        font_size = self.dialog.calculate_font_size()
        for button in self.buttons:
            # button.font().setPointSize(font_size)
            button_font = button.font()
            button_font.setPointSize(font_size)
            button.setFont(button_font)