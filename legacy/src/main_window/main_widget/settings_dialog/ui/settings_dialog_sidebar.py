from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QEvent
from PyQt6.QtGui import QPixmap, QPainter, QColor

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.settings_dialog.legacy_settings_dialog import (
        LegacySettingsDialog,
    )


class SidebarItem(QWidget):
    """Custom widget for sidebar items with icon and text"""

    def __init__(self, name: str, icon_name: str = None, parent=None):
        super().__init__(parent)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.label = QLabel(name)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        # Add icon if provided (you would need to set up your icon resources)
        if icon_name:
            self.icon = QLabel()
            # Example of creating a simple colored icon as placeholder
            # You can replace this with real icons from resources
            pixmap = QPixmap(24, 24)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setBrush(QColor("#569cd6"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, 24, 24)
            painter.end()

            self.icon.setPixmap(pixmap)
            self.layout.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class SettingsDialogSidebar(QListWidget):
    tab_selected = pyqtSignal(int)

    def __init__(self, dialog: "LegacySettingsDialog"):
        super().__init__(dialog)
        self.setFixedWidth(240)  # Wider for better readability
        self.setSpacing(6)  # Slightly tighter spacing for modern look
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIconSize(QSize(24, 24))  # For potential icons
        self.currentRowChanged.connect(self.tab_selected)

        # Enable smooth selection effects
        self.setMouseTracking(True)

        # Remove focus outline for cleaner look
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Enable smooth animations
        self.setProperty("animated", True)

        # Set object name for styling
        self.setObjectName("modernSidebar")

    def add_item(self, name: str, icon_name: str = None):
        """Adds an item to the sidebar only if it doesn't exist."""
        for i in range(self.count()):
            if self.item(i).text() == name:
                print(
                    f"[WARNING] Sidebar already contains '{name}', skipping duplicate."
                )
                return  # Prevent duplicates

        item = QListWidgetItem(name)

        # Set item data for icon (if you want to implement this feature later)
        if icon_name:
            item.setData(Qt.ItemDataRole.UserRole, icon_name)

        # Height for better touch targets and modern spacing
        item.setSizeHint(QSize(0, 48))  # Slightly taller for modern look

        self.addItem(item)

    def enterEvent(self, event: QEvent):
        """Custom hover effect when mouse enters the widget"""
        super().enterEvent(event)
        # Don't refresh stylesheet - this was causing style overrides!

    def leaveEvent(self, event: QEvent):
        """Custom hover effect when mouse leaves the widget"""
        super().leaveEvent(event)
        # Don't refresh stylesheet - this was causing style overrides!
