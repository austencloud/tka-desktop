import logging
from typing import TYPE_CHECKING

from main_window.main_widget.json_manager.json_act_saver import JsonActSaver
from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
    JsonSequenceUpdater,
)
from .json_ori_calculator import JsonOriCalculator

from .json_ori_validation_engine import JsonOrientationValidationEngine
from .json_start_position_handler import JsonStartPositionHandler
from .sequence_data_loader_saver import SequenceDataLoaderSaver
from .json_special_placement_handler import JsonSpecialPlacementHandler

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class JsonManager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.logger = logging.getLogger(__name__)

        # special placement
        self.special_placement_handler = JsonSpecialPlacementHandler(self)

        # current sequence
        self.loader_saver = SequenceDataLoaderSaver(self)
        self.updater = JsonSequenceUpdater(self)
        self.start_pos_handler = JsonStartPositionHandler(self)
        self.ori_calculator = JsonOriCalculator(self)
        self.ori_validation_engine = JsonOrientationValidationEngine(self)
        self.act_saver = JsonActSaver(self)

    def save_act(self, act_data: dict):
        """Save the act using the JsonActSaver."""
        self.act_saver.save_act(act_data)
