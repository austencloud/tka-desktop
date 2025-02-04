from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Enums.letters import LetterType
from main_window.main_widget.generate_tab.freeform.letter_type_button_widget import (
    LetterTypeButtonWidget,
)

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.freeform.freeform_sequence_generator_frame import (
        FreeformSequenceGeneratorFrame,
    )


class LetterTypePickerWidget(QWidget):
    def __init__(self, generator_frame: "FreeformSequenceGeneratorFrame"):
        super().__init__(generator_frame)
        self.generator_frame = generator_frame
        self.sequence_generator_settings = generator_frame.generate_tab_settings
        self.builder_type = generator_frame.generator_type

        # Instead of a checkbox, use a label
        self.filter_label = QLabel("Filter by type:")
        self.filter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout for letter type buttons
        self.letter_types_layout = QHBoxLayout()
        self.letter_types_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create 6 letter type button widgets
        self.letter_type_widgets: list[LetterTypeButtonWidget] = []
        for i, letter_type in enumerate(LetterType, start=1):
            w = LetterTypeButtonWidget(self, letter_type, i)
            w.clicked.connect(self._on_letter_type_clicked)
            self.letter_types_layout.addWidget(w)
            self.letter_type_widgets.append(w)

        # Initially hide these since the default could be "All Letters"
        # (Adjust logic as needed if you want them always visible)
        self._set_letter_type_buttons_visible(False)

        # Main layout
        main_layout = QVBoxLayout(self)
        mode_layout = QHBoxLayout()
        mode_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mode_layout.addWidget(self.filter_label)
        main_layout.addLayout(mode_layout)
        main_layout.addLayout(self.letter_types_layout)
        main_layout.addStretch(1)

    def _on_letter_type_clicked(self, letter_type: LetterType, is_selected: bool):
        # Ensure at least one is selected
        selected_count = sum(w.is_selected for w in self.letter_type_widgets)
        if selected_count == 0:
            # revert this one to selected if none remain selected
            for lt, w in zip(LetterType, self.letter_type_widgets):
                if lt == letter_type:
                    w.is_selected = True
                    w.update_colors()

        chosen = [
            lt.description
            for lt, w in zip(LetterType, self.letter_type_widgets)
            if w.is_selected
        ]
        self.sequence_generator_settings.set_sequence_generator_setting(
            "selected_letter_types", chosen, self.builder_type
        )

    def _set_letter_type_buttons_visible(self, visible: bool):
        for w in self.letter_type_widgets:
            w.setVisible(visible)

    def apply_settings(self):
        selected_types = (
            self.sequence_generator_settings.get_sequence_generator_setting(
                "selected_letter_types", self.builder_type
            )
        )

        if selected_types is None:
            # Means all letters are used, so hide the buttons if you like
            self._set_letter_type_buttons_visible(False)
        else:
            # Specific letters mode, show buttons and restore their states
            self._set_letter_type_buttons_visible(True)
            if len(selected_types) > 0:
                any_selected = False
                for lt, w in zip(LetterType, self.letter_type_widgets):
                    is_selected = lt.description in selected_types
                    w.is_selected = is_selected
                    w.update_colors()
                    if is_selected:
                        any_selected = True
                if not any_selected:
                    # If none selected, select all by default
                    for w in self.letter_type_widgets:
                        w.is_selected = True
                        w.update_colors()
                    self.sequence_generator_settings.set_sequence_generator_setting(
                        "selected_letter_types",
                        [lt.description for lt in LetterType],
                        self.builder_type,
                    )
            else:
                # None chosen, select all
                for w in self.letter_type_widgets:
                    w.is_selected = True
                    w.update_colors()
                self.sequence_generator_settings.set_sequence_generator_setting(
                    "selected_letter_types",
                    [lt.description for lt in LetterType],
                    self.builder_type,
                )

    def get_selected_letter_types(self) -> list[LetterType]:
        return [
            lt for lt, w in zip(LetterType, self.letter_type_widgets) if w.is_selected
        ]

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font_size = self.generator_frame.tab.main_widget.height() // 50
        self.filter_label.setFont(QFont("Arial", font_size))
        self.layout().setSpacing(self.generator_frame.height() // 50)
        width = self.generator_frame.width() // 16
        for w in self.letter_type_widgets:
            w.setFixedSize(width, width)
            f = w.label.font()
            f.setPointSize(font_size)
            w.label.setFont(f)

        f = self.filter_label.font()
        f.setPointSize(font_size)
        self.filter_label.setFont(f)
        global_settings = (
            self.generator_frame.tab.main_widget.main_window.settings_manager.global_settings
        )
        color = self.generator_frame.tab.main_widget.font_color_updater.get_font_color(
            global_settings.get_background_type()
        )
        existing_style = self.filter_label.styleSheet()
        new_style = f"{existing_style} color: {color};"
        self.filter_label.setStyleSheet(new_style)
