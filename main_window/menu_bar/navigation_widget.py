# navigation_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFrame, QVBoxLayout
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal


if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class NavigationWidget(QWidget):
    tab_changed = pyqtSignal(int)

    def __init__(self, menu_bar: "MenuBarWidget"):
        super().__init__(menu_bar)
        self.mw = menu_bar.main_widget

        self.container_frame = QFrame(self)
        self.container_layout = QVBoxLayout(self.container_frame)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        self.tab_buttons: dict[str, QPushButton] = {}
        self.tab_layout = QHBoxLayout()
        self.tab_layout.addStretch(1)
        self.tab_names = [
            "Construct ⚒️",
            "Generate 🤖",
            "Browse 🔍",
            "Learn 🧠",
            # "Write ✍️",
        ]
        self.current_index = 0
        for index, name in enumerate(self.tab_names):
            button = QPushButton(name)
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.clicked.connect(lambda _, idx=index: self.on_button_clicked(idx))
            self.tab_buttons[name] = button
            self.tab_layout.addWidget(button)
        self.tab_layout.addStretch(1)

        self.container_layout.addLayout(self.tab_layout)

        self.tab_changed.connect(
            lambda: self.mw.tab_switcher.on_tab_changed(self.current_index)
        )
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.container_frame)

        self.set_active_tab(self.current_index)

    def on_button_clicked(self, index):
        self.set_active_tab(index)
        self.tab_changed.emit(index)

    def set_active_tab(self, index):
        self.current_index = index
        for idx, button in enumerate(self.tab_buttons.values()):
            self.set_button_appearance(index, idx, button)

    def set_button_appearance(self, active_index, idx, button: "QPushButton"):
        font_size = self.mw.width() // 120
        if idx == active_index:
            button.setStyleSheet(
                f"background-color: lightblue; font-size: {font_size}pt; font-family: Georgia;"
            )
        else:
            button.setStyleSheet(f"font-size: {font_size}pt; font-family: Georgia;")
        button.setFixedWidth(self.mw.width() // 10)
        button.setFixedHeight(self.mw.height() // 22)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for idx, button in enumerate(self.tab_buttons.values()):
            self.set_button_appearance(self.current_index, idx, button)
