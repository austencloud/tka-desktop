from typing import TYPE_CHECKING, Callable
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from utils.path_helpers import get_image_path

if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget


class CodexControlButton(QPushButton):
    """A reusable button class for the Codex control panel."""

    ICON_BASE_PATH = "icons/sequence_workbench_icons"

    def __init__(
        self, control_widget: "CodexControlWidget", icon_name: str, callback: Callable
    ):
        """
        Initializes the control button with the specified icon and callback.

        :param control_widget: The CodexControlWidget that this button belongs to.
        :param icon_name: Name of the icon file (e.g. 'rotate.png').
        :param callback: The function to call when this button is clicked.
        """
        super().__init__(control_widget)
        self._control_widget = control_widget
        self.icon_name = icon_name
        self.callback = callback

        self._setup_appearance()
        self._setup_connections()

    def _setup_appearance(self) -> None:
        """Sets the button icon and basic appearance."""
        icon_path = get_image_path(f"{self.ICON_BASE_PATH}/{self.icon_name}")
        self.setIcon(QIcon(icon_path))
        font = QFont()
        font.setBold(True)
        self.setFont(font)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _setup_connections(self) -> None:
        """Connects the button click signal to the specified callback."""
        self.clicked.connect(self.callback)

    def resizeEvent(self, event) -> None:
        """Adjust icon sizes and selector size dynamically on resize."""
        super().resizeEvent(event)
        codex = self._control_widget.codex
        if not codex:
            return

        button_size = int(codex.height() * 0.05)
        icon_size = QSize(int(button_size * 0.8), int(button_size * 0.8))
        self.setFixedSize(button_size, button_size)
        self.setIconSize(icon_size)
