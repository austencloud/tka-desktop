from ...turns_adjustment_manager.json_turns_repository import JsonTurnsRepository
from ...turns_adjustment_manager.motion_type_setter import MotionTypeSetter
from ...turns_adjustment_manager.turns_adjustment_manager import (
from ...turns_adjustment_manager.turns_presenter import TurnsPresenter
from ...turns_adjustment_manager.turns_state import TurnsState
from ...turns_adjustment_manager.turns_value import TurnsValue
from ...turns_box.turns_widget.turns_display_frame.turns_display_frame import (
from ..base_adjustment_box_header_widget import BaseAdjustmentBoxHeaderWidget
from ..color_utils import ColorUtils
from ..data_updater.special_placement_data_updater import SpecialPlacementDataUpdater
from ..turns_adjustment_manager.turns_value import TurnsValue
from .GE_turns_label import GE_TurnsLabel
from .adjust_turns_button import AdjustTurnsButton
from .adjustment_panel.beat_adjustment_panel import BeatAdjustmentPanel
from .arrow_movement_manager import ArrowMovementManager
from .arrow_selection_manager import ArrowSelectionManager
from .clickable_ori_label import ClickableOriLabel
from .color_utils import ColorUtils
from .data_updater.special_placement_entry_remover import SpecialPlacementEntryRemover
from .direct_set_dialog.direct_set_turns_dialog import DirectSetTurnsDialog
from .direct_set_turns_button import DirectSetTurnsButton
from .graph_editor_layout_manager import GraphEditorLayoutManager
from .mirrored_entry_adapter import MirroredEntryAdapter
from .mirrored_entry_factory import MirroredEntryFactory
from .mirrored_entry_manager.mirrored_entry_manager import MirroredEntryManager
from .mirrored_entry_service import MirroredEntryService
from .mirrored_entry_utils import MirroredEntryUtils
from .motion_type_label import MotionTypeLabel
from .ori_button import OriButton  # Import the new OriButton class
from .ori_key_generator import OriKeyGenerator
from .ori_picker_box.ori_picker_box import OriPickerBox
from .ori_picker_header import OriPickerHeader
from .ori_picker_widget.ori_picker_widget import OriPickerWidget
from .ori_setter import OrientationSetter
from .ori_text_label import OrientationTextLabel
from .orientation_handler import OrientationHandler
from .pictograph_container.GE_pictograph_container import GraphEditorPictographContainer
from .prop_placement_override_manager import PropPlacementOverrideManager
from .prop_rot_dir_button import PropRotDirButton
from .prop_rot_dir_button_manager.prop_rot_dir_button_manager import (
from .rot_angle_override.rot_angle_override_manager import RotAngleOverrideManager
from .rot_angle_override_coordinator import RotAngleOverrideCoordinator
from .rot_angle_override_data_handler import RotAngleOverrideDataHandler
from .rot_angle_override_mirror_handler import RotAngleOverrideMirrorHandler
from .rot_angle_override_validator import RotAngleOverrideValidator
from .rot_angle_override_view_updater import RotAngleOverrideViewUpdater
from .rotate_button import RotateButton
from .rotate_buttons_widget import RotateButtonsWidget
from .rotation_angle_processor import RotationAngleProcessor
from .special_placement_repository import SpecialPlacementRepository
from .turns_box.turns_box import TurnsBox
from .turns_box_header import TurnsBoxHeader
from .turns_command import AdjustTurnsCommand, SetTurnsCommand, TurnsCommand
from .turns_pattern_manager import TurnsPatternManager
from .turns_text_label import TurnsTextLabel
from .turns_value import TurnsValue
from .turns_widget.turns_widget import TurnsWidget
from PyQt6.QtCore import QObject
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QPoint
from PyQt6.QtCore import QPropertyAnimation, QRect, QPoint, QEasingCurve, QObject
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt, QRectF, QByteArray
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import (
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtGui import QFont, QFontMetrics
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtGui import QMouseEvent, QFont, QFontMetrics
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import (
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtWidgets import QDialog, QHBoxLayout
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QWidget, QSizePolicy
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedLayout, QSizePolicy
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QFrame, QHBoxLayout
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from abc import ABC, abstractmethod
from base_widgets.pictograph.elements.views.GE_pictograph_view import GE_PictographView
from base_widgets.pictograph.pictograph import Pictograph
from data.constants import (
from data.constants import *
from data.constants import ANTI, BLUE, FLOAT, HEX_BLUE, HEX_RED, PRO
from data.constants import ANTI, CLOCKWISE, PRO
from data.constants import ANTI, FLOAT, PRO
from data.constants import BLUE, HEX_BLUE, HEX_RED
from data.constants import BLUE, IN, OUT, RED
from data.constants import BLUE, RED
from data.constants import BLUE, RED, IN
from data.constants import BLUE, RED, IN, OUT
from data.constants import BLUE, RED, IN, OUT, CLOCK, COUNTER
from data.constants import BLUE_ATTRS, RED_ATTRS, TURNS
from data.constants import CLOCK, COUNTER, IN, OUT
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, HEX_BLUE, HEX_RED, OPP, SAME
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, NO_ROT
from data.constants import DASH, STATIC
from data.constants import FLOAT, NO_ROT
from data.constants import ICON_DIR
from data.constants import IN, COUNTER, OUT, CLOCK
from data.constants import RED, BLUE, IN, OUT, CLOCK, COUNTER
from data.constants import STATIC, DASH
from enums.letter.letter import Letter
from enums.letter.letter_condition import LetterCondition
from main_window.main_widget.json_manager.json_manager import JsonManager
from main_window.main_widget.json_manager.special_placement_saver import (
from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph import (
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_selection_dialog import (
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.motion_type_setter import (
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_repository import (
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_state import (
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import TurnsValue
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_btn_state import (
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_button import PropRotDirButton
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_button_manager import (
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_logic_handler import (
from main_window.main_widget.sequence_workbench.graph_editor.graph_editor_animator import (
from main_window.main_widget.sequence_workbench.graph_editor.graph_editor_toggle_tab import (
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rot_angle_override.types import (
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import (
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import ArrowRotAngleOverrideKeyGenerator
from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import TurnsTupleGenerator
from main_window.main_window import TYPE_CHECKING
from objects.arrow.arrow import Arrow
from objects.arrow.arrow import Motion
from objects.motion.motion import Motion
from objects.prop.prop import Prop
from placement_managers.arrow_placement_manager.arrow_placement_context import ArrowPlacementContext
from placement_managers.attr_key_generator import (
from placement_managers.prop_placement_manager.handlers.beta_offset_calculator import (
from settings_manager.global_settings.app_context import AppContext
from settings_manager.settings_manager import pyqtSignal
from styles.styled_button import StyledButton
from typing import Dict, Any
from typing import Dict, Any, Optional
from typing import Dict, Any, Tuple
from typing import List
from typing import NotRequired
from typing import Optional
from typing import TYPE_CHECKING
from typing import TYPE_CHECKING, Any
from typing import TYPE_CHECKING, Dict
from typing import TYPE_CHECKING, Dict, Any
from typing import TYPE_CHECKING, Literal
from typing import TYPE_CHECKING, Optional
from typing import TYPE_CHECKING, Union
from typing import TypedDict
from typing import Union
from typing import cast
from utils.path_helpers import get_data_path
from utils.path_helpers import get_image_path
from utils.reversal_detector import ReversalDetector
import logging
import os

# From arrow_selection_manager.py
from PyQt6.QtCore import pyqtSignal, QObject
from typing import TYPE_CHECKING
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.graph_editor import (
        GraphEditor,
    )
    from objects.arrow.arrow import Arrow


class ArrowSelectionManager(QObject):
    selection_changed = pyqtSignal(object)

    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__()
        self.graph_editor = graph_editor

    def set_selected_arrow(self, arrow: "Arrow") -> None:
        """Update the global selected arrow via AppContext."""
        AppContext.set_selected_arrow(arrow)
        self.selection_changed.emit(arrow)  # Notify listeners

    def clear_selection(self):
        """Clear the global selection via AppContext."""
        AppContext.clear_selected_arrow()


# From concatenated_graph_editor.py


# From GE_pictograph.py
from typing import TYPE_CHECKING


from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )
    from main_window.main_widget.sequence_workbench.graph_editor.pictograph_container.GE_pictograph_container import (
        GraphEditorPictographContainer,
    )


class GE_Pictograph(Beat):
    view: "GE_PictographView"

    def __init__(self, pictograph_container: "GraphEditorPictographContainer") -> None:
        super().__init__(
            pictograph_container.graph_editor.sequence_workbench.beat_frame
        )
        self.is_blank = True
        self.main_widget = pictograph_container.graph_editor.main_widget
        self.graph_editor = pictograph_container.graph_editor


# From GE_pictograph_view_mouse_event_handler.py
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING
from PyQt6.QtGui import QMouseEvent

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


class GE_PictographViewMouseEventHandler:
    def __init__(self, pictograph_view: "GE_PictographView") -> None:
        self.pictograph_view = pictograph_view
        self.pictograph = pictograph_view.pictograph
        self.selection_manager = self.pictograph_view.graph_editor.selection_manager

    def handle_mouse_press(self, event: QMouseEvent) -> None:
        widget_pos = event.pos()
        scene_pos = self.pictograph_view.mapToScene(widget_pos)
        items_at_pos = self.pictograph_view.scene().items(scene_pos)
        arrow = next((item for item in items_at_pos if isinstance(item, Arrow)), None)

        if arrow:
            self.selection_manager.set_selected_arrow(arrow)
        else:
            self.selection_manager.clear_selection()

        self.pictograph_view.repaint()

    def is_arrow_under_cursor(self, event: "QMouseEvent") -> bool:
        widget_pos = event.pos()
        scene_pos = self.pictograph_view.mapToScene(widget_pos)
        items_at_pos = self.pictograph_view.scene().items(scene_pos)
        return any(isinstance(item, Arrow) for item in items_at_pos)

    def clear_selections(self) -> None:
        for arrow in self.pictograph.elements.arrows.values():
            arrow.setSelected(False)
        for prop in self.pictograph.elements.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None


# From graph_editor.py
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

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._setup_components()
        self.layout_manager.setup_layout()
        self.hide()

    def _setup_components(self) -> None:
        self.selection_manager = ArrowSelectionManager(self)
        self.pictograph_container = GraphEditorPictographContainer(self)
        self.adjustment_panel = BeatAdjustmentPanel(self)
        self.layout_manager = GraphEditorLayoutManager(self)
        self.toggle_tab = GraphEditorToggleTab(self)
        self.placeholder = QFrame(self)
        self.animator = GraphEditorAnimator(self)

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


# From graph_editor_animator.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import QPropertyAnimation, QRect, QPoint, QEasingCurve, QObject

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.graph_editor import (
        GraphEditor,
    )


class GraphEditorAnimator(QObject):
    def __init__(self, graph_editor: "GraphEditor"):
        super().__init__(graph_editor)
        self.sequence_workbench = graph_editor.sequence_workbench
        self.graph_editor = graph_editor
        self.toggle_tab = graph_editor.toggle_tab
        self.graph_editor_placeholder = self.graph_editor.placeholder
        self.button_panel_bottom_placeholder = (
            self.sequence_workbench.button_panel.bottom_placeholder
        )
        self.current_animations = []

    def toggle(self):
        if self.graph_editor.is_toggled:
            self.graph_editor.is_toggled = False
            self.animate_graph_editor(show=False)
        else:
            self.sequence_workbench.layout_manager.main_layout.addWidget(
                self.graph_editor_placeholder
            )
            self.graph_editor.show()
            self.graph_editor.is_toggled = True
            self.animate_graph_editor(show=True)

    def clear_previous_animations(self):
        """Stop all currently running animations and clear effects."""
        for animation in self.current_animations:
            animation.stop()
        self.current_animations.clear()

        # Clear any lingering graphics effects (if used)
        self.graph_editor.setGraphicsEffect(None)
        self.graph_editor_placeholder.setGraphicsEffect(None)
        self.toggle_tab.setGraphicsEffect(None)

    def animate_graph_editor(self, show):
        self.clear_previous_animations()

        parent_height = self.sequence_workbench.height()
        parent_width = self.sequence_workbench.width()
        desired_height = self.sequence_workbench.graph_editor.get_graph_editor_height()

        if show:
            editor_start_rect = QRect(0, parent_height, parent_width, 0)
            editor_end_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            toggle_start_pos = QPoint(0, parent_height - self.toggle_tab.height())
            toggle_end_pos = QPoint(
                0, parent_height - desired_height - self.toggle_tab.height()
            )
            placeholder_start_height = 0
            placeholder_end_height = desired_height
        else:
            editor_start_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            editor_end_rect = QRect(0, parent_height, parent_width, 0)
            toggle_start_pos = QPoint(
                0, parent_height - desired_height - self.toggle_tab.height()
            )
            toggle_end_pos = QPoint(0, parent_height - self.toggle_tab.height())
            placeholder_start_height = desired_height
            placeholder_end_height = 0

        # Animate GraphEditor geometry
        graph_editor_animation = QPropertyAnimation(self.graph_editor, b"geometry")
        graph_editor_animation.setStartValue(editor_start_rect)
        graph_editor_animation.setEndValue(editor_end_rect)
        graph_editor_animation.setDuration(300)
        graph_editor_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.current_animations.append(graph_editor_animation)

        # Animate graph editor placeholder height
        placeholder_animation = QPropertyAnimation(
            self.graph_editor_placeholder, b"minimumHeight"
        )
        placeholder_animation.setStartValue(placeholder_start_height)
        placeholder_animation.setEndValue(placeholder_end_height)
        placeholder_animation.setDuration(300)
        placeholder_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.current_animations.append(placeholder_animation)

        # Animate toggle tab position
        toggle_tab_animation = QPropertyAnimation(self.toggle_tab, b"pos")
        toggle_tab_animation.setStartValue(toggle_start_pos)
        toggle_tab_animation.setEndValue(toggle_end_pos)
        toggle_tab_animation.setDuration(300)
        toggle_tab_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.current_animations.append(toggle_tab_animation)

        # Handle cleanup on collapse
        if not show:
            graph_editor_animation.finished.connect(
                lambda: self.sequence_workbench.layout_manager.main_layout.removeWidget(
                    self.graph_editor_placeholder
                )
            )
            graph_editor_animation.finished.connect(self.graph_editor.hide)

        # Start all animations
        for animation in self.current_animations:
            animation.start()


# From graph_editor_layout_manager.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedLayout, QSizePolicy

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.graph_editor import (
        GraphEditor,
    )


class GraphEditorLayoutManager:
    def __init__(self, graph_editor: "GraphEditor") -> None:
        self.ge = graph_editor
        self.sequence_workbench = graph_editor.sequence_workbench

    def setup_layout(self) -> None:
        self._setup_main_layout()
        self.ge.pictograph_layout = self._setup_pictograph_layout()
        self.ge.adjustment_panel_layout = self._setup_adjustment_panel_layout()
        self._setup_stacks()

        # Make the pictograph container "fixed" in the middle:
        self.ge.pictograph_container.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        # You’ll still call setFixedSize(w, h) in the pictograph code (below),
        # or do it in the resize event to enforce a perfect square.

        # Add them to the main_layout with no spacing:
        self.ge.main_layout.addLayout(self.ge.left_stack, stretch=1)
        self.ge.main_layout.addLayout(self.ge.pictograph_layout, stretch=0)
        self.ge.main_layout.addLayout(self.ge.right_stack, stretch=1)

    def _setup_main_layout(self):
        self.ge.main_layout = QHBoxLayout(self.ge)
        self.ge.main_layout.setSpacing(0)
        self.ge.main_layout.setContentsMargins(0, 0, 0, 0)

    def _setup_stacks(self):
        self.ge.left_stack = QStackedLayout()
        self.ge.left_stack.addWidget(self.ge.adjustment_panel.blue_ori_picker)
        self.ge.left_stack.addWidget(self.ge.adjustment_panel.blue_turns_box)

        self.ge.right_stack = QStackedLayout()
        self.ge.right_stack.addWidget(self.ge.adjustment_panel.red_ori_picker)
        self.ge.right_stack.addWidget(self.ge.adjustment_panel.red_turns_box)

    def _setup_pictograph_layout(self) -> None:
        pictograph_layout = QVBoxLayout()
        pictograph_layout.addWidget(self.ge.pictograph_container)
        pictograph_layout.setContentsMargins(0, 0, 0, 0)
        pictograph_layout.setSpacing(0)
        return pictograph_layout

    def _setup_adjustment_panel_layout(self) -> None:
        adjustment_panel_layout = QVBoxLayout()
        adjustment_panel_layout.addWidget(self.ge.adjustment_panel)
        adjustment_panel_layout.setContentsMargins(0, 0, 0, 0)
        adjustment_panel_layout.setSpacing(0)
        return adjustment_panel_layout


# From graph_editor_toggle_tab.py
# graph_editor_toggle_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.graph_editor import (
        GraphEditor,
    )

# Define transparency value for easy modification
OPACITY = 0.7

# Define common gradients as constants for readability
BLUESTEEL_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #1e3c72,
        stop: 0.3 #6c9ce9,
        stop: 0.6 #4a77d4,
        stop: 1 #2a52be
    )
"""

SILVER_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(80, 80, 80, {OPACITY}),
        stop: 0.3 rgba(160, 160, 160, {OPACITY}),
        stop: 0.6 rgba(120, 120, 120, {OPACITY}),
        stop: 1 rgba(40, 40, 40, {OPACITY})
    )
"""


class GraphEditorToggleTab(QWidget):
    """Toggle tab widget to expand/collapse the GraphEditor."""

    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor.sequence_workbench)
        self.graph_editor = graph_editor
        self.sequence_workbench = graph_editor.sequence_workbench
        self._setup_layout()
        self._setup_components()
        self.move(0, self.sequence_workbench.height() - self.height())
        self.raise_()

    def _setup_components(self):
        self.label = QLabel("Editor", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout.addWidget(self.label)
        self.label.setStyleSheet(
            f"""
            QLabel {{
                color: white;
                font-weight: bold;
                border-radius: 10px;
                background: {SILVER_GRADIENT};
            }}
            QLabel:hover {{
                color: white;
                font-weight: bold;
                background: {BLUESTEEL_GRADIENT};
                border-radius: 10px;
                border: 1px solid white;
            }}
        """
        )

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def mousePressEvent(self, event) -> None:
        toggler = self.graph_editor.animator
        if toggler:
            toggler.toggle()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.setFixedHeight(self.sequence_workbench.main_widget.height() // 20)
        self.setFixedWidth(self.sequence_workbench.width() // 8)
        font_size = self.height() // 3
        font = QFont()
        font.setPointSize(font_size)
        self.label.setFont(font)
        family = "Georgia"
        self.label.setFont(QFont(family, font_size))
        self.setStyleSheet("background-color: white")

    def reposition_toggle_tab(self):
        sequence_workbench_height = self.sequence_workbench.height()
        graph_editor_height = (
            self.sequence_workbench.height()
            - self.sequence_workbench.graph_editor.get_graph_editor_height()
        )
        if self.graph_editor.is_toggled:
            self.move(0, graph_editor_height - self.height())
        else:
            self.move(0, sequence_workbench_height - self.height())


# From graph_editor_view_key_event_handler.py
from typing import TYPE_CHECKING
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt

from settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


class GraphEditorViewKeyEventHandler:
    def __init__(self, pictograph_view: "GE_PictographView") -> None:
        self.ge_view = pictograph_view
        self.pictograph = pictograph_view.pictograph
        self.graph_editor = pictograph_view.graph_editor

    def handle_key_press(self, event: QKeyEvent) -> bool:
        self.hotkey_graph_adjuster = self.ge_view.hotkey_graph_adjuster
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        key = event.key()
        selected_arrow = AppContext.get_selected_arrow()

        if selected_arrow:
            if key in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
                self.hotkey_graph_adjuster.movement_manager.handle_arrow_movement(
                    key, shift_held, ctrl_held
                )
            elif key == Qt.Key.Key_X:
                self.hotkey_graph_adjuster.rot_angle_override_manager.handle_arrow_rot_angle_override()
                self.pictograph.managers.updater.update_pictograph()
            elif key == Qt.Key.Key_Z:
                self.hotkey_graph_adjuster.entry_remover.remove_special_placement_entry(
                    self.ge_view.pictograph.state.letter,
                    arrow=AppContext.get_selected_arrow(),
                )
            else:
                return False

        if key == Qt.Key.Key_C:
            self.hotkey_graph_adjuster.prop_placement_override_manager.handle_prop_placement_override()
        return True


# From __init__.py


# From base_adjustment_box_header_widget.py
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from typing import TYPE_CHECKING, Union

from data.constants import BLUE, RED

if TYPE_CHECKING:
    from .ori_picker_box.ori_picker_box import OriPickerBox
    from .turns_box.turns_box import TurnsBox


class BaseAdjustmentBoxHeaderWidget(QWidget):
    def __init__(self, adjustment_box: Union["OriPickerBox", "TurnsBox"]) -> None:
        super().__init__(adjustment_box)
        self.adjustment_box = adjustment_box
        self.graph_editor = self.adjustment_box.graph_editor
        self.separator: QFrame = self.create_separator()
        self.header_label: QLabel = self._setup_header_label()
        self.layout: QVBoxLayout = self._setup_layout()

    def _setup_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout(self)
        self.top_hbox = QHBoxLayout()
        self.separator_hbox = QHBoxLayout()
        layout.addLayout(self.top_hbox)
        layout.addLayout(self.separator_hbox)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        return layout

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")
        return separator

    def _setup_header_label(self) -> QLabel:
        header_label = QLabel(self)
        color = self.adjustment_box.color
        text, font_color = self._get_label_text_and_color(color)

        self.header_label_font = QFont("Georgia")
        self.header_label_font.setBold(True)
        header_label.setFont(self.header_label_font)
        header_label.setText(text)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet(f"color: {font_color.name()};")
        return header_label

    def _get_label_text_and_color(self, color: str) -> tuple[str, QColor]:
        if color == RED:
            return "Right", QColor("#ED1C24")
        elif color == BLUE:
            return "Left", QColor("#2E3192")
        else:
            return "", QColor("#000000")

    def resizeEvent(self, event) -> None:
        self.setFixedHeight(self.adjustment_box.graph_editor.height() // 4)

        font_size = self.graph_editor.sequence_workbench.main_widget.width() // 80
        self.header_label_font.setPointSize(font_size)
        self.header_label.setFont(self.header_label_font)
        self.header_label.repaint()

        super().resizeEvent(event)


# From beat_adjustment_panel.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QWidget, QSizePolicy
from data.constants import BLUE, RED, IN
from .ori_picker_box.ori_picker_box import OriPickerBox
from .turns_box.turns_box import TurnsBox

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor


ORI_WIDGET_INDEX = 0
TURNS_WIDGET_INDEX = 1


class BeatAdjustmentPanel(QFrame):
    turns_boxes: list[TurnsBox]
    ori_picker_boxes: list[OriPickerBox]

    def __init__(self, graph_editor: "GraphEditor") -> None:
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


# From __init__.py


# From color_utils.py
class ColorUtils:
    @staticmethod
    def lighten_color(color_hex: str) -> str:
        """
        Lightens a given hex color by a factor of 2 (makes it brighter).

        Args:
            color_hex (str): The hex color code to lighten (e.g., "#RRGGBB").

        Returns:
            str: The lightened hex color code (e.g., "rgb(r, g, b)").
        """
        r, g, b = (
            int(color_hex[1:3], 16),
            int(color_hex[3:5], 16),
            int(color_hex[5:7], 16),
        )
        whitened_r = min(255, r + (255 - r) // 2)
        whitened_g = min(255, g + (255 - g) // 2)
        whitened_b = min(255, b + (255 - b) // 2)
        whitened_color = f"rgb({whitened_r}, {whitened_g}, {whitened_b})"
        return whitened_color


# From ori_picker_box.py
from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, HEX_BLUE, HEX_RED, OPP, SAME
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from .ori_picker_widget.ori_picker_widget import OriPickerWidget
from .ori_picker_header import OriPickerHeader
from .color_utils import ColorUtils

if TYPE_CHECKING:
    from ..beat_adjustment_panel import BeatAdjustmentPanel
    from base_widgets.pictograph.pictograph import Pictograph


class OriPickerBox(QFrame):
    vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
    prop_rot_dir_btn_state: dict[str, bool] = {
        CLOCKWISE: False,
        COUNTER_CLOCKWISE: False,
    }

    def __init__(
        self,
        adjustment_panel: "BeatAdjustmentPanel",
        start_pos: "Pictograph",
        color: str,
    ) -> None:
        super().__init__(adjustment_panel)
        self.adjustment_panel = adjustment_panel
        self.color = color
        self.start_pos = start_pos
        self.graph_editor = self.adjustment_panel.graph_editor
        self.setObjectName(self.__class__.__name__)

        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.header = OriPickerHeader(self)
        self.ori_picker_widget = OriPickerWidget(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.ori_picker_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resizeEvent(self, event):
        border_width = self.graph_editor.sequence_workbench.width() // 200
        color_hex = (
            HEX_RED
            if self.color == "red"
            else HEX_BLUE if self.color == "blue" else self.color
        )
        whitened_color = ColorUtils.lighten_color(color_hex)
        self.setStyleSheet(
            f"#{self.__class__.__name__} {{ border: {border_width}px solid "
            f"{color_hex}; background-color: {whitened_color};}}"
        )
        self.ori_picker_widget.resizeEvent(event)
        super().resizeEvent(event)


# From ori_picker_header.py
from typing import TYPE_CHECKING
from ..base_adjustment_box_header_widget import BaseAdjustmentBoxHeaderWidget

if TYPE_CHECKING:
    from .ori_picker_box import OriPickerBox


class OriPickerHeader(BaseAdjustmentBoxHeaderWidget):
    def __init__(self, ori_picker_box: "OriPickerBox") -> None:
        super().__init__(ori_picker_box)
        self._add_widgets()

    def _add_widgets(self) -> None:
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.header_label)
        self.top_hbox.addStretch(1)
        self.separator_hbox.addWidget(self.separator)


# From __init__.py


# From clickable_ori_label.py
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QMouseEvent, QFont, QFontMetrics
from PyQt6.QtCore import Qt, pyqtSignal
from typing import TYPE_CHECKING, Literal

from PyQt6.QtCore import QPoint
from data.constants import RED, BLUE, IN, OUT, CLOCK, COUNTER
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_selection_dialog import (
    OriSelectionDialog,
)


if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget


class ClickableOriLabel(QLabel):
    leftClicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def __init__(self, ori_picker_widget: "OriPickerWidget"):
        super().__init__(ori_picker_widget)
        self.ori_picker_widget = ori_picker_widget
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.leftClicked.connect(self._on_orientation_display_clicked)
        self.rightClicked.connect(self._on_orientation_label_right_clicked)
        self.dialog = OriSelectionDialog(self.ori_picker_widget)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftClicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightClicked.emit()

    def set_orientation(self, orientation):
        self.setText(orientation)

    def _get_border_color(
        self, color
    ) -> Literal["#ED1C24"] | Literal["#2E3192"] | Literal["black"]:
        if color == RED:
            return "#ED1C24"
        elif color == BLUE:
            return "#2E3192"
        else:
            return "black"

    def _on_orientation_display_clicked(self):
        self.dialog.move(self.mapToGlobal(QPoint(0, 0)))
        if self.dialog.exec():
            new_orientation = self.dialog.selected_orientation
            self.ori_picker_widget.ori_setter.set_orientation(new_orientation)

    def _on_orientation_label_right_clicked(self):
        current_ori = self.ori_picker_widget.orientations[
            self.ori_picker_widget.current_orientation_index
        ]
        if current_ori in [IN, OUT]:
            new_ori = OUT if current_ori == IN else IN
        elif current_ori in [CLOCK, COUNTER]:
            new_ori = COUNTER if current_ori == CLOCK else CLOCK
        else:
            new_ori = current_ori
        self.ori_picker_widget.ori_setter.set_orientation(new_ori)

    def resizeEvent(self, event):
        font_size = self.ori_picker_widget.ori_picker_box.graph_editor.width() // 30
        font = QFont("Arial", font_size, QFont.Weight.Bold)
        self.setFont(font)

        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance("counter")
        padding = font_metrics.horizontalAdvance("  ")

        required_width = text_width + padding
        self.setFixedWidth(int(required_width * 1.1))

        # Calculate the height based on font metrics and border size
        text_height = font_metrics.height()
        border_size = max(int(required_width / 60), 1)
        total_height = text_height + 2 * border_size  # Account for top and bottom borders
        self.setFixedHeight(total_height)

        border_color = self._get_border_color(self.ori_picker_widget.color)
        border_radius = total_height // 2  # Use half the height for radius to ensure rounded corners

        self.setStyleSheet(
            f"QLabel {{"
            f"    border: {border_size}px solid {border_color};"
            f"    background-color: white;"
            f"    border-radius: {border_radius}px;"
            f"}}"
        )

        super().resizeEvent(event)

# From ori_button.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QFontMetrics
from data.constants import BLUE, HEX_BLUE, HEX_RED

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_selection_dialog import (
        OriSelectionDialog,
    )


class OriButton(QPushButton):
    def __init__(self, orientation: str, ori_selection_dialog: "OriSelectionDialog"):
        super().__init__(orientation)
        self.orientation = orientation
        self.ori_selection_dialog = ori_selection_dialog
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ori_picker_widget = ori_selection_dialog.ori_picker_widget

    def resize_buttons(self):
        """Resize buttons according to the orientation label's size."""
        ori_label_width = self.ori_picker_widget.clickable_ori_label.width()
        button_height = int(self.ori_picker_widget.ori_picker_box.height() // 3)
        font_size = int(button_height * 0.5)  # Font size based on button height

        font = QFont("Arial", font_size, QFont.Weight.Bold)
        font_metrics = QFontMetrics(font)

        self.setFont(font)

        # Calculate button width based on text length
        text_width = font_metrics.horizontalAdvance(self.orientation)
        button_width = max(text_width + 40, ori_label_width // 2)  # Add padding
        border_width = button_height // 20
        self.setFixedSize(QSize(button_width, button_height))
        self.setStyleSheet(
            f"""
            QPushButton {{
                border: {border_width}px solid {HEX_BLUE if self.ori_picker_widget.color == BLUE else HEX_RED};
                border-radius: {button_height // 2}px;
                background-color: #ffffff;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
            """
        )

    def resizeEvent(self, event):
        self.resize_buttons()
        super().resizeEvent(event)


# From ori_picker_widget.py
# ori_picker_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import TYPE_CHECKING
from data.constants import IN, COUNTER, OUT, CLOCK
from settings_manager.global_settings.app_context import AppContext
from .ori_setter import OrientationSetter
from .ori_text_label import OrientationTextLabel
from .clickable_ori_label import ClickableOriLabel
from .rotate_buttons_widget import RotateButtonsWidget

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.widgets.option_picker_widget import (
        OptionPickerWidget,
    )
    from ..ori_picker_box import OriPickerBox


class OriPickerWidget(QWidget):
    """Minimalist widget that displays the orientation controls."""

    ori_adjusted = pyqtSignal(str)
    current_orientation_index = 0
    orientations = [IN, COUNTER, OUT, CLOCK]
    option_picker: "OptionPickerWidget" = None

    def __init__(self, ori_picker_box: "OriPickerBox") -> None:
        super().__init__(ori_picker_box)
        self.ori_picker_box = ori_picker_box
        self.color = self.ori_picker_box.color

        self.json_manager = AppContext.json_manager()
        self.json_validation_engine = self.json_manager.ori_validation_engine
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_workbench.beat_frame

        self.orientation_text_label = OrientationTextLabel(self)
        self.clickable_ori_label = ClickableOriLabel(self)
        self.rotate_buttons_widget = RotateButtonsWidget(self)
        self.ori_setter = OrientationSetter(self)

        self._setup_layout()

    def _setup_layout(self):
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        widgets = [
            self.orientation_text_label,
            self.clickable_ori_label,
            self.rotate_buttons_widget,
        ]

        for widget in widgets:
            layout.addStretch(1)
            layout.addWidget(widget)
        layout.addStretch(1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.orientation_text_label.resizeEvent(event)
        self.clickable_ori_label.resizeEvent(event)


# From ori_selection_dialog.py
from PyQt6.QtWidgets import QDialog, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from data.constants import BLUE, HEX_BLUE, HEX_RED
from .ori_button import OriButton  # Import the new OriButton class
from ..color_utils import ColorUtils

if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget


class OriSelectionDialog(QDialog):
    buttons: dict[str, OriButton] = {}

    def __init__(self, ori_picker_widget: "OriPickerWidget"):
        super().__init__(
            ori_picker_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.ori_picker_widget = ori_picker_widget
        self.selected_orientation = None
        self._set_dialog_style()
        self._setup_buttons()
        self._setup_layout()

    def _set_dialog_style(self):
        border_color = HEX_BLUE if self.ori_picker_widget.color == BLUE else HEX_RED
        background_color = ColorUtils.lighten_color(border_color)
        self.setStyleSheet(
            f"background-color: {background_color}; border: 2px solid {border_color};"
        )

    def _setup_buttons(self):
        for orientation in self.ori_picker_widget.orientations:
            button = OriButton(orientation, self)  # Use OriButton
            button.clicked.connect(
                lambda _, ori=orientation: self.select_orientation(ori)
            )
            self.buttons[orientation] = button

    def _setup_layout(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        for button in self.buttons.values():
            layout.addWidget(button)
        self.adjustSize()

    def select_orientation(self, orientation):
        self.selected_orientation = orientation
        self.accept()


# From ori_setter.py
# orientation_setter.py
from typing import TYPE_CHECKING
from base_widgets.pictograph.pictograph import Pictograph
from data.constants import (
    BLUE,
    BLUE_ATTRS,
    RED_ATTRS,
    START_ORI,
    END_ORI,
    BOX,
    DIAMOND,
)

if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget


class OrientationSetter:
    def __init__(self, ori_picker_widget: "OriPickerWidget") -> None:
        self.ori_picker_widget = ori_picker_widget
        self.color = ori_picker_widget.color
        self.json_manager = ori_picker_widget.json_manager
        self.json_validation_engine = ori_picker_widget.json_validation_engine
        self.ori_picker_box = ori_picker_widget.ori_picker_box
        self.ori_adjusted = ori_picker_widget.ori_adjusted
        self.option_picker = ori_picker_widget.option_picker
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_workbench.beat_frame

    def set_orientation(self, orientation: str) -> None:
        """Apply the orientation to the related pictographs and data structures."""
        self.update_current_orientation_index(orientation)
        self._update_clickable_ori_label(orientation)

        if len(self.json_manager.loader_saver.load_current_sequence()) > 1:
            self._update_start_pos_ori(orientation)
            self._update_start_position_pictographs(orientation)
            self._update_graph_editor_orientation(orientation)
            self._refresh_option_picker()
        else:
            self._update_start_options(orientation)
            self._update_advanced_start_pos_picker(orientation)

        self._update_beats_from_current_sequence_json()

    def _update_graph_editor_orientation(self, orientation: str) -> None:
        self.ori_picker_box.graph_editor.pictograph_container.GE_view.pictograph.managers.updater.update_pictograph(
            {
                f"{self.color}_attributes": {
                    START_ORI: orientation,
                    END_ORI: orientation,
                }
            }
        )

    def update_current_orientation_index(self, orientation: str) -> None:
        self.ori_picker_widget.current_orientation_index = (
            self.ori_picker_widget.orientations.index(orientation)
        )

    def _update_clickable_ori_label(self, orientation: str) -> None:
        self.ori_picker_widget.clickable_ori_label.setText(orientation)

    def _update_start_pos_ori(self, orientation: str) -> None:
        self.json_manager.start_pos_handler.update_start_pos_ori(
            self.color, orientation
        )
        self.json_validation_engine.run(is_current_sequence=True)

    def _update_start_position_pictographs(self, orientation: str) -> None:
        construct_tab = (
            self.ori_picker_box.graph_editor.sequence_workbench.main_widget.construct_tab
        )
        start_position_pictographs = (
            construct_tab.start_pos_picker.pictograph_frame.start_positions
        )
        if start_position_pictographs:
            for pictograph in start_position_pictographs.values():
                pictograph.managers.updater.update_pictograph(
                    {
                        f"{self.color}_attributes": {
                            START_ORI: orientation,
                            END_ORI: orientation,
                        }
                    }
                )

    def _refresh_option_picker(self) -> None:
        construct_tab = (
            self.ori_picker_box.graph_editor.sequence_workbench.main_widget.construct_tab
        )
        self.option_picker = construct_tab.option_picker
        self.option_picker.updater.refresh_options()

    def _update_start_options(self, orientation: str) -> None:
        construct_tab = (
            self.ori_picker_box.graph_editor.sequence_workbench.main_widget.construct_tab
        )
        start_pos_picker = construct_tab.start_pos_picker
        for pictograph in start_pos_picker.start_options.values():
            pictograph.managers.updater.update_pictograph(
                {
                    f"{self.color}_attributes": {
                        START_ORI: orientation,
                        END_ORI: orientation,
                    }
                }
            )

    def _update_advanced_start_pos_picker(self, orientation: str) -> None:
        construct_tab = (
            self.ori_picker_box.graph_editor.sequence_workbench.main_widget.construct_tab
        )
        advanced_start_pos_picker = construct_tab.advanced_start_pos_picker
        grid_mode = DIAMOND
        if grid_mode == BOX:
            pictograph_list = advanced_start_pos_picker.box_pictographs
        elif grid_mode == DIAMOND:
            pictograph_list = advanced_start_pos_picker.diamond_pictographs
        else:
            pictograph_list = []
        for pictograph in pictograph_list:
            pictograph.managers.updater.update_pictograph(
                {
                    f"{self.color}_attributes": {
                        START_ORI: orientation,
                        END_ORI: orientation,
                    }
                }
            )

    def _update_beats_from_current_sequence_json(self) -> None:
        self.beat_frame.updater.update_beats_from_current_sequence_json()

    def set_initial_orientation(
        self, start_pos_pictograph: "Pictograph", color: str
    ) -> None:
        initial_orientation = self._get_initial_orientation(start_pos_pictograph, color)
        self.current_orientation_index = self.ori_picker_widget.orientations.index(
            initial_orientation
        )
        self.ori_picker_widget.clickable_ori_label.setText(initial_orientation)

    def _get_initial_orientation(
        self, start_pos_pictograph: "Pictograph", color: str
    ) -> str:
        if color == BLUE:
            return start_pos_pictograph.state.pictograph_data[BLUE_ATTRS][START_ORI]
        else:
            return start_pos_pictograph.state.pictograph_data[RED_ATTRS][START_ORI]


# From ori_text_label.py
# orientation_text_label.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_picker_widget import (
        OriPickerWidget,
    )


class OrientationTextLabel(QLabel):
    def __init__(self, ori_picker_widget: "OriPickerWidget"):
        super().__init__("Orientation", ori_picker_widget)
        self.ori_picker_widget = ori_picker_widget
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        font_size = int(
            self.ori_picker_widget.ori_picker_box.graph_editor.width() // 60
        )
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.setFont(font)
        super().resizeEvent(event)


# From ori_updater.py
from typing import TYPE_CHECKING
from data.constants import *

if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget
    from base_widgets.pictograph.pictograph import Pictograph

    from objects.motion.motion import Motion


class OriUpdater:
    def __init__(self, ori_picker_widget: "OriPickerWidget") -> None:
        self.ori_picker_box = ori_picker_widget.ori_picker_box
        self.turns_widget = ori_picker_widget

    def set_motion_turns(self, motion: "Motion", new_turns: int) -> None:
        pictograph_data = {f"{motion.state.color}_turns": new_turns}
        motion.pictograph.managers.updater.update_pictograph(pictograph_data)

    def _adjust_turns_for_pictograph(
        self, pictograph: "Pictograph", adjustment: int
    ) -> None:
        """Adjust turns for each relevant motion in the pictograph."""
        for motion in pictograph.elements.motion_set.values():
            if motion.state.color == self.ori_picker_box.color:
                new_turns = self._calculate_new_turns(motion.state.turns, adjustment)
                self.set_motion_turns(motion, new_turns)

    def _calculate_new_turns(self, current_turns: int, adjustment: int) -> int:
        """Calculate new turns value based on adjustment."""
        new_turns = max(0, min(3, current_turns + adjustment))
        return int(new_turns) if new_turns.is_integer() else new_turns

    def _set_vtg_dir_state_default(self) -> None:
        """set the vtg direction state to default."""
        self.ori_picker_box.vtg_dir_btn_state[SAME] = True
        self.ori_picker_box.vtg_dir_btn_state[OPP] = False

    def _set_prop_rot_dir_state_default(self) -> None:
        """set the vtg direction state to default."""
        self.ori_picker_box.prop_rot_dir_btn_state[SAME] = True
        self.ori_picker_box.prop_rot_dir_btn_state[OPP] = False

    def _clamp_turns(self, turns: int) -> int:
        """Clamp the turns value to be within allowable range."""
        return max(0, min(3, turns))


# From rotate_button.py
# rotate_button.py
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.rotate_buttons_widget import (
        RotateButtonsWidget,
    )


class RotateButton(StyledButton):
    def __init__(
        self,
        rotate_buttons_widget: "RotateButtonsWidget",
        icon_path: str,
        click_function: callable,
    ):
        super().__init__(rotate_buttons_widget)
        self.rotate_buttons_widget = rotate_buttons_widget
        self.setIcon(QIcon(icon_path))
        self.clicked.connect(click_function)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def resize_button(self):
        button_size = int(
            self.rotate_buttons_widget.ori_picker_widget.ori_picker_box.graph_editor.height()
            // 4.5
        )
        icon_size = int(button_size * 0.6)
        self.setFixedSize(QSize(button_size, button_size))
        self.setIconSize(QSize(icon_size, icon_size))


# From rotate_buttons_widget.py
# rotate_buttons_widget.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from typing import TYPE_CHECKING
from utils.path_helpers import get_image_path
from .rotate_button import RotateButton

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_picker_widget import (
        OriPickerWidget,
    )


class RotateButtonsWidget(QWidget):
    def __init__(
        self,
        ori_picker_widget: "OriPickerWidget",
    ):
        super().__init__(ori_picker_widget)
        self.ori_picker_widget = ori_picker_widget
        path = get_image_path("icons")
        self.ccw_button = RotateButton(
            self, f"{path}/rotate_ccw_white.png", self.rotate_ccw
        )
        self.cw_button = RotateButton(
            self, f"{path}/rotate_cw_white.png", self.rotate_cw
        )

        layout = QHBoxLayout(self)
        layout.addWidget(self.ccw_button)
        layout.addWidget(self.cw_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def resize_rotate_buttons_widget(self):
        self.ccw_button.resize_button()
        self.cw_button.resize_button()

    def rotate_cw(self) -> None:
        self.ori_picker_widget.current_orientation_index = (
            self.ori_picker_widget.current_orientation_index + 1
        ) % len(self.ori_picker_widget.orientations)
        new_ori = self.ori_picker_widget.orientations[
            self.ori_picker_widget.current_orientation_index
        ]
        self.ori_picker_widget.ori_setter.set_orientation(new_ori)

    def rotate_ccw(self) -> None:
        self.ori_picker_widget.current_orientation_index = (
            self.ori_picker_widget.current_orientation_index - 1
        ) % len(self.ori_picker_widget.orientations)
        new_ori = self.ori_picker_widget.orientations[
            self.ori_picker_widget.current_orientation_index
        ]
        self.ori_picker_widget.ori_setter.set_orientation(new_ori)

    def resizeEvent(self, event):
        self.resize_rotate_buttons_widget()
        event.accept()


# From __init__.py


# From __init__.py


# From __init__.py


# From json_turns_repository.py
# src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/new_turns_adjustment_manager/json_turns_repository.py
from typing import Optional
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_repository import (
    TurnsRepository,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
    TurnsValue,
)
from settings_manager.global_settings.app_context import AppContext
from main_window.main_widget.json_manager.json_manager import JsonManager

class JsonTurnsRepository(TurnsRepository):
    def __init__(self, json_manager: "JsonManager"):
        self._manager = json_manager

    def save(self, value: TurnsValue, color: str):  # ✅ Accept color
        """Saves turns value to JSON through the existing JSON manager"""
        self.beat_frame = (
            AppContext.main_window().main_widget.sequence_workbench.beat_frame
        )
        try:
            pictograph_index = self._get_pictograph_index()
            self._manager.updater.turns_updater.update_turns_in_json_at_index(
                pictograph_index,
                color,
                value.raw_value,
                self.beat_frame,  # ✅ Use passed color
            )
        except Exception as e:
            raise RuntimeError(f"JSON save failed: {str(e)}") from e

    def load(self) -> Optional[TurnsValue]:
        """Loads turns value from JSON"""
        try:
            pictograph_index = self._get_pictograph_index()
            raw_value = self._manager.loader_saver.get_json_turns(
                pictograph_index, self._get_color()
            )
            return TurnsValue(raw_value)
        except Exception as e:
            raise RuntimeError(f"JSON load failed: {str(e)}") from e

    def _get_pictograph_index(self) -> int:
        return self.beat_frame.get.index_of_currently_selected_beat() + 2

    def _get_color(self) -> str:
        """Retrieve the color of the motion being modified, as explicitly stored."""
        return self._color  # ✅ No more guessing – we now always use the correct color


# From motion_type_setter.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from ..turns_box.turns_widget.turns_widget import TurnsWidget


class MotionTypeSetter:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget

    def set_motion_type(self, motion: "Motion", motion_type: str) -> None:
        """Set the motion type and update the pictograph."""
        motion.state.motion_type = motion_type
        self.turns_widget.motion_type_label.update_display(motion_type)


# From turns_adjustment_manager.py
from PyQt6.QtCore import QObject

from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_button_manager import (
    PropRotDirButtonManager,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.motion_type_setter import (
    MotionTypeSetter,
)
from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat
from data.constants import FLOAT, NO_ROT
from objects.motion.motion import Motion

from .turns_value import TurnsValue
from main_window.main_window import TYPE_CHECKING
from .turns_command import AdjustTurnsCommand, SetTurnsCommand, TurnsCommand
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from .turns_state import TurnsState
    from .json_turns_repository import JsonTurnsRepository
    from .turns_presenter import TurnsPresenter


class TurnsAdjustmentManager(QObject):
    def __init__(
        self,
        state: "TurnsState",
        repository: "JsonTurnsRepository",
        presenter: "TurnsPresenter",
        color: str,
    ):
        super().__init__()
        self._state = state
        self._repo = repository
        self._presenter = presenter
        self._prop_rot_manager = None
        self._motion_type_setter = None
        self._color = color
        self._prefloat_motion_type = None
        self._prefloat_prop_rot_dir = None

        self._state.turns_changed.connect(self._on_turns_changed)
        self._state.validation_error.connect(self._presenter.show_error)

    def connect_prop_rot_dir_btn_mngr(self, manager: "PropRotDirButtonManager"):
        self._prop_rot_manager = manager

    def connect_motion_type_setter(self, setter: "MotionTypeSetter"):
        self._motion_type_setter = setter

    def adjust(self, delta: float):
        current_motion = self._current_motion()
        if current_motion and delta < 0 and self._state.current.raw_value == 0:
            self._store_prefloat_state(current_motion)

        command = AdjustTurnsCommand(self._state, delta, self._color)
        self._execute_command(command)

    def direct_set(self, value: TurnsValue):
        current_motion = self._current_motion()
        if (
            current_motion
            and self._state.current.raw_value != "fl"
            and value.raw_value == "fl"
        ):
            self._store_prefloat_state(current_motion)

        command = SetTurnsCommand(self._state, value, self._color)
        self._execute_command(command)

    def _store_prefloat_state(self, motion: "Motion"):
        self._prefloat_motion_type = motion.state.motion_type
        self._prefloat_prop_rot_dir = motion.state.prop_rot_dir

        beat_index = self._get_beat_index()
        if beat_index:
            json_manager = AppContext.json_manager()
            json_manager.updater.motion_type_updater.update_prefloat_motion_type_in_json(
                beat_index, self._color, self._prefloat_motion_type
            )
            json_manager.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
                beat_index, self._color, self._prefloat_prop_rot_dir
            )

    def _restore_prefloat_state(self, motion: "Motion"):
        beat_index = self._get_beat_index()
        if beat_index:
            json_manager = AppContext.json_manager()
            prefloat_motion_type = (
                json_manager.loader_saver.get_json_prefloat_motion_type(
                    beat_index, self._color
                )
            )
            prefloat_prop_rot_dir = (
                json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                    beat_index, self._color
                )
            )

            if prefloat_motion_type:
                self._prefloat_motion_type = prefloat_motion_type
            if prefloat_prop_rot_dir:
                self._prefloat_prop_rot_dir = prefloat_prop_rot_dir

        if self._prefloat_motion_type:
            motion.state.motion_type = self._prefloat_motion_type
            if self._motion_type_setter:
                self._motion_type_setter.set_motion_type(
                    motion, self._prefloat_motion_type
                )

        if self._prefloat_prop_rot_dir and self._prop_rot_manager:
            motion.state.prop_rot_dir = self._prefloat_prop_rot_dir
            self._prop_rot_manager.update_buttons_for_prop_rot_dir(
                self._prefloat_prop_rot_dir
            )

    def _get_beat_index(self) -> int:
        beat_frame = AppContext.sequence_beat_frame()
        current_beat = beat_frame.get.beat_number_of_currently_selected_beat()
        duration = beat_frame.get.duration_of_currently_selected_beat()
        return current_beat + duration

    def _execute_command(self, command: "TurnsCommand"):
        try:
            previous_value = self._state.current

            command.execute()

            current_motion = self._current_motion()
            if current_motion:
                if (
                    previous_value.raw_value != "fl"
                    and self._state.current.raw_value == "fl"
                ):
                    json_manager = AppContext.json_manager()

                    current_motion.state.motion_type = FLOAT
                    current_motion.state.prop_rot_dir = NO_ROT

                    beat_index = self._get_beat_index()
                    if beat_index:
                        json_manager.updater.motion_type_updater.update_motion_type_in_json(
                            beat_index, self._color, FLOAT
                        )
                        json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                            beat_index, self._color, NO_ROT
                        )

                    current_motion.pictograph.state.pictograph_data[
                        f"{self._color}_attributes"
                    ]["motion_type"] = FLOAT
                    current_motion.pictograph.state.pictograph_data[
                        f"{self._color}_attributes"
                    ]["prop_rot_dir"] = NO_ROT

                    self._prop_rot_manager.turns_box.header.update_turns_box_header()
                    self._prop_rot_manager.turns_box.header.hide_prop_rot_dir_buttons()
                    self._prop_rot_manager.turns_box.header.unpress_prop_rot_dir_buttons()
                    self._prop_rot_manager.update_pictograph_letter(
                        current_motion.pictograph
                    )
                elif (
                    previous_value.raw_value == "fl"
                    and self._state.current.raw_value != "fl"
                ):
                    self._restore_prefloat_state(current_motion)

                    beat_index = self._get_beat_index()
                    if (
                        beat_index
                        and self._prefloat_motion_type
                        and self._prefloat_prop_rot_dir
                    ):
                        json_manager = AppContext.json_manager()
                        json_manager.updater.motion_type_updater.update_motion_type_in_json(
                            beat_index, self._color, self._prefloat_motion_type
                        )
                        json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                            beat_index, self._color, self._prefloat_prop_rot_dir
                        )

                    if self._prefloat_motion_type:
                        current_motion.pictograph.state.pictograph_data[
                            f"{self._color}_attributes"
                        ]["motion_type"] = self._prefloat_motion_type
                    if self._prefloat_prop_rot_dir:
                        current_motion.pictograph.state.pictograph_data[
                            f"{self._color}_attributes"
                        ]["prop_rot_dir"] = self._prefloat_prop_rot_dir

            self._repo.save(self._state.current, self._color)
            self._sync_external_state()
        except Exception as e:
            self._presenter.show_error(str(e))

    def _on_turns_changed(self, new_value: TurnsValue):
        motion_type = self._determine_motion_type(new_value)
        self._presenter.update_display(new_value, motion_type)
        self._update_related_components(new_value)

    def _current_motion(self):
        current_beat = self._current_beat()
        if current_beat:
            return current_beat.elements.motion_set.get(self._color)
        return None

    def _update_related_components(self, value: TurnsValue):
        if self._prop_rot_manager:
            self._prop_rot_manager.update_for_turns_change(value)

        if self._motion_type_setter:
            motion_type = self._determine_motion_type(value)
            current_motion = self._current_motion()
            if current_motion:
                self._motion_type_setter.set_motion_type(current_motion, motion_type)

    def _determine_motion_type(self, value: TurnsValue) -> str:
        if value.raw_value == "fl":
            return FLOAT

        current_motion = self._current_motion()
        if current_motion:
            return current_motion.state.motion_type
        return "standard"

    def _sync_external_state(self):
        sequence = AppContext.json_manager().loader_saver.load_current_sequence()
        AppContext.sequence_beat_frame().updater.update_beats_from(sequence)

    def _current_beat(self) -> Beat:
        selected_beat_view = (
            AppContext.sequence_beat_frame().get.currently_selected_beat_view()
        )
        if selected_beat_view:
            return selected_beat_view.beat
        return None


# From turns_command.py
# Abstract command
from abc import ABC, abstractmethod

from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_state import (
    TurnsState,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
    TurnsValue,
)


class TurnsCommand(ABC):
    def __init__(self, state: TurnsState, color: str):  # ✅ Add color
        self._state = state
        self._color = color  # ✅ Store color

    @abstractmethod
    def execute(self):
        pass


class AdjustTurnsCommand(TurnsCommand):
    def __init__(self, state: TurnsState, delta: float, color: str):  # ✅ Pass color
        super().__init__(state, color)
        self._delta = delta

    def execute(self):
        new_value = self._state.current.adjust(self._delta)
        self._state.current = new_value


class SetTurnsCommand(TurnsCommand):
    def __init__(
        self, state: TurnsState, value: TurnsValue, color: str
    ):  # ✅ Pass color
        super().__init__(state, color)
        self._value = value

    def execute(self):
        self._state.current = self._value


# From turns_presenter.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox
from data.constants import ANTI, FLOAT, PRO

from ..turns_adjustment_manager.turns_value import TurnsValue

if TYPE_CHECKING:
    from ..turns_box.turns_widget.turns_widget import TurnsWidget
    from ..turns_box.turns_widget.motion_type_label import MotionTypeLabel


class TurnsPresenter:
    def __init__(self, turns_widget: "TurnsWidget", motion_type_label: "MotionTypeLabel"):
        self._motion_type_label = motion_type_label
        self.turns_widget = turns_widget

    def update_display(self, value: "TurnsValue", motion_type: str = None):
        self.turns_widget.display_frame.turns_label.setText(value.display_value)
        self._update_buttons(value, motion_type)
        if motion_type:
            self._update_motion_type(motion_type)
        elif value.raw_value == "fl":
            self._update_motion_type(FLOAT)

    def _update_buttons(self, value: "TurnsValue", motion_type: str):
        is_float = value.raw_value == "fl"
        if value.raw_value == 0 and motion_type in [PRO, ANTI]:
            self.turns_widget.display_frame.decrement_button.setEnabled(True)
            self.turns_widget.display_frame.increment_button.setEnabled(True)
        elif is_float:
            self.turns_widget.display_frame.decrement_button.setEnabled(False)
            self.turns_widget.display_frame.increment_button.setEnabled(True)
        else:
            self.turns_widget.display_frame.decrement_button.setEnabled(value.raw_value != 0)
            self.turns_widget.display_frame.increment_button.setEnabled(value.raw_value != 3)

        header = self.turns_widget.turns_box.header
        if is_float:
            header.hide_prop_rot_dir_buttons()
            header.unpress_prop_rot_dir_buttons()
        else:
            if value.raw_value > 0 or  motion_type in [PRO, ANTI]:
                header.show_prop_rot_dir_buttons()
            else:
                header.hide_prop_rot_dir_buttons()

    def _update_motion_type(self, motion_type: str):
        if not motion_type:
            return
        display_text = motion_type.capitalize()
        self._motion_type_label.update_display(display_text)

    def show_error(self, message):
        QMessageBox.critical(None, "Turns Error", message)


# From turns_repository.py
# Abstract repository
from abc import ABC, abstractmethod

from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
    TurnsValue,
)


class TurnsRepository(ABC):
    @abstractmethod
    def save(self, value: TurnsValue):
        pass

    @abstractmethod
    def load(self) -> TurnsValue:
        pass


# From turns_state.py
# src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/new_turns_adjustment_manager/turns_state.py
from PyQt6.QtCore import QObject, pyqtSignal
from .turns_value import TurnsValue

class TurnsState(QObject):
    turns_changed = pyqtSignal(TurnsValue)
    validation_error = pyqtSignal(str)

    def __init__(self, initial_value: TurnsValue):
        super().__init__()
        self._current_turns = initial_value

    @property
    def current(self) -> TurnsValue:
        return self._current_turns

    @current.setter
    def current(self, value: TurnsValue):
        try:
            if self._current_turns != value:
                self._validate_transition(value)
                self._current_turns = value
                self.turns_changed.emit(value)
        except ValueError as e:
            self.validation_error.emit(str(e))

    def _validate_transition(self, new_value: TurnsValue):
        """Ensure valid state transitions"""
        current = self._current_turns.raw_value
        new = new_value.raw_value
        
        if current == "fl" and new == 0:
            return  # Valid float to zero transition
        if current == 0 and new == "fl":
            return  # Valid zero to float transition
        if isinstance(new, (int, float)) and not (0 <= new <= 3):
            raise ValueError("Turns must be between 0 and 3")

# From turns_value.py
from typing import Union

class TurnsValue:
    def __init__(self, value: Union[int, float, str]):
        self._validate(value)
        self.raw_value = value

    @staticmethod
    def _validate(value):
        if not isinstance(value, (int, float, str)):
            raise ValueError("Invalid turns type")
        if isinstance(value, str) and value != "fl":
            raise ValueError("Invalid string value")
        if isinstance(value, (int, float)) and not (-0.5 <= value <= 3):
            raise ValueError("Turns out of range")

    @property
    def display_value(self) -> str:
        return (
            "fl"
            if self.raw_value == "fl"
            else str(float(self.raw_value)).rstrip("0").rstrip(".")
        )

    def adjust(self, delta: Union[int, float]) -> "TurnsValue":
        if self.raw_value == "fl":
            new_value = 0
        else:
            new_value = self.raw_value + delta

        if new_value < -0.5:
            return TurnsValue("fl")
        if new_value < 0:
            return TurnsValue("fl")
        return TurnsValue(min(3, new_value))

    def __eq__(self, other: "TurnsValue"):
        return self.raw_value == other.raw_value


# From __init__.py


# From __init__.py


# From turns_box.py
from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, HEX_BLUE, HEX_RED, OPP, SAME
from .prop_rot_dir_button_manager.prop_rot_dir_button_manager import (
    PropRotDirButtonManager,
)
from .turns_box_header import TurnsBoxHeader
from .turns_widget.turns_widget import TurnsWidget
from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from ..beat_adjustment_panel import BeatAdjustmentPanel
    from base_widgets.pictograph.pictograph import Pictograph


class TurnsBox(QFrame):
    def __init__(
        self,
        adjustment_panel: "BeatAdjustmentPanel",
        pictograph: "Pictograph",
        color: str,
    ) -> None:
        super().__init__(adjustment_panel)
        self.adjustment_panel = adjustment_panel
        self.color = color
        self.pictograph = pictograph
        self.graph_editor = self.adjustment_panel.graph_editor
        self.matching_motion = self.pictograph.managers.get.motion_by_color(self.color)
        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.prop_rot_dir_btn_state: dict[str, bool] = {
            CLOCKWISE: False,
            COUNTER_CLOCKWISE: False,
        }
        self.setObjectName(self.__class__.__name__)

        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.header = TurnsBoxHeader(self)
        self.prop_rot_dir_button_manager = PropRotDirButtonManager(self)
        self.turns_widget = TurnsWidget(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.turns_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resizeEvent(self, event):
        border_width = self.graph_editor.sequence_workbench.width() // 200
        # Convert named colors to hex
        color_hex = (
            HEX_RED
            if self.color == "red"
            else HEX_BLUE if self.color == "blue" else self.color
        )
        # Convert hex to RGB
        r, g, b = (
            int(color_hex[1:3], 16),
            int(color_hex[3:5], 16),
            int(color_hex[5:7], 16),
        )
        # Whiten the color by blending with white (255, 255, 255)
        whitened_r = min(255, r + (255 - r) // 2)
        whitened_g = min(255, g + (255 - g) // 2)
        whitened_b = min(255, b + (255 - b) // 2)
        whitened_color = f"rgb({whitened_r}, {whitened_g}, {whitened_b})"
        self.setStyleSheet(
            f"#{self.__class__.__name__} {{ border: {border_width}px solid "
            f"{color_hex}; background-color: {whitened_color};}}"
        )
        self.turns_widget.resizeEvent(event)
        self.header.resizeEvent(event)
        super().resizeEvent(event)


# From turns_box_header.py
from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, NO_ROT
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_button import PropRotDirButton
from ..base_adjustment_box_header_widget import BaseAdjustmentBoxHeaderWidget
from utils.path_helpers import get_image_path
from data.constants import ICON_DIR

if TYPE_CHECKING:
    from .turns_box import TurnsBox


class TurnsBoxHeader(BaseAdjustmentBoxHeaderWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.graph_editor = self.turns_box.adjustment_panel.graph_editor
        self.main_widget = self.graph_editor.main_widget

        # ✅ Create buttons HERE, not in PropRotDirButtonManager
        self.cw_button = PropRotDirButton(
            self.turns_box, CLOCKWISE, get_image_path(f"{ICON_DIR}clock/clockwise.png")
        )
        self.ccw_button = PropRotDirButton(
            self.turns_box, COUNTER_CLOCKWISE, get_image_path(f"{ICON_DIR}clock/counter_clockwise.png")
        )

        self._add_widgets()

    def update_turns_box_header(self) -> None:
        """Update the header to display correct buttons based on motion type."""
        pictograph = self.turns_box.graph_editor.pictograph_container.GE_view.pictograph
        motion = pictograph.managers.get.motion_by_color(self.turns_box.color)

        if motion.state.prop_rot_dir == NO_ROT:
            self.hide_prop_rot_dir_buttons()
        else:
            self.show_prop_rot_dir_buttons()
            if motion.state.prop_rot_dir == CLOCKWISE:
                self.cw_button.set_selected(True)
                self.ccw_button.set_selected(False)
            elif motion.state.prop_rot_dir == COUNTER_CLOCKWISE:
                self.ccw_button.set_selected(True)
                self.cw_button.set_selected(False)

    def _add_widgets(self) -> None:
        """Add buttons to the header layout."""
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.ccw_button)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.header_label)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.cw_button)
        self.top_hbox.addStretch(1)
        self.separator_hbox.addWidget(self.separator)

    def show_prop_rot_dir_buttons(self) -> None:
        self.cw_button.show()
        self.ccw_button.show()

    def hide_prop_rot_dir_buttons(self) -> None:
        self.cw_button.hide()
        self.ccw_button.hide()

    def resizeEvent(self, event):
        self.cw_button.resizeEvent(event)
        self.ccw_button.resizeEvent(event)
        super().resizeEvent(event)

    def unpress_prop_rot_dir_buttons(self) -> None:
        self.cw_button.set_selected(True)
        self.ccw_button.set_selected(True)

# From __init__.py


# From prop_rot_dir_btn_state.py
# === prop_rot_dir_button_manager/core.py ===
from PyQt6.QtCore import QObject, pyqtSignal
from typing import TYPE_CHECKING, Dict

from data.constants import CLOCKWISE, COUNTER_CLOCKWISE

if TYPE_CHECKING:
    pass


class PropRotationState(QObject):
    """Manages the state machine for rotation directions"""

    state_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._state: Dict[str, bool] = {CLOCKWISE: False, COUNTER_CLOCKWISE: False}

    def update_state(self, direction: str, value: bool):
        """Atomic state update with validation"""
        if direction not in self._state:
            return
        self._state = {
            k: (v if k == direction else not v) for k, v in self._state.items()
        }
        self.state_changed.emit(self._state)

    @property
    def current(self):
        return self._state.copy()


# From prop_rot_dir_button.py
# ==========================================
# File: prop_rot_dir_button.py
# ==========================================
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QSize

from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.turns_box import (
        TurnsBox,
    )


class PropRotDirButton(StyledButton):
    def __init__(
        self, turns_box: "TurnsBox", prop_rot_dir: str, icon_path: str
    ) -> None:
        super().__init__(label="", icon_path=icon_path)
        self.turns_box = turns_box
        self.prop_rot_dir = prop_rot_dir

        self._setup_button()
        self.clicked.connect(
            lambda: self.turns_box.prop_rot_dir_button_manager.set_prop_rot_dir(
                self.prop_rot_dir
            )
        )

    def _setup_button(self) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Set {self.prop_rot_dir.replace('_', ' ').title()} Rotation")

    def update_state_dict(self, state_dict: dict, value: bool) -> None:
        state_dict[self.prop_rot_dir] = value

    def resizeEvent(self, event) -> None:
        button_size = int(self.turns_box.graph_editor.height() * 0.25)
        icon_size = int(button_size * 0.8)
        self.setFixedSize(button_size, button_size)
        self.setIconSize(QSize(icon_size, icon_size))
        super().resizeEvent(event)


# From prop_rot_dir_button_manager.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from data.constants import (
    END_ORI,
    LETTER,
    MOTION_TYPE,
    NO_ROT,
    PROP_ROT_DIR,
    TURNS,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
    TurnsValue,
)
from base_widgets.pictograph.pictograph import Pictograph
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_btn_state import (
    PropRotationState,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_logic_handler import (
    PropRotDirLogicHandler,
)
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class PropRotDirButtonManager:
    def __init__(self, turns_box: "TurnsBox") -> None:
        self.turns_box = turns_box
        self.state = PropRotationState()
        self.logic_handler = PropRotDirLogicHandler(turns_box, self.state)

        self.state.state_changed.connect(self.turns_box.header.update_turns_box_header)

    def update_buttons_for_prop_rot_dir(self, prop_rot_dir: str) -> None:
        """Update the button UI to reflect the given prop rotation direction."""
        if prop_rot_dir == NO_ROT:
            # Handle the NO_ROT case - unselect all buttons
            self.state.update_state(CLOCKWISE, False)  # Clear all selections
            if hasattr(self.turns_box.header, "unpress_prop_rot_dir_buttons"):
                self.turns_box.header.unpress_prop_rot_dir_buttons()
        else:
            # Set the state for the given direction
            self.state.update_state(prop_rot_dir, True)

            # Update header buttons visually
            header = self.turns_box.header
            if prop_rot_dir == CLOCKWISE:
                if hasattr(header, "cw_button"):
                    header.cw_button.set_selected(True)
                if hasattr(header, "ccw_button"):
                    header.ccw_button.set_selected(False)
            else:  # COUNTER_CLOCKWISE
                if hasattr(header, "cw_button"):
                    header.cw_button.set_selected(False)
                if hasattr(header, "ccw_button"):
                    header.ccw_button.set_selected(True)

            # Make sure buttons are visible
            if hasattr(header, "show_prop_rot_dir_buttons"):
                header.show_prop_rot_dir_buttons()

    def set_prop_rot_dir(self, prop_rot_dir: str) -> None:
        """Set the prop rotation direction and update the motion and letter."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        if self.turns_box.prop_rot_dir_btn_state[prop_rot_dir]:
            return

        self.logic_handler.update_rotation_states(prop_rot_dir)
        self.logic_handler.update_related_components()

        self.turns_box.graph_editor.sequence_workbench.main_widget.construct_tab.option_picker.updater.refresh_options()

        QApplication.restoreOverrideCursor()

    def update_for_motion_change(self, motion: "Motion") -> None:
        """Update buttons when motion changes."""
        self.logic_handler.current_motion = motion

        self.turns_box.header.update_turns_box_header()

        if motion.state.turns > 0 and motion.state.prop_rot_dir == NO_ROT:
            self.set_prop_rot_dir(self.logic_handler._get_default_prop_rot_dir())

    def update_for_turns_change(self, value: "TurnsValue") -> None:
        """Update buttons when turns change."""

        # Ensure valid motion reference
        if not self.logic_handler.current_motion:
            return

        motion = self.logic_handler.current_motion

        # If turns are zero or float, reset rotation direction
        if value.raw_value == 0 or value.raw_value == "fl":
            self.set_prop_rot_dir(NO_ROT)  # Reset to default if no turns

        # If turns are non-zero, ensure a valid rotation direction is set
        elif motion.state.prop_rot_dir == NO_ROT:
            default_dir = self.logic_handler._get_default_prop_rot_dir()
            self.set_prop_rot_dir(default_dir)

        # Sync button states
        self.state.update_state(motion.state.prop_rot_dir, True)

        # Update pictograph and JSON
        self._update_pictograph_and_json(motion)

        # Refresh UI to reflect changes
        self.turns_box.header.update_turns_box_header()

    def set_motion(self, motion: "Motion") -> None:
        """Called when motion changes to update UI and logic states."""
        self.update_for_motion_change(motion)

    def update_pictograph_letter(self, pictograph: "Pictograph") -> None:
        new_letter = (
            self.turns_box.graph_editor.main_widget.letter_determiner.determine_letter(
                pictograph.state.pictograph_data, swap_prop_rot_dir=True
            )
        )
        self.json_manager = (
            self.turns_box.graph_editor.sequence_workbench.main_widget.json_manager
        )
        self.beat_frame = (
            self.turns_box.graph_editor.sequence_workbench.main_widget.sequence_workbench.beat_frame
        )
        if new_letter:
            pictograph.state.pictograph_data[LETTER] = new_letter.value
            pictograph.state.letter = new_letter
            pictograph.managers.updater.update_pictograph(
                pictograph.state.pictograph_data
            )

        if new_letter:
            json_updater = self.json_manager.updater
            pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
            json_index = pictograph_index + 2
            json_updater.letter_updater.update_letter_in_json_at_index(
                json_index, new_letter.value
            )

    def _update_pictograph_and_json(self, motion: "Motion") -> None:
        """Update the pictograph and JSON with the new letter and motion attributes."""
        self.beat_frame = self.turns_box.graph_editor.sequence_workbench.beat_frame
        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        self.graph_editor = self.turns_box.graph_editor
        self.json_manager = self.graph_editor.main_widget.json_manager
        beat = motion.pictograph
        new_dict = {
            MOTION_TYPE: motion.state.motion_type,
            PROP_ROT_DIR: motion.state.prop_rot_dir,
            END_ORI: motion.state.end_ori,
            TURNS: motion.state.turns,
        }

        beat.state.pictograph_data[motion.state.color + "_attributes"].update(new_dict)

        beat.managers.updater.update_pictograph(beat.state.pictograph_data)
        json_index = pictograph_index + 2
        json_updater = self.json_manager.updater
        self.turns_box.turns_widget.motion_type_label.update_display(
            motion.state.motion_type
        )
        json_updater.motion_type_updater.update_motion_type_in_json(
            json_index, motion.state.color, motion.state.motion_type
        )
        json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
            json_index, motion.state.color, motion.state.prop_rot_dir
        )
        self.graph_editor.main_widget.json_manager.ori_validation_engine.run(
            is_current_sequence=True
        )
        self.graph_editor.sequence_workbench.beat_frame.updater.update_beats_from_current_sequence_json()
        self.graph_editor.main_widget.sequence_workbench.current_word_label.set_current_word(
            self.graph_editor.sequence_workbench.beat_frame.get.current_word()
        )


# From prop_rot_dir_logic_handler.py
# ==========================================
# File: prop_rot_dir_logic_handler.py
# ==========================================
from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal
from data.constants import ANTI, CLOCKWISE, PRO
from objects.motion.motion import Motion
from base_widgets.pictograph.pictograph import Pictograph
from utils.reversal_detector import ReversalDetector

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_ui_handler import (
        PropRotDirUIHandler,
    )
    from ..turns_box import TurnsBox


class PropRotDirLogicHandler(QObject):
    rotation_updated = pyqtSignal(dict)

    def __init__(
        self, turns_box: "TurnsBox", ui_handler: "PropRotDirUIHandler"
    ) -> None:
        super().__init__()
        self.turns_box = turns_box
        self.ui_handler = ui_handler
        self.current_motion: "Motion" = None

    def validate_rotation_change(self, new_direction: str) -> bool:
        """Check if rotation change is valid."""
        return (
            not self.turns_box.prop_rot_dir_btn_state[new_direction]
            and self.current_motion is not None
        )

    def update_rotation_states(self, new_direction: str) -> None:
        """Update all related states for rotation change."""
        self.update_button_states(new_direction)
        self._update_motion_properties(new_direction)
        self._update_pictograph_data()
        self._detect_reversals()
        self.update_related_components()

        # Refresh UI elements
        self.turns_box.graph_editor.sequence_workbench.main_widget.construct_tab.option_picker.updater.refresh_options()

    def update_button_states(self, direction: str) -> None:
        """✅ Update button states in TurnsBoxHeader instead of missing `ui_handler`."""
        self.turns_box.prop_rot_dir_button_manager.state.update_state(direction, True)

        # ✅ Update the buttons inside the TurnsBoxHeader
        header = self.turns_box.header
        if direction == CLOCKWISE:
            header.cw_button.set_selected(True)
            header.ccw_button.set_selected(False)
        else:
            header.ccw_button.set_selected(True)
            header.cw_button.set_selected(False)

    def _update_motion_properties(self, direction: str) -> None:
        """Update motion objects with new rotation direction."""
        for pictograph in self._get_affected_pictographs():
            motion = pictograph.managers.get.motion_by_color(self.turns_box.color)
            motion.state.prop_rot_dir = direction
            motion.state.motion_type = self._determine_motion_type(motion)

        # Update pictographs & JSON
        self.turns_box.graph_editor.sequence_workbench.beat_frame.updater.update_beats_from_current_sequence_json()
        self.turns_box.graph_editor.main_widget.json_manager.ori_validation_engine.run(
            is_current_sequence=True
        )

    def _update_pictograph_data(self) -> None:
        """Update pictograph JSON data after a rotation change."""
        pictograph_index = (
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
        )
        json_index = pictograph_index + 2  # JSON stores additional metadata

        json_updater = self.turns_box.graph_editor.main_widget.json_manager.updater

        for pictograph in self._get_affected_pictographs():
            motion = pictograph.managers.get.motion_by_color(self.turns_box.color)
            new_data = {
                "motion_type": motion.state.motion_type,
                "prop_rot_dir": motion.state.prop_rot_dir,
                "end_ori": motion.state.end_ori,
                "turns": motion.state.turns,
            }
            pictograph.state.pictograph_data[motion.state.color + "_attributes"].update(
                new_data
            )
            pictograph.managers.updater.update_pictograph(
                pictograph.state.pictograph_data
            )

            # Sync changes with JSON
            json_updater.motion_type_updater.update_motion_type_in_json(
                json_index, motion.state.color, motion.state.motion_type
            )
            json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                json_index, motion.state.color, motion.state.prop_rot_dir
            )

    def _detect_reversals(self) -> None:
        """Detect motion reversals and update pictograph UI accordingly."""
        pictograph_index = (
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
        )
        sequence_so_far = self.turns_box.graph_editor.main_widget.json_manager.loader_saver.load_current_sequence()[
            : pictograph_index + 2
        ]

        for pictograph in self._get_affected_pictographs():
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, pictograph.state.pictograph_data
            )

            pictograph.state.blue_reversal = reversal_info["blue_reversal"]
            pictograph.state.red_reversal = reversal_info["red_reversal"]

            # Update UI with reversal symbols
            pictograph.elements.reversal_glyph.update_reversal_symbols()

    def _get_affected_pictographs(self) -> list[Pictograph]:
        """Retrieve pictographs that need updating due to rotation changes."""
        selected_beat = (
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.currently_selected_beat_view()
        )
        if not selected_beat:
            return []

        return [
            selected_beat.beat,
            self.turns_box.graph_editor.pictograph_container.GE_view.pictograph,
        ]

    def _determine_motion_type(self, motion: "Motion") -> str:
        """Determine new motion type based on rotation."""
        if motion.state.motion_type == ANTI:
            return PRO
        elif motion.state.motion_type == PRO:
            return ANTI
        return motion.state.motion_type

    def _get_default_prop_rot_dir(self) -> str:
        """Set default prop rotation direction to clockwise."""
        self.turns_box.prop_rot_dir_button_manager.state.update_state(CLOCKWISE, True)
        return CLOCKWISE

    def update_related_components(self) -> None:
        """Updates JSON, detects reversals, updates UI labels, and ensures UI consistency."""
        pictograph_index = (
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
        )
        json_index = pictograph_index + 2  # JSON stores additional metadata

        # Update JSON data
        json_updater = self.turns_box.graph_editor.main_widget.json_manager.updater

        for pictograph in self._get_affected_pictographs():
            motion = pictograph.managers.get.motion_by_color(self.turns_box.color)
            new_data = {
                "motion_type": motion.state.motion_type,
                "prop_rot_dir": motion.state.prop_rot_dir,
                "end_ori": motion.state.end_ori,
                "turns": motion.state.turns,
            }
            pictograph.state.pictograph_data[motion.state.color + "_attributes"].update(
                new_data
            )
            pictograph.managers.updater.update_pictograph(
                pictograph.state.pictograph_data
            )

            # Sync changes with JSON
            json_updater.motion_type_updater.update_motion_type_in_json(
                json_index, motion.state.color, motion.state.motion_type
            )
            json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                json_index, motion.state.color, motion.state.prop_rot_dir
            )

        # Run orientation validation
        self.turns_box.graph_editor.main_widget.json_manager.ori_validation_engine.run(
            is_current_sequence=True
        )

        # Detect reversals
        self._detect_reversals()

        # Update UI labels and letters
        self.turns_box.graph_editor.sequence_workbench.beat_frame.updater.update_beats_from_current_sequence_json()
        self.turns_box.graph_editor.main_widget.sequence_workbench.current_word_label.set_current_word(
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.current_word()
        )

        # Also update the letter
        self.turns_box.prop_rot_dir_button_manager.update_pictograph_letter(pictograph)


# From prop_rot_dir_ui_handler.py
# ==========================================
# File: prop_rot_dir_ui_handler.py
# ==========================================
from typing import TYPE_CHECKING
from objects.arrow.arrow import Motion
from utils.path_helpers import get_image_path
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR
from .prop_rot_dir_button import PropRotDirButton

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class PropRotDirUIHandler:
    def __init__(self, turns_box: "TurnsBox") -> None:
        self.turns_box = turns_box
        self.buttons = []

    def setup_buttons(self) -> None:
        """Initialize rotation direction buttons."""
        self.buttons = [
            self._create_button(CLOCKWISE, "clockwise.png"),
            self._create_button(COUNTER_CLOCKWISE, "counter_clockwise.png"),
        ]
        self._arrange_buttons()

    def _create_button(self, direction, icon_name) -> PropRotDirButton:
        """Factory method for creating buttons."""
        button = PropRotDirButton(
            self.turns_box, direction, get_image_path(f"{ICON_DIR}clock/{icon_name}")
        )
        button.clicked.connect(
            lambda _, d=direction: self.turns_box.prop_rot_dir_button_manager.set_prop_rot_dir(
                d
            )
        )
        return button

    def sync_button_states(self) -> None:
        """Sync UI states with the current rotation state."""
        current_state = self.turns_box.prop_rot_dir_button_manager.state.current
        for button in self.buttons:
            is_active = current_state.get(button.prop_rot_dir, False)
            button.set_selected(is_active)
            button.setVisible(True)  # Ensure visibility sync

    def handle_button_visibility(self, motion: Motion) -> None:
        """Control button visibility based on motion state."""
        if motion.state.turns == 0:
            self._hide_all_buttons()
        elif motion.state.turns == "fl":
            self._hide_all_buttons()
        else:
            self._show_all_buttons()

    def _hide_all_buttons(self) -> None:
        for button in self.buttons:
            button.hide()

    def _show_all_buttons(self) -> None:
        for button in self.buttons:
            button.show()

    def _arrange_buttons(self) -> None:
        """Arrange buttons in the UI layout."""
        layout = self.turns_box.layout()
        for button in self.buttons:
            layout.addWidget(button)


# From __init__.py


# From __init__.py


# From motion_type_label.py
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget


class MotionTypeLabel(QLabel):
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__("", turns_widget)
        self.turns_widget = turns_widget
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_display(self, motion_type: str) -> None:
        """Update the display based on the motion type."""
        self.setText(motion_type.capitalize())

    def resizeEvent(self, event) -> None:
        """Resize the label based on the parent widget size."""
        font_size = self.turns_widget.turns_box.graph_editor.width() // 40
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        self.setFont(font)


# From turns_text_label.py
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget


class TurnsTextLabel(QLabel):
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__("Turns", turns_widget)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_widget = turns_widget

    def resizeEvent(self, event) -> None:
        font_size = self.turns_widget.turns_box.graph_editor.width() // 50
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.setFont(font)
        super().resizeEvent(event)


# From turns_widget.py
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from typing import TYPE_CHECKING

from ...turns_adjustment_manager.json_turns_repository import JsonTurnsRepository
from ...turns_adjustment_manager.turns_adjustment_manager import (
    TurnsAdjustmentManager,
)
from ...turns_adjustment_manager.turns_presenter import TurnsPresenter
from ...turns_adjustment_manager.turns_state import TurnsState
from ...turns_adjustment_manager.turns_value import TurnsValue
from ...turns_box.turns_widget.turns_display_frame.turns_display_frame import (
    TurnsDisplayFrame,
)

from .turns_text_label import TurnsTextLabel
from ...turns_adjustment_manager.motion_type_setter import MotionTypeSetter
from .direct_set_dialog.direct_set_turns_dialog import DirectSetTurnsDialog
from .motion_type_label import MotionTypeLabel
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class TurnsWidget(QWidget):
    turns_adjusted = pyqtSignal()

    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self._setup_components()
        self._setup_layout()
        self._connect_signals()

        
        if hasattr(self.turns_box.graph_editor, "pictograph_selected"):
            self.turns_box.graph_editor.pictograph_selected.connect(
                self.reset_state_for_new_pictograph
            )

    def _setup_components(self) -> None:
        
        initial_value = self._get_initial_turns_value()
        self.state = TurnsState(initial_value)

        self.repository = JsonTurnsRepository(AppContext.json_manager())
        self.motion_type_label = MotionTypeLabel(self)
        self.presenter = TurnsPresenter(self, self.motion_type_label)
        self.adjustment_manager = TurnsAdjustmentManager(
            self.state, self.repository, self.presenter, self.turns_box.color
        )
        self.display_frame = TurnsDisplayFrame(self)
        self.turns_text = TurnsTextLabel(self)
        self.motion_type_setter = MotionTypeSetter(self)
        self.direct_set_dialog = DirectSetTurnsDialog(self)

        self.adjustment_manager.connect_prop_rot_dir_btn_mngr(
            self.turns_box.prop_rot_dir_button_manager
        )
        self.adjustment_manager.connect_motion_type_setter(self.motion_type_setter)

        
        current_motion = self._get_current_motion()
        if current_motion:
            motion_type = current_motion.state.motion_type
            self.presenter.update_display(initial_value, motion_type)

    def _get_initial_turns_value(self) -> TurnsValue:
        """Get the initial turns value from the current pictograph"""
        try:
            current_motion = self._get_current_motion()
            if current_motion:
                turns_value = current_motion.state.turns
                print(f"Initial turns value: {turns_value}")
                return TurnsValue(turns_value)
        except (AttributeError, KeyError) as e:
            print(f"Error getting initial turns value: {e}")
        return TurnsValue(0)  

    def _get_current_motion(self):
        """Get the current motion based on the color"""
        try:
            current_beat = (
                self.turns_box.graph_editor.pictograph_container.GE_view.pictograph
            )
            return current_beat.elements.motion_set[self.turns_box.color]
        except (AttributeError, KeyError) as e:
            print(f"Error getting current motion: {e}")
            return None

    def reset_state_for_new_pictograph(self) -> None:
        """Reset the turns state when a new pictograph is selected"""
        try:
            current_motion = self._get_current_motion()
            if not current_motion:
                return

            new_value = current_motion.state.turns
            motion_type = current_motion.state.motion_type
            print(f"Resetting turns state to: {new_value}, motion type: {motion_type}")

            
            new_turns_value = TurnsValue(new_value)

            
            self.state.current = new_turns_value

            
            self.presenter.update_display(new_turns_value, motion_type)

            
            if new_value == "fl" and hasattr(
                self.adjustment_manager, "_prefloat_motion_type"
            ):
                
                beat_index = self.adjustment_manager._get_beat_index()
                if beat_index:
                    json_manager = AppContext.json_manager()
                    prefloat_motion_type = (
                        json_manager.loader_saver.get_json_prefloat_motion_type(
                            beat_index, self.turns_box.color
                        )
                    )
                    prefloat_prop_rot_dir = (
                        json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                            beat_index, self.turns_box.color
                        )
                    )

                    
                    if prefloat_motion_type:
                        self.adjustment_manager._prefloat_motion_type = (
                            prefloat_motion_type
                        )
                    if prefloat_prop_rot_dir:
                        self.adjustment_manager._prefloat_prop_rot_dir = (
                            prefloat_prop_rot_dir
                        )

        except (AttributeError, KeyError) as e:
            print(f"Error resetting turns state: {e}")

    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.turns_text, 1)
        layout.addWidget(self.display_frame, 3)
        layout.addWidget(self.motion_type_label, 1)

    def _connect_signals(self):
        self.state.turns_changed.connect(self._notify_external_components)


    def _handle_direct_set(self):
        current = self.state.current
        options = [TurnsValue(v) for v in [0, 0.5, 1, 1.5, 2, 2.5, 3, "fl"]]
        value = self.direct_set_dialog.get_value(options, current)
        if value:
            self.adjustment_manager.direct_set(value)

    def _notify_external_components(self):
        self.turns_adjusted.emit()
        
        if (
            hasattr(self.turns_box, "adjustment_panel")
            and hasattr(self.turns_box.adjustment_panel, "graph_editor")
            and hasattr(self.turns_box.adjustment_panel.graph_editor, "main_widget")
            and hasattr(
                self.turns_box.adjustment_panel.graph_editor.main_widget,
                "settings_dialog",
            )
            and hasattr(
                self.turns_box.adjustment_panel.graph_editor.main_widget.settings_dialog,
                "ui",
            )
            and hasattr(
                self.turns_box.adjustment_panel.graph_editor.main_widget.settings_dialog.ui,
                "image_export_tab",
            )
        ):
            self.turns_box.adjustment_panel.graph_editor.main_widget.settings_dialog.ui.image_export_tab.update_preview()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "display_frame"):
            self.display_frame.resizeEvent(event)
        if hasattr(self, "turns_text"):
            self.turns_text.resizeEvent(event)
        if hasattr(self, "motion_type_label"):
            self.motion_type_label.resizeEvent(event)
        if hasattr(self, "direct_set_dialog"):
            self.direct_set_dialog.resizeEvent(event)

    
    def showEvent(self, event):
        super().showEvent(event)
        
        self.reset_state_for_new_pictograph()


# From __init__.py


# From direct_set_turns_button.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from data.constants import BLUE, HEX_BLUE, HEX_RED

if TYPE_CHECKING:
    from .direct_set_turns_dialog import DirectSetTurnsDialog


class DirectSetTurnsButton(QPushButton):
    def __init__(self, value, direct_set_dialog: "DirectSetTurnsDialog") -> None:
        super().__init__(value)
        self.turns_widget = direct_set_dialog.turns_widget
        self.turns_box = self.turns_widget.turns_box
        self.clicked.connect(self.direct_set_adjustment)
        self.setMouseTracking(True)

    def enterEvent(self, event) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event) -> None:
        QApplication.restoreOverrideCursor()

    def direct_set_adjustment(self):
        pass

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        button_size = self.turns_box.height() // 2
        turns_display_font_size = int(
            self.turns_box.adjustment_panel.graph_editor.height() / 6
        )
        self.setFixedSize(QSize(button_size, button_size))
        self.setFont(QFont("Arial", turns_display_font_size, QFont.Weight.Bold))
        self.setStyleSheet(
            f"""
            QPushButton {{
                border: 4px solid {HEX_BLUE if self.turns_box.color == BLUE else HEX_RED};
                border-radius: {button_size // 2}px;
                background-color: white;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
        """
        )


# From direct_set_turns_dialog.py
from PyQt6.QtWidgets import QDialog, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from data.constants import ANTI, BLUE, FLOAT, HEX_BLUE, HEX_RED, PRO
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import TurnsValue
from .direct_set_turns_button import DirectSetTurnsButton

if TYPE_CHECKING:
    from ..turns_widget import TurnsWidget
from PyQt6.QtWidgets import QHBoxLayout


class DirectSetTurnsDialog(QDialog):
    buttons: dict[str, DirectSetTurnsButton] = {}

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(
            turns_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.turns_display_frame = turns_widget.display_frame
        self.adjustment_manager = turns_widget.adjustment_manager
        self._set_dialog_style()
        self._setup_buttons()
        self._setup_layout()

    def _set_dialog_style(self):
        border_color = HEX_BLUE if self.turns_box.color == BLUE else HEX_RED
        self.setStyleSheet(
            f"""
            QDialog {{
                border: 2px solid {border_color};
                border-radius: 5px;
            }}
        """
        )

    def _setup_buttons(self):
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]  
        if self.turns_box.matching_motion.state.motion_type in [PRO, ANTI, FLOAT]:
            turns_values.insert(0, "fl")
        for value in turns_values:
            button = DirectSetTurnsButton(value, self)
            
            button.clicked.connect(
                lambda _, v=value: self.select_turns(
                    "fl" if v == "fl" else float(v) if "." in v else int(v)
                )
            )
            self.buttons[value] = button

    def _setup_layout(self):
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for button in self.buttons.values():
            layout.addWidget(button)
        self.adjustSize()

    def show_direct_set_dialog(self) -> None:

        self.resize_direct_set_buttons()
        turns_label_rect = self.turns_display_frame.turns_label.geometry()
        global_turns_label_pos = self.turns_display_frame.turns_label.mapToGlobal(
            self.turns_display_frame.turns_label.pos()
        )
        
        turns_widget_pos = self.turns_widget.mapToGlobal(self.turns_widget.pos())
        dialog_x = turns_widget_pos.x()
        dialog_y = global_turns_label_pos.y() + turns_label_rect.height()
        self.move(int(dialog_x), int(dialog_y))
        self.exec()

    def resize_direct_set_buttons(self) -> None:

        self.adjustSize()
        self.updateGeometry()

    def select_turns(self, value):
        self.turns_widget.adjustment_manager.direct_set(TurnsValue(value))
        self.accept()


# From __init__.py


# From __init__.py


# From adjust_turns_button.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QRectF, QByteArray
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QCursor,
    QPen,
)
from PyQt6.QtSvg import QSvgRenderer

from data.constants import BLUE, RED
from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from ..turns_widget import TurnsWidget


class AdjustTurnsButton(StyledButton):
    def __init__(self, svg_path, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.svg_path = svg_path
        self.turns_widget = turns_widget
        self.turns_box = self.turns_widget.turns_box
        self.svg_renderer = QSvgRenderer(svg_path)
        self.hovered = False
        self.pressed = False
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw a translucent white background if hovered
        if self.hovered and self.isEnabled():
            painter.fillRect(self.rect(), QColor(255, 255, 255, 80))

        turns_box_color = self.turns_widget.turns_box.color
        if turns_box_color == RED:
            border_color = "#ED1C24"
        elif turns_box_color == BLUE:
            border_color = "#2E3192"
        else:
            border_color = "black"

        # If hovered, draw a white border. If pressed, use the turns_box color. Otherwise black border.
        if self.isEnabled():
            if self.hovered:
                painter.setPen(QPen(QColor("white"), 4))
            elif self.pressed:
                painter.setPen(QPen(QColor(f"{border_color}"), 5))
            else:
                painter.setPen(QPen(QColor("black"), 2))

        icon_size = int(min(self.width(), self.height()) * 0.9)
        x = (self.width() - icon_size) / 2
        y = (self.height() - icon_size) / 2
        icon_rect = QRectF(x, y, icon_size, icon_size)
        self.svg_renderer.render(painter, icon_rect)
        painter.end()

    def mousePressEvent(self, event):
        self.pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event) -> None:
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.hovered = True
        self.update()

    def leaveEvent(self, event) -> None:
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.hovered = False
        self.update()

    def setEnabled(self, enabled) -> None:
        super().setEnabled(enabled)
        svgData = QByteArray()
        with open(self.svg_path, "r") as file:
            svgData = QByteArray(file.read().encode("utf-8"))

        if not enabled:
            svgData.replace(b"black", b"gray")

        self.svg_renderer.load(svgData)
        self.update()

    def resizeEvent(self, event) -> None:
        size = int(self.turns_box.graph_editor.height() * 0.3)
        self.setMaximumWidth(size)
        self.setMaximumHeight(size)
        super().resizeEvent(event)


# From GE_turns_label.py
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from data.constants import BLUE, RED

if TYPE_CHECKING:
    from .turns_display_frame import TurnsDisplayFrame


class GE_TurnsLabel(QLabel):
    """This is the colored box that displays the turns number inside the turns box display frame of the graph editor."""

    clicked = pyqtSignal()

    def __init__(self, turns_display_frame: "TurnsDisplayFrame") -> None:
        super().__init__()
        self.turns_box = turns_display_frame.turns_box
        self.turns_display_font_size = 20
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()

    def resizeEvent(self, event) -> None:
        self.turns_display_font_size = int(
            (self.turns_box.adjustment_panel.graph_editor.width() / 22)
        )
        self.setFont(QFont("Arial", self.turns_display_font_size, QFont.Weight.Bold))
        self.setMaximumWidth(
            int(self.turns_box.adjustment_panel.graph_editor.width() / 9)
        )
        self.setMaximumHeight(
            int(self.turns_box.adjustment_panel.graph_editor.height() / 4)
        )
        border_radius = self.width() // 4

        turn_display_border = int(self.width() / 20)

        turns_box_color = self.turns_box.color
        if turns_box_color == RED:
            border_color = "#ED1C24"
        elif turns_box_color == BLUE:
            border_color = "#2E3192"
        else:
            border_color = "black"

        self.setStyleSheet(
            f"""
            QLabel {{
                border: {turn_display_border}px solid {border_color};
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )
        super().resizeEvent(event)


# From turns_display_frame.py
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from typing import TYPE_CHECKING

from data.constants import ANTI, FLOAT, PRO
from objects.motion.motion import Motion

from .adjust_turns_button import AdjustTurnsButton
from .GE_turns_label import GE_TurnsLabel
from utils.path_helpers import get_image_path

if TYPE_CHECKING:
    from ..turns_widget import TurnsWidget


class TurnsDisplayFrame(QFrame):
    """This is the frame that contains the turns label and the buttons to adjust the turns."""

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.adjustment_manager = turns_widget.adjustment_manager
        self._setup_components()
        self._attach_listeners()
        self._setup_layout()

    def _setup_components(self) -> None:
        plus_path = get_image_path("icons/plus.svg")
        minus_path = get_image_path("icons/minus.svg")
        self.increment_button = AdjustTurnsButton(plus_path, self)
        self.decrement_button = AdjustTurnsButton(minus_path, self)
        self.turns_label = GE_TurnsLabel(self)

    def _setup_layout(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.decrement_button, 1)
        layout.addWidget(self.turns_label, 2)
        layout.addWidget(self.increment_button, 1)

    def _attach_listeners(self):
        self.increment_button.clicked.connect(lambda: self.adjustment_manager.adjust(1))
        self.decrement_button.clicked.connect(
            lambda: self.adjustment_manager.adjust(-1)
        )
        self.decrement_button.customContextMenuRequested.connect(
            lambda: self.adjustment_manager.adjust(-0.5)
        )
        self.increment_button.customContextMenuRequested.connect(
            lambda: self.adjustment_manager.adjust(0.5)
        )
        self.turns_label.clicked.connect(self.on_turns_label_clicked)

    def update_turns_display(self, motion: "Motion", new_turns: str) -> None:
        self.turns_box.matching_motion = motion
        display_value = "fl" if new_turns == "fl" else str(new_turns)
        self.turns_label.setText(display_value)

        if self.turns_box.matching_motion.state.motion_type in [PRO, ANTI, FLOAT]:
            self.decrement_button.setEnabled(new_turns not in ["fl"])
        else:
            self.decrement_button.setEnabled(new_turns != 0)

        if display_value == "3":
            self.increment_button.setEnabled(False)
        else:
            self.increment_button.setEnabled(True)

        self.turns_widget.motion_type_label.update_display(motion.state.motion_type)

    def on_turns_label_clicked(self) -> None:
        self.turns_widget.direct_set_dialog.show_direct_set_dialog()

    def resizeEvent(self, event):
        self.turns_label.resizeEvent(event)
        self.increment_button.resizeEvent(event)
        self.decrement_button.resizeEvent(event)
        return super().resizeEvent(event)


# From __init__.py


# From __init__.py


# From __init__.py


# From __init__.py


# From __init__.py


# From arrow_movement_manager.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)


if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


from PyQt6.QtCore import Qt


class ArrowMovementManager:
    def __init__(self, ge_view: "GE_PictographView") -> None:
        self.ge_view = ge_view
        self.graph_editor = ge_view.graph_editor

    def handle_arrow_movement(self, key, shift_held, ctrl_held) -> None:
        self.ge_pictograph = self.ge_view.pictograph
        self.data_updater = (
            self.ge_pictograph.managers.arrow_placement_manager.data_updater
        )

        adjustment_increment = 5
        if shift_held:
            adjustment_increment = 20
        if shift_held and ctrl_held:
            adjustment_increment = 200

        adjustment = self.get_adjustment(key, adjustment_increment)
        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(self.ge_pictograph)
        self.data_updater.update_arrow_adjustments_in_json(adjustment, turns_tuple)
        self.data_updater.mirrored_entry_manager.update_mirrored_entry_in_json()
        for (
            pictograph
        ) in (
            self.ge_pictograph.main_widget.pictograph_collector.collect_all_pictographs()
        ):
            if pictograph.state.letter == self.ge_pictograph.state.letter:
                pictograph.managers.updater.placement_updater.update()

        QApplication.processEvents()

    def get_adjustment(self, key, increment) -> tuple[int, int]:
        direction_map = {
            Qt.Key.Key_W: (0, -1),
            Qt.Key.Key_A: (-1, 0),
            Qt.Key.Key_S: (0, 1),
            Qt.Key.Key_D: (1, 0),
        }
        dx, dy = direction_map.get(key, (0, 0))
        return dx * increment, dy * increment


# From hotkey_graph_adjuster.py
from typing import TYPE_CHECKING

from .arrow_movement_manager import ArrowMovementManager
from .prop_placement_override_manager import PropPlacementOverrideManager
from .data_updater.special_placement_entry_remover import SpecialPlacementEntryRemover
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)


from .rot_angle_override.rot_angle_override_manager import RotAngleOverrideManager

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


class HotkeyGraphAdjuster:
    def __init__(self, view: "GE_PictographView") -> None:
        self.ge_view = view

        self.movement_manager = ArrowMovementManager(view)
        self.turns_tuple_generator = TurnsTupleGenerator()

        self.rot_angle_override_manager = RotAngleOverrideManager(self)
        self.prop_placement_override_manager = PropPlacementOverrideManager(self)
        self.entry_remover = SpecialPlacementEntryRemover(self)


# From prop_placement_override_manager.py
from typing import TYPE_CHECKING

from enums.letter.letter import Letter

from settings_manager.global_settings.app_context import AppContext
from objects.prop.prop import Prop
from placement_managers.prop_placement_manager.handlers.beta_offset_calculator import (
    BetaOffsetCalculator,
)


if TYPE_CHECKING:
    from .hotkey_graph_adjuster import HotkeyGraphAdjuster


class PropPlacementOverrideManager:
    def __init__(self, hotkey_adjuster: "HotkeyGraphAdjuster") -> None:
        self.view = hotkey_adjuster.ge_view
        self.data_updater = (
            hotkey_adjuster.ge_view.scene().managers.arrow_placement_manager.data_updater
        )
        self.turns_tuple_generator = hotkey_adjuster.turns_tuple_generator
        self.beta_offset_calculator = BetaOffsetCalculator(self)

    def handle_prop_placement_override(self) -> None:
        self.ge_pictograph = self.view.scene()
        self.special_placements = (
            AppContext.special_placement_loader().load_or_return_special_placements()
        )
        if self._is_mixed_ori():
            return
        beta_ori = self._get_beta_ori()
        self.letter = self.ge_pictograph.state.letter

        if self.view.scene().managers.check.ends_with_beta():
            adjustment_key_str, ori_key, override_key = self._get_keys(beta_ori)
            letter_data = self._get_letter_data(ori_key, self.letter)
            turn_data = self._get_turn_data(letter_data, adjustment_key_str)

            if override_key in turn_data:
                del turn_data[override_key]
            else:
                turn_data[override_key] = True

            letter_data[adjustment_key_str] = turn_data
            self.special_placements[self.view.scene().state.grid_mode][ori_key][
                self.letter
            ] = letter_data
            self._update_json_entry(self.letter, letter_data)
            self.view.scene().managers.updater.update_pictograph()
            for (
                pictograph
            ) in (
                self.ge_pictograph.main_widget.pictograph_collector.collect_all_pictographs()
            ):
                if pictograph.state.letter == self.ge_pictograph.state.letter:
                    pictograph.managers.updater.update_pictograph()

        AppContext.special_placement_loader().reload()

    def _get_keys(self, beta_ori):
        adjustment_key_str = self._generate_adjustment_key_str(self.letter)
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.view.scene().elements.blue_motion
        )
        override_key = self._generate_override_key(beta_ori)
        return adjustment_key_str, ori_key, override_key

    def _is_mixed_ori(self) -> bool:
        return not (
            self.view.scene().managers.check.ends_with_nonradial_ori()
            or self.view.scene().managers.check.ends_with_radial_ori()
        )

    def _get_beta_ori(self):
        if self.view.scene().managers.check.ends_with_nonradial_ori():
            beta_ori = "nonradial"
        elif self.view.scene().managers.check.ends_with_radial_ori():
            beta_ori = "radial"
        return beta_ori

    def _generate_adjustment_key_str(self, letter) -> str:
        return self.turns_tuple_generator.generate_turns_tuple(self.view.scene())

    def _generate_override_key(self, beta_state) -> str:
        return (
            f"swap_beta_{self.view.scene().elements.blue_prop.loc}_{beta_state}_"
            f"blue_{self.view.scene().elements.blue_motion.state.motion_type}_{self.view.scene().elements.blue_arrow.state.loc}_"
            f"red_{self.view.scene().elements.red_motion.state.motion_type}_{self.view.scene().elements.red_arrow.state.loc}"
        )

    def _get_letter_data(self, ori_key, letter: Letter) -> dict:
        return (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()[self.view.scene().state.grid_mode][
                ori_key
            ]
            .get(letter.value, {})
        )

    def _get_turn_data(self, letter_data, adjustment_key_str) -> dict:
        return letter_data.get(adjustment_key_str, {})

    def _update_json_entry(self, letter, letter_data) -> None:
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.view.scene().elements.blue_motion
        )
        self.data_updater.update_specific_entry_in_json(letter, letter_data, ori_key)

    def move_prop(self, prop: Prop, direction: str) -> None:
        offset_calculator = self.beta_offset_calculator
        offset = offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)

    def _swap_props(
        self, prop_a: Prop, prop_b: Prop, direction_a: str, direction_b: str
    ) -> None:
        """Yes, this DOES have to be called twice for each prop to swap them. It's complicated."""
        self.move_prop(prop_a, direction_a)
        self.move_prop(prop_a, direction_a)
        self.move_prop(prop_b, direction_b)
        self.move_prop(prop_b, direction_b)


# From rotation_angle_override_key_generator.py
from typing import TYPE_CHECKING
from data.constants import CLOCK, COUNTER, IN, OUT

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowRotAngleOverrideKeyGenerator:
    def get_start_ori_layer(self, arrow: "Arrow") -> str:
        if arrow.motion.state.start_ori in [IN, OUT]:
            return "layer1"
        elif arrow.motion.state.start_ori in [CLOCK, COUNTER]:
            return "layer2"

    def get_end_ori_layer(self, arrow: "Arrow") -> str:
        if arrow.motion.state.end_ori in [IN, OUT]:
            return "layer1"
        elif arrow.motion.state.end_ori in [CLOCK, COUNTER]:
            return "layer2"

    def generate_rotation_angle_override_key(self, arrow: "Arrow") -> str:
        motion_type = arrow.motion.state.motion_type
        if arrow.pictograph.state.letter.value in ["α", "β", "Γ", "Φ-", "Ψ-", "Λ-"]:
            return f"{arrow.motion.state.color}_rot_angle_override"
        elif arrow.pictograph.managers.check.starts_from_mixed_orientation():
            start_ori_layer = self.get_start_ori_layer(arrow)
            return f"{motion_type}_from_{start_ori_layer}_rot_angle_override"
        elif (
            arrow.pictograph.managers.check.starts_from_standard_orientation()
            and arrow.pictograph.managers.check.ends_in_mixed_orientation()
        ):
            end_ori_layer = self.get_end_ori_layer(arrow)
            return f"{motion_type}_to_{end_ori_layer}_rot_angle_override"
        else:
            return f"{motion_type}_rot_angle_override"


# From __init__.py


# From ori_key_generator.py
import logging
from typing import TYPE_CHECKING



from placement_managers.arrow_placement_manager.arrow_placement_context import ArrowPlacementContext


from data.constants import (
    BLUE,
    CLOCK,
    COUNTER,
    IN,
    OUT,
    RED,
)
from objects.motion.motion import Motion

if TYPE_CHECKING:

    from base_widgets.pictograph.managers.getter.pictograph_getter import PictographGetter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class OriKeyGenerator:
    def __init__(self, getter: "PictographGetter"):
        self.getter = getter

    def generate_ori_key_from_context(self, context: ArrowPlacementContext) -> str:
        """
        Generates an orientation key based on arrow placement context.

        :param context: ArrowPlacementContext object containing motion details.
        :return: Orientation key string.
        """
        # Instead of `motion`, use `context` directly.
        start_ori = context.start_ori
        color = context.arrow_color

        # Determine the other motion (assuming getter logic still applies)
        other_motion = self.getter.other_motion(
            self.getter.motion_by_color(context.arrow_color)
        )
        other_start_ori = other_motion.state.start_ori if other_motion else None

        if start_ori in [IN, OUT] and other_start_ori in [IN, OUT]:
            return "from_layer1"
        elif start_ori in [CLOCK, COUNTER] and other_start_ori in [CLOCK, COUNTER]:
            return "from_layer2"
        elif (
            color == RED
            and start_ori in [IN, OUT]
            and other_start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue2_red1"
        elif (
            color == RED
            and start_ori in [CLOCK, COUNTER]
            and other_start_ori in [IN, OUT]
        ):
            return "from_layer3_blue1_red2"
        elif (
            color == BLUE
            and start_ori in [IN, OUT]
            and other_start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue1_red2"
        elif (
            color == BLUE
            and start_ori in [CLOCK, COUNTER]
            and other_start_ori in [IN, OUT]
        ):
            return "from_layer3_blue2_red1"

    def generate_ori_key_from_motion(self, motion: Motion) -> str:
        other_motion: Motion = self.getter.other_motion(motion)
        if motion.state.start_ori in [IN, OUT] and other_motion.state.start_ori in [
            IN,
            OUT,
        ]:
            return "from_layer1"
        elif motion.state.start_ori in [
            CLOCK,
            COUNTER,
        ] and other_motion.state.start_ori in [
            CLOCK,
            COUNTER,
        ]:
            return "from_layer2"
        elif (
            motion.state.color == RED
            and motion.state.start_ori in [IN, OUT]
            and other_motion.state.start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue2_red1"
        elif (
            motion.state.color == RED
            and motion.state.start_ori in [CLOCK, COUNTER]
            and other_motion.state.start_ori in [IN, OUT]
        ):
            return "from_layer3_blue1_red2"
        elif (
            motion.state.color == BLUE
            and motion.state.start_ori in [IN, OUT]
            and other_motion.state.start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue1_red2"
        elif (
            motion.state.color == BLUE
            and motion.state.start_ori in [CLOCK, COUNTER]
            and other_motion.state.start_ori in [IN, OUT]
        ):
            return "from_layer3_blue2_red1"

    def get_other_layer3_ori_key(self, ori_key: str) -> str:
        if ori_key == "from_layer3_blue1_red2":
            return "from_layer3_blue2_red1"
        elif ori_key == "from_layer3_blue2_red1":
            return "from_layer3_blue1_red2"


# From placement_data_cleaner.py
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


# From special_placement_data_updater.py
import os
import logging
from typing import TYPE_CHECKING

from enums.letter.letter import Letter
from utils.path_helpers import get_data_path

from .mirrored_entry_manager.mirrored_entry_manager import MirroredEntryManager
from .ori_key_generator import OriKeyGenerator
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from settings_manager.global_settings.app_context import AppContext
from placement_managers.attr_key_generator import (
    AttrKeyGenerator,
)


from objects.arrow.arrow import Arrow
from PyQt6.QtCore import QPoint

if TYPE_CHECKING:

    from base_widgets.pictograph.managers.pictograph_checker import PictographChecker
    from base_widgets.pictograph.managers.getter.pictograph_getter import (
        PictographGetter,
    )
    from base_widgets.pictograph.state.pictograph_state import PictographState

    from placement_managers.arrow_placement_manager.arrow_placement_manager import (
        ArrowPlacementManager,
    )


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SpecialPlacementDataUpdater:
    def __init__(
        self,
        placement_manager: "ArrowPlacementManager",
        state: "PictographState",
        get_default_adjustment_callback: callable,
        getter: "PictographGetter",
        checker: "PictographChecker",
    ) -> None:
        self.placement_manager = placement_manager
        self.state = state
        self.attr_key_generator = AttrKeyGenerator()
        self.get_default_adjustment_callback = get_default_adjustment_callback
        self.getter = getter
        self.checker = checker
        self.grid_mode = self.getter.grid_mode()
        self.ori_key_generator = OriKeyGenerator(getter)
        self.turns_tuple_generator = TurnsTupleGenerator()
        self.mirrored_entry_manager = MirroredEntryManager(self)

    def _get_letter_data(self, letter: Letter, ori_key: str) -> dict:
        letter_data = (
            AppContext.special_placement_loader()
            .load_special_placements_fresh()
            .get(self.state.grid_mode, {})
            .get(ori_key, {})
            .get(letter.value, {})
        )

        return letter_data

    def _update_or_create_turn_data(
        self,
        letter_data: dict,
        turns_tuple: str,
        arrow: Arrow,
        adjustment: QPoint,  # Ensure this is a QPoint
    ) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        key = self.attr_key_generator.get_key_from_arrow(arrow)

        if key in turn_data and turn_data[key] != {}:
            turn_data[key][0] += adjustment.x()  # ✅ Extract x value
            turn_data[key][1] += adjustment.y()  # ✅ Extract y value
            turn_data[key] = [int(turn_data[key][0]), int(turn_data[key][1])]
        else:
            default_adjustment = self.get_default_adjustment_callback(arrow)
            turn_data[key] = [
                int(default_adjustment.x() + adjustment.x()),  # ✅ Extract x value
                int(default_adjustment.y() + adjustment.y()),  # ✅ Extract y value
            ]

        letter_data[turns_tuple] = turn_data

    def _update_placement_json_data(
        self, letter: Letter, letter_data: dict, ori_key: str, grid_mode: str
    ) -> None:
        # Time to get surgical with our JSON updates! 🔪
        file_path = get_data_path(
            os.path.join(
                "arrow_placement",
                grid_mode,
                "special",
                ori_key,
                f"{letter.value}_placements.json",
            )
        )

        placement_data = (
            AppContext.special_placement_loader().load_json_data(file_path) or {}
        )

        placement_data[letter.value] = letter_data
        AppContext.special_placement_saver().save_json_data(placement_data, file_path)

    def update_arrow_adjustments_in_json(
        self, adjustment: tuple[int, int] | QPoint, turns_tuple: str
    ) -> None:
        selected_arrow = AppContext.get_selected_arrow()
        if not selected_arrow:
            return

        if isinstance(adjustment, tuple):
            adjustment = QPoint(*adjustment)

        letter = selected_arrow.pictograph.state.letter
        ori_key = self.ori_key_generator.generate_ori_key_from_motion(
            selected_arrow.motion
        )
        letter_data = self._get_letter_data(letter, ori_key)
        self._update_or_create_turn_data(
            letter_data, turns_tuple, selected_arrow, adjustment
        )
        self._update_placement_json_data(
            letter, letter_data, ori_key, self.state.grid_mode
        )

    def update_specific_entry_in_json(
        self, letter: Letter, letter_data: dict, ori_key
    ) -> None:
        try:
            self._update_placement_json_data(
                letter, letter_data, ori_key, self.state.grid_mode
            )
        except Exception as e:
            logging.error(f"Error in update_specific_entry_in_json: {e}")

    def get_other_layer3_ori_key(self, ori_key: str) -> str:
        if ori_key == "from_layer3_blue1_red2":
            return "from_layer3_blue2_red1"
        elif ori_key == "from_layer3_blue2_red1":
            return "from_layer3_blue1_red2"


# From special_placement_entry_remover.py
import os
from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from data.constants import BLUE, RED
from main_window.main_widget.json_manager.special_placement_saver import (
    SpecialPlacementSaver,
)

from settings_manager.global_settings.app_context import AppContext
from objects.arrow.arrow import Arrow
from placement_managers.attr_key_generator import (
    AttrKeyGenerator,
)
if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.hotkey_graph_adjuster import (
        HotkeyGraphAdjuster,
    )
    from .special_placement_data_updater import SpecialPlacementDataUpdater




class SpecialPlacementEntryRemover:
    """Handles removal of special placement entries."""

    def __init__(
        self,
        hotkey_graph_adjuster: "HotkeyGraphAdjuster",
    ) -> None:
        self.turns_tuple_generator = hotkey_graph_adjuster.turns_tuple_generator
        self.special_placement_saver = SpecialPlacementSaver()
        self.special_placement_loader = AppContext.special_placement_loader()
        self.ge_view = hotkey_graph_adjuster.ge_view
        self.data_updater: "SpecialPlacementDataUpdater" = (
            self.ge_view.pictograph.managers.arrow_placement_manager.data_updater
        )

    def remove_special_placement_entry(self, letter: Letter, arrow: Arrow) -> None:
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            arrow.motion
        )
        file_path = self._generate_file_path(
            ori_key, letter, arrow.pictograph.state.grid_mode
        )

        if os.path.exists(file_path):
            data = self.load_data(file_path)
            self._process_removal(letter, arrow, ori_key, file_path, data)
            AppContext.special_placement_loader().reload()
        arrow.pictograph.managers.updater.placement_updater.update()
        for (
            pictograph
        ) in self.ge_view.main_widget.pictograph_collector.collect_all_pictographs():
            if pictograph.state.letter == letter:
                pictograph.managers.updater.update_pictograph()
                pictograph.managers.arrow_placement_manager.update_arrow_placements()

    def _process_removal(
        self, letter: Letter, arrow: Arrow, ori_key: str, file_path: str, data: dict
    ):
        self.turns_tuple = self.turns_tuple_generator.generate_turns_tuple(
            self.data_updater.placement_manager.pictograph
        )
        if letter.value in data:
            letter_data = data[letter.value]

            key = AttrKeyGenerator().get_key_from_arrow(arrow)
            self._remove_turn_data_entry(letter_data, self.turns_tuple, key)

            if arrow.pictograph.managers.check.starts_from_mixed_orientation():
                self._handle_mixed_start_ori_mirrored_entry_removal(
                    letter, arrow, ori_key, letter_data, key
                )
            elif arrow.pictograph.managers.check.starts_from_standard_orientation():
                self._handle_standard_start_ori_mirrored_entry_removal(
                    letter, arrow, letter_data, key
                )

            data[letter.value] = letter_data
            AppContext.special_placement_saver().save_json_data(data, file_path)

    def _handle_standard_start_ori_mirrored_entry_removal(
        self, letter, arrow: Arrow, letter_data: dict, key
    ):
        if (
            arrow.motion.state.turns
            == arrow.pictograph.managers.get.other_arrow(arrow).motion.state.turns
            or arrow.motion.state.motion_type
            != arrow.pictograph.managers.get.other_arrow(arrow).motion.state.motion_type
            or letter in ["S", "T"]
        ):
            return

        mirrored_tuple = self.turns_tuple_generator.generate_mirrored_tuple(arrow)

        if key == BLUE:
            new_key = RED
        elif key == RED:
            new_key = BLUE
        else:
            new_key = key

        if letter_data.get(mirrored_tuple, {}).get(new_key, {}):
            del letter_data[mirrored_tuple][new_key]
            if not letter_data[mirrored_tuple]:
                del letter_data[mirrored_tuple]

    def _handle_mixed_start_ori_mirrored_entry_removal(
        self, letter: Letter, arrow: "Arrow", ori_key, letter_data, key
    ):

        other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
        other_file_path = self._generate_file_path(
            other_ori_key, letter, arrow.pictograph.state.grid_mode
        )
        other_data = self.special_placement_loader.load_json_data(other_file_path)
        other_letter_data = other_data.get(letter, {})
        mirrored_tuple = self.turns_tuple_generator.generate_mirrored_tuple(arrow)
        if key == BLUE:
            new_key = RED
        elif key == RED:
            new_key = BLUE
        else:
            new_key = key
        if other_letter_data != letter_data:
            if mirrored_tuple not in other_letter_data:
                other_letter_data[mirrored_tuple] = {}
            if new_key not in other_letter_data[mirrored_tuple]:
                if self.turns_tuple in letter_data:
                    if key not in letter_data[self.turns_tuple]:
                        letter_data[self.turns_tuple][key] = {}
                    other_letter_data[mirrored_tuple][new_key] = letter_data[
                        self.turns_tuple
                    ][key]
            if other_data:
                if other_data[letter.value].get(mirrored_tuple, {}):
                    if other_data[letter.value].get(mirrored_tuple, {}).get(new_key):
                        del other_data[letter.value][mirrored_tuple][new_key]

            elif key not in letter_data[self.turns_tuple]:
                if other_data:
                    del other_data[letter][mirrored_tuple][new_key]
            self.special_placement_saver.save_json_data(other_data, other_file_path)
        new_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(arrow)
        self._remove_turn_data_entry(other_letter_data, new_turns_tuple, new_key)

    def load_data(self, file_path):  # -> Any:
        return self.special_placement_loader.load_json_data(file_path)

    def _generate_file_path(self, ori_key: str, letter: Letter, grid_mode: str) -> str:
        file_path = os.path.join(
            "src",
            "data",
            "arrow_placement",
            grid_mode,
            "special",
            ori_key,
            f"{letter.value}_placements.json",
        )

        return file_path

    def _get_other_color(self, color: str) -> str:
        return RED if color == BLUE else BLUE

    def _remove_turn_data_entry(self, letter_data: dict, turns_tuple: str, key) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        if key in turn_data:
            del turn_data[key]
            if not turn_data:
                del letter_data[turns_tuple]


# From __init__.py


# From mirrored_entry_adapter.py
import logging
from typing import TYPE_CHECKING, Optional

from data.constants import DASH, STATIC
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import ArrowRotAngleOverrideKeyGenerator
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import TurnsTupleGenerator
from objects.arrow.arrow import Arrow
from settings_manager.global_settings.app_context import AppContext

from .mirrored_entry_factory import MirroredEntryFactory
from .mirrored_entry_utils import MirroredEntryUtils

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.data_updater.special_placement_data_updater import (
        SpecialPlacementDataUpdater,
    )


class MirroredEntryAdapter:
    """Adapter for integrating the new mirrored entry system with existing code."""

    def __init__(self, data_updater):
        """Initialize the adapter with the given data updater."""
        self.data_updater = data_updater
        self.utils = MirroredEntryUtils()
        self.factory = MirroredEntryFactory

    def update_mirrored_entry_in_json(self) -> None:
        """Update the mirrored entry in JSON."""
        selected_arrow = AppContext.get_selected_arrow()
        if not selected_arrow:
            logger.warning("No arrow selected, cannot update mirrored entry")
            return

        try:
            if MirroredEntryUtils.is_new_entry_needed(selected_arrow):
                self._create_new_entry(selected_arrow)
            else:
                self._update_existing_entry(selected_arrow)

            AppContext.special_placement_loader().reload()
        except Exception as e:
            logger.error(
                f"Failed to update mirrored entry in JSON: {str(e)}", exc_info=True
            )

    def _create_new_entry(self, arrow: Arrow) -> None:
        """Create a new mirrored entry for the given arrow."""
        service = self.factory.create_service(self.data_updater)
        service.update_mirrored_entry(arrow)

    def _update_existing_entry(self, arrow: Arrow) -> None:
        """Update an existing mirrored entry for the given arrow."""
        service = self.factory.create_service(self.data_updater)
        service.update_mirrored_entry(arrow)

    def rot_angle_manager(self):
        """Get a rotation angle processor for compatibility with old code."""
        data_updater = self.data_updater

        class RotationAngleManagerAdapter:
            def __init__(self):
                self.data_updater: "SpecialPlacementDataUpdater" = data_updater
                self.turns_tuple_generator = TurnsTupleGenerator()

            def update_rotation_angle_in_mirrored_entry(
                self, arrow: Arrow, updated_turn_data: dict
            ) -> None:
                if not self._should_handle_rotation_angle(arrow):
                    return

                rot_angle_override = self._check_for_rotation_angle_override(
                    updated_turn_data
                )
                if rot_angle_override is None:
                    return

                ori_key = (
                    self.data_updater.ori_key_generator.generate_ori_key_from_motion(
                        arrow.motion
                    )
                )
                letter = arrow.pictograph.state.letter
                grid_mode = arrow.pictograph.state.grid_mode

                # Use MirroredEntryUtils directly to match original behavior
                other_ori_key, other_letter_data = (
                    MirroredEntryUtils.get_keys_for_mixed_start_ori(
                        grid_mode, letter, ori_key
                    )
                )

                mirrored_turns_tuple = (
                    self.turns_tuple_generator.generate_mirrored_tuple(arrow)
                )

                # Handle the override exactly as in the original
                self._handle_mirrored_rotation_angle_override(
                    other_letter_data,
                    rot_angle_override,
                    mirrored_turns_tuple,
                )

                # Save the data using the data updater
                self.data_updater.update_specific_entry_in_json(
                    letter, other_letter_data, other_ori_key
                )

            def remove_rotation_angle_in_mirrored_entry(
                self, arrow: Arrow, hybrid_key: str
            ):
                letter = arrow.pictograph.state.letter
                ori_key = (
                    self.data_updater.ori_key_generator.generate_ori_key_from_motion(
                        arrow.motion
                    )
                )
                grid_mode = arrow.pictograph.state.grid_mode

                # Use MirroredEntryUtils directly to match original behavior
                other_ori_key, other_letter_data = (
                    MirroredEntryUtils.get_keys_for_mixed_start_ori(
                        grid_mode, letter, ori_key
                    )
                )

                mirrored_turns_tuple = (
                    self.turns_tuple_generator.generate_mirrored_tuple(arrow)
                )

                # Exactly match original deletion logic
                if (
                    mirrored_turns_tuple in other_letter_data
                    and hybrid_key in other_letter_data[mirrored_turns_tuple]
                ):
                    del other_letter_data[mirrored_turns_tuple][hybrid_key]

                # Save the updated data
                self.data_updater.update_specific_entry_in_json(
                    letter, other_letter_data, other_ori_key
                )

            def _handle_mirrored_rotation_angle_override(
                self, other_letter_data, rotation_angle_override, mirrored_turns_tuple
            ):
                key = ArrowRotAngleOverrideKeyGenerator().generate_rotation_angle_override_key(
                    AppContext.get_selected_arrow()
                )
                if mirrored_turns_tuple not in other_letter_data:
                    other_letter_data[mirrored_turns_tuple] = {}
                other_letter_data[mirrored_turns_tuple][key] = rotation_angle_override

            def _should_handle_rotation_angle(self, arrow: Arrow) -> bool:
                return arrow.motion.state.motion_type in [STATIC, DASH]

            def _check_for_rotation_angle_override(
                self, turn_data: dict
            ) -> Optional[int]:
                for key in turn_data.keys():
                    if "rot_angle_override" in key:
                        return turn_data[key]
                return None

        return RotationAngleManagerAdapter()


# From mirrored_entry_creator.py
from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from settings_manager.global_settings.app_context import AppContext
from objects.arrow.arrow import Arrow
from placement_managers.attr_key_generator import (
    AttrKeyGenerator,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.data_updater.special_placement_data_updater import (
        SpecialPlacementDataUpdater,
    )

    from .mirrored_entry_manager import MirroredEntryManager

    from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
        TurnsTupleGenerator,
    )


class MirroredEntryCreator:
    def __init__(self, mirrored_entry_manager: "MirroredEntryManager"):
        self.special_placement_data_updater: "SpecialPlacementDataUpdater" = (
            mirrored_entry_manager.data_updater
        )
        self.turns_tuple_generator: TurnsTupleGenerator = (
            mirrored_entry_manager.turns_tuple_generator
        )

    def create_entry(self, letter: Letter, arrow: Arrow):
        ori_key = self.special_placement_data_updater.ori_key_generator.generate_ori_key_from_motion(
            arrow.motion
        )
        letter_data, _ = self._fetch_letter_data_and_original_turn_data(
            ori_key, letter, arrow
        )
        turns_tuple = self.turns_tuple_generator.generate_turns_tuple(arrow.pictograph)
        if arrow.pictograph.managers.check.starts_from_mixed_orientation():
            other_ori_key, other_letter_data = self._get_keys_for_mixed_start_ori(
                letter, ori_key
            )

            mirrored_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(
                arrow
            )

            attr_key = AttrKeyGenerator().get_key_from_arrow(arrow)

            if mirrored_turns_tuple not in other_letter_data:
                other_letter_data[mirrored_turns_tuple] = {}
            if attr_key not in letter_data:
                letter_data[attr_key] = {}

            other_letter_data[mirrored_turns_tuple][attr_key] = letter_data[
                turns_tuple
            ][attr_key]

            self._initialize_dicts(mirrored_turns_tuple, other_letter_data, attr_key)
            self.special_placement_data_updater.update_specific_entry_in_json(
                letter, other_letter_data, other_ori_key
            )

    def _initialize_dicts(self, mirrored_turns_tuple, other_letter_data, attr):
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        if attr not in other_letter_data[mirrored_turns_tuple]:
            other_letter_data[mirrored_turns_tuple][attr] = {}

    def _fetch_letter_data_and_original_turn_data(
        self, ori_key, letter: Letter, arrow: Arrow
    ) -> tuple[dict, dict]:
        letter_data: dict = (
            AppContext.special_placement_loader()
            .load_special_placements_fresh()
            .get(self.special_placement_data_updater.getter.grid_mode(), {})
            .get(ori_key, {})
            .get(letter.value, {})
        )
        original_turns_tuple = self.turns_tuple_generator.generate_turns_tuple(
            arrow.pictograph
        )
        return letter_data, letter_data.get(original_turns_tuple, {})

    def _get_keys_for_mixed_start_ori(
        self, letter: Letter, ori_key
    ) -> tuple[str, dict]:
        AppContext.special_placement_loader().reload()
        other_ori_key = self.special_placement_data_updater.get_other_layer3_ori_key(
            ori_key
        )
        other_letter_data = (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()
            .get(self.special_placement_data_updater.getter.grid_mode(), {})
            .get(other_ori_key, {})
            .get(letter.value, {})
        )
        return other_ori_key, other_letter_data


# From mirrored_entry_data_prep.py
from enums.letter.letter import Letter

from typing import TYPE_CHECKING

from settings_manager.global_settings.app_context import AppContext
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from .mirrored_entry_manager import MirroredEntryManager


class MirroredEntryDataPrep:
    def __init__(self, manager: "MirroredEntryManager"):
        self.manager = manager

    def is_new_entry_needed(self, arrow: Arrow) -> bool:
        """Determines if a new mirrored entry is needed for the given arrow."""
        AppContext.special_placement_loader().reload()
        ori_key = self._get_ori_key(arrow.motion)
        return (
            arrow.pictograph.state.letter
            not in AppContext.special_placement_loader()
            .load_or_return_special_placements()
            .get(ori_key, {})
        )

    def _get_ori_key(self, motion):
        """Fetches the orientation key based on the motion's properties."""
        return self.manager.data_updater.ori_key_generator.generate_ori_key_from_motion(
            motion
        )

    def get_keys_for_mixed_start_ori(
        self, grid_mode, letter, ori_key
    ) -> tuple[str, dict]:
        """Fetches keys and data for mixed start orientation cases."""
        if self.manager.data_updater.checker.starts_from_mixed_orientation():
            other_ori_key = (
                self.manager.data_updater.ori_key_generator.get_other_layer3_ori_key(
                    ori_key
                )
            )
            other_letter_data = self._get_letter_data(grid_mode, other_ori_key, letter)
            return other_ori_key, other_letter_data
        return ori_key, self._get_letter_data(grid_mode, ori_key, letter)

    def _get_letter_data(self, grid_mode: str, ori_key: str, letter: Letter) -> dict:
        """Fetches letter data for a given orientation key and letter."""
        return (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()
            .get(grid_mode, {})
            .get(ori_key, {})
            .get(letter.value, {})
        )

    def _fetch_letter_data_and_original_turn_data(
        self, ori_key: str, letter: Letter, arrow: Arrow
    ) -> tuple[dict, dict]:
        """Fetches letter data and the original turns tuple for the given arrow."""
        letter_data = self._get_letter_data(
            arrow.pictograph.state.grid_mode, ori_key, letter
        )
        original_turns_tuple = self.manager.turns_tuple_generator.generate_turns_tuple(
            arrow.pictograph
        )
        original_turn_data = letter_data.get(original_turns_tuple, {})
        return letter_data, original_turn_data


# From mirrored_entry_factory.py
"""
Factory for creating and configuring mirrored entry components.
"""
import logging

from objects.arrow.arrow import Arrow
from settings_manager.global_settings.app_context import AppContext

from .mirrored_entry_service import MirroredEntryService

logger = logging.getLogger(__name__)

class MirroredEntryFactory:
    """
    Factory for creating and configuring mirrored entry components.
    Provides a simple way to get a fully configured mirrored entry service.
    """
    
    @staticmethod
    def create_service(data_updater) -> MirroredEntryService:
        """
        Create a fully configured mirrored entry service.
        
        Args:
            data_updater: The data updater to use
            
        Returns:
            A configured mirrored entry service
        """
        try:
            # Create and return the service
            return MirroredEntryService(data_updater)
        except Exception as e:
            logger.error(f"Failed to create mirrored entry service: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def update_mirrored_entry(arrow: Arrow) -> bool:
        """
        Update the mirrored entry for the given arrow.
        This is a convenience method that creates a service and updates the entry.
        
        Args:
            arrow: The arrow to update the mirrored entry for
            
        Returns:
            True if the update was successful, False otherwise
        """
        try:
            data_updater = arrow.pictograph.managers.arrow_placement_manager.data_updater
            service = MirroredEntryFactory.create_service(data_updater)
            service.update_mirrored_entry(arrow)
            AppContext.special_placement_loader().reload()
            return True
        except Exception as e:
            logger.error(f"Failed to update mirrored entry: {str(e)}", exc_info=True)
            return False

# From mirrored_entry_manager.py
import logging
from .mirrored_entry_adapter import MirroredEntryAdapter

logger = logging.getLogger(__name__)

class MirroredEntryManager:
    
    def __init__(self, data_updater) -> None:
        self.data_updater = data_updater
        self.adapter = MirroredEntryAdapter(data_updater)
        self.turns_tuple_generator = self.adapter.factory.create_service(data_updater).turns_manager
        self.rot_angle_manager = self.adapter.rot_angle_manager()
        self.data_prep = type('DataPrep', (), {
            'is_new_entry_needed': lambda arrow: False,
            'get_keys_for_mixed_start_ori': lambda grid_mode, letter, ori_key: (ori_key, {})
        })()
    
    def update_mirrored_entry_in_json(self) -> None:
        self.adapter.update_mirrored_entry_in_json()


# From mirrored_entry_rot_angle_manager.py
from typing import Optional
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import (
    ArrowRotAngleOverrideKeyGenerator,
)
from settings_manager.global_settings.app_context import AppContext
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mirrored_entry_manager import MirroredEntryManager
from data.constants import DASH, STATIC


class MirroredEntryRotAngleManager:
    def __init__(self, manager: "MirroredEntryManager"):
        self.manager = manager

    def update_rotation_angle_in_mirrored_entry(
        self, arrow: Arrow, updated_turn_data: dict
    ) -> None:
        if not self._should_handle_rotation_angle(arrow):
            return

        rot_angle_override = self._check_for_rotation_angle_override(updated_turn_data)
        if rot_angle_override is None:
            return

        ori_key = (
            self.manager.data_updater.ori_key_generator.generate_ori_key_from_motion(
                arrow.motion
            )
        )
        letter = arrow.pictograph.state.letter
        grid_mode = arrow.pictograph.state.grid_mode
        other_ori_key, other_letter_data = (
            self.manager.data_prep.get_keys_for_mixed_start_ori(grid_mode, letter, ori_key)
        )

        mirrored_turns_tuple = (
            self.manager.turns_tuple_generator.generate_mirrored_tuple(arrow)
        )

        self._handle_mirrored_rotation_angle_override(
            other_letter_data,
            rot_angle_override,
            mirrored_turns_tuple,
        )

        self.manager.data_updater.update_specific_entry_in_json(
            letter, other_letter_data, other_ori_key
        )

    def remove_rotation_angle_in_mirrored_entry(self, arrow: Arrow, hybrid_key: str):
        letter = arrow.pictograph.state.letter
        ori_key = (
            self.manager.data_updater.ori_key_generator.generate_ori_key_from_motion(
                arrow.motion
            )
        )
        grid_mode = arrow.pictograph.state.grid_mode
        other_ori_key, other_letter_data = (
            self.manager.data_prep.get_keys_for_mixed_start_ori(grid_mode, letter, ori_key)
        )
        
        mirrored_turns_tuple = (
            self.manager.turns_tuple_generator.generate_mirrored_tuple(arrow)
        )

        if hybrid_key in other_letter_data.get(mirrored_turns_tuple, {}):
            del other_letter_data[mirrored_turns_tuple][hybrid_key]

        self.manager.data_updater.update_specific_entry_in_json(
            letter, other_letter_data, other_ori_key
        )

    def _handle_mirrored_rotation_angle_override(
        self, other_letter_data, rotation_angle_override, mirrored_turns_tuple
    ):
        key = ArrowRotAngleOverrideKeyGenerator().generate_rotation_angle_override_key(
            AppContext.get_selected_arrow()
        )
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        other_letter_data[mirrored_turns_tuple][key] = rotation_angle_override

    def _should_handle_rotation_angle(self, arrow: Arrow) -> bool:
        return arrow.motion.state.motion_type in [STATIC, DASH]

    def _check_for_rotation_angle_override(self, turn_data: dict) -> Optional[int]:
        for key in turn_data.keys():
            if "rot_angle_override" in key:
                return turn_data[key]
        return None


# From mirrored_entry_service.py
"""
Core functionality for managing mirrored entries in special placements.
"""

import logging
from typing import TYPE_CHECKING, Any
from data.constants import BLUE, IN, OUT, RED

from enums.letter.letter import Letter
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from objects.arrow.arrow import Arrow
from settings_manager.global_settings.app_context import AppContext

from .orientation_handler import OrientationHandler
from .turns_pattern_manager import TurnsPatternManager
from .special_placement_repository import SpecialPlacementRepository
from .rotation_angle_processor import RotationAngleProcessor

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.data_updater.special_placement_data_updater import (
        SpecialPlacementDataUpdater,
    )


class MirroredEntryService:
    """Service for managing mirrored entries in special placements."""

    def __init__(self, data_updater: "SpecialPlacementDataUpdater") -> None:
        """Initialize with required dependencies."""
        self.data_updater = data_updater
        self.turns_manager = TurnsPatternManager()
        self.repository = SpecialPlacementRepository(data_updater.getter.grid_mode())
        self.rotation_processor = RotationAngleProcessor()
        self.orientation_handler = None

    def update_mirrored_entry(self, arrow: Arrow) -> None:
        """Update mirrored entry for the given arrow."""
        logger.debug(f"Updating mirrored entry for arrow: {arrow.state.color}")

        try:
            self.orientation_handler = OrientationHandler(arrow, self.turns_manager)
            letter = arrow.pictograph.state.letter
            ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
                arrow.motion
            )
            letter_data = self._load_letter_data(letter, ori_key)

            if self.orientation_handler.is_mixed_orientation():
                self._process_mixed_orientation_entry(
                    arrow, letter, ori_key, letter_data
                )
            else:
                self._process_standard_orientation_entry(
                    arrow, letter, ori_key, letter_data
                )

            AppContext.special_placement_loader().reload()

        except Exception as e:
            logger.error(f"Failed to update mirrored entry: {str(e)}", exc_info=True)
            raise

    def _load_letter_data(self, letter: Letter, ori_key: str) -> dict[str, Any]:
        """Load letter data for the given orientation key."""
        return self.repository.get_letter_data(letter, ori_key)

    def _process_mixed_orientation_entry(
        self, arrow: "Arrow", letter, ori_key, letter_data: dict[str, Any]
    ):
        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(arrow.pictograph)
        mirrored_tuple = TurnsTupleGenerator().generate_mirrored_tuple(arrow)
        mirror_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
        mirror_letter_data = self.repository.get_letter_data(letter, mirror_ori_key)
        attribute_key = self.orientation_handler.get_mixed_attribute_key()
        if attribute_key in [RED, BLUE]:
            other_attribute_key = self.orientation_handler.get_other_attr_key(
                attribute_key
            )
        else:
            other_attribute_key = attribute_key
        if turns_tuple not in letter_data:
            letter_data[turns_tuple] = {}
        if attribute_key not in letter_data[turns_tuple]:
            letter_data[turns_tuple][attribute_key] = {}

        if mirrored_tuple not in mirror_letter_data:
            mirror_letter_data[mirrored_tuple] = {}

        mirror_letter_data[mirrored_tuple][attribute_key] = letter_data[
            turns_tuple
        ].get(other_attribute_key, {})

        self.rotation_processor.process_rotation_override(
            arrow, letter_data.get(turns_tuple, {}), mirror_letter_data, mirrored_tuple
        )

        self.data_updater.update_specific_entry_in_json(
            letter, mirror_letter_data, mirror_ori_key
        )

    def _process_standard_orientation_entry(
        self,
        arrow: Arrow,
        letter: Letter,
        ori_key: str,
        letter_data: dict[str, dict[str, Any]],
    ) -> None:
        """Process a standard orientation entry."""
        if (
            letter.value in ["S", "T", "β"]
            or letter in self.orientation_handler.get_hybrid_letters()
        ):
            return

        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(arrow.pictograph)
        mirrored_tuple = TurnsTupleGenerator().generate_mirrored_tuple(arrow)
        other_arrow = arrow.pictograph.managers.get.other_arrow(arrow)
        should_mirror = self.orientation_handler.should_create_standard_mirror(
            other_arrow
        )

        if not should_mirror:
            return

        attribute_key = self.orientation_handler.get_standard_attribute_key(other_arrow)
        source_data = letter_data.get(turns_tuple, {}).get(arrow.state.color, {})

        if mirrored_tuple not in letter_data:
            letter_data[mirrored_tuple] = {}

        letter_data[mirrored_tuple][attribute_key] = source_data

        self.data_updater.update_specific_entry_in_json(letter, letter_data, ori_key)


# From mirrored_entry_utils.py
"""
Utility functions for working with mirrored entries.
"""
import logging
from typing import Dict, Any, Tuple

from enums.letter.letter import Letter
from data.constants import BLUE, RED, IN, OUT, CLOCK, COUNTER
from objects.arrow.arrow import Arrow
from settings_manager.global_settings.app_context import AppContext

logger = logging.getLogger(__name__)

class MirroredEntryUtils:
    """
    Utility functions for working with mirrored entries.
    Provides helper methods for common operations.
    """
    
    @staticmethod
    def is_new_entry_needed(arrow: Arrow) -> bool:
        """
        Determine if a new mirrored entry is needed for the given arrow.
        
        Args:
            arrow: The arrow to check
            
        Returns:
            True if a new mirrored entry is needed, False otherwise
        """
        try:
            AppContext.special_placement_loader().reload()
            
            # Get the orientation key
            data_updater = arrow.pictograph.managers.arrow_placement_manager.data_updater
            ori_key = data_updater.ori_key_generator.generate_ori_key_from_motion(arrow.motion)
            
            # Check if the letter exists in the special placements
            letter = arrow.pictograph.state.letter
            return letter not in AppContext.special_placement_loader().load_or_return_special_placements().get(ori_key, {})
        except Exception as e:
            logger.error(f"Failed to check if new entry is needed: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def determine_opposite_color(color: str) -> str:
        """
        Determine the opposite color for the given color.
        
        Args:
            color: The color to get the opposite of
            
        Returns:
            The opposite color
        """
        return RED if color == BLUE else BLUE
    
    @staticmethod
    def get_orientation_layer(orientation: str) -> str:
        """
        Get the layer for the given orientation.
        
        Args:
            orientation: The orientation to get the layer for
            
        Returns:
            The layer ('1' or '2')
        """
        return "1" if orientation in [IN, OUT] else "2"
    
    @staticmethod
    def get_other_layer3_ori_key(ori_key: str) -> str:
        """
        Get the other layer 3 orientation key for the given orientation key.
        
        Args:
            ori_key: The orientation key to get the other key for
            
        Returns:
            The other layer 3 orientation key
        """
        if ori_key == "from_layer3_blue1_red2":
            return "from_layer3_blue2_red1"
        elif ori_key == "from_layer3_blue2_red1":
            return "from_layer3_blue1_red2"
        return ori_key
    
    @staticmethod
    def is_mixed_orientation(arrow: Arrow) -> bool:
        """
        Check if the arrow's pictograph has mixed orientation.
        
        Args:
            arrow: The arrow to check
            
        Returns:
            True if the pictograph has mixed orientation, False otherwise
        """
        other_motion = arrow.pictograph.managers.get.other_motion(arrow.motion)
        blue_in_layer1 = arrow.state.color == BLUE and arrow.motion.state.start_ori in [IN, OUT]
        red_in_layer2 = arrow.state.color == RED and other_motion.state.start_ori in [CLOCK, COUNTER]
        blue_in_layer2 = arrow.state.color == BLUE and arrow.motion.state.start_ori in [CLOCK, COUNTER]
        red_in_layer1 = arrow.state.color == RED and other_motion.state.start_ori in [IN, OUT]
        
        return (blue_in_layer1 and red_in_layer2) or (blue_in_layer2 and red_in_layer1)
    
    @staticmethod
    def get_keys_for_mixed_start_ori(grid_mode: str, letter: Letter, ori_key: str) -> Tuple[str, Dict[str, Any]]:
        """
        Get the keys and data for mixed start orientation.
        
        Args:
            grid_mode: The grid mode to use
            letter: The letter to get data for
            ori_key: The orientation key to use
            
        Returns:
            A tuple of (other_ori_key, other_letter_data)
        """
        other_ori_key = MirroredEntryUtils.get_other_layer3_ori_key(ori_key)
        other_letter_data = MirroredEntryUtils._get_letter_data(grid_mode, other_ori_key, letter)
        return other_ori_key, other_letter_data
    
    @staticmethod
    def _get_letter_data(grid_mode: str, ori_key: str, letter: Letter) -> Dict[str, Any]:
        """
        Get the letter data for the given grid mode, orientation key, and letter.
        
        Args:
            grid_mode: The grid mode to use
            ori_key: The orientation key to use
            letter: The letter to get data for
            
        Returns:
            The letter data
        """
        return (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()
            .get(grid_mode, {})
            .get(ori_key, {})
            .get(letter.value, {})
        )


# From orientation_handler.py
import logging
from typing import List
from enums.letter.letter import Letter
from enums.letter.letter_condition import LetterCondition
from data.constants import BLUE, RED, IN, OUT
from objects.arrow.arrow import Arrow
from .turns_pattern_manager import TurnsPatternManager

logger = logging.getLogger(__name__)

class OrientationHandler:
    def __init__(self, arrow: Arrow, turns_manager: TurnsPatternManager):
        self.arrow = arrow
        self.pictograph = arrow.pictograph
        self.motion = arrow.motion
        self.turns_manager = turns_manager

    def is_mixed_orientation(self) -> bool:
        return self.pictograph.managers.check.starts_from_mixed_orientation()

    def get_hybrid_letters(self) -> List[Letter]:
        return Letter.get_letters_by_condition(LetterCondition.HYBRID)

    def get_mixed_attribute_key(self) -> str:
        letter = self.pictograph.state.letter
        layer = "1" if self.motion.state.start_ori in [IN, OUT] else "2"

        if letter.value in ["S", "T"]:
            attr = self.motion.state.lead_state
            return f"{attr}_from_layer{layer}"
        elif self.pictograph.managers.check.has_hybrid_motions():
            attr = self.motion.state.motion_type
            return f"{attr}_from_layer{layer}"
        else:
            return BLUE if self.arrow.state.color == RED else RED

    def get_standard_attribute_key(self, other_arrow: Arrow) -> str:
        letter = self.pictograph.state.letter

        if letter.value in ["S", "T"]:
            return self.motion.state.lead_state
        elif self.pictograph.managers.check.has_hybrid_motions():
            return self.motion.state.motion_type
        else:
            return BLUE if self.arrow.state.color == RED else RED

    def should_create_standard_mirror(self, other_arrow: "Arrow"):
        turns = self.motion.state.turns
        other_turns = other_arrow.motion.state.turns
        motion_type = self.motion.state.motion_type
        other_motion_type = other_arrow.motion.state.motion_type

        if turns != other_turns and motion_type == other_motion_type:
            return True

        if (
            turns != other_turns
            and motion_type != other_motion_type
            and not self.pictograph.managers.check.has_one_float()
        ):
            return True

        if (
            turns != other_turns
            and motion_type != other_motion_type
            and self.pictograph.managers.check.has_one_float()
        ):
            return True

        return False

    def determine_layer(self) -> str:
        return "1" if self.motion.state.start_ori in [IN, OUT] else "2"

    def get_other_attr_key(self, attribute_key: str) -> str:
        return RED if attribute_key == BLUE else BLUE

# From rotation_angle_processor.py
import logging
from typing import Dict, Any, Optional

from data.constants import DASH, STATIC
from objects.arrow.arrow import Arrow
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import (
    ArrowRotAngleOverrideKeyGenerator,
)

logger = logging.getLogger(__name__)

class RotationAngleProcessor:
    def __init__(self):
        self.key_generator = ArrowRotAngleOverrideKeyGenerator()

    def process_rotation_override(
        self, arrow, original_data, mirrored_data, mirrored_turns_tuple
    ):
        try:
            if not self._should_handle_rotation_angle(arrow):
                return

            rot_angle_override = self._find_rotation_angle_override(original_data)
            if rot_angle_override is None:
                return

            key = self.key_generator.generate_rotation_angle_override_key(arrow)

            if mirrored_turns_tuple not in mirrored_data:
                mirrored_data[mirrored_turns_tuple] = {}

            mirrored_data[mirrored_turns_tuple][key] = rot_angle_override

        except Exception as e:
            logger.error(
                f"Failed to process rotation angle override: {str(e)}", exc_info=True
            )

    def remove_rotation_angle_override(
        self,
        arrow: Arrow,
        mirrored_data: Dict[str, Any],
        mirrored_turns_tuple: str,
        hybrid_key: str,
    ) -> None:
        try:
            if mirrored_turns_tuple in mirrored_data:
                if hybrid_key in mirrored_data[mirrored_turns_tuple]:
                    del mirrored_data[mirrored_turns_tuple][hybrid_key]

                    if not mirrored_data[mirrored_turns_tuple]:
                        del mirrored_data[mirrored_turns_tuple]
        except Exception as e:
            logger.error(
                f"Failed to remove rotation angle override: {str(e)}", exc_info=True
            )

    def _should_handle_rotation_angle(self, arrow: Arrow) -> bool:
        return arrow.motion.state.motion_type in [STATIC, DASH]

    def _find_rotation_angle_override(self, data: Dict[str, Any]) -> Optional[Any]:
        for key, value in data.items():
            if "rot_angle_override" in key:
                return value
        return None


# From special_placement_repository.py
import logging
import os
from typing import Dict, Any

from enums.letter.letter import Letter
from settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_data_path

logger = logging.getLogger(__name__)

class SpecialPlacementRepository:
    """Repository for accessing and updating special placement data."""
    
    def __init__(self, grid_mode: str):
        """Initialize the repository with the given grid mode."""
        self.grid_mode = grid_mode
    
    def get_letter_data(self, letter: Letter, ori_key: str) -> Dict[str, Any]:
        """Get the letter data for the given letter and orientation key."""
        try:
            placements = AppContext.special_placement_loader().load_special_placements_fresh()
            grid_data = placements.get(self.grid_mode, {})
            ori_data = grid_data.get(ori_key, {})
            letter_data = ori_data.get(letter.value, {})
            return letter_data or {}
        except Exception as e:
            logger.error(f"Failed to get letter data: {str(e)}", exc_info=True)
            return {}
    
    def save_letter_data(self, letter: Letter, ori_key: str, letter_data: Dict[str, Any]) -> bool:
        """Save the letter data for the given letter and orientation key."""
        try:
            file_path = self._get_file_path(letter, ori_key)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            placement_data = AppContext.special_placement_loader().load_json_data(file_path) or {}
            placement_data[letter.value] = letter_data
            AppContext.special_placement_saver().save_json_data(placement_data, file_path)
            return True
        except Exception as e:
            logger.error(f"Failed to save letter data: {str(e)}", exc_info=True)
            return False
    
    def _get_file_path(self, letter: Letter, ori_key: str) -> str:
        """Get the file path for the given letter and orientation key."""
        return get_data_path(
            os.path.join(
                "arrow_placement",
                self.grid_mode,
                "special",
                ori_key,
                f"{letter.value}_placements.json",
            )
        )
    
    def clean_placement_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean the placement data by removing empty dictionaries and normalizing values."""
        if not isinstance(data, dict):
            return data
        
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                cleaned_value = self.clean_placement_data(value)
                if cleaned_value:
                    result[key] = cleaned_value
            elif isinstance(value, list):
                result[key] = [int(item) if isinstance(item, float) and item.is_integer() else item for item in value]
            elif isinstance(value, float) and value.is_integer():
                result[key] = int(value)
            else:
                result[key] = value
        
        return result


# From turns_pattern_manager.py
"""
Manages the generation and manipulation of turns patterns.
"""

import logging
from typing import TYPE_CHECKING, Dict, Any

from objects.arrow.arrow import Arrow
from data.constants import BLUE_ATTRS, RED_ATTRS, TURNS

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph


class TurnsPatternManager:
    """
    Manages the generation and mirroring of turns patterns.
    Provides functionality to create consistent representations of turns patterns
    for both normal and mirrored entries.
    """




    def extract_turns_from_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract turns values from pictograph data.

        Args:
            data: The pictograph data to extract turns from

        Returns:
            A dictionary mapping color attributes to turns values
        """
        try:
            result = {}
            if BLUE_ATTRS in data and TURNS in data[BLUE_ATTRS]:
                result[BLUE_ATTRS] = data[BLUE_ATTRS][TURNS]
            if RED_ATTRS in data and TURNS in data[RED_ATTRS]:
                result[RED_ATTRS] = data[RED_ATTRS][TURNS]
            return result
        except Exception as e:
            logger.error(f"Failed to extract turns from data: {str(e)}", exc_info=True)
            return {}


# From __init__.py
"""
Mirrored Entry Management System
-------------------------------

This module provides functionality for managing mirrored entries in special placements.
It is designed to be a clean replacement for the old mirrored entry system.

Main Components:
- MirroredEntryService: Main entry point for all mirrored entry operations
- MirroredEntryFactory: Factory for creating and configuring mirrored entry components
- MirroredEntryAdapter: Adapter for integrating with existing code
"""

from .mirrored_entry_service import MirroredEntryService
from .mirrored_entry_factory import MirroredEntryFactory
from .mirrored_entry_adapter import MirroredEntryAdapter
from .mirrored_entry_utils import MirroredEntryUtils

# Export the main components
__all__ = [
    'MirroredEntryService',
    'MirroredEntryFactory',
    'MirroredEntryAdapter',
    'MirroredEntryUtils',
]


# From __init__.py.py
"""
Mirrored Entry Management System
-------------------------------

This module provides functionality for managing mirrored entries in special placements.
It is designed to be a clean replacement for the old mirrored entry system.

Main Components:
- MirroredEntryService: Main entry point for all mirrored entry operations
- MirroredEntryFactory: Factory for creating and configuring mirrored entry components
- MirroredEntryAdapter: Adapter for integrating with existing code
"""

from .mirrored_entry_service import MirroredEntryService
from .mirrored_entry_factory import MirroredEntryFactory
from .mirrored_entry_adapter import MirroredEntryAdapter
from .mirrored_entry_utils import MirroredEntryUtils

# Export the main components
__all__ = [
    'MirroredEntryService',
    'MirroredEntryFactory',
    'MirroredEntryAdapter',
    'MirroredEntryUtils',
]


# From __init__.py


# From __init__.py


# From rot_angle_override_coordinator.py
# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideCoordinator:
    """Handles high-level coordination of rotation angle overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager

    def execute_override_flow(self) -> None:
        if not self._should_execute_override():
            return

        override_data = self.manager.data_handler.prepare_override_data()
        self.manager.data_handler.apply_rotation_override(override_data)
        self.manager.view_updater.refresh_affected_views()

    def _should_execute_override(self) -> bool:
        return self.manager.validator.is_valid_override_condition()


# From rot_angle_override_data_handler.py
# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rot_angle_override.types import (
    OverrideData,
)
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import (
    ArrowRotAngleOverrideKeyGenerator,
)
from settings_manager.global_settings.app_context import AppContext

from typing import cast

if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideDataHandler:
    """Manages data operations for rotation overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager
        self.key_generator = ArrowRotAngleOverrideKeyGenerator()

    def prepare_override_data(self) -> OverrideData:

        letter = self.manager.current_letter
        ori_key = self._generate_ori_key()
        turns_tuple = self.manager.turns_generator.generate_turns_tuple(
            self.manager.view.pictograph
        )

        rot_angle_key = self._generate_rot_angle_key()
        placement_data = (
            AppContext.special_placement_loader().load_or_return_special_placements()
        )
        if not self._validate_placement_data(placement_data):
            raise ValueError("Invalid placement data structure")

        return cast(
            OverrideData,
            {
                "letter": letter,
                "ori_key": ori_key,
                "turns_tuple": turns_tuple,
                "rot_angle_key": rot_angle_key,
                "placement_data": placement_data,
            },
        )

    def _validate_placement_data(self, data: dict) -> bool:
        try:
            # Basic structure validation
            return all(
                isinstance(mode_data.get(ori_key, {}).get(letter, {}), dict)
                for mode_data in data.values()
                for ori_key in mode_data
                for letter in mode_data[ori_key]
            )
        except AttributeError:
            return False

    def apply_rotation_override(self, override_data: OverrideData) -> None:
        letter_data = self._get_letter_data(override_data)
        turn_data = letter_data.get(override_data["turns_tuple"], {})

        if override_data["rot_angle_key"] in turn_data:
            self._remove_rotation_override(override_data, turn_data)
        else:
            self._add_rotation_override(override_data, turn_data)

        self._save_updated_data(override_data, letter_data)
        self._handle_mirrored_entries(override_data, turn_data)

    def _generate_ori_key(self) -> str:
        return self.manager.data_updater.ori_key_generator.generate_ori_key_from_motion(
            AppContext.get_selected_arrow().motion
        )

    def _generate_rot_angle_key(self) -> str:
        return self.key_generator.generate_rotation_angle_override_key(
            AppContext.get_selected_arrow()
        )

    # rot_angle_override_data_handler.py

    def _get_letter_data(
        self, override_data: OverrideData
    ) -> dict[str, dict[str, bool]]:
        grid_mode = self.manager.view.pictograph.state.grid_mode
        ori_key = override_data["ori_key"]

        return (
            override_data["placement_data"]
            .get(grid_mode, {})
            .get(ori_key, {})
            .get(override_data["letter"].value, {})
        )

    def _remove_rotation_override(self, override_data: dict, turn_data: dict) -> None:
        del turn_data[override_data["rot_angle_key"]]
        self.manager.mirror_handler.handle_removal(override_data["rot_angle_key"])

    # rot_angle_override_data_handler.py
    def _add_rotation_override(
        self, override_data: OverrideData, turn_data: dict[str, bool]
    ) -> None:
        turn_data[override_data["rot_angle_key"]] = True
        self.manager.mirror_handler.handle_addition(cast(dict[str, bool], turn_data))

    def _save_updated_data(
        self, override_data: OverrideData, letter_data: dict
    ) -> None:
        self.manager.data_updater.update_specific_entry_in_json(
            override_data["letter"], letter_data, override_data["ori_key"]
        )

    def _handle_mirrored_entries(
        self, override_data: OverrideData, turn_data: dict
    ) -> None:
        self.manager.mirror_handler.update_mirrored_entries(
            override_data["rot_angle_key"],
            turn_data.get(override_data["rot_angle_key"], None),
        )


# From rot_angle_override_manager.py
# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING
from enums.letter.letter import Letter
from ..data_updater.special_placement_data_updater import SpecialPlacementDataUpdater
from .rot_angle_override_data_handler import RotAngleOverrideDataHandler
from .rot_angle_override_coordinator import RotAngleOverrideCoordinator
from .rot_angle_override_validator import RotAngleOverrideValidator
from .rot_angle_override_mirror_handler import RotAngleOverrideMirrorHandler
from .rot_angle_override_view_updater import RotAngleOverrideViewUpdater
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)

if TYPE_CHECKING:
    from ..hotkey_graph_adjuster import HotkeyGraphAdjuster


class RotAngleOverrideManager:
    """Main coordinator for arrow rotation angle override functionality"""

    def __init__(self, hotkey_graph_adjuster: "HotkeyGraphAdjuster") -> None:
        self.hotkey_graph_adjuster = hotkey_graph_adjuster
        self.view = hotkey_graph_adjuster.ge_view
        self.current_letter = self.view.pictograph.state.letter

        self.data_updater = self._get_data_updater()
        self.turns_generator = TurnsTupleGenerator()

        self.validator = RotAngleOverrideValidator(self)
        self.data_handler = RotAngleOverrideDataHandler(self)
        self.view_updater = RotAngleOverrideViewUpdater(self)
        self.mirror_handler = RotAngleOverrideMirrorHandler(self)
        self.coordinator = RotAngleOverrideCoordinator(self)

    def handle_arrow_rot_angle_override(self) -> None:
        """Main entry point for handling rotation angle overrides"""
        self.coordinator.execute_override_flow()

    def _get_data_updater(self) -> SpecialPlacementDataUpdater:
        return self.view.pictograph.managers.arrow_placement_manager.data_updater

    @property
    def current_letter(self) -> Letter:
        return self.view.pictograph.state.letter

    @current_letter.setter
    def current_letter(self, value: Letter):
        self.view.pictograph.state.letter = value


# From rot_angle_override_mirror_handler.py
# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING, Optional


from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideMirrorHandler:
    """Manages mirrored entry updates for rotation overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager

    def handle_addition(self, turn_data: dict[str, bool]) -> None:
        mirrored_entry_manager = self.manager.data_updater.mirrored_entry_manager
        mirrored_entry_manager.rot_angle_manager.update_rotation_angle_in_mirrored_entry(
            AppContext.get_selected_arrow(),
            turn_data,  # Now properly typed
        )

    def handle_removal(self, hybrid_key: str) -> None:
        mirrored_entry_handler = self.manager.data_updater.mirrored_entry_manager
        if mirrored_entry_handler:
            mirrored_entry_handler.rot_angle_manager.remove_rotation_angle_in_mirrored_entry(
                AppContext.get_selected_arrow(),
                hybrid_key,
            )

    def update_mirrored_entries(self, key: str, value: Optional[bool]) -> None:
        if value is not None:
            self.handle_addition({key: value})
        else:
            self.handle_removal(key)


# From rot_angle_override_validator.py
# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING
from data.constants import STATIC, DASH

from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideValidator:
    """Validates conditions for rotation overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager

    def is_valid_override_condition(self) -> bool:
        selected_arrow = AppContext.get_selected_arrow()
        return (
            selected_arrow is not None
            and selected_arrow.motion.state.motion_type in [STATIC, DASH]
        )


# From rot_angle_override_view_updater.py
# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING

from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideViewUpdater:
    """Handles UI updates related to rotation overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager

    def refresh_affected_views(self) -> None:
        AppContext.special_placement_loader().reload()
        self._update_pictographs()

    def _update_pictographs(self) -> None:
        target_letter = self.manager.current_letter
        collector = self.manager.view.main_widget.pictograph_collector

        for pictograph in collector.collect_all_pictographs():
            if pictograph.state.letter == target_letter:
                pictograph.managers.updater.update_pictograph(
                    pictograph.state.pictograph_data
                )
                pictograph.managers.arrow_placement_manager.update_arrow_placements()


# From types.py
# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/rot_angle_override/types.py
from typing import TypedDict
from enums.letter.letter import Letter


# types.py
from typing import NotRequired


class PlacementDataEntry(TypedDict):
    turns_tuple: dict[str, dict[str, bool]]


class OrientationData(TypedDict):
    letters: dict[str, PlacementDataEntry]


class GridModeData(TypedDict):
    orientations: dict[str, OrientationData]


class PlacementData(TypedDict):
    grid_modes: dict[str, GridModeData]


class OverrideData(TypedDict):
    letter: Letter
    ori_key: str
    turns_tuple: str
    rot_angle_key: str
    placement_data: PlacementData
    validation_hash: NotRequired[str]  # Example of optional field


# From __init__.py


# From __init__.py


# From __init__.py


# From GE_pictograph_container.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from base_widgets.pictograph.elements.views.GE_pictograph_view import GE_PictographView
from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph import (
    GE_Pictograph,
)


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat
    from ..graph_editor import GraphEditor


class GraphEditorPictographContainer(QWidget):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.setup_pictograph()

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.GE_view)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def setup_pictograph(self):
        self.GE_pictograph = GE_Pictograph(self)
        self.GE_view = GE_PictographView(self, self.GE_pictograph)

    def update_pictograph(self, reference_beat: "Beat" = None) -> None:
        selected_beat_view = (
            self.graph_editor.sequence_workbench.beat_frame.get.currently_selected_beat_view()
        )
        if not selected_beat_view:
            return
        if not reference_beat:
            reference_beat = selected_beat_view.beat

        view = self.GE_view
        pictograph = view.pictograph

        pictograph.is_blank = False
        view.reference_beat = reference_beat
        view.is_start_pos = reference_beat.view.is_start_pos
        pictograph.state.blue_reversal = reference_beat.state.blue_reversal
        pictograph.state.red_reversal = reference_beat.state.red_reversal

        pictograph.managers.updater.update_pictograph(
            reference_beat.state.pictograph_data
        )

        beat_number_text = reference_beat.beat_number_item.beat_number_int
        if beat_number_text:
            pictograph.beat_number_item.update_beat_number(beat_number_text)
        else:
            pictograph.start_text_item.add_start_text()
        self.graph_editor.pictograph_selected.emit()

    def resizeEvent(self, event):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)


# From __init__.py


# From __init__.py


# From __init__.py


