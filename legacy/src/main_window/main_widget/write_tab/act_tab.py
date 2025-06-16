from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from .act_browser.act_browser import ActBrowser
from .act_sheet.act_sheet import ActSheet

if TYPE_CHECKING:
    from ..main_widget import MainWidget


class WriteTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        self.act_sheet = ActSheet(self)
        self.act_browser = ActBrowser(self)
        self.setAcceptDrops(False)

        self._setup_layout()
        self.act_sheet.act_loader.load_act()

    def _setup_layout(self):
        layout = QHBoxLayout(self)
        layout.addWidget(self.act_sheet, 5)
        layout.addWidget(self.act_browser, 4)
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_act_tab()

    def resize_act_tab(self):
        self.act_sheet.resize_act_sheet()
        self.act_browser.resize_browser()

    def showEvent(self, event):
        self.act_sheet.resize_act_sheet()
        super().showEvent(event)
