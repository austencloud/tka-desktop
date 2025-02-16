from typing import TYPE_CHECKING, Callable
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from main_window.main_widget.construct_tab.option_picker.option_view import OptionView
from .option_scroll.option_scroll import OptionScroll
from .option_factory import OptionFactory
from .option_picker_layout_manager import OptionPickerLayoutManager
from .option_updater import OptionUpdater
from .option_click_handler import OptionClickHandler
from .reversal_filter.option_picker_reversal_filter import OptionPickerReversalFilter
from .option_getter import OptionGetter
from .choose_your_next_pictograph_label import ChooseYourNextPictographLabel
from base_widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from ..construct_tab import ConstructTab


class OptionPicker(QWidget):
    COLUMN_COUNT = 8
    option_selected = pyqtSignal(str)
    layout: QVBoxLayout
    option_pool: list["Pictograph"]

    def __init__(
        self,
        construct_tab: "ConstructTab",
        pictograph_dataset: dict,
        ori_calculator,
        ori_validation_engine,
        beat_frame,
        mw_height_provider: Callable[[], int],
    ):
        super().__init__(construct_tab)
        self.construct_tab = construct_tab
        self.mw_height_provider = mw_height_provider

        # Components
        self.choose_next_label = ChooseYourNextPictographLabel(self.mw_height_provider)
        self.reversal_filter = OptionPickerReversalFilter(self)
        self.option_scroll = OptionScroll(self)

        # Managers
        self.option_getter = OptionGetter(
            pictograph_dataset, ori_calculator, ori_validation_engine
        )
        self.click_handler = OptionClickHandler(self, beat_frame)
        self.updater = OptionUpdater(self)
        self.option_factory = OptionFactory(self)
        self.layout_manager = OptionPickerLayoutManager(self)

    def resizeEvent(self, event):
        for option in self.option_pool:
            option.view.resize_option_view()
