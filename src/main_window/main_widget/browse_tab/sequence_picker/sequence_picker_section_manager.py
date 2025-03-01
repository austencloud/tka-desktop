import json
from datetime import datetime
from typing import TYPE_CHECKING
from enums.letter.letter_type import LetterType
from ..browse_tab_section_header import BrowseTabSectionHeader
from PIL import Image

if TYPE_CHECKING:
    from .sequence_picker import SequencePicker


class SequencePickerSectionManager:
    def __init__(self, sequence_picker: "SequencePicker"):
        self.sequence_picker = sequence_picker

    def add_header(self, row_index, num_columns, section):
        header_title = f"{section}"
        header = BrowseTabSectionHeader(header_title)
        self.sequence_picker.scroll_widget.section_headers[section] = header
        self.sequence_picker.scroll_widget.grid_layout.addWidget(
            header, row_index, 0, 1, num_columns
        )

    def get_sorted_sections(self, sort_method: str, sections: list[str]) -> list[str]:
        if sort_method == "sequence_length":
            sorted_sections = sorted(
                sections, key=lambda x: int(x) if x.isdigit() else x
            )
        elif sort_method == "date_added":
            sorted_sections = sorted(
                [s for s in sections if s != "Unknown"],
                key=lambda x: datetime.strptime(x, "%m-%d-%Y"),
                reverse=True,
            )

            if "Unknown" in sections:
                sorted_sections.append("Unknown")
        else:
            sorted_sections = sorted(sections, key=self.custom_sort_key)
        return sorted_sections

    def custom_sort_key(self, section_str: str) -> tuple[int, int]:
        return LetterType.sort_key(section_str)

    def get_section_from_word(
        self, word, sort_order, sequence_length=None, thumbnails=None
    ):
        if sort_order == "sequence_length":
            return str(sequence_length) if sequence_length is not None else "Unknown"
        elif sort_order == "date_added":
            if thumbnails:
                date_added = self.get_date_added(thumbnails)
                return date_added.strftime("%m-%d-%Y") if date_added else "Unknown"
            return "Unknown"
        else:
            section: str = word[:2] if len(word) > 1 and word[1] == "-" else word[0]
            if not section.isdigit():
                if section[0] in set(["α", "β", "θ"]):
                    section = section.lower()
                else:
                    section = section.upper()
            return section

    def get_date_added(self, thumbnails):
        dates = []
        for thumbnail in thumbnails:
            image = Image.open(thumbnail)
            info = image.info
            metadata = info.get("metadata")
            if metadata:
                metadata_dict = json.loads(metadata)
                date_added = metadata_dict.get("date_added")
                if date_added:
                    try:
                        dates.append(datetime.fromisoformat(date_added))
                    except ValueError:
                        pass

        return max(dates, default=datetime.min)
