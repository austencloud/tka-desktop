# ==========================================
# File: prop_rot_dir_logic_handler.py
# ==========================================
from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal
from data.constants import ANTI, CLOCKWISE, PRO
from objects.motion.motion import Motion
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from utils.reversal_detector import ReversalDetector

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_ui_handler import (
        PropRotDirUIHandler,
    )
    from ..turns_box import TurnsBox


class PropRotDirLogicHandler(QObject):
    rotation_updated = pyqtSignal(dict)

    def __init__(
        self, turns_box: "TurnsBox", ui_handler: "PropRotDirUIHandler"
    ) -> None:
        super().__init__()
        self.turns_box = turns_box
        self.ui_handler = ui_handler
        self.current_motion: "Motion" = None

    def validate_rotation_change(self, new_direction: str) -> bool:
        """Check if rotation change is valid."""
        return (
            not self.turns_box.prop_rot_dir_btn_state[new_direction]
            and self.current_motion is not None
        )

    def update_rotation_states(self, new_direction: str) -> None:
        """Update all related states for rotation change."""
        self.update_button_states(new_direction)
        self._update_motion_properties(new_direction)
        self._update_pictograph_data()
        self._detect_reversals()
        self.update_related_components()

        # Refresh UI elements with graceful fallbacks
        self._refresh_construct_tab_options()

    def update_button_states(self, direction: str) -> None:
        """✅ Update button states in TurnsBoxHeader instead of missing `ui_handler`."""
        self.turns_box.prop_rot_dir_button_manager.state.update_state(direction, True)

        # ✅ Update the buttons inside the TurnsBoxHeader
        header = self.turns_box.header
        if direction == CLOCKWISE:
            header.cw_button.set_selected(True)
            header.ccw_button.set_selected(False)
        else:
            header.ccw_button.set_selected(True)
            header.cw_button.set_selected(False)

    def _update_motion_properties(self, direction: str) -> None:
        """Update motion objects with new rotation direction."""
        for pictograph in self._get_affected_pictographs():
            motion = pictograph.managers.get.motion_by_color(self.turns_box.color)
            motion.state.prop_rot_dir = direction
            motion.state.motion_type = self._determine_motion_type(motion)

        # Update pictographs & JSON
        self.turns_box.graph_editor.sequence_workbench.beat_frame.updater.update_beats_from_current_sequence_json()
        self.turns_box.graph_editor.main_widget.json_manager.ori_validation_engine.run(
            is_current_sequence=True
        )

    def _update_pictograph_data(self) -> None:
        """Update pictograph JSON data after a rotation change."""
        pictograph_index = (
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
        )
        json_index = pictograph_index + 2  # JSON stores additional metadata

        json_updater = self.turns_box.graph_editor.main_widget.json_manager.updater

        for pictograph in self._get_affected_pictographs():
            motion = pictograph.managers.get.motion_by_color(self.turns_box.color)
            new_data = {
                "motion_type": motion.state.motion_type,
                "prop_rot_dir": motion.state.prop_rot_dir,
                "end_ori": motion.state.end_ori,
                "turns": motion.state.turns,
            }
            pictograph.state.pictograph_data[motion.state.color + "_attributes"].update(
                new_data
            )
            pictograph.managers.updater.update_pictograph(
                pictograph.state.pictograph_data
            )

            # Sync changes with JSON
            json_updater.motion_type_updater.update_motion_type_in_json(
                json_index, motion.state.color, motion.state.motion_type
            )
            json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                json_index, motion.state.color, motion.state.prop_rot_dir
            )

    def _detect_reversals(self) -> None:
        """Detect motion reversals and update pictograph UI accordingly."""
        pictograph_index = (
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
        )
        sequence_so_far = self.turns_box.graph_editor.main_widget.json_manager.loader_saver.load_current_sequence()[
            : pictograph_index + 2
        ]

        for pictograph in self._get_affected_pictographs():
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, pictograph.state.pictograph_data
            )

            pictograph.state.blue_reversal = reversal_info["blue_reversal"]
            pictograph.state.red_reversal = reversal_info["red_reversal"]

            # Update UI with reversal symbols
            pictograph.elements.reversal_glyph.update_reversal_symbols()

    def _get_affected_pictographs(self) -> list[LegacyPictograph]:
        """Retrieve pictographs that need updating due to rotation changes."""
        selected_beat = (
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.currently_selected_beat_view()
        )
        if not selected_beat:
            return []

        return [
            selected_beat.beat,
            self.turns_box.graph_editor.pictograph_container.GE_view.pictograph,
        ]

    def _determine_motion_type(self, motion: "Motion") -> str:
        """Determine new motion type based on rotation."""
        if motion.state.motion_type == ANTI:
            return PRO
        elif motion.state.motion_type == PRO:
            return ANTI
        return motion.state.motion_type

    def _get_default_prop_rot_dir(self) -> str:
        """Set default prop rotation direction to clockwise."""
        self.turns_box.prop_rot_dir_button_manager.state.update_state(CLOCKWISE, True)
        return CLOCKWISE

    def update_related_components(self) -> None:
        """Updates JSON, detects reversals, updates UI labels, and ensures UI consistency."""
        pictograph_index = (
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
        )
        json_index = pictograph_index + 2  # JSON stores additional metadata

        # Update JSON data
        json_updater = self.turns_box.graph_editor.main_widget.json_manager.updater

        for pictograph in self._get_affected_pictographs():
            motion = pictograph.managers.get.motion_by_color(self.turns_box.color)
            new_data = {
                "motion_type": motion.state.motion_type,
                "prop_rot_dir": motion.state.prop_rot_dir,
                "end_ori": motion.state.end_ori,
                "turns": motion.state.turns,
            }
            pictograph.state.pictograph_data[motion.state.color + "_attributes"].update(
                new_data
            )
            pictograph.managers.updater.update_pictograph(
                pictograph.state.pictograph_data
            )

            # Sync changes with JSON
            json_updater.motion_type_updater.update_motion_type_in_json(
                json_index, motion.state.color, motion.state.motion_type
            )
            json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                json_index, motion.state.color, motion.state.prop_rot_dir
            )

        # Run orientation validation
        self.turns_box.graph_editor.main_widget.json_manager.ori_validation_engine.run(
            is_current_sequence=True
        )

        # Detect reversals
        self._detect_reversals()

        # Update UI labels and letters
        self.turns_box.graph_editor.sequence_workbench.beat_frame.updater.update_beats_from_current_sequence_json()
        self.turns_box.graph_editor.main_widget.sequence_workbench.current_word_label.set_current_word(
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.current_word()
        )

        # Update the letter for all affected pictographs
        for pictograph in self._get_affected_pictographs():
            self.turns_box.prop_rot_dir_button_manager.update_pictograph_letter(
                pictograph
            )

    def _refresh_construct_tab_options(self) -> None:
        """Refresh construct tab options using the new MVVM architecture with graceful fallbacks."""
        try:
            # Try to get construct tab through the new coordinator pattern
            main_widget = self.turns_box.graph_editor.sequence_workbench.main_widget
            construct_tab = main_widget.get_tab_widget("construct")
            if (
                construct_tab
                and hasattr(construct_tab, "option_picker")
                and hasattr(construct_tab.option_picker, "updater")
            ):
                construct_tab.option_picker.updater.refresh_options()
                return
        except AttributeError:
            pass

        try:
            # Fallback: try through tab_manager for backward compatibility
            main_widget = self.turns_box.graph_editor.sequence_workbench.main_widget
            construct_tab = main_widget.tab_manager.get_tab_widget("construct")
            if (
                construct_tab
                and hasattr(construct_tab, "option_picker")
                and hasattr(construct_tab.option_picker, "updater")
            ):
                construct_tab.option_picker.updater.refresh_options()
                return
        except AttributeError:
            pass

        try:
            # Final fallback: try direct access for legacy compatibility
            main_widget = self.turns_box.graph_editor.sequence_workbench.main_widget
            if hasattr(main_widget, "construct_tab"):
                construct_tab = main_widget.construct_tab
                if hasattr(construct_tab, "option_picker") and hasattr(
                    construct_tab.option_picker, "updater"
                ):
                    construct_tab.option_picker.updater.refresh_options()
                    return
        except AttributeError:
            pass

        # If all else fails, log a warning but don't crash
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(
            "Could not refresh construct tab options - construct tab not available"
        )
