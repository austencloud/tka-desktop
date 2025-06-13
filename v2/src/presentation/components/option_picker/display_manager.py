from typing import List, Dict
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from ....domain.models.core_models import BeatData
from .option_picker_section import OptionPickerSection
from .pictograph_pool_manager import PictographPoolManager
from .letter_types import LetterType


class OptionPickerDisplayManager:
    """V1-style simple display manager - just add sections to layout"""

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

        print(f"🔧 V1-STYLE DISPLAY MANAGER: Simple approach initialized")

    def create_sections(self) -> None:
        """V1-style: Create sections and simply add them to layout"""
        for section_type in LetterType.ALL_TYPES:
            section = OptionPickerSection(
                section_type,
                parent=self.sections_container,
                mw_size_provider=self.mw_size_provider,
            )
            self._sections[section_type] = section

            # V1 approach: just add to layout, that's it!
            self.sections_layout.addWidget(section)

            print(f"✅ V1-style: Added section {section_type} to layout")

    # V1 approach: no finalization needed, QVBoxLayout just works!

    def update_beat_display(self, beat_options: List[BeatData]) -> None:
        """V1-style: Update beat display simply"""
        print("🔍 UPDATING BEAT DISPLAY")

        # Clear existing pictographs
        for section in self._sections.values():
            section.clear_pictographs_v1_style()

        # Add new pictographs to sections
        pool_index = 0
        for beat in beat_options:
            if pool_index >= self.pool_manager.get_pool_size():
                break

            if beat.letter:
                from ....domain.models.letter_type_classifier import (
                    LetterTypeClassifier,
                )

                letter_type = LetterTypeClassifier.get_letter_type(beat.letter)

                if letter_type in self._sections:
                    target_section = self._sections[letter_type]
                    frame = self.pool_manager.get_pool_frame(pool_index)
                    if frame:
                        frame.update_beat_data(beat)
                        frame.setParent(target_section.pictograph_container)
                        target_section.add_pictograph_from_pool(frame)
                        pool_index += 1
                        print(
                            f"✅ Reused pool object {pool_index} for pictograph {beat.letter}"
                        )

        print("📐 LAYOUT AFTER BEAT DISPLAY UPDATE:")
        self._debug_layout_structure()

    # V1 approach: no complex visibility forcing needed

    def get_sections(self) -> Dict[str, OptionPickerSection]:
        """Get all sections"""
        return self._sections

    def _debug_layout_structure(self) -> None:
        """Simple debug output"""
        print("📐 LAYOUT STRUCTURE ANALYSIS:")
        if self.sections_container:
            print(f"📦 Container visible: {self.sections_container.isVisible()}")

        for i, (section_type, section) in enumerate(self._sections.items()):
            if section:
                section_rect = section.geometry()
                print(
                    f"📄 Section {i} ({section_type}): {section_rect.width()}×{section_rect.height()} at ({section_rect.x()}, {section_rect.y()})"
                )
                print(f"📄 Section {i} visible: {section.isVisible()}")
        print("📐 END LAYOUT ANALYSIS")
