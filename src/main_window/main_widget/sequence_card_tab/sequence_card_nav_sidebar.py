from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QSizePolicy,
    QFrame,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QFont
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )

DEFAULT_SEQUENCE_LENGTH = 0  # 0 means show all sequences


class SequenceCardNavSidebar(QWidget):
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        super().__init__(sequence_card_tab)
        self.sequence_card_tab = sequence_card_tab
        self.selected_length = DEFAULT_SEQUENCE_LENGTH
        self.labels: dict[int, QLabel] = {}
        self._setup_scroll_area()
        self._create_labels()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self._set_styles()

    def _setup_scroll_area(self):
        """Set up the scroll area for the sidebar with improved styling."""
        self.scroll_content = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.scroll_content)
        self.layout.setSpacing(8)  # Add consistent spacing between items
        self.layout.setContentsMargins(
            5, 10, 5, 10
        )  # Add padding inside the scroll area

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)

        # Ensure scrollbar doesn't cause content to overflow
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # Make the scroll area responsive
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)

        # Improve scroll area styling
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(60, 60, 60, 0.2);
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(80, 80, 80, 0.5);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(100, 100, 100, 0.7);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """
        )

    def _create_labels(self):
        # Add a header label with improved styling
        header_label = QLabel("Sequence Length")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setBold(True)
        header_font.setPointSize(10)
        header_label.setFont(header_font)
        header_label.setStyleSheet(
            """
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #444444, stop:1 #333333);
            padding: 12px 8px;
            border-radius: 8px;
            margin-bottom: 15px;
            border: 1px solid #555555;
        """
        )
        self.layout.addWidget(header_label)

        # Add "Show All" option
        self._add_length_option(0, "Show All")

        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #555555; margin: 10px 0;")
        separator.setMaximumHeight(1)
        self.layout.addWidget(separator)

        # Add length option labels for common sequence lengths
        for length in [2, 3, 4, 5, 6, 8, 10, 12, 16]:
            self._add_length_option(length)

    def _add_length_option(self, length, label_text=None):
        """Helper method to add a length option to the sidebar with enhanced styling."""
        # Create a frame for the label with improved styling
        label_frame = QFrame()
        label_frame.setObjectName(f"lengthFrame_{length}")

        # Set minimum height to ensure consistent button sizes
        label_frame.setMinimumHeight(40)

        # Apply initial styling
        label_frame.setStyleSheet(
            """
            border-radius: 8px;
            margin: 4px 2px;
        """
        )

        # Create a layout with proper spacing
        label_layout = QHBoxLayout(label_frame)
        label_layout.setContentsMargins(8, 6, 8, 6)
        label_layout.setSpacing(0)

        # Use the provided label text or the length as a string
        display_text = label_text if label_text else f"{length}"

        # Create the label with improved styling
        label = QLabel(display_text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Make the label fill the available space
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set the click handler
        label.mousePressEvent = self.create_label_click_handler(length)

        # Add the label to the frame
        label_layout.addWidget(label)

        # Add the frame to the sidebar layout
        self.layout.addWidget(label_frame)

        # Store the label for later styling updates
        self.labels[length] = label

    def create_label_click_handler(self, length):
        def handler(_):  # Use underscore to indicate unused parameter
            self.selected_length = length
            self._update_label_styles()
            self.sequence_card_tab.refresher.refresh_sequence_cards()

        return handler

    def _update_label_styles(self):
        """Update the styles of the sidebar labels with modern effects."""
        # Use a more reasonable font size calculation
        font_size = min(max(12, self.width() // 10), 14)  # Between 12-14px

        for length, label in self.labels.items():
            # Get the parent frame
            frame = label.parent().parent()

            if length == self.selected_length:
                # Selected label style with enhanced gradient
                frame.setStyleSheet(
                    f"""
                    #lengthFrame_{length} {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #4a9efa, stop:1 #2a82da);
                        border-radius: 8px;
                        border: none;
                        margin: 4px 2px;
                    }}
                """
                )

                # Add shadow effect using QGraphicsDropShadowEffect instead of CSS
                from PyQt6.QtWidgets import QGraphicsDropShadowEffect
                from PyQt6.QtGui import QColor

                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(4)
                shadow.setColor(QColor(0, 0, 0, 76))  # 0.3 opacity = 76/255
                shadow.setOffset(0, 2)
                frame.setGraphicsEffect(shadow)

                # Selected label text style
                label.setStyleSheet(
                    f"""
                    QLabel {{
                        font-size: {font_size}px;
                        font-weight: bold;
                        color: white;
                        padding: 8px;
                    }}
                """
                )
            else:
                # Unselected label style with enhanced hover effects
                frame.setStyleSheet(
                    f"""
                    #lengthFrame_{length} {{
                        background-color: rgba(60, 60, 60, 0.3);
                        border-radius: 8px;
                        border: none;
                        margin: 4px 2px;
                    }}
                """
                )

                # Create a property animation for hover effect
                # Since we can't use CSS transitions directly, we'll use the enterEvent/leaveEvent
                # handlers in the parent class to handle hover effects

                # Unselected label text style
                label.setStyleSheet(
                    f"""
                    QLabel {{
                        font-size: {font_size}px;
                        color: #dddddd;
                        font-weight: bold;
                        padding: 8px;
                    }}
                """
                )

                # Install event filter for hover effects if not already installed
                if not frame.property("has_hover_effect"):
                    frame.setProperty("has_hover_effect", True)
                    frame.enterEvent = lambda event, f=frame: self._handle_frame_enter(
                        event, f, length
                    )
                    frame.leaveEvent = lambda event, f=frame: self._handle_frame_leave(
                        event, f, length
                    )

    def resizeEvent(self, event):
        self._set_styles()
        super().resizeEvent(event)

    def _set_styles(self):
        """Update all styles when the widget is shown or resized."""
        self._update_label_styles()

    def _handle_frame_enter(self, _, frame, length):
        """Handle mouse enter event for label frames with hover effect."""
        if length != self.selected_length:
            frame.setStyleSheet(
                f"""
                #lengthFrame_{length} {{
                    background-color: rgba(80, 80, 80, 0.5);
                    border-radius: 8px;
                    border: none;
                    margin: 4px 2px;
                }}
                """
            )

            # Update the label color
            label = self.labels[length]
            font_size = min(max(12, self.width() // 10), 14)
            label.setStyleSheet(
                f"""
                QLabel {{
                    font-size: {font_size}px;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                }}
                """
            )

    def _handle_frame_leave(self, _, frame, length):
        """Handle mouse leave event for label frames with hover effect."""
        if length != self.selected_length:
            frame.setStyleSheet(
                f"""
                #lengthFrame_{length} {{
                    background-color: rgba(60, 60, 60, 0.3);
                    border-radius: 8px;
                    border: none;
                    margin: 4px 2px;
                }}
                """
            )

            # Reset the label color
            label = self.labels[length]
            font_size = min(max(12, self.width() // 10), 14)
            label.setStyleSheet(
                f"""
                QLabel {{
                    font-size: {font_size}px;
                    color: #dddddd;
                    font-weight: bold;
                    padding: 8px;
                }}
                """
            )
