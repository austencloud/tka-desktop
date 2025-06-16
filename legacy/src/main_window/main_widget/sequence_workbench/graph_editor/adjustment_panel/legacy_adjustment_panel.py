from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QWidget, QSizePolicy
from data.constants import BLUE, RED, IN
from .ori_picker_box.ori_picker_box import OriPickerBox
from .turns_box.turns_box import TurnsBox

if TYPE_CHECKING:
    from ..legacy_graph_editor import LegacyGraphEditor


ORI_WIDGET_INDEX = 0
TURNS_WIDGET_INDEX = 1


class LegacyAdjustmentPanel(QFrame):
    turns_boxes: list[TurnsBox]
    ori_picker_boxes: list[OriPickerBox]

    def __init__(self, graph_editor: "LegacyGraphEditor") -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.GE_pictograph = graph_editor.pictograph_container.GE_pictograph
        self.beat_frame = self.graph_editor.sequence_workbench.beat_frame
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self._initialize_ui()

    def _initialize_ui(self):
        """Initialize layout and widgets with stacked sections for turns and orientation pickers."""
        self.stacked_widget = QStackedWidget(self)

        # Create and set up the main layout without parameters
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Set margins after creation
        self.layout.setSpacing(0)  # Set spacing after creation
        self.layout.addWidget(self.stacked_widget)

        # Set the layout on this panel
        self.setLayout(self.layout)

        # Initialize and configure box pairs
        self.blue_turns_box, self.red_turns_box = TurnsBox(
            self, self.GE_pictograph, BLUE
        ), TurnsBox(self, self.GE_pictograph, RED)
        self.blue_ori_picker, self.red_ori_picker = OriPickerBox(
            self, self.GE_pictograph, BLUE
        ), OriPickerBox(self, self.GE_pictograph, RED)
        self.turns_boxes = [self.blue_turns_box, self.red_turns_box]
        self.ori_picker_boxes = [self.blue_ori_picker, self.red_ori_picker]
        for picker in (self.blue_ori_picker, self.red_ori_picker):
            picker.ori_picker_widget.clickable_ori_label.setText(IN)

        # Add box sets to stacked widget
        self.stacked_widget.addWidget(
            self._create_box_set(self.blue_turns_box, self.red_turns_box)
        )
        self.stacked_widget.addWidget(
            self._create_box_set(self.blue_ori_picker, self.red_ori_picker)
        )

    def _create_box_set(self, blue_box, red_box):
        """Creates a container with a horizontal layout for a pair of boxes."""
        box_set = QWidget(self)
        layout = QHBoxLayout(box_set)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(blue_box)
        layout.addWidget(red_box)
        return box_set

    def update_adjustment_panel(self) -> None:
        selected = self.beat_frame.get.currently_selected_beat_view()
        if selected is None or selected == self.beat_frame.start_pos_view:
            widget_index = ORI_WIDGET_INDEX
        else:
            widget_index = TURNS_WIDGET_INDEX

        self._set_current_stack_widgets(widget_index)

        if widget_index == TURNS_WIDGET_INDEX:
            self.update_turns_displays()
            self.update_rot_dir_buttons()

        elif widget_index == ORI_WIDGET_INDEX:
            self.update_ori_displays()

    def update_ori_displays(self) -> None:
        """Update the orientation displays in the orientation boxes."""
        selected_beat_view = self.beat_frame.get.currently_selected_beat_view()
        if not selected_beat_view:
            return
        blue_motion = selected_beat_view.beat.elements.blue_motion
        red_motion = selected_beat_view.beat.elements.red_motion
        for box, motion in zip(
            [self.blue_ori_picker, self.red_ori_picker], [blue_motion, red_motion]
        ):
            box.ori_picker_widget.clickable_ori_label.set_orientation(
                motion.state.end_ori
            )
            box.ori_picker_widget.ori_setter.update_current_orientation_index(
                motion.state.end_ori
            )

    def update_rot_dir_buttons(self) -> None:
        """Update the rotation direction buttons based on the current pictograph state."""
        reference_beat = self.beat_frame.get.currently_selected_beat_view()
        if reference_beat:
            blue_motion = reference_beat.beat.elements.blue_motion
            red_motion = reference_beat.beat.elements.red_motion

            blue_rot_dir = blue_motion.state.prop_rot_dir
            red_rot_dir = red_motion.state.prop_rot_dir

            self.blue_turns_box.prop_rot_dir_button_manager.logic_handler.update_button_states(
                blue_rot_dir
            )
            self.red_turns_box.prop_rot_dir_button_manager.logic_handler.update_button_states(
                red_rot_dir
            )

    def _set_current_stack_widgets(self, index):
        """Synchronize left and right stacks to the specified index."""
        for stack in [self.graph_editor.left_stack, self.graph_editor.right_stack]:
            stack.setCurrentWidget(stack.widget(index))

    def update_turns_displays(self) -> None:
        """Update the turns displays in the turns boxes."""
        selected_beat_view = self.beat_frame.get.currently_selected_beat_view()
        if not selected_beat_view:
            return
        blue_motion = selected_beat_view.beat.elements.blue_motion
        red_motion = selected_beat_view.beat.elements.red_motion
        for box, motion in zip(
            [self.blue_turns_box, self.red_turns_box], [blue_motion, red_motion]
        ):
            box.turns_widget.display_frame.update_turns_display(
                motion, motion.state.turns
            )

    def update_turns_panel(self) -> None:
        """Update the turns panel with new motion data."""
        blue_motion = self.GE_pictograph.elements.blue_motion
        red_motion = self.GE_pictograph.elements.red_motion
        self.update_turns_displays()
        [
            (
                box.header.update_turns_box_header(),
                setattr(box, "matching_motion", motion),
            )
            for box, motion in zip(
                [self.blue_turns_box, self.red_turns_box], [blue_motion, red_motion]
            )
        ]
