from typing import TYPE_CHECKING

from data.constants import DIAMOND, END_POS, GRID_MODE, LETTER
from main_window.main_widget.sequence_level_evaluator import SequenceLevelEvaluator
from main_window.main_widget.sequence_properties_manager.strict_swapped_CAP_checker import (
    StrictSwappedCAPChecker,
)
from settings_manager.global_settings.app_context import AppContext

from .mirrored_swapped_CAP_checker import (
    MirroredSwappedCAPChecker,
)
from .strict_mirrored_CAP_checker import StrictMirroredCAPChecker
from .rotated_swapped_CAP_checker import (
    RotatedSwappedCAPChecker,
)
from .strict_rotated_CAP_checker import StrictRotatedCAPChecker

if TYPE_CHECKING:
    pass


class SequencePropertiesManager:
    def __init__(self):
        self.sequence: list[dict] = []

        # Default properties
        self.properties = {
            "ends_at_start_pos": False,
            "can_be_CAP": False,
            "is_strict_rotated_CAP": False,
            "is_strict_mirrored_CAP": False,
            "is_strict_swapped_CAP": False,
            "is_mirrored_swapped_CAP": False,
            "is_rotated_swapped_CAP": False,
        }

        # Instantiate the individual checkers
        self.checkers = {
            "is_strict_rotated_CAP": StrictRotatedCAPChecker(self),
            "is_strict_mirrored_CAP": StrictMirroredCAPChecker(self),
            "is_strict_swapped_CAP": StrictSwappedCAPChecker(self),
            "is_mirrored_swapped_CAP": MirroredSwappedCAPChecker(self),
            "is_rotated_swapped_CAP": RotatedSwappedCAPChecker(self),
        }

    def instantiate_sequence(self, sequence):
        self.sequence = sequence[1:]

    def update_sequence_properties(self):
        sequence = AppContext.json_manager().loader_saver.load_current_sequence()
        if len(sequence) <= 1:
            return

        self.instantiate_sequence(sequence)
        properties = self.check_all_properties()
        sequence[0].update(properties)

        AppContext.json_manager().loader_saver.save_current_sequence(sequence)

    def calculate_word(self, sequence):
        if sequence is None or not isinstance(sequence, list):
            sequence = AppContext.json_manager().loader_saver.load_current_sequence()

        if len(sequence) < 2:
            return ""

        word = "".join(
            entry.get(LETTER, "") for entry in sequence[2:] if LETTER in entry
        )
        return word

    def check_all_properties(self):
        if not self.sequence:
            return self._default_properties()

        # Check basic properties
        self.properties["ends_at_start_pos"] = self._check_ends_at_start_pos()
        self.properties["can_be_CAP"] = self._check_can_be_CAP()

        # Check for CAPs, starting with strict rotated
        self.properties["is_strict_rotated_CAP"] = self.checkers[
            "is_strict_rotated_CAP"
        ].check()

        if not self.properties["is_strict_rotated_CAP"]:
            # Cascade checks if not rotated
            for key in [
                "is_strict_mirrored_CAP",
                "is_strict_swapped_CAP",
                "is_mirrored_swapped_CAP",
                "is_rotated_swapped_CAP",
            ]:
                self.properties[key] = self.checkers[key].check()

                # Stop further checks if a property is set to True
                if self.properties[key]:
                    break

        return self._gather_properties()

    def _gather_properties(self):
        return {
            "word": self.calculate_word(
                AppContext.json_manager().loader_saver.load_current_sequence()
            ),
            "author": AppContext.settings_manager().users.user_manager.get_current_user(),
            "level": SequenceLevelEvaluator().get_sequence_difficulty_level(
                self.sequence
            ),
            "is_circular": self.properties["ends_at_start_pos"],
            "can_be_CAP": self.properties["can_be_CAP"],
            **{
                key: self.properties[key]
                for key in self.properties
                if key.startswith("is_")
            },
        }

    def _default_properties(self):
        return {
            "word": "",
            "author": AppContext.settings_manager().users.user_manager.get_current_user(),
            "level": 0,
            "is_circular": False,
            "can_be_CAP": False,
            "is_strict_rotated_CAP": False,
            "is_strict_mirrored_CAP": False,
            "is_strict_swapped_CAP": False,
            "is_mirrored_swapped_CAP": False,
            "is_rotated_swapped_CAP": False,
        }

    def _check_ends_at_start_pos(self) -> bool:
        if self.sequence[-1].get("is_placeholder", False):
            return self.sequence[-2][END_POS] == self.sequence[0][END_POS]
        else:
            return self.sequence[-1][END_POS] == self.sequence[0][END_POS]

    def _check_can_be_CAP(self) -> bool:
        if self.sequence[-1].get("is_placeholder", False):
            return self.sequence[-2][END_POS].rstrip("0123456789") == self.sequence[0][
                END_POS
            ].rstrip("0123456789")
        else:
            return self.sequence[-1][END_POS].rstrip("0123456789") == self.sequence[0][
                END_POS
            ].rstrip("0123456789")
