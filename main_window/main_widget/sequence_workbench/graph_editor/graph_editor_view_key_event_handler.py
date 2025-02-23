from typing import TYPE_CHECKING
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph_view import GE_PictographView


class GraphEditorViewKeyEventHandler:
    def __init__(self, pictograph_view: "GE_PictographView") -> None:
        self.pictograph_view = pictograph_view
        self.graph_editor = pictograph_view.graph_editor
        
    def handle_key_press(self, event: QKeyEvent) -> bool:
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        wasd_manager = self.pictograph_view.pictograph.managers.wasd_manager

        if event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            wasd_manager.movement_manager.handle_arrow_movement(
                self.pictograph_view.pictograph, event.key(), shift_held, ctrl_held
            )
            return True
        elif event.key() == Qt.Key.Key_X:
            wasd_manager.rotation_angle_override_manager.handle_rotation_angle_override()
            return True
        elif event.key() == Qt.Key.Key_Z:
            wasd_manager.entry_remover.remove_special_placement_entry(
                self.pictograph_view.pictograph.state.letter,
                arrow=self.pictograph_view.graph_editor.selection_manager.selected_arrow,
            )
            return True
        elif event.key() == Qt.Key.Key_C:
            wasd_manager.prop_placement_override_manager.handle_prop_placement_override(
                event.key()
            )
            return True
        else:
            return False
