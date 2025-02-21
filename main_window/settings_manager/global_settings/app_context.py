from typing import TYPE_CHECKING

from main_window.main_widget.special_placement_loader import SpecialPlacementLoader


if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JsonManager
    from main_window.main_widget.json_manager.json_special_placement_handler import (
        JsonSpecialPlacementHandler,
    )
    from main_window.settings_manager.settings_manager import SettingsManager


class AppContext:
    _settings_manager = None
    _json_manager = None
    _special_placement_handler = None
    _special_placement_loader = None
    _sequence_beat_frame = None  # 👈 Initially None

    @classmethod
    def init(
        cls,
        settings_manager,
        json_manager,
        special_placement_handler,
        special_placement_loader,
    ):
        cls._settings_manager = settings_manager
        cls._json_manager = json_manager
        cls._special_placement_handler = special_placement_handler
        cls._special_placement_loader = special_placement_loader

    @classmethod
    def set_sequence_beat_frame(cls, sequence_beat_frame):
        """Set the sequence beat frame after initialization."""
        cls._sequence_beat_frame = sequence_beat_frame

    @classmethod
    def sequence_beat_frame(cls):
        """Retrieve sequence_beat_frame only if it's set."""
        if cls._sequence_beat_frame is None:
            raise RuntimeError(
                "AppContext.sequence_beat_frame() accessed before being set. Ensure it is initialized in MainWindow."
            )
        return cls._sequence_beat_frame

    @classmethod
    def settings_manager(cls) -> "SettingsManager":
        if cls._settings_manager is None:
            raise RuntimeError("AppContext.settings_manager() accessed before init()")
        return cls._settings_manager

    @classmethod
    def json_manager(cls) -> "JsonManager":
        if cls._json_manager is None:
            raise RuntimeError("AppContext.json_manager() accessed before init()")
        return cls._json_manager

    @classmethod
    def special_placement_handler(cls) -> "JsonSpecialPlacementHandler":
        if cls._special_placement_handler is None:
            raise RuntimeError(
                "AppContext.special_placement_handler() accessed before init()"
            )
        return cls._special_placement_handler

    @classmethod
    def special_placement_loader(cls) -> SpecialPlacementLoader:
        if cls._special_placement_loader is None:
            cls._special_placement_loader = SpecialPlacementLoader()
        return cls._special_placement_loader
