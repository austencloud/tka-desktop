from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget

from typing import TYPE_CHECKING
from Enums.PropTypes import PropType

from main_window.main_widget.generate_tab.generate_tab import GenerateTab
from main_window.main_widget.pictograph_collector import PictographCollector
from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog
from main_window.main_widget.startup_dialog import StartupDialog
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
from .main_widget_events import MainWidgetEvents
from .main_widget_state import MainWidgetState

if TYPE_CHECKING:
    from main_window.main_widget.pictograph_data_loader import PictographDataLoader
    from main_window.settings_manager.settings_manager import SettingsManager
    from main_window.menu_bar.menu_bar import MenuBarWidget
    from splash_screen.splash_screen import SplashScreen
    from ..main_window import MainWindow

    from .json_manager.json_manager import JsonManager
    from .sequence_workbench.sequence_workbench import SequenceWorkbench

    from base_widgets.base_pictograph.svg_manager import (
        SvgManager,
    )
    from .main_background_widget.backgrounds.base_background import (
        BaseBackground,
    )
    from .turns_tuple_generator.turns_tuple_generator import TurnsTupleGenerator
    from .pictograph_key_generator import PictographKeyGenerator
    from .special_placement_loader import SpecialPlacementLoader
    from .metadata_extractor import MetaDataExtractor
    from .sequence_level_evaluator import SequenceLevelEvaluator
    from .sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )
    from .thumbnail_finder import ThumbnailFinder
    from .grid_mode_checker import GridModeChecker
    from base_widgets.base_pictograph.pictograph import Pictograph
    from Enums.Enums import Letter
    from letter_determiner.letter_determiner import LetterDeterminer


class MainWidget(QWidget):
    main_window: "MainWindow"
    settings_manager: "SettingsManager"
    splash: "SplashScreen"
    settings_dialog: "SettingsDialog"

    # Tabs
    construct_tab: "ConstructTab"
    generate_tab: "GenerateTab"
    browse_tab: "BrowseTab"
    learn_tab: "LearnTab"
    write_tab: "WriteTab"

    # Widgets
    sequence_workbench: "SequenceWorkbench"
    background_widget: "MainBackgroundWidget"
    full_screen_overlay: "FullScreenImageOverlay"

    # Handlers
    tab_switcher: "MainWidgetTabSwitcher"
    manager: "MainWidgetManagers"
    ui_handler: "MainWidgetUI"
    event_handler: "MainWidgetEvents"
    state_handler: "MainWidgetState"

    # Managers and Helpers
    svg_manager: "SvgManager"
    turns_tuple_generator: "TurnsTupleGenerator"
    pictograph_key_generator: "PictographKeyGenerator"
    special_placement_loader: "SpecialPlacementLoader"
    metadata_extractor: "MetaDataExtractor"
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

    # Indices for tabs
    main_construct_tab_index: int = 0
    main_generate_tab_index: int = 1
    main_browse_tab_index: int = 2
    main_learn_tab_index: int = 3
    main_write_tab_index: int = 4

    # Left Indices
    left_sequence_picker_index: int = 4

    # Right Indices
    right_start_pos_picker_index: int = 0
    right_advanced_start_pos_picker_index: int = 1
    right_option_picker_index: int = 2
    right_generate_tab_index: int = 3
    right_learn_tab_index: int = 4
    right_write_tab_index: int = 5
    right_sequence_viewer_index: int = 6

    # Current state
    current_tab: str
    background: "BaseBackground"
    json_manager: "JsonManager"

    # Other attributes
    pictograph_cache: dict[str, dict[str, "Pictograph"]]
    prop_type: PropType
    pictograph_data_loader: "PictographDataLoader"
    pictograph_dataset: dict["Letter", list[dict]]
    letter_determiner: "LetterDeterminer"
    special_placements: dict[str, dict[str, dict[str, dict[str, list[int]]]]]

    def __init__(self, main_window: "MainWindow", splash_screen: "SplashScreen" = None):
        super().__init__(main_window)
        self.main_window = main_window
        self.main_window.main_widget = self
        self.settings_manager = main_window.settings_manager
        self.splash = splash_screen

        self.tab_switcher = MainWidgetTabSwitcher(self)
        self.manager = MainWidgetManagers(self)
        self.state_handler = MainWidgetState(self)
        self.ui_handler = MainWidgetUI(self)
        self.event_handler = MainWidgetEvents(self)

        # QTimer.singleShot(0, self.ui_handler.load_current_tab)
        # QTimer.singleShot(10, self.ensure_user_exists)

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
        self.beat_frame = self.sequence_workbench.beat_frame
        if self.left_stack.currentIndex() == self.left_sequence_picker_index and self.right_stack.currentIndex() == self.right_sequence_viewer_index:
            total_width = self.width()
            left_width = int(total_width * (2 / 3))
            right_width = total_width - left_width
            self.left_stack.setFixedWidth(left_width)
            self.right_stack.setFixedWidth(right_width)
        else:
            total_width = self.width()
            half_width = int(total_width / 2)
            self.left_stack.setFixedWidth(half_width)
            self.right_stack.setFixedWidth(half_width)