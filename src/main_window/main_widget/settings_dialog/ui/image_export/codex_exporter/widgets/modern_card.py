"""
Modern card widget with rounded corners and shadow.
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout


class ModernCard(QFrame):
    """A modern card widget with rounded corners and shadow."""

    def __init__(self, parent=None, title="", content_margin=12):
        super().__init__(parent)
        self.title = title
        self.content_margin = content_margin
        self._setup_ui()

    def _setup_ui(self):
        # Set frame style
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setObjectName("modernCard")

        # Apply stylesheet that works in both light and dark mode
        self.setStyleSheet(
            """
            #modernCard {
                background-color: palette(light);
                border-radius: 10px;
                border: 1px solid palette(mid);
                color: palette(text);
            }
        """
        )

        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(
            self.content_margin,
            self.content_margin,
            self.content_margin,
            self.content_margin,
        )
        self.layout.setSpacing(10)

        # Add title if provided
        if self.title:
            from PyQt6.QtWidgets import QLabel

            title_label = QLabel(self.title)
            title_label.setObjectName("cardTitle")
            title_label.setStyleSheet(
                """
                #cardTitle {
                    font-size: 16px;
                    font-weight: bold;
                    color: palette(text);
                }
            """
            )
            self.layout.addWidget(title_label)
