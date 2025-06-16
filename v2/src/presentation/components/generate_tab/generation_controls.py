"""
Modern generation control components for Modern Generate Tab.

These components provide clean, modern UI controls for sequence generation
parameters, following Modern's architecture patterns.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFrame,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from typing import Set, Optional

from ....core.interfaces.generation_services import (
    GenerationMode,
    PropContinuity,
    LetterType,
    SliceSize,
    CAPType,
)


class ModernControlBase(QWidget):
    """Base class for modern generation controls"""

    def __init__(
        self, title: str, description: str = "", parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._title = title
        self._description = description
        self._setup_base_ui()

    def _setup_base_ui(self):
        """Setup the base UI structure"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Title
        title_label = QLabel(self._title)
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Description (if provided)
        if self._description:
            desc_label = QLabel(self._description)
            desc_label.setStyleSheet("color: #666666; font-size: 10px;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        # Content area (to be filled by subclasses)
        self._content_layout = QVBoxLayout()
        self._content_layout.setContentsMargins(0, 4, 0, 0)
        layout.addWidget(self._create_content_widget())

        # Apply styling
        self.setStyleSheet(
            """
            ModernControlBase {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
            }
            ModernControlBase:hover {
                border-color: #BDBDBD;
            }
        """
        )

    def _create_content_widget(self) -> QWidget:
        """Create the content widget (override in subclasses)"""
        content_widget = QWidget()
        content_widget.setLayout(self._content_layout)
        return content_widget


class ModernGenerationModeToggle(ModernControlBase):
    """Toggle between freeform and circular generation modes"""

    mode_changed = pyqtSignal(GenerationMode)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Generation Mode",
            "Choose between freeform or circular sequence generation",
            parent,
        )
        self._current_mode = GenerationMode.FREEFORM
        self._setup_controls()

    def _setup_controls(self):
        """Setup the mode toggle controls"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)

        # Create button group for exclusive selection
        self._button_group = QButtonGroup(self)

        # Freeform button
        self._freeform_button = QPushButton("Freeform")
        self._freeform_button.setCheckable(True)
        self._freeform_button.setChecked(True)
        self._freeform_button.setMinimumHeight(32)
        self._freeform_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._freeform_button, 0)
        button_layout.addWidget(self._freeform_button)

        # Circular button
        self._circular_button = QPushButton("Circular")
        self._circular_button.setCheckable(True)
        self._circular_button.setMinimumHeight(32)
        self._circular_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._circular_button, 1)
        button_layout.addWidget(self._circular_button)

        self._content_layout.addLayout(button_layout)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

        # Apply styling
        self._apply_button_styling()

    def _apply_button_styling(self):
        """Apply modern toggle button styling"""
        button_style = """
            QPushButton {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
                color: #424242;
            }
            QPushButton:hover {
                background-color: #E8F5E8;
                border-color: #4CAF50;
            }
            QPushButton:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
                color: white;
            }
            QPushButton:checked:hover {
                background-color: #45a049;
            }
        """
        self._freeform_button.setStyleSheet(button_style)
        self._circular_button.setStyleSheet(button_style)

    def _on_button_clicked(self, button):
        """Handle button click"""
        if button == self._freeform_button:
            self._current_mode = GenerationMode.FREEFORM
        else:
            self._current_mode = GenerationMode.CIRCULAR

        self.mode_changed.emit(self._current_mode)

    def set_mode(self, mode: GenerationMode):
        """Set the current mode"""
        self._current_mode = mode
        if mode == GenerationMode.FREEFORM:
            self._freeform_button.setChecked(True)
        else:
            self._circular_button.setChecked(True)


class ModernLengthSelector(ModernControlBase):
    """Selector for sequence length"""

    value_changed = pyqtSignal(int)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Sequence Length",
            "Number of beats in the generated sequence (4-32)",
            parent,
        )
        self._current_value = 16
        self._setup_controls()

    def _setup_controls(self):
        """Setup length selector controls"""
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)

        # Slider
        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setMinimum(4)
        self._slider.setMaximum(32)
        self._slider.setValue(16)
        self._slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._slider.setTickInterval(4)
        control_layout.addWidget(self._slider, 1)

        # Value display/input
        self._spinbox = QSpinBox()
        self._spinbox.setMinimum(4)
        self._spinbox.setMaximum(32)
        self._spinbox.setValue(16)
        self._spinbox.setMinimumWidth(60)
        control_layout.addWidget(self._spinbox)

        self._content_layout.addLayout(control_layout)

        # Connect signals
        self._slider.valueChanged.connect(self._on_value_changed)
        self._spinbox.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value: int):
        """Handle value change"""
        if value != self._current_value:
            self._current_value = value

            # Sync controls
            self._slider.blockSignals(True)
            self._spinbox.blockSignals(True)
            self._slider.setValue(value)
            self._spinbox.setValue(value)
            self._slider.blockSignals(False)
            self._spinbox.blockSignals(False)

            self.value_changed.emit(value)

    def set_value(self, value: int):
        """Set the current value"""
        self._on_value_changed(value)


class ModernLevelSelector(ModernControlBase):
    """Selector for difficulty level"""

    value_changed = pyqtSignal(int)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Difficulty Level", "Complexity of the generated sequence (1-6)", parent
        )
        self._current_value = 1
        self._setup_controls()

    def _setup_controls(self):
        """Setup level selector controls"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)

        self._button_group = QButtonGroup(self)
        self._buttons = []

        for i in range(1, 7):
            button = QPushButton(str(i))
            button.setCheckable(True)
            button.setMinimumSize(32, 32)
            button.setMaximumSize(32, 32)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            if i == 1:
                button.setChecked(True)

            self._button_group.addButton(button, i)
            self._buttons.append(button)
            button_layout.addWidget(button)

        button_layout.addStretch()
        self._content_layout.addLayout(button_layout)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

        # Apply styling
        self._apply_level_button_styling()

    def _apply_level_button_styling(self):
        """Apply styling to level buttons"""
        button_style = """
            QPushButton {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 16px;
                font-weight: bold;
                color: #424242;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
                border-color: #2196F3;
            }
            QPushButton:checked {
                background-color: #2196F3;
                border-color: #2196F3;
                color: white;
            }
        """
        for button in self._buttons:
            button.setStyleSheet(button_style)

    def _on_button_clicked(self, button):
        """Handle button click"""
        level = self._button_group.id(button)
        if level != self._current_value:
            self._current_value = level
            self.value_changed.emit(level)

    def set_value(self, value: int):
        """Set the current value"""
        if 1 <= value <= 6:
            self._current_value = value
            button = self._button_group.button(value)
            if button:
                button.setChecked(True)


class ModernTurnIntensitySelector(ModernControlBase):
    """Selector for turn intensity"""

    value_changed = pyqtSignal(float)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Turn Intensity", "How complex the turns should be (0.5-3.0)", parent
        )
        self._current_value = 1.0
        self._setup_controls()

    def _setup_controls(self):
        """Setup turn intensity controls"""
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)

        # Preset buttons for common values
        preset_layout = QHBoxLayout()
        preset_layout.setSpacing(4)

        self._preset_group = QButtonGroup(self)
        presets = [
            ("0.5", 0.5),
            ("1", 1.0),
            ("1.5", 1.5),
            ("2", 2.0),
            ("2.5", 2.5),
            ("3", 3.0),
        ]

        for i, (label, value) in enumerate(presets):
            button = QPushButton(label)
            button.setCheckable(True)
            button.setMinimumSize(32, 24)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            if value == 1.0:
                button.setChecked(True)

            self._preset_group.addButton(button, i)
            preset_layout.addWidget(button)

        preset_layout.addStretch()
        self._content_layout.addLayout(preset_layout)

        # Connect signals
        self._preset_group.buttonClicked.connect(self._on_preset_clicked)

        # Store preset values
        self._preset_values = [value for _, value in presets]

        # Apply styling
        self._apply_preset_styling()

    def _apply_preset_styling(self):
        """Apply styling to preset buttons"""
        button_style = """
            QPushButton {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-weight: 500;
                color: #424242;
            }
            QPushButton:hover {
                background-color: #FFF3E0;
                border-color: #FF9800;
            }
            QPushButton:checked {
                background-color: #FF9800;
                border-color: #FF9800;
                color: white;
            }
        """
        for button in self._preset_group.buttons():
            button.setStyleSheet(button_style)

    def _on_preset_clicked(self, button):
        """Handle preset button click"""
        preset_index = self._preset_group.id(button)
        value = self._preset_values[preset_index]
        if value != self._current_value:
            self._current_value = value
            self.value_changed.emit(value)

    def set_value(self, value: float):
        """Set the current value"""
        self._current_value = value
        # Find closest preset
        for i, preset_value in enumerate(self._preset_values):
            if abs(preset_value - value) < 0.01:
                button = self._preset_group.button(i)
                if button:
                    button.setChecked(True)
                break


class ModernPropContinuityToggle(ModernControlBase):
    """Toggle for prop continuity setting"""

    value_changed = pyqtSignal(PropContinuity)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Prop Continuity", "How props should behave throughout the sequence", parent
        )
        self._current_value = PropContinuity.CONTINUOUS
        self._setup_controls()

    def _setup_controls(self):
        """Setup prop continuity controls"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)

        self._button_group = QButtonGroup(self)

        # Continuous button
        self._continuous_button = QPushButton("Continuous")
        self._continuous_button.setCheckable(True)
        self._continuous_button.setChecked(True)
        self._continuous_button.setMinimumHeight(32)
        self._continuous_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._continuous_button, 0)
        button_layout.addWidget(self._continuous_button)

        # Random button
        self._random_button = QPushButton("Random")
        self._random_button.setCheckable(True)
        self._random_button.setMinimumHeight(32)
        self._random_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._random_button, 1)
        button_layout.addWidget(self._random_button)

        self._content_layout.addLayout(button_layout)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

        # Apply styling
        self._apply_toggle_styling()

    def _apply_toggle_styling(self):
        """Apply toggle button styling"""
        button_style = """
            QPushButton {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
                color: #424242;
            }
            QPushButton:hover {
                background-color: #E8F5E8;
                border-color: #4CAF50;
            }
            QPushButton:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
                color: white;
            }
        """
        self._continuous_button.setStyleSheet(button_style)
        self._random_button.setStyleSheet(button_style)

    def _on_button_clicked(self, button):
        """Handle button click"""
        if button == self._continuous_button:
            self._current_value = PropContinuity.CONTINUOUS
        else:
            self._current_value = PropContinuity.RANDOM

        self.value_changed.emit(self._current_value)

    def set_value(self, value: PropContinuity):
        """Set the current value"""
        self._current_value = value
        if value == PropContinuity.CONTINUOUS:
            self._continuous_button.setChecked(True)
        else:
            self._random_button.setChecked(True)


class ModernLetterTypeSelector(ModernControlBase):
    """Multi-select for letter types (freeform mode)"""

    value_changed = pyqtSignal(set)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Letter Types", "Select which letter types to include in generation", parent
        )
        self._current_value = {
            LetterType.TYPE1,
            LetterType.TYPE2,
            LetterType.TYPE3,
            LetterType.TYPE4,
            LetterType.TYPE5,
            LetterType.TYPE6,
        }
        self._setup_controls()

    def _setup_controls(self):
        """Setup letter type controls"""
        checkbox_layout = QVBoxLayout()
        checkbox_layout.setSpacing(4)

        self._checkboxes = {}

        # Legacy's letter type descriptions
        letter_type_info = [
            (LetterType.TYPE1, "Type 1 (Dual-Shift: A-V)"),
            (LetterType.TYPE2, "Type 2 (Shift: W,X,Y,Z,Σ,Δ,θ,Ω)"),
            (LetterType.TYPE3, "Type 3 (Cross-Shift: W-,X-,Y-,Z-,Σ-,Δ-,θ-,Ω-)"),
            (LetterType.TYPE4, "Type 4 (Dash: Φ,Ψ,Λ)"),
            (LetterType.TYPE5, "Type 5 (Dual-Dash: Φ-,Ψ-,Λ-)"),
            (LetterType.TYPE6, "Type 6 (Static: α,β,Γ)"),
        ]

        for letter_type, description in letter_type_info:
            checkbox = QCheckBox(description)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self._on_checkbox_changed)
            self._checkboxes[letter_type] = checkbox
            checkbox_layout.addWidget(checkbox)

        self._content_layout.addLayout(checkbox_layout)

    def _on_checkbox_changed(self):
        """Handle checkbox state change"""
        new_value = set()
        for letter_type, checkbox in self._checkboxes.items():
            if checkbox.isChecked():
                new_value.add(letter_type)

        if new_value != self._current_value:
            self._current_value = new_value
            self.value_changed.emit(new_value)

    def set_value(self, value: Set[LetterType]):
        """Set the current value"""
        self._current_value = value
        for letter_type, checkbox in self._checkboxes.items():
            checkbox.blockSignals(True)
            checkbox.setChecked(letter_type in value)
            checkbox.blockSignals(False)


class ModernSliceSizeSelector(ModernControlBase):
    """Selector for slice size (circular mode)"""

    value_changed = pyqtSignal(SliceSize)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Slice Size",
            "Size of circular sequence slices (quartered or halved)",
            parent,
        )
        self._current_value = SliceSize.HALVED
        self._setup_controls()

    def _setup_controls(self):
        """Setup slice size controls"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)

        self._button_group = QButtonGroup(self)

        # Halved button (default)
        self._halved_button = QPushButton("Halved")
        self._halved_button.setCheckable(True)
        self._halved_button.setChecked(True)
        self._halved_button.setMinimumHeight(32)
        self._halved_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._halved_button, 0)
        button_layout.addWidget(self._halved_button)

        # Quartered button
        self._quartered_button = QPushButton("Quartered")
        self._quartered_button.setCheckable(True)
        self._quartered_button.setMinimumHeight(32)
        self._quartered_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._quartered_button, 1)
        button_layout.addWidget(self._quartered_button)

        self._content_layout.addLayout(button_layout)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

        # Apply styling
        self._apply_button_styling()

    def _apply_button_styling(self):
        """Apply toggle button styling"""
        button_style = """
            QPushButton {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
                color: #424242;
            }
            QPushButton:hover {
                background-color: #E8F5E8;
                border-color: #4CAF50;
            }
            QPushButton:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
                color: white;
            }
        """
        self._halved_button.setStyleSheet(button_style)
        self._quartered_button.setStyleSheet(button_style)

    def _on_button_clicked(self, button):
        """Handle button click"""
        if button == self._halved_button:
            self._current_value = SliceSize.HALVED
        else:
            self._current_value = SliceSize.QUARTERED

        self.value_changed.emit(self._current_value)

    def set_value(self, value: SliceSize):
        """Set the current value"""
        self._current_value = value
        if value == SliceSize.HALVED:
            self._halved_button.setChecked(True)
        else:
            self._quartered_button.setChecked(True)


class ModernCAPTypeSelector(ModernControlBase):
    """Selector for CAP type (circular mode)"""

    value_changed = pyqtSignal(CAPType)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("CAP Type", "Circular arrangement pattern type", parent)
        self._current_value = CAPType.STRICT_ROTATED
        self._setup_controls()

    def _setup_controls(self):
        """Setup CAP type controls"""
        combo = QComboBox()

        # Add all Legacy CAP types
        cap_types = [
            ("Strict Rotated", CAPType.STRICT_ROTATED),
            ("Strict Mirrored", CAPType.STRICT_MIRRORED),
            ("Strict Swapped", CAPType.STRICT_SWAPPED),
            ("Strict Complementary", CAPType.STRICT_COMPLEMENTARY),
            ("Swapped Complementary", CAPType.SWAPPED_COMPLEMENTARY),
            ("Rotated Complementary", CAPType.ROTATED_COMPLEMENTARY),
            ("Mirrored Swapped", CAPType.MIRRORED_SWAPPED),
            ("Mirrored Complementary", CAPType.MIRRORED_COMPLEMENTARY),
            ("Rotated Swapped", CAPType.ROTATED_SWAPPED),
            ("Mirrored Rotated", CAPType.MIRRORED_ROTATED),
            ("Mirrored Complementary Rotated", CAPType.MIRRORED_COMPLEMENTARY_ROTATED),
        ]

        for name, cap_type in cap_types:
            combo.addItem(name, cap_type)

        combo.currentIndexChanged.connect(self._on_combo_changed)
        self._combo = combo

        self._content_layout.addWidget(combo)

    def _on_combo_changed(self, index: int):
        """Handle combo box change"""
        value = self._combo.itemData(index)
        if value != self._current_value:
            self._current_value = value
            self.value_changed.emit(value)

    def set_value(self, value: CAPType):
        """Set the current value"""
        self._current_value = value
        for i in range(self._combo.count()):
            if self._combo.itemData(i) == value:
                self._combo.setCurrentIndex(i)
                break
