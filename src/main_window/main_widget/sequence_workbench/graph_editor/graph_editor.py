# graph_editor.py (modification)
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QStackedLayout,
)
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_workbench.graph_editor.graph_editor_animator import (
    GraphEditorAnimator,
)
from main_window.main_widget.sequence_workbench.graph_editor.graph_editor_toggle_tab import (
    GraphEditorToggleTab,
)
from main_window.main_widget.sequence_workbench.graph_editor.graph_editor_state import (
    GraphEditorState,
)
from settings_manager.settings_manager import pyqtSignal

from .arrow_selection_manager import ArrowSelectionManager
from .graph_editor_layout_manager import GraphEditorLayoutManager
from .adjustment_panel.beat_adjustment_panel import BeatAdjustmentPanel
from .pictograph_container.GE_pictograph_container import GraphEditorPictographContainer

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class GraphEditor(QFrame):
    main_layout: QHBoxLayout
    pictograph_layout: QVBoxLayout
    adjustment_panel_layout: QVBoxLayout
    left_stack: QStackedLayout
    right_stack: QStackedLayout
    is_toggled: bool = False
    pictograph_selected: pyqtSignal = pyqtSignal()

    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        super().__init__(sequence_workbench)
        self.sequence_workbench = sequence_workbench
        self.main_widget = sequence_workbench.main_widget

        # Initialize state before components
        self.state = GraphEditorState()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._setup_components()
        self.layout_manager.setup_layout()

        # Connect state change signals
        self._connect_state_signals()

        self.hide()

    def _setup_components(self) -> None:
        self.selection_manager = ArrowSelectionManager(self)
        self.pictograph_container = GraphEditorPictographContainer(self)
        self.adjustment_panel = BeatAdjustmentPanel(self)
        self.layout_manager = GraphEditorLayoutManager(self)
        self.toggle_tab = GraphEditorToggleTab(self)
        self.placeholder = QFrame(self)
        self.animator = GraphEditorAnimator(self)

    def _connect_state_signals(self) -> None:
        """Connect state change signals to component handlers"""
        # Connect turns changes
        self.state.turns_changed.connect(self._handle_turns_changed)
        self.state.orientation_changed.connect(self._handle_orientation_changed)
        self.state.prop_rot_dir_changed.connect(self._handle_prop_rot_dir_changed)
        self.state.motion_type_changed.connect(self._handle_motion_type_changed)
        self.state.letter_changed.connect(self._handle_letter_changed)
        self.state.selected_arrow_changed.connect(self._handle_arrow_selection_changed)

        # Connect back from selection manager
        self.selection_manager.selection_changed.connect(self.state.set_selected_arrow)

    def _handle_turns_changed(self, color, value):
        """Handle turns changes in state"""
        # Update the turns box display
        if color == "blue":
            self.adjustment_panel.blue_turns_box.turns_widget.display_frame.update_turns_display(
                self.pictograph_container.GE_pictograph.elements.blue_motion, value
            )
        else:
            self.adjustment_panel.red_turns_box.turns_widget.display_frame.update_turns_display(
                self.pictograph_container.GE_pictograph.elements.red_motion, value
            )

    def _handle_orientation_changed(self, color, orientation):
        """Handle orientation changes in state"""
        if color == "blue":
            self.adjustment_panel.blue_ori_picker.ori_picker_widget.clickable_ori_label.set_orientation(
                orientation
            )
        else:
            self.adjustment_panel.red_ori_picker.ori_picker_widget.clickable_ori_label.set_orientation(
                orientation
            )

    def _handle_prop_rot_dir_changed(self, color, direction):
        """Handle prop rotation direction changes in state"""
        if color == "blue":
            self.adjustment_panel.blue_turns_box.prop_rot_dir_button_manager.update_buttons_for_prop_rot_dir(
                direction
            )
        else:
            self.adjustment_panel.red_turns_box.prop_rot_dir_button_manager.update_buttons_for_prop_rot_dir(
                direction
            )

    def _handle_motion_type_changed(self, color, motion_type):
        """Handle motion type changes in state"""
        if color == "blue":
            self.adjustment_panel.blue_turns_box.turns_widget.motion_type_label.update_display(
                motion_type
            )
        else:
            self.adjustment_panel.red_turns_box.turns_widget.motion_type_label.update_display(
                motion_type
            )

    def _handle_letter_changed(self, letter):
        """Handle letter changes in state"""
        # Update any letter-dependent components
        self.pictograph_container.GE_view.pictograph.state.letter = letter

    def _handle_arrow_selection_changed(self, arrow):
        """Handle arrow selection changes in state"""
        # Update UI to reflect selected arrow
        self.pictograph_container.GE_view.update()

    def get_graph_editor_height(self):
        return min(int(self.main_widget.height() // 3.5), self.width() // 4)

    def resizeEvent(self, event) -> None:
        self.graph_editor_height = self.get_graph_editor_height()
        width = self.main_widget.left_stack.width()
        self.setFixedSize(width, self.graph_editor_height)
        self.raise_()
        self.pictograph_container.GE_view.resizeEvent(event)
        for turns_box in self.adjustment_panel.turns_boxes:
            turns_box.resizeEvent(event)
        for ori_picker_box in self.adjustment_panel.ori_picker_boxes:
            ori_picker_box.resizeEvent(event)
        self.position_graph_editor()
        super().resizeEvent(event)
        self.toggle_tab.reposition_toggle_tab()

    def update_graph_editor(self) -> None:
        # Update state from current pictograph first
        self.state.sync_from_pictograph(self.pictograph_container.GE_view.pictograph)

        # Then update UI components
        self.adjustment_panel.update_adjustment_panel()
        self.pictograph_container.update_pictograph()

    def position_graph_editor(self):
        if self.is_toggled:
            desired_height = self.get_graph_editor_height()
            new_width = self.sequence_workbench.width()
            new_height = desired_height
            new_x = 0
            new_y = self.sequence_workbench.height() - new_height

            self.setGeometry(new_x, new_y, new_width, new_height)
            self.raise_()
