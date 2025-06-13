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
        """V1-style: Create sections with single-row layout for sections 4,5,6"""
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
            print(f"✅ V1-style: Added section {section_type} to layout")

        # V1-style: Create horizontal container for sections 4, 5, 6 in single row
        self.bottom_row_container = QWidget(self.sections_container)
        self.bottom_row_layout = QHBoxLayout(self.bottom_row_container)
        self.bottom_row_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_row_layout.setSpacing(10)

        # Create sections 4, 5, 6 in horizontal layout
        for section_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
            section = OptionPickerSection(
                section_type,
                parent=self.bottom_row_container,
                mw_size_provider=self.mw_size_provider,
            )
            self._sections[section_type] = section
            self.bottom_row_layout.addWidget(section)

            # CRITICAL: Set proper width for bottom row sections (1/3 each)
            if self.mw_size_provider:
                full_width = self.mw_size_provider().width()
                section_width = (full_width - 20) // 3  # Account for spacing
                section.setFixedWidth(section_width)
                print(
                    f"✅ V1-style: Set bottom row section {section_type} width to {section_width}px (1/3 of {full_width}px)"
                )

            print(f"✅ V1-style: Added section {section_type} to horizontal row")

        # Add the horizontal container to main layout
        self.sections_layout.addWidget(self.bottom_row_container)
        print("✅ V1-style: Added bottom row container with sections 4,5,6")

        # CRITICAL: Make container AND all sections visible after adding all sections
        if self.sections_container:
            self.sections_container.setVisible(True)
            self.sections_container.show()
            print("🔧 CRITICAL: Made sections container visible")

        # CRITICAL: Make all individual sections visible too
        for section_type, section in self._sections.items():
            if section:
                section.setVisible(True)
                section.show()
                print(f"🔧 CRITICAL: Made section {section_type} visible")

                # Also ensure pictograph containers are visible
                if hasattr(section, "pictograph_container"):
                    section.pictograph_container.setVisible(True)
                    section.pictograph_container.show()
                    print(
                        f"🔧 CRITICAL: Made section {section_type} pictograph container visible"
                    )

        # CRITICAL: Make bottom row container visible too
        if hasattr(self, "bottom_row_container"):
            self.bottom_row_container.setVisible(True)
            self.bottom_row_container.show()
            print("🔧 CRITICAL: Made bottom row container visible")

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
                print(
                    f"🔧 Resized bottom row section {section_type} to {section_width}px (1/3 of {full_width}px)"
                )
