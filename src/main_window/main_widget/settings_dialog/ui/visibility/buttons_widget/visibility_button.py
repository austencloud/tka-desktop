from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from styles.button_state import ButtonState
from styles.dark_theme_styler import DarkThemeStyler
from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from .visibility_buttons_widget import VisibilityButtonsWidget


class VisibilityButton(StyledButton):

    def __init__(self, name: str, visibility_buttons_widget: "VisibilityButtonsWidget"):
        super().__init__(name)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.visibility_buttons_widget = visibility_buttons_widget
        self.name = name
        self.is_toggled = False

        self.clicked.connect(self._toggle_state)

    def _initialize_state(self):
        self.update_is_toggled(self.name)
        self.repaint()

    def update_is_toggled(self, name: str):
        if name in ["Red Motion", "Blue Motion"]:
            color = name.split(" ")[0].lower()
            is_toggled = self.visibility_buttons_widget.visibility_tab.settings.get_motion_visibility(
                color
            )
        else:
            is_toggled = self.visibility_buttons_widget.visibility_tab.settings.get_glyph_visibility(
                name
            )
        self.is_toggled = is_toggled

    def _toggle_state(self):
        self.is_toggled = not self.is_toggled
        view = self.visibility_buttons_widget.visibility_tab.pictograph_view

        if self.name in ["Red Motion", "Blue Motion"]:
            color = self.name.split(" ")[0].lower()
            motion = view.pictograph.managers.get.motion_by_color(color)
            self.visibility_buttons_widget.visibility_tab.toggler.toggle_prop_visibility(
                color, self.is_toggled
            )
            view.interaction_manager.fade_and_toggle_visibility(
                motion.prop, self.is_toggled
            )
            view.interaction_manager.fade_and_toggle_visibility(
                motion.arrow, self.is_toggled
            )

        elif self.name in self.visibility_buttons_widget.glyph_names:
            element = view.pictograph.managers.get.glyph(self.name)
            view.interaction_manager.fade_and_toggle_visibility(
                element, self.is_toggled
            )
        else:
            element = view.pictograph.managers.get.non_radial_points()
            view.interaction_manager.fade_and_toggle_visibility(
                element, self.is_toggled
            )

        self.state = ButtonState.ACTIVE if self.is_toggled else ButtonState.NORMAL
        self.update_appearance()

    def set_active(self, is_active: bool):
        self.is_toggled = is_active
        self.state = ButtonState.ACTIVE if is_active else ButtonState.NORMAL
        self.update_appearance()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        tab_width = self.visibility_buttons_widget.visibility_tab.width()
        font_size = int(tab_width / 40)
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
