from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget


from main_window.main_widget.fade_manager.fade_manager import FadeManager
from main_window.main_widget.pictograph_collector import PictographCollector
from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog
from .construct_tab.construct_tab import ConstructTab
from .generate_tab.generate_tab import GenerateTab
from .write_tab.write_tab import WriteTab
from .browse_tab.browse_tab import BrowseTab
from .learn_tab.learn_tab import LearnTab
from .main_background_widget.main_background_widget import MainBackgroundWidget
from .font_color_updater.font_color_updater import (
    FontColorUpdater,
)
from ..menu_bar.menu_bar import MenuBarWidget
from .sequence_workbench.sequence_workbench import SequenceWorkbench

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetUI:
    def __init__(self, main_widget: "MainWidget"):
        self.mw = main_widget
        self.splash_screen = main_widget.splash_screen
        self._setup_components()
        self._setup_layout()
        self._setup_indices()

    def _setup_components(self):
        self.mw.left_stack = QStackedWidget()
        self.mw.right_stack = QStackedWidget()

        self.mw.fade_manager = FadeManager(self.mw)
        self.mw.font_color_updater = FontColorUpdater(self.mw)
        splash = self.splash_screen
        splash.updater.update_progress("MenuBarWidget")
        self.mw.menu_bar = MenuBarWidget(self.mw)

        splash.updater.update_progress("SequenceWorkbench")
        self.mw.sequence_workbench = SequenceWorkbench(self.mw)
        splash.updater.update_progress("ConstructTab")
        self.mw.construct_tab = ConstructTab(self.mw)
        splash.updater.update_progress("GenerateTab")
        self.mw.generate_tab = GenerateTab(self.mw)
        splash.updater.update_progress("BrowseTab")
        self.mw.browse_tab = BrowseTab(self.mw)
        splash.updater.update_progress("LearnTab")
        self.mw.learn_tab = LearnTab(self.mw)
        splash.updater.update_progress("WriteTab")
        self.mw.write_tab = WriteTab(self.mw)
        splash.updater.update_progress("Finalizing")

        self.mw.pictograph_collector = PictographCollector(self.mw)
        self.mw.settings_dialog = SettingsDialog(self.mw)
        self.mw.background_widget = MainBackgroundWidget(self.mw)
        self.mw.background_widget.lower()

        filter_selector = self.mw.browse_tab.sequence_picker.filter_stack
        construct_tab = self.mw.construct_tab

        self.mw.left_stack.addWidget(self.mw.sequence_workbench)  # 0
        self.mw.left_stack.addWidget(self.mw.learn_tab.codex)  # 1
        self.mw.left_stack.addWidget(self.mw.write_tab.act_sheet)  # 2
        self.mw.left_stack.addWidget(filter_selector)  # 3
        self.mw.left_stack.addWidget(self.mw.browse_tab.sequence_picker)  # 4

        self.mw.right_stack.addWidget(construct_tab.start_pos_picker)  # 0
        self.mw.right_stack.addWidget(construct_tab.advanced_start_pos_picker)  # 1
        self.mw.right_stack.addWidget(construct_tab.option_picker)  # 2
        self.mw.right_stack.addWidget(self.mw.generate_tab)  # 3
        self.mw.right_stack.addWidget(self.mw.learn_tab)  # 4
        self.mw.right_stack.addWidget(self.mw.write_tab)  # 5
        self.mw.right_stack.addWidget(self.mw.browse_tab.sequence_viewer)  # 6

    def _setup_layout(self):
        self.mw.main_layout = QVBoxLayout(self.mw)
        self.mw.main_layout.setContentsMargins(0, 0, 0, 0)
        self.mw.main_layout.setSpacing(0)
        self.mw.setLayout(self.mw.main_layout)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.mw.menu_bar.social_media_widget, 1)
        top_layout.addWidget(self.mw.menu_bar.navigation_widget, 16)
        top_layout.addWidget(self.mw.menu_bar.settings_button, 1)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.mw.left_stack, 1)
        content_layout.addWidget(self.mw.right_stack, 1)

        self.mw.main_layout.addLayout(top_layout)
        self.mw.main_layout.addLayout(content_layout)

    def _setup_indices(self):
        self.mw.main_construct_tab_index = 0
        self.mw.main_generate_tab_index = 1
        self.mw.main_browse_tab_index = 2
        self.mw.main_learn_tab_index = 3
        self.mw.main_write_tab_index = 4

    def load_current_tab(self):
        mw = self.mw
        mw.current_tab = mw.settings_manager.global_settings.get_current_tab()
        mw.tab_switcher.update_tab_based_on_settings()
