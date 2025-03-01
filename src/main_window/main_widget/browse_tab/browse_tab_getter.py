from typing import TYPE_CHECKING
import os
from utils.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabGetter:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab

    def all_sequences(self) -> list[tuple[str, list[str], int]]:
        """Retrieve all sequences with their respective lengths."""
        dictionary_dir = get_images_and_data_path("src\data\generated_data\dictionary")
        sequences = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.base_words(dictionary_dir)
            for thumbnail in thumbnails
        ]
        return sequences

    def base_words(self, dictionary_dir) -> list[tuple[str, list[str]]]:
        """Helper method to retrieve words and their thumbnails."""
        return [
            (
                word,
                self.browse_tab.main_widget.thumbnail_finder.find_thumbnails(
                    os.path.join(dictionary_dir, word)
                ),
            )
            for word in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, word))
            and "__pycache__" not in word
        ]
