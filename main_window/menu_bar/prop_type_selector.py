# prop_type_selector.py

from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from PyQt6.QtWidgets import QWidget, QLabel, QDialog, QPushButton, QVBoxLayout
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


class PropTypeSelector(QWidget):
    def __init__(self, menu_bar: "MenuBarWidget"):
        super().__init__()
        self.menu_bar = menu_bar
        self.main_widget = menu_bar.main_widget
        self.settings_manager = self.main_widget.settings_manager
        self.prop_type_changer = self.settings_manager.global_settings.prop_type_changer

        current_prop_type = self.settings_manager.global_settings.get_prop_type().name

        self.label = ClickableLabel(current_prop_type)
        self.label.clicked.connect(self.on_label_clicked)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def style_widget(self):
        font_size = self.menu_bar.selectors_widget.selector_font_size
        font = QFont("Georgia", font_size)
        self.label.setFont(font)

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
        self.label.setCursor(Qt.CursorShape.PointingHandCursor)

        self.label.setStyleSheet(
            f"""
            QLabel {{
                {style_sheet}
            }}
            QLabel:hover {{
                {hover_style}
            }}
            """
        )

    def on_label_clicked(self):
        self.show_prop_type_dialog()

    def show_prop_type_dialog(self):
        # Create the dialog
        self.dialog = QDialog(self)
        self.dialog.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.dialog.setStyleSheet(
            """
            QDialog {
                border: 2px solid black;
                border-radius: 5px;
                background-color: white;
            }
            QPushButton {
                padding: 5px 10px;
            }
            """
        )

        # Create the layout
        layout = QVBoxLayout(self.dialog)
        layout.setContentsMargins(5, 5, 5, 5)

        # Define prop types
        prop_types = [
            PropType.Hand,
            PropType.Staff,
            PropType.Club,
            PropType.Fan,
            PropType.Triad,
            PropType.Minihoop,
            PropType.Buugeng,
            PropType.Sword,
            PropType.Ukulele,
        ]

        # Create buttons with larger font
        font = QFont()
        font.setPointSize(14)  # Adjust the font size as needed

        for prop_type in prop_types:
            button = QPushButton(prop_type.name)
            button.setFont(font)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda _, pt=prop_type: self.set_current_prop_type(pt)
            )
            layout.addWidget(button)

        self.dialog.setLayout(layout)
        self.dialog.adjustSize()

        # Position the dialog below the label
        global_pos = self.label.mapToGlobal(self.label.rect().bottomLeft())
        self.dialog.move(global_pos)
        self.dialog.exec()

    def set_current_prop_type(self, prop_type: PropType):
        self.label.setText(prop_type.name)

        # Collect pictographs from MainWidget's PictographCollector
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()

        # Pass them into set_prop_type
        self.settings_manager.global_settings.set_prop_type(prop_type, pictographs)

        self.dialog.accept()

