from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from styles.button_state import ButtonState
from styles.metallic_blue_button_theme import MetallicBlueButtonTheme


class BaseStyledButton(QPushButton):
    """A base QPushButton with shared metallic blue styling and state handling."""

    clicked_signal = pyqtSignal(str)  # Custom signal for button clicks

    def __init__(self, label: str):
        super().__init__(label)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._state = ButtonState.NORMAL
        self._border_radius = 5
        self.update_appearance()

        self.clicked.connect(self._on_clicked)

    @property
    def state(self) -> ButtonState:
        return self._state

    @state.setter
    def state(self, new_state: ButtonState) -> None:
        if self._state != new_state:
            self._state = new_state
            self.update_appearance()

    def update_appearance(self) -> None:
        """Update button appearance dynamically based on state and enabled status."""
        theme = MetallicBlueButtonTheme.get_default_theme(self._state, self.isEnabled())

        self.setStyleSheet(
            f"""
            QPushButton {{
                background: {theme.background};
                border-radius: {self._border_radius}px;
                color: {theme.font_color};
                padding: 10px;
                font-weight: bold;
                text-align: center;
                border: 1px solid {theme.border_color};
            }}
            QPushButton:hover {{
                background: {theme.hover_background};
                color: {theme.hover_font_color};
                border: 1px solid white;
            }}
            QPushButton:pressed {{
                background: {theme.pressed_background};
                color: {theme.pressed_font_color};
                border: 1px solid white;
            }}
        """
        )

    def set_selected(self, selected: bool) -> None:
        """Update selection state and restyle the button."""
        self.state = ButtonState.SELECTED if selected else ButtonState.NORMAL

    def setEnabled(self, enabled: bool) -> None:
        """Enable or disable the button and update its style dynamically."""
        super().setEnabled(enabled)
        self.setCursor(
            QCursor(
                Qt.CursorShape.PointingHandCursor
                if enabled
                else Qt.CursorShape.ForbiddenCursor
            )
        )
        self.update_appearance()

    def _on_clicked(self) -> None:
        """Emit a signal when clicked."""
        self.clicked_signal.emit(self.text())

    def resizeEvent(self, event: QEvent) -> None:
        """Handle resizing to adjust border radius dynamically."""
        self._border_radius = min(self.height(), self.width()) // 2
        self.update_appearance()
        super().resizeEvent(event)
