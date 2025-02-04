from typing import TYPE_CHECKING
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QTabWidget, QPushButton
if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class SettingsDialogStyler:
    def __init__(self, dialog: "SettingsDialog"):
        self.dialog = dialog
    
    def style_tab_widget(self, tab_widget: QTabWidget):
        # Tab widget palette
        palette = tab_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#F5F5F5"))
        tab_widget.setPalette(palette)

        tab_bar = tab_widget.tabBar()

        # Iterate through each tab and adjust margins for spacing
        for i in range(tab_bar.count()):
            tab_bar.setTabTextColor(i, QColor("#333333"))
            tab_bar.setTabData(i, {"hovered": False})  # Store hover state

    def style_button(self, button: QPushButton):
        # Default button styling
        button.setStyleSheet("""
            QPushButton {
                background-color: #66B2FF;
                color: white;
                border-radius: 10px;
                padding: 10px 15px;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)



