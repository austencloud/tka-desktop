import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from settings_manager.global_settings.app_context import AppContext
from .title_label import TitleLabel

if TYPE_CHECKING:
    from ..act_sheet import ActSheet


class ActHeader(QWidget):
    def __init__(self, act_sheet: "ActSheet"):
        super().__init__(act_sheet)
        self.act_sheet = act_sheet
        self.settings_manager = AppContext.settings_manager()

        # Initial header setup
        self._configure_header_style()
        self._initialize_components()
        self._layout_components()
        self._initialize_content()

    def _configure_header_style(self):
        """Set up styling for the header widget."""
        self.header_container = QWidget(self)
        self.header_container.setObjectName("timelineHeader")
        self.header_container.setStyleSheet(
            """
            #timelineHeader {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid black;
                border-radius: 10px;
                padding: 10px;
            }
            """
        )

    def _initialize_components(self):
        """Initialize the labels for date, title, and author."""
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        saved_title = self.settings_manager.write_tab_settings.get_act_title()
        self.title_label = TitleLabel(self, saved_title)
        self.title_label.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.author_label = QLabel(self)
        self.author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _layout_components(self):
        """Arrange components in a vertical layout for the header."""
        layout = QVBoxLayout(self.header_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.date_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.author_label)
        self.header_container.setLayout(layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.header_container)
        self.setLayout(main_layout)

    def _initialize_content(self):
        """Set initial content for date and author labels."""
        self.display_date()
        self.display_author()

    def display_date(self):
        """Fetch and display the current date."""
        date = datetime.datetime.now().strftime("%m/%d/%Y")
        self.date_label.setText(date)

    def display_author(self):
        """Fetch and display the author name."""
        author = self._get_current_author()
        self.author_label.setText(f"Choreography by {author}")

    def save_title(self):
        """Save the current title to settings."""
        new_title = self.title_label.label.text()
        self.settings_manager.write_tab_settings.save_act_title(new_title)

    def resizeEvent(self, event):
        """Adjust the size of each label based on the width of the act sheet."""
        super().resizeEvent(event)
        self.title_label.resize_title_label()
        self._resize_label(self.date_label, self.act_sheet.width() // 50)
        self._resize_label(self.author_label, self.act_sheet.width() // 50)

    def _resize_label(self, label: QLabel, font_size: int):
        """Helper method to resize a QLabel's font size."""
        label.setStyleSheet(f"font-size: {font_size}px;")

    def _get_current_author(self) -> str:
        """Fetch the current author name from settings."""
        return self.settings_manager.users.user_manager.get_current_user()

    def get_title(self) -> str:
        """Return the current title of the act."""
        return self.title_label.label.text()

    def set_title(self, title: str):
        """Set the title of the act."""
        self.title_label.label.setText(title)
        self.save_title()
