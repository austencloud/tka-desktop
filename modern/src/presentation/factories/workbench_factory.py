from typing import Optional
from PyQt6.QtWidgets import QWidget
from core.dependency_injection.di_container import DIContainer
from core.interfaces.core_services import ILayoutService, IUIStateManagementService
from core.interfaces.workbench_services import (
    ISequenceWorkbenchService,
    IFullScreenService,
    IBeatDeletionService,
    IGraphEditorService,
    IDictionaryService,
)
from application.services.core.sequence_management_service import (
    SequenceManagementService,
)
from application.services.ui.ui_state_management_service import (
    UIStateManagementService,
)
from application.services.ui.full_screen_service import FullScreenService
from application.services.graph_editor_service import GraphEditorService

from presentation.components.workbench import ModernSequenceWorkbench


def create_modern_workbench(
    container: DIContainer, parent: Optional[QWidget] = None
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


def configure_workbench_services(container: DIContainer) -> None:
    """Configure workbench services in the dependency injection container"""

    # Get UI state service for services that need it
    ui_state_service = container.resolve(IUIStateManagementService)

    # Register consolidated services directly with event bus support
    try:
        from core.events import IEventBus

        event_bus = (
            container.resolve(IEventBus)
            if hasattr(container, "_singletons") and IEventBus in container._singletons
            else None
        )
    except ImportError:
        event_bus = None

    # Create sequence management service with event bus
    sequence_service = SequenceManagementService(event_bus=event_bus)
    container.register_instance(ISequenceWorkbenchService, sequence_service)
    container.register_instance(IBeatDeletionService, sequence_service)
    container.register_instance(IDictionaryService, sequence_service)
    container.register_singleton(
        IFullScreenService, FullScreenService
    )  # Register GraphEditorService with UI state service dependency
    graph_editor_service = GraphEditorService(ui_state_service)
    container.register_instance(IGraphEditorService, graph_editor_service)

    # ILayoutService should already be registered in main.py
    # No need to register again - using the service registered in main.py
