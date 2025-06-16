from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QCheckBox,
    QFrame,
    QPushButton,
)
from PyQt6.QtCore import pyqtSignal

from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab_button import (
    ImageExportTabButton,
)
from main_window.main_widget.settings_dialog.ui.image_export.pictograph_dataset_exporter import (
    PictographDatasetExporter,
)


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )
    from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager


class ImageExportControlPanel(QWidget):
    """
    A control panel for configuring image export settings.
    """

    settingChanged = pyqtSignal()

    def __init__(
        self,
        settings_manager: "LegacySettingsManager",
        image_export_tab: "ImageExportTab",
    ):
        super().__init__(image_export_tab)
        self.image_export_tab = image_export_tab
        self.settings_manager = settings_manager
        self.user_combo_box = QComboBox()
        self.note_input = QLineEdit()  # Single text field for notes
        self.save_dir_checkbox = QCheckBox("Remember last save directory")
        self.save_dir_checkbox.setToolTip(
            "When enabled, the file dialog will open in the last directory where an image was saved"
        )

        # Create the export all pictographs button
        self.export_all_pictographs_button = QPushButton("Export All Pictographs")
        self.export_all_pictographs_button.setToolTip(
            "Export all pictographs from the dataset as individual images, organized by grid mode and letter"
        )
        self.pictograph_exporter = PictographDatasetExporter(image_export_tab)
        self.export_all_pictographs_button.clicked.connect(
            self.pictograph_exporter.export_all_pictographs
        )

        # Connect the stateChanged signal to our handler
        self.save_dir_checkbox.stateChanged.connect(self._save_directory_preference)
        self.buttons = {}
        self.button_settings_keys = {
            "Start Position": "include_start_position",
            "User Info": "add_user_info",
            "Word": "add_word",
            "Difficulty Level": "add_difficulty_level",
            "Beat Numbers": "add_beat_numbers",
            "Reversal Symbols": "add_reversal_symbols",
            "Combined Grids": "combined_grids",
        }
        self._setup_ui()

    def _setup_ui(self):
        """Sets up the user interface layout."""
        main_layout = QVBoxLayout(self)

        # Create layouts
        top_layout = self._create_user_notes_layout()
        save_dir_layout = self._create_save_directory_layout()
        grid_layout = self._create_buttons_grid_layout()
        export_buttons_layout = self._create_export_buttons_layout()

        # Add layouts to main layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(save_dir_layout)
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(export_buttons_layout)
        self.setLayout(main_layout)

        # Load settings
        self._load_user_profiles()
        self._load_saved_note()
        self._load_directory_preference()

    def _create_export_buttons_layout(self) -> QHBoxLayout:
        """Creates the layout for the export buttons."""
        layout = QHBoxLayout()

        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # Create a vertical layout for the separator and buttons
        v_layout = QVBoxLayout()
        v_layout.addWidget(separator)

        # Create a horizontal layout for the buttons
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)  # Add stretch before buttons
        h_layout.addWidget(self.export_all_pictographs_button)
        h_layout.addStretch(1)  # Add stretch after buttons

        v_layout.addLayout(h_layout)
        layout.addLayout(v_layout)

        return layout

    def _create_user_notes_layout(self) -> QHBoxLayout:
        """Creates the horizontal layout for user and custom note field."""
        top_layout = QHBoxLayout()

        # User dropdown
        top_layout.addWidget(QLabel("User:"))
        top_layout.addWidget(self.user_combo_box)

        # Custom note field
        top_layout.addWidget(QLabel("Custom Note:"))
        self.note_input.setPlaceholderText("Enter note to include in exports")
        self.note_input.textChanged.connect(self._save_current_note)
        top_layout.addWidget(self.note_input)

        return top_layout

    def _save_current_note(self):
        """Save the current note to settings."""
        note_text = self.note_input.text()
        self.settings_manager.image_export.set_custom_note(note_text)

    def _load_saved_note(self):
        """Load the saved custom note."""
        saved_note = self.settings_manager.image_export.get_custom_note()
        if saved_note:
            self.note_input.setText(saved_note)

    def _create_save_directory_layout(self) -> QHBoxLayout:
        """Creates the layout for the save directory checkbox."""
        layout = QHBoxLayout()

        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # Create a vertical layout for the separator and checkbox
        v_layout = QVBoxLayout()
        v_layout.addWidget(separator)

        # Create a horizontal layout for the checkbox with some padding
        h_layout = QHBoxLayout()

        if self.save_dir_checkbox.parent() is None:
            h_layout.addWidget(self.save_dir_checkbox)
        else:
            print("Checkbox already has a parent, not adding it again")

        h_layout.addStretch(1)  # Push checkbox to the left

        v_layout.addLayout(h_layout)
        layout.addLayout(v_layout)

        return layout

    def _save_directory_preference(self, state):
        """Save the directory preference setting."""
        is_checked = state == 2

        # Force the checkbox to be checked/unchecked based on the state
        self.save_dir_checkbox.setChecked(is_checked)

        # Save the setting
        self.settings_manager.image_export.set_image_export_setting(
            "use_last_save_directory", is_checked
        )

        # Verify the setting was saved
        saved_value = self.settings_manager.image_export.get_image_export_setting(
            "use_last_save_directory"
        )

        # Force sync the settings
        self.settings_manager.settings.sync()

        # Emit the signal to update the preview
        self.emit_setting_changed()

    def _load_directory_preference(self):
        """Load the directory preference setting."""
        use_last_dir = self.settings_manager.image_export.get_image_export_setting(
            "use_last_save_directory"
        )
        self.save_dir_checkbox.setChecked(use_last_dir)

    def _load_user_profiles(self):
        """Loads the current user into the user combo box."""
        self.user_combo_box.clear()
        current_user = self.settings_manager.users.get_current_user()

        # Add the current user or a default placeholder
        if current_user:
            self.user_combo_box.addItem(current_user)
            self.user_combo_box.setCurrentText(current_user)
        else:
            self.user_combo_box.addItem("No user set")
            self.user_combo_box.setCurrentText("No user set")

    def _create_buttons_grid_layout(self) -> QGridLayout:
        """Creates the grid layout for the export option buttons."""
        grid_layout = QGridLayout()

        for i, (label, setting_key) in enumerate(self.button_settings_keys.items()):
            button = ImageExportTabButton(
                label, setting_key, self.settings_manager, self.image_export_tab
            )
            button.clicked.connect(self.emit_setting_changed)
            self.buttons[label] = button
            row, col = divmod(i, 3)
            grid_layout.addWidget(button, row, col)

        return grid_layout

    def emit_setting_changed(self):
        """Emits a signal when a setting is changed."""
        self.settingChanged.emit()

    # Removed _show_codex_turns_dialog method as it's no longer needed
