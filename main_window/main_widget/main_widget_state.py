from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetState:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def load_state(self):
        current_sequence = (
            self.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        if len(current_sequence) > 1:
            self.main_widget.sequence_widget.beat_frame.populator.populate_beat_frame_from_json(
                current_sequence
            )
        left_stack = self.main_widget.left_stack
        right_stack = self.main_widget.right_stack

        total_width = self.main_widget.width()
        left_width = int(total_width * 0.5)
        left_stack.setFixedWidth(left_width)
        right_stack.setFixedWidth(total_width - left_width)
