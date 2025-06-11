from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..tab import SequenceCardTab


class SequenceCardRefresher:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.nav_sidebar = sequence_card_tab.nav_sidebar
        self.currently_displayed_length = 16
        self.initialized = False

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
                self.nav_sidebar.selected_length = length

            # Use the existing load_sequences method from the tab
            self.sequence_card_tab.load_sequences()

        except Exception as e:
            # Update the description label with error
            self.sequence_card_tab.header.description_label.setText(f"Error: {str(e)}")

        finally:
            # Reset cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)
