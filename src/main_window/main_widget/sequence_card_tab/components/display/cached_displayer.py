# src/main_window/main_widget/sequence_card_tab/components/display/cached_displayer.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class PageLoaderWorker(QObject):
    """Worker thread for loading sequence card pages in the background."""

    # Signal to update progress
    progress_updated = pyqtSignal(int, int)  # current, total

    # Signal when loading is complete
    loading_complete = pyqtSignal(int)  # selected_length

    # Signal when an error occurs
    error_occurred = pyqtSignal(str)

    def __init__(self, sequence_card_tab: "SequenceCardTab", selected_length: int):
        super().__init__()
        self.sequence_card_tab = sequence_card_tab
        self.selected_length = selected_length
        self.is_cancelled = False

    def cancel(self):
        """Cancel the loading operation."""
        self.is_cancelled = True

    def run(self):
        """Load pages in the background thread."""
        try:
            # Get the cached pages
            pages_cache = self.sequence_card_tab.pages_cache

            # If we already have cached pages for this length, emit complete signal
            if self.selected_length in pages_cache:
                self.loading_complete.emit(self.selected_length)
                return

            # Otherwise, we need to load the pages from the cache manager
            # Check if refresher exists and is initialized
            if (
                not hasattr(self.sequence_card_tab, "refresher")
                or not self.sequence_card_tab.refresher
            ):
                self.error_occurred.emit("Refresher not initialized")
                return

            # Check if cache manager exists
            cache_manager = getattr(
                self.sequence_card_tab.refresher, "cache_manager", None
            )
            if not cache_manager:
                self.error_occurred.emit("Cache manager not initialized")
                return

            # Emit initial progress update
            self.progress_updated.emit(0, 100)

            # Try to load from persistent cache first
            try:
                cached_sequences = cache_manager.load_from_cache(self.selected_length)

                # Update progress
                self.progress_updated.emit(20, 100)
            except Exception as cache_error:
                self.error_occurred.emit(
                    f"Error loading from cache: {str(cache_error)}"
                )
                return

            # Check for cancellation
            if self.is_cancelled:
                return

            # If we have cached sequences, process them
            if cached_sequences:
                # Update progress
                self.progress_updated.emit(40, 100)

                # Filter sequences by length if needed
                filtered_sequences = []
                try:
                    for seq in cached_sequences:
                        # Check for cancellation periodically
                        if self.is_cancelled:
                            return

                        metadata = seq.get("metadata", {})
                        if "sequence" in metadata:
                            # Count the number of beats (excluding metadata and start position)
                            seq_length = len(metadata["sequence"]) - 2

                            # If the sequence length matches or we're showing all (length=0)
                            if (
                                seq_length == self.selected_length
                                or self.selected_length == 0
                            ):
                                filtered_sequences.append(seq)
                except Exception as filter_error:
                    self.error_occurred.emit(
                        f"Error filtering sequences: {str(filter_error)}"
                    )
                    return

                # Update progress
                self.progress_updated.emit(60, 100)

                # Check for cancellation
                if self.is_cancelled:
                    return

                # Sort sequences by word and then by filename
                if filtered_sequences:
                    try:
                        import os

                        sorted_sequences = sorted(
                            filtered_sequences,
                            key=lambda seq: (
                                seq.get("word", ""),
                                os.path.basename(seq.get("path", "")),
                            ),
                        )

                        # Update progress
                        self.progress_updated.emit(80, 100)

                        # Check for cancellation
                        if self.is_cancelled:
                            return

                        # Store the sorted sequences for the main thread to use
                        self.sequence_card_tab.filtered_sequences = sorted_sequences

                        # Update progress
                        self.progress_updated.emit(100, 100)

                        # Signal completion
                        self.loading_complete.emit(self.selected_length)
                    except Exception as sort_error:
                        self.error_occurred.emit(
                            f"Error sorting sequences: {str(sort_error)}"
                        )
                        return
                else:
                    # No sequences found for this length
                    self.error_occurred.emit(
                        f"No sequences found for length {self.selected_length}"
                    )
            else:
                # No valid cache, we need to load from the source
                # Instead of showing an error, we'll signal completion to let the main thread handle it
                self.progress_updated.emit(100, 100)
                self.loading_complete.emit(self.selected_length)

        except Exception as e:
            import traceback

            traceback.print_exc()
            self.error_occurred.emit(f"Error in PageLoaderWorker: {str(e)}")


class SequenceCardCachedPageDisplayer:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab

        # Initialize scroll_layout to None - it will be set when needed
        self.scroll_layout = None

        # Fixed margin between pages
        self.margin = 25

        # Initialize pages_cache to empty dict - it will be updated when needed
        self.pages_cache = {}

        # Thread and worker for background loading
        self.thread = None
        self.worker = None

        # Progress indicator
        self.progress_bar = None

    def __del__(self):
        """Clean up resources when the object is destroyed."""
        self._cancel_background_thread()

    def display_cached_pages(self, selected_length: int):
        """
        Display the cached pages without recalculating.

        This method now uses background threading to avoid UI freezing.
        """
        # Make sure we have the latest references
        self.scroll_layout = self.sequence_card_tab.scroll_layout
        self.pages_cache = self.sequence_card_tab.pages_cache

        # Show loading indicator
        self._show_loading_indicator()

        # If we already have the pages cached in memory, display them immediately
        if selected_length in self.pages_cache:
            self._display_pages_from_cache(selected_length)
            return

        # Otherwise, start background loading
        self._start_background_loading(selected_length)

    def _display_pages_from_cache(self, selected_length: int):
        """Display pages from the in-memory cache."""
        # Always get the latest reference to scroll_layout
        self.scroll_layout = self.sequence_card_tab.scroll_layout

        # If scroll_layout is still None or not accessible, create a debug message and try to fix
        if not self.scroll_layout:
            print("ERROR: scroll_layout is not available yet - attempting to fix")

            # Check if scroll_content exists and try to recreate the layout
            if hasattr(self.sequence_card_tab, "scroll_content"):
                print("Recreating scroll_layout on existing scroll_content")
                self.sequence_card_tab.scroll_layout = QVBoxLayout(
                    self.sequence_card_tab.scroll_content
                )
                self.sequence_card_tab.scroll_layout.setAlignment(
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
                )
                self.sequence_card_tab.scroll_layout.setSpacing(20)
                self.sequence_card_tab.scroll_layout.setContentsMargins(10, 20, 10, 20)
                self.scroll_layout = self.sequence_card_tab.scroll_layout
            else:
                print(
                    "CRITICAL ERROR: Cannot display pages - scroll_content not available"
                )
                return

        # Make sure we have the latest pages_cache
        self.pages_cache = self.sequence_card_tab.pages_cache

        # Verify the selected length exists in the cache
        if selected_length not in self.pages_cache:
            print(f"No cached pages found for length {selected_length}")
            return

        # Clear the scroll layout
        self._clear_scroll_layout()

        # Hide loading indicator if it exists
        if self.progress_bar:
            self.progress_bar.setParent(None)
            self.progress_bar = None

        # Calculate the available width for two pages side by side
        scroll_area_width = self.sequence_card_tab.scroll_area.width()
        nav_sidebar_width = self.sequence_card_tab.nav_sidebar.width()
        available_width = (
            scroll_area_width - nav_sidebar_width - 40
        )  # Account for margins

        # Calculate the width for each page (A4 aspect ratio: 8.5:11)
        page_width = (available_width - self.margin) // 2
        page_height = int(page_width * 11 / 8.5)  # Maintain A4 aspect ratio

        # Update the page dimensions for all cached pages
        for page in self.pages_cache[selected_length]:
            page.setFixedSize(page_width, page_height)

        # Add cached pages back into the scroll layout
        for i in range(0, len(self.pages_cache[selected_length]), 2):
            # Create a new row layout for each pair of pages
            row_layout = QHBoxLayout()
            row_layout.setSpacing(self.margin)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            for j in range(2):  # Only add up to two items per row
                if i + j < len(self.pages_cache[selected_length]):
                    page_widget = self.pages_cache[selected_length][i + j]
                    row_layout.addWidget(page_widget)

            self.scroll_layout.addLayout(row_layout)

        # Update the current pages reference
        self.sequence_card_tab.pages = self.pages_cache[selected_length]

        # Force update
        self.sequence_card_tab.scroll_content.update()

    def _start_background_loading(self, selected_length: int):
        """Start background loading of sequence card pages."""
        # Cancel any existing thread
        self._cancel_background_thread()

        # Create a new thread and worker
        self.thread = QThread()
        self.worker = PageLoaderWorker(self.sequence_card_tab, selected_length)

        # Move the worker to the thread
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.thread.started.connect(self.worker.run)
        self.worker.progress_updated.connect(self._update_loading_progress)
        self.worker.loading_complete.connect(self._on_loading_complete)
        self.worker.error_occurred.connect(self._on_loading_error)

        # Start the thread
        self.thread.start()

    def _cancel_background_thread(self):
        """Cancel any running background thread."""
        if self.thread and self.thread.isRunning():
            if self.worker:
                self.worker.cancel()
            self.thread.quit()
            self.thread.wait()

    def _show_loading_indicator(self):
        """Show a loading progress bar."""
        # Make sure we have the latest reference to the scroll layout
        if not self.scroll_layout and hasattr(self.sequence_card_tab, "scroll_layout"):
            self.scroll_layout = self.sequence_card_tab.scroll_layout

        # If scroll_layout is still None or not accessible, return early
        if not self.scroll_layout:
            print("Warning: scroll_layout is not available yet")
            return

        # Clear the scroll layout first
        self._clear_scroll_layout()

        # Create a progress bar if it doesn't exist
        if not self.progress_bar:
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            self.progress_bar.setTextVisible(True)
            self.progress_bar.setFormat("Loading sequence cards... %p%")
            self.progress_bar.setMinimumWidth(300)
            self.progress_bar.setStyleSheet(
                """
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    text-align: center;
                    height: 25px;
                    background-color: #f0f0f0;
                }
                QProgressBar::chunk {
                    background-color: #2a82da;
                    border-radius: 5px;
                }
                """
            )

            # Add to the scroll layout
            self.scroll_layout.addWidget(
                self.progress_bar, 0, Qt.AlignmentFlag.AlignCenter
            )

    def _update_loading_progress(self, current: int, total: int):
        """Update the loading progress bar."""
        if self.progress_bar:
            self.progress_bar.setValue(int((current / total) * 100))

    def _on_loading_complete(self, selected_length: int):
        """Handle completion of background loading."""
        # Clean up the thread
        self._cancel_background_thread()

        # Check if we have filtered sequences to display
        if (
            hasattr(self.sequence_card_tab, "filtered_sequences")
            and self.sequence_card_tab.filtered_sequences
        ):
            # If we have filtered sequences, we need to display them
            # This would normally be done by the image_displayer, but we'll handle it here

            # First, check if we already have cached pages for this length
            if selected_length in self.sequence_card_tab.pages_cache:
                # If we do, just display them
                self._display_pages_from_cache(selected_length)
            else:
                # Otherwise, we need to tell the image displayer to create the pages
                self.sequence_card_tab.image_displayer.display_sequences(
                    self.sequence_card_tab.filtered_sequences
                )

                # After the image displayer has created the pages, they should be cached
                # So we can display them from the cache
                if selected_length in self.sequence_card_tab.pages_cache:
                    self._display_pages_from_cache(selected_length)
                else:
                    # If they're still not cached, something went wrong
                    self._on_loading_error("Failed to create pages for display")
        else:
            # If we don't have filtered sequences, try to display from cache
            # This might happen if the worker found that the pages were already cached
            self._display_pages_from_cache(selected_length)

    def _on_loading_error(self, error_message: str):
        """Handle errors during background loading."""
        print(f"Error loading sequence card pages: {error_message}")

        # Clean up the thread
        self._cancel_background_thread()

        # Hide the progress bar
        if self.progress_bar:
            self.progress_bar.setParent(None)
            self.progress_bar = None

        # Make sure we have the latest reference to the scroll layout
        if not self.scroll_layout and hasattr(self.sequence_card_tab, "scroll_layout"):
            self.scroll_layout = self.sequence_card_tab.scroll_layout

        # If scroll_layout is still None or not accessible, return early
        if not self.scroll_layout:
            print("Warning: scroll_layout is not available yet")
            return

        # Show an error message in the scroll area
        error_label = QLabel(f"Error loading sequence cards: {error_message}")
        error_label.setStyleSheet("color: red; font-weight: bold; padding: 20px;")
        self.scroll_layout.addWidget(error_label, 0, Qt.AlignmentFlag.AlignCenter)

    def _clear_scroll_layout(self):
        """Helper method to clear all widgets from the scroll layout."""
        # Always get the latest reference to scroll_layout
        self.scroll_layout = self.sequence_card_tab.scroll_layout

        # If scroll_layout is still None or not accessible, try to fix it
        if not self.scroll_layout:
            print(
                "ERROR: scroll_layout is not available in _clear_scroll_layout - attempting to fix"
            )

            # Check if scroll_content exists and try to recreate the layout
            if hasattr(self.sequence_card_tab, "scroll_content"):
                print("Recreating scroll_layout on existing scroll_content")

                # First, remove any existing layout
                if self.sequence_card_tab.scroll_content.layout():
                    old_layout = self.sequence_card_tab.scroll_content.layout()
                    while old_layout.count():
                        item = old_layout.takeAt(0)
                        if item.widget():
                            item.widget().setParent(None)

                    # Delete the old layout
                    old_layout.setParent(None)

                # Create a new layout
                self.sequence_card_tab.scroll_layout = QVBoxLayout(
                    self.sequence_card_tab.scroll_content
                )
                self.sequence_card_tab.scroll_layout.setAlignment(
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
                )
                self.sequence_card_tab.scroll_layout.setSpacing(20)
                self.sequence_card_tab.scroll_layout.setContentsMargins(10, 20, 10, 20)
                self.scroll_layout = self.sequence_card_tab.scroll_layout
                return  # Layout is now empty, no need to clear further
            else:
                print(
                    "CRITICAL ERROR: Cannot clear layout - scroll_content not available"
                )
                return

        # Clear all items from the layout
        try:
            while self.scroll_layout.count():
                layout_item = self.scroll_layout.takeAt(0)
                if not layout_item:
                    continue

                widget = layout_item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    sub_layout = layout_item.layout()
                    if sub_layout is not None:
                        while sub_layout.count():
                            sub_item = sub_layout.takeAt(0)
                            if not sub_item:
                                continue

                            sub_widget = sub_item.widget()
                            if sub_widget is not None:
                                sub_widget.setParent(None)
        except Exception as e:
            print(f"Error clearing scroll layout: {e}")

            # Try a more aggressive approach if the normal clearing fails
            try:
                if hasattr(self.sequence_card_tab, "scroll_content"):
                    # Create a completely new widget and layout
                    old_content = self.sequence_card_tab.scroll_content
                    new_content = QWidget()
                    self.sequence_card_tab.scroll_layout = QVBoxLayout(new_content)
                    self.sequence_card_tab.scroll_layout.setAlignment(
                        Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
                    )
                    self.sequence_card_tab.scroll_layout.setSpacing(20)
                    self.sequence_card_tab.scroll_layout.setContentsMargins(
                        10, 20, 10, 20
                    )

                    # Replace the old content with the new one
                    self.sequence_card_tab.scroll_area.setWidget(new_content)
                    self.sequence_card_tab.scroll_content = new_content
                    self.scroll_layout = self.sequence_card_tab.scroll_layout

                    # Clean up the old content
                    old_content.setParent(None)
            except Exception as e2:
                print(f"Critical error recreating scroll layout: {e2}")
