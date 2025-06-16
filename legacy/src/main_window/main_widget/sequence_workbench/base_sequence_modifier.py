from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

from src.legacy_settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class BaseSequenceModifier:
    success_message: str
    error_message: str

    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        self.sequence_workbench = sequence_workbench
        self.json_loader = AppContext.json_manager().loader_saver

    def _update_ui(self):
        """Update all UI components after a modification."""
        self._refresh_construct_tab_options()
        self.sequence_workbench.graph_editor.update_graph_editor()
        self.sequence_workbench.indicator_label.show_message(self.success_message)

    def _refresh_construct_tab_options(self):
        """Refresh construct tab options using the new MVVM architecture with graceful fallbacks."""
        try:
            # Try to get construct tab through the new coordinator pattern
            construct_tab = self.sequence_workbench.main_widget.get_tab_widget(
                "construct"
            )
            if (
                construct_tab
                and hasattr(construct_tab, "option_picker")
                and hasattr(construct_tab.option_picker, "updater")
            ):
                construct_tab.option_picker.updater.refresh_options()
                return
        except AttributeError:
            pass

        try:
            # Fallback: try through tab_manager for backward compatibility
            construct_tab = (
                self.sequence_workbench.main_widget.tab_manager.get_tab_widget(
                    "construct"
                )
            )
            if (
                construct_tab
                and hasattr(construct_tab, "option_picker")
                and hasattr(construct_tab.option_picker, "updater")
            ):
                construct_tab.option_picker.updater.refresh_options()
                return
        except AttributeError:
            pass

        try:
            # Final fallback: try direct access for legacy compatibility
            if hasattr(self.sequence_workbench.main_widget, "construct_tab"):
                construct_tab = self.sequence_workbench.main_widget.construct_tab
                if hasattr(construct_tab, "option_picker") and hasattr(
                    construct_tab.option_picker, "updater"
                ):
                    construct_tab.option_picker.updater.refresh_options()
                    return
        except AttributeError:
            pass

        # If all else fails, log a warning but don't crash
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(
            "Could not refresh construct tab options - construct tab not available"
        )

    def _check_length(self):
        """Check if the sequence is long enough to modify."""
        current_sequence = (
            AppContext.json_manager().loader_saver.load_current_sequence()
        )

        if len(current_sequence) < 2:
            self.sequence_workbench.indicator_label.show_message(self.error_message)
            QApplication.restoreOverrideCursor()
            return False
        return True
