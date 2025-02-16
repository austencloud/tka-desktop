from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from typing import TYPE_CHECKING
from base_widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker


class StartPosPickerPictographFrame(QWidget):
    COLUMN_COUNT = 3

    def __init__(self, start_pos_picker: "StartPosPicker") -> None:
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.option_click_handler = (
            self.start_pos_picker.construct_tab.option_picker.click_handler
        )
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.pictographs_layout = QHBoxLayout()
        self.layout.addLayout(self.pictographs_layout)
        self.variation_buttons: dict[str, QPushButton] = {}
        self.start_positions: dict[str, Pictograph] = {}

    def resizeEvent(self, event) -> None:
        # self.start_pos_picker.choose_your_start_pos_label.set_stylesheet()
        for button in self.variation_buttons.values():
            button.setMaximumWidth(
                self.start_positions[list(self.start_positions.keys())[0]].view.width()
            )

    def _add_start_pos_to_layout(self, start_pos: Pictograph) -> None:
        # start_pos.view.mousePressEvent = self.option_click_handler.handle_click(
        #     start_pos
        # )
        self.pictographs_layout.addWidget(start_pos.view)
        self.start_pos_picker.start_options[start_pos.letter] = start_pos
        key = f"{start_pos.letter}_{start_pos.start_pos}_{start_pos.end_pos}"
        self.start_pos_picker.main_widget.pictograph_cache[start_pos.letter][
            key
        ] = start_pos
        self.start_positions[start_pos.letter] = start_pos

    def clear_pictographs(self) -> None:
        for i in reversed(range(self.pictographs_layout.count())):
            widget_to_remove = self.pictographs_layout.itemAt(i).widget()
            self.pictographs_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
