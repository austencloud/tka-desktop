from typing import TYPE_CHECKING, Callable
from PyQt6.QtWidgets import QVBoxLayout, QGroupBox
from enums.letter.letter_type import LetterType

from data.constants import OPP, SAME
from PyQt6.QtCore import Qt
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from main_window.main_widget.pictograph_key_generator import PictographKeyGenerator
from PyQt6.QtCore import QSize
from main_window.main_widget.construct_tab.option_picker.widgets.scroll.section_pictograph_frame import (
    OptionPickerSectionPictographFrame,
)
from main_window.main_widget.construct_tab.option_picker.widgets.scroll.section_header import (
    OptionPickerSectionHeader,
)

if TYPE_CHECKING:
    from .option_scroll import OptionScroll


class OptionPickerSectionWidget(QGroupBox):
    SCROLLBAR_WIDTH = 20

    def __init__(
        self,
        letter_type: LetterType,
        scroll_area: "OptionScroll",
        mw_size_provider: Callable[[], QSize],
    ):
        super().__init__(None)
        self.option_scroll = scroll_area
        self.letter_type = letter_type
        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.is_groupable = letter_type in [
            LetterType.Type4,
            LetterType.Type5,
            LetterType.Type6,
        ]
        self.mw_size_provider = mw_size_provider

    def setup_components(self) -> None:
        self.pictograph_frame = OptionPickerSectionPictographFrame(self)
        self.pictographs: dict[str, LegacyPictograph] = {}
        self.pictograph_frame.setStyleSheet("QFrame {border: none;}")
        self._setup_header()
        self._setup_layout()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.pictograph_frame)

    def _setup_header(self) -> None:
        self.header = OptionPickerSectionHeader(self)
        self.header.type_button.clicked.connect(self.toggle_section)

    def toggle_section(self) -> None:
        is_visible = not self.pictograph_frame.isVisible()
        self.pictograph_frame.setVisible(is_visible)

    def clear_pictographs(self) -> None:

        for pictograph in self.pictographs.values():
            self.pictograph_frame.layout.removeWidget(pictograph.elements.view)
            pictograph.elements.view.setVisible(False)
        self.pictographs = {}

    def add_pictograph(self, pictograph: LegacyPictograph) -> None:
        COLUMN_COUNT = self.option_scroll.option_picker.COLUMN_COUNT
        self.pictographs[
            PictographKeyGenerator().generate_pictograph_key(
                pictograph.state.pictograph_data
            )
        ] = pictograph

        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)
        self.pictograph_frame.layout.addWidget(pictograph.elements.view, row, col)
        pictograph.elements.view.setVisible(True)

    def resizeEvent(self, event) -> None:
        """Resizes the section widget and ensures minimal space usage."""
        width = self.mw_size_provider().width() // 2

        if self.letter_type in [LetterType.Type1, LetterType.Type2, LetterType.Type3]:
            self.setFixedWidth(width)

        elif self.letter_type in [LetterType.Type4, LetterType.Type5, LetterType.Type6]:
            COLUMN_COUNT = self.option_scroll.option_picker.COLUMN_COUNT

            calculated_width = int(
                (width / COLUMN_COUNT) - ((self.option_scroll.spacing))
            )

            view_width = (
                calculated_width
                if calculated_width < self.mw_size_provider().height() // 8
                else self.mw_size_provider().height() // 8
            )
            width = int(view_width * 8) // 3
            self.setFixedWidth(width)

        super().resizeEvent(event)
