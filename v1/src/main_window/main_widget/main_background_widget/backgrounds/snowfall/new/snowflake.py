from PyQt6.QtGui import QPixmap


class Snowflake:
    def __init__(self, x, y, speed, pixmap):
        self.x = x
        self.y = y
        self.speed = speed
        self.pixmap: QPixmap = pixmap

    def update_position(self):
        self.y += self.speed
