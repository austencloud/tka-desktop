import os
import time
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication
from utils.path_helpers import get_sequence_card_image_exporter_path
from main_window.main_widget.metadata_extractor import MetaDataExtractor
from ..core.cache_manager import SequenceCardCacheManager
from ..loading.loading_dialog import SequenceCardLoadingDialog

if TYPE_CHECKING:
    from ..tab import SequenceCardTab


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

        # Initialize cache manager
        self.cache_manager = SequenceCardCacheManager()
        self.loading_dialog = None

        # Clean up cache on startup
        QTimer.singleShot(5000, self.cache_manager.clean_cache)

    def load_images(self):
        """
        Load sequence card images for the selected length from the sequence_card_images directory.

        This method:
        1. Checks the persistent cache first for faster loading
        2. Falls back to loading from the sequence_card_images directory if needed
        3. Organizes sequences by word
        4. Filters them by the selected length
        5. Caches the results for better performance
        """
        try:
            selected_length = self.nav_sidebar.selected_length
            self.currently_displayed_length = selected_length

            # If we have in-memory cached pages for this length, use them
            if selected_length in self.pages_cache:
                self.cached_page_displayer.display_cached_pages(selected_length)
                return

            # Check if we have a valid persistent cache for this length
            try:
                cached_sequences = self.cache_manager.load_from_cache(selected_length)
            except Exception as cache_error:
                print(f"Error loading from cache: {cache_error}")
                cached_sequences = None

            if cached_sequences:
                # We have valid cached data, use it
                print(f"Using cached sequence data for length {selected_length}")

                try:
                    # Filter sequences by the selected length (should already be filtered, but just in case)
                    filtered_sequences = self.filter_sequences_by_length(
                        cached_sequences, selected_length
                    )

                    # Display the filtered sequences
                    self.image_displayer.display_sequences(filtered_sequences)

                    # Cache the pages for future use
                    self.pages_cache[selected_length] = self.pages.copy()
                except Exception as e:
                    print(f"Error processing cached sequences: {e}")
                    # Fall back to loading from source
                    cached_sequences = None

            # If no valid cache or error processing cached data, load from source
            if not cached_sequences:
                # No valid cache, load from the sequence_card_images directory
                print(
                    f"No valid cache for length {selected_length}, loading from source"
                )

                # Show loading dialog for initial cache creation
                self._show_loading_dialog()

                try:
                    # Load sequences from the sequence_card_images directory
                    images_path = get_sequence_card_image_exporter_path()

                    # Ensure the directory exists
                    if not os.path.exists(images_path):
                        os.makedirs(images_path, exist_ok=True)
                        print(f"Created sequence card images directory: {images_path}")

                    # Get all sequences from the sequence_card_images directory
                    sequences = self.get_all_sequences(images_path)

                    # Update loading dialog
                    if self.loading_dialog:
                        self.loading_dialog.set_operation("Filtering sequences...")
                        QApplication.processEvents()

                    # Filter sequences by the selected length
                    filtered_sequences = self.filter_sequences_by_length(
                        sequences, selected_length
                    )

                    # Update loading dialog
                    if self.loading_dialog:
                        self.loading_dialog.set_operation("Displaying sequences...")
                        QApplication.processEvents()

                    # Display the filtered sequences
                    self.image_displayer.display_sequences(filtered_sequences)

                    # Cache the pages for future use
                    self.pages_cache[selected_length] = self.pages.copy()

                    # Save to persistent cache
                    if self.loading_dialog:
                        self.loading_dialog.set_operation("Saving to cache...")
                        QApplication.processEvents()

                    try:
                        self.cache_manager.save_to_cache(
                            selected_length, filtered_sequences
                        )
                    except Exception as save_error:
                        print(f"Error saving to cache: {save_error}")

                    # Preload cache for common sequence lengths in the background
                    if selected_length == 0:  # Only preload when showing all sequences
                        if self.loading_dialog:
                            self.loading_dialog.set_operation(
                                "Preloading common sequence lengths..."
                            )
                            QApplication.processEvents()

                        try:
                            # Preload common lengths using the full sequence list
                            self.cache_manager.preload_common_lengths(sequences)
                        except Exception as preload_error:
                            print(f"Error preloading common lengths: {preload_error}")

                except Exception as e:
                    print(f"Error loading sequences from source: {e}")
                    import traceback

                    traceback.print_exc()

                    # Show error message
                    if self.loading_dialog:
                        self.loading_dialog.set_operation(f"Error: {str(e)}")
                        QApplication.processEvents()
                        time.sleep(2)  # Show error for 2 seconds
                finally:
                    # Close loading dialog
                    self._close_loading_dialog()

        except Exception as e:
            print(f"Unexpected error in load_images: {e}")
            import traceback

            traceback.print_exc()
            self._close_loading_dialog()

    def get_all_sequences(self, images_path: str) -> list[dict]:
        """
        Get all sequences from the sequence_card_images directory with their metadata and file paths.

        Returns a list of dictionaries, each containing:
        - path: The path to the sequence file
        - word: The word associated with the sequence
        - metadata: The metadata extracted from the sequence file
        """
        sequences = []
        metadata_extractor = MetaDataExtractor()

        # Validate the images path
        if not os.path.exists(images_path):
            try:
                os.makedirs(images_path, exist_ok=True)
            except Exception:
                return sequences

        # First, count total files for progress reporting
        total_files = 0
        word_folders = []

        try:
            # Get all word folders in the sequence_card_images directory
            for word in os.listdir(images_path):
                word_path = os.path.join(images_path, word)

                # Skip non-directories and special directories
                if not os.path.isdir(word_path) or word.startswith("__"):
                    continue

                word_folders.append(word)

                # Count PNG files in the word folder
                try:
                    for file in os.listdir(word_path):
                        if file.endswith(".png") and not file.startswith("__"):
                            total_files += 1
                except Exception:
                    pass
        except Exception:
            return sequences

        # If no files found, return empty list
        if total_files == 0:
            return sequences

        # Update loading dialog
        if self.loading_dialog:
            self.loading_dialog.set_progress(0, total_files)
            self.loading_dialog.set_operation(
                f"Loading metadata for {total_files} sequence images..."
            )
            QApplication.processEvents()

        # Process each word folder
        processed_files = 0
        success_count = 0
        error_count = 0

        for word in word_folders:
            word_path = os.path.join(images_path, word)

            try:
                # Get all PNG files in the word folder
                for file in os.listdir(word_path):
                    if file.endswith(".png") and not file.startswith("__"):
                        file_path = os.path.join(word_path, file)

                        # Update loading dialog every 5 files to improve performance
                        if processed_files % 5 == 0 and self.loading_dialog:
                            self._update_loading_progress(
                                processed_files,
                                total_files,
                                f"Processing: {word}/{file}",
                            )

                        try:
                            # Validate file exists
                            if not os.path.exists(file_path):
                                print(f"File does not exist: {file_path}")
                                error_count += 1
                                processed_files += 1
                                continue

                            # Extract metadata
                            metadata = metadata_extractor.extract_metadata_from_file(
                                file_path
                            )

                            if metadata and "sequence" in metadata:
                                sequences.append(
                                    {
                                        "path": file_path,
                                        "word": word,
                                        "metadata": metadata,
                                    }
                                )
                                success_count += 1
                            else:
                                print(f"Invalid or missing metadata in {file_path}")
                                error_count += 1
                        except Exception as e:
                            print(f"Error loading image: {file_path}")
                            print(f"Error details: {e}")
                            error_count += 1

                        processed_files += 1
            except Exception as e:
                print(f"Error processing word folder {word_path}: {e}")

        # Update loading dialog
        if self.loading_dialog:
            self._update_loading_progress(
                total_files,
                total_files,
                f"Metadata extraction complete: {success_count} successful, {error_count} errors",
            )

        print(
            f"Sequence metadata extraction complete: {len(sequences)} sequences loaded, {error_count} errors"
        )
        return sequences

    def filter_sequences_by_length(
        self, sequences: list[dict], length: int
    ) -> list[dict]:
        """
        Filter sequences by the specified length.

        If length is 0, return all sequences.
        """
        if length == 0:
            return sequences

        filtered_sequences = []

        for sequence in sequences:
            metadata = sequence.get("metadata", {})
            sequence_length = metadata.get("sequence_length", 0)

            if sequence_length == length:
                filtered_sequences.append(sequence)

        return filtered_sequences

    def _update_loading_progress(self, current: int, total: int, message: str):
        """Update the loading dialog with progress information."""
        if self.loading_dialog:
            self.loading_dialog.set_progress(current, total)
            self.loading_dialog.set_operation(message)
            QApplication.processEvents()

    def _show_loading_dialog(self):
        """Show the loading dialog."""
        if not self.loading_dialog:
            self.loading_dialog = SequenceCardLoadingDialog(self.sequence_card_tab)
            self.loading_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.loading_dialog.show()
            QApplication.processEvents()

    def _close_loading_dialog(self):
        """Close the loading dialog."""
        if self.loading_dialog:
            self.loading_dialog.close()
            self.loading_dialog = None
            QApplication.processEvents()

    def refresh_sequence_cards(self, length: int = None):
        """
        Refresh the sequence cards display.

        If length is specified, filter by that length.
        Otherwise, use the currently selected length from the sidebar.
        """
        # Update cursor to indicate loading
        self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)

        try:
            # If length is specified, update the sidebar selection
            if length is not None:
                self.nav_sidebar.select_length(length)

            # Load images for the selected length
            self.load_images()

            # Update the description label
            selected_length = self.nav_sidebar.selected_length
            length_text = f"{selected_length}-step" if selected_length > 0 else "all"
            self.sequence_card_tab.header.description_label.setText(
                f"Showing {length_text} sequences"
            )

        except Exception as e:
            print(f"Error refreshing sequence cards: {e}")
            import traceback

            traceback.print_exc()

            # Update the description label with error
            self.sequence_card_tab.header.description_label.setText(f"Error: {str(e)}")

        finally:
            # Reset cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)
