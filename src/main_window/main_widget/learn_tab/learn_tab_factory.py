from typing import TYPE_CHECKING

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.learn_tab.learn_tab import LearnTab

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LearnTabFactory:
    """Factory for creating LearnTab instances with proper dependencies."""
    
    @staticmethod
    def create(
        main_widget: "MainWidget",
        settings_manager: ISettingsManager,
        json_manager: IJsonManager
    ) -> LearnTab:
        """Create a LearnTab with all required dependencies."""
        return LearnTab(
            main_widget=main_widget,
            settings_manager=settings_manager,
            json_manager=json_manager
        )
