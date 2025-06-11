"""
Modern card widget with rounded corners and shadow.
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QColor
from ..theme import Sizing, StyleSheet


class ModernCard(QFrame):
    """A modern card widget with rounded corners and shadow."""

    def __init__(self, parent=None, title="", content_margin=16):
        super().__init__(parent)
        self.title = title
        self.content_margin = content_margin
        self._setup_ui()

    def _setup_ui(self):
        # Create sizing and style sheet instances
        sizing = Sizing(self)
        style_sheet = StyleSheet(sizing)

        # Set frame style
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setObjectName("modernCard")

        # Set cssClass property for QSS styling
        self.setProperty("cssClass", "card")

        # Apply modern styling using the central theme
        self.setStyleSheet(style_sheet.card())

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        # Create layout with improved spacing
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(
            self.content_margin,
            self.content_margin,
            self.content_margin,
            self.content_margin,
        )
        self.layout.setSpacing(sizing.spacing_md)  # Use theme spacing

        # Add title if provided
        if self.title:
            title_label = QLabel(self.title)
            title_label.setObjectName("cardTitle")

            # Set font
            title_font = QFont()
            title_font.setPointSize(sizing.font_xlarge)
            title_font.setBold(True)
            title_label.setFont(title_font)

            # The styling for the title is included in the card style sheet
            self.layout.addWidget(title_label)
