from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .initial_filter_choice_widget import InitialFilterChoiceWidget


class FilterButton(QPushButton):
    def __init__(self, label: str):
        super().__init__(label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._radius = 0
        self._default_stylesheet = """
            QPushButton {
                border: 2px solid black;
            }
            QPushButton:hover {
                background-color: lightgray; 
            }
        """
        self.setStyleSheet(self._default_stylesheet)

    def _update_style(self, background_color: str = "lightgray", shadow: bool = False):
        shadow_effect = (
            """
            box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.2);
        """
            if shadow
            else ""
        )

        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {background_color};
                border: 2px solid black;
                color: black;
                padding: 5px;
                border-radius: {self._radius}px;
                {shadow_effect}
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(200, 200, 200, 1),
                    stop:1 rgba(150, 150, 150, 1)
                );
            }}
            QPushButton:pressed {{
                background-color: #d0d0d0;
            }}
        """
        )

    def enterEvent(self, event):
        self._update_style(background_color="lightgray", shadow=True)

    def leaveEvent(self, event):
        self._update_style(background_color="lightgray", shadow=False)

    def set_rounded_button_style(self, radius: int):
        self._radius = radius
        self._update_style()

    def mousePressEvent(self, event):
        self._update_style(background_color="#aaaaaa")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._update_style(background_color="lightgray")
        super().mouseReleaseEvent(event)


class FilterButtonGroup(QWidget):
    """A group consisting of a button and its description label."""

    def __init__(
        self,
        label: str,
        description: str,
        handler: callable,
        filter_choice_widget: "InitialFilterChoiceWidget",
    ):
        super().__init__()
        self.main_widget = filter_choice_widget.main_widget
        self.settings_manager = self.main_widget.settings_manager

        self.button = FilterButton(label)
        self.button.clicked.connect(handler)

        self.description_label = QLabel(description)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def resizeEvent(self, event: QResizeEvent) -> None:
        button_font = QFont()
        button_font.setPointSize(self.main_widget.width() // 80)

        button_width = self.main_widget.width() // 7
        button_height = self.main_widget.height() // 10
        border_radius = min(button_width, button_height) // 4

        self.button.setFixedSize(button_width, button_height)
        self.button.setFont(button_font)
        self.button.set_rounded_button_style(border_radius)

        font_size = self.main_widget.width() // 150
        color = self.settings_manager.global_settings.get_current_font_color()
        self.description_label.setStyleSheet(
            f"font-size: {font_size}px; color: {color};"
        )

        super().resizeEvent(event)
