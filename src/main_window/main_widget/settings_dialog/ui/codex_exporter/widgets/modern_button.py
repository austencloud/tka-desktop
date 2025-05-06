"""
Modern button with custom styling.
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Dark Mode Theme Colors
DARK_BG = "#121212"  # Main background
CARD_BG = "#1E1E1E"  # Card background
SURFACE = "#252525"  # Surface elements
BORDER_LIGHT = "#333333"  # Light border
ACCENT_RED = "#FF4F6C"  # Red hand color
ACCENT_BLUE = "#4F9BFF"  # Blue hand color
ACCENT_GREEN = "#4FFF8F"  # Action button color
TEXT_PRIMARY = "#FFFFFF"  # Primary text
TEXT_SECONDARY = "#B0B0B0"  # Secondary text
DISABLED_BG = "#2A2A2A"  # Disabled element background
DISABLED_TEXT = "#666666"  # Disabled text


class ModernButton(QPushButton):
    """A modern button with custom styling."""

    def __init__(self, text, parent=None, primary=True):
        super().__init__(text, parent)
        self.primary = primary

        # Set the appropriate objectName for theming
        if primary:
            self.setObjectName("primary")
        else:
            self.setObjectName("secondary")

        # Set cursor to pointing hand
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Set minimum size for better touch targets
        self.setMinimumHeight(44)
        self.setMinimumWidth(120)

        # Set font
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.setFont(font)

        # Apply styling based on primary/secondary
        self._apply_styling()

    def _apply_styling(self):
        """Apply styling based on primary/secondary button type."""
        if self.primary:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {ACCENT_GREEN};
                    color: {DARK_BG};
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                }}
                QPushButton:hover {{
                    background-color: #62FFAC;
                }}
                QPushButton:pressed {{
                    background-color: #3AE07A;
                }}
                QPushButton:disabled {{
                    background-color: {DISABLED_BG};
                    color: {DISABLED_TEXT};
                }}
            """
            )
        else:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: transparent;
                    color: {TEXT_PRIMARY};
                    border: 1px solid {BORDER_LIGHT};
                    border-radius: 8px;
                    padding: 12px 24px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                }}
                QPushButton:pressed {{
                    background-color: rgba(255, 255, 255, 0.15);
                }}
                QPushButton:disabled {{
                    background-color: transparent;
                    color: {DISABLED_TEXT};
                    border: 1px solid {DISABLED_BG};
                }}
            """
            )
