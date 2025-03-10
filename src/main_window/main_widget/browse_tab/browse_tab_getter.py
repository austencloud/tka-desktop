from typing import TYPE_CHECKING, Any, Generator
import os
from main_window.main_widget.metadata_extractor import MetaDataExtractor
from utils.path_helpers import get_data_path

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabGetter:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab

    def all_sequences(self) -> list[tuple[str, list[str], int]]:
        """Retrieve all sequences with their respective difficulty levels."""
        sequences = [
            (
                word,
                thumbnails,
                max(
                    [
                        MetaDataExtractor().get_level(thumbnail)
                        for thumbnail in thumbnails
                        if MetaDataExtractor().get_level(thumbnail) is not None
                    ],
                    default=1,  # Default difficulty level
                ),
            )
            for word, thumbnails in self.base_words()
        ]
        return sequences

    def base_words(self) -> Generator[tuple[str, list[str]], Any, None]:
        """Generator version of base_words() to optimize performance."""
        dictionary_dir = get_data_path("dictionary")

        for word in os.listdir(dictionary_dir):
            if (
                os.path.isdir(os.path.join(dictionary_dir, word))
                and "__pycache__" not in word
            ):
                thumbnails = (
                    self.browse_tab.main_widget.thumbnail_finder.find_thumbnails(
                        os.path.join(dictionary_dir, word)
                    )
                )
                yield word, thumbnails
