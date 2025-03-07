# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING, Optional
from enums.letter.letter import Letter
from data.constants import STATIC, DASH
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import (
    ArrowRotAngleOverrideKeyGenerator,
)
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from .hotkey_graph_adjuster import HotkeyGraphAdjuster
    from objects.arrow.arrow import Arrow


class ArrowRotationOverrideCoordinator:
    """Handles high-level coordination of rotation angle overrides"""

    def __init__(self, manager: "ArrowRotAngleOverrideManager"):
        self.manager = manager

    def execute_override_flow(self) -> None:
        if not self._should_execute_override():
            return

        override_data = self.manager.data_handler.prepare_override_data()
        self.manager.data_handler.apply_rotation_override(override_data)
        self.manager.view_updater.refresh_affected_views()

    def _should_execute_override(self) -> bool:
        return self.manager.validator.is_valid_override_condition()


class RotationDataHandler:
    """Manages data operations for rotation overrides"""

    def __init__(self, manager: "ArrowRotAngleOverrideManager"):
        self.manager = manager
        self.key_generator = ArrowRotAngleOverrideKeyGenerator()

    def prepare_override_data(self) -> dict:
        return {
            "letter": self.manager.current_letter,
            "ori_key": self._generate_ori_key(),
            "turns_tuple": self.manager.turns_generator.generate_turns_tuple(
                self.manager.view.pictograph
            ),
            "rot_angle_key": self._generate_rotation_key(),
            "placement_data": AppContext.special_placement_loader().load_or_return_special_placements(),
        }

    def apply_rotation_override(self, override_data: dict) -> None:
        letter_data = self._get_letter_data(override_data)
        turn_data = letter_data.get(override_data["turns_tuple"], {})

        if override_data["rot_angle_key"] in turn_data:
            self._remove_rotation_override(override_data, turn_data)
        else:
            self._add_rotation_override(override_data, turn_data)

        self._save_updated_data(override_data, letter_data)
        self._handle_mirrored_entries(override_data, turn_data)

    def _generate_ori_key(self) -> str:
        return self.manager.data_updater.ori_key_generator.generate_ori_key_from_motion(
            AppContext.get_selected_arrow().motion
        )

    def _generate_rotation_key(self) -> str:
        return self.key_generator.generate_rotation_angle_override_key(
            AppContext.get_selected_arrow()
        )

    def _get_letter_data(self, override_data: dict) -> dict:
        return (
            override_data["placement_data"]
            .get(self.manager.view.pictograph.state.grid_mode, {})
            .get(override_data["ori_key"], {})
            .get(override_data["letter"].value, {})
        )

    def _remove_rotation_override(self, override_data: dict, turn_data: dict) -> None:
        del turn_data[override_data["rot_angle_key"]]
        self.manager.mirror_handler.handle_removal(override_data["rot_angle_key"])

    def _add_rotation_override(self, override_data: dict, turn_data: dict) -> None:
        turn_data[override_data["rot_angle_key"]] = True
        self.manager.mirror_handler.handle_addition(turn_data)

    def _save_updated_data(self, override_data: dict, letter_data: dict) -> None:
        self.manager.data_updater.update_specific_entry_in_json(
            override_data["letter"], letter_data, override_data["ori_key"]
        )

    def _handle_mirrored_entries(self, override_data: dict, turn_data: dict) -> None:
        self.manager.mirror_handler.update_mirrored_entries(
            override_data["rot_angle_key"],
            turn_data.get(override_data["rot_angle_key"], None),
        )


class RotationViewUpdater:
    """Handles UI updates related to rotation overrides"""

    def __init__(self, manager: "ArrowRotAngleOverrideManager"):
        self.manager = manager

    def refresh_affected_views(self) -> None:
        AppContext.special_placement_loader().reload()
        self._update_pictographs()

    def _update_pictographs(self) -> None:
        target_letter = self.manager.current_letter
        collector = self.manager.view.main_widget.pictograph_collector

        for pictograph in collector.collect_all_pictographs():
            if pictograph.state.letter == target_letter:
                pictograph.managers.updater.update_pictograph()
                pictograph.managers.arrow_placement_manager.update_arrow_placements()


class MirrorRotationHandler:
    """Manages mirrored entry updates for rotation overrides"""

    def __init__(self, manager: "ArrowRotAngleOverrideManager"):
        self.manager = manager

    def handle_addition(self, turn_data: dict) -> None:
        mirrored_entry_manager = self.manager.data_updater.mirrored_entry_manager
        mirrored_entry_manager.rot_angle_manager.update_rotation_angle_in_mirrored_entry(
            AppContext.get_selected_arrow(),
            turn_data,
        )

    def handle_removal(self, hybrid_key: str) -> None:
        mirrored_entry_handler = self.manager.data_updater.mirrored_entry_manager
        if mirrored_entry_handler:
            mirrored_entry_handler.rot_angle_manager.remove_rotation_angle_in_mirrored_entry(
                AppContext.get_selected_arrow(),
                hybrid_key,
            )

    def update_mirrored_entries(self, key: str, value: Optional[bool]) -> None:
        if value is not None:
            self.handle_addition({key: value})
        else:
            self.handle_removal(key)


class RotationOverrideValidator:
    """Validates conditions for rotation overrides"""

    def __init__(self, manager: "ArrowRotAngleOverrideManager"):
        self.manager = manager

    def is_valid_override_condition(self) -> bool:
        selected_arrow = AppContext.get_selected_arrow()
        return (
            selected_arrow is not None
            and selected_arrow.motion.state.motion_type in [STATIC, DASH]
        )


class ArrowRotAngleOverrideManager:
    """Main coordinator for rotation angle override functionality"""

    def __init__(self, hotkey_graph_adjuster: "HotkeyGraphAdjuster") -> None:
        self.hotkey_graph_adjuster = hotkey_graph_adjuster
        self.view = hotkey_graph_adjuster.ge_view
        self.current_letter = self.view.pictograph.state.letter

        # Initialize sub-components
        self.data_updater = self._get_data_updater()
        self.turns_generator = TurnsTupleGenerator()

        self.validator = RotationOverrideValidator(self)
        self.data_handler = RotationDataHandler(self)
        self.view_updater = RotationViewUpdater(self)
        self.mirror_handler = MirrorRotationHandler(self)
        self.coordinator = ArrowRotationOverrideCoordinator(self)

    def handle_arrow_rot_angle_override(self) -> None:
        """Main entry point for handling rotation angle overrides"""
        self.coordinator.execute_override_flow()

    def _get_data_updater(self):
        return self.view.pictograph.managers.arrow_placement_manager.data_updater

    @property
    def current_letter(self) -> Letter:
        return self.view.pictograph.state.letter

    @current_letter.setter
    def current_letter(self, value: Letter):
        self.view.pictograph.state.letter = value
