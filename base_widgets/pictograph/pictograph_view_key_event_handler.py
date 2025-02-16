from typing import TYPE_CHECKING
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_view import PictographView


class PictographViewKeyEventHandler:
    def __init__(self, pictograph_view: "PictographView") -> None:
        self.pictograph_view = pictograph_view
        # self.pictograph = pictograph_view.pictograph

    def handle_key_press(self, event: QKeyEvent) -> bool:
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        wasd_manager = self.pictograph_view.pictograph.wasd_manager

        if event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            wasd_manager.movement_manager.handle_arrow_movement(
                self.pictograph_view.pictograph, event.key(), shift_held, ctrl_held
            )
            return True
        elif event.key() == Qt.Key.Key_X:
            wasd_manager.rotation_angle_override_manager.handle_rotation_angle_override()
            return True
        elif event.key() == Qt.Key.Key_Z:
            wasd_manager.handle_special_placement_removal()
            return True
        elif event.key() == Qt.Key.Key_Q or event.key() == Qt.Key.Key_F5:
            self.pictograph_view.pictograph.main_widget.special_placement_loader.refresh_placements()
            return True
        elif event.key() == Qt.Key.Key_C:
            wasd_manager.prop_placement_override_manager.handle_prop_placement_override(
                event.key()
            )
            return True
        else:
            return False
