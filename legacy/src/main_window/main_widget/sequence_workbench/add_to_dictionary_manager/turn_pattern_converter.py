class TurnPatternConverter:
    def sequence_to_pattern(self, sequence: list[dict]) -> str:
        """
        Convert sequence data to a more readable turn pattern string, including tuples for differing turns.
        Format turns in a beat using just the numbers separated by a comma, and different beats using an underscore.
        """
        pattern_parts = []
        for item in sequence:
            if SEQUENCE_START_POSITION in item or "prop_type" in item:
                continue  # Skip the item with the starting position key

            blue_attributes = item[BLUE_ATTRIBUTES]
            red_attributes = item[RED_ATTRIBUTES]
            blue_turns = blue_attributes.get(TURNS, 0)
            red_turns = red_attributes.get(TURNS, 0)

            pattern_part = (
                f"{blue_turns},{red_turns}" if blue_turns or red_turns else "0"
            )
            pattern_parts.append(pattern_part)

        return "_".join(pattern_parts)
