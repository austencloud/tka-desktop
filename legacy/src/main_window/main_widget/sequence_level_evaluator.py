from data.constants import BLUE_ATTRS, IN, OUT, RED_ATTRS, START_ORI, END_ORI, TURNS


class SequenceLevelEvaluator:
    def get_sequence_difficulty_level(self, sequence: list[dict]) -> int:
        if len(sequence) < 3:
            return ""
        has_non_radial_orientation = False
        has_turns = False

        for entry in sequence[1:]:  # Skip the first entry with metadata
            if entry.get("is_placeholder", False):
                continue
            if self._has_non_radial_orientation(entry):
                has_non_radial_orientation = True
            if self._has_turns(entry):
                has_turns = True

        if has_non_radial_orientation:
            return 3  # Level 3: Contains non-radial orientations
        elif has_turns:
            return 2  # Level 2: Contains turns
        else:
            return 1  # Level 1: No turns, only radial orientations

    def _has_turns(self, entry: dict) -> bool:
        has_turns = False
        if entry[BLUE_ATTRS][TURNS] != "fl" and entry[RED_ATTRS][TURNS] != "fl":
            has_turns = entry[BLUE_ATTRS][TURNS] > 0 or entry[RED_ATTRS][TURNS] > 0
        else:
            if entry[BLUE_ATTRS][TURNS] == "fl":
                if entry[RED_ATTRS][TURNS] == "fl":
                    has_turns = False
                if entry[RED_ATTRS][TURNS] != "fl":
                    has_turns = entry[RED_ATTRS][TURNS] > 0
            if entry[RED_ATTRS][TURNS] == "fl":
                if entry[BLUE_ATTRS][TURNS] == "fl":
                    has_turns = False
                if entry[BLUE_ATTRS][TURNS] != "fl":
                    has_turns = entry[BLUE_ATTRS][TURNS] > 0
        return has_turns

    def _has_non_radial_orientation(self, entry: dict) -> bool:
        self.RADIAL_ORIENTATIONS = {IN, OUT}
        blue_start_ori = entry[BLUE_ATTRS][START_ORI]
        blue_end_ori = entry[BLUE_ATTRS][END_ORI]
        red_start_ori = entry[RED_ATTRS][START_ORI]
        red_end_ori = entry[RED_ATTRS][END_ORI]
        return (
            blue_start_ori not in self.RADIAL_ORIENTATIONS
            or blue_end_ori not in self.RADIAL_ORIENTATIONS
            or red_start_ori not in self.RADIAL_ORIENTATIONS
            or red_end_ori not in self.RADIAL_ORIENTATIONS
        )
