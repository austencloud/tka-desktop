import os
from typing import TYPE_CHECKING, Optional

from utils.path_helpers import get_data_path

from main_window.main_widget.metadata_extractor import (
    MetaDataExtractor,
    ThumbnailFinder,
)

if TYPE_CHECKING:
    pass


class LevelDataManager:
    def __init__(self):
        self.metadata_extractor = MetaDataExtractor()
        self._all_sequences_with_levels: Optional[list[tuple[str, list[str], int]]] = (
            None
        )

    def get_all_sequences_with_levels(self) -> list[tuple[str, list[str], int]]:
        if self._all_sequences_with_levels is None:
            self._load_sequences()
        return self._all_sequences_with_levels

    def _load_sequences(self) -> None:
        dictionary_dir = get_data_path("dictionary")
        base_words = [
            (
                d,
                ThumbnailFinder().find_thumbnails(os.path.join(dictionary_dir, d)),
            )
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d)) and "__pycache__" not in d
        ]

        sequences_with_levels: list[tuple[str, list[str], int]] = []
        for word, thumbnails in base_words:
            level = self.get_sequence_level_from_thumbnails(thumbnails)
            if level is not None:
                sequences_with_levels.append((word, thumbnails, level))

        self._all_sequences_with_levels = sequences_with_levels

    def get_sequence_counts_per_level(self) -> dict[int, int]:
        level_counts: dict[int, int] = {}
        sequences = self.get_all_sequences_with_levels()
        for _, _, level in sequences:
            level_counts[level] = level_counts.get(level, 0) + 1
        return level_counts

    def get_sequences_by_level(self, level: int) -> list[tuple[str, list[str]]]:
        sequences = self.get_all_sequences_with_levels()
        return [
            (word, thumbnails)
            for word, thumbnails, seq_level in sequences
            if seq_level == level
        ]

    def get_sequence_level_from_thumbnails(
        self, thumbnails: list[str]
    ) -> Optional[int]:
        for thumbnail in thumbnails:
            level = self.metadata_extractor.get_level(thumbnail)
            if level is not None:
                return level
        return None
