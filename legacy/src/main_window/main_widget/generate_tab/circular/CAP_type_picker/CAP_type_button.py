# updated file: main_window/main_widget/generate_tab/widgets/CAP_type_button.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal
from styles.dark_theme_styler import DarkThemeStyler

if TYPE_CHECKING:
    from .CAP_picker import CAPPicker


class CAPTypeButton(QPushButton):
    toggled = pyqtSignal(bool)

    def __init__(
        self,
        text: str,
        perm_type: str,
        CAP_type_picker: "CAPPicker",
    ):
        super().__init__(text, CAP_type_picker)
        self.CAP_type_picker = CAP_type_picker
        self.perm_type = perm_type
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setCheckable(True)
        self._is_toggled = False
        self.clicked.connect(self._handle_click)
        self._apply_style(False)

    def _handle_click(self):
        self.set_active(not self._is_toggled)
        self.toggled.emit(self._is_toggled)

    def set_active(self, is_active: bool):
        self._is_toggled = is_active
        self.setChecked(is_active)
        self._apply_style(is_active)

    def _apply_style(self, is_active: bool):
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
            """
            )

    def resizeEvent(self, event):
        target_width = self.CAP_type_picker.generate_tab.main_widget.width() // 12
        target_height = self.CAP_type_picker.generate_tab.main_widget.height() // 24
        self.setFixedSize(target_width, target_height)

        # Set font size based on button height
        font = self.font()
        font.setPointSize(int(target_height * 0.2))  # Font size ~30% of button height
        self.setFont(font)

        super().resizeEvent(event)
