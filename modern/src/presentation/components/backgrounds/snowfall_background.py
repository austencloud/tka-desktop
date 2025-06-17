from typing import TYPE_CHECKING
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer, Qt
from PyQt6.QtGui import QPainter, QPixmap, QColor, QLinearGradient
from PyQt6.QtWidgets import QWidget

from .base_background import BaseBackground
from .asset_utils import get_image_path

from .snowfall.snowflake_worker import SnowflakeWorker
from .snowfall.shooting_star_manager import ShootingStarManager
from .snowfall.santa_manager import SantaManager

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget as ParentWidget


class SnowfallBackground(BaseBackground):
    snowflake_count = 100

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent

        self.widget_width = 800  # Default width
        self.widget_height = 600  # Default height

        if parent:
            self.widget_width = parent.width()
            self.widget_height = parent.height()

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
        self.worker_thread.started.connect(
            self.worker.start
        )  # Call start() instead of process()

        self.shooting_star_manager = ShootingStarManager()
        self.santa_manager = SantaManager()

        # Start the worker thread
        self.worker_thread.start()

    def paint_background(self, widget: QWidget, painter: QPainter):
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor(20, 30, 48))
        gradient.setColorAt(1, QColor(50, 80, 120))
        painter.fillRect(widget.rect(), gradient)

        # Draw snowflakes
        for snowflake in self.snowflakes:
            if 0 <= snowflake["image_index"] < len(self.snowflake_images):
                image = self.snowflake_images[snowflake["image_index"]]
                size = snowflake["size"]
                scaled_image = image.scaled(
                    size,
                    size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                painter.drawPixmap(
                    int(snowflake["x"]), int(snowflake["y"]), scaled_image
                )

        # Draw shooting stars and Santa
        self.shooting_star_manager.draw_shooting_star(painter, widget)
        if self.santa_manager.santa["active"]:
            self.santa_manager.draw_santa(painter, widget)

    @pyqtSlot(list)
    def _update_snowflakes_from_worker(self, snowflakes):
        """Slot to receive updated snowflake positions from the worker."""
        self.snowflakes = snowflakes
        self.update_required.emit()

    def animate_background(self):
        """Animate additional background effects."""
        self.shooting_star_manager.animate_shooting_star()
        self.shooting_star_manager.manage_shooting_star(self.parent_widget or self)
        self.santa_manager.animate_santa()
        self.update_required.emit()

    def update_bounds(self, width, height):
        """Handle resizing of the widget and update worker bounds."""
        self.widget_width = width
        self.widget_height = height
        if hasattr(self, "worker"):
            self.worker.update_bounds(width, height)

    def cleanup(self):
        """Clean up the worker thread when background is destroyed."""
        if hasattr(self, "worker"):
            self.worker.stop()
        if hasattr(self, "worker_thread"):
            self.worker_thread.quit()
            self.worker_thread.wait(1000)  # Wait up to 1 second for thread to finish
