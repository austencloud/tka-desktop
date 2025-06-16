from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text: str):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class BaseSelector(QWidget):
    def __init__(self, menu_bar: "MenuBarWidget", widget: QWidget):
        super().__init__()
        self.menu_bar = menu_bar
        self.main_widget = menu_bar.main_widget
        self.widget = widget

        # Set up layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.widget)
        self.setLayout(layout)

    def style_widget(self):
        font_size = self.menu_bar.selectors_widget.selector_font_size
        font = QFont("Georgia", font_size)
        self.widget.setFont(font)

        style_sheet = """
            border: 1px solid black;
            padding: 4px;
            background-color: white;
            border-radius: 5px;
        """

        hover_style = """
            background-color: #F0F0F0;
        """

        # Set the cursor to pointing hand
        self.widget.setCursor(Qt.CursorShape.PointingHandCursor)

        if isinstance(self.widget, ClickableLabel):
            self.widget.setStyleSheet(
                f"""
                QLabel {{
                    {style_sheet}
                }}
                QLabel:hover {{
                    {hover_style}
                }}
                """
            )
        elif isinstance(self.widget, QPushButton):
            self.widget.setStyleSheet(
                f"""
                QPushButton {{
                    {style_sheet}
                }}
                QPushButton:hover {{
                    {hover_style}
                }}
                """
            )


class LabelSelector(BaseSelector):
    def __init__(self, menu_bar: "MenuBarWidget", label_text: str):
        self.label = ClickableLabel(label_text)
        self.label.clicked.connect(self.on_label_clicked)
        super().__init__(menu_bar, self.label)

    def on_label_clicked(self):
        """To be implemented by subclasses."""

    def set_display_text(self, text: str):
        self.label.setText(text)


class ButtonSelector(BaseSelector):
    def __init__(self, menu_bar: "MenuBarWidget", button_text: str):
        self.button = QPushButton(button_text)
        self.button.clicked.connect(self.on_button_clicked)
        super().__init__(menu_bar, self.button)

    def on_button_clicked(self):
        """To be implemented by subclasses."""
