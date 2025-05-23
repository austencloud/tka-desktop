# src/main_window/main_widget/sequence_card_tab/components/display/scroll_area.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QFrame, QWidget
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QWheelEvent

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class SequenceCardScrollArea(QScrollArea):
    """
    Enhanced scroll area for sequence cards with smooth scrolling and better performance.
    """
    
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        super().__init__(sequence_card_tab)
        self.sequence_card_tab = sequence_card_tab
        
        # Configure scroll area
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Enable smooth scrolling
        self.setProperty("smoothScroll", True)
        
        # Apply styling
        self.setStyleSheet("""
            QScrollArea {
                background-color: #f8f9fa;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(0,0,0,0.1);
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0,0,0,0.3);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0,0,0,0.5);
            }
        """)
        
        # Install event filter for smooth scrolling
        self.viewport().installEventFilter(self)
    
    def eventFilter(self, obj: QWidget, event: QEvent) -> bool:
        """
        Event filter for smooth scrolling.
        
        This intercepts wheel events and makes scrolling smoother.
        """
        if obj is self.viewport() and event.type() == QEvent.Type.Wheel:
            wheel_event = QWheelEvent(event)
            
            # Get current scroll position
            scroll_bar = self.verticalScrollBar()
            current_value = scroll_bar.value()
            
            # Calculate smooth scroll amount
            delta = wheel_event.angleDelta().y()
            smooth_delta = delta // 2  # Reduce scroll speed by half for smoother scrolling
            
            # Apply smooth scroll
            scroll_bar.setValue(current_value - smooth_delta)
            
            # Consume the event
            return True
            
        # Let other events pass through
        return super().eventFilter(obj, event)
    
    def setWidget(self, widget: QWidget) -> None:
        """
        Set the widget for the scroll area with optimized settings.
        """
        super().setWidget(widget)
        
        # Apply optimizations to the widget
        if widget:
            # REDUCED MARGINS: Significantly reduced from (10, 20, 10, 20) to minimal margins
            widget.setContentsMargins(2, 5, 2, 5)  # left, top, right, bottom
            
            # Enable attribute to improve scrolling performance
            widget.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
            
            # Set background for better appearance
            widget.setStyleSheet("""
                background-color: #f8f9fa;
                border: none;
            """)
    
    def resizeEvent(self, event):
        """
        Handle resize events with optimized layout updates.
        """
        super().resizeEvent(event)
        
        # Notify the tab that a resize occurred
        if hasattr(self.sequence_card_tab, 'on_scroll_area_resize'):
            self.sequence_card_tab.on_scroll_area_resize()