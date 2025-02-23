from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget, QWidget


from .settings_dialog_sidebar import SettingsDialogSidebar
from .settings_dialog_tab_manager import SettingsDialogTabManager
from .beat_layout_tab.beat_layout_tab import BeatLayoutTab
from .prop_type_tab.prop_type_tab import PropTypeTab
from .user_profile_tab.user_profile_tab import UserProfileTab
from .visibility_tab.visibility_tab import VisibilityTab

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class SettingsDialogUI(QWidget):
    def __init__(self, dialog: "SettingsDialog"):
        super().__init__(dialog)
        self.dialog = dialog
        self.sidebar = SettingsDialogSidebar(dialog)
        self.content_area = QStackedWidget(self)
        self.tab_manager = SettingsDialogTabManager(dialog)

    def setup_ui(self):
        """Initializes UI components and layout."""
        main_layout = QHBoxLayout(self)
        self.setLayout(main_layout)

        self.tab_manager.tabs = {
            "User Profile": UserProfileTab(self.dialog),
            "Prop Type": PropTypeTab(self.dialog),
            "Visibility": VisibilityTab(self.dialog),
            "Beat Layout": BeatLayoutTab(self.dialog),
        }

        # Store individual tab references for easier access
        self.user_profile_tab: UserProfileTab = self.tab_manager.tabs["User Profile"]
        self.prop_type_tab: PropTypeTab = self.tab_manager.tabs["Prop Type"]
        self.visibility_tab: VisibilityTab = self.tab_manager.tabs["Visibility"]
        self.beat_layout_tab: BeatLayoutTab = self.tab_manager.tabs["Beat Layout"]

        for name, widget in self.tab_manager.tabs.items():
            self.tab_manager.add_tab(name, widget)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area, stretch=1)

        self.sidebar.tab_selected.connect(self.tab_manager.on_tab_selected)

    def _on_tab_selected(self, index: int):
        self.tab_manager.on_tab_selected(index)
