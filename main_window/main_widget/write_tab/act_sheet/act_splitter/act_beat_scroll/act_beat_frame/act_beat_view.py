# act_tab_beat.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QGraphicsTextItem, QMenu
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QFont, QAction

from main_window.main_widget.sequence_workbench.sequence_beat_frame.act_beat import (
    ActBeat,
)

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.act_sheet.act_splitter.act_beat_scroll.act_beat_frame.act_beat_frame import (
        ActBeatFrame,
    )

# act_tab_beat.py
from PyQt6.QtWidgets import QGraphicsView, QGraphicsTextItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QFont


class ActBeatView(QGraphicsView):
    def __init__(self, beat_frame: "ActBeatFrame", beat_number=None):
        super().__init__()
        self.beat_frame = beat_frame
        self.is_filled = False
        self.beat_number = beat_number  # Beat number to display
        self.beat = ActBeat(beat_frame, 1)
        self.setScene(self.beat)
        self.beat_number_item = None
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: none; border: 1px solid black;")

        # Disable both scrollbars
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Prevent scrolling by disabling scrolling behavior
        self.setInteractive(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def is_populated(self) -> bool:
        """Check if this beat view has been populated with any data."""
        return bool(self.beat.letter)  # or another attribute indicating population

    def extract_metadata(self):
        """Extract beat data for saving in act JSON."""
        return {
            "beat_number": self.get_beat_number_in_act_beat_frame(),
            "pictograph_data": self.beat.state.pictograph_data,
        }

    def get_beat_number_in_act_beat_frame(self):
        """Get the beat number in the act beat frame."""
        return self.beat_frame.get.beat_number(self)

    def show_context_menu(self, position):
        menu = QMenu()
        test_action = QAction("Test", self)
        menu.addAction(test_action)
        menu.exec(self.mapToGlobal(position))

    def add_beat_number(self, beat_number_text=None):
        """Display the beat number."""
        self.beat_number_text = beat_number_text
        if not beat_number_text:
            self.beat_number_text = str(self.beat_number) if self.beat_number else "N/A"

        if self.beat_number_item:
            self.beat.removeItem(self.beat_number_item)

        self.beat_number_item = QGraphicsTextItem(str(self.beat_number_text))
        self.beat_number_item.setFont(QFont("Georgia", 80, QFont.Weight.DemiBold))
        self.beat_number_item.setPos(
            QPointF(
                self.beat_number_item.boundingRect().height() // 3,
                self.beat_number_item.boundingRect().height() // 5,
            )
        )
        self.scene().addItem(self.beat_number_item)
        self.beat_number_item.setVisible(True)  # Ensure visibility

    def remove_beat_number(self):
        if self.beat_number_item:
            self.beat_number_item.setVisible(False)

    def resizeEvent(self, event):
        """Resize the beat view to fit the container."""
        size = self.beat_frame.beat_size
        self.setFixedSize(size, size)

        # Rescale the beat view to fit the container
        beat_scene_size = (950, 950)
        view_size = self.size()

        self.view_scale = min(
            view_size.width() / beat_scene_size[0],
            view_size.height() / beat_scene_size[1],
        )
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def clear_beat(self):
        """Clear the beat from the view."""
        self.beat.clear()

    def wheelEvent(self, event):
        """Override to prevent scrolling."""
        self.beat_frame.wheelEvent(event)
