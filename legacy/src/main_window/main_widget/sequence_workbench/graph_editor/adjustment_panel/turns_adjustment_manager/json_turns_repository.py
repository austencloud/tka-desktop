# src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/new_turns_adjustment_manager/json_turns_repository.py
from typing import Optional
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_repository import (
    TurnsRepository,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
    TurnsValue,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext
from main_window.main_widget.json_manager.json_manager import JsonManager


class JsonTurnsRepository(TurnsRepository):
    def __init__(self, json_manager: "JsonManager"):
        self._manager = json_manager

    def save(self, value: TurnsValue, color: str):  # ✅ Accept color
        """Saves turns value to JSON through the existing JSON manager"""
        self.beat_frame = (
            AppContext.main_window().main_widget.sequence_workbench.beat_frame
        )
        try:
            pictograph_index = self._get_pictograph_index()
            self._manager.updater.turns_updater.update_turns_in_json(
                pictograph_index,
                color,
                value.raw_value,
            )
        except Exception as e:
            raise RuntimeError(f"JSON save failed: {str(e)}") from e

    def load(self) -> Optional[TurnsValue]:
        """Loads turns value from JSON"""
        try:
            pictograph_index = self._get_pictograph_index()
            raw_value = self._manager.loader_saver.get_json_turns(
                pictograph_index, self._get_color()
            )
            return TurnsValue(raw_value)
        except Exception as e:
            raise RuntimeError(f"JSON load failed: {str(e)}") from e

    def _get_pictograph_index(self) -> int:
        return self.beat_frame.get.index_of_currently_selected_beat() + 2

    def _get_color(self) -> str:
        """Retrieve the color of the motion being modified, as explicitly stored."""
        return self._color  # ✅ No more guessing – we now always use the correct color
