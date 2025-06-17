"""
Modern Generate Panel for Modern Generate Tab.

This panel contains all the generation controls and orchestrates the generation workflow
following Modern's modern UI patterns and clean architecture.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QFrame,
    QPushButton,
    QLabel,
    QProgressBar,
    QTextEdit,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from typing import Optional

from domain.models.generation_models import (
    GenerationConfig,
    GenerationState,
    GenerationResult,
)
from core.interfaces.generation_services import GenerationMode
from .generation_controls import (
    ModernGenerationModeToggle,
    ModernLengthSelector,
    ModernLevelSelector,
    ModernTurnIntensitySelector,
    ModernPropContinuityToggle,
    ModernLetterTypeSelector,
    ModernSliceSizeSelector,
    ModernCAPTypeSelector,
)


class GeneratePanel(QWidget):

    generate_requested = pyqtSignal(GenerationConfig)
    auto_complete_requested = pyqtSignal()
    config_changed = pyqtSignal(GenerationConfig)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_config = GenerationConfig()
        self._current_state = GenerationState(config=self._current_config)
        self._setup_ui()
        self._connect_signals()
        self._apply_styling()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        self._setup_header(layout)

        # Controls scroll area
        self._setup_controls_area(layout)

        # Action buttons
        self._setup_action_buttons(layout)

        # Status area
        self._setup_status_area(layout)

    def _setup_header(self, layout: QVBoxLayout):
        header = QLabel("Generate Sequence")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

    def _setup_controls_area(self, layout: QVBoxLayout):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setSpacing(12)

        # Generation mode toggle
        self._mode_toggle = ModernGenerationModeToggle()
        controls_layout.addWidget(self._mode_toggle)

        # Basic parameters
        self._setup_basic_parameters(controls_layout)

        # Mode-specific controls
        self._setup_mode_specific_controls(controls_layout)

        controls_layout.addStretch()
        scroll_area.setWidget(controls_widget)
        layout.addWidget(scroll_area, 1)

    def _setup_basic_parameters(self, layout: QVBoxLayout):
        basic_frame = QFrame()
        basic_frame.setFrameShape(QFrame.Shape.Box)
        basic_layout = QVBoxLayout(basic_frame)
        basic_layout.setSpacing(8)

        # Basic controls
        self._length_selector = ModernLengthSelector()
        self._level_selector = ModernLevelSelector()
        self._turn_intensity_selector = ModernTurnIntensitySelector()
        self._prop_continuity_toggle = ModernPropContinuityToggle()

        basic_layout.addWidget(self._length_selector)
        basic_layout.addWidget(self._level_selector)
        basic_layout.addWidget(self._turn_intensity_selector)
        basic_layout.addWidget(self._prop_continuity_toggle)

        layout.addWidget(basic_frame)

    def _setup_mode_specific_controls(self, layout: QVBoxLayout):
        # Container for mode-specific controls
        self._mode_specific_layout = QVBoxLayout()

        # Freeform controls
        self._setup_freeform_controls()

        # Circular controls
        self._setup_circular_controls()

        layout.addLayout(self._mode_specific_layout)

    def _setup_freeform_controls(self):
        self._freeform_controls = QWidget()
        freeform_layout = QVBoxLayout(self._freeform_controls)
        freeform_layout.setContentsMargins(0, 0, 0, 0)
        freeform_layout.setSpacing(12)

        # Letter type selector
        self._letter_type_selector = ModernLetterTypeSelector()
        freeform_layout.addWidget(self._letter_type_selector)

        self._mode_specific_layout.addWidget(self._freeform_controls)

    def _setup_circular_controls(self):
        self._circular_controls = QWidget()
        circular_layout = QVBoxLayout(self._circular_controls)
        circular_layout.setContentsMargins(0, 0, 0, 0)
        circular_layout.setSpacing(12)

        # Slice size selector
        self._slice_size_selector = ModernSliceSizeSelector()
        circular_layout.addWidget(self._slice_size_selector)

        # CAP type selector
        self._cap_type_selector = ModernCAPTypeSelector()
        circular_layout.addWidget(self._cap_type_selector)

        self._mode_specific_layout.addWidget(self._circular_controls)

        # Initially hide circular controls
        self._circular_controls.hide()

    def _setup_action_buttons(self, layout: QVBoxLayout):
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self._generate_button = QPushButton("Generate New Sequence")
        self._generate_button.setMinimumHeight(40)
        self._generate_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self._auto_complete_button = QPushButton("Auto Complete")
        self._auto_complete_button.setMinimumHeight(40)
        self._auto_complete_button.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout.addWidget(self._auto_complete_button)
        button_layout.addWidget(self._generate_button)

        layout.addLayout(button_layout)

    def _setup_status_area(self, layout: QVBoxLayout):
        self._status_frame = QFrame()
        self._status_frame.setFrameShape(QFrame.Shape.StyledPanel)
        status_layout = QVBoxLayout(self._status_frame)

        self._progress_bar = QProgressBar()
        self._progress_bar.hide()

        self._status_text = QTextEdit()
        self._status_text.setMaximumHeight(100)
        self._status_text.setReadOnly(True)
        self._status_text.hide()

        status_layout.addWidget(self._progress_bar)
        status_layout.addWidget(self._status_text)

        layout.addWidget(self._status_frame)
        self._status_frame.hide()

    def _connect_signals(self):
        # Mode change
        self._mode_toggle.mode_changed.connect(self._on_mode_changed)

        # Parameter changes
        self._length_selector.value_changed.connect(
            lambda v: self._update_config(length=v)
        )
        self._level_selector.value_changed.connect(
            lambda v: self._update_config(level=v)
        )
        self._turn_intensity_selector.value_changed.connect(
            lambda v: self._update_config(turn_intensity=v)
        )
        self._prop_continuity_toggle.value_changed.connect(
            lambda v: self._update_config(prop_continuity=v)
        )

        # Freeform controls
        self._letter_type_selector.value_changed.connect(
            lambda v: self._update_config(letter_types=v)
        )

        # Circular controls
        self._slice_size_selector.value_changed.connect(
            lambda v: self._update_config(slice_size=v)
        )
        self._cap_type_selector.value_changed.connect(
            lambda v: self._update_config(cap_type=v)
        )

        # Action buttons
        self._generate_button.clicked.connect(self._on_generate_clicked)
        self._auto_complete_button.clicked.connect(self._on_auto_complete_clicked)

    def _apply_styling(self):
        self.setStyleSheet(
            """
            ModernGeneratePanel {
                background-color: #FAFAFA;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
            QFrame {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
                padding: 8px;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """
        )

    def _on_mode_changed(self, mode: GenerationMode):
        self._update_config(mode=mode)

        # Show/hide mode-specific controls
        is_freeform = mode == GenerationMode.FREEFORM
        self._freeform_controls.setVisible(is_freeform)
        self._circular_controls.setVisible(not is_freeform)

    def _update_config(self, **kwargs):
        try:
            self._current_config = self._current_config.with_updates(**kwargs)
            self._current_state = self._current_state.with_config(self._current_config)
            self.config_changed.emit(self._current_config)
        except Exception as e:
            self._show_error(f"Configuration error: {e}")

    def _on_generate_clicked(self):
        if self._current_state.is_generating:
            return

        self._current_state = self._current_state.start_generation()
        self._update_ui_for_generation_state()
        self.generate_requested.emit(self._current_config)

    def _on_auto_complete_clicked(self):
        if self._current_state.is_generating:
            return

        self.auto_complete_requested.emit()

    def _update_ui_for_generation_state(self):
        is_generating = self._current_state.is_generating

        self._generate_button.setEnabled(not is_generating)
        self._auto_complete_button.setEnabled(not is_generating)

        if is_generating:
            self._show_progress("Generating sequence...")
        else:
            self._hide_progress()

    def _show_progress(self, message: str):
        self._status_frame.show()
        self._progress_bar.show()
        self._progress_bar.setRange(0, 0)  # Indeterminate
        self._status_text.show()
        self._status_text.setText(message)

    def _hide_progress(self):
        self._progress_bar.hide()
        self._status_text.hide()
        self._status_frame.hide()

    def _show_error(self, message: str):
        self._status_frame.show()
        self._status_text.show()
        self._status_text.setText(f"Error: {message}")
        self._status_text.setStyleSheet("color: red;")

    def set_state(self, state: GenerationState):
        self._current_state = state
        self._current_config = state.config
        self._update_controls_from_config()
        self._update_ui_for_generation_state()

    def set_generation_result(self, result: GenerationResult):
        self._current_state = self._current_state.with_result(result)
        self._update_ui_for_generation_state()

        if result.success:
            self._status_text.setText("Generation completed successfully!")
            self._status_text.setStyleSheet("color: green;")
        else:
            self._show_error(result.error_message or "Generation failed")

    def _update_controls_from_config(self):
        # Update all controls to reflect current config
        self._mode_toggle.set_mode(self._current_config.mode)
        self._length_selector.set_value(self._current_config.length)
        self._level_selector.set_value(self._current_config.level)
        self._turn_intensity_selector.set_value(self._current_config.turn_intensity)
        self._prop_continuity_toggle.set_value(self._current_config.prop_continuity)

        if self._current_config.letter_types:
            self._letter_type_selector.set_value(self._current_config.letter_types)

        self._slice_size_selector.set_value(self._current_config.slice_size)
        if self._current_config.cap_type:
            self._cap_type_selector.set_value(self._current_config.cap_type)
