from PyQt6.QtCore import Qt

from styles.styled_button import StyledButton


class FilterButton(StyledButton):
    def __init__(self, label: str):
        super().__init__(label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
