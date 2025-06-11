import random
from PyQt6.QtCore import Qt, QTimer, QThreadPool
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from main_window.main_widget.main_background_widget.backgrounds.snowfall.new.snowflake import (
    Snowflake,
)
from main_window.main_widget.main_background_widget.backgrounds.snowfall.new.snowflake_config_manager import (
    SnowflakeConfigManager,
)
from main_window.main_widget.main_background_widget.backgrounds.snowfall.new.snowflake_update_task import (
    SnowflakeUpdateTask,
)


class SnowflakeRenderer(QOpenGLWidget):
    def __init__(self, config_path):
        super().__init__()
        self.config_manager = SnowflakeConfigManager(config_path)
        self.config_manager.config_updated.connect(self.on_config_updated)

        self.snowflakes: list[Snowflake] = []
        self.thread_pool = QThreadPool.globalInstance()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_snowflakes)
        self.timer.start(16)

        self.cached_snowflakes = self._generate_snowflake_pixmaps()
        self._initialize_snowflakes()

    def _generate_snowflake_pixmaps(self):
        sizes = [10, 15, 20]
        types = ["star", "spiky"]
        cached = {}

        for snowflake_type in types:
            cached[snowflake_type] = {}
            for size in sizes:
                pixmap = QPixmap(size, size)
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                if snowflake_type == "star":
                    self._draw_star(painter, size)
                elif snowflake_type == "spiky":
                    self._draw_spiky(painter, size)
                painter.end()
                cached[snowflake_type][size] = pixmap

        return cached

    def _draw_star(self, painter: QPainter, size):
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawEllipse(size // 4, size // 4, size // 2, size // 2)

    def _draw_spiky(self, painter: QPainter, size):
        painter.setPen(Qt.GlobalColor.white)
        painter.drawLine(0, size // 2, size, size // 2)
        painter.drawLine(size // 2, 0, size // 2, size)

    def _initialize_snowflakes(self):
        for _ in range(100):
            x = random.randint(0, self.width())
            y = random.randint(-self.height(), 0)
            speed = random.uniform(1, 3)
            snowflake_type = random.choice(["star", "spiky"])
            size = random.choice([10, 15, 20])
            pixmap = self.cached_snowflakes[snowflake_type][size]
            self.snowflakes.append(Snowflake(x, y, speed, pixmap))

    def on_config_updated(self, config):
        # Example: Adjust snowflake count dynamically
        if "snowflake_count" in config:
            current_count = len(self.snowflakes)
            target_count = config["snowflake_count"]

            if target_count > current_count:
                for _ in range(target_count - current_count):
                    self._initialize_snowflakes()
            elif target_count < current_count:
                self.snowflakes = self.snowflakes[:target_count]

    def update_snowflakes(self):
        task = SnowflakeUpdateTask(self.snowflakes)
        self.thread_pool.start(task)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for snowflake in self.snowflakes:
            if snowflake.y > self.height():
                snowflake.y = -snowflake.pixmap.height()
                snowflake.x = random.randint(0, self.width())
            painter.drawPixmap(snowflake.x, snowflake.y, snowflake.pixmap)
        painter.end()
