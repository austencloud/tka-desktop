from typing import Optional
from PyQt6.QtWidgets import QWidget
from core.dependency_injection.di_container import DIContainer
from src.core.interfaces.core_services import ILayoutService, IUIStateManagementService
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

    # Register consolidated services directly
    container.register_singleton(ISequenceWorkbenchService, SequenceManagementService)
    container.register_singleton(IBeatDeletionService, SequenceManagementService)
    container.register_singleton(IDictionaryService, SequenceManagementService)
    container.register_singleton(IFullScreenService, FullScreenService)

    # Register GraphEditorService with UI state service dependency
    graph_editor_service = GraphEditorService(ui_state_service)
    container.register_instance(IGraphEditorService, graph_editor_service)

    # Note: ILayoutService should already be registered in main.py
    # Only register if not already registered to avoid overriding register_instance with register_singleton
    try:
        layout_service = container.resolve(ILayoutService)

        # Don't register again - this would override the existing registration
    except Exception as e:

        # Register fallback if not found
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )

        container.register_singleton(ILayoutService, LayoutManagementService)
