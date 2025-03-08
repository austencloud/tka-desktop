from data.constants import CLOCKWISE


class MockBeatFrame:
    def __init__(self):
        self.get = MockBeatFrameGetter()


class MockBeatFrameGetter:
    def index_of_currently_selected_beat(self) -> int:
        return 0


class MockSequenceWorkbench:
    def __init__(self):
        self.beat_frame = MockBeatFrame()


class MockJsonManager:
    def __init__(self):
        self.loader_saver = MockLoaderSaver()
        self.updater = MockUpdater()


class MockLoaderSaver:
    def get_json_prefloat_prop_rot_dir(self, json_index: int, color: str) -> str:
        return CLOCKWISE


class MockstrUpdater:
    def update_json_prefloat_motion_type(self, *args, **kwargs):
        pass


class MockPropRotDirUpdater:
    def update_prefloat_prop_rot_dir_in_json(self, *args, **kwargs):
        pass


class MockUpdater:
    def __init__(self):
        self.motion_type_updater = MockstrUpdater()
        self.prop_rot_dir_updater = MockPropRotDirUpdater()


class MockMainWidget:
    def __init__(self):
        self.pictograph_dataset = None
        self.json_manager = MockJsonManager()
        self.sequence_workbench = MockSequenceWorkbench()
