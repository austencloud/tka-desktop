from PyQt6.QtCore import QObject, pyqtSignal
import random
import time


class SnowflakeWorker(QObject):
    update_snowflakes = pyqtSignal(list)

    def __init__(self, snowflake_count, width, height, image_count):
        super().__init__()
        self.snowflake_count = snowflake_count
        self.width = width
        self.height = height
        self.image_count = image_count
        self.snowflakes = []
        self.running = False
        self._initialize_snowflakes()

    def _initialize_snowflakes(self):
        """Initialize snowflake positions and properties."""
        self.snowflakes = [
            {
                "x": random.randint(0, self.width),
                "y": random.randint(-self.height, 0),
                "size": random.randint(2, 6),
                "speed": random.uniform(0.5, 2.0),
                "image_index": random.randint(0, self.image_count - 1),
            }
            for _ in range(self.snowflake_count)
        ]

    def start(self):
        """Start the worker loop."""
        self.running = True
        self.process()

    def stop(self):
        """Stop the worker loop."""
        self.running = False

    def process(self):
        """Main loop for updating snowflakes."""
        while self.running:
            self._update_snowflakes()
            self.update_snowflakes.emit(self.snowflakes)
            time.sleep(0.016)  # Yield CPU (approximately 60 FPS)

    def _update_snowflakes(self):
        """Update snowflake positions and reset out-of-bounds snowflakes."""
        for snowflake in self.snowflakes:
            snowflake["y"] += snowflake["speed"]
            if snowflake["y"] > self.height:
                snowflake["y"] = random.randint(-20, 0)
                snowflake["x"] = random.randint(0, self.width)
                snowflake["size"] = random.randint(2, 6)
                snowflake["speed"] = random.uniform(0.5, 2.0)
                snowflake["image_index"] = random.randint(0, self.image_count - 1)

    def update_bounds(self, width, height):
        """Update the worker's bounds for snowflake generation."""
        self.width = width
        self.height = height
        self._initialize_snowflakes()
