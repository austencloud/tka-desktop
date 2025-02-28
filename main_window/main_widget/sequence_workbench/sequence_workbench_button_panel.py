from datetime import datetime
import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QStandardPaths, QFileInfo
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QPushButton,
    QFrame,
    QVBoxLayout,
    QApplication,
    QSpacerItem,
    QSizePolicy,
    QFileDialog,
)

from main_window.main_widget.sequence_workbench.workbench_button import WorkbenchButton
from .button_panel_placeholder import ButtonPanelPlaceholder
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from .sequence_workbench import SequenceWorkbench


class SequenceWorkbenchButtonPanel(QFrame):
    swap_colors_button: QPushButton
    colors_swapped = False
    spacers: list[QSpacerItem] = []

    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        super().__init__(sequence_workbench)
        self.sequence_workbench = sequence_workbench
        self.main_widget = self.sequence_workbench.main_widget
        self.beat_frame = self.sequence_workbench.sequence_beat_frame
        self.export_manager = self.beat_frame.image_export_manager
        self.indicator_label = self.sequence_workbench.indicator_label

        self.font_size = self.sequence_workbench.width() // 45

        self.top_placeholder = ButtonPanelPlaceholder(self)
        self.bottom_placeholder = ButtonPanelPlaceholder(self)

        self._setup_buttons()
        self._setup_layout()

    def _setup_buttons(self) -> None:
        self.buttons: dict[str, WorkbenchButton] = {}

        button_dict = {
            "add_to_dictionary": {
                "icon": "add_to_dictionary.svg",
                "callback": self.sequence_workbench.add_to_dictionary_ui.add_to_dictionary,
                "tooltip": "Add to Dictionary",
            },
            "save_image": {
                "icon": "save_image.svg",
                "callback": self.export_image_directly,
                "tooltip": "Save Image",
            },
            "view_full_screen": {
                "icon": "eye.png",
                "callback": lambda: self.sequence_workbench.full_screen_viewer.view_full_screen(),
                "tooltip": "View Full Screen",
            },
            "mirror_sequence": {
                "icon": "mirror.png",
                "callback": lambda: self.sequence_workbench.mirror_manager.reflect_current_sequence(),
                "tooltip": "Mirror Sequence",
            },
            "swap_colors": {
                "icon": "yinyang1.svg",
                "callback": lambda: self.sequence_workbench.color_swap_manager.swap_current_sequence(),
                "tooltip": "Swap Colors",
            },
            "rotate_sequence": {
                "icon": "rotate.svg",
                "callback": lambda: self.sequence_workbench.rotation_manager.rotate_current_sequence(),
                "tooltip": "Rotate Sequence",
            },
            "delete_beat": {
                "icon": "delete.svg",
                "callback": lambda: self.sequence_workbench.beat_deleter.delete_selected_beat(),
                "tooltip": "Delete Beat",
            },
            "clear_sequence": {
                "icon": "clear.svg",
                "callback": lambda: self.clear_sequence(),
                "tooltip": "Clear Sequence",
            },
        }

        for button_name, button_data in button_dict.items():
            icon_path = get_images_and_data_path(
                f"images/icons/sequence_workbench_icons/{button_data['icon']}"
            )
            button = self._create_button(
                icon_path, button_data["callback"], button_data["tooltip"]
            )
            setattr(self, f"{button_name}_button", button)
            self.buttons[button_name] = button

    def clear_sequence(self):
        sequence_length = len(
            self.main_widget.json_manager.loader_saver.load_current_sequence()
        )
        # collapse the grpah editor
        graph_editor = self.sequence_workbench.graph_editor
        if sequence_length < 2:
            self.indicator_label.show_message("No sequence to clear")
            return
        if graph_editor.is_toggled:
            graph_editor.animator.toggle()
        self.sequence_workbench.indicator_label.show_message("Sequence cleared")
        self.beat_frame.sequence_workbench.beat_deleter.start_position_deleter.delete_all_beats(
            show_indicator=True
        )

    def _create_button(self, icon_path: str, callback, tooltip: str) -> WorkbenchButton:
        button_size = self.sequence_workbench.main_widget.height() // 20  # Initial size
        button = WorkbenchButton(icon_path, tooltip, callback, button_size)
        return button

    def toggle_swap_colors_icon(self):
        icon_name = "yinyang1.svg" if self.colors_swapped else "yinyang2.svg"
        new_icon_path = get_images_and_data_path(
            f"images/icons/sequence_workbench_icons/{icon_name}"
        )
        self.colors_swapped = not self.colors_swapped
        new_icon = QIcon(new_icon_path)
        self.swap_colors_button.setIcon(new_icon)
        QApplication.processEvents()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.top_placeholder)

        # Group 1 (Basic Tools)
        for name in ["add_to_dictionary", "save_image", "view_full_screen"]:
            self.layout.addWidget(self.buttons[name])

        # Add spacing to separate groups
        self.spacer1 = QSpacerItem(
            20,
            self.sequence_workbench.height() // 20,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )
        self.layout.addItem(self.spacer1)

        # Group 2 (Transform Tools)
        for name in ["mirror_sequence", "swap_colors", "rotate_sequence"]:
            self.layout.addWidget(self.buttons[name])

        # Add spacing before next group
        self.spacer2 = QSpacerItem(
            20,
            self.sequence_workbench.height() // 20,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )
        self.layout.addItem(self.spacer2)

        # Group 3 (Sequence Management)
        for name in ["delete_beat", "clear_sequence"]:
            self.layout.addWidget(self.buttons[name])

        self.layout.addWidget(self.bottom_placeholder)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Initial spacing setup
        self.spacer3 = QSpacerItem(
            20,
            self.sequence_workbench.height() // 40,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )
        self.layout.addItem(self.spacer3)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.resize_button_panel()

    def resize_button_panel(self):
        button_size = self.sequence_workbench.main_widget.height() // 20
        for button in self.buttons.values():
            button.update_size(button_size)

        self.layout.setSpacing(
            self.sequence_workbench.sequence_beat_frame.main_widget.height() // 120
        )

        spacer_size = (
            self.sequence_workbench.sequence_beat_frame.main_widget.height() // 20
        )
        for spacer in self.spacers:
            spacer.changeSize(
                20,
                spacer_size,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        self.layout.update()

    def export_image_directly(self):
        """Immediately exports the image using current settings and opens the save dialog."""
        sequence = (
            self.sequence_workbench.main_widget.json_manager.loader_saver.load_current_sequence()
        )

        if len(sequence) < 3:
            self.sequence_workbench.indicator_label.show_message(
                "The sequence is empty."
            )
            return

        # Retrieve the export settings
        settings_manager = self.sequence_workbench.main_widget.settings_manager
        options = settings_manager.image_export.get_all_image_export_options()
        
        options["user_name"] = settings_manager.users.get_current_user()
        options["notes"] = settings_manager.users.get_current_note()
        options["export_date"] = datetime.now().strftime("%m-%d-%Y")
        
        # Generate the image
        image_creator = self.export_manager.image_creator
        sequence_image = image_creator.create_sequence_image(
            sequence,
            options,
        )



        # Save the image
        self.export_manager.image_saver.save_image(sequence_image)
        # open the folder containing the image

        self.sequence_workbench.indicator_label.show_message(
            "Image saved successfully!"
        )

