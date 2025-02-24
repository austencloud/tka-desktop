from typing import TYPE_CHECKING
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QPainter, QPixmap, QColor, QLinearGradient
from PyQt6.QtWidgets import QWidget

from .snowflake_worker import SnowflakeWorker
from .shooting_star_manager import ShootingStarManager
from .santa_manager import SantaManager

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SnowfallBackground(QWidget):
    snowflake_count = 100
    update_required = pyqtSignal()  # Signal for requesting an update

    def __init__(self, main_widget: "MainWidget" = None):
        super().__init__(main_widget)
        self.main_widget = main_widget

        # Dimensions and properties
        self.widget_width = self.main_widget.width()
        self.widget_height = self.main_widget.height()
        self.setFixedSize(self.widget_width, self.widget_height)
        self.setAutoFillBackground(True)

        # Snowflake properties
        self.snowflake_images = [
            QPixmap(f"images/snowflakes/snowflake{i}.png") for i in range(1, 21)
        ]
        self.snowflakes = []

        # Worker thread setup
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

        # Animation timer
        # self.animation_timer = QTimer()
        # self.animation_timer.timeout.connect(self.update)
        # self.animation_timer.timeout.connect(self.animate_background)

        # Additional managers
        self.shooting_star_manager = ShootingStarManager()
        self.santa_manager = SantaManager()

    # def start_animation(self):
    #     """Start the background animation."""
    #     self.worker.running = True
    #     self.worker_thread.start()
    #     self.animation_timer.start(16)  # Approximately 60 FPS

    # def stop_animation(self):
    #     """Stop the background animation."""
    #     self.worker.running = False
    #     self.worker_thread.quit()
    #     self.worker_thread.wait()
    #     self.animation_timer.stop()

    # def closeEvent(self, event):
    #     """Stop the worker thread and timer when the widget is closed."""
    #     self.stop_animation()
    #     super().closeEvent(event)

    def paint_background(self, parent_widget: QWidget, painter: QPainter):
        # Ensure gradient, snowflakes, Santa, and shooting stars are all drawn
        gradient = QLinearGradient(0, 0, 0, self.widget_height)
        gradient.setColorAt(0, QColor(20, 30, 48))  # Dark blue
        gradient.setColorAt(1, QColor(50, 80, 120))  # Light blue
        painter.fillRect(self.main_widget.rect(), gradient)

        # # Draw Snowflakes
        # for snowflake in self.snowflakes:
        #     x, y, image_index = snowflake["x"], snowflake["y"], snowflake["image_index"]
        #     pixmap = self.snowflake_images[image_index]
        #     painter.drawPixmap(int(x), int(y), pixmap)

        # # Draw Shooting Stars and Santa
        # self.shooting_star_manager.draw_shooting_star(painter, parent_widget)
        # self.santa_manager.draw_santa(painter, parent_widget)

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

    # def _on_animation_tick(self):
    #     self.animate_background()  # Animate Santa and shooting stars
    #     self.update()  # Trigger repaint
