from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

from .base_sidebar_section import BaseSidebarSection


class SidebarLetterSection(BaseSidebarSection):
    def create_widgets(self, sections_data):
        letter_label = QLabel("Letter")
        self.style_header_label(letter_label)
        self.manager.layout.addWidget(letter_label)
        self._widgets_created.append(letter_label)

        spacer_line = QLabel()
        spacer_line.setStyleSheet(
            "border: 1px solid black; margin: 0; background: black;"
        )
        self.manager.layout.addWidget(spacer_line)
        self._widgets_created.append(spacer_line)

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
            self.manager.buttons.append(button)
