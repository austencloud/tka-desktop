from PyQt6.QtWidgets import QDialog, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from data.constants import ANTI, BLUE, FLOAT, HEX_BLUE, HEX_RED, PRO
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import TurnsValue
from .direct_set_turns_button import DirectSetTurnsButton

if TYPE_CHECKING:
    from ..turns_widget import TurnsWidget
from PyQt6.QtWidgets import QHBoxLayout


class DirectSetTurnsDialog(QDialog):
    buttons: dict[str, DirectSetTurnsButton] = {}

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(
            turns_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.turns_display_frame = turns_widget.display_frame
        self.adjustment_manager = turns_widget.adjustment_manager
        self._set_dialog_style()
        self._setup_buttons()
        self._setup_layout()

    def _set_dialog_style(self):
        border_color = HEX_BLUE if self.turns_box.color == BLUE else HEX_RED
        self.setStyleSheet(
            f"""
            QDialog {{
                border: 2px solid {border_color};
                border-radius: 5px;
            }}
        """
        )

    def _setup_buttons(self):
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]  
        if self.turns_box.matching_motion.state.motion_type in [PRO, ANTI, FLOAT]:
            turns_values.insert(0, "fl")
        for value in turns_values:
            button = DirectSetTurnsButton(value, self)
            
            button.clicked.connect(
                lambda _, v=value: self.select_turns(
                    "fl" if v == "fl" else float(v) if "." in v else int(v)
                )
            )
            self.buttons[value] = button

    def _setup_layout(self):
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for button in self.buttons.values():
            layout.addWidget(button)
        self.adjustSize()

    def show_direct_set_dialog(self) -> None:

        self.resize_direct_set_buttons()
        turns_label_rect = self.turns_display_frame.turns_label.geometry()
        global_turns_label_pos = self.turns_display_frame.turns_label.mapToGlobal(
            self.turns_display_frame.turns_label.pos()
        )
        
        turns_widget_pos = self.turns_widget.mapToGlobal(self.turns_widget.pos())
        dialog_x = turns_widget_pos.x()
        dialog_y = global_turns_label_pos.y() + turns_label_rect.height()
        self.move(int(dialog_x), int(dialog_y))
        self.exec()

    def resize_direct_set_buttons(self) -> None:

        self.adjustSize()
        self.updateGeometry()

    def select_turns(self, value):
        self.turns_widget.adjustment_manager.direct_set(TurnsValue(value))
        self.accept()
