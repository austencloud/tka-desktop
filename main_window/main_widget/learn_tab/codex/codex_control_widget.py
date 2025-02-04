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

