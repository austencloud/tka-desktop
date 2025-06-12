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
from src.presentation.components.sequence_workbench import ModernSequenceWorkbench


class GraphEditorService(IGraphEditorService):
    """Placeholder graph editor service"""

    def update_graph_display(self, sequence) -> None:
        pass

    def toggle_graph_visibility(self) -> bool:
        return False


def create_modern_workbench(
    container: SimpleContainer, parent: Optional[QWidget] = None
) -> ModernSequenceWorkbench:
    """
    Factory function to create a modern sequence workbench with all dependencies injected.

    This demonstrates how v2 architecture eliminates v1 technical debt:

    ELIMINATED FROM V1:
    - AppContext.json_manager() global access
    - self.main_widget coupling
    - self.sequence_workbench.beat_frame.sequence_workbench chains
    - Hard-coded dependencies in constructors
    - Mutable state scattered across components

    PROVIDED IN V2:
    - Clean dependency injection
    - Immutable domain models
    - Service-based architecture
    - Testable components
    - Zero global state access
    """

    # Resolve services from container (no global state!)
    layout_service = container.resolve(ILayoutService)

    # Create workbench services with v1 business logic
    workbench_service = SequenceWorkbenchService()
    fullscreen_service = FullScreenService()
    deletion_service = BeatDeletionService()
    graph_service = GraphEditorService()
    dictionary_service = DictionaryService()

    # Create the modern workbench with injected dependencies
    workbench = ModernSequenceWorkbench(
        layout_service=layout_service,
        workbench_service=workbench_service,
        fullscreen_service=fullscreen_service,
        deletion_service=deletion_service,
        graph_service=graph_service,
        dictionary_service=dictionary_service,
        parent=parent,
    )

    return workbench


def configure_workbench_services(container: SimpleContainer) -> None:
    """Configure workbench services in the dependency injection container"""

    # Register workbench services as singletons
    container.register_singleton(ISequenceWorkbenchService, SequenceWorkbenchService)
    container.register_singleton(IFullScreenService, FullScreenService)
    container.register_singleton(IBeatDeletionService, BeatDeletionService)
    container.register_singleton(IGraphEditorService, GraphEditorService)
    container.register_singleton(IDictionaryService, DictionaryService)
