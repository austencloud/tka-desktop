import json
from typing import TYPE_CHECKING, Optional
from data.constants import (
    BEAT,
    BLUE_ATTRS,
    DIAMOND,
    END_ORI,
    GRID_MODE,
    LETTER,
    MOTION_TYPE,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PROP_ROT_DIR,
    RED_ATTRS,
    SEQUENCE_START_POSITION,
)
from main_window.main_widget.sequence_level_evaluator import SequenceLevelEvaluator
from main_window.main_widget.sequence_properties_manager.sequence_properties_manager_factory import (
    SequencePropertiesManagerFactory,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_user_editable_resource_path
from utils.word_simplifier import WordSimplifier

if TYPE_CHECKING:
    from core.application_context import ApplicationContext


class SequenceDataLoaderSaver:
    def __init__(self, app_context: Optional["ApplicationContext"] = None) -> None:
        """
        Initialize SequenceDataLoaderSaver with optional dependency injection.

        Args:
            app_context: Application context with dependencies. If None, uses legacy approach.
        """
        # Try multiple possible locations for current_sequence.json
        import os

        possible_paths = [
            get_user_editable_resource_path(
                "current_sequence.json"
            ),  # Primary: legacy directory
            os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                ),
                "current_sequence.json",
            ),  # Legacy directory root
            os.path.abspath("current_sequence.json"),  # Current directory
            os.path.join("..", "current_sequence.json"),  # Parent directory
            os.path.join("..", "..", "current_sequence.json"),  # Grandparent directory
        ]

        self.current_sequence_json = None
        for path in possible_paths:
            if os.path.exists(path):
                self.current_sequence_json = path
                break

        # Fallback to the original path if none found
        if self.current_sequence_json is None:
            self.current_sequence_json = get_user_editable_resource_path(
                "current_sequence.json"
            )

        # Create sequence properties manager with dependency injection
        if app_context:
            self.sequence_properties_manager = SequencePropertiesManagerFactory.create(
                app_context
            )
        else:
            self.sequence_properties_manager = (
                SequencePropertiesManagerFactory.create_legacy()
            )

    def load_current_sequence(self) -> list[dict]:
        try:
            with open(self.current_sequence_json, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return self.get_default_sequence()

                sequence = json.loads(content)
                if not sequence or not isinstance(sequence, list):
                    return self.get_default_sequence()

            return sequence

        except (FileNotFoundError, json.JSONDecodeError):
            # Create the file with default data if it doesn't exist
            default_sequence = self.get_default_sequence()
            try:
                # Ensure the directory exists before creating the file
                import os

                directory = os.path.dirname(self.current_sequence_json)
                if directory:
                    os.makedirs(directory, exist_ok=True)

                # Create the file directly to avoid circular dependencies during initialization
                with open(self.current_sequence_json, "w", encoding="utf-8") as file:
                    json.dump(default_sequence, file, indent=4, ensure_ascii=False)
            except Exception:
                # If we can't create the file, just return the default sequence
                pass
            return default_sequence

    def get_default_sequence(self) -> list[dict]:
        """Return a default sequence if JSON is missing, empty, or invalid."""
        # Use safe defaults that don't depend on AppContext during initialization
        try:
            author = AppContext.settings_manager().users.get_current_user()
        except:
            author = "Unknown"

        try:
            prop_type = (
                AppContext.settings_manager()
                .global_settings.get_prop_type()
                .name.lower()
            )
        except:
            prop_type = "staff"

        return [
            {
                "word": "",
                "author": author,
                "level": 0,
                "prop_type": prop_type,
                GRID_MODE: DIAMOND,
                "is_circular": False,
                "can_be_CAP": False,
                "is_strict_rotated_CAP": False,
                "is_strict_mirrored_CAP": False,
                "is_strict_swapped_CAP": False,
                "is_mirrored_swapped_CAP": False,
                "is_rotated_swapped_CAP": False,
            }
        ]

    def save_current_sequence(self, sequence: list[dict]):
        if not sequence:
            sequence = self.get_default_sequence()
        else:
            sequence[0]["word"] = WordSimplifier.simplify_repeated_word(
                self.sequence_properties_manager.calculate_word(sequence)
            )
            if "author" not in sequence[0]:
                sequence[0][
                    "author"
                ] = AppContext.settings_manager().users.get_current_user()
            if "level" not in sequence[0]:
                sequence[0]["level"] = (
                    SequenceLevelEvaluator.get_sequence_difficulty_level(sequence)
                )
            if "prop_type" not in sequence[0]:
                sequence[0]["prop_type"] = (
                    AppContext.settings_manager()
                    .global_settings.get_prop_type()
                    .name.lower()
                )
            if "is_circular" not in sequence[0]:
                sequence[0]["is_circular"] = False
            if "can_be_CAP" not in sequence[0]:
                sequence[0]["can_be_CAP"] = False

        # Add beat numbers to each beat at the beginning
        beat_number = 0
        for beat in sequence:
            if LETTER in beat or SEQUENCE_START_POSITION in beat:
                beat_data_with_beat_number = {BEAT: beat_number}
                beat_data_with_beat_number.update(beat)
                sequence[sequence.index(beat)] = beat_data_with_beat_number
                beat_number += 1

        with open(self.current_sequence_json, "w", encoding="utf-8") as file:
            json.dump(sequence, file, indent=4, ensure_ascii=False)

    def clear_current_sequence_file(self):
        self.save_current_sequence([])

    def get_json_prop_rot_dir(self, index: int, color: str) -> int:
        sequence = self.load_current_sequence()
        if sequence:
            return sequence[index][f"{color}_attributes"].get(PROP_ROT_DIR, 0)
        return 0

    def get_json_motion_type(self, index: int, color: str) -> int:
        sequence = self.load_current_sequence()
        if sequence:
            return sequence[index][f"{color}_attributes"].get(MOTION_TYPE, 0)
        return 0

    def get_json_prefloat_prop_rot_dir(self, index: int, color: str) -> int:
        sequence = self.load_current_sequence()
        if sequence:
            return sequence[index][f"{color}_attributes"].get(PREFLOAT_PROP_ROT_DIR, "")
        return 0

    def get_json_prefloat_motion_type(self, index: int, color: str) -> int:
        sequence = self.load_current_sequence()
        if sequence:
            return sequence[index][f"{color}_attributes"].get(
                PREFLOAT_MOTION_TYPE,
                sequence[index][f"{color}_attributes"].get(MOTION_TYPE, 0),
            )
        return 0

    def get_red_end_ori(self, sequence):
        last_pictograph_data = (
            sequence[-1]
            if sequence[-1].get("is_placeholder", "") != True
            else sequence[-2]
        )

        if sequence:
            return last_pictograph_data[RED_ATTRS][END_ORI]
        return 0

    def get_blue_end_ori(self, sequence):
        last_pictograph_data = (
            sequence[-1]
            if sequence[-1].get("is_placeholder", "") != True
            else sequence[-2]
        )

        if sequence:
            return last_pictograph_data[BLUE_ATTRS][END_ORI]
        return 0

    def load_last_beat_data(self) -> dict:
        sequence = self.load_current_sequence()
        if sequence:
            return sequence[-1]
        return {}

    def get_json_turns(self, index: int, color: str) -> int:
        sequence = self.load_current_sequence()
        if sequence:
            return sequence[index][f"{color}_attributes"].get("turns", 0)
        return 0
