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
from legacy.src.legacy_settings_manager.legacy_settings_manager import pyqtSignal

from .arrow_selection_manager import ArrowSelectionManager
from .graph_editor_layout_manager import GraphEditorLayoutManager
from .adjustment_panel.legacy_adjustment_panel import LegacyAdjustmentPanel
from .pictograph_container.legacy_GE_pictograph_container import (
    LegacyGraphEditorPictographContainer,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class LegacyGraphEditor(QFrame):
    main_layout: QHBoxLayout
    pictograph_layout: QVBoxLayout
    adjustment_panel_layout: QVBoxLayout
    left_stack: QStackedLayout
    right_stack: QStackedLayout
    is_toggled: bool = False
    pictograph_selected: pyqtSignal = pyqtSignal()

    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        super().__init__(sequence_workbench)
        self.sequence_workbench = sequence_workbench
        self.main_widget = sequence_workbench.main_widget

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._setup_components()
        self.layout_manager.setup_layout()
        self.hide()

    def _setup_components(self) -> None:
        self.selection_manager = ArrowSelectionManager(self)
        self.pictograph_container = LegacyGraphEditorPictographContainer(self)
        self.adjustment_panel = LegacyAdjustmentPanel(self)
        self.layout_manager = GraphEditorLayoutManager(self)
        self.toggle_tab = GraphEditorToggleTab(self)
        self.placeholder = QFrame(self)
        self.animator = GraphEditorAnimator(self)

    def get_graph_editor_height(self):
        return min(int(self.main_widget.height() // 3.5), self.width() // 4)

    def resizeEvent(self, event) -> None:
        self.graph_editor_height = self.get_graph_editor_height()
        width = self.main_widget.left_stack.width()
        self.setFixedSize(width, self.graph_editor_height)
        self.raise_()
        self.pictograph_container.GE_view.resizeEvent(event)
        for turns_box in self.adjustment_panel.turns_boxes:
            turns_box.resizeEvent(event)
        for ori_picker_box in self.adjustment_panel.ori_picker_boxes:
            ori_picker_box.resizeEvent(event)
        self.position_graph_editor()
        super().resizeEvent(event)
        self.toggle_tab.reposition_toggle_tab()

    def update_graph_editor(self) -> None:
        self.adjustment_panel.update_adjustment_panel()
        self.pictograph_container.update_pictograph()

    def position_graph_editor(self):
        if self.is_toggled:
            desired_height = self.get_graph_editor_height()
            new_width = self.sequence_workbench.width()
            new_height = desired_height
            new_x = 0
            new_y = self.sequence_workbench.height() - new_height

            self.setGeometry(new_x, new_y, new_width, new_height)
            self.raise_()
