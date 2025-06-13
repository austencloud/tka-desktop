from typing import Optional
from PyQt6.QtWidgets import QWidget
from src.core.dependency_injection.simple_container import SimpleContainer
from src.core.interfaces.core_services import ILayoutService
from src.core.interfaces.workbench_services import (
    ISequenceWorkbenchService,
    IFullScreenService,
    IBeatDeletionService,
    IGraphEditorService,
    IDictionaryService,
)
from src.application.services.workbench_services import (
    SequenceWorkbenchService,
    BeatDeletionService,
    DictionaryService,
    FullScreenService,
)
from src.application.services.graph_editor_service import GraphEditorService
from src.presentation.components.sequence_workbench import ModernSequenceWorkbench


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

    # Register core workbench services
    container.register_singleton(ISequenceWorkbenchService, SequenceWorkbenchService)
    container.register_singleton(IBeatDeletionService, BeatDeletionService)
    container.register_singleton(IDictionaryService, DictionaryService)
    container.register_singleton(IFullScreenService, FullScreenService)

    # Register modern graph editor service (replaces placeholder)
    container.register_singleton(IGraphEditorService, GraphEditorService)
