from typing import TYPE_CHECKING
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.graph_editor.graph_editor import (
        GraphEditor,
    )
    from objects.arrow.arrow import Arrow


class ArrowSelectionManager(QObject):
    selection_changed = pyqtSignal(object)

    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__()
        self.selected_arrow = None
        self.graph_editor = graph_editor

    def set_selected_arrow(self, arrow: "Arrow") -> None:
        if self.selected_arrow:
            self.selected_arrow.setSelected(False)
        self.selected_arrow = arrow
        if arrow:
            arrow.setSelected(True)
        self.selection_changed.emit(arrow)  # Notify listeners

    def clear_selection(self):
        if self.selected_arrow:
            self.selected_arrow.setSelected(False)
        self.selected_arrow = None
