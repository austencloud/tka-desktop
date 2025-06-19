# Application services package

# Conditional imports to handle Qt DLL loading issues during testing
try:
    from .positioning.arrow_management_service import (
        ArrowManagementService,
        IArrowManagementService,
    )
    from .positioning.prop_management_service import (
        PropManagementService,
        IPropManagementService,
    )

    QT_SERVICES_AVAILABLE = True
except ImportError:
    # Create mock classes for testing when Qt is not available
    class ArrowManagementService:
        def __init__(self, *_args, **_kwargs):
            pass

    class IArrowManagementService:
        def __init__(self, *_args, **_kwargs):
            pass

    class PropManagementService:
        def __init__(self, *_args, **_kwargs):
            pass

    class IPropManagementService:
        def __init__(self, *_args, **_kwargs):
            pass

    QT_SERVICES_AVAILABLE = False

from .motion.motion_validation_service import (
    MotionValidationService,
    IMotionValidationService,
)
from .motion.motion_orientation_service import (
    MotionOrientationService,
    IMotionOrientationService,
)

# Layout services consolidated into LayoutManagementService (ILayoutService)
from .core.pictograph_management_service import PictographManagementService
from .core.sequence_management_service import SequenceManagementService

__all__ = [
    "ArrowManagementService",
    "IArrowManagementService",
    "PropManagementService",
    "IPropManagementService",
    "MotionValidationService",
    "IMotionValidationService",
    "MotionOrientationService",
    "IMotionOrientationService",
    # Layout services consolidated into LayoutManagementService
    "PictographManagementService",
    "SequenceManagementService",
]
