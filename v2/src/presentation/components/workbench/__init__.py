"""
Sequence Workbench Components

Modern sequence workbench with modern architecture.
"""

from presentation.components.workbench.sequence_beat_frame import (
    SequenceBeatFrame,
    BeatView,
    StartPositionView,
    BeatSelectionManager,
)

from .workbench import (
    ModernSequenceWorkbench,
)

from .indicator_section import WorkbenchIndicatorSection
from .beat_frame_section import WorkbenchBeatFrameSection
from .graph_section import WorkbenchGraphSection
from .event_controller import WorkbenchEventController
from .button_interface import (
    WorkbenchButtonInterfaceAdapter,
    IWorkbenchButtonInterface,
    WorkbenchButtonSignals,
    ButtonOperationResult,
)

# Legacy compatibility
from .button_interface import (
    WorkbenchButtonInterfaceAdapter as ButtonInterface,
)

__all__ = [
    "ModernSequenceWorkbench",
    "SequenceBeatFrame",
    "BeatView",
    "StartPositionView",
    "BeatSelectionManager",
    # Core components
    "WorkbenchIndicatorSection",
    "WorkbenchBeatFrameSection",
    "WorkbenchGraphSection",
    "WorkbenchEventController",
    # Interface adapters
    "WorkbenchButtonInterfaceAdapter",
    "IWorkbenchButtonInterface",
    "WorkbenchButtonSignals",
    "ButtonOperationResult",
    "ButtonInterface",  # Legacy alias
]
