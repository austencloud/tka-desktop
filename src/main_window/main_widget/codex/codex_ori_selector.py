# codex_ori_selector.py

from typing import TYPE_CHECKING
import logging

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QComboBox, QVBoxLayout
from PyQt6.QtCore import Qt

from data.constants import BLUE_ATTRS, RED_ATTRS, START_ORI, IN, CLOCK, OUT, COUNTER

if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget

logger = logging.getLogger(__name__)


class CodexOriSelector(QWidget):
    """A widget containing a label and combo box for selecting Codex orientation/rotation modes."""

    options = [IN, CLOCK, OUT, COUNTER]

    def __init__(self, control_widget: "CodexControlWidget"):
        """Initializes the orientation selector widget with references from the control widget."""
        super().__init__(control_widget)
        self.control_widget = control_widget
        self.codex = control_widget.codex

        self.start_ori_label = QLabel("Start Orientation:", self)
        self.start_ori_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(self.options)
        self.combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combo_box.currentIndexChanged.connect(
            lambda: self.update_orientations(self.combo_box.currentText())
        )

        combo_box_layout = QHBoxLayout()
        combo_box_layout.addStretch(1)
        combo_box_layout.addWidget(self.combo_box)
        combo_box_layout.addStretch(1)

        # Arrange them in a horizontal layout
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.start_ori_label)
        self.layout.addLayout(combo_box_layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

    def update_orientations(self, orientation: str):
        """Updates the 'start_ori' attribute of all pictographs to the selected orientation."""
        try:
            self.setCursor(Qt.CursorShape.WaitCursor)
            for letter_str, view in self.codex.section_manager.codex_views.items():
                scene = view.pictograph
                if scene.state.pictograph_data:
                    new_dict = scene.state.pictograph_data.copy()
                    if BLUE_ATTRS in new_dict:
                        new_dict[BLUE_ATTRS][START_ORI] = orientation
                    if RED_ATTRS in new_dict:
                        new_dict[RED_ATTRS][START_ORI] = orientation
                    scene.managers.updater.update_pictograph(new_dict)
                    logger.debug(
                        f"Updated orientation for pictograph '{letter_str}' to '{orientation}'."
                    )
        except Exception as e:
            logger.exception(f"Error during update_orientation_all: {e}")
        finally:
            self.unsetCursor()

    def resizeEvent(self, event) -> None:
        """Handles resizing logic, adjusting label and combo box sizes proportionally."""
        super().resizeEvent(event)
        self._resize_combo_box()
        self._resize_start_ori_label()

    def _resize_start_ori_label(self):
        label_font = self.start_ori_label.font()
        label_font.setPointSize(int(self.codex.main_widget.height() * 0.018))
        self.start_ori_label.setFont(label_font)

    def _resize_combo_box(self):
        combo_width = int(self.codex.main_widget.width() * 0.06)
        combo_height = int(self.codex.main_widget.height() * 0.04)

        combo_font = self.combo_box.font()
        combo_font_size = combo_height // 2
        combo_font.setPointSize(combo_font_size)
        combo_font.setBold(True)

        self.combo_box.setFixedHeight((combo_height))
        self.combo_box.setFixedWidth(combo_width)
        self.combo_box.setFont(combo_font)
