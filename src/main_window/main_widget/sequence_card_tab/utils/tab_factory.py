from typing import TYPE_CHECKING

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.sequence_card_tab.tab import SequenceCardTab

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceCardTabFactory:
    """Factory for creating SequenceCardTab instances with proper dependencies."""

    @staticmethod
    def create(
        main_widget: "MainWidget",
        settings_manager: ISettingsManager,
        json_manager: IJsonManager,
    ) -> SequenceCardTab:
        """Create a SequenceCardTab with all required dependencies."""
        return SequenceCardTab(
            main_widget=main_widget,
            settings_manager=settings_manager,
            json_manager=json_manager,
        )
