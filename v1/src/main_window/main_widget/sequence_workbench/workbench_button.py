from PyQt6.QtCore import Qt, QSize

from styles.styled_button import StyledButton, ButtonContext


class WorkbenchButton(StyledButton):
    def __init__(self, icon_path: str, tooltip: str, callback):
        super().__init__("", icon_path=icon_path, context=ButtonContext.WORKBENCH)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.clicked.connect(callback)
        self._icon_path = icon_path

    def update_size(self, button_size: int):
        self._button_size = button_size
        self.setFixedSize(button_size, button_size)
        self.setIconSize(QSize(int(button_size * 0.75), int(button_size * 0.75)))
