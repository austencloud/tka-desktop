from enums.letter.letter import Letter

from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mirrored_entry_updater import MirroredEntryUpdater


class BaseMirroredEntryUpdater:
    def __init__(self, mirrored_entry_updater: "MirroredEntryUpdater", arrow: Arrow):
        self.mirrored_entry_updater = mirrored_entry_updater
        self.arrow = arrow

    def update_entry(self, letter: Letter, original_turn_data: dict):
        # Common update logic
        pass
