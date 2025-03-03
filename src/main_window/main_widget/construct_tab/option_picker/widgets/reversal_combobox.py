from typing import TYPE_CHECKING, Callable
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt, QSize

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.widgets.reversal_filter_widget import (
        OptionPickerReversalFilter,
    )


class ReversalCombobox(QComboBox):
    def __init__(
        self,
        reversal_filter: "OptionPickerReversalFilter",
        mw_size_provider: Callable[[], QSize],
    ):
        super().__init__(reversal_filter)
        self.mw_size_provider = mw_size_provider
        self.addItem("All", userData=None)
        self.addItem("Continuous", userData="continuous")
        self.addItem("One Reversal", userData="one_reversal")
        self.addItem("Two Reversals", userData="two_reversals")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.currentTextChanged.connect(reversal_filter.on_filter_changed)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.mw_size_provider().width()
        font = self.font()
        font.setPointSize(int(w // 100))
        font.setFamily("Georgia")
        self.setFont(font)
        self.setStyleSheet(
            f"""
            QComboBox {{
                background-color: white;
                color: black;
                border: 1px solid gray;
                padding: 2px 4px;
                font-size: {int(w//100)}px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: black;
                selection-background-color: lightgray;
                selection-color: black;
                font-size: {int(w//100)}px;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: lightblue;
                color: black;
                font-size: {int(w//100)}px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox:hover {{
                border: 1px solid lightgray;
            }}
            QComboBox:focus {{
                border: 1px solid blue;
            }}
        """
        )
