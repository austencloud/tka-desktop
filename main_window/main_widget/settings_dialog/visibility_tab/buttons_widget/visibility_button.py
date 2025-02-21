from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QEvent, pyqtProperty
from PyQt6.QtGui import QCursor, QFont, QColor, QPainter, QPen, QBrush
from typing import TYPE_CHECKING
from .visibility_button_animation import VisibilityButtonAnimation

if TYPE_CHECKING:
    from .visibility_buttons_widget import VisibilityButtonsWidget


class VisibilityButton(QPushButton):
    def __init__(
        self, name: str, visibility_checkbox_widget: "VisibilityButtonsWidget"
    ):
        super().__init__(name)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.visibility_checkbox_widget = visibility_checkbox_widget
        self.toggler = self.visibility_checkbox_widget.toggler
        self.name = name
        self.view = self.visibility_checkbox_widget.visibility_tab.pictograph_view
        self.visibility_tab = self.visibility_checkbox_widget.visibility_tab

        # Custom properties
        self.is_hovered = False
        self.is_toggled = False
        self._background_color = QColor("#F5F5F5")
        self._text_color = QColor("#000000")

        # Animation manager
        self.animations = VisibilityButtonAnimation(self)

        self._connect_signals()
        self._initialize_state()

    def _initialize_state(self):
        """Initialize the toggle state and colors based on settings."""
        self.update_is_toggled(self.name)
        self.update_colors()

    def update_colors(self):
        """Update the background and text colors based on the toggle state."""
        self.background_color = QColor("#4CAF50" if self.is_toggled else "#F5F5F5")
        self.text_color = QColor("#FFFFFF" if self.is_toggled else "#000000")

    @pyqtProperty(QColor)
    def background_color(self):
        """Custom property for animating background color."""
        return self._background_color

    @background_color.setter
    def background_color(self, color: QColor):
        self._background_color = color
        self.update()  # Trigger a repaint when the color changes

    @pyqtProperty(QColor)
    def text_color(self):
        """Custom property for animating text color."""
        return self._text_color

    @text_color.setter
    def text_color(self, color: QColor):
        self._text_color = color
        self.update()  # Trigger a repaint when the color changes

    def update_is_toggled(self, name):
        """Update toggle state based on settings."""
        if name in self.visibility_checkbox_widget.glyph_names:
            self.is_toggled = self.visibility_checkbox_widget.visibility_tab.settings.get_glyph_visibility(
                name
            )
        else:
            self.is_toggled = (
                self.visibility_checkbox_widget.visibility_tab.settings.get_non_radial_visibility()
            )
        self.update_colors()

    def _connect_signals(self):
        self.clicked.connect(self._toggle_state)

    def _toggle_state(self):
        """Handle button toggle state with parallel fading."""
        self.is_toggled = not self.is_toggled

        self.animations.play_toggle_animation(self.is_toggled)

        target_opacity = 1.0 if self.is_toggled else 0.1

        if self.name in self.visibility_checkbox_widget.glyph_names:
            element = self.view.pictograph.managers.get.glyph(self.name)
        else:
            element = self.view.pictograph.managers.get.non_radial_points()

        # Create a parallel fade animation
        self.visibility_tab.pictograph.elements.view.interaction_manager.fade_and_toggle_visibility(
            element, self.is_toggled
        )

    def paintEvent(self, event):
        """Custom paint event for button visuals."""
        painter = QPainter(self)
        rect = self.rect()

        # Set the background color
        painter.setBrush(QBrush(self.background_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self.height() // 5, self.height() // 5)

        # Draw border
        border_color = QColor("#388E3C" if self.is_toggled else "#9E9E9E")
        pen = QPen(border_color, 2 if self.is_hovered or self.is_toggled else 1)
        painter.setPen(pen)
        painter.drawRoundedRect(rect, self.height() // 5, self.height() // 5)

        # Draw text
        painter.setPen(self.text_color)
        font = self.font()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
        painter.end()

    def enterEvent(self, event):
        """Mouse enters the button area."""
        self.is_hovered = True
        self.update()  # Repaint on hover

    def leaveEvent(self, event):
        """Mouse leaves the button area."""
        self.is_hovered = False
        self.update()  # Repaint on hover exit

    def resizeEvent(self, event: QEvent):
        """Adjust font size dynamically on resize."""
        width = self.visibility_tab.width()
        font_size = max(10, width // 40)
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        super().resizeEvent(event)
