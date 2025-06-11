from typing import TYPE_CHECKING
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QPainter, QPixmap, QColor, QLinearGradient
from PyQt6.QtWidgets import QWidget

from utils.path_helpers import get_image_path

from .snowflake_worker import SnowflakeWorker
from .shooting_star_manager import ShootingStarManager
from .santa_manager import SantaManager

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SnowfallBackground(QWidget):
    snowflake_count = 100
    update_required = pyqtSignal()

    def __init__(self, main_widget: "MainWidget" = None):
        super().__init__(main_widget)
        self.main_widget = main_widget

        self.widget_width = self.main_widget.width()
        self.widget_height = self.main_widget.height()
        self.setFixedSize(self.widget_width, self.widget_height)
        self.setAutoFillBackground(True)

        self.snowflake_images = [
            QPixmap(get_image_path(f"snowflakes/snowflake{i}.png"))
            for i in range(1, 21)
        ]
        self.snowflakes = []

        self.worker_thread = QThread()
        self.worker = SnowflakeWorker(
            self.snowflake_count,
            self.widget_width,
            self.widget_height,
            len(self.snowflake_images),
        )
        self.worker.moveToThread(self.worker_thread)
        self.worker.update_snowflakes.connect(self._update_snowflakes_from_worker)
        self.worker_thread.started.connect(self.worker.process)

        self.shooting_star_manager = ShootingStarManager()
        self.santa_manager = SantaManager()

    def paint_background(self, parent_widget: QWidget, painter: QPainter):

        gradient = QLinearGradient(0, 0, 0, self.widget_height)
        gradient.setColorAt(0, QColor(20, 30, 48))
        gradient.setColorAt(1, QColor(50, 80, 120))
        painter.fillRect(self.main_widget.rect(), gradient)

    @pyqtSlot(list)
    def _update_snowflakes_from_worker(self, snowflakes):
        """Slot to receive updated snowflake positions from the worker."""
        self.snowflakes = snowflakes
        self.update_required.emit()

    def animate_background(self):
        """Animate additional background effects."""
        self.shooting_star_manager.animate_shooting_star()
        self.shooting_star_manager.manage_shooting_star(self)
        self.santa_manager.animate_santa()

    def resizeEvent(self, event):
        """Handle resizing of the widget and update worker bounds."""

        def update_bounds():
            self.widget_width = self.main_widget.width()
            self.widget_height = self.main_widget.height()

            self.worker.update_bounds(self.widget_width, self.widget_height)

        QTimer.singleShot(0, update_bounds)
        super().resizeEvent(event)
