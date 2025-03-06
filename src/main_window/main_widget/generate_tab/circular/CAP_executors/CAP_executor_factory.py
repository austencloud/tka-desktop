from main_window.main_widget.generate_tab.circular.CAP_executors.CAP_executor import (
    CAPExecutor,
)
from .CAP_type import CAPType
from .strict_mirrored_CAP_executor import StrictMirroredCAPExecutor
from .strict_rotated_CAP_executor import StrictRotatedCAPExecutor


class CAPExecutorFactory:
    _executor_map = {
        CAPType.STRICT_MIRRORED: StrictMirroredCAPExecutor,
        CAPType.STRICT_ROTATED: StrictRotatedCAPExecutor,
        # CAPExecutorType.STRICT_SWAPPED: StrictSwappedCAPExecutor,
        # CAPExecutorType.MIRRORED_SWAPPED: MirroredSwappedCAPExecutor,
        # CAPExecutorType.MIRRORED_COMPLIMENTARY: MirroredComplimentaryCAPExecutor,
        # CAPExecutorType.COMPLIMENTARY_SWAPPED: ComplimentarySwappedCAPExecutor,
    }

    @staticmethod
    def create_executor(cap_type: CAPType, circular_sequence_generator) -> CAPExecutor:
        executor_class = CAPExecutorFactory._executor_map.get(cap_type)
        if executor_class:
            if cap_type == CAPType.STRICT_MIRRORED:
                return executor_class(circular_sequence_generator, False)
            else:
                return executor_class(circular_sequence_generator)
        else:
            raise ValueError(f"Unknown CAPExecutorType: {cap_type}")
