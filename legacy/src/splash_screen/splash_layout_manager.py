from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .splash_screen import SplashScreen


class SplashLayoutManager:
    """Handles the layout of the splash screen components."""

    def __init__(self, splash_screen: "SplashScreen"):
        self.splash_screen = splash_screen
        self._setup_layout()

    def _setup_layout(self):
        layout = QVBoxLayout(self.splash_screen)

        top_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addStretch(1)
        left_layout.addWidget(self.splash_screen.title_label)
        left_layout.addStretch(1)
        left_layout.addWidget(self.splash_screen.created_by_label)
        left_layout.addStretch(1)
        left_layout.addWidget(self.splash_screen.currently_loading_label)
        left_layout.addStretch(1)

        top_layout.addLayout(left_layout)
        top_layout.addWidget(
            self.splash_screen.logo_label, alignment=Qt.AlignmentFlag.AlignRight
        )

        layout.addLayout(top_layout)
        layout.addSpacerItem(
            QSpacerItem(
                20,
                self.splash_screen.height() // 10,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        )

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.splash_screen.progress_bar)
        layout.addLayout(bottom_layout)
