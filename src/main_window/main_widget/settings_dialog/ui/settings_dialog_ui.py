from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget, QWidget, QVBoxLayout

from .beat_layout.beat_layout_tab import BeatLayoutTab
from .codex_exporter.codex_exporter_tab import CodexExporterTab
from .image_export.image_export_tab import ImageExportTab
from .prop_type.prop_type_tab import PropTypeTab
from .user_profile.user_profile_tab import UserProfileTab
from .visibility.visibility_tab import VisibilityTab
from .settings_dialog_action_buttons import SettingsDialogActionButtons
from .settings_dialog_sidebar import SettingsDialogSidebar
from .settings_dialog_tab_manager import SettingsDialogTabManager

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class SettingsDialogUI(QWidget):
    def __init__(self, dialog: "SettingsDialog"):
        super().__init__(dialog)
        self.dialog = dialog
        self.sidebar = SettingsDialogSidebar(dialog)
        self.content_area = QStackedWidget(self)
        self.tab_selection_manager = SettingsDialogTabManager(dialog)
        self.action_buttons = SettingsDialogActionButtons(dialog)

    def setup_ui(self):
        """Initializes UI components and layout."""
        self.main_vertical_layout = QVBoxLayout(self)
        horizontal_main_layout = QHBoxLayout()

        self.tab_selection_manager.tabs = {
            "User Profile": UserProfileTab(self.dialog),
            "Prop Type": PropTypeTab(self.dialog),
            "Visibility": VisibilityTab(self.dialog),
            "Beat Layout": BeatLayoutTab(self.dialog),
            "Image Export": ImageExportTab(self.dialog),
            "Codex Exporter": CodexExporterTab(self.dialog),
        }

        self.user_profile_tab: UserProfileTab = self.tab_selection_manager.tabs[
            "User Profile"
        ]

        self.prop_type_tab: PropTypeTab = self.tab_selection_manager.tabs["Prop Type"]
        self.visibility_tab: VisibilityTab = self.tab_selection_manager.tabs[
            "Visibility"
        ]
        self.beat_layout_tab: BeatLayoutTab = self.tab_selection_manager.tabs[
            "Beat Layout"
        ]
        self.image_export_tab: ImageExportTab = self.tab_selection_manager.tabs[
            "Image Export"
        ]
        self.codex_exporter_tab: CodexExporterTab = self.tab_selection_manager.tabs[
            "Codex Exporter"
        ]
        for name, widget in self.tab_selection_manager.tabs.items():
            self.tab_selection_manager.add_tab(name, widget)

        horizontal_main_layout.addWidget(self.sidebar)
        horizontal_main_layout.addWidget(self.content_area, stretch=1)

        self.main_vertical_layout.addLayout(horizontal_main_layout)
        self.main_vertical_layout.addWidget(self.action_buttons)

        self.sidebar.tab_selected.connect(self.tab_selection_manager.on_tab_selected)

    def _on_tab_selected(self, index: int):
        self.tab_selection_manager.on_tab_selected(index)
