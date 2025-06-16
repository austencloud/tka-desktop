"""
Beat Frame Components

Modern beat frame system for V2 sequence workbench.
"""

from .sequence_beat_frame import SequenceBeatFrame
from .beat_view import ModernBeatView
from .start_position_view import StartPositionView
from .beat_selection_manager import BeatSelectionManager

__all__ = [
    "SequenceBeatFrame",
    "ModernBeatView",
    "StartPositionView",
    "BeatSelectionManager",
]
