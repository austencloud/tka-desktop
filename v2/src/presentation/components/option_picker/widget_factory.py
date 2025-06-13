from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt

from ....core.dependency_injection.simple_container import SimpleContainer
from ....core.interfaces.core_services import ILayoutService
from .option_picker_widget import ModernOptionPickerWidget
from .option_picker_filter import OptionPickerFilter


class OptionPickerWidgetFactory:
    """Factory for creating and configuring the option picker widget"""

    def __init__(self, container: SimpleContainer):
        self.container = container
        self._layout_service: Optional[ILayoutService] = None

    def create_widget(
        self, resize_callback=None
    ) -> tuple[QWidget, QWidget, QVBoxLayout, OptionPickerFilter]:
        """Create the main option picker widget with all components"""
        self._layout_service = self.container.resolve(ILayoutService)

        widget = ModernOptionPickerWidget()
        if resize_callback:
            widget.set_resize_callback(resize_callback)
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        widget.setMinimumSize(600, 800)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Add filter widget
        filter_widget = OptionPickerFilter()
        layout.addWidget(filter_widget.widget)

        # Create scroll area and sections container
        scroll_area, sections_container, sections_layout = self._create_scroll_area()
        layout.addWidget(scroll_area, 1)

        # Apply styling
        self._apply_styling(widget)

        return widget, sections_container, sections_layout, filter_widget

    def _create_scroll_area(self) -> tuple[QScrollArea, QWidget, QVBoxLayout]:
        """Create the scroll area and sections container"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )  # Prevent horizontal overflow
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        sections_container = QWidget()
        sections_layout = QVBoxLayout(sections_container)
        sections_layout.setContentsMargins(5, 5, 5, 5)  # Minimal margins
        sections_layout.setSpacing(10)  # Reduced spacing between sections
        sections_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        sections_container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        scroll_area.setWidget(sections_container)
        return scroll_area, sections_container, sections_layout

    def _apply_styling(self, widget: QWidget) -> None:
        """Apply CSS styling to the widget"""
        widget.setStyleSheet(
            """
            QWidget {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """
        )

    def get_size(self) -> tuple[int, int]:
        """Get the recommended widget size"""
        if self._layout_service:
            picker_size = self._layout_service.get_picker_size()
            return (picker_size.width(), picker_size.height())
        return (600, 800)
