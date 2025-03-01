from typing import TYPE_CHECKING

from main_window.main_widget.tab_index import TAB_INDEX
from main_window.main_widget.tab_indices import LeftStackIndex, RightStackIndex
from main_window.main_widget.tab_name import TabName
from main_window.settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabSwitcher:
    def __init__(self, main_widget: "MainWidget"):
        self.mw = main_widget

        self.tab_to_right_stack = {
            self.mw.main_browse_tab_index: RightStackIndex.SEQUENCE_VIEWER,
            self.mw.main_generate_tab_index: RightStackIndex.GENERATE_TAB,
            self.mw.main_learn_tab_index: RightStackIndex.LEARN_TAB,
            # self.mw.main_write_tab_index: RightStackIndex.WRITE_TAB,
        }

        self.tab_to_left_stack = {
            self.mw.main_learn_tab_index: LeftStackIndex.LEARN_CODEX,
            # self.mw.main_write_tab_index: LeftStackIndex.WRITE_ACT_SHEET,
            self.mw.main_browse_tab_index: LeftStackIndex.SEQUENCE_PICKER,
            self.mw.main_generate_tab_index: LeftStackIndex.WORKBENCH,
            self.mw.main_construct_tab_index: LeftStackIndex.WORKBENCH,
        }

        self.index_to_tab_name = {v: k for k, v in TAB_INDEX.items()}



    def on_tab_changed(self, index: int) -> None:
        """Handle the transition when a tab is changed."""
        left_new_index, right_new_index = self.get_stack_indices_for_tab(index)

        tab_name = self.index_to_tab_name.get(index, TabName.CONSTRUCT)
        AppContext.settings_manager().global_settings.set_current_tab(tab_name.value)

        is_browse_tab = index == self.mw.main_browse_tab_index
        width_ratio = (2 / 3, 1 / 3) if is_browse_tab else (1 / 2, 1 / 2)

        self.mw.fade_manager.parallel_stack_fader.fade_both_stacks(
            self.mw.right_stack,
            right_new_index,
            self.mw.left_stack,
            left_new_index,
            width_ratio,
        )

    def set_stacks_silently(self, left_index: int, right_index: int):
        """Set the current indices of left and right stacks without animation."""
        self.mw.left_stack.setCurrentIndex(left_index)
        self.mw.right_stack.setCurrentIndex(right_index)

    def get_stack_indices_for_tab(self, index: int) -> tuple[int, int]:
        """Get the left and right stack indices for the given tab index."""
        left_index = self.tab_to_left_stack.get(index, LeftStackIndex.WORKBENCH)
        right_index: int
        if index == TAB_INDEX[TabName.CONSTRUCT]:
            current_sequence = self.mw.json_manager.loader_saver.load_current_sequence()
            right_index = (
                RightStackIndex.OPTION_PICKER
                if len(current_sequence) > 1
                else RightStackIndex.START_POS_PICKER
            )
        else:
            right_index = self.tab_to_right_stack.get(index, index)

        return left_index, right_index
