from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

from .base_sidebar_section import BaseSidebarSection


class SidebarLengthSection(BaseSidebarSection):
    def create_widgets(self, sections_data):
        """sections_data is a list of 'section' strings with lengths."""
        # Create a header
        length_label = QLabel("Length")
        self.style_header_label(length_label)
        self.manager.layout.addWidget(length_label)
        self._widgets_created.append(length_label)

        # Create a horizontal line or spacer
        spacer_line = QLabel()
        spacer_line.setStyleSheet(
            "border: 1px solid black; margin: 0; background: black;"
        )
        self.manager.layout.addWidget(spacer_line)
        self._widgets_created.append(spacer_line)

        # Create a button for each length
        for section in sections_data:
            button = QPushButton(str(section))
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.clicked.connect(
                lambda _, sec=section, btn=button: self.manager.scroll_to_section(
                    sec, btn
                )
            )
            self.manager.layout.addWidget(button)
            self._widgets_created.append(button)
            self.manager.buttons.append(button)  # So the manager can style it
