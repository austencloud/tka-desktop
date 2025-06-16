from typing import TYPE_CHECKING
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt

from src.legacy_settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


class GraphEditorViewKeyEventHandler:
    def __init__(self, pictograph_view: "GE_PictographView") -> None:
        self.ge_view = pictograph_view
        self.pictograph = pictograph_view.pictograph
        self.graph_editor = pictograph_view.graph_editor

    def handle_key_press(self, event: QKeyEvent) -> bool:
        self.hotkey_graph_adjuster = self.ge_view.hotkey_graph_adjuster
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        key = event.key()
        selected_arrow = AppContext.get_selected_arrow()

        if selected_arrow:
            if key in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
                self.hotkey_graph_adjuster.movement_manager.handle_arrow_movement(
                    key, shift_held, ctrl_held
                )
            elif key == Qt.Key.Key_X:
                self.hotkey_graph_adjuster.rot_angle_override_manager.handle_arrow_rot_angle_override()
                self.pictograph.managers.updater.update_pictograph()
            elif key == Qt.Key.Key_Z:
                self.hotkey_graph_adjuster.entry_remover.remove_special_placement_entry(
                    self.ge_view.pictograph.state.letter,
                    arrow=AppContext.get_selected_arrow(),
                )
            else:
                return False

        if key == Qt.Key.Key_C:
            self.hotkey_graph_adjuster.prop_placement_override_manager.handle_prop_placement_override()
        return True
