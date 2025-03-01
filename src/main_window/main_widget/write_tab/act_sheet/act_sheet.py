from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.write_tab.act_sheet.act_loader import ActLoader
from settings_manager.global_settings.app_context import AppContext
from .act_header.act_header import ActHeader
from .act_splitter.act_container import ActContainer
from .act_saver import ActSaver
from .sequence_collector import SequenceCollector

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


class ActSheet(QWidget):
    DEFAULT_ROWS = 24
    DEFAULT_COLUMNS = 8

    def __init__(self, write_tab: "WriteTab") -> None:
        super().__init__(write_tab)
        self.write_tab = write_tab
        self.settings = AppContext.settings_manager().write_tab_settings
        self.act_header = ActHeader(self)
        self.act_container = ActContainer(self)
        self.setAcceptDrops(False)

        self.act_saver = ActSaver(self)
        self.act_loader = ActLoader(self)
        self.sequence_collector = SequenceCollector(self)

        self._setup_layout()
        self.act_container.connect_scroll_sync()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.act_header, 1)
        layout.addWidget(self.act_container, 10)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def closeEvent(self, event):
        self.act_container.save_scrollbar_state()
        super().closeEvent(event)

    def showEvent(self, event):
        self.act_container.restore_scrollbar_state()
        super().showEvent(event)
