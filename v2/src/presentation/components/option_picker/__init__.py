from typing import List, Optional, Dict, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy, QLabel
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtGui import QFont

from ....core.dependency_injection.simple_container import SimpleContainer
from ....core.interfaces.core_services import ILayoutService
from ....domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from .option_picker_widget import ModernOptionPickerWidget
from .option_picker_section import OptionPickerSection
from .option_picker_filter import OptionPickerFilter
from .letter_types import LetterType
from .clickable_pictograph_frame import ClickablePictographFrame


class ModernOptionPicker(QObject):
    option_selected = pyqtSignal(str)

    def __init__(self, container: SimpleContainer):
        super().__init__()
        self.container = container
        self.widget: Optional[QWidget] = None
        self._beat_options: List[BeatData] = []
        self._sections: Dict[str, OptionPickerSection] = {}
        self._layout_service: Optional[ILayoutService] = None
        self.sections_container: Optional[QWidget] = None
        self.sections_layout: Optional[QVBoxLayout] = None
        self.filter_widget: Optional[OptionPickerFilter] = None

    def initialize(self) -> None:
        self._layout_service = self.container.resolve(ILayoutService)
        self.widget = self._create_widget()
        self._load_beat_options()

    def _create_widget(self) -> QWidget:
        widget = ModernOptionPickerWidget()
        widget.set_resize_callback(self._on_widget_resize)
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        widget.setMinimumSize(600, 800)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        title = QLabel("Choose Your Next Pictograph")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            QLabel {
                color: #2d3748;
                margin: 5px 0px;
                padding: 8px;
                background: transparent;
            }
        """
        )
        layout.addWidget(title)

        self.filter_widget = OptionPickerFilter()
        self.filter_widget.filter_changed.connect(self._on_filter_changed)
        layout.addWidget(self.filter_widget.widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.sections_container = QWidget()
        self.sections_layout = QVBoxLayout(self.sections_container)
        self.sections_layout.setContentsMargins(5, 5, 5, 5)
        self.sections_layout.setSpacing(8)
        self.sections_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._create_sections()
        scroll_area.setWidget(self.sections_container)
        layout.addWidget(scroll_area, 1)

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

        return widget

    def _create_sections(self):
        for section_type in LetterType.ALL_TYPES:
            section = OptionPickerSection(section_type)
            self._sections[section_type] = section
            if self.sections_layout:
                self.sections_layout.addWidget(section)

    def _load_beat_options(self) -> None:
        """Load beat options for the option picker."""
        # Options will be loaded when start position is selected
        self._beat_options = []
        self._update_beat_display()

    def load_motion_combinations(self, sequence_data: List[Dict[str, Any]]) -> None:
        """Load motion combinations based on sequence data."""
        try:
            from ....application.services.motion_combination_service import (
                MotionCombinationService,
            )

            motion_service = MotionCombinationService()
            combinations = motion_service.generate_motion_combinations(sequence_data)

            self._beat_options = combinations
            self._update_beat_display()

            print(f"✅ Loaded {len(combinations)} motion combinations")

        except Exception as e:
            print(f"❌ Error loading motion combinations: {e}")
            # Fallback to sample data
            self._load_sample_beat_options()

    def _load_sample_beat_options(self) -> None:
        """Load sample beat options as fallback."""
        self._beat_options = [
            BeatData(
                letter="A",
                blue_motion=MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.NORTH,
                    end_loc=Location.NORTH,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.SOUTH,
                ),
            ),
            BeatData(
                letter="B",
                blue_motion=MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                    turns=1.0,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.SOUTH,
                    end_loc=Location.WEST,
                    turns=1.0,
                ),
            ),
            BeatData(
                letter="C",
                blue_motion=MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.EAST,
                    end_loc=Location.WEST,
                ),
            ),
        ]
        self._update_beat_display()

    def _update_beat_display(self) -> None:
        for section in self._sections.values():
            section.clear_pictographs()

        for beat in self._beat_options:
            if beat.letter:
                letter_type = LetterType.get_letter_type(beat.letter)
                frame = ClickablePictographFrame(beat)
                frame.clicked.connect(self._handle_beat_click)

                if letter_type in self._sections:
                    self._sections[letter_type].add_pictograph(frame)

    def _handle_beat_click(self, beat_id: str) -> None:
        self.option_selected.emit(beat_id)

    def _on_widget_resize(self) -> None:
        for section in self._sections.values():
            section.update_layout()

    def _on_filter_changed(self, filter_text: str):
        self._update_beat_display()

    def refresh_options(self) -> None:
        self._load_beat_options()

    def set_enabled(self, enabled: bool) -> None:
        if self.widget:
            self.widget.setEnabled(enabled)

    def get_size(self) -> tuple[int, int]:
        if self._layout_service:
            picker_size = self._layout_service.get_picker_size()
            return (picker_size.width(), picker_size.height())
        return (600, 800)
