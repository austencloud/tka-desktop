from datetime import datetime
from typing import TYPE_CHECKING

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabFilterManager:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.metadata_extractor = self.browse_tab.main_widget.metadata_extractor

    def filter_favorites(self) -> list[tuple[str, list[str], int]]:
        dictionary_dir = get_images_and_data_path("dictionary")
        return [
            (word, thumbnails, self._get_sequence_length(thumbnails[0]))
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
            if any(self._is_favorite(thumbnail) for thumbnail in thumbnails)
        ]

    def filter_all_sequences(self) -> list[tuple[str, list[str], int]]:
        dictionary_dir = get_images_and_data_path("dictionary")
        return [
            (word, thumbnails, self._get_sequence_length(thumbnails[0]))
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
        ]

    def filter_most_recent(self, date: datetime) -> list[tuple[str, list[str], int]]:
        dictionary_dir = get_images_and_data_path("dictionary")
        return [
            (word, thumbnails, self._get_sequence_length(thumbnails[0]))
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
            if self.browse_tab.sequence_picker.section_manager.get_date_added(
                thumbnails
            )
            >= date
        ]

    def filter_by_tag(self, tag: str) -> list[tuple[str, list[str], int]]:
        dictionary_dir = get_images_and_data_path("dictionary")
        return [
            (word, thumbnails, self._get_sequence_length(thumbnails[0]))
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
            if tag in self.metadata_extractor.get_tags(thumbnails[0])
        ]

    def _get_sequence_length(self, thumbnail: str) -> int:
        return self.metadata_extractor.get_length(thumbnail)

    def _is_favorite(self, thumbnail: str) -> bool:
        return self.metadata_extractor.get_favorite_status(thumbnail)
