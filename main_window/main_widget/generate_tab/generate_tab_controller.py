from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .generate_tab import GenerateTab


class GenerateTabController:
    def __init__(self, parent_tab: "GenerateTab"):
        self.tab = parent_tab
        self.settings = parent_tab.settings
        self.current_mode = "freeform"

    def init_from_settings(self):
        saved_mode = self.settings.get_setting("generator_mode", "global") or "freeform"
        if saved_mode not in ["freeform", "circular"]:
            saved_mode = "freeform"
        self.current_mode = saved_mode

        self.tab.mode_toggle.set_state(self.current_mode == "circular")

        self._apply_unified_settings()

        if self.current_mode == "circular":
            self._load_circular_settings()
        else:
            self._load_freeform_settings()

        self._update_ui_visibility()

    def on_mode_changed(self, new_mode: str):
        self.current_mode = new_mode
        self.settings.set_setting("generator_mode", new_mode, "global")
        self._update_ui_visibility()

    def handle_generate_sequence(self, overwrite: bool):
        if overwrite:
            self.tab.main_widget.sequence_workbench.sequence_beat_frame.sequence_workbench.beat_deleter.reset_widgets(
                False
            )

        length = int(self.settings.get_setting("length") or 16)
        intensity = (
            float(self.settings.get_setting("turn_intensity"))
            if self.settings.get_setting("turn_intensity") in ["0.5", "1.5", "2.5"]
            else int(self.settings.get_setting("turn_intensity") or 1)
        )
        level = int(self.settings.get_setting("level") or 1)
        prop_continuity = self.settings.get_setting("prop_continuity")

        if self.current_mode == "freeform":
            self.tab.freeform_builder.build_sequence(
                length, intensity, level, prop_continuity
            )
        else:
            rotation_type = self.settings.get_setting("rotation_type") or "halved"
            permutation_type = (
                self.settings.get_setting("permutation_type") or "rotated"
            )

            self.tab.circular_builder.build_sequence(
                length,
                intensity,
                level,
                rotation_type,
                permutation_type,
                prop_continuity,
            )

    def _apply_unified_settings(self):
        seq_level = self.settings.get_setting("sequence_level") or 1
        seq_length = self.settings.get_setting("length") or 16
        turn_intensity = self.settings.get_setting("max_turn_intensity") or 1
        cont_rot = self.settings.get_setting("prop_continuity") or "continuous"
        self.tab.level_selector.set_level(int(seq_level))
        self.tab.length_adjuster.set_length(int(seq_length))
        self.tab.turn_intensity.set_intensity(turn_intensity)
        self.tab.prop_continuity_toggle.set_state(cont_rot == "continuous")
        self.tab.slice_size_toggle.set_state(
            self.settings.get_setting("rotation_type") == "quartered"
        )
        self.tab.permutation_type_toggle.set_state(
            self.settings.get_setting("permutation_type") == "rotated"
        )
        current_sequence_length = (
            len(self.tab.main_widget.json_manager.loader_saver.load_current_sequence())
            - 1
        )
        self.tab.auto_complete_button.setEnabled(int(current_sequence_length) > 1)

    def _load_circular_settings(self):
        rotation_type = self.settings.get_setting("rotation_type", "circular")
        if rotation_type:
            self.tab.slice_size_toggle.set_state(rotation_type == "quartered")

        permutation_type = self.settings.get_setting("permutation_type", "circular")
        if permutation_type:
            self.tab.permutation_type_toggle.set_state(permutation_type == "rotated")

    def _load_freeform_settings(self):
        letter_types = self.settings.get_setting("selected_letter_types", "freeform")
        if letter_types:
            self.tab.letter_picker.set_selected_types(letter_types)

    def _update_ui_visibility(self):
        is_freeform = self.current_mode == "freeform"
        self.tab.letter_picker.setVisible(is_freeform)
        self.tab.slice_size_toggle.setVisible(not is_freeform)
        self.tab.permutation_type_toggle.setVisible(not is_freeform)

    def _as_bool(self, val) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.lower() == "true"
        return False
