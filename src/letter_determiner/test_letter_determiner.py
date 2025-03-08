# import pytest
# from dataclasses import dataclass
# from data.constants import (
#     ANTI,
#     BLUE_ATTRS,
#     CLOCKWISE,
#     COUNTER_CLOCKWISE,
#     EAST,
#     END_LOC,
#     FLOAT,
#     MOTION_TYPE,
#     NO_ROT,
#     NORTH,
#     NORTHEAST,
#     NORTHWEST,
#     PREFLOAT_MOTION_TYPE,
#     PREFLOAT_PROP_ROT_DIR,
#     PRO,
#     PROP_ROT_DIR,
#     RED_ATTRS,
#     SOUTH,
#     START_LOC,
#     WEST,
# )
# from enums.letter.letter import Letter
# from letter_determiner.letter_determiner import LetterDeterminer
# from main_window.main_widget.pictograph_data_loader import PictographDataLoader


# class MockBeatFrame:
#     def __init__(self):
#         self.get = MockBeatFrameGetter()


# class MockBeatFrameGetter:
#     def index_of_currently_selected_beat(self) -> int:
#         return 0


# class MockSequenceWorkbench:
#     def __init__(self):
#         self.beat_frame = MockBeatFrame()


# class MockMainWidget:
#     def __init__(self):
#         self.pictograph_dataset = None
#         self.json_manager = MockJsonManager()
#         self.sequence_workbench = MockSequenceWorkbench()


# class MockJsonManager:
#     def __init__(self):
#         self.loader_saver = MockLoaderSaver()
#         self.updater = MockUpdater()


# class MockLoaderSaver:
#     def get_json_prefloat_prop_rot_dir(self, json_index: int, color: str) -> str:
#         return CLOCKWISE


# class MockUpdater:
#     def update_json_prefloat_motion_type(
#         self, json_index: int, color: str, motion_type: str
#     ) -> None:
#         pass

#     def update_prefloat_prop_rot_dir_in_json(
#         self, json_index: int, color: str, prop_rot_dir: str
#     ) -> None:
#         pass


# @pytest.fixture
# def mock_main_widget():
#     widget = MockMainWidget()
#     loader = PictographDataLoader(widget)
#     widget.pictograph_dataset = loader.load_pictograph_dataset()
#     return widget


# @pytest.fixture
# def letter_determiner(mock_main_widget):
#     return LetterDeterminer(mock_main_widget)


# @pytest.fixture
# def pictograph_dataset(mock_main_widget):
#     return mock_main_widget.pictograph_dataset


# def test_specific_pictograph(letter_determiner, pictograph_dataset):
#     pictograph = pictograph_dataset[Letter.A][0]
#     expected_letter = Letter.A
#     determined_letter = letter_determiner.determine_letter(pictograph)
#     assert (
#         determined_letter == expected_letter
#     ), f"Expected {expected_letter}, got {determined_letter} for pictograph: {pictograph}"


# @dataclass
# class MotionCase:
#     input_data: dict
#     expected_letter: Letter
#     description: str


# TEST_CASES = [
#     MotionCase(
#         input_data={
#             BLUE_ATTRS: {
#                 MOTION_TYPE: ANTI,
#                 START_LOC: SOUTH,
#                 END_LOC: WEST,
#                 PROP_ROT_DIR: COUNTER_CLOCKWISE,
#             },
#             RED_ATTRS: {
#                 MOTION_TYPE: FLOAT,
#                 START_LOC: NORTH,
#                 END_LOC: EAST,
#                 PROP_ROT_DIR: NO_ROT,
#                 PREFLOAT_MOTION_TYPE: PRO,
#                 PREFLOAT_PROP_ROT_DIR: CLOCKWISE,
#             },
#         },
#         expected_letter=Letter.B,
#         description="Pro motion with mirrored float pre-float",
#     )
# ]
