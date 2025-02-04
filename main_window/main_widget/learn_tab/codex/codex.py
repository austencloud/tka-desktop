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
