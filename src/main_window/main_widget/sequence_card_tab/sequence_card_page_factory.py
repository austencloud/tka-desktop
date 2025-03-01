from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout

if TYPE_CHECKING:
    from widgets.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab


class SequenceCardPageFactory:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab

    def create_page(self) -> QFrame: 
        self.image_displayer = self.sequence_card_tab.image_displayer
        scroll_layout = self.sequence_card_tab.scroll_layout
        margin = self.sequence_card_tab.image_displayer.margin
        if (
            not scroll_layout.count()
            or scroll_layout.itemAt(scroll_layout.count() - 1).layout().count() >= 2
        ):
            current_row_layout = QHBoxLayout()
            current_row_layout.setSpacing(margin)
            current_row_layout.setContentsMargins(margin, margin, margin, margin)
            scroll_layout.addLayout(current_row_layout)
        else:
            current_row_layout = scroll_layout.itemAt(
                scroll_layout.count() - 1
            ).layout()

        page_frame = QFrame(self.sequence_card_tab.scroll_content)
        page_frame.setFixedSize(
            self.image_displayer.page_width, self.image_displayer.page_height
        )
        page_frame.setStyleSheet("background-color: white; border: 1px solid black;")
        page_layout = QGridLayout(page_frame)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)
        current_row_layout.addWidget(page_frame)

        return page_frame  # Return the frame instead of the layout
