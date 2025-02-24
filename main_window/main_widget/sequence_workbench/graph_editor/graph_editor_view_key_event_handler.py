from typing import TYPE_CHECKING
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt

from main_window.settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


class GraphEditorViewKeyEventHandler:
    def __init__(self, pictograph_view: "GE_PictographView") -> None:
        self.pictograph_view = pictograph_view
        self.pictograph = pictograph_view.pictograph
        self.graph_editor = pictograph_view.graph_editor
        self.wasd_manager = self.pictograph_view.pictograph.managers.wasd_manager

    def handle_key_press(self, event: QKeyEvent) -> bool:
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        key = event.key()

        if key in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            self.wasd_manager.movement_manager.handle_arrow_movement(
                self.pictograph_view.pictograph, key, shift_held, ctrl_held
            )
        elif key == Qt.Key.Key_X:
            self.wasd_manager.rotation_angle_override_manager.handle_arrow_rot_angle_override()
            # update arrow placements after rotation
            self.pictograph.managers.updater.update_pictograph()
        elif key == Qt.Key.Key_Z:
            self.wasd_manager.entry_remover.remove_special_placement_entry(
                self.pictograph_view.pictograph.state.letter,
                arrow=AppContext.get_selected_arrow(),
            )
        elif key == Qt.Key.Key_C:
            self.wasd_manager.prop_placement_override_manager.handle_prop_placement_override(
                key
            )
        else:
            return False

        for (
            pictograph
        ) in self.pictograph.main_widget.pictograph_collector.collect_all_pictographs():
            pictograph.managers.arrow_placement_manager.update_arrow_placements()

        return True
