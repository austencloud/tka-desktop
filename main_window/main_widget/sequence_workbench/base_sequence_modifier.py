from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

from main_window.settings_manager.global_settings.app_context import AppContext

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
        self.sequence_workbench.main_widget.construct_tab.option_picker.option_updater.refresh_options()
        self.sequence_workbench.graph_editor.update_graph_editor()
        self.sequence_workbench.indicator_label.show_message(self.success_message)

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
