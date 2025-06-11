from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QRect

from main_window.main_widget.write_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from .act_header import ActHeader


class TitleLabel(EditableLabel):
    def __init__(self, header_widget: "ActHeader", title_text: str):
        title_text = header_widget.act_sheet.settings.get_act_title()
        super().__init__(header_widget, title_text)
        self.header_widget = header_widget
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit.setStyleSheet("background-color: #F0F0F0; padding: 5px;")
        self.edit.textChanged.connect(self._adjust_edit_geometry)

    def _show_edit(self, event=None):
        """Show the QLineEdit for editing with the current title pre-filled."""
        self.edit.setFixedHeight(self.label.height())
        super()._show_edit(event)
        self._adjust_edit_geometry()

    def _hide_edit(self):
        """Save changes and hide the editor."""
        new_title = self.edit.text()
        self.label.setText(new_title or self.label.text())
        self.header_widget.act_sheet.settings.save_act_title(new_title)
        self.layout.setCurrentWidget(self.label)
        super()._hide_edit()
        self.header_widget.act_sheet.act_saver.save_act()

    def _adjust_edit_geometry(self):
        """Adjust geometry to keep the QLineEdit centered based on text content."""
        text_width = self.edit.fontMetrics().horizontalAdvance(self.edit.text()) + 20

        label_rect = self.label.geometry()
        center_x = label_rect.center().x()

        edit_x = center_x - (text_width // 2)
        self.edit.setGeometry(
            QRect(edit_x, label_rect.y(), text_width, label_rect.height())
        )

    def resize_title_label(self):
        """Resize the title label based on the act sheet width."""
        title_size = self.header_widget.act_sheet.width() // 20
        title_label_stylesheet = (
            f"font-size: {title_size}px; "
            f"font-weight: bold; "
            f"font-family: 'Monotype Corsiva', cursive;"
        )
        self.label.setStyleSheet(title_label_stylesheet)

        self._adjust_edit_geometry()
