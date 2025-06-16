from typing import TYPE_CHECKING


from .level_ui_manager import LevelUIManager
from .level_image_handler import LevelImageHandler

if TYPE_CHECKING:
    from .filter_by_level_section import FilterByLevelSection


class LevelResizeHandler:
    def __init__(
        self,
        filter_section: "FilterByLevelSection",
        ui_manager: LevelUIManager,
        image_handler: LevelImageHandler,
    ):
        self.filter_section = filter_section
        self.ui_manager = ui_manager
        self.image_handler = image_handler

    def handle_resize(self) -> None:
        self.image_handler.scale_images()
        self._resize_buttons()
        self._resize_labels()

    def _resize_buttons(self) -> None:
        button_width = max(1, self.filter_section.main_widget.width() // 5)
        button_height = max(1, self.filter_section.main_widget.height() // 20)
        font_size = max(10, self.filter_section.main_widget.width() // 100)

        for button in self.ui_manager.buttons.values():
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)
            button.setFixedSize(button_width, button_height)

    def _resize_labels(self) -> None:
        font_size_desc = max(10, self.filter_section.main_widget.width() // 140)
        font_size_header = max(12, self.filter_section.main_widget.width() // 100)

        for label in self.ui_manager.description_labels.values():
            font = label.font()
            font.setPointSize(font_size_desc)
            label.setFont(font)

        for label in self.ui_manager.tally_labels.values():
            font = label.font()
            font.setPointSize(font_size_desc)
            label.setFont(font)

        header_font = self.filter_section.header_label.font()
        header_font.setPointSize(font_size_header)
        self.filter_section.header_label.setFont(header_font)
