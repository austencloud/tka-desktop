from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsItemGroup
from PyQt6.QtGui import QFont, QColor

from data.constants import BLUE, HEX_BLUE, HEX_RED, RED
from main_window.main_widget.json_manager.current_sequence_loader import (
    CurrentSequenceLoader,
)
from utilities.reversal_detector import ReversalDetector

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_scene import PictographScene


class BeatReversalGroup(QGraphicsItemGroup):
    name = "Reversals"

    def __init__(self, pictograph: "PictographScene"):
        super().__init__()
        self.pictograph = pictograph
        self.reversal_items: dict[str, QGraphicsTextItem] = {}
        self.create_reversal_symbols()

    def create_reversal_symbols(self):
        red_R = self._create_reversal_text_item(HEX_RED)
        blue_R = self._create_reversal_text_item(HEX_BLUE)

        self.addToGroup(red_R)
        self.addToGroup(blue_R)

        self.pictograph.addItem(self)

        self.pictograph.blue_reversal_symbol = blue_R
        self.pictograph.red_reversal_symbol = red_R

        self.reversal_items[RED] = red_R
        self.reversal_items[BLUE] = blue_R

        self.setVisible(False)

    def update_reversal_symbols(self, visible: bool = True):
        if visible:
            if self.pictograph.view.__class__.__name__ == "OptionView":
                sequence_so_far = CurrentSequenceLoader().load_current_sequence_json()
                if not self.pictograph.pictograph_data:
                    return
                reversal_dict = ReversalDetector.detect_reversal(
                    sequence_so_far, self.pictograph.pictograph_data
                )
                blue_visible = reversal_dict.get("blue_reversal", False)
                red_visible = reversal_dict.get("red_reversal", False)
            else:
                blue_visible = self.pictograph.blue_reversal
                red_visible = self.pictograph.red_reversal
        else:
            blue_visible = False
            red_visible = False

        self.reversal_items[BLUE].setVisible(blue_visible)
        self.reversal_items[RED].setVisible(red_visible)

        center_y = self.pictograph.height() / 2

        if blue_visible and red_visible:
            red_R = self.reversal_items[RED]
            blue_R = self.reversal_items[BLUE]
            total_height = (
                red_R.boundingRect().height() + blue_R.boundingRect().height()
            )
            red_R_y = -total_height / 2
            blue_R_y = red_R_y + red_R.boundingRect().height()
            red_R.setPos(0, red_R_y)
            blue_R.setPos(0, blue_R_y)
        elif blue_visible:
            blue_R = self.reversal_items[BLUE]
            blue_R_y = -blue_R.boundingRect().height() / 2
            blue_R.setPos(0, blue_R_y)
        elif red_visible:
            red_R = self.reversal_items[RED]
            red_R_y = -red_R.boundingRect().height() / 2
            red_R.setPos(0, red_R_y)

        self.setVisible(blue_visible or red_visible)

        x_position = 40
        self.setPos(x_position, center_y)

        # self.pictograph.update()

    def _create_reversal_text_item(self, color) -> QGraphicsTextItem:
        text_item = QGraphicsTextItem("R")
        font = QFont("Georgia", 60, QFont.Weight.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(color))
        return text_item
