from typing import TYPE_CHECKING

from interfaces.settings_manager_interface import ISettingsManager
from main_window.main_widget.main_background_widget.main_background_widget import MainBackgroundWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainBackgroundWidgetFactory:
    """Factory for creating MainBackgroundWidget instances with proper dependencies."""
    
    @staticmethod
    def create(
        main_widget: "MainWidget",
        settings_manager: ISettingsManager
    ) -> MainBackgroundWidget:
        """Create a MainBackgroundWidget with all required dependencies."""
        return MainBackgroundWidget(
            main_widget=main_widget,
            settings_manager=settings_manager
        )
