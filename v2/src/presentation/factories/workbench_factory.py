from typing import Optional
from PyQt6.QtWidgets import QWidget
from core.dependency_injection.di_container import SimpleContainer
from core.interfaces.core_services import ILayoutService
from core.interfaces.workbench_services import (
    ISequenceWorkbenchService,
    IFullScreenService,
    IBeatDeletionService,
    IGraphEditorService,
    IDictionaryService,
)
from application.services.sequence_management_service import (
    SequenceManagementService,
)
from application.services.ui_state_management_service import (
    UIStateManagementService,
)

from presentation.components.workbench import ModernSequenceWorkbench


def create_modern_workbench(
    container: SimpleContainer, parent: Optional[QWidget] = None
) -> ModernSequenceWorkbench:
    """Factory function to create a fully configured modern sequence workbench"""

    # Configure all services if not already done
    configure_workbench_services(container)

    # Get services from container
    layout_service = container.resolve(ILayoutService)
    workbench_service = container.resolve(ISequenceWorkbenchService)
    fullscreen_service = container.resolve(IFullScreenService)
    deletion_service = container.resolve(IBeatDeletionService)
    graph_service = container.resolve(IGraphEditorService)
    dictionary_service = container.resolve(IDictionaryService)

    # Create and return configured workbench
    return ModernSequenceWorkbench(
        layout_service=layout_service,
        workbench_service=workbench_service,
        fullscreen_service=fullscreen_service,
        deletion_service=deletion_service,
        graph_service=graph_service,
        dictionary_service=dictionary_service,
        parent=parent,
    )


def configure_workbench_services(container: SimpleContainer) -> None:
    """Configure workbench services in the dependency injection container"""

    # Register consolidated services directly
    container.register_singleton(ISequenceWorkbenchService, SequenceManagementService)
    container.register_singleton(IBeatDeletionService, SequenceManagementService)
    container.register_singleton(IDictionaryService, SequenceManagementService)
    container.register_singleton(IFullScreenService, UIStateManagementService)
    container.register_singleton(IGraphEditorService, UIStateManagementService)
