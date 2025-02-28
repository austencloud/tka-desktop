import json
from typing import TYPE_CHECKING
from data.constants import (
    BEAT,
    BLUE_ATTRIBUTES,
    END_ORI,
    LETTER,
    MOTION_TYPE,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PROP_ROT_DIR,
    RED_ATTRIBUTES,
    SEQUENCE_START_POSITION,
)
from main_window.main_widget.json_manager.current_sequence_loader import (
    CurrentSequenceLoader,
)
from utilities.word_simplifier import WordSimplifier

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JsonManager


class JsonSequenceLoaderSaver:
    def __init__(self, json_manager: "JsonManager") -> None:
        self.json_manager = json_manager
        self.current_sequence_loader = CurrentSequenceLoader()

    def load_current_sequence_json(self) -> list[dict]:
        return self.current_sequence_loader.load_current_sequence_json()

    def get_default_sequence(self) -> list[dict]:
        return self.current_sequence_loader.get_default_sequence()

    def save_current_sequence(self, sequence: list[dict]):
        if not sequence:
            sequence = self.get_default_sequence()

        with open(
            self.current_sequence_loader.current_sequence_json,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(sequence, file, indent=4, ensure_ascii=False)

    def _get_attribute_from_json(
        self, index: int, color: str, attribute: str, default=None
    ):
        sequence = self.load_current_sequence_json()
        if sequence and index < len(sequence):
            return sequence[index][f"{color}_attributes"].get(attribute, default)
        return default

    def get_prop_rot_dir_from_json(self, index: int, color: str) -> int:
        return self._get_attribute_from_json(index, color, PROP_ROT_DIR, 0)

    def get_motion_type_from_json_at_index(self, index: int, color: str) -> int:
        return self._get_attribute_from_json(index, color, MOTION_TYPE, 0)

    def get_prefloat_prop_rot_dir_from_json(self, index: int, color: str) -> int:
        return self._get_attribute_from_json(index, color, PREFLOAT_PROP_ROT_DIR, "")

    def get_prefloat_motion_type_from_json_at_index(
        self, index: int, color: str
    ) -> int:
        return self._get_attribute_from_json(
            index,
            color,
            PREFLOAT_MOTION_TYPE,
            self._get_attribute_from_json(index, color, MOTION_TYPE, 0),
        )

    def _get_last_pictograph_data(self, sequence: list[dict]) -> dict:
        return next(
            (
                beat
                for beat in reversed(sequence)
                if not beat.get("is_placeholder", False) == True
            ),
            sequence[-1] if sequence else {},
        )

    def get_red_end_ori(self, sequence: list[dict]) -> int:
        last_pictograph_data = self._get_last_pictograph_data(sequence)
        return (
            last_pictograph_data.get(RED_ATTRIBUTES, {}).get(END_ORI, 0)
            if sequence
            else 0
        )

    def get_blue_end_ori(self, sequence: list[dict]) -> int:
        last_pictograph_data = self._get_last_pictograph_data(sequence)
        return (
            last_pictograph_data.get(BLUE_ATTRIBUTES, {}).get(END_ORI, 0)
            if sequence
            else 0
        )

    def load_last_beat_dict(self) -> dict:
        sequence = self.load_current_sequence_json()
        return sequence[-1] if sequence else {}
