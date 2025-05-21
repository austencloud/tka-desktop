from typing import TYPE_CHECKING

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.browse_tab.browse_tab import BrowseTab

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BrowseTabFactory:
    """Factory for creating BrowseTab instances with proper dependencies."""
    
    @staticmethod
    def create(
        main_widget: "MainWidget",
        settings_manager: ISettingsManager,
        json_manager: IJsonManager
    ) -> BrowseTab:
        """Create a BrowseTab with all required dependencies."""
        return BrowseTab(
            main_widget=main_widget,
            settings_manager=settings_manager,
            json_manager=json_manager
        )
