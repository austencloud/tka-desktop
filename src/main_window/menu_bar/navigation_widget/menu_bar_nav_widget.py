from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal

from main_window.main_widget.tab_index import TAB_INDEX
from styles.base_styled_button import BaseStyledButton


if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class MenuBarNavWidget(QWidget):
    tab_changed = pyqtSignal(int)

    def __init__(self, menu_bar: "MenuBarWidget"):
        super().__init__(menu_bar)
        self.mw = menu_bar.main_widget

        self.tab_buttons: list[BaseStyledButton] = []
        self.tab_names = ["Construct ⚒️", "Generate 🤖", "Browse 🔍", "Learn 🧠"]

        self.current_index = 0

        self.container_frame = QFrame(self)
        self.container_layout = QVBoxLayout(self.container_frame)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        self.tab_layout = QHBoxLayout()
        self.tab_layout.addStretch()  # Add stretch before the buttons

        for index, name in enumerate(self.tab_names):
            button = BaseStyledButton(name)
            button.clicked.connect(lambda _, idx=index: self.set_active_tab(idx))
            self.tab_buttons.append(button)
            self.tab_layout.addWidget(button)

        self.tab_layout.addStretch()  # Add stretch after the buttons

        self.container_layout.addLayout(self.tab_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.container_frame)

        self.tab_changed.connect(
            lambda: self.mw.tab_switcher.on_tab_changed(
                list(TAB_INDEX.keys())[self.current_index]
            )
        )

        self.set_active_tab(self.current_index)

    def set_active_tab(self, index: int):
        if index == self.current_index:
            return  # No need to reapply the same state

        self.current_index = index
        self.update_buttons()
        self.tab_changed.emit(index)

    def update_buttons(self):
        """Update button styles and resize based on main widget width."""
        font_size = self.mw.width() // 130
        font = QFont("Georgia", self.mw.width() // 100)

        button_width = self.mw.width() // 8
        button_height = int(button_width * 0.2)

        for idx, button in enumerate(self.tab_buttons):
            is_active = idx == self.current_index
            button.set_selected(is_active)
            button.setFont(font)
            button.update_appearance()
            button.setFixedWidth(button_width)
            button.setFixedHeight(button_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_buttons()
        self.tab_layout.setSpacing(self.mw.width() // 100)
