from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, QPoint
from typing import TYPE_CHECKING

from settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from ..sequence_picker import SequencePicker


class SequencePickerNavSidebar(QWidget):
    buttons: list[QPushButton] = []
    year_labels: dict[str, QLabel] = {}
    spacer_lines: list[QLabel] = []
    length_spacer_line: QLabel = None
    letter_spacer_line: QLabel = None
    selected_button: QPushButton = None

    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.length_label = QLabel("Length")
        self.letter_label = QLabel("Letter")

        self._setup_scroll_area()

        self.settings_manager = AppContext.settings_manager()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def _setup_scroll_area(self):
        self.scroll_content = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.scroll_content)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setStyleSheet("background: transparent;")

    def update_sidebar(self, sections, sort_order):
        self.clear_sidebar()

        if sort_order == "sequence_length":
            self.layout.setAlignment(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignVCenter
            )

            self.length_label = QLabel("Length")
            self.style_header_label(self.length_label)
            self.layout.addWidget(self.length_label)

            self.length_spacer_line = QLabel()
            self.length_spacer_line.setStyleSheet(
                "border: 1px solid black; margin: 0px 0; background: black;"
            )
            self.layout.addWidget(self.length_spacer_line)

            for section in sections:
                button = QPushButton(str(section))
                button.clicked.connect(
                    lambda checked, sec=section, btn=button: self.scroll_to_section(
                        sec, btn
                    )
                )
                button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.layout.addWidget(button)
                self.buttons.append(button)

        elif sort_order == "alphabetical":
            self.layout.setAlignment(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignVCenter
            )

            self.letter_label = QLabel("Letter")
            self.style_header_label(self.letter_label)
            self.layout.addWidget(self.letter_label)

            self.letter_spacer_line = QLabel()
            self.letter_spacer_line.setStyleSheet(
                "border: 1px solid black; margin: 0px 0; background: black;"
            )
            self.layout.addWidget(self.letter_spacer_line)

            for section in sections:
                button = QPushButton(str(section))
                button.clicked.connect(
                    lambda checked, sec=section, btn=button: self.scroll_to_section(
                        sec, btn
                    )
                )
                button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.layout.addWidget(button)
                self.buttons.append(button)

        elif sort_order == "date_added":
            self.layout.setAlignment(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignVCenter
            )

            current_year = None
            for section in sections:
                if section == "Unknown":
                    continue
                year = section.split("-")[2]
                date = section
                day = self.get_formatted_day(date)

                if year != current_year:
                    year_label = QLabel(year)
                    year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.style_header_label(year_label)
                    self.layout.addWidget(year_label)
                    spacer_line = QLabel()
                    spacer_line.setStyleSheet(
                        "border: 1px solid black; margin: 0px 0; background: black;"
                    )
                    self.spacer_lines.append(spacer_line)
                    self.layout.addWidget(spacer_line)

                    self.year_labels[year] = year_label
                    current_year = year

                date_button = QPushButton(day)
                date_button.clicked.connect(
                    lambda checked, sec=section, btn=date_button: self.scroll_to_section(
                        sec, btn
                    )
                )
                date_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.layout.addWidget(date_button)
                self.buttons.append(date_button)

        else:
            self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            for section in sections:
                button = QPushButton(str(section))
                button.clicked.connect(
                    lambda checked, sec=section, btn=button: self.scroll_to_section(
                        sec, btn
                    )
                )
                button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.layout.addWidget(button)
                self.buttons.append(button)

        self.set_styles()
        self.resize_sidebar()

    def clear_sidebar(self):
        widgets = self.buttons + list(self.year_labels.values()) + self.spacer_lines
        if self.length_label:
            widgets.append(self.length_label)
        if self.length_spacer_line:
            widgets.append(self.length_spacer_line)
        if self.letter_label:
            widgets.append(self.letter_label)
        if self.letter_spacer_line:
            widgets.append(self.letter_spacer_line)

        for widget in widgets:
            self.layout.removeWidget(widget)
            widget.hide()
            widget.deleteLater()

        self.buttons.clear()
        self.year_labels.clear()
        self.spacer_lines.clear()
        self.length_label = None
        self.length_spacer_line = None
        self.letter_label = None
        self.letter_spacer_line = None
        self.selected_button = None

    def get_formatted_day(self, date: str) -> str:
        day = date.split("-")[0].lstrip("0") + "-" + date.split("-")[1].lstrip("0")
        return day

    def style_button(self, button: QPushButton, selected: bool = False):
        font_color = self.sequence_picker.main_widget.font_color_updater.get_font_color(
            self.settings_manager.global_settings.get_background_type()
        )
        button_background_color = "lightgray" if font_color == "black" else "#555"
        hover_color = "lightgray" if font_color == "black" else "#555"
        if selected:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {button_background_color};
                    color: {font_color};
                    border-radius: 5px;
                    padding: 5px;
                    font-weight: bold;
                }}
                """
            )
        else:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    color: {font_color};
                    padding: 5px;
                    text-align: center;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: {hover_color};
                }}
            """
            )

    def style_header_label(self, label: QLabel):
        font_color = self.sequence_picker.main_widget.font_color_updater.get_font_color(
            self.settings_manager.global_settings.get_background_type()
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"""
            QLabel {{
                color: {font_color};
                padding: 5px;
                font-weight: bold;
            }}
        """
        )

    def scroll_to_section(self, section: str, button: QPushButton):
        if self.selected_button:
            self.style_button(self.selected_button, selected=False)
        self.style_button(button, selected=True)
        self.selected_button = button

        if "-" in section:
            section = (
                section.split("-")[0].lstrip("0")
                + "-"
                + section.split("-")[1].lstrip("0")
            )
        header = self.sequence_picker.scroll_widget.section_headers.get(section)
        if header:
            scroll_area = self.sequence_picker.scroll_widget.scroll_area
            header_global_pos = header.mapToGlobal(QPoint(0, 0))
            content_widget_pos = scroll_area.widget().mapFromGlobal(header_global_pos)
            vertical_pos = content_widget_pos.y()
            scroll_area.verticalScrollBar().setValue(vertical_pos)

    def set_styles(self):
        for button in self.buttons:
            selected = button == self.selected_button
            self.style_button(button, selected=selected)
        for year_label in self.year_labels.values():
            self.style_header_label(year_label)
        if self.length_label:
            self.style_header_label(self.length_label)
        if self.letter_label:
            self.style_header_label(self.letter_label)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_sidebar()

    def resize_sidebar(self):
        for spacer_line in self.spacer_lines:
            spacer_line.setFixedHeight(1)
        if self.letter_spacer_line:
            self.letter_spacer_line.setFixedHeight(1)
        if self.length_spacer_line:
            self.length_spacer_line.setFixedHeight(1)
        if self.length_label:
            self.resize_label(self.length_label)
        if self.letter_label:
            self.resize_label(self.letter_label)
        if self.year_labels:
            for year_label in self.year_labels.values():
                self.resize_label(year_label)

        for button in self.buttons:
            font_size = self.sequence_picker.main_widget.width() // 80
            button_font = button.font()
            button_font.setPointSize(font_size)
            button.setFont(button_font)

        max_width = 0
        for button in self.buttons:
            max_width = max(
                max_width, button.fontMetrics().boundingRect("12-33").width()
            )
        extra_padding = self.sequence_picker.width() // 25
        self.setFixedWidth(self.sequence_picker.main_widget.width() // 16)

    def resize_label(self, label: QLabel):
        font_size = self.sequence_picker.height() // 40
        label_font = label.font()
        label_font.setPointSize(max(font_size, 8))
        label.setFont(label_font)
