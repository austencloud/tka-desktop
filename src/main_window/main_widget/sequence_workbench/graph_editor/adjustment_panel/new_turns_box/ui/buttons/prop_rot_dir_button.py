# === turns_box/ui/buttons/prop_rot_dir_button.py ===
from typing import TYPE_CHECKING, Callable
from PyQt6.QtCore import Qt, QSize

from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class PropRotDirButton(StyledButton):
    """Button for selecting prop rotation direction"""

    def __init__(
        self, turns_box: "TurnsBox", prop_rot_dir: str, icon_path: str
    ) -> None:
        super().__init__(label="", icon_path=icon_path)
        self.turns_box = turns_box
        self.prop_rot_dir = prop_rot_dir

        # Setup
        self._setup_button()

        # Connect signals
        self.clicked.connect(self._on_clicked)

    def _setup_button(self) -> None:
        """Setup button appearance and behavior"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        direction_name = self.prop_rot_dir.replace("_", " ").title()
        self.setToolTip(f"Set {direction_name} Rotation")

    def _on_clicked(self) -> None:
        """Handle button clicks"""
        self.turns_box.prop_rot_dir_manager.set_prop_rot_dir(self.prop_rot_dir)

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        # Calculate sizes based on parent dimensions
        button_size = int(self.turns_box.graph_editor.height() * 0.25)
        icon_size = int(button_size * 0.8)

        # Apply sizes
        self.setFixedSize(button_size, button_size)
        self.setIconSize(QSize(icon_size, icon_size))

        super().resizeEvent(event)
