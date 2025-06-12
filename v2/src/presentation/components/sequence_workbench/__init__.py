"""
Sequence Workbench Components

V2 sequence workbench with modern architecture.
"""

from src.presentation.components.sequence_workbench.beat_frame import (
    ModernBeatFrame,
    ModernBeatView,
    StartPositionView,
    BeatSelectionManager,
)

from src.presentation.components.modern_sequence_workbench import (
    ModernSequenceWorkbench,
)

__all__ = [
    "ModernSequenceWorkbench",
    "ModernBeatFrame",
    "ModernBeatView",
    "StartPositionView",
    "BeatSelectionManager",
]
