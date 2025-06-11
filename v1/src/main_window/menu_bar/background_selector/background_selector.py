# background_selector.py
from typing import TYPE_CHECKING
from ..base_selector import LabelSelector
from .background_dialog import BackgroundDialog

if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class BackgroundSelector(LabelSelector):
    def __init__(self, menu_bar: "MenuBarWidget"):
        try:
            settings_manager = menu_bar.main_widget.app_context.settings_manager
            current_background = settings_manager.global_settings.get_background_type()
            self.settings_manager = settings_manager
        except AttributeError:
            # Fallback when settings not available
            current_background = "Starfield"  # Default background
            self.settings_manager = None

        super().__init__(menu_bar, current_background)

    def on_label_clicked(self):
        dialog = BackgroundDialog(self)
        dialog.show_dialog()

    def set_current_background(self, background: str):
        self.set_display_text(background)

        # Update settings if available
        if self.settings_manager:
            self.settings_manager.global_settings.set_background_type(background)

        # Apply background if widget available
        try:
            background_widget = self.main_widget.widget_manager.get_widget(
                "background_widget"
            )
            if background_widget and hasattr(background_widget, "apply_background"):
                background_widget.apply_background()
        except AttributeError:
            # Fallback when background_widget not available
            pass
