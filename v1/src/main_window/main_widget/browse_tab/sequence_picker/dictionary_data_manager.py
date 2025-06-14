# data_manager.py
import os
import json
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from PIL import Image
from utils.path_helpers import get_data_path


@dataclass
class SequenceRecord:
    word: str
    thumbnails: list[str]
    author: Optional[str] = None
    level: Optional[int] = None
    date_added: Optional[datetime] = None
    grid_mode: Optional[str] = None
    # Add more fields as needed: favorites, length, start_pos, etc.


@dataclass
class DictionaryDataManager:
    """Central place to scan the dictionary folder, parse metadata, and cache a list of SequenceRecords."""

    _loaded_records: list[SequenceRecord] = field(default_factory=list, init=False)
    _has_loaded: bool = field(default=False, init=False)

    def load_all_sequences(self) -> None:
        if self._has_loaded:
            return
        dictionary_dir = get_data_path("dictionary")

        for entry in os.listdir(dictionary_dir):
            full_path = os.path.join(dictionary_dir, entry)
            if not os.path.isdir(full_path) or "__pycache__" in entry:
                continue

            # 1) Find thumbnails
            thumbnails = self._find_thumbnails(full_path)
            if not thumbnails:
                # Maybe skip empty folder or do something else
                continue

            # 2) Build a SequenceRecord
            record = SequenceRecord(
                word=entry,
                thumbnails=thumbnails,
            )

            # 3) Extract metadata from the first thumbnail or from each
            #    (adjust as needed for your existing usage)
            meta = self._extract_metadata_from_any_thumbnail(thumbnails)
            record.author = meta.get("author")
            record.level = meta.get("level")
            record.date_added = meta.get("date_added")
            record.grid_mode = meta.get("grid_mode")
            # etc. for favorites, length, etc.

            self._loaded_records.append(record)

        self._has_loaded = True

    def _find_thumbnails(self, folder: str) -> list[str]:
        """
        Your existing logic to find .png / .jpg / etc.
        But for illustration, you might do:
        """
        # This might be the same code you have in main_widget.thumbnail_finder, or
        # you could keep using that. Just unify the usage. For example:
        all_files = os.listdir(folder)
        # return only images
        return [
            os.path.join(folder, f)
            for f in all_files
            if f.lower().endswith((".png", ".jpg"))  # or whatever
        ]

    def _extract_metadata_from_any_thumbnail(self, thumbnails: list[str]) -> dict:
        """
        For brevity, let's just pick the first one.
        Or you might glean combined info from them all.
        """
        if not thumbnails:
            return {}
        first_thumb = thumbnails[0]
        meta_dict = {}
        try:
            with Image.open(first_thumb) as im:
                info = im.info
                metadata_json = info.get("metadata")
                if metadata_json:
                    metadata: dict = json.loads(metadata_json)
                    raw = metadata.get("sequence", {})[0]
                    # e.g. raw = {"author": "Bob", "level": 2, "date_added": "2023-12-01T10:00:00", ...}
                    meta_dict["author"] = raw.get("author")
                    meta_dict["grid_mode"] = raw.get("grid_mode")
                    meta_dict["level"] = raw.get("level")
                    meta_dict["is_favorite"] = raw.get("is_favorite")

                    date_str = raw.get("date_added")
                    if date_str:
                        try:
                            meta_dict["date_added"] = datetime.fromisoformat(date_str)
                        except ValueError:
                            meta_dict["date_added"] = None

                    # Extract sequence details
                    sequence = raw.get("sequence", [])
                    if sequence:
                        first_sequence = sequence[0]
                        meta_dict["word"] = first_sequence.get("word")
                        meta_dict["prop_type"] = first_sequence.get("prop_type")
                        meta_dict["is_circular"] = first_sequence.get("is_circular")
                        meta_dict["can_be_CAP"] = first_sequence.get("can_be_CAP")
                        meta_dict["is_strict_rotational_CAP"] = first_sequence.get(
                            "is_strict_rotational_CAP"
                        )
                        meta_dict["is_strict_mirrored_CAP"] = first_sequence.get(
                            "is_strict_mirrored_CAP"
                        )
                        meta_dict["is_strict_swapped_CAP"] = first_sequence.get(
                            "is_strict_swapped_CAP"
                        )
                        meta_dict["is_mirrored_swapped_CAP"] = first_sequence.get(
                            "is_mirrored_swapped_CAP"
                        )
                        meta_dict["is_rotational_swapped_CAP"] = first_sequence.get(
                            "is_rotational_swapped_CAP"
                        )
        except FileNotFoundError:
            print(f"[WARNING] Thumbnail not found: {first_thumb}")
        except Exception as e:
            print(f"[ERROR] Problem reading {first_thumb}: {e}")
        return meta_dict

    # -----------------------------------------------------------------
    # Now come the query methods that each filter can use
    # -----------------------------------------------------------------

    def get_all_records(self) -> list[SequenceRecord]:
        """Return everything, or if not yet loaded, load them."""
        self.load_all_sequences()
        return self._loaded_records

    def get_records_by_author(self, author: str) -> list[SequenceRecord]:
        self.load_all_sequences()
        return [r for r in self._loaded_records if r.author == author]

    def get_distinct_authors(self) -> list[str]:
        self.load_all_sequences()
        authors = set()
        for r in self._loaded_records:
            if r.author:
                authors.add(r.author)
        return sorted(authors)

    def get_records_by_level(self, level: int) -> list[SequenceRecord]:
        self.load_all_sequences()
        return [r for r in self._loaded_records if r.level == level]

    def get_distinct_levels(self) -> list[int]:
        self.load_all_sequences()
        lvls = set()
        for r in self._loaded_records:
            if r.level is not None:
                lvls.add(r.level)
        return sorted(lvls)

    def get_records_by_grid_mode(self, mode: str) -> list[SequenceRecord]:
        self.load_all_sequences()
        return [r for r in self._loaded_records if r.grid_mode == mode]

    # etc. for "starting_position", "contains_letter", etc.
    # The main idea: you have a single data set, and each filter is just a "query" on it.

    def get_all_words(self) -> list[str]:
        self.load_all_sequences()
        return [r.word for r in self._loaded_records]

    def get_distinct_sequence_lengths(self) -> list[int]:
        self.load_all_sequences()
        return [len(r.word) for r in self._loaded_records]

    def get_records_by_length(self, length: int) -> list[SequenceRecord]:
        self.load_all_sequences()
        return [r for r in self._loaded_records if len(r.word) == length]
