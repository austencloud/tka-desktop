from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from .advanced_start_pos_picker import AdvancedStartPosPicker


class AdvancedStartPosOriPicker(QWidget):
    DEFAULT_BUTTON_STYLE = """
        QPushButton {
            padding: 4px;
            margin: 2px;
            background-color: rgba(255, 255, 255, 0.5);
            border: 1px solid lightgray;
        }
        QPushButton:hover {
            background-color: rgba(220, 220, 220, 1);
        }
    """

    PRESSED_BUTTON_STYLE = """
        QPushButton {
            padding: 4px;
            margin: 2px;
            background-color: rgba(180, 180, 180, 1);
            border: 1px solid gray;
        }
        QPushButton:hover {
            background-color: rgba(180, 180, 180, 1);
        }
    """

    def __init__(self, advanced_start_pos_picker: "AdvancedStartPosPicker") -> None:
        super().__init__(advanced_start_pos_picker)
        self.advanced_start_pos_picker = advanced_start_pos_picker
        self.main_widget = advanced_start_pos_picker.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        # Store selected buttons by color (blue for left, red for right)
        self.selected_button: dict[str, QPushButton] = {"blue": None, "red": None}
        self.buttons: dict[str, list[QPushButton]] = {"blue": [], "red": []}

        self.init_ui()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(0)

        # Create buttons based on color (blue for left, red for right)
        self.blue_header = self.setup_orientation_buttons("Left", "blue")
        self.red_header = self.setup_orientation_buttons("Right", "red")

        self.header_labels: list[QLabel] = [self.blue_header, self.red_header]

        # Set default orientation ("in") for both blue and red buttons
        self.set_orientation("in", self.buttons["blue"][0], "blue")
        self.set_orientation("in", self.buttons["red"][0], "red")

    def setup_orientation_buttons(self, hand_label_text: str, color: str) -> QLabel:
        layout = QVBoxLayout()
        header = QLabel(hand_label_text)
        header.setStyleSheet(f"color: {color}; font-weight: bold;")
        layout.addWidget(
            header,
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
        )

        line = QLabel()
        line.setFixedHeight(4)
        line.setStyleSheet(f"background-color: {color};")
        layout.addWidget(line)
        layout.setSpacing(5)

        # Create buttons for the specified color (blue or red)
        self.create_orientation_buttons(layout, color, ["in", "out"])
        self.create_orientation_buttons(layout, color, ["counter", "clock"])

        self.main_layout.addLayout(layout)
        return header

    def create_orientation_buttons(
        self, layout: QVBoxLayout, color: str, orientations: list[str]
    ) -> None:
        row_layout = QHBoxLayout()
        for orientation in orientations:
            button = QPushButton(orientation)
            self.buttons[color].append(button)

            button.setStyleSheet(self.DEFAULT_BUTTON_STYLE)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked, ori=orientation, btn=button: self.set_orientation(
                    ori, btn, color
                )
            )
            row_layout.addWidget(button)
        layout.addLayout(row_layout)

    def set_orientation(self, ori: str, button: QPushButton, color: str) -> None:
        if self.selected_button[color]:
            self.selected_button[color].setStyleSheet(self.DEFAULT_BUTTON_STYLE)

        self.selected_button[color] = button
        self.selected_button[color].setStyleSheet(self.PRESSED_BUTTON_STYLE)

        self.update_orientation(ori, color)

    def update_orientation(self, ori: str, color: str) -> None:
        for (
            start_pos_pictographs_by_letter
        ) in self.advanced_start_pos_picker.start_pos_cache.values():
            for pictograph in start_pos_pictographs_by_letter:
                pictograph.pictograph_dict[f"{color}_attributes"]["start_ori"] = ori
                if color == "red":
                    pictograph.pictograph_dict["red_attributes"]["end_ori"] = ori
                pictograph.updater.update_pictograph(pictograph.pictograph_dict)

    def resize_default_ori_picker(self) -> None:
        width = int(self.advanced_start_pos_picker.construct_tab.width())
        header_font_size = width // 35
        for header in self.header_labels:
            header.setFont(QFont("Arial", header_font_size, QFont.Weight.Bold))
        self.setMaximumWidth(width)

        for button in self.buttons["blue"] + self.buttons["red"]:
            button.setFixedWidth(width // 6)
            button.setFont(QFont("Arial", width // 40))
