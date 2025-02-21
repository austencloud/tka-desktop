from typing import Callable, List, Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, QSize

from base_widgets.pictograph.pictograph_scene import PictographScene
from main_window.main_widget.construct_tab.add_to_sequence_manager import (
    AddToSequenceManager,
)
from main_window.main_widget.fade_manager.fade_manager import FadeManager
from .choose_your_next_pictograph_label import ChooseYourNextPictographLabel
from .option_scroll.option_scroll import OptionScroll
from .option_factory import OptionFactory
from .option_getter import OptionGetter
from .option_click_handler import OptionClickHandler
from .option_updater import OptionUpdater
from .reversal_filter.option_picker_reversal_filter import OptionPickerReversalFilter
from .option_picker_layout_manager import OptionPickerLayoutManager
from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
    SequenceBeatFrame,
)


class OptionPicker(QWidget):
    option_selected = pyqtSignal(str)
    COLUMN_COUNT = 8

    def __init__(
        self,
        add_to_sequence_manager: "AddToSequenceManager",
        pictograph_dataset: dict,
        beat_frame: "SequenceBeatFrame",
        mw_size_provider: Callable[[], QSize],
        fade_manager: "FadeManager",
    ):
        super().__init__()
        self.add_to_sequence_manager = add_to_sequence_manager
        self.option_pool: List[PictographScene] = []
        self.choose_next_label = ChooseYourNextPictographLabel(mw_size_provider)
        self.option_scroll = OptionScroll(self, mw_size_provider)
        self.option_getter = OptionGetter(pictograph_dataset)
        self.option_click_handler = OptionClickHandler(self, beat_frame)
        self.updater = OptionUpdater(self, fade_manager)
        self.reversal_filter = OptionPickerReversalFilter(
            mw_size_provider, self.updater.update_options
        )
        self.option_factory = OptionFactory(self, mw_size_provider)
        self.layout_manager = OptionPickerLayoutManager(self)
        self.option_pool = self.option_factory.create_options()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for option in self.option_pool:
            option.view.resize_option_view()
