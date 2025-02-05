from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_getter import (
        OptionGetter,
    )


class PictographWorker(QObject):
    pictographs_ready = pyqtSignal(list)  # Emit prepared pictographs

    def __init__(self, option_getter: "OptionGetter", sequence, selected_filter):
        super().__init__()
        self.option_getter = option_getter
        self.sequence = sequence
        self.selected_filter = selected_filter

    def run(self):
        # Prepare the next options asynchronously
        next_options = self.option_getter.get_next_options(
            self.sequence, self.selected_filter
        )
        self.pictographs_ready.emit(next_options)
