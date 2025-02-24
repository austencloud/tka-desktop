from PyQt6.QtWidgets import QPushButton


class BaseRotDirButton(QPushButton):
    def __init__(self, direction) -> None:
        super().__init__()
