from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QApplication,
    QToolTip,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from typing import Optional, Dict, Callable
import json


class ModernWorkbenchButton(QPushButton):
    def __init__(
        self,
        text: str = "",
        icon_path: str = "",
        tooltip: str = "",
        callback: Optional[Callable] = None,
    ):
        super().__init__()

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_appearance()

        if text:
            self.setText(text)
        if icon_path:
            self.setIcon(QIcon(icon_path))
        if tooltip:
            self.setToolTip(tooltip)
        if callback:
            self.clicked.connect(callback)

    def _setup_appearance(self):
        self.setStyleSheet(
            """
            ModernWorkbenchButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 8px;
                color: white;
                font-weight: 500;
            }
            ModernWorkbenchButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            ModernWorkbenchButton:pressed {
                background: rgba(255, 255, 255, 0.3);
            }
        """
        )

    def update_size(self, size: int):
        self.setFixedSize(size, size)
        if self.icon():
            self.setIconSize(self.size() * 0.6)


class ModernSequenceWorkbenchButtonPanel(QFrame):
    # Signals for workbench integration
    add_to_dictionary_requested = pyqtSignal()
    save_image_requested = pyqtSignal()
    view_fullscreen_requested = pyqtSignal()
    mirror_sequence_requested = pyqtSignal()
    swap_colors_requested = pyqtSignal()
    rotate_sequence_requested = pyqtSignal()
    copy_json_requested = pyqtSignal()
    delete_beat_requested = pyqtSignal()
    clear_sequence_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._buttons: Dict[str, ModernWorkbenchButton] = {}
        self._spacers: list = []
        self._colors_swapped = False

        self._setup_appearance()
        self._create_buttons()
        self._setup_layout()

    def _setup_appearance(self):
        self.setStyleSheet(
            """
            ModernSequenceWorkbenchButtonPanel {
                background: rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin: 8px;
            }
        """
        )
        self.setMaximumWidth(80)
        self.setMinimumWidth(60)

    def _create_buttons(self):
        """Create all workbench buttons with modern styling"""
        button_config = {
            # Dictionary & Export Tools
            "add_to_dictionary": {
                "text": "📚",
                "tooltip": "Add to Dictionary",
                "callback": self._handle_add_to_dictionary,
            },
            "save_image": {
                "text": "💾",
                "tooltip": "Save Image",
                "callback": self._handle_save_image,
            },
            "view_fullscreen": {
                "text": "👁️",
                "tooltip": "View Full Screen",
                "callback": self._handle_view_fullscreen,
            },
            # Transform Tools
            "mirror_sequence": {
                "text": "🪞",
                "tooltip": "Mirror Sequence",
                "callback": self._handle_mirror_sequence,
            },
            "swap_colors": {
                "text": "☯️",
                "tooltip": "Swap Colors",
                "callback": self._handle_swap_colors,
            },
            "rotate_sequence": {
                "text": "🔄",
                "tooltip": "Rotate Sequence",
                "callback": self._handle_rotate_sequence,
            },
            # Sequence Management
            "copy_json": {
                "text": "📋",
                "tooltip": "Copy Sequence JSON",
                "callback": self._handle_copy_json,
            },
            "delete_beat": {
                "text": "🗑️",
                "tooltip": "Delete Selected Beat",
                "callback": self._handle_delete_beat,
            },
            "clear_sequence": {
                "text": "🧹",
                "tooltip": "Clear All Beats",
                "callback": self._handle_clear_sequence,
            },
        }

        for name, config in button_config.items():
            button = ModernWorkbenchButton(
                text=config["text"],
                tooltip=config["tooltip"],
                callback=config["callback"],
            )

            # Enhanced emoji font for better visibility
            font = button.font()
            font.setPointSize(16)
            button.setFont(font)

            self._buttons[name] = button

    def _setup_layout(self):
        """Setup vertical layout with grouped buttons"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 12, 8, 12)

        # Top spacer
        layout.addItem(
            QSpacerItem(
                20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Group 1: Dictionary & Export Tools
        self._add_button_group(
            layout, ["add_to_dictionary", "save_image", "view_fullscreen"]
        )

        # Group separator
        self._add_group_separator(layout)

        # Group 2: Transform Tools
        self._add_button_group(
            layout, ["mirror_sequence", "swap_colors", "rotate_sequence"]
        )

        # Group separator
        self._add_group_separator(layout)

        # Group 3: Sequence Management
        self._add_button_group(layout, ["copy_json", "delete_beat", "clear_sequence"])

        # Bottom spacer
        layout.addItem(
            QSpacerItem(
                20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

    def _add_button_group(self, layout: QVBoxLayout, button_names: list):
        """Add a group of buttons to the layout"""
        for name in button_names:
            if name in self._buttons:
                layout.addWidget(self._buttons[name])

    def _add_group_separator(self, layout: QVBoxLayout):
        """Add spacing between button groups"""
        spacer = QSpacerItem(
            20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        layout.addItem(spacer)
        self._spacers.append(spacer)

    # Button event handlers
    def _handle_add_to_dictionary(self):
        self.add_to_dictionary_requested.emit()

    def _handle_save_image(self):
        self.save_image_requested.emit()

    def _handle_view_fullscreen(self):
        self.view_fullscreen_requested.emit()

    def _handle_mirror_sequence(self):
        self.mirror_sequence_requested.emit()

    def _handle_swap_colors(self):
        self._toggle_color_swap_icon()
        self.swap_colors_requested.emit()

    def _handle_rotate_sequence(self):
        self.rotate_sequence_requested.emit()

    def _handle_copy_json(self):
        self.copy_json_requested.emit()

    def _handle_delete_beat(self):
        self.delete_beat_requested.emit()

    def _handle_clear_sequence(self):
        self.clear_sequence_requested.emit()

    def _toggle_color_swap_icon(self):
        """Toggle between color swap states"""
        swap_button = self._buttons.get("swap_colors")
        if swap_button:
            if self._colors_swapped:
                swap_button.setText("☯️")  # Normal yin-yang
            else:
                swap_button.setText("⚫")  # Alternative representation
            self._colors_swapped = not self._colors_swapped

    def update_button_sizes(self, base_size: int):
        """Update all button sizes based on parent size"""
        button_size = max(40, min(60, base_size // 20))

        for button in self._buttons.values():
            button.update_size(button_size)

            # Update font size for emoji visibility
            font = button.font()
            font.setPointSize(max(12, button_size // 3))
            button.setFont(font)

    def get_button(self, name: str) -> Optional[ModernWorkbenchButton]:
        """Get a specific button by name"""
        return self._buttons.get(name)

    def set_button_enabled(self, name: str, enabled: bool):
        """Enable/disable a specific button"""
        button = self._buttons.get(name)
        if button:
            button.setEnabled(enabled)

    def show_message_tooltip(
        self, button_name: str, message: str, duration: int = 2000
    ):
        """Show a temporary tooltip message on a button"""
        button = self._buttons.get(button_name)
        if button:
            original_tooltip = button.toolTip()
            button.setToolTip(message)

            # Reset tooltip after duration
            def reset_tooltip():
                button.setToolTip(original_tooltip)

            from PyQt6.QtCore import QTimer

            QTimer.singleShot(duration, reset_tooltip)

    def resizeEvent(self, event):
        """Handle resize events to maintain responsive design"""
        super().resizeEvent(event)

        # Update button sizes based on new panel size
        panel_height = self.height()
        self.update_button_sizes(panel_height)
