import logging
from typing import TYPE_CHECKING, Dict, Any, List, Optional

from src.interfaces.json_manager_interface import IJsonManager
from src.main_window.main_widget.json_manager.json_act_saver import JsonActSaver
from src.main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
    JsonSequenceUpdater,
)
from .json_ori_calculator import JsonOriCalculator
from .json_ori_validation_engine import JsonOriValidationEngine
from .json_start_position_handler import JsonStartPositionHandler
from .sequence_data_loader_saver import SequenceDataLoaderSaver

if TYPE_CHECKING:
    from core.application_context import ApplicationContext


class JsonManager:  # IJsonManager is a Protocol, no need to inherit
    def __init__(self, app_context: Optional["ApplicationContext"] = None) -> None:
        """
        Initialize JsonManager with optional dependency injection.

        Args:
            app_context: Application context with dependencies. If None, uses legacy approach.
        """
        self.logger = logging.getLogger(__name__)

        # current sequence - pass app_context to break circular dependency
        self.loader_saver = SequenceDataLoaderSaver(app_context)
        self.updater = JsonSequenceUpdater(self)
        self.start_pos_handler = JsonStartPositionHandler(self)
        self.ori_calculator = JsonOriCalculator()
        self.ori_validation_engine = JsonOriValidationEngine(self)
        self.act_saver = JsonActSaver()

    def save_act(self, act_data: dict):
        """Save the act using the JsonActSaver."""
        self.act_saver.save_act(act_data)

    # IJsonManager interface implementation
    def save_sequence(self, sequence_data: List[Dict[str, Any]]) -> bool:
        """Save the current sequence to the default location."""
        return self.loader_saver.save_sequence(sequence_data)

    def load_sequence(self, file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load a sequence from the specified file path or the default location."""
        return self.loader_saver.load_sequence(file_path)

    def get_updater(self):
        """Get the JSON sequence updater."""
        return self.updater
