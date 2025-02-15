from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
)

from main_window.main_widget.fade_manager.fade_manager import FadeManager
from main_window.main_widget.pictograph_collector import PictographCollector
from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog
from main_window.main_widget.tab_index import TAB_INDEX
from main_window.main_widget.tab_name import TabName
from .construct_tab.construct_tab import ConstructTab
from .generate_tab.generate_tab import GenerateTab
from .write_tab.write_tab import WriteTab
from .browse_tab.browse_tab import BrowseTab
from .learn_tab.learn_tab import LearnTab
from .main_background_widget.main_background_widget import MainBackgroundWidget
from .font_color_updater.font_color_updater import FontColorUpdater
from ..menu_bar.menu_bar import MenuBarWidget
from .sequence_workbench.sequence_workbench import SequenceWorkbench

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetUI:
    def __init__(self, main_widget: "MainWidget"):
        self.mw = main_widget
        self.splash_screen = main_widget.splash
        self._create_components()
        self._populate_stacks()
        self._initialize_layout()
        self._set_initial_stack_indices()

    def _set_initial_stack_indices(self):
        mw = self.mw
        current_tab_name = TabName.from_string(
            mw.settings_manager.global_settings.get_current_tab()
        )

        tab_index = TAB_INDEX[current_tab_name]
        left_index, right_index = mw.tab_switcher.get_stack_indices_for_tab(tab_index)

        mw.tab_switcher.set_stacks_silently(left_index, right_index)

        mw.menu_bar.navigation_widget.set_active_tab(tab_index)
        mw.tab_switcher.set_current_tab(current_tab_name)

    def _create_components(self):
        mw = self.mw

        mw.left_stack = QStackedWidget()
        mw.right_stack = QStackedWidget()

        mw.fade_manager = FadeManager(mw)
        mw.font_color_updater = FontColorUpdater(mw)
        mw.pictograph_collector = PictographCollector(mw)

        mw.menu_bar = MenuBarWidget(mw)
        mw.sequence_workbench = SequenceWorkbench(mw)
        mw.construct_tab = ConstructTab(mw)
        mw.generate_tab = GenerateTab(mw)
        mw.browse_tab = BrowseTab(mw)
        mw.learn_tab = LearnTab(mw)
        mw.write_tab = WriteTab(mw)

        mw.settings_dialog = SettingsDialog(mw)
        mw.background_widget = MainBackgroundWidget(mw)
        mw.background_widget.lower()
        mw.state_handler.load_state(mw.sequence_workbench.beat_frame)
        self.splash_screen.updater.update_progress("Finalizing")

    def _populate_stacks(self):
        mw = self.mw

        mw.left_stack.addWidget(mw.sequence_workbench)  # 0
        mw.left_stack.addWidget(mw.learn_tab.codex)  # 1
        mw.left_stack.addWidget(mw.write_tab.act_sheet)  # 2
        mw.left_stack.addWidget(mw.browse_tab.sequence_picker.filter_stack)  # 3
        mw.left_stack.addWidget(mw.browse_tab.sequence_picker)  # 4

        mw.right_stack.addWidget(mw.construct_tab.start_pos_picker)  # 0
        mw.right_stack.addWidget(mw.construct_tab.advanced_start_pos_picker)  # 1
        mw.right_stack.addWidget(mw.construct_tab.option_picker)  # 2
        mw.right_stack.addWidget(mw.generate_tab)  # 3
        mw.right_stack.addWidget(mw.learn_tab)  # 4
        mw.right_stack.addWidget(mw.write_tab)  # 5
        mw.right_stack.addWidget(mw.browse_tab.sequence_viewer)  # 6

    def _initialize_layout(self):
        mw = self.mw

        mw.main_layout = QVBoxLayout(mw)
        mw.main_layout.setContentsMargins(0, 0, 0, 0)
        mw.main_layout.setSpacing(0)
        mw.setLayout(mw.main_layout)

        top_layout = QHBoxLayout()
        top_layout.addWidget(mw.menu_bar.social_media_widget, 1)
        top_layout.addWidget(mw.menu_bar.navigation_widget, 16)
        top_layout.addWidget(mw.menu_bar.settings_button, 1)

        content_layout = QHBoxLayout()
        content_layout.addWidget(mw.left_stack, 1)
        content_layout.addWidget(mw.right_stack, 1)

        mw.main_layout.addLayout(top_layout)
        mw.main_layout.addLayout(content_layout)
