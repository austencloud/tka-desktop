from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from main_window.main_widget.browse_tab.sequence_picker.filter_stack.sequence_picker_filter_stack import (
    BrowseTabSection,
)
from main_window.main_widget.tab_index import TAB_INDEX
from main_window.main_widget.tab_indices import LeftStackIndex, RightStackIndex
from main_window.main_widget.tab_name import TabName

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from core.application_context import ApplicationContext


class MainWidgetTabSwitcher:
    def __init__(
        self, main_widget: "MainWidget", app_context: "ApplicationContext" = None
    ):
        self.mw = main_widget
        self.app_context = app_context or getattr(main_widget, "app_context", None)

        self.tab_to_right_stack = {
            TAB_INDEX[TabName.GENERATE]: RightStackIndex.GENERATE_TAB,
            TAB_INDEX[TabName.LEARN]: RightStackIndex.LEARN_TAB,
            TAB_INDEX[TabName.SEQUENCE_CARD]: RightStackIndex.SEQUENCE_CARD_TAB,
        }

        self.tab_to_left_stack = {
            TAB_INDEX[TabName.LEARN]: LeftStackIndex.LEARN_CODEX,
            TAB_INDEX[TabName.GENERATE]: LeftStackIndex.WORKBENCH,
            TAB_INDEX[TabName.CONSTRUCT]: LeftStackIndex.WORKBENCH,
            TAB_INDEX[TabName.SEQUENCE_CARD]: LeftStackIndex.WORKBENCH,
        }

        self.index_to_tab_name = {v: k for k, v in TAB_INDEX.items()}

    def on_tab_changed(self, new_tab: TabName):
        print(
            f"DEBUG: MainWidgetTabSwitcher.on_tab_changed called with new_tab={new_tab}"
        )
        print(f"DEBUG: TAB_INDEX={TAB_INDEX}")

        index = TAB_INDEX[new_tab]
        print(f"DEBUG: index={index}")

        left_new_index, right_new_index = self.get_stack_indices_for_tab(new_tab)
        print(
            f"DEBUG: left_new_index={left_new_index}, right_new_index={right_new_index}"
        )

        # This line might be causing the issue - it's overriding the new_tab parameter
        original_new_tab = new_tab
        new_tab = self.index_to_tab_name.get(index, TabName.CONSTRUCT)
        print(
            f"DEBUG: original_new_tab={original_new_tab}, overridden new_tab={new_tab}"
        )

        current_tab_str = self._get_current_tab()
        print(f"DEBUG: current_tab_str={current_tab_str}")

        self._set_current_tab(new_tab.value)
        print(f"DEBUG: Set current tab to {new_tab.value}")

        # Set width ratio based on tab type using stretch factors
        if new_tab == TabName.BROWSE:
            width_ratio = (2, 1)  # Browse tab uses 2:1 ratio (2/3 left, 1/3 right)
        elif new_tab == TabName.SEQUENCE_CARD:
            width_ratio = (0, 1)  # Sequence card tab uses full width for right panel
        else:
            width_ratio = (1, 1)  # Default is equal split

        if (current_tab_str == "construct" and new_tab == TabName.GENERATE) or (
            current_tab_str == "generate" and new_tab == TabName.CONSTRUCT
        ):
            self.mw.fade_manager.stack_fader.fade_stack(
                self.mw.right_stack,
                right_new_index,
            )
        else:
            self.mw.fade_manager.parallel_stack_fader.fade_both_stacks(
                self.mw.right_stack,
                right_new_index,
                self.mw.left_stack,
                left_new_index,
                width_ratio,
            )
        QApplication.processEvents()
        if new_tab == TabName.BROWSE:
            # Get browse tab using the new dependency injection pattern
            browse_tab = self._get_browse_tab()
            if browse_tab and hasattr(browse_tab, "sequence_viewer"):
                sequence_viewer = browse_tab.sequence_viewer
                if hasattr(sequence_viewer, "thumbnail_box") and hasattr(
                    sequence_viewer.thumbnail_box, "image_label"
                ):
                    sequence_viewer.thumbnail_box.image_label._resize_pixmap_to_fit()
            if browse_tab and hasattr(browse_tab, "ui_updater"):
                browse_tab.ui_updater.resize_thumbnails_top_to_bottom()
        elif new_tab == TabName.SEQUENCE_CARD:
            # Initialize the sequence card tab if needed using dependency injection
            sequence_card_tab = self._get_sequence_card_tab()
            if sequence_card_tab and hasattr(sequence_card_tab, "initialized"):
                if not sequence_card_tab.initialized:
                    sequence_card_tab.initialized = True
                    if hasattr(sequence_card_tab, "refresher"):
                        sequence_card_tab.refresher.refresh_sequence_cards()

    def set_stacks_silently(self, left_index, right_index):
        tab_name_str = self._get_current_tab()

        # Set width ratio based on tab type using stretch factors instead of fixed widths
        if tab_name_str == "browse":
            stretch_ratio = (2, 1)  # Browse tab uses 2:1 ratio (2/3 left, 1/3 right)
        elif tab_name_str == "sequence_card":
            stretch_ratio = (0, 1)  # Sequence card tab uses full width for right panel
        else:
            stretch_ratio = (1, 1)  # Default is equal split

        # Apply stretch factors to maintain proper aspect ratio
        if hasattr(self.mw, "content_layout"):
            self.mw.content_layout.setStretch(0, stretch_ratio[0])
            self.mw.content_layout.setStretch(1, stretch_ratio[1])

            # Clear any fixed width constraints that might interfere
            self.mw.left_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
            self.mw.right_stack.setMaximumWidth(16777215)
            self.mw.left_stack.setMinimumWidth(0)
            self.mw.right_stack.setMinimumWidth(0)

        # Handle both enum values and integers
        left_idx = left_index.value if hasattr(left_index, "value") else left_index
        right_idx = right_index.value if hasattr(right_index, "value") else right_index

        self.mw.left_stack.setCurrentIndex(left_idx)
        self.mw.right_stack.setCurrentIndex(right_idx)

    def get_stack_indices_for_tab(
        self, tab_name: TabName
    ) -> tuple[LeftStackIndex, RightStackIndex]:
        index = TAB_INDEX[tab_name]
        left_index = self.tab_to_left_stack.get(index, LeftStackIndex.WORKBENCH)
        if tab_name == TabName.CONSTRUCT:
            current_sequence = self.mw.json_manager.loader_saver.load_current_sequence()
            right_index = (
                RightStackIndex.OPTION_PICKER
                if len(current_sequence) > 1
                else RightStackIndex.START_POS_PICKER
            )
        elif tab_name == TabName.BROWSE:
            current_section_str = (
                self.mw.browse_tab.browse_settings.get_current_section()
            )

            filter_section_strs = [section.value for section in BrowseTabSection]
            if current_section_str in filter_section_strs:
                if current_section_str == BrowseTabSection.FILTER_SELECTOR.value:
                    left_index = LeftStackIndex.FILTER_SELECTOR
                else:
                    left_index = LeftStackIndex.SEQUENCE_PICKER
            right_index = RightStackIndex.SEQUENCE_VIEWER
        elif tab_name == TabName.SEQUENCE_CARD:
            # For Sequence Card Tab, we use the sequence card tab on both left and right panels
            # This gives us a full-screen experience for the sequence cards
            left_index = LeftStackIndex.WORKBENCH  # We'll hide this panel
            right_index = RightStackIndex.SEQUENCE_CARD_TAB
        else:
            right_index = self.tab_to_right_stack.get(index, index)

        return left_index, right_index

    def _get_current_tab(self) -> str:
        """Get current tab through dependency injection or fallback to legacy."""
        try:
            if self.app_context and hasattr(self.app_context, "settings_manager"):
                return (
                    self.app_context.settings_manager.global_settings.get_current_tab()
                )
        except (AttributeError, RuntimeError):
            pass

        # Fallback to legacy AppContext for backward compatibility
        try:
            from src.settings_manager.global_settings.app_context import AppContext

            return AppContext.settings_manager().global_settings.get_current_tab()
        except (AttributeError, RuntimeError):
            # If all else fails, default to construct tab
            return "construct"

    def _set_current_tab(self, tab_name: str) -> None:
        """Set current tab through dependency injection or fallback to legacy."""
        try:
            if self.app_context and hasattr(self.app_context, "settings_manager"):
                self.app_context.settings_manager.global_settings.set_current_tab(
                    tab_name
                )
                return
        except (AttributeError, RuntimeError):
            pass

        # Fallback to legacy AppContext for backward compatibility
        try:
            from src.settings_manager.global_settings.app_context import AppContext

            AppContext.settings_manager().global_settings.set_current_tab(tab_name)
        except (AttributeError, RuntimeError):
            # If all else fails, silently ignore
            pass

    def _get_browse_tab(self):
        """Get the browse tab using the new dependency injection pattern with graceful fallbacks."""
        try:
            # Try to get browse tab through the new coordinator pattern
            return self.mw.get_tab_widget("browse")
        except AttributeError:
            # Fallback: try through tab_manager for backward compatibility
            try:
                return self.mw.tab_manager.get_tab_widget("browse")
            except AttributeError:
                # Final fallback: try direct access for legacy compatibility
                try:
                    if hasattr(self.mw, "browse_tab"):
                        return self.mw.browse_tab
                except AttributeError:
                    pass
        return None

    def _get_sequence_card_tab(self):
        """Get the sequence card tab using the new dependency injection pattern with graceful fallbacks."""
        try:
            # Try to get sequence card tab through the new coordinator pattern
            return self.mw.get_tab_widget("sequence_card")
        except AttributeError:
            # Fallback: try through tab_manager for backward compatibility
            try:
                return self.mw.tab_manager.get_tab_widget("sequence_card")
            except AttributeError:
                # Final fallback: try direct access for legacy compatibility
                try:
                    if hasattr(self.mw, "sequence_card_tab"):
                        return self.mw.sequence_card_tab
                except AttributeError:
                    pass
        return None
