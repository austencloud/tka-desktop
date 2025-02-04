from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from data.constants import PRO, ANTI, FLOAT, RED, BLUE
from .motion_type_dialog import MotionTypeDialog

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget


class MotionTypeLabelWidget(QWidget):
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.turns_widget = turns_widget
        self.label = QLabel("", self)
        self._setup_components()
        self._setup_layout()

    def _setup_components(self) -> None:
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # self.label.mousePressEvent = self._on_label_clicked  # Add click handler
        # self.label.enterEvent = self._on_hover_enter  # Add hover enter handler
        # self.label.leaveEvent = self._on_hover_leave  # Add hover leave handler

        # Set initial styles
        self.label.setStyleSheet("""
            padding: 5px 10px;
            border: 2px solid transparent;
            border-radius: 5px;
        """)

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(1)
        self.layout.addWidget(self.label)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def _on_label_clicked(self, event) -> None:
        """Open a dialog to select the motion type."""
        if self.turns_widget.turns_box.matching_motion.motion_type in [PRO, ANTI, FLOAT]:
            dialog = MotionTypeDialog(self)
            dialog.show_motion_type_dialog()

    def set_motion_type(self, motion_type: str) -> None:
        """Set the motion type and update the label."""
        motion = self.turns_widget.turns_box.matching_motion
        self.turns_widget.motion_type_setter.set_motion_type(motion, motion_type)
        self.label.setText(motion_type.capitalize())

    def update_display(self, motion_type: str) -> None:
        """Update the display based on the motion type."""
        self.label.setText(motion_type.capitalize())
        turns_box_size = self.turns_widget.turns_box.size()

        self.label.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.label.setStyleSheet(f"""
            padding: 5px 10px;
            border-radius: 5px;
            background-color: white;
        """)

    def update_motion_type_label(self, motion_type: str) -> None:
        """Update the motion type label based on the selected motion type."""
        self.label.setText(motion_type.capitalize())

    def resize_buttons(self) -> None:
        """Resize the label based on the parent widget size."""
        font_size = self.turns_widget.turns_box.graph_editor.width() // 40
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        self.label.setFont(font)

    def _on_hover_enter(self, event) -> None:
        """Handle the hover enter event for the label."""
        if self.turns_widget.turns_box.matching_motion.motion_type in [PRO, ANTI, FLOAT]:
            turns_box_color = self.turns_widget.turns_box.color
            turns_box_size = self.turns_widget.turns_box.size()

            if turns_box_color == RED:
                border_color = "#ED1C24"
            elif turns_box_color == BLUE:
                border_color = "#2E3192"
            else:
                border_color = "black"

            border_thickness = turns_box_size.height() // 100

            self.label.setStyleSheet(f"""
                padding: 5px 10px;
                border: {border_thickness}px solid {border_color};
                border-radius: 5px;
                background-color: #e0e0e0;
            """)

    def _on_hover_leave(self, event) -> None:
        """Handle the hover leave event for the label."""
        if self.turns_widget.turns_box.matching_motion.motion_type in [PRO, ANTI, FLOAT]:
            turns_box_size = self.turns_widget.turns_box.size()

            border_thickness = turns_box_size.height() // 100

            self.label.setStyleSheet(f"""
                padding: 5px 10px;
                border: {border_thickness}px solid black;
                border-radius: 5px;
                background-color: white;
            """)
        else:
            self.label.setStyleSheet("""
                padding: 5px 10px;
                border: 2px solid black;
                border-radius: 5px;
                background-color: transparent;
                color: black;
            """)
