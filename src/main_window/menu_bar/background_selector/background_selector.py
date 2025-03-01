# background_selector.py
from typing import TYPE_CHECKING
from ..base_selector import LabelSelector
from .background_dialog import BackgroundDialog

if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class BackgroundSelector(LabelSelector):
    def __init__(self, menu_bar: "MenuBarWidget"):
        current_background = (
            menu_bar.main_widget.settings_manager.global_settings.get_background_type()
        )
        super().__init__(menu_bar, current_background)
        self.settings_manager = self.main_widget.settings_manager

    def on_label_clicked(self):
        dialog = BackgroundDialog(self)
        dialog.show_dialog()

    def set_current_background(self, background: str):
        self.set_display_text(background)
        self.settings_manager.global_settings.set_background_type(background)
        self.main_widget.background_widget.apply_background()
