class ReversalDetector:
    @staticmethod
    def detect_reversal(sequence_so_far: list, current_beat_data: dict):
        """
        Detects reversals between the last valid prop_rot_dir in the sequence and the current beat.
        """
        reversal_info = {"blue_reversal": False, "red_reversal": False}

        for color in ["blue_attributes", "red_attributes"]:
            last_prop_rot_dir = ReversalDetector._get_last_valid_prop_rot_dir(
                sequence_so_far, color
            )
            curr_prop_rot_dir = current_beat_data.get(color, {}).get("prop_rot_dir")

            # For 'no_rot' or None, use last known direction
            if curr_prop_rot_dir == "no_rot" or curr_prop_rot_dir is None:
                curr_prop_rot_dir = last_prop_rot_dir

            # If still None, consider continuous
            if last_prop_rot_dir is None or curr_prop_rot_dir is None:
                continue  # No reversal

            if curr_prop_rot_dir != last_prop_rot_dir:
                reversal_info[f'{color.split("_")[0]}_reversal'] = True

        return reversal_info

    @staticmethod
    def _get_last_valid_prop_rot_dir(sequence: list, color: str) -> str:
        """
        Traverse the sequence backward to find the last valid prop_rot_dir for the given color.
        """
        for beat_data in reversed(sequence):
            prop_rot_dir = beat_data.get(color, {}).get("prop_rot_dir")
            if prop_rot_dir and prop_rot_dir != "no_rot":
                return prop_rot_dir
        return None  # No valid previous direction found
