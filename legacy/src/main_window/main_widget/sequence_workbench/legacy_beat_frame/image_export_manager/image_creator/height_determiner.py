class HeightDeterminer:
    @staticmethod
    def determine_additional_heights(
        options: dict, num_filled_beats: int, beat_scale: float
    ) -> tuple[int, int]:
        if num_filled_beats == 0:
            additional_height_top = 0
            additional_height_bottom = 55 if options.get("add_user_info", False) else 0
        elif num_filled_beats == 1:
            additional_height_top = 150 if options.get("add_word", False) else 0
            additional_height_bottom = 55 if options.get("add_user_info", False) else 0
        elif num_filled_beats == 2:
            additional_height_top = 200 if options.get("add_word", False) else 0
            additional_height_bottom = 75 if options.get("add_user_info", False) else 0
        else:
            additional_height_top = 300 if options.get("add_word", False) else 0
            additional_height_bottom = 150 if options.get("add_user_info", False) else 0
        return int(additional_height_top * beat_scale), int(
            additional_height_bottom * beat_scale
        )
