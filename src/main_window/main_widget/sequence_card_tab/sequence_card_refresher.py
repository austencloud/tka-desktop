import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from utils.path_helpers import get_dictionary_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )


class SequenceCardRefresher:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.nav_sidebar = sequence_card_tab.nav_sidebar
        self.image_displayer = sequence_card_tab.image_displayer
        self.pages_cache = sequence_card_tab.pages_cache
        self.pages = sequence_card_tab.pages
        self.cached_page_displayer = sequence_card_tab.cached_page_displayer
        self.currently_displayed_length = 16
        self.initialized = False

    def load_images(self):
        """
        Load sequence card images for the selected length directly from the dictionary.

        This method:
        1. Loads sequences directly from the dictionary
        2. Organizes them by word
        3. Filters them by the selected length
        4. Caches the results for better performance
        """
        selected_length = self.nav_sidebar.selected_length
        self.currently_displayed_length = selected_length

        print(f"Loading sequences for length: {selected_length}")

        # If we have cached pages for this length, use them
        if selected_length in self.pages_cache:
            print(f"Using cached pages for length {selected_length}")
            self.cached_page_displayer.display_cached_pages(selected_length)
        else:
            # Otherwise, load sequences directly from the dictionary
            dictionary_path = get_dictionary_path()
            print(f"Loading sequences from dictionary: {dictionary_path}")

            # Get all sequences from the dictionary
            sequences = self.get_all_sequences(dictionary_path)
            print(f"Found {len(sequences)} total sequences in dictionary")

            # Filter sequences by the selected length
            filtered_sequences = self.filter_sequences_by_length(
                sequences, selected_length
            )
            print(
                f"Filtered to {len(filtered_sequences)} sequences with length {selected_length}"
            )

            # Display the filtered sequences
            self.image_displayer.display_sequences(filtered_sequences)

            # Cache the pages for future use
            self.pages_cache[selected_length] = self.pages.copy()
            print(f"Cached {len(self.pages)} pages for length {selected_length}")

    def get_all_sequences(self, dictionary_path: str) -> list[dict]:
        """
        Get all sequences from the dictionary with their metadata and file paths.

        Returns a list of dictionaries, each containing:
        - path: The path to the sequence file
        - word: The word associated with the sequence
        - metadata: The metadata extracted from the sequence file
        """
        sequences = []

        # Get all word folders in the dictionary
        for word in os.listdir(dictionary_path):
            word_path = os.path.join(dictionary_path, word)

            # Skip non-directories and special directories
            if not os.path.isdir(word_path) or word.startswith("__"):
                continue

            # Get all PNG files in the word folder
            for file in os.listdir(word_path):
                if file.endswith(".png") and not file.startswith("__"):
                    file_path = os.path.join(word_path, file)

                    # Extract metadata
                    from main_window.main_widget.metadata_extractor import (
                        MetaDataExtractor,
                    )

                    metadata = MetaDataExtractor().extract_metadata_from_file(file_path)

                    if metadata and "sequence" in metadata:
                        sequences.append(
                            {"path": file_path, "word": word, "metadata": metadata}
                        )

        return sequences

    def filter_sequences_by_length(
        self, sequences: list[dict], length: int
    ) -> list[dict]:
        """
        Filter sequences by their length.

        The sequence length is calculated as the number of beats in the sequence,
        excluding the metadata entry and the start position entry.
        """
        filtered = []

        # If length is 0, return all sequences (no filtering)
        if length == 0:
            return sequences

        for seq in sequences:
            metadata = seq["metadata"]
            if "sequence" in metadata:
                # Get the sequence array
                sequence_array = metadata["sequence"]

                # Count the number of beats (excluding metadata and start position)
                # The first entry is metadata, the second is start position
                # The rest are actual sequence steps
                seq_length = len(sequence_array) - 2

                # If the sequence length matches the selected length, add it to the filtered list
                if seq_length == length:
                    filtered.append(seq)

        return filtered

    def refresh_sequence_cards(self):
        """Refresh the displayed sequence cards based on selected options."""
        self.scroll_layout = self.sequence_card_tab.scroll_layout
        self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)
        selected_length = self.nav_sidebar.selected_length

        # Update the description label to show the current length
        if selected_length == 0:
            description = "Viewing all sequences - Select a length from the sidebar"
        else:
            description = f"Viewing sequences with length {selected_length} - Select a length from the sidebar"
        self.sequence_card_tab.description_label.setText(description)

        # If we already have this length cached and it's not the current display, just switch
        if (
            self.initialized
            and self.pages_cache
            and selected_length in self.pages_cache
            and selected_length != self.currently_displayed_length
        ):
            self.clear_scroll_layout()
            self.pages.clear()
            self.cached_page_displayer.display_cached_pages(selected_length)
            self.currently_displayed_length = selected_length
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)
            return
        # If we're already displaying this length, do nothing
        elif selected_length == self.currently_displayed_length and self.initialized:
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)
            return

        # Otherwise, we need to load the images
        self.clear_scroll_layout()
        self.pages.clear()
        self.load_images()
        self.initialized = True
        self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

    def clear_scroll_layout(self):
        """Clear all widgets from the scroll layout."""
        for i in reversed(range(self.scroll_layout.count())):
            layout_item = self.scroll_layout.itemAt(i)
            widget = layout_item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                sub_layout = layout_item.layout()
                if sub_layout is not None:
                    while sub_layout.count():
                        sub_item = sub_layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget is not None:
                            sub_widget.setParent(None)
                    self.scroll_layout.removeItem(layout_item)
