from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal

from styles.styled_button import StyledButton, ButtonContext


if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class MenuBarNavWidget(QWidget):
    tab_changed = pyqtSignal(int)

    def __init__(self, menu_bar: "MenuBarWidget"):
        super().__init__(menu_bar)
        self.mw = menu_bar.main_widget

        self.tab_buttons: list[StyledButton] = []
        self.tab_names = [
            "Construct ⚒️",
            "Generate 🤖",
            "Browse 🔍",
            "Learn 🧠",
            "Sequence Card 📋",
        ]

        self.current_index = 0

        self.container_frame = QFrame(self)
        self.container_layout = QVBoxLayout(self.container_frame)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        self.tab_layout = QHBoxLayout()
        self.tab_layout.addStretch()  # Add stretch before the buttons

        for index, name in enumerate(self.tab_names):
            button = StyledButton(name, context=ButtonContext.NAVIGATION)
            button.clicked.connect(lambda _, idx=index: self.set_active_tab(idx))
            self.tab_buttons.append(button)
            self.tab_layout.addWidget(button)

        self.tab_layout.addStretch()  # Add stretch after the buttons

        self.container_layout.addLayout(self.tab_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.container_frame)

        def on_tab_changed_handler(index):

            # Create a direct mapping from button index to tab names
            tab_mapping = {
                0: "construct",
                1: "generate",
                2: "browse",
                3: "learn",
                4: "sequence_card",
            }

            if index in tab_mapping:
                tab_name = tab_mapping[index]
                # Always use the new coordinator interface - no fallback to old tab switcher
                if hasattr(self.mw, "switch_to_tab"):
                    print(f"DEBUG: Using new TabManager to switch to {tab_name}")
                    self.mw.switch_to_tab(tab_name)
                else:
                    print(
                        f"DEBUG: ERROR - MainWidget does not have switch_to_tab method!"
                    )
                    print(f"DEBUG: MainWidget type: {type(self.mw).__name__}")
                    print(
                        f"DEBUG: MainWidget attributes: {[attr for attr in dir(self.mw) if not attr.startswith('_')]}"
                    )
            else:
                print(f"DEBUG: ERROR - index {index} not found in tab_mapping")

        self.tab_changed.connect(on_tab_changed_handler)

        self.set_active_tab(self.current_index)

    def set_active_tab(self, index: int):
        if index == self.current_index:
            return  # No need to reapply the same state

        self.current_index = index
        self.update_buttons()
        self.tab_changed.emit(index)

    def update_buttons(self):
        """Update button styles and resize based on main widget width with improved readability."""
        # Improved font sizing for better readability
        font_size = max(10, min(16, self.mw.width() // 80))  # Better scaling ratio
        font = QFont("Segoe UI", font_size, QFont.Weight.Medium)

        # Better button proportions for text readability
        button_width = max(120, self.mw.width() // 7)  # Minimum width for text
        button_height = max(35, int(font_size * 2.5))  # Height based on font size

        for idx, button in enumerate(self.tab_buttons):
            is_active = idx == self.current_index
            button.set_selected(is_active)
            button.setFont(font)
            button.update_appearance()
            button.setFixedWidth(button_width)
            button.setFixedHeight(button_height)

    def on_tab_changed_programmatically(self, tab_name: str):
        """Handle tab changes that occur programmatically (not from button clicks)."""
        # Map tab names to button indices
        tab_name_to_index = {
            "construct": 0,
            "generate": 1,
            "browse": 2,
            "learn": 3,
            "sequence_card": 4,
        }

        if tab_name in tab_name_to_index:
            new_index = tab_name_to_index[tab_name]
            if new_index != self.current_index:
                # Update the current index without emitting the signal (to avoid circular calls)
                self.current_index = new_index
                self.update_buttons()
                print(
                    f"DEBUG: Navigation updated to highlight {tab_name} tab (index {new_index})"
                )
        else:
            print(f"DEBUG: Unknown tab name for navigation update: {tab_name}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_buttons()
        self.tab_layout.setSpacing(self.mw.width() // 100)
