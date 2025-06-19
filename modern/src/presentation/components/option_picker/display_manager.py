from typing import List, Dict
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from domain.models.core_models import BeatData
from .option_picker_section import OptionPickerSection
from .pictograph_pool_manager import PictographPoolManager
from .letter_types import LetterType


class OptionPickerDisplayManager:
    """Legacy-style simple display manager - just add sections to layout"""

    def __init__(
        self,
        sections_container: QWidget,
        sections_layout: QVBoxLayout,
        pool_manager: PictographPoolManager,
        mw_size_provider=None,
    ):
        self.sections_container = sections_container
        self.sections_layout = sections_layout
        self.pool_manager = pool_manager
        self.mw_size_provider = mw_size_provider
        self._sections: Dict[str, OptionPickerSection] = {}

    def create_sections(self) -> None:
        """Legacy-style: Create sections with single-row layout for sections 4,5,6"""
        from PyQt6.QtWidgets import QHBoxLayout, QWidget

        # Create sections 1, 2, 3 normally (vertical layout)
        for section_type in [LetterType.TYPE1, LetterType.TYPE2, LetterType.TYPE3]:
            section = OptionPickerSection(
                section_type,
                parent=self.sections_container,
                mw_size_provider=self.mw_size_provider,
            )
            self._sections[section_type] = section
            self.sections_layout.addWidget(section)

        # Legacy-style: Create transparent horizontal container for sections 4, 5, 6
        self.bottom_row_container = QWidget(self.sections_container)
        self.bottom_row_container.setStyleSheet(
            "background: transparent; border: none;"
        )
        self.bottom_row_layout = QHBoxLayout(self.bottom_row_container)
        self.bottom_row_layout.setContentsMargins(5, 0, 5, 0)  # Reduced margins
        self.bottom_row_layout.setSpacing(8)  # Reduced spacing

        # Create sections 4, 5, 6 in horizontal layout
        for section_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
            section = OptionPickerSection(
                section_type,
                parent=self.bottom_row_container,
                mw_size_provider=self.mw_size_provider,
            )
            self._sections[section_type] = section
            self.bottom_row_layout.addWidget(section)

            # Calculate proper width accounting for margins and spacing
            if self.mw_size_provider:
                full_width = self.mw_size_provider().width()
                total_margins = 10  # Left + right margins
                total_spacing = 16  # 2 spacing gaps between 3 sections
                available_width = full_width - total_margins - total_spacing
                section_width = available_width // 3
                section.setFixedWidth(section_width)

        self.sections_layout.addWidget(self.bottom_row_container)

        # Make all containers transparent
        if self.sections_container:
            self.sections_container.setVisible(True)
            self.sections_container.show()

        for section_type, section in self._sections.items():
            if section:
                section.setVisible(True)
                section.show()
                if hasattr(section, "pictograph_container"):
                    section.pictograph_container.setVisible(True)
                    section.pictograph_container.show()

        if hasattr(self, "bottom_row_container"):
            self.bottom_row_container.setVisible(True)
            self.bottom_row_container.show()

    # Legacy approach: no finalization needed, QVBoxLayout just works!

    def update_beat_display(self, beat_options: List[BeatData]) -> None:
        """Optimized: Batch update beat display for instant performance"""
        try:
            # Batch all operations to minimize UI updates
            self._batch_update_beat_display(beat_options)
        except Exception as e:
            print(f"❌ Error in batched beat display update: {e}")
            # Fallback to original method
            self._fallback_update_beat_display(beat_options)

    def _batch_update_beat_display(self, beat_options: List[BeatData]) -> None:
        """Optimized batch update implementation"""
        from domain.models.letter_type_classifier import LetterTypeClassifier

        # Step 1: Clear all sections in one pass
        for section in self._sections.values():
            section.clear_pictographs_legacy_style()

        # Step 2: Pre-categorize beats by letter type to minimize lookups
        beats_by_type = {}
        for i, beat in enumerate(beat_options):
            if i >= self.pool_manager.get_pool_size():
                break
            if beat.letter:
                letter_type = LetterTypeClassifier.get_letter_type(beat.letter)
                if letter_type in self._sections:
                    if letter_type not in beats_by_type:
                        beats_by_type[letter_type] = []
                    beats_by_type[letter_type].append((i, beat))

        # Step 3: Batch update frames and add to sections
        for letter_type, beat_list in beats_by_type.items():
            target_section = self._sections[letter_type]
            for pool_index, beat in beat_list:
                frame = self.pool_manager.get_pool_frame(pool_index)
                if frame:
                    frame.update_beat_data(beat)
                    frame.setParent(target_section.pictograph_container)
                    target_section.add_pictograph_from_pool(frame)

    def _fallback_update_beat_display(self, beat_options: List[BeatData]) -> None:
        """Fallback to original implementation if batch update fails"""
        from domain.models.letter_type_classifier import LetterTypeClassifier

        # Clear existing pictographs
        for section in self._sections.values():
            section.clear_pictographs_legacy_style()

        # Add new pictographs to sections
        pool_index = 0
        for beat in beat_options:
            if pool_index >= self.pool_manager.get_pool_size():
                break

            if beat.letter:
                letter_type = LetterTypeClassifier.get_letter_type(beat.letter)

                if letter_type in self._sections:
                    target_section = self._sections[letter_type]
                    frame = self.pool_manager.get_pool_frame(pool_index)
                    if frame:
                        frame.update_beat_data(beat)
                        frame.setParent(target_section.pictograph_container)
                        target_section.add_pictograph_from_pool(frame)
                        pool_index += 1

    # Legacy approach: no complex visibility forcing needed

    def get_sections(self) -> Dict[str, OptionPickerSection]:
        """Get all created sections"""
        return self._sections.copy()

    def resize_bottom_row_sections(self):
        """Resize bottom row sections to proper 1/3 width when window resizes"""
        if not self.mw_size_provider:
            return

        full_width = self.mw_size_provider().width()
        section_width = (full_width - 20) // 3  # Account for spacing

        for section_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
            if section_type in self._sections:
                section = self._sections[section_type]
                section.setFixedWidth(section_width)

    def display_pictographs(self, pictographs_by_type, sections):
        available_pictographs = sum(
            len(frames) for frames in pictographs_by_type.values()
        )

        if available_pictographs == 0:
            return

        for letter_type, pictograph_frames in pictographs_by_type.items():
            if letter_type not in sections:
                continue

            section = sections[letter_type]
            for pictograph_frame in pictograph_frames:
                section.add_pictograph_from_pool(pictograph_frame)

        self._ensure_visibility(sections)

    def _ensure_visibility(self, sections):
        for section in sections.values():
            if section:
                section.setVisible(True)
                section.show()
                if hasattr(section, "pictograph_container"):
                    section.pictograph_container.setVisible(True)
                    section.pictograph_container.show()
