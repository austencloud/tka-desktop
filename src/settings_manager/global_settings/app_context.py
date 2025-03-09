from typing import TYPE_CHECKING, Optional
from main_window.main_widget.browse_tab.sequence_picker.dictionary_data_manager import (
    DictionaryDataManager,
)
from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.widgets.option_picker import (
        OptionPicker,
    )
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )
    from main import MainWindow
    from objects.arrow.arrow import Arrow
    from main_window.main_widget.json_manager.json_manager import JsonManager
    from main_window.main_widget.json_manager.special_placement_saver import (
        SpecialPlacementSaver,
    )
    from settings_manager.settings_manager import SettingsManager


class AppContext:
    _settings_manager = None
    _json_manager = None
    _special_placement_handler = None
    _special_placement_loader = None
    _sequence_beat_frame = None
    _selected_arrow: Optional["Arrow"] = None
    _dict_data_manager = DictionaryDataManager()
    _main_window = None  # Will be resolved dynamically

    @classmethod
    def init(
        cls,
        settings_manager,
        json_manager,
        special_placement_handler,
        special_placement_loader,
    ):
        """Initialize AppContext with required services."""
        cls._settings_manager = settings_manager
        cls._json_manager = json_manager
        cls._special_placement_handler = special_placement_handler
        cls._special_placement_loader = special_placement_loader

    @classmethod
    def set_selected_arrow(cls, arrow: Optional["Arrow"]) -> None:
        """Set the globally selected arrow."""
        if cls._selected_arrow:
            cls._selected_arrow.setSelected(False)  # Unselect previous arrow
        cls._selected_arrow = arrow
        if arrow:
            arrow.setSelected(True)  # Select the new arrow

    @classmethod
    def clear_selected_arrow(cls) -> None:
        """Clear the global arrow selection."""
        if cls._selected_arrow:
            cls._selected_arrow.setSelected(False)
        cls._selected_arrow = None

    @classmethod
    def get_selected_arrow(cls) -> Optional["Arrow"]:
        """Retrieve the globally selected arrow."""
        return cls._selected_arrow

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
    def special_placement_saver(cls) -> "SpecialPlacementSaver":
        if cls._special_placement_handler is None:
            raise RuntimeError(
                "AppContext.special_placement_handler() accessed before init()"
            )
        return cls._special_placement_handler

    @classmethod
    def special_placement_loader(cls) -> "SpecialPlacementLoader":
        if cls._special_placement_loader is None:
            raise RuntimeError(
                "AppContext.special_placement_loader() accessed before init()"
            )
        return cls._special_placement_loader

    @classmethod
    def set_sequence_beat_frame(cls, sequence_beat_frame):
        """Set the sequence beat frame after initialization."""
        cls._sequence_beat_frame = sequence_beat_frame

    @classmethod
    def dictionary_data_manager(cls) -> DictionaryDataManager:
        return cls._dict_data_manager

    @classmethod
    def main_window(cls) -> "MainWindow":
        """Retrieve the MainWindow instance safely"""
        if cls._main_window:  # First check if it's already set
            return cls._main_window

        from main_window.main_window import MainWindow  # Lazy import

        app: QApplication = QApplication.instance()
        if not app:
            raise RuntimeError("QApplication not initialized")

        # Search through top-level widgets
        for widget in app.topLevelWidgets():
            if isinstance(widget, MainWindow):
                cls._main_window = widget
                return cls._main_window

        raise RuntimeError(
            f"MainWindow not found! Top-level widgets found: {app.topLevelWidgets()}"
        )

    @classmethod
    def sequence_beat_frame(cls) -> "SequenceBeatFrame":
        """Retrieve sequence_beat_frame only if it's set."""
        if cls._sequence_beat_frame is None:
            raise RuntimeError(
                "AppContext.sequence_beat_frame() accessed before being set. Ensure it is initialized in MainWindow."
            )
        return cls._sequence_beat_frame

    @classmethod
    def option_picker(cls) -> "OptionPicker":
        return cls.main_widget().construct_tab.option_picker

    @classmethod
    def main_widget(cls):
        return cls.main_window().main_widget
