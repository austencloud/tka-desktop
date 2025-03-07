from main_window.main_widget.generate_tab.circular.CAP_executors.rotated_complementary_CAP_executor import RotatedComplementaryCAPExecutor
from .CAP_executors.CAP_executor import CAPExecutor
from .CAP_executors.mirrored_swapped_CAP_executor import MirroredSwappedCAPExecutor
from .CAP_executors.swapped_complementary_CAP_executor import (
    SwappedComplementaryCAPExecutor,
)
from .CAP_type import CAPType
from .CAP_executors.strict_mirrored_CAP_executor import StrictMirroredCAPExecutor
from .CAP_executors.strict_rotated_CAP_executor import StrictRotatedCAPExecutor
from .CAP_executors.strict_swapped_CAP_executor import StrictSwappedCAPExecutor
from .CAP_executors.strict_complementary_CAP_executor import StrictComplementaryCAPExecutor
from .CAP_executors.mirrored_complementary_CAP_executor import MirroredComplementaryCAPExecutor
from .CAP_executors.rotated_swapped_CAP_executor import RotatedSwappedCAPExecutor
from .CAP_executors.mirrored_rotated_CAP_executor import MirroredRotatedCAPExecutor
# from .CAP_executors.rotated_swapped_complementary_CAP_executor import RotatedSwappedComplementaryCAPExecutor
# from .CAP_executors.mirrored_swapped_complementary_CAP_executor import MirroredSwappedComplementaryCAPExecutor
# from .CAP_executors.mirrored_rotated_swapped_CAP_executor import MirroredRotatedSwappedCAPExecutor
# from .CAP_executors.mirrored_rotated_complementary_swapped_CAP_executor import MirroredRotatedComplementarySwappedCAPExecutor

class CAPExecutorFactory:
    _executor_map = {
        CAPType.STRICT_MIRRORED: StrictMirroredCAPExecutor,
        CAPType.STRICT_ROTATED: StrictRotatedCAPExecutor,
        CAPType.STRICT_SWAPPED: StrictSwappedCAPExecutor,
        CAPType.MIRRORED_SWAPPED: MirroredSwappedCAPExecutor,
        CAPType.SWAPPED_COMPLEMENTARY: SwappedComplementaryCAPExecutor,
        CAPType.STRICT_COMPLEMENTARY: StrictComplementaryCAPExecutor,
        CAPType.ROTATED_COMPLEMENTARY: RotatedComplementaryCAPExecutor,
        CAPType.MIRRORED_COMPLEMENTARY: MirroredComplementaryCAPExecutor,
        CAPType.ROTATED_SWAPPED: RotatedSwappedCAPExecutor,
        CAPType.MIRRORED_ROTATED: StrictMirroredCAPExecutor,
        CAPType.MIRRORED_COMPLEMENTARY_ROTATED: MirroredComplementaryCAPExecutor,
        # CAPType.ROTATED_SWAPPED_COMPLEMENTARY: RotatedSwappedComplementaryCAPExecutor,
        # CAPType.MIRRORED_SWAPPED_COMPLEMENTARY: MirroredSwappedComplementaryCAPExecutor,
        # CAPType.MIRRORED_ROTATED_SWAPPED: MirroredRotatedSwappedCAPExecutor,
        # CAPType.MIRRORED_ROTATED_COMPLEMENTARY_SWAPPED: MirroredRotatedComplementarySwappedCAPExecutor,
        
    }

    @staticmethod
    def create_executor(cap_type: CAPType, circular_sequence_generator) -> CAPExecutor:
        executor_class = CAPExecutorFactory._executor_map.get(cap_type)
        if executor_class:
            return executor_class(circular_sequence_generator)
        else:
            raise ValueError(f"Unknown CAPType: {cap_type}")
