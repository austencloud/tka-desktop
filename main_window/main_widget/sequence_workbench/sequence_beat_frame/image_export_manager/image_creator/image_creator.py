from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat_view import (
    BeatView,
)
from main_window.main_widget.sequence_workbench.sequence_beat_frame.image_export_manager.image_creator.beat_reversal_processor import (
    BeatReversalProcessor,
)

from .height_determiner import HeightDeterminer
from .beat_drawer import BeatDrawer
from .user_info_drawer import UserInfoDrawer
from .word_drawer import WordDrawer
from .difficulty_level_drawer import DifficultyLevelDrawer

if TYPE_CHECKING:
    from ..image_export_manager import ImageExportManager


class ImageCreator:
    """Class responsible for creating sequence images."""

    BASE_MARGIN = 50

    def __init__(self, export_manager: "ImageExportManager"):
        self.export_manager = export_manager
        self.beat_frame = export_manager.beat_frame
        self.layout_manager = export_manager.layout_handler
        self.beat_size = self.beat_frame.start_pos_view.beat.width()
        self.beat_factory = export_manager.beat_factory
        self.beat_scale = 1
        self._setup_drawers()
        self.reversal_processor = BeatReversalProcessor()

    def _setup_drawers(self):
        """Set up drawer instances."""
        self.beat_drawer = BeatDrawer(self)
        self.word_drawer = WordDrawer(self)
        self.user_info_drawer = UserInfoDrawer(self)
        self.difficulty_level_drawer = DifficultyLevelDrawer(self)

    def create_sequence_image(
        self, sequence: list[dict], include_start_pos=True, options: dict = None
    ) -> QImage:
        """Create an image of the sequence."""

        options = self._parse_options(options)
        filled_beats = self._process_sequence(sequence)
        num_filled_beats = len(filled_beats)
        column_count, row_count = self.layout_manager.calculate_layout(
            num_filled_beats, include_start_pos
        )

        options["additional_height_top"], options["additional_height_bottom"] = (
            self._determine_additional_heights(options, num_filled_beats)
        )

        if options["add_reversal_symbols"]:
            self.reversal_processor.process_reversals(sequence, filled_beats)

        image = self._create_image(
            column_count,
            row_count,
            options["additional_height_top"] + options["additional_height_bottom"],
        )

        self.beat_drawer.draw_beats(
            image,
            filled_beats,
            column_count,
            row_count,
            include_start_pos,
            options["additional_height_top"],
            options["add_beat_numbers"],
        )

        self._draw_additional_info(image, filled_beats, options, num_filled_beats)

        return image

    def _parse_options(self, options: dict = None) -> dict:
        """Parse options and set default values."""
        default_options = {
            "add_beat_numbers": True,
            "add_reversal_symbols": True,
            "add_user_info": False,
            "add_word": False,
            "add_difficulty_level": False,
        }
        if options:
            default_options.update(options)
        return default_options

    def _process_sequence(self, sequence: list[dict]) -> list[BeatView]:
        """Process the sequence into beat views."""
        return self.beat_factory.process_sequence_to_beats(sequence)

    def _determine_additional_heights(
        self, options: dict, num_filled_beats: int
    ) -> tuple:
        """Determine additional heights needed for the image."""
        return HeightDeterminer.determine_additional_heights(
            options, num_filled_beats, self.beat_scale
        )

    def _draw_additional_info(
        self,
        image: QImage,
        filled_beats: list[BeatView],
        options: dict,
        num_filled_beats: int,
    ):
        """Draw additional information like user info, word, and difficulty level."""
        if options["add_user_info"]:
            self.user_info_drawer.draw_user_info(image, options, num_filled_beats)

        if options["add_word"]:
            word = self.beat_frame.get.current_word()
            self.word_drawer.draw_word(
                image, word, num_filled_beats, options["additional_height_top"]
            )

        if options["add_difficulty_level"]:
            difficulty_level = self.export_manager.main_widget.sequence_level_evaluator.get_sequence_difficulty_level(
                self.export_manager.beat_frame.json_manager.loader_saver.load_current_sequence()
            )
            self.difficulty_level_drawer.draw_difficulty_level(
                image, difficulty_level, options["additional_height_top"]
            )

        for beat_view in filled_beats:
            beat_view.beat.beat_number_item.setVisible(options["add_beat_numbers"])

    def _create_image(self, column_count, row_count, additional_height=0) -> QImage:
        """Create a new QImage with the given dimensions."""
        image_width = int((column_count * self.beat_size * self.beat_scale))
        image_height = int(
            (row_count * self.beat_size * self.beat_scale) + additional_height
        )
        image = QImage(image_width, image_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        return image
