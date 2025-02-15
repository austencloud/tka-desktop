from typing import TYPE_CHECKING
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabUIUpdater:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab

        self.settings_manager = browse_tab.main_widget.main_window.settings_manager
        self.font_color_updater = browse_tab.main_widget.font_color_updater

    def update_and_display_ui(self, total_sequences: int):
        if total_sequences == 0:
            total_sequences = 1

        # Show and reset the progress bar
        self.browse_tab.sequence_picker.progress_bar.setVisible(True)
        self.browse_tab.sequence_picker.progress_bar.set_value(0)
        QApplication.processEvents()

        # For easier reading
        displayed_sequences = (
            self.browse_tab.sequence_picker.currently_displayed_sequences
        )
        n = total_sequences

        def update_ui():
            ###############################################
            # PHASE 1: Create all thumbnail boxes (0→50%)
            ###############################################
            for i, (word, thumbnails, _) in enumerate(displayed_sequences):
                row_index = i // self.browse_tab.sequence_picker.sorter.num_columns
                column_index = i % self.browse_tab.sequence_picker.sorter.num_columns

                # Create box but skip the immediate 'update_thumbnail'
                self.browse_tab.sequence_picker.sorter.add_thumbnail_box(
                    row_index,
                    column_index,
                    word,
                    thumbnails,
                    hidden=False,  # or True if you prefer to show them later
                    skip_image=True,  # new parameter
                )

                # Update progress bar from 0%→50%
                fraction = (i + 1) / n  # e.g. 0.0..1.0
                progress_val = int(fraction * 50)  # scale to 0..50
                self.browse_tab.sequence_picker.progress_bar.set_value(progress_val)

                # Let the GUI remain responsive
                QApplication.processEvents()

            ###############################################
            # PHASE 2: Scale each thumbnail (50%→100%)
            ###############################################
            # At this point, all boxes exist in self.scroll_widget.thumbnail_boxes
            boxes = list(
                self.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.values()
            )
            num_boxes = len(boxes)

            for j, tb in enumerate(boxes):
                # Actually do the scaling now:
                # We call the same method that was skipped above.
                tb.image_label.update_thumbnail(tb.state.current_index)

                # Update progress from 50%→100%
                fraction = (j + 1) / num_boxes
                progress_val = 50 + int(fraction * 50)
                self.browse_tab.sequence_picker.progress_bar.set_value(progress_val)

                QApplication.processEvents()

            # Hide progress bar, do final styling, restore cursor
            self.browse_tab.sequence_picker.progress_bar.setVisible(False)
            self._apply_sorting_and_styling()
            QApplication.restoreOverrideCursor()

        QTimer.singleShot(0, update_ui)

    def _apply_sorting_and_styling(self):
        """Apply sorting to thumbnails and style elements based on current settings."""
        self.browse_tab.sequence_picker.sorter.sort_and_display_currently_filtered_sequences_by_method(
            self.settings_manager.browse_settings.get_sort_method()
        )

        font_color = self.font_color_updater.get_font_color(
            self.settings_manager.global_settings.get_background_type()
        )

        for (
            thumbnail_box
        ) in self.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.values():
            thumbnail_box.word_label.setStyleSheet(f"color: {font_color};")
            thumbnail_box.word_label.star_icon_empty_path = (
                "star_empty_white.png"
                if font_color == "white"
                else "star_empty_black.png"
            )
            thumbnail_box.word_label.reload_favorite_icon()
            thumbnail_box.variation_number_label.setStyleSheet(f"color: {font_color};")
