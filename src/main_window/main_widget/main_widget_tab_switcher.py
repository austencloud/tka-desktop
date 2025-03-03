from typing import TYPE_CHECKING
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from main_window.main_widget.tab_index import TAB_INDEX
from main_window.main_widget.tab_indices import LeftStackIndex, RightStackIndex
from main_window.main_widget.tab_name import TabName
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabSwitcher:
    def __init__(self, main_widget: "MainWidget"):
        self.mw = main_widget

        self.tab_to_right_stack = {
            TAB_INDEX[TabName.BROWSE]: RightStackIndex.SEQUENCE_VIEWER,
            TAB_INDEX[TabName.GENERATE]: RightStackIndex.GENERATE_TAB,
            TAB_INDEX[TabName.LEARN]: RightStackIndex.LEARN_TAB,
        }

        self.tab_to_left_stack = {
            TAB_INDEX[TabName.LEARN]: LeftStackIndex.LEARN_CODEX,
            TAB_INDEX[TabName.BROWSE]: LeftStackIndex.SEQUENCE_PICKER,
            TAB_INDEX[TabName.GENERATE]: LeftStackIndex.WORKBENCH,
            TAB_INDEX[TabName.CONSTRUCT]: LeftStackIndex.WORKBENCH,
        }

        self.index_to_tab_name = {v: k for k, v in TAB_INDEX.items()}

    def on_tab_changed(self, tab_name: TabName):
        """Handle the transition when a tab is changed."""
        index = TAB_INDEX[tab_name]
        left_new_index, right_new_index = self.get_stack_indices_for_tab(tab_name)

        tab_name = self.index_to_tab_name.get(index, TabName.CONSTRUCT)
        AppContext.settings_manager().global_settings.set_current_tab(tab_name.value)

        width_ratio = (2 / 3, 1 / 3) if tab_name == TabName.BROWSE else (1 / 2, 1 / 2)

        self.mw.fade_manager.parallel_stack_fader.fade_both_stacks(
            self.mw.right_stack,
            right_new_index,
            self.mw.left_stack,
            left_new_index,
            width_ratio,
        )
        QApplication.processEvents()
        if tab_name == TabName.BROWSE:
            self.mw.browse_tab.sequence_viewer.image_label.set_pixmap_to_fit()
            self.mw.browse_tab.ui_updater.resize_thumbnails_top_to_bottom()

    def set_stacks_silently(
        self, left_index: LeftStackIndex, right_index: RightStackIndex
    ):
        """
        Set the current indices of left and right stacks without animation,
        and also apply the same 2/3 ratio used by on_tab_changed if it's the browse tab.
        """

        tab_name_str = AppContext.settings_manager().global_settings.get_current_tab()
        width_ratio = (2 / 3, 1 / 3) if tab_name_str == "browse" else (1 / 2, 1 / 2)
        total_width = self.mw.width()
        left_width = int(total_width * width_ratio[0])
        right_width = total_width - left_width  # ensures total == self.mw.width()

        self.mw.left_stack.setFixedWidth(left_width)
        self.mw.right_stack.setFixedWidth(right_width)
        self.mw.left_stack.setCurrentIndex(left_index.value)
        self.mw.right_stack.setCurrentIndex(right_index.value)

    def get_stack_indices_for_tab(
        self, tab_name: TabName
    ) -> tuple[LeftStackIndex, RightStackIndex]:
        """Get the left and right stack indices for the given tab index."""
        index = TAB_INDEX[tab_name]
        left_index = self.tab_to_left_stack.get(index, LeftStackIndex.WORKBENCH)
        if tab_name == TabName.CONSTRUCT:
            current_sequence = self.mw.json_manager.loader_saver.load_current_sequence()
            right_index = (
                RightStackIndex.OPTION_PICKER
                if len(current_sequence) > 1
                else RightStackIndex.START_POS_PICKER
            )
        else:
            right_index = self.tab_to_right_stack.get(index, index)

        return left_index, right_index
