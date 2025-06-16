from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedLayout, QSizePolicy

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.graph_editor.legacy_graph_editor import (
        LegacyGraphEditor,
    )


class GraphEditorLayoutManager:
    def __init__(self, graph_editor: "LegacyGraphEditor") -> None:
        self.ge = graph_editor
        self.sequence_workbench = graph_editor.sequence_workbench

    def setup_layout(self) -> None:
        self._setup_main_layout()
        self.ge.pictograph_layout = self._setup_pictograph_layout()
        self.ge.adjustment_panel_layout = self._setup_adjustment_panel_layout()
        self._setup_stacks()

        # Make the pictograph container "fixed" in the middle:
        self.ge.pictograph_container.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        # You’ll still call setFixedSize(w, h) in the pictograph code (below),
        # or do it in the resize event to enforce a perfect square.

        # Add them to the main_layout with no spacing:
        self.ge.main_layout.addLayout(self.ge.left_stack, stretch=1)
        self.ge.main_layout.addLayout(self.ge.pictograph_layout, stretch=0)
        self.ge.main_layout.addLayout(self.ge.right_stack, stretch=1)

    def _setup_main_layout(self):
        self.ge.main_layout = QHBoxLayout(self.ge)
        self.ge.main_layout.setSpacing(0)
        self.ge.main_layout.setContentsMargins(0, 0, 0, 0)

    def _setup_stacks(self):
        self.ge.left_stack = QStackedLayout()
        self.ge.left_stack.addWidget(self.ge.adjustment_panel.blue_ori_picker)
        self.ge.left_stack.addWidget(self.ge.adjustment_panel.blue_turns_box)

        self.ge.right_stack = QStackedLayout()
        self.ge.right_stack.addWidget(self.ge.adjustment_panel.red_ori_picker)
        self.ge.right_stack.addWidget(self.ge.adjustment_panel.red_turns_box)

    def _setup_pictograph_layout(self) -> None:
        pictograph_layout = QVBoxLayout()
        pictograph_layout.addWidget(self.ge.pictograph_container)
        pictograph_layout.setContentsMargins(0, 0, 0, 0)
        pictograph_layout.setSpacing(0)
        return pictograph_layout

    def _setup_adjustment_panel_layout(self) -> None:
        adjustment_panel_layout = QVBoxLayout()
        adjustment_panel_layout.addWidget(self.ge.adjustment_panel)
        adjustment_panel_layout.setContentsMargins(0, 0, 0, 0)
        adjustment_panel_layout.setSpacing(0)
        return adjustment_panel_layout
