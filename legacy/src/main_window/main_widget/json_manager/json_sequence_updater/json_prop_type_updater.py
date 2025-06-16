from typing import TYPE_CHECKING

from enums.prop_type import PropType


if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )


class JsonPropTypeUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater") -> None:
        self.json_manager = json_updater.json_manager

    def update_prop_type_in_json(self, prop_type: PropType) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence()
        sequence[0]["prop_type"] = prop_type.name.lower()
        self.json_manager.loader_saver.save_current_sequence(sequence)
