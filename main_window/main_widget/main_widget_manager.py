import json
from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from letter_determiner.letter_determiner import LetterDeterminer
from main_window.main_widget.pictograph_data_loader import PictographDataLoader
from utilities.path_helpers import get_images_and_data_path

from .grid_mode_checker import GridModeChecker
from .sequence_properties_manager.sequence_properties_manager import (
    SequencePropertiesManager,
)
from .sequence_level_evaluator import SequenceLevelEvaluator
from .thumbnail_finder import ThumbnailFinder
from .metadata_extractor import MetaDataExtractor
from .json_manager.json_manager import JsonManager
from .turns_tuple_generator.turns_tuple_generator import TurnsTupleGenerator
from .pictograph_key_generator import PictographKeyGenerator
from .special_placement_loader import SpecialPlacementLoader
from objects.graphical_object.svg_manager.graphical_object_svg_manager import SvgManager

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetManager:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.splash_screen = main_widget.splash
        self.settings_manager = main_widget.settings_manager
        self._setup_pictograph_cache()
        self._set_prop_type()
        self._initialize_managers()
        self._setup_letters()

    def _initialize_managers(self):
        """Setup all the managers and helper components."""
        mw = self.main_widget

        mw.json_manager = JsonManager(mw)
        mw.svg_manager = SvgManager(mw)
        mw.turns_tuple_generator = TurnsTupleGenerator()
        mw.pictograph_key_generator = PictographKeyGenerator(mw)
        mw.special_placement_loader = SpecialPlacementLoader(mw)
        mw.metadata_extractor = MetaDataExtractor(mw)
        mw.sequence_level_evaluator = SequenceLevelEvaluator()
        mw.thumbnail_finder = ThumbnailFinder(mw)
        mw.grid_mode_checker = GridModeChecker(self)

    def _setup_pictograph_cache(self) -> None:
        from Enums.Enums import Letter

        self.main_widget.pictograph_cache = {}
        for letter in Letter:
            self.main_widget.pictograph_cache[letter] = {}

    def _set_prop_type(self) -> None:
        settings_path = get_images_and_data_path("settings.json")
        with open(settings_path, "r", encoding="utf-8") as file:
            settings: dict[str, dict[str, str | bool]] = json.load(file)
        prop_type_value = settings.get("global", {}).get("prop_type", "staff")
        self.main_widget.prop_type = PropType.get_prop_type(prop_type_value)

    def _setup_letters(self) -> None:
        self.main_widget.pictograph_data_loader = PictographDataLoader(self.main_widget)
        self.main_widget.pictograph_dataset = (
            self.main_widget.pictograph_data_loader.load_all_pictograph_data()
        )
        self.main_widget.letter_determiner = LetterDeterminer(self.main_widget)
