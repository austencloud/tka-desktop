from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
    ImageExportTab,
)
from .beat_layout.beat_layout_tab import BeatLayoutTab
from .prop_type.prop_type_tab import PropTypeTab
from .user_profile.user_profile_tab import UserProfileTab
from .visibility.visibility_tab import VisibilityTab
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from ..settings_dialog import SettingsDialog


class SettingsDialogTabManager:
    def __init__(self, dialog: "SettingsDialog"):
        self.dialog = dialog
        self.tabs = {}

    def add_tab(self, name: str, widget: QWidget):
        self.dialog.ui.sidebar.add_item(name)
        self.dialog.ui.content_area.addWidget(widget)
        self.tabs[name] = widget

    def on_tab_selected(self, index: int):
        selected_tab = self.dialog.ui.content_area.widget(index)
        selected_tab_name = self._get_tab_name(selected_tab)

        if not selected_tab_name:
            return

        AppContext.settings_manager().global_settings.set_current_settings_dialog_tab(
            selected_tab_name
        )

        self._update_tab(selected_tab)
        self.dialog.ui.content_area.setCurrentIndex(index)

    def _get_tab_name(self, selected_tab: QWidget) -> str:
        for name, widget in self.tabs.items():
            if widget is selected_tab:
                return name
        return None

    def _update_tab(self, selected_tab: QWidget):
        if isinstance(selected_tab, PropTypeTab):
            selected_tab.update_active_prop_type_from_settings()
        elif isinstance(selected_tab, UserProfileTab):
            selected_tab.ui_manager.update_active_user_from_settings()
        elif isinstance(selected_tab, VisibilityTab):
            selected_tab.buttons_widget.update_visibility_buttons_from_settings()
        elif isinstance(selected_tab, BeatLayoutTab):
            selected_tab.update_beat_layout_tab(selected_tab)
        elif isinstance(selected_tab, ImageExportTab):
            selected_tab.update_image_export_tab_from_settings()

    def get_tab_index(self, tab_name: str) -> int:
        return list(self.tabs.keys()).index(tab_name) if tab_name in self.tabs else 0
