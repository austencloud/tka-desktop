from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QStackedLayout,
)
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_workbench.graph_editor.graph_editor_animator import (
    GraphEditorAnimator,
)
from main_window.main_widget.sequence_workbench.graph_editor.graph_editor_toggle_tab import (
    GraphEditorToggleTab,
)

from .arrow_selection_manager import ArrowSelectionManager
from .graph_editor_layout_manager import GraphEditorLayoutManager
from .adjustment_panel.beat_adjustment_panel import BeatAdjustmentPanel
from .pictograph_container.GE_pictograph_container import GraphEditorPictographContainer

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class GraphEditor(QFrame):
    main_layout: QHBoxLayout
    pictograph_layout: QVBoxLayout
    adjustment_panel_layout: QVBoxLayout
    left_stack: QStackedLayout
    right_stack: QStackedLayout
    is_toggled: bool = False

    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        super().__init__(sequence_workbench)
        self.sequence_workbench = sequence_workbench
        self.main_widget = sequence_workbench.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._setup_components()
        self.layout_manager.setup_layout()
        self.hide()

    def _setup_components(self) -> None:
        self.selection_manager = ArrowSelectionManager(self)
        self.pictograph_container = GraphEditorPictographContainer(self)
        self.adjustment_panel = BeatAdjustmentPanel(self)
        self.layout_manager = GraphEditorLayoutManager(self)
        self.toggle_tab = GraphEditorToggleTab(self)
        self.placeholder = QFrame(self)
        self.animator = GraphEditorAnimator(self)

    def get_graph_editor_height(self):
        return int(self.sequence_workbench.height() // 3.5)

    def resizeEvent(self, event) -> None:
        graph_editor_height = self.get_graph_editor_height()
        width = self.sequence_workbench.width()
        self.setFixedSize(width, graph_editor_height)
        self.raise_()
        super().resizeEvent(event)

    def update_graph_editor(self) -> None:
        self.adjustment_panel.update_adjustment_panel()
        self.pictograph_container.update_pictograph()
