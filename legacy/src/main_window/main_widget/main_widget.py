from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget

from typing import TYPE_CHECKING
from enums.letter.letter import Letter
from enums.prop_type import PropType

from main_window.main_widget.pictograph_collector import PictographCollector
from legacy.src.main_window.main_widget.settings_dialog.legacy_settings_dialog import (
    LegacySettingsDialog,
)
from main_window.main_widget.startup_dialog import StartupDialog
from main_window.main_widget.tab_index import TAB_INDEX
from main_window.main_widget.tab_name import TabName
from main_window.main_widget.sequence_card_tab.tab import SequenceCardTab
from .browse_tab.browse_tab import BrowseTab
from .fade_manager.fade_manager import FadeManager
from .full_screen_image_overlay import FullScreenImageOverlay
from .construct_tab.construct_tab import ConstructTab
from .learn_tab.learn_tab import LearnTab
from .write_tab.write_tab import WriteTab
from .main_background_widget.main_background_widget import MainBackgroundWidget
from .main_widget_tab_switcher import MainWidgetTabSwitcher
from .font_color_updater.font_color_updater import FontColorUpdater


from .main_widget_managers import MainWidgetManagers
from .main_widget_ui import MainWidgetUI
from .main_widget_state import MainWidgetState

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab
    from main_window.main_widget.codex.codex import Codex
    from main_window.main_widget.pictograph_data_loader import PictographDataLoader
    from main_window.menu_bar.menu_bar import MenuBarWidget
    from splash_screen.splash_screen import SplashScreen
    from ..main_window import MainWindow

    from .json_manager.json_manager import JsonManager
    from .sequence_workbench.sequence_workbench import SequenceWorkbench

    from .main_background_widget.backgrounds.base_background import (
        BaseBackground,
    )
    from .sequence_level_evaluator import SequenceLevelEvaluator
    from .sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )
    from .thumbnail_finder import ThumbnailFinder
    from .grid_mode_checker import GridModeChecker
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from letter_determination.core import LetterDeterminer


class MainWidget(QWidget):
    main_window: "MainWindow"
    # settings_manager: "SettingsManager"
    splash: "SplashScreen"
    settings_dialog: "LegacySettingsDialog"

    # Tabs
    construct_tab: "ConstructTab"
    generate_tab: "GenerateTab"
    browse_tab: "BrowseTab"
    learn_tab: "LearnTab"
    write_tab: "WriteTab"
    sequence_card_tab: "SequenceCardTab"

    # Widgets
    sequence_workbench: "SequenceWorkbench"
    background_widget: "MainBackgroundWidget"
    full_screen_overlay: "FullScreenImageOverlay"
    codex: "Codex"

    # Handlers
    tab_switcher: "MainWidgetTabSwitcher"
    manager: "MainWidgetManagers"
    ui: "MainWidgetUI"
    state_handler: "MainWidgetState"

    # Managers and Helpers
    sequence_level_evaluator: "SequenceLevelEvaluator"
    sequence_properties_manager: "SequencePropertiesManager"
    thumbnail_finder: "ThumbnailFinder"
    grid_mode_checker: "GridModeChecker"
    fade_manager: FadeManager
    font_color_updater: "FontColorUpdater"
    pictograph_collector: "PictographCollector"

    # Layouts and Widgets
    top_layout: QHBoxLayout
    main_layout: QVBoxLayout
    menu_bar: "MenuBarWidget"
    left_stack: QStackedWidget
    right_stack: QStackedWidget

    # Current state
    current_tab: str
    background: "BaseBackground"
    json_manager: "JsonManager"

    # Other attributes
    pictograph_cache: dict[str, dict[str, "LegacyPictograph"]]
    prop_type: PropType
    pictograph_data_loader: "PictographDataLoader"
    pictograph_dataset: dict["Letter", list[dict]]
    letter_determiner: "LetterDeterminer"
    special_placements: dict[str, dict[str, dict[str, dict[str, list[int]]]]]

    def __init__(self, main_window: "MainWindow", splash_screen: "SplashScreen" = None):
        super().__init__(main_window)
        self.main_window = main_window
        self.main_window.main_widget = self
        self.splash = splash_screen

        # Get dependencies from AppContext safely
        try:
            # Use a consistent import path - always use the src-prefixed version
            from src.legacy_settings_manager.global_settings.app_context import (
                AppContext,
            )
            from src.utils.logging_config import get_logger

            logger = get_logger(__name__)
            logger.info("MainWidget: Accessing AppContext...")

            # Check if AppContext is initialized
            if AppContext._settings_manager is None:
                logger.error(
                    "AppContext._settings_manager is None in MainWidget.__init__"
                )
                raise RuntimeError(
                    "AppContext not initialized before MainWidget creation"
                )

            self.settings_manager = AppContext.settings_manager()
            self.json_manager = AppContext.json_manager()
            logger.info(
                "MainWidget: Successfully retrieved dependencies from AppContext"
            )
        except Exception as e:
            from src.utils.logging_config import get_logger

            logger = get_logger(__name__)
            logger.error(f"MainWidget: Failed to access AppContext: {e}")
            raise

        # Get app_context for dependency injection
        app_context = getattr(self, "app_context", None)
        self.tab_switcher = MainWidgetTabSwitcher(self, app_context)
        self.manager = MainWidgetManagers(self, app_context)
        self.state_handler = MainWidgetState(self)
        self.ui = MainWidgetUI(self)
        self._already_initialized_once = False

    def ensure_user_exists(self):
        """Check if a user exists; if not, prompt for a name and show welcome info."""
        show_welcome = self.settings_manager.global_settings.get_show_welcome_screen()
        current_user = self.settings_manager.users.get_current_user()

        if show_welcome or not current_user:
            dialog = StartupDialog(self.settings_manager, self)
            if dialog.exec():
                user_name = dialog.get_name()
                self.settings_manager.users.set_current_user(user_name)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.background_widget.resize_background()
        self.right_stack.resizeEvent(event)
        self.left_stack.resizeEvent(event)
        # self.construct_tab.option_picker.setFixedWidth(
        #     int(self.main_window.width() * 0.5)
        # )

    def showEvent(self, event):
        super().showEvent(event)
        if not self._already_initialized_once:
            self._already_initialized_once = True

            tab_name = TabName.from_string(
                self.settings_manager.global_settings.get_current_tab()
            )
            tab_index = TAB_INDEX[tab_name]
            left_index, right_index = self.tab_switcher.get_stack_indices_for_tab(
                tab_name
            )

            self.tab_switcher.set_stacks_silently(left_index, right_index)

            self.menu_bar.navigation_widget.current_index = tab_index
            self.menu_bar.navigation_widget.update_buttons()
