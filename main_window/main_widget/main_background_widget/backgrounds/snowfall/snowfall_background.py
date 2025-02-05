from typing import TYPE_CHECKING, Union
from PyQt6.QtGui import QColor, QPainter, QLinearGradient
from PyQt6.QtWidgets import QWidget
from main_window.main_widget.main_background_widget.backgrounds.base_background import BaseBackground
if TYPE_CHECKING:

    from main_window.main_widget.browse_tab.browse_tab import (
        BrowseTab,
    )
    from main_window.main_widget.learn_tab.learn_tab import LearnTab
    from main_window.main_widget.write_tab.write_tab import WriteTab

from .snowflake_manager import SnowflakeManager
from .santa_manager import SantaManager
from .shooting_star_manager import ShootingStarManager


class SnowfallBackground(BaseBackground):
    def __init__(
        self,
        widget: Union["BrowseTab", "LearnTab", "WriteTab"],
    ):
        super().__init__(widget)
        self.widget = widget

        # self.snowflake_manager = SnowflakeManager()
        # self.santa_manager = SantaManager()
        # self.shooting_star_manager = ShootingStarManager()

    # def animate_background(self):
    #     self.snowflake_manager.animate_snowflakes()
    #     self.santa_manager.animate_santa()
    #     self.shooting_star_manager.animate_shooting_star()
    #     self.shooting_star_manager.manage_shooting_star(self.widget)

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor("#0b1d2a"))
        gradient.setColorAt(0.3, QColor("#142030"))
        gradient.setColorAt(0.7, QColor("#325078"))
        gradient.setColorAt(1, QColor("#49708a"))
        painter.fillRect(widget.rect(), gradient)

        # self.snowflake_manager.draw_snowflakes(painter, widget)
        # if self.santa_manager.santa["active"]:
        #     self.santa_manager.draw_santa(painter, widget)

        # self.shooting_star_manager.draw_shooting_star(painter, widget)
