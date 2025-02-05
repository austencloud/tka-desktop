from .codex_animation_manager import CodexAnimationManager
from .codex_color_swap_manager import CodexColorSwapManager
from .codex_control_button import CodexControlButton
from .codex_control_widget import CodexControlWidget
from .codex_data_manager import CodexDataManager
from .codex_mirror_manager import CodexMirrorManager
from .codex_ori_selector import CodexOriSelector
from .codex_pictograph_view import CodexPictographView
from .codex_rotation_manager import CodexRotationManager
from .codex_scroll_area import CodexScrollArea
from .codex_section_manager import CodexSectionManager
from .codex_section_type_label import CodexSectionTypeLabel
from .codex_toggle_button import CodexToggleButton
from Enums.letters import Letter
from Enums.letters import LetterType
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QObject, QAbstractAnimation
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QComboBox, QVBoxLayout
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from base_widgets.base_pictograph.pictograph import Pictograph
from base_widgets.base_pictograph.pictograph_view import PictographView
from data.locations import cw_loc_order
from data.locations import vertical_loc_mirror_map
from data.positions import mirrored_positions
from data.positions_map import positions_map
from typing import TYPE_CHECKING
from typing import TYPE_CHECKING, Callable
from typing import TYPE_CHECKING, Optional
from utilities.path_helpers import get_images_and_data_path
import logging

# From codex.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout


from .codex_scroll_area import CodexScrollArea
from .codex_toggle_button import CodexToggleButton
from .codex_control_widget import CodexControlWidget
from .codex_section_manager import CodexSectionManager
from .codex_animation_manager import CodexAnimationManager
from .codex_data_manager import CodexDataManager

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.learn_tab import LearnTab


class Codex(QWidget):
    """Displays pictographs with a control panel to modify them."""

    def __init__(self, learn_tab: "LearnTab") -> None:
        super().__init__(learn_tab)
        self.main_widget = learn_tab.main_widget
        self.learn_tab = learn_tab

        # Components
        self.toggle_button = CodexToggleButton(self)
        self.control_widget = CodexControlWidget(self)
        self.scroll_area = CodexScrollArea(self)

        # Managers
        self.data_manager = CodexDataManager(self)
        self.section_manager = CodexSectionManager(self)
        self.animation_manager = CodexAnimationManager(self)

        self._setup_layout()

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.control_widget)
        self.main_layout.addWidget(self.scroll_area)


# From codex_animation_manager.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QObject, QAbstractAnimation
import logging

if TYPE_CHECKING:
    from .codex import Codex

logger = logging.getLogger(__name__)


class CodexAnimationManager(QObject):
    """Manages animations for the CodexWidget, including opening and closing."""

    ANIMATION_DURATION = 350  # milliseconds

    def __init__(self, codex: "Codex"):
        super().__init__(codex)
        self.codex = codex

        self.animation = QPropertyAnimation(self.codex, b"maximumWidth")
        self.animation.setDuration(self.ANIMATION_DURATION)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.target_width = 0

    def animate(self, show: bool):
        """Toggle the visibility of the codex with animations for both showing and hiding."""
        logger.debug(f"Toggling codex visibility to {'show' if show else 'hide'}.")

        if self.animation.state() == QAbstractAnimation.State.Running:
            self.animation.stop()

        learn_widget = self.codex.learn_tab
        learn_widget_width = learn_widget.width()
        current_width = self.codex.width()

        if show:
            self.target_width = int(learn_widget_width * 0.5)
            self.animation.setStartValue(current_width)
            self.animation.setEndValue(self.target_width)

        else:
            self.target_width = 0
            self.animation.setStartValue(current_width)
            self.animation.setEndValue(self.target_width)

        self.animation.start()


# From codex_color_swap_manager.py
from typing import TYPE_CHECKING

import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex.codex_control_widget import (
        CodexControlWidget,
    )


class CodexColorSwapManager:
    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex

    def _swap_colors(self, pictograph):
        if not pictograph:
            return
        pictograph["blue_attributes"], pictograph["red_attributes"] = (
            pictograph["red_attributes"],
            pictograph["blue_attributes"],
        )

    def swap_colors_in_codex(self):
        for pictograph in self.codex.data_manager.pictograph_data.values():
            self._swap_colors(pictograph)
        try:
            for letter_str, view in self.codex.section_manager.codex_views.items():
                scene = view.pictograph
                if scene.pictograph_data:
                    # Implement actual color swap logic here
                    scene.updater.update_pictograph(scene.pictograph_data)
                    logger.debug(f"Swapped colors for pictograph '{letter_str}'.")
        except Exception as e:
            logger.exception(f"Error during color_swap_all: {e}")


# From codex_constants.py


# From codex_control_button.py
from typing import TYPE_CHECKING, Callable
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex.codex_control_widget import (
        CodexControlWidget,
    )


class CodexControlButton(QPushButton):
    """A reusable button class for the Codex control panel."""

    ICON_BASE_PATH = "images/icons/sequence_workbench_icons"

    def __init__(
        self, control_widget: "CodexControlWidget", icon_name: str, callback: Callable
    ):
        """
        Initializes the control button with the specified icon and callback.

        :param control_widget: The CodexControlWidget that this button belongs to.
        :param icon_name: Name of the icon file (e.g. 'rotate.png').
        :param callback: The function to call when this button is clicked.
        """
        super().__init__(control_widget)
        self._control_widget = control_widget
        self.icon_name = icon_name
        self.callback = callback

        self._setup_appearance()
        self._setup_connections()

    def _setup_appearance(self) -> None:
        """Sets the button icon and basic appearance."""
        icon_path = get_images_and_data_path(f"{self.ICON_BASE_PATH}/{self.icon_name}")
        self.setIcon(QIcon(icon_path))
        font = QFont()
        font.setBold(True)
        self.setFont(font)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _setup_connections(self) -> None:
        """Connects the button click signal to the specified callback."""
        self.clicked.connect(self.callback)

    def resizeEvent(self, event) -> None:
        """Adjust icon sizes and selector size dynamically on resize."""
        super().resizeEvent(event)
        codex = self._control_widget.codex
        if not codex:
            return

        button_size = int(codex.height() * 0.05)
        icon_size = QSize(int(button_size * 0.8), int(button_size * 0.8))
        self.setFixedSize(button_size, button_size)
        self.setIconSize(icon_size)


# From codex_control_widget.py
# codex_control_widget.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt

from .codex_color_swap_manager import CodexColorSwapManager
from .codex_mirror_manager import CodexMirrorManager
from .codex_rotation_manager import CodexRotationManager
from .codex_control_button import CodexControlButton
from .codex_ori_selector import CodexOriSelector

if TYPE_CHECKING:
    from .codex import Codex


class CodexControlWidget(QWidget):

    def __init__(self, codex: "Codex"):
        super().__init__(codex)
        self.codex = codex

        # Managers
        self.mirror_manager = CodexMirrorManager(self)
        self.color_swap_manager = CodexColorSwapManager(self)
        self.rotation_manager = CodexRotationManager(self)

        # Components
        self.ori_selector = CodexOriSelector(self)
        self.codex_buttons: list[CodexControlButton] = self._setup_buttons()

        self._setup_layout()

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.ori_selector)
        self.setLayout(self.main_layout)

        self.setStyleSheet(
            """
            QWidget {
                background: transparent;
            }
            QPushButton {
                background-color: lightgray;
                border: 1px solid gray;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: white;
            }
            QComboBox {
                background-color: lightgray;
                border: 1px solid gray;
                border-radius: 5px;
            }
            """
        )

    def _setup_buttons(self) -> list[CodexControlButton]:
        """Creates the control buttons (rotate, mirror, color swap) in a systematic way."""
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.setContentsMargins(5, 5, 5, 5)
        self.button_layout.setSpacing(10)

        codex_buttons: list[CodexControlButton] = []
        buttons_data = [
            ("rotate.png", self.rotation_manager.rotate_codex),
            ("mirror.png", self.mirror_manager.mirror_codex),
            ("yinyang1.png", self.color_swap_manager.swap_colors_in_codex),
        ]

        for icon_name, callback in buttons_data:
            button = CodexControlButton(
                control_widget=self, icon_name=icon_name, callback=callback
            )
            codex_buttons.append(button)
            self.button_layout.addWidget(button)

        return codex_buttons


# From codex_data_manager.py
# pictograph_data_manager.py

from typing import TYPE_CHECKING, Optional
from Enums.letters import Letter

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex.codex import Codex
from Enums.letters import Letter


class CodexDataManager:
    """Manages the initialization and retrieval of pictograph data."""

    def __init__(self, codex: "Codex"):
        self.main_widget = codex.main_widget
        self.pictograph_data: dict[str, Optional[dict]] = (
            self._initialize_pictograph_data()
        )

    def _initialize_pictograph_data(self) -> dict[str, Optional[dict]]:
        """Initializes the pictograph data for all letters."""
        letters = [letter.value for letter in Letter]

        pictograph_data = {}
        for letter in letters:
            data = self._get_pictograph_data(letter)
            if data:
                current_data = (
                    self.main_widget.pictograph_data_loader.find_pictograph_data(
                        {
                            "letter": letter,
                            "start_pos": data["start_pos"],
                            "end_pos": data["end_pos"],
                            "blue_motion_type": data["blue_motion_type"],
                            "red_motion_type": data["red_motion_type"],
                        }
                    )
                )
                pictograph_data[letter] = current_data
            else:
                pictograph_data[letter] = None  # Or handle as needed

        return pictograph_data

    def _get_pictograph_data(self, letter: str) -> Optional[dict]:
        """Returns the parameters for a given letter."""
        params_map = {
            "A": {
                "start_pos": "alpha1",
                "end_pos": "alpha3",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "B": {
                "start_pos": "alpha1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "C": {
                "start_pos": "alpha1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "D": {
                "start_pos": "beta1",
                "end_pos": "alpha3",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "E": {
                "start_pos": "beta1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "F": {
                "start_pos": "beta1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "G": {
                "start_pos": "beta3",
                "end_pos": "beta5",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "H": {
                "start_pos": "beta3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "I": {
                "start_pos": "beta3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "J": {
                "start_pos": "alpha3",
                "end_pos": "beta5",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "K": {
                "start_pos": "alpha3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "L": {
                "start_pos": "alpha3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "M": {
                "start_pos": "gamma13",
                "end_pos": "gamma3",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "N": {
                "start_pos": "gamma13",
                "end_pos": "gamma3",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "O": {
                "start_pos": "gamma13",
                "end_pos": "gamma3",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "P": {
                "start_pos": "gamma3",
                "end_pos": "gamma9",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "Q": {
                "start_pos": "gamma3",
                "end_pos": "gamma9",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "R": {
                "start_pos": "gamma3",
                "end_pos": "gamma9",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "S": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "T": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "U": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "V": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "pro",
                "red_motion_type": "anti",
            },
            "W": {
                "start_pos": "gamma13",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "X": {
                "start_pos": "gamma13",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "Y": {
                "start_pos": "gamma11",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "Z": {
                "start_pos": "gamma11",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "Σ": {
                "start_pos": "alpha3",
                "end_pos": "gamma13",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "Δ": {
                "start_pos": "alpha3",
                "end_pos": "gamma13",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "θ": {
                "start_pos": "beta5",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "Ω": {
                "start_pos": "beta5",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "W-": {
                "start_pos": "gamma5",
                "end_pos": "alpha3",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "X-": {
                "start_pos": "gamma5",
                "end_pos": "alpha3",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "Y-": {
                "start_pos": "gamma3",
                "end_pos": "beta5",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "Z-": {
                "start_pos": "gamma3",
                "end_pos": "beta5",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "Σ-": {
                "start_pos": "beta3",
                "end_pos": "gamma13",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "Δ-": {
                "start_pos": "beta3",
                "end_pos": "gamma13",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "θ-": {
                "start_pos": "alpha5",
                "end_pos": "gamma11",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "Ω-": {
                "start_pos": "alpha5",
                "end_pos": "gamma11",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "Φ": {
                "start_pos": "beta7",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "dash",
            },
            "Ψ": {
                "start_pos": "alpha1",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "dash",
            },
            "Λ": {
                "start_pos": "gamma7",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "dash",
            },
            "Φ-": {
                "start_pos": "alpha3",
                "end_pos": "alpha7",
                "blue_motion_type": "dash",
                "red_motion_type": "dash",
            },
            "Ψ-": {
                "start_pos": "beta1",
                "end_pos": "beta5",
                "blue_motion_type": "dash",
                "red_motion_type": "dash",
            },
            "Λ-": {
                "start_pos": "gamma15",
                "end_pos": "gamma11",
                "blue_motion_type": "dash",
                "red_motion_type": "dash",
            },
            "α": {
                "start_pos": "alpha3",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            "β": {
                "start_pos": "beta5",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            "Γ": {
                "start_pos": "gamma11",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            # Add more letters and their parameters as needed
        }

        return params_map.get(letter)

    def get_pictograph_data(self) -> dict[str, Optional[dict]]:
        """Returns the initialized pictograph data."""
        return self.pictograph_data


# From codex_letter_groups.py
# codex_letter_groups.py

from Enums.letters import LetterType

LETTER_TYPE_GROUPS = {
    LetterType.Type1: [
        ["A", "B", "C"],
        ["D", "E", "F"],
        ["G", "H", "I"],
        ["J", "K", "L"],
        ["M", "N", "O"],
        ["P", "Q", "R"],
        ["S", "T", "U", "V"],
    ],
    LetterType.Type2: [["W", "X"], ["Y", "Z"], ["Σ", "Δ"], ["θ", "Ω"]],
    LetterType.Type3: [["W-", "X-"], ["Y-", "Z-"], ["Σ-", "Δ-"], ["θ-", "Ω-"]],
    LetterType.Type4: [["Φ", "Ψ", "Λ"]],
    LetterType.Type5: [["Φ-", "Ψ-", "Λ-"]],
    LetterType.Type6: [["α", "β", "Γ"]],
}


# From codex_mirror_manager.py
import logging
from typing import TYPE_CHECKING
from data.locations import vertical_loc_mirror_map
from data.positions import mirrored_positions

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex.codex_control_widget import (
        CodexControlWidget,
    )


class CodexMirrorManager:
    """Handles mirroring of pictographs in the Codex."""

    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex
        self.vertical_mirror_positions = mirrored_positions["vertical"]

    def mirror_all(self):
        try:
            for letter_str, view in self.codex.section_manager.codex_views.items():
                scene = view.pictograph
                if scene.pictograph_data:
                    scene.updater.update_pictograph(scene.pictograph_data)
                    logger.debug(f"Mirrored pictograph for letter '{letter_str}'.")
        except Exception as e:
            logger.exception(f"Error during mirror_all: {e}")

    def mirror_codex(self):
        """Apply mirroring logic to all pictographs in the Codex."""
        for letter, pictograph in self.codex.data_manager.pictograph_data.items():
            if pictograph:
                self._mirror_pictograph(pictograph)
        self._refresh_pictograph_views()

    def _mirror_pictograph(self, pictograph):
        """Mirror an individual pictograph dictionary."""
        if "start_pos" in pictograph:
            pictograph["start_pos"] = self.vertical_mirror_positions.get(
                pictograph["start_pos"], pictograph["start_pos"]
            )
        if "end_pos" in pictograph:
            pictograph["end_pos"] = self.vertical_mirror_positions.get(
                pictograph["end_pos"], pictograph["end_pos"]
            )

        for color in ["blue_attributes", "red_attributes"]:
            if color in pictograph:
                attributes = pictograph[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = vertical_loc_mirror_map.get(
                        attributes["start_loc"], attributes["start_loc"]
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = vertical_loc_mirror_map.get(
                        attributes["end_loc"], attributes["end_loc"]
                    )
                if "prop_rot_dir" in attributes:
                    attributes["prop_rot_dir"] = self._reverse_prop_rot_dir(
                        attributes["prop_rot_dir"]
                    )

    def _reverse_prop_rot_dir(self, prop_rot_dir):
        """Reverse the rotation direction."""
        return {"cw": "ccw", "ccw": "cw"}.get(prop_rot_dir)

    def _refresh_pictograph_views(self):
        """Refresh all views to reflect the updated pictograph data."""
        for letter, view in self.codex.section_manager.codex_views.items():
            if letter in self.codex.data_manager.pictograph_data:
                pictograph_data = self.codex.data_manager.pictograph_data[letter]
                view.pictograph.updater.update_pictograph(pictograph_data)
                view.scene().update()


# From codex_ori_selector.py
# codex_ori_selector.py

from typing import TYPE_CHECKING
import logging

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QComboBox, QVBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget

logger = logging.getLogger(__name__)


class CodexOriSelector(QWidget):
    """A widget containing a label and combo box for selecting Codex orientation/rotation modes."""

    options = ["in", "clock", "out", "counter"]

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
            for letter_str, view in self.codex.section_manager.codex_views.items():
                scene = view.pictograph
                if scene.pictograph_data:
                    new_dict = scene.pictograph_data.copy()
                    if "blue_attributes" in new_dict:
                        new_dict["blue_attributes"]["start_ori"] = orientation
                    if "red_attributes" in new_dict:
                        new_dict["red_attributes"]["start_ori"] = orientation
                    scene.updater.update_pictograph(new_dict)
                    logger.debug(
                        f"Updated orientation for pictograph '{letter_str}' to '{orientation}'."
                    )
        except Exception as e:
            logger.exception(f"Error during update_orientation_all: {e}")

    def resizeEvent(self, event) -> None:
        """Handles resizing logic, adjusting label and combo box sizes proportionally."""
        super().resizeEvent(event)
        self._resize_combo_box()
        self._resize_start_ori_label()

    def _resize_start_ori_label(self):
        label_font = self.start_ori_label.font()
        label_font.setPointSize(int(self.codex.learn_tab.main_widget.height() * 0.018))
        self.start_ori_label.setFont(label_font)

    def _resize_combo_box(self):
        combo_width = int(self.codex.learn_tab.main_widget.width() * 0.06)
        combo_height = int(self.codex.learn_tab.main_widget.height() * 0.04)

        combo_font = self.combo_box.font()
        combo_font_size = combo_height // 2
        combo_font.setPointSize(combo_font_size)
        combo_font.setBold(True)

        self.combo_box.setFixedHeight((combo_height))
        self.combo_box.setFixedWidth(combo_width)
        self.combo_box.setFont(combo_font)


# From codex_pictograph_view.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.pictograph_view import PictographView

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex.codex import Codex
    from base_widgets.base_pictograph.pictograph import Pictograph


class CodexPictographView(PictographView):
    def __init__(self, pictograph: "Pictograph", codex: "Codex") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.codex = codex
        self.setStyleSheet("border: 1px solid black;")

    def resizeEvent(self, event):
        size = self.codex.learn_tab.main_widget.width() // 16
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)


# From codex_rotation_manager.py
from typing import TYPE_CHECKING
from data.positions_map import positions_map
from data.locations import cw_loc_order

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget


class CodexRotationManager:
    """Handles rotating the codex in 45° increments."""

    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex

    def rotate_codex(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        for letter, pictograph_data in self.codex.data_manager.pictograph_data.items():
            if pictograph_data:
                pictograph_data = self._rotate_pictograph_data(pictograph_data)
                self.codex.data_manager.pictograph_data[letter] = pictograph_data

        for view in self.codex.section_manager.codex_views.values():
            view.pictograph.grid.update_grid_mode()

        self._refresh_pictograph_views()

        QApplication.restoreOverrideCursor()

    def _rotate_pictograph_data(self, pictograph_data: dict) -> dict:
        """Rotate a single pictograph dictionary."""
        for color in ["blue_attributes", "red_attributes"]:
            if color in pictograph_data:
                attributes = pictograph_data[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = self._rotate_location(
                        attributes["start_loc"]
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = self._rotate_location(attributes["end_loc"])

        if "blue_attributes" in pictograph_data and "red_attributes" in pictograph_data:
            bl = pictograph_data["blue_attributes"]
            rl = pictograph_data["red_attributes"]
            if "start_loc" in bl and "start_loc" in rl:
                pictograph_data["start_pos"] = positions_map[
                    (bl["start_loc"], rl["start_loc"])
                ]
            if "end_loc" in bl and "end_loc" in rl:
                pictograph_data["end_pos"] = positions_map[
                    (bl["end_loc"], rl["end_loc"])
                ]
        return pictograph_data

    def _rotate_location(self, location: str) -> str:
        """Rotate a single location by 45° increments."""
        if location not in cw_loc_order:
            return location
        idx = cw_loc_order.index(location)
        new_idx = (idx + 1) % len(cw_loc_order)
        new_loc = cw_loc_order[new_idx]
        return new_loc

    def update_grid_mode(self):
        for view in self.codex.section_manager.codex_views.values():
            grid_mode = self.codex.main_widget.grid_mode_checker.get_grid_mode(
                view.pictograph.pictograph_data
            )
            view.pictograph.grid.hide()
            view.pictograph.grid.__init__(
                view.pictograph, view.pictograph.grid.grid_data, grid_mode
            )

    def _refresh_pictograph_views(self):
        """Refresh all views to reflect the updated pictograph data."""
        for letter, view in self.codex.section_manager.codex_views.items():
            if letter in self.codex.data_manager.pictograph_data:
                pictograph_data = self.codex.data_manager.pictograph_data[letter]
                view.pictograph.arrow_placement_manager.default_positioner.__init__(
                    view.pictograph.arrow_placement_manager
                )
                view.pictograph.updater.update_pictograph(pictograph_data)


# From codex_scroll_area.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

if TYPE_CHECKING:
    from .codex import Codex


class CodexScrollArea(QScrollArea):
    def __init__(self, codex: "Codex") -> None:
        super().__init__(codex)
        self.codex = codex
        self.setWidgetResizable(True)
        self.setStyleSheet("background: transparent;")

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.setWidget(content_widget)


# From codex_section_manager.py
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from Enums.letters import LetterType
from .codex_pictograph_view import CodexPictographView
from .codex_section_type_label import CodexSectionTypeLabel
from base_widgets.base_pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from .codex import Codex


class CodexSectionManager:
    """Manages the loading and organization of pictograph sections in the Codex."""

    VERT_SPACING = 7
    HOR_SPACING = 7
    ROWS = [
        ["A", "B", "C", "D", "E", "F"],
        ["G", "H", "I", "J", "K", "L"],
        ["M", "N", "O", "P", "Q", "R"],
        ["S", "T", "U", "V"],
        ["W", "X", "Y", "Z"],
        ["Σ", "Δ", "θ", "Ω"],
        ["W-", "X-", "Y-", "Z-"],
        ["Σ-", "Δ-", "θ-", "Ω-"],
        ["Φ", "Ψ", "Λ"],
        ["Φ-", "Ψ-", "Λ-"],
        ["α", "β", "Γ"],
    ]

    def __init__(self, codex: "Codex"):
        self.codex = codex
        self.scroll_area = self.codex.scroll_area
        self.content_layout = self.scroll_area.content_layout
        self.codex_views: dict[str, "CodexPictographView"] = {}
        self.setup_sections()

    def setup_sections(self) -> None:
        for letter_type in LetterType:
            self._load_letter_type_section(letter_type)

    def _load_letter_type_section(self, letter_type: LetterType) -> None:
        type_label = CodexSectionTypeLabel(self.codex, letter_type)
        self._add_type_label(type_label)

        letters = letter_type.letters
        if not letters:
            return

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(self.VERT_SPACING)
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        for _, row_letters in enumerate(self.ROWS):
            current_letters = [l for l in row_letters if l in letters]
            if not current_letters:
                continue

            row_layout = self._create_row_layout(current_letters)
            vertical_layout.addLayout(row_layout)

        self.content_layout.addLayout(vertical_layout)

    def _add_type_label(self, type_label: CodexSectionTypeLabel) -> None:
        self.content_layout.addSpacing(self.VERT_SPACING)
        self.content_layout.addWidget(
            type_label, alignment=Qt.AlignmentFlag.AlignHCenter
        )

        self.content_layout.addSpacing(self.VERT_SPACING)

    def _create_row_layout(self, row_letters: list[str]) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(self.HOR_SPACING)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        for letter_str in row_letters:
            self._add_pictograph_view(letter_str, layout)

        return layout

    def _add_pictograph_view(self, letter_str: str, layout: QHBoxLayout) -> None:
        p_dict = self.codex.data_manager.pictograph_data.get(letter_str)
        if p_dict is None:
            return

        if letter_str not in self.codex_views:
            pictograph = Pictograph(self.codex.main_widget)
            view = CodexPictographView(pictograph, self.codex)
            pictograph.updater.update_pictograph(p_dict)
            self.codex_views[letter_str] = view
        else:
            view = self.codex_views[letter_str]

        layout.addWidget(view)


# From codex_section_type_label.py
# section_type_label.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from Enums.letters import LetterType
from utilities.letter_type_text_painter import (
    LetterTypeTextPainter,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex.codex import Codex


class CodexSectionTypeLabel(QLabel):
    def __init__(self, codex: "Codex", letter_type: LetterType) -> None:
        super().__init__()
        self.codex = codex
        self.letter_type = letter_type
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_styled_text(letter_type)

    def set_styled_text(self, letter_type: LetterType) -> None:
        styled_description = LetterTypeTextPainter.get_colored_text(
            letter_type.description
        )
        type_name = "".join(
            [i if not i.isdigit() else f" {i}" for i in letter_type.name]
        )
        self.setText(f"{type_name}: {styled_description}")

    def get_font_size(self):
        return max(12, self.codex.main_widget.height() // 45)

    def resizeEvent(self, event):
        self.label_height = self.get_font_size() * 2
        self.setFixedHeight(self.label_height)
        # self.setFixedWidth(self.fontMetrics().horizontalAdvance(self.text()))
        border_style = "2px solid black"
        self.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  border-radius: {self.label_height // 2}px;"
            f"  font-size: {self.get_font_size()}px;"
            f"  font-weight: bold;"
            f"  border: {border_style};"
            f"  padding: 0 10px;"
            f"}}"
        )


# From codex_toggle_button.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex.codex import Codex


class CodexToggleButton(QPushButton):
    """A button dedicated to toggling the Codex open/closed."""

    def __init__(self, codex: "Codex"):
        """Initializes the toggle button with a reference to the parent Codex."""
        super().__init__("Codex", codex)
        self.codex = codex
        self.learn_widget = codex.learn_tab
        self.codex_shown = True
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.toggle_codex)

    def toggle_codex(self) -> None:
        """Toggles the visibility of the codex with an animation."""
        self.codex_shown = not self.codex_shown
        self.codex.animation_manager.animate(self.codex_shown)

    def resizeEvent(self, event) -> None:
        """Adjusts the toggle button size based on the Codex's parent widget dimensions."""
        if self.learn_widget is not None:
            button_height = self.learn_widget.main_widget.height() // 30
            button_width = self.learn_widget.main_widget.width() // 14
            self.setFixedHeight(button_height)
            self.setFixedWidth(button_width)

        font = self.font()
        font.setBold(True)
        font_size = self.learn_widget.main_widget.height() // 60
        font.setPointSize(font_size)
        self.setFont(font)
        super().resizeEvent(event)


# From concatenated_classes.py
