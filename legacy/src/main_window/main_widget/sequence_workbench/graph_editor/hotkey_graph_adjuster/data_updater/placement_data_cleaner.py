class PlacementDataCleaner:
    """This class iterates over all the keys in the letter data and removes any empty keys.
    It goes through each item recursively and removes any {} from keys or values."""

    @staticmethod
    def clean_placement_data(letter_data: dict) -> dict:
        for key, value in list(letter_data.items()):
            if not value:
                del letter_data[key]
            elif isinstance(value, dict):
                letter_data[key] = PlacementDataCleaner.clean_placement_data(value)
            elif isinstance(value, list):
                letter_data[key] = [
                    int(item) if isinstance(item, float) else item for item in value
                ]
            elif isinstance(value, float):
                letter_data[key] = int(value)
        return letter_data
