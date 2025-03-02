from PyQt6.QtWidgets import (
    QPushButton,
    QLabel,
)
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .nav_sidebar_manager import NavSidebarManager


class BaseSidebarSection:
    """
    Abstract-ish base for a 'section' that draws some part
    of the sidebar (header, spacer, buttons).
    """

    def __init__(self, manager: "NavSidebarManager"):
        self.manager = manager
        self._widgets_created: list[QPushButton, QLabel] = []

    def create_widgets(self, sections_data):
        """
        Create whatever label(s) and button(s) are needed for this section.
        'sections_data' is flexible (like a list of sections or levels).
        Store references in self._widgets_created so we can hide/clear them.
        """
        raise NotImplementedError("Implement in subclass")

    def clear(self):
        """
        Hide and remove from layout all the widgets we created.
        """
        for w in self._widgets_created:
            self.manager.layout.removeWidget(w)
            w.hide()

        self._widgets_created.clear()

    # Optional convenience wrappers
    def style_header_label(self, label: QLabel):
        self.manager.style_header_label(label)

    def style_button(self, button: QPushButton, selected=False):
        self.manager.style_button(button, selected)

    def get_formatted_day(self, date_str: str) -> str:
        """
        If you have date 'MM-DD-YYYY', you want to display something else.
        Provide that logic here or in the manager.
        """
        parts = date_str.split("-")
        day = parts[0].lstrip("0")
        month = parts[1].lstrip("0")
        return f"{day}-{month}"
