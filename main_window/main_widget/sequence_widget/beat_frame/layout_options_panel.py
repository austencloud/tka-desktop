from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.layout_options_dialog import (
        LayoutOptionsDialog,
    )


class LayoutOptionsPanel(QWidget):
    """Displays the 'grow sequence' checkbox, the number of beats dropdown,
    and the layout options dropdown in the layout options dialog."""

    def __init__(self, dialog: "LayoutOptionsDialog"):
        super().__init__(dialog)
        self.dialog = dialog
        self.sequence_widget = dialog.sequence_widget
        self.settings_manager = (
            self.sequence_widget.main_widget.main_window.settings_manager
        )
        self.beat_frame = self.sequence_widget.beat_frame
        self.layout_options = self._get_layout_options()

        # Initialize UI components
        self._initialize_components()

        # Setup layout after initializing components
        self._setup_layout()

        # Setup layout options based on initial component values
        self._setup_layout_options()
        self._attach_listeners()

    def _attach_listeners(self):
        self.sequence_growth_checkbox.toggled.connect(self._toggle_grow_sequence)
        self.beats_combo_box.currentIndexChanged.connect(self._setup_layout_options)

    def _initialize_components(self):
        """Initialize all UI components."""
        self.beats_label = QLabel("Number of Beats:")
        self.layout_label = QLabel("Layout Options:")
        self.beats_combo_box = QComboBox(self)
        self.layout_combo_box = QComboBox(self)

        self._setup_grow_sequence_checkbox()
        self._setup_number_of_beats_dropdown()
        self._setup_layout_options_dropdown()

    def _setup_layout(self):
        """Setup the layout of the UI components."""
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.combobox_layout = self._setup_combobox_layout()

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(
            self.checkbox_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addLayout(self.combobox_layout)
        self.main_layout.addStretch(1)

    def _setup_layout_options(self):
        """Setup the layout options in the combo box."""
        self.layout_combo_box.clear()
        num_beats = int(self.beats_combo_box.currentText())
        layouts = self.layout_options.get(num_beats, [])
        for layout in layouts:
            self.layout_combo_box.currentIndexChanged.disconnect(
                self.dialog.beat_frame.update_preview
            )
            self.layout_combo_box.addItem(f"{layout[0]} x {layout[1]}")
            self.layout_combo_box.currentIndexChanged.connect(
                self.dialog.beat_frame.update_preview
            )
        if layouts:
            self.layout_combo_box.setCurrentIndex(0)
            self.save_layout_setting()

    def _get_layout_options(self):
        """Return a dictionary of layout options based on the number of beats."""
        layout_options = {
            1: [(1, 1)],
            2: [(1, 2)],
            3: [(1, 3), (2, 2)],
            4: [(2, 2), (1, 4)],
            5: [(3, 2), (2, 3)],
            6: [(3, 2), (2, 3)],
            8: [(4, 2), (2, 4)],
            7: [(4, 2), (2, 4)],
            9: [(3, 3), (2, 5), (5, 2)],
            10: [(5, 2), (2, 5)],
            11: [(4, 3), (3, 4)],
            12: [(4, 3), (3, 4)],
            13: [(5, 3), (3, 5)],
            14: [(4, 4), (2, 7), (7, 2)],
            15: [(5, 3), (3, 5)],
            16: [(4, 4), (2, 8), (8, 2)],
            17: [(5, 4), (4, 4)],
            18: [(6, 3), (3, 6)],
            19: [(5, 4), (4, 5)],
            20: [(5, 4), (4, 5)],
            21: [(6, 4), (4, 6)],
            22: [(6, 4), (4, 6)],
            23: [(7, 4), (4, 7)],
            24: [(6, 4), (4, 6)],
            25: [(5, 5), (6, 4), (4, 6)],
            26: [(6, 4), (4, 6)],
            27: [(6, 4), (4, 6)],
            28: [(7, 4), (4, 7)],
            29: [(7, 4), (4, 7)],
            30: [(6, 5), (5, 6)],
            31: [(7, 4), (4, 7)],
            32: [(8, 4), (4, 8)],
        }
        return layout_options

    def _setup_combobox_layout(self):
        """Setup the layout for the combo boxes."""
        beats_vbox = QVBoxLayout()
        layout_options_vbox = QVBoxLayout()
        combobox_hbox = QHBoxLayout()

        beats_vbox.addWidget(self.beats_label)
        beats_vbox.addWidget(self.beats_combo_box)
        beats_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_options_vbox.addWidget(self.layout_label)
        layout_options_vbox.addWidget(self.layout_combo_box)
        layout_options_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        combobox_hbox.addStretch(3)
        combobox_hbox.addLayout(beats_vbox)
        combobox_hbox.addStretch(1)
        combobox_hbox.addLayout(layout_options_vbox)
        combobox_hbox.addStretch(3)
        return combobox_hbox

    def _setup_grow_sequence_checkbox(self):
        """Setup the 'grow sequence' checkbox."""
        self.sequence_growth_checkbox = QCheckBox("Grow sequence")
        grow_sequence = self.settings_manager.sequence_layout.get_layout_setting(
            "grow_sequence"
        )
        if grow_sequence == "true":
            grow_sequence = True
        elif grow_sequence == "false":
            grow_sequence = False
        self.sequence_growth_checkbox.setChecked(grow_sequence)
        font = self.sequence_growth_checkbox.font()
        font_size = self.sequence_widget.main_widget.width() // 120
        font.setPointSize(font_size)
        self.sequence_growth_checkbox.setFont(font)
        self.sequence_growth_checkbox.setStyleSheet(
            f"QCheckBox::indicator {{ width: {font_size}px; height: {font_size}px; }}"
        )

        self.checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(self.checkbox_widget)
        checkbox_layout.addWidget(self.sequence_growth_checkbox)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_number_of_beats_dropdown(self):
        """Setup the dropdown for the number of beats."""
        self.beats_combo_box.addItems([str(i) for i in self.layout_options.keys()])

        # Temporarily disconnect the signal to avoid triggering _setup_layout_options prematurely
        self.beats_combo_box.blockSignals(True)
        saved_beats = self.settings_manager.sequence_layout.get_layout_setting(
            "num_beats"
        )
        self.beats_combo_box.setCurrentText(str(saved_beats))
        self.beats_combo_box.blockSignals(False)

    def _setup_layout_options_dropdown(self):
        """Setup the dropdown for the layout options."""
        self.layout_combo_box.currentIndexChanged.connect(
            self.dialog.beat_frame.update_preview
        )

        saved_layout = self.settings_manager.sequence_layout.get_layout_setting(
            "layout_option"
        )
        self.layout_combo_box.setCurrentText(saved_layout)

    def _toggle_grow_sequence(self):
        """Handle the toggling of the 'grow sequence' checkbox."""
        is_grow_sequence_checked = self.sequence_growth_checkbox.isChecked()
        self.settings_manager.sequence_layout.set_layout_setting(
            "grow_sequence", is_grow_sequence_checked
        )

        self.beats_label.setEnabled(not is_grow_sequence_checked)
        self.beats_combo_box.setEnabled(not is_grow_sequence_checked)
        self.layout_label.setEnabled(not is_grow_sequence_checked)
        self.layout_combo_box.setEnabled(not is_grow_sequence_checked)

        color = "grey" if is_grow_sequence_checked else "black"
        self.beats_label.setStyleSheet(f"color: {color};")
        self.layout_label.setStyleSheet(f"color: {color};")

        if not is_grow_sequence_checked:
            num_beats = self.sequence_widget.beat_frame.get.next_available_beat() or 0
            self.beats_combo_box.setCurrentText(str(num_beats))
            self._setup_layout_options()
            layout_option = (
                self.get_layout_option_from_current_sequence_beat_frame_layout()
            )
            self.layout_combo_box.setCurrentText(layout_option)

        self.dialog.beat_frame.update_preview()

    def get_layout_option_from_current_sequence_beat_frame_layout(self):
        """Get the current layout option from the sequence beat frame layout."""
        cols = self.beat_frame.layout_manager.get_cols()
        rows = self.beat_frame.layout_manager.get_rows()
        return f"{cols} x {rows}"

    def load_settings(self):
        """Load settings into the UI components."""
        grow_sequence = self.settings_manager.sequence_layout.get_layout_setting(
            "grow_sequence"
        )
        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self._toggle_grow_sequence()

    def initialize_from_state(self, state: dict):
        """Initialize UI components based on a given state."""
        num_beats = state.get("num_beats", 0)
        rows = state.get("rows", 1)
        cols = state.get("cols", 1)
        grow_sequence = state.get("grow_sequence", False)

        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self.beats_combo_box.setCurrentText(str(num_beats))
        self.layout_combo_box.setCurrentText(f"{rows} x {cols}")
        self._toggle_grow_sequence()

    def get_currently_visible_beats(self) -> int:
        """Get the number of currently visible beats."""
        num_beats = 0
        for beat in self.beat_frame.beat_views:
            if beat.isVisible():
                num_beats += 1
        return num_beats

    def save_layout_setting(self):
        """Save the current layout settings."""
        num_beats = int(self.beats_combo_box.currentText())
        layout_option = self.layout_combo_box.currentText()
        self.settings_manager.sequence_layout.set_layout_setting("num_beats", num_beats)
        self.settings_manager.sequence_layout.set_layout_setting(
            "layout_option", layout_option
        )

    def showEvent(self, event):
        """Handle the show event for the panel."""
        super().showEvent(event)
        num_beats = self.get_currently_visible_beats()
        self.beats_combo_box.setCurrentText(str(num_beats))

        layout_option = self.get_layout_option_from_current_sequence_beat_frame_layout()
        self.layout_combo_box.setCurrentText(layout_option)
