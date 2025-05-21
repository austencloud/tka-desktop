from typing import TYPE_CHECKING

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.generate_tab.generate_tab import GenerateTab

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class GenerateTabFactory:
    """Factory for creating GenerateTab instances with proper dependencies."""

    @staticmethod
    def create(
        main_widget: "MainWidget",
        settings_manager: ISettingsManager,
        json_manager: IJsonManager,
    ) -> GenerateTab:
        """Create a GenerateTab with all required dependencies."""
        return GenerateTab(
            main_widget=main_widget,
            settings_manager=settings_manager,
            json_manager=json_manager,
        )
