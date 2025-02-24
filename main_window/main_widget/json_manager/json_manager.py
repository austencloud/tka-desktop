import logging
from typing import TYPE_CHECKING

from main_window.main_widget.json_manager.json_act_saver import JsonActSaver
from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
    JsonSequenceUpdater,
)
from .json_ori_calculator import JsonOriCalculator

from .json_ori_validation_engine import JsonOriValidationEngine
from .json_start_position_handler import JsonStartPositionHandler
from .sequence_data_loader_saver import SequenceDataLoaderSaver

if TYPE_CHECKING:
    pass


class JsonManager:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)


        # current sequence
        self.loader_saver = SequenceDataLoaderSaver()
        self.updater = JsonSequenceUpdater(self)
        self.start_pos_handler = JsonStartPositionHandler(self)
        self.ori_calculator = JsonOriCalculator()
        self.ori_validation_engine = JsonOriValidationEngine(self)
        self.act_saver = JsonActSaver()

    def save_act(self, act_data: dict):
        """Save the act using the JsonActSaver."""
        self.act_saver.save_act(act_data)
