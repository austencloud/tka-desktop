import json
from data.constants import DIAMOND, GRID_MODE
from utils.path_helpers import get_user_editable_resource_path


class CurrentSequenceLoader:
    def __init__(self, filename="current_sequence.json"):
        self.current_sequence_json = get_user_editable_resource_path(filename)

    def load_current_sequence_json(self) -> list[dict]:
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
            return self.get_default_sequence()

    def get_default_sequence(self) -> list[dict]:
        """Return a default sequence if JSON is missing, empty, or invalid."""
        return [
            {
                "word": "",
                "author": "",  # Placeholder, will be updated later
                "level": 0,
                "prop_type": "",  # Placeholder, will be updated later
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
