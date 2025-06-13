from typing import TYPE_CHECKING
import os
from enums.letter.letter_type import LetterType
from main_window.main_widget.fade_manager.fade_manager import FadeManager
from interfaces.json_manager_interface import IJsonManager

if TYPE_CHECKING:
    from ..widgets.option_picker import OptionPicker


class OptionUpdater:
    def __init__(
        self,
        option_picker: "OptionPicker",
        fade_manager: FadeManager,
        json_manager: IJsonManager,
    ) -> None:
        self.option_picker = option_picker
        self.scroll_area = option_picker.option_scroll
        self.fade_manager = fade_manager
        self.json_loader = json_manager.loader_saver
        self.app_root = self._get_app_root()

    def _get_app_root(self) -> str:
        current_file = os.path.abspath(__file__)
        return os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

    def refresh_options(self) -> None:
        sequence = self.json_loader.load_current_sequence()
        if len(sequence) <= 1:
            return
        sections = self.scroll_area.sections
        frames = [section.pictograph_frame for section in sections.values()]

        self.fade_manager.widget_fader.fade_and_update(frames, self.update_options, 200)

    def update_options(self) -> None:
        print("\n" + "🔄" * 40)
        print("🔄 V1 OPTION UPDATER ANALYSIS - update_options()")
        print("🔄" * 40)

        sequence = self.json_loader.load_current_sequence()
        sequence_without_metdata = sequence[1:]

        print(f"📊 Full sequence length: {len(sequence)}")
        print(f"📊 Sequence without metadata: {len(sequence_without_metdata)}")

        # Get the selected filter if the reversal_filter is available
        selected_filter = None
        if hasattr(self.option_picker, "reversal_filter"):
            selected_filter = (
                self.option_picker.reversal_filter.reversal_combobox.currentData()
            )
        print(f"🔧 Selected filter: {selected_filter}")

        next_options = self.option_picker.option_getter.get_next_options(
            sequence_without_metdata, selected_filter
        )

        print(f"\n📋 SECTIONAL ASSIGNMENT ANALYSIS:")
        print(f"   Available option pool size: {len(self.option_picker.option_pool)}")
        print(f"   Next options to assign: {len(next_options)}")

        for section in self.option_picker.option_scroll.sections.values():
            section.clear_pictographs()

        section_assignments = {}
        for i, option_data in enumerate(next_options):
            if i >= len(self.option_picker.option_pool):
                print(f"⚠️  Reached option pool limit at index {i}")
                break
            option = self.option_picker.option_pool[i]
            option.managers.updater.update_pictograph(option_data)
            option.elements.view.update_borders()

            letter = option.state.letter
            letter_type = LetterType.get_letter_type(letter)
            section = self.option_picker.option_scroll.sections.get(letter_type)

            if section:
                section.add_pictograph(option)
                if letter_type not in section_assignments:
                    section_assignments[letter_type] = []
                section_assignments[letter_type].append(letter)
                print(f"   ✅ Assigned Letter {letter} to Section {letter_type}")
            else:
                print(
                    f"   ❌ No section found for Letter {letter} (type: {letter_type})"
                )

        print(f"\n📊 FINAL SECTION SUMMARY:")
        for section_name, letters in section_assignments.items():
            print(f"   {section_name}: {letters} ({len(letters)} pictographs)")

        print("🔄" * 40)
