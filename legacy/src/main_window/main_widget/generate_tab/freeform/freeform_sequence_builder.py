from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
import random
from copy import deepcopy
from PyQt6.QtCore import Qt
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, LETTER
from ..base_sequence_builder import BaseSequenceBuilder
from ..turn_intensity_manager import TurnIntensityManager

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class FreeFormSequenceBuilder(BaseSequenceBuilder):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__(generate_tab)
        self.generate_tab = generate_tab

    def build_sequence(
        self,
        length: int,
        turn_intensity: int,
        level: int,
        prop_continuity: str = "continuous",
    ):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.initialize_sequence(length)

        if prop_continuity == "continuous":
            blue_rot_dir = random.choice([CLOCKWISE, COUNTER_CLOCKWISE])
            red_rot_dir = random.choice([CLOCKWISE, COUNTER_CLOCKWISE])
        elif prop_continuity == "random":
            blue_rot_dir = None
            red_rot_dir = None

        length_of_sequence_upon_start = len(self.sequence) - 2

        turn_manager = TurnIntensityManager(length, level, turn_intensity)
        turns_blue, turns_red = turn_manager.allocate_turns_for_blue_and_red()

        for i in range(length - length_of_sequence_upon_start):
            next_pictograph = self._generate_next_pictograph(
                level,
                turns_blue[i],
                turns_red[i],
                prop_continuity,
                blue_rot_dir,
                red_rot_dir,
            )
            self.sequence.append(next_pictograph)
            self.sequence_workbench.beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                next_pictograph,
                override_grow_sequence=True,
                update_image_export_preview=False,
            )
            QApplication.processEvents()

        self._update_construct_tab_options()

        QApplication.restoreOverrideCursor()

    def _generate_next_pictograph(
        self,
        level: int,
        turn_blue: float,
        turn_red: float,
        prop_continuity: str,
        blue_rot_dir: str,
        red_rot_dir: str,
    ):

        option_dicts = self._get_option_dicts()
        option_dicts = [deepcopy(option) for option in option_dicts]

        option_dicts = self._filter_options_by_letter_type(option_dicts)

        if prop_continuity == "continuous":
            option_dicts = self.filter_options_by_rotation(
                option_dicts, blue_rot_dir, red_rot_dir
            )

        last_beat = self.sequence[-1]
        next_beat = random.choice(option_dicts)

        if level == 2 or level == 3:
            next_beat = self.set_turns(next_beat, turn_blue, turn_red)

        self.update_start_orientations(next_beat, last_beat)
        self.update_dash_static_prop_rot_dirs(
            next_beat, prop_continuity, blue_rot_dir, red_rot_dir
        )
        self.update_end_orientations(next_beat)
        next_beat = self.update_beat_number(next_beat, self.sequence)
        return next_beat

    def _get_option_dicts(self) -> list[dict]:
        construct_tab = self._ensure_construct_tab_available()
        if not construct_tab or not hasattr(construct_tab, "option_picker"):
            raise RuntimeError(
                "Construct tab and option picker must be available for sequence generation"
            )

        return construct_tab.option_picker.option_getter._load_all_next_option_dicts(
            self.sequence
        )

    def _ensure_construct_tab_available(self):
        """Ensure construct tab is created and available before using it."""
        construct_tab = self.main_widget.get_tab_widget("construct")
        if construct_tab:
            return construct_tab

        construct_tab = getattr(self.main_widget, "construct_tab", None)
        if construct_tab:
            return construct_tab

        if hasattr(self.main_widget, "tab_manager"):
            construct_tab = self.main_widget.tab_manager.create_tab("construct")
            if construct_tab:
                return construct_tab

        raise RuntimeError(
            "Unable to create or access construct tab - sequence generation requires construct tab dependencies"
        )

    def _filter_options_by_letter_type(self, options: list[dict]) -> list[dict]:
        """Filter options based on selected letter types."""
        selected_types = self.generate_tab.letter_picker.get_selected_letter_types()
        selected_letters = []
        for letter_type in selected_types:
            selected_letters.extend(letter_type.letters)

        filtered_options = [
            option for option in options if option[LETTER] in selected_letters
        ]
        return filtered_options

    def _update_construct_tab_options(self):
        """Update construct tab options using the new MVVM architecture with graceful fallbacks."""
        try:
            # Try to get construct tab through the new coordinator pattern
            construct_tab = self.main_widget.get_tab_widget("construct")
            if (
                construct_tab
                and hasattr(construct_tab, "option_picker")
                and hasattr(construct_tab.option_picker, "updater")
            ):
                construct_tab.option_picker.updater.update_options()
                return
        except AttributeError:
            pass

        try:
            # Fallback: try through tab_manager for backward compatibility
            construct_tab = self.main_widget.tab_manager.get_tab_widget("construct")
            if (
                construct_tab
                and hasattr(construct_tab, "option_picker")
                and hasattr(construct_tab.option_picker, "updater")
            ):
                construct_tab.option_picker.updater.update_options()
                return
        except AttributeError:
            pass

        try:
            # Final fallback: try direct access for legacy compatibility
            if hasattr(self.main_widget, "construct_tab"):
                construct_tab = self.main_widget.construct_tab
                if hasattr(construct_tab, "option_picker") and hasattr(
                    construct_tab.option_picker, "updater"
                ):
                    construct_tab.option_picker.updater.update_options()
                    return
        except AttributeError:
            pass

        # If all else fails, log a warning but don't crash
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(
            "Could not update construct tab options - construct tab not available"
        )
