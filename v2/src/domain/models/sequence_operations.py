from typing import List, Dict, Any
from dataclasses import dataclass
from .core_models import SequenceData, BeatData


@dataclass(frozen=True)
class SequenceOperation:
    """Base class for sequence modification operations"""

    success_message: str
    error_message: str


@dataclass(frozen=True)
class ColorSwapOperation(SequenceOperation):
    """Color swap operation for sequences"""

    success_message: str = "Colors swapped!"
    error_message: str = "No sequence to color swap."

    def execute(self, sequence: SequenceData) -> SequenceData:
        """Execute color swap on sequence"""
        if not sequence.beats:
            return sequence

        new_beats = []
        for beat in sequence.beats:
            new_blue = self._swap_motion_color(beat.red_motion)
            new_red = self._swap_motion_color(beat.blue_motion)
            new_beat = beat.update(blue_motion=new_blue, red_motion=new_red)
            new_beats.append(new_beat)

        from dataclasses import replace

        return replace(sequence, beats=new_beats)

    def _swap_motion_color(self, color: Any) -> Any:
        """Swap motion color (placeholder implementation)"""
        # Actual color swapping logic would go here
        return color  # Placeholder


@dataclass(frozen=True)
class ReflectionOperation(SequenceOperation):
    """Reflection operation for sequences"""

    success_message: str = "Sequence reflected!"
    error_message: str = "No sequence to reflect."

    def execute(self, sequence: SequenceData) -> SequenceData:
        """Execute reflection on sequence"""
        if sequence.length < 2:
            raise ValueError(self.error_message)

        reflected_beats = []
        for beat in sequence.beats:
            reflected_beat = self._reflect_beat(beat)
            reflected_beats.append(reflected_beat)

        from dataclasses import replace

        return replace(sequence, beats=reflected_beats)

    def _reflect_beat(self, beat: BeatData) -> BeatData:
        """Reflect a single beat"""
        # Implementation would use legacy reflection logic
        return beat  # Placeholder


@dataclass(frozen=True)
class RotationOperation(SequenceOperation):
    """Rotation operation for sequences"""

    success_message: str = "Sequence rotated!"
    error_message: str = "No sequence to rotate."

    def execute(self, sequence: SequenceData) -> SequenceData:
        """Execute rotation on sequence"""
        if sequence.length < 2:
            raise ValueError(self.error_message)

        rotated_beats = []
        for beat in sequence.beats:
            rotated_beat = self._rotate_beat(beat)
            rotated_beats.append(rotated_beat)

        from dataclasses import replace

        return replace(sequence, beats=rotated_beats)

    def _rotate_beat(self, beat: BeatData) -> BeatData:
        """Rotate a single beat"""
        # Implementation would use legacy rotation logic
        return beat  # Placeholder
