# updated file: main_window/main_widget/generate_tab/widgets/permutation_type_button.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import Qt, pyqtSignal
from styles.dark_theme_styler import DarkThemeStyler

if TYPE_CHECKING:
    from .permutation_type_picker import PermutationTypePicker


class PermutationTypeButton(QPushButton):
    toggled = pyqtSignal(bool)

    def __init__(
        self,
        text: str,
        perm_type: str,
        permutation_type_picker: "PermutationTypePicker",
    ):
        super().__init__(text, permutation_type_picker)
        self.permutation_type_picker = permutation_type_picker
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
        font = self.font()
        font.setPointSize(self.permutation_type_picker.generate_tab.height() // 60)
        self.setFont(font)
        self.setFixedSize(
            self.permutation_type_picker.generate_tab.width() // 4,
            self.permutation_type_picker.generate_tab.height() // 12,
        )
        super().resizeEvent(event)
