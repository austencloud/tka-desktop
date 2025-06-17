from typing import Optional
from domain.models.core_models import SequenceData
from core.interfaces.workbench_services import IFullScreenService


class FullScreenService(IFullScreenService):
    """Service for full screen viewing functionality"""

    def __init__(self):
        pass

    def create_sequence_thumbnail(self, sequence: SequenceData) -> bytes:
        """Create thumbnail from sequence"""
        # TODO: Implement thumbnail creation
        # For now, return empty bytes
        return b""

    def show_full_screen_view(self, sequence: SequenceData) -> None:
        """Show sequence in full screen overlay"""
        # TODO: Implement full screen view
        # For now, just print that it was requested
        print(
            f"🖥️ Full screen view requested for sequence with {len(sequence.beats)} beats"
        )
        pass
