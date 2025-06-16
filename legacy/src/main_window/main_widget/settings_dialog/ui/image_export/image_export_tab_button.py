from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from styles.dark_theme_styler import DarkThemeStyler

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )
    from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager


class ImageExportTabButton(QPushButton):
    def __init__(
        self,
        name: str,
        setting_key: str,
        settings_manager: "LegacySettingsManager",
        image_export_tab: "ImageExportTab",
    ):
        super().__init__(name, image_export_tab)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setting_key = setting_key
        self.settings_manager = settings_manager
        self.is_toggled = False
        self.clicked.connect(self._toggle_state)
        self._initialize_state()

    def _initialize_state(self):
        self.update_is_toggled()
        self.repaint()

    def update_is_toggled(self):
        is_toggled = self.settings_manager.image_export.get_image_export_setting(
            self.setting_key
        )
        self.is_toggled = is_toggled
        self._apply_style(self.is_toggled)

    def _toggle_state(self):
        self.is_toggled = not self.is_toggled
        self.settings_manager.image_export.set_image_export_setting(
            self.setting_key, self.is_toggled
        )
        self._apply_style(self.is_toggled)

    def set_active(self, is_active: bool):
        self.is_toggled = is_active
        self._apply_style(is_active)

    def _apply_style(self, is_active=False):
        if is_active:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    {DarkThemeStyler.ACTIVE_BG_GRADIENT}
                    border: 2px solid {DarkThemeStyler.ACCENT_COLOR};
                    color: white;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    {DarkThemeStyler.ACTIVE_BG_GRADIENT}
                }}
                QPushButton:pressed {{
                    background-color: {DarkThemeStyler.BORDER_COLOR};
                }}
            """
            )
        else:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    {DarkThemeStyler.DEFAULT_BG_GRADIENT}
                    border: 2px solid {DarkThemeStyler.BORDER_COLOR};
                    color: {DarkThemeStyler.TEXT_COLOR};
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    {DarkThemeStyler.DARK_HOVER_GRADIENT}
                }}
                QPushButton:pressed {{
                    background-color: {DarkThemeStyler.BORDER_COLOR};
                }}
            """
            )
        self.update()
        self.repaint()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        parent_width = self.parentWidget().width() if self.parentWidget() else 200
        font_size = int(parent_width / 60)
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
