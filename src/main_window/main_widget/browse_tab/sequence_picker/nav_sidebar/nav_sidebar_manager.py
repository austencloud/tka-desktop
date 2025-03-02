from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtCore import Qt, QPoint
from typing import TYPE_CHECKING

from main_window.main_widget.browse_tab.sequence_picker.nav_sidebar.level_section import (
    SidebarLevelSection,
)
from .base_sidebar_section import BaseSidebarSection
from .date_added_section import SidebarDateAddedSection
from .generic_section import SidebarGenericSection
from .length_section import SidebarLengthSection
from .letter_section import SidebarLetterSection
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from ..sequence_picker import SequencePickerNavSidebar


class NavSidebarManager:
    def __init__(self, sidebar: "SequencePickerNavSidebar"):
        self.sidebar = sidebar
        self.layout = sidebar.layout
        self.sequence_picker = sidebar.sequence_picker
        self.settings_manager = AppContext.settings_manager()
        self.buttons: list[QPushButton] = []
        self.current_section_obj: BaseSidebarSection | None = None
        self.selected_button: QPushButton | None = None

    def update_sidebar(self, sections, sort_order: str):
        self.clear_sidebar()
        if sort_order == "sequence_length":
            section_obj = SidebarLengthSection(self)
        elif sort_order == "alphabetical":
            section_obj = SidebarLetterSection(self)
        elif sort_order == "date_added":
            section_obj = SidebarDateAddedSection(self)
        elif sort_order == "level":
            section_obj = SidebarLevelSection(self)
        else:
            section_obj = SidebarGenericSection(self)
        section_obj.create_widgets(sections)
        self.current_section_obj = section_obj
        self.set_button_styles()
        self.sidebar.resize_sidebar()

    def clear_sidebar(self):
        if self.current_section_obj:
            self.current_section_obj.clear()
            self.current_section_obj = None
        self.buttons.clear()
        self.selected_button = None

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

    def set_button_styles(self):
        for button in self.buttons:
            selected = button == self.selected_button
            self.style_button(button, selected=selected)

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
        self.selected_button = button
        self.style_button(button, selected=True)
        sort_method = self.settings_manager.browse_settings.get_sort_method()
        if sort_method == "level":
            section = f"Level {section}"
        elif sort_method == "date_added":
            parts = section.split("-")
            section = f"{int(parts[0])}-{int(parts[1])}"
        header = self.sequence_picker.scroll_widget.section_headers.get(section)
        if header:
            scroll_area = self.sequence_picker.scroll_widget.scroll_area
            header_global_pos = header.mapToGlobal(QPoint(0, 0))
            content_widget_pos = scroll_area.widget().mapFromGlobal(header_global_pos)
            vertical_pos = content_widget_pos.y()
            scroll_area.verticalScrollBar().setValue(vertical_pos)

    def apply_font_color(self):
        # Re-check the current font color from settings

        # Re-style all widgets in the current section
        if self.current_section_obj:
            for w in self.current_section_obj._widgets_created:
                if isinstance(w, QLabel):
                    self.style_header_label(w)
                elif isinstance(w, QPushButton):
                    # Keep “selected” logic for the selected button
                    selected = w == self.selected_button
                    self.style_button(w, selected)
