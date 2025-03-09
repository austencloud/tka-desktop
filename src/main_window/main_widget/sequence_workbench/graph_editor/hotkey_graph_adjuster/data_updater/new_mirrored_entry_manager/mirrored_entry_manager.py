import logging
from .mirrored_entry_adapter import MirroredEntryAdapter

logger = logging.getLogger(__name__)

class MirroredEntryManager:
    
    def __init__(self, data_updater) -> None:
        self.data_updater = data_updater
        self.adapter = MirroredEntryAdapter(data_updater)
        self.turns_tuple_generator = self.adapter.factory.create_service(data_updater).turns_manager
        self.rot_angle_manager = self.adapter.rot_angle_manager()
        self.data_prep = type('DataPrep', (), {
            'is_new_entry_needed': lambda arrow: False,
            'get_keys_for_mixed_start_ori': lambda grid_mode, letter, ori_key: (ori_key, {})
        })()
    
    def update_mirrored_entry_in_json(self) -> None:
        self.adapter.update_mirrored_entry_in_json()
