from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QFont, QColor

from main_window.main_widget.settings_dialog.ui.user_profile.profile_picture_manager import (
    ProfilePictureManager,
)
from styles.dark_theme_styler import DarkThemeStyler

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.user_profile.user_profile_tab import (
        UserProfileTab,
    )


class UserButton(QPushButton):
    """A button representing a user with profile picture support."""

    def __init__(
        self, user_name: str, parent: "UserProfileTab", is_current: bool = False
    ):
        super().__init__(parent)
        self.user_name = user_name
        self.parent_tab = parent
        self._is_current = is_current
        self.profile_pixmap = ProfilePictureManager.get_profile_picture(user_name)

        # Setup the button appearance
        self.setText("")  # We'll handle text rendering in paintEvent
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(lambda: self.parent_tab.set_current_user(self.user_name))

        # Set active state styling
        self.set_current(is_current)

    def update_size(self):
        """Update button size based on available space."""
        width = self.parent_tab.width() // 4
        height = width  # Make it square

        # Set a minimum size
        width = max(100, width)
        height = max(100, height)

        self.setFixedSize(width, height)

    def set_current(self, is_current: bool):
        """Sets this user as the current active user."""
        self._is_current = is_current

        if is_current:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    {DarkThemeStyler.ACTIVE_BG_GRADIENT}
                    border: 2px solid {DarkThemeStyler.ACCENT_COLOR};
                    color: white;
                    padding: 8px;
                    border-radius: 10px;
                    font-weight: bold;
                    text-align: center;
                }}
                """
            )
        else:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    {DarkThemeStyler.DEFAULT_BG_GRADIENT}
                    border: 1px solid {DarkThemeStyler.BORDER_COLOR};
                    color: {DarkThemeStyler.TEXT_COLOR};
                    padding: 8px;
                    border-radius: 10px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    {DarkThemeStyler.DARK_HOVER_GRADIENT}
                }}
                """
            )

    def paintEvent(self, event):
        """Custom paint event to show username and profile picture."""
        # First, let the button draw its background
        super().paintEvent(event)

        # Get button dimensions
        rect = self.rect()
        width = rect.width()
        height = rect.height()

        # Set up painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the username at the top
        username_height = height // 4
        font = QFont(self.font())
        font.setPointSize(max(9, width // 12))
        font.setBold(True)
        painter.setFont(font)

        # Set text color based on active state
        if self._is_current:
            painter.setPen(Qt.GlobalColor.white)
        else:
            # Convert string color to QColor object
            painter.setPen(QColor(DarkThemeStyler.TEXT_COLOR))

        # Draw username text
        username_rect = QRect(0, 8, width, username_height)
        painter.drawText(
            username_rect,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
            self.user_name,
        )

        # If we have a profile picture, draw it below the username
        if self.profile_pixmap and not self.profile_pixmap.isNull():
            # Calculate image size (60% of button width)
            image_size = int(width * 0.6)

            # Calculate positions - center horizontally, position below username
            image_x = (width - image_size) // 2
            image_y = username_height + 8  # Leave some space after username

            # Create and draw circular profile picture
            circular_pixmap = ProfilePictureManager.create_circular_pixmap(
                self.profile_pixmap, image_size
            )
            painter.drawPixmap(image_x, image_y, circular_pixmap)
        # No placeholder needed when no profile picture is available

        painter.end()
