from typing import Callable, TYPE_CHECKING
from PyQt6.QtCore import QSize

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.fade_manager.fade_manager import FadeManager
from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import SequenceBeatFrame
from .construct_tab import ConstructTab

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class ConstructTabFactory:
    """Factory for creating ConstructTab instances with proper dependencies."""
    
    @staticmethod
    def create(
        main_widget: "MainWidget",
        settings_manager: ISettingsManager,
        json_manager: IJsonManager
    ) -> ConstructTab:
        """Create a ConstructTab with all required dependencies."""
        return ConstructTab(
            beat_frame=main_widget.sequence_workbench.beat_frame,
            pictograph_dataset=main_widget.pictograph_dataset,
            size_provider=lambda: main_widget.size(),
            fade_to_stack_index=lambda index: main_widget.fade_manager.stack_fader.fade_stack(
                main_widget.right_stack, index
            ),
            fade_manager=main_widget.fade_manager,
            settings_manager=settings_manager,
            json_manager=json_manager,
        )
