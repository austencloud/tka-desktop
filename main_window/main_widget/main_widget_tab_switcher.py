from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabSwitcher:
    """Handles tab-switch logic, referencing the TabFadeManager for fade animations."""

    def __init__(self, main_widget: "MainWidget"):
        """Initialize MainWidgetTabs."""
        self.mw = main_widget

    def on_tab_changed(self, index: int) -> None:

        left_new_index = {
            self.mw.main_learn_tab_index: 1,
            self.mw.main_write_tab_index: 2,
            self.mw.main_browse_tab_index: 3,
            self.mw.main_generate_tab_index: 0,
            self.mw.main_construct_tab_index: 0,
        }.get(index, None)

        right_new_index = (
            self.mw.right_sequence_viewer_index
            if index == self.mw.main_browse_tab_index
            else index
        )
        right_new_index = (
            self.mw.right_generate_tab_index
            if index == self.mw.main_generate_tab_index
            else right_new_index
        )
        right_new_index = (
            self.mw.right_learn_tab_index
            if index == self.mw.main_learn_tab_index
            else right_new_index
        )
        right_new_index = (
            self.mw.right_write_tab_index
            if index == self.mw.main_write_tab_index
            else right_new_index
        )
        width_ratio = (
            (2 / 3, 1 / 3) if index == self.mw.main_browse_tab_index else (1 / 2, 1 / 2)
        )

        right_construct_tab_index = self.get_construct_tab_index()
        if (
            index in [self.mw.main_generate_tab_index, self.mw.main_construct_tab_index]
            and self.mw.left_stack.currentIndex() == self.mw.left_sequence_widget_index
        ):
            new_index = (
                3
                if index == self.mw.main_generate_tab_index
                else right_construct_tab_index
            )
            self.mw.fade_manager.stack_fader.fade_stack(self.mw.right_stack, new_index)
        elif index in [self.mw.main_construct_tab_index]:
            self.mw.fade_manager.parallel_stack_fader.fade_both_stacks(
                self.mw.right_stack,
                right_construct_tab_index,
                self.mw.left_stack,
                left_new_index,
                width_ratio,
            )
        elif index in [self.mw.main_generate_tab_index]:
            self.mw.fade_manager.parallel_stack_fader.fade_both_stacks(
                self.mw.right_stack,
                self.mw.right_generate_tab_index,
                self.mw.left_stack,
                left_new_index,
                width_ratio,
            )

        else:
            self.mw.fade_manager.parallel_stack_fader.fade_both_stacks(
                right_stack=self.mw.right_stack,
                right_new_index=right_new_index,
                left_stack=self.mw.left_stack,
                left_new_index=left_new_index,
                width_ratio=width_ratio,
            )

    def get_construct_tab_index(self):
        """Return the index of the construct tab."""
        beat_frame = self.mw.sequence_widget.beat_frame
        for beat in beat_frame.beat_views:
            if beat.is_filled:
                return self.mw.right_option_picker_index
        return self.mw.right_start_pos_picker_index

    def update_tab_based_on_settings(self) -> None:
        """Switch to the tab indicated by saved settings."""
        tab_indices = {
            "construct": self.mw.main_construct_tab_index,
            "generate": self.mw.main_generate_tab_index,
            "browse": self.mw.main_browse_tab_index,
            "learn": self.mw.main_learn_tab_index,
            "write": self.mw.main_write_tab_index,
        }
        current_tab_name = self.mw.current_tab
        if current_tab_name in tab_indices:
            idx = tab_indices[current_tab_name]
            self.mw.menu_bar.navigation_widget.on_button_clicked(idx)
            self.on_tab_changed(idx)
