from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

from .base_sidebar_section import BaseSidebarSection


class SidebarDateAddedSection(BaseSidebarSection):
    def create_widgets(self, sections_data):
        """
        sections_data might be a list of date-strings like ["01-12-2024", ...]
        We'll group them by year, for example.
        """
        current_year = None

        for section in sections_data:
            if section == "Unknown":
                continue
            # parse e.g. 'day-month-year'
            day, month, year = section.split("-")

            # If the year changes, create a new label + line
            if year != current_year:
                year_label = QLabel(year)
                year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.style_header_label(year_label)
                self.manager.layout.addWidget(year_label)
                self._widgets_created.append(year_label)

                line_label = QLabel()
                line_label.setStyleSheet(
                    "border: 1px solid black; margin: 0; background: black;"
                )
                self.manager.layout.addWidget(line_label)
                self._widgets_created.append(line_label)

                current_year = year

            # Now create a date button
            day_button = QPushButton(self.get_formatted_day(section))
            day_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            day_button.clicked.connect(
                lambda _, sec=section, btn=day_button: self.manager.scroll_to_section(
                    sec, btn
                )
            )
            self.manager.layout.addWidget(day_button)
            self._widgets_created.append(day_button)
            self.manager.buttons.append(day_button)
