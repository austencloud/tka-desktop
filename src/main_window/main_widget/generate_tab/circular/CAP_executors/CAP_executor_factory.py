from main_window.main_widget.generate_tab.circular.CAP_executors.CAP_executor import (
    CAPExecutor,
)
from .CAP_type import CAPType
from .strict_mirrored.strict_mirrored_CAP_executor import StrictMirroredCAPExecutor
from .strict_rotated.strict_rotated_CAP_executor import StrictRotatedCAPExecutor
from .strict_swapped.strict_swapped_CAP_executor import StrictSwappedCAPExecutor

class CAPExecutorFactory:
    _executor_map = {
        CAPType.STRICT_MIRRORED: StrictMirroredCAPExecutor,
        CAPType.STRICT_ROTATED: StrictRotatedCAPExecutor,
        CAPType.STRICT_SWAPPED: StrictSwappedCAPExecutor,
        # CAPType.MIRRORED_SWAPPED: MirroredSwappedCAPExecutor,
        # CAPType.MIRRORED_COMPLIMENTARY: MirroredComplimentaryCAPExecutor,
        # CAPType.COMPLIMENTARY_SWAPPED: ComplimentarySwappedCAPExecutor,
    }

    @staticmethod
    def create_executor(cap_type: CAPType, circular_sequence_generator) -> CAPExecutor:
        executor_class = CAPExecutorFactory._executor_map.get(cap_type)
        if executor_class:
            return executor_class(circular_sequence_generator)
        else:
            raise ValueError(f"Unknown CAPType: {cap_type}")
