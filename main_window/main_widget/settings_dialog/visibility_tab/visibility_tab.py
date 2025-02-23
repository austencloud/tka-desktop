from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from .pictograph.visibility_pictograph import VisibilityPictograph
from .visibility_toggler import VisibilityToggler
from .buttons_widget.visibility_buttons_widget import VisibilityButtonsWidget
from .pictograph.visibility_pictograph_view import VisibilityPictographView
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..settings_dialog import SettingsDialog


class VisibilityTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.main_widget = settings_dialog.main_widget
        self.settings = self.main_widget.settings_manager.visibility
        self.dialog = settings_dialog
        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        """Initialize the pictograph and button toggles."""
        self.toggler = VisibilityToggler(self)
        self.pictograph = VisibilityPictograph(self)
        self.pictograph_view = VisibilityPictographView(self, self.pictograph)
        self.buttons_widget = VisibilityButtonsWidget(self)

    def _setup_layout(self):
        """Organizes the layout: pictograph on top, buttons in a grid below."""
        layout = QVBoxLayout(self)
        # layout.setSpacing(15)

        # 📌 Add the pictograph at the top
        layout.addWidget(
            self.pictograph_view, stretch=3, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # 📌 Add the button grid below the pictograph
        layout.addWidget(self.buttons_widget, 1)

        self.setLayout(layout)
