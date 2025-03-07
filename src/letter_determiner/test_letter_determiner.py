import pytest
from enums.letter.letter import Letter
from letter_determiner.letter_determiner import LetterDeterminer
from main_window.main_widget.pictograph_data_loader import PictographDataLoader

# Mock BeatFrame and SequenceWorkbench
class MockBeatFrame:
    def __init__(self):
        self.get = MockBeatFrameGetter()

class MockBeatFrameGetter:
    def index_of_currently_selected_beat(self) -> int:
        # Return a fixed index for testing
        return 0  # You can adjust this value if needed

class MockSequenceWorkbench:
    def __init__(self):
        self.beat_frame = MockBeatFrame()

# Mock MainWidget for testing
class MockMainWidget:
    def __init__(self):
        self.pictograph_dataset = None
        self.json_manager = MockJsonManager()
        self.sequence_workbench = MockSequenceWorkbench()  # Add mock sequence_workbench

class MockJsonManager:
    def __init__(self):
        self.loader_saver = MockLoaderSaver()
        self.updater = MockUpdater()

class MockLoaderSaver:
    def get_json_prefloat_prop_rot_dir(self, json_index: int, color: str) -> str:
        # Mock implementation for testing
        return "clockwise"  # Default value for testing

class MockUpdater:
    def update_json_prefloat_motion_type(self, json_index: int, color: str, motion_type: str) -> None:
        pass

    def update_prefloat_prop_rot_dir_in_json(self, json_index: int, color: str, prop_rot_dir: str) -> None:
        pass

@pytest.fixture
def mock_main_widget():
    widget = MockMainWidget()
    loader = PictographDataLoader(widget)
    widget.pictograph_dataset = loader.load_pictograph_dataset()  # Load the dataset
    return widget

@pytest.fixture
def letter_determiner(mock_main_widget):
    return LetterDeterminer(mock_main_widget)

@pytest.fixture
def pictograph_dataset(mock_main_widget):
    return mock_main_widget.pictograph_dataset  # Use the dataset from the mock widget

def test_letter_determiner_with_full_dataset(letter_determiner, pictograph_dataset):
    """Test the LetterDeterminer with the entire pictograph dataset."""
    failures = []

    for letter, pictographs in pictograph_dataset.items():
        for pictograph in pictographs:
            # Determine the letter using the LetterDeterminer
            determined_letter = letter_determiner.determine_letter(pictograph)

            # Compare the determined letter to the expected letter
            if determined_letter != letter:
                failures.append((pictograph, letter, determined_letter))

    # Report results
    if failures:
        print("\nFailures:")
        for pictograph, expected_letter, actual_letter in failures:
            print(
                f"Pictograph: {pictograph}\n"
                f"Expected: {expected_letter}, Got: {actual_letter}\n"
            )
        pytest.fail(f"{len(failures)} pictographs did not match their expected letters.")
    else:
        print("All pictographs matched their expected letters.")

def test_specific_pictograph(letter_determiner, pictograph_dataset):
    """Test a specific pictograph to debug issues."""
    # Example: Test the first pictograph for letter "A"
    pictograph = pictograph_dataset[Letter.A][0]
    expected_letter = Letter.A

    determined_letter = letter_determiner.determine_letter(pictograph)
    assert determined_letter == expected_letter, (
        f"Expected {expected_letter}, got {determined_letter} for pictograph: {pictograph}"
    )