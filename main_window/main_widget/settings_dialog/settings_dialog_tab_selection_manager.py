from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
)

from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import (
    VisibilityTab,
)

from .prop_type_tab.prop_type_tab import PropTypeTab
from .user_profile_tab.user_profile_tab import UserProfileTab
from main_window.settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class SettingsDialogTabSelectionManager:
    def __init__(self, dialog: "SettingsDialog"):
        self.dialog = dialog
        self.tabs = {}

    def add_tab(self, name: str, widget: QWidget):
        self.dialog.ui.sidebar.add_item(name)
        self.dialog.ui.content_area.addWidget(widget)

    def on_tab_selected(self, index: int):
        selected_tab = self.dialog.ui.content_area.widget(index)

        selected_tab_name = None
        for name, widget in self.tabs.items():
            if widget is selected_tab:
                selected_tab_name = name
                break

        if not selected_tab_name:
            print("[ERROR] No tab name found for index:", index)
            return

        print(f"[DEBUG] Switched to tab: {selected_tab_name}")

        AppContext.settings_manager().global_settings.set_current_settings_dialog_tab(
            selected_tab_name
        )

        if isinstance(selected_tab, PropTypeTab):
            selected_tab.update_active_prop_type_from_settings()
        elif isinstance(selected_tab, UserProfileTab):
            selected_tab.ui_manager.update_active_user_from_settings()
        elif isinstance(selected_tab, VisibilityTab):
            selected_tab.buttons_widget.update_visibility_buttons_from_settings()
        self.dialog.ui.content_area.setCurrentIndex(index)

    def get_tab_index(self, tab_name: str) -> int:
        return list(self.tabs.keys()).index(tab_name) if tab_name in self.tabs else 0
