from typing import Any, Optional
from data.constants import (
    BLUE,
    BLUE_ATTRS,
    END_ORI,
    END_POS,
    NO_ROT,
    PROP_ROT_DIR,
    RED,
    RED_ATTRS,
    START_ORI,
    START_POS,
)
from interfaces.json_manager_interface import IJsonManager


class OptionGetter:
    def __init__(
        self,
        pictograph_dataset: dict[Any, list[dict[str, Any]]],
        json_manager: IJsonManager,
    ) -> None:
        self.pictograph_dataset = pictograph_dataset
        self.ori_calculator = json_manager.ori_calculator
        self.ori_validation_engine = json_manager.ori_validation_engine

    def get_next_options(
        self, sequence: list[dict[str, Any]], selected_filter: Optional[str] = None
    ) -> list[dict[str, Any]]:
        print("\n" + "=" * 80)
        print("🔍 V1 MOTION GENERATION ANALYSIS - get_next_options()")
        print("=" * 80)
        print(f"📊 Input sequence length: {len(sequence)}")
        if sequence:
            last_beat = sequence[-1]
            print(f"📍 Last beat end_pos: {last_beat.get('end_pos', 'N/A')}")
            print(
                f"🔵 Last blue end_ori: {last_beat.get('blue_attributes', {}).get('end_ori', 'N/A')}"
            )
            print(
                f"🔴 Last red end_ori: {last_beat.get('red_attributes', {}).get('end_ori', 'N/A')}"
            )

        options = self._load_all_next_option_dicts(sequence)
        print(f"🎯 Raw options found: {len(options)}")

        if selected_filter is not None:
            print(f"🔧 Applying filter: {selected_filter}")
            options = [
                o
                for o in options
                if self._determine_reversal_filter(sequence, o) == selected_filter
            ]
            print(f"🎯 Filtered options: {len(options)}")

        self.update_orientations(sequence, options)

        print(f"✅ Final options count: {len(options)}")
        for i, option in enumerate(options[:10]):  # Show first 10
            letter = option.get("letter", "Unknown")
            start_pos = option.get("start_pos", "N/A")
            end_pos = option.get("end_pos", "N/A")
            print(f"   {i+1:2d}. Letter: {letter}, {start_pos} → {end_pos}")
        if len(options) > 10:
            print(f"   ... and {len(options) - 10} more options")
        print("=" * 80)

        return options

    def update_orientations(
        self, sequence: list[dict[str, Any]], options: list[dict[str, Any]]
    ) -> None:
        # Validate sequence is not empty before accessing last element
        if not sequence:
            return  # No orientations to update if sequence is empty

        last = sequence[-1]
        for option in options:
            option[BLUE_ATTRS][START_ORI] = last[BLUE_ATTRS][END_ORI]
            option[RED_ATTRS][START_ORI] = last[RED_ATTRS][END_ORI]
            option[BLUE_ATTRS][END_ORI] = self.ori_calculator.calculate_end_ori(
                option, BLUE
            )
            option[RED_ATTRS][END_ORI] = self.ori_calculator.calculate_end_ori(
                option, RED
            )

    def _load_all_next_option_dicts(
        self, sequence: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        print("\n🔍 V1 DATASET QUERY ANALYSIS - _load_all_next_option_dicts()")
        print("-" * 60)

        next_opts: list[dict[str, Any]] = []
        if not sequence:
            print("❌ Empty sequence - no options to load")
            return next_opts

        # Additional safety check for sequence length
        if len(sequence) < 1:
            print("❌ Sequence too short - no options to load")
            return next_opts

        # Handle placeholder case with additional safety check
        if sequence[-1].get("is_placeholder") and len(sequence) >= 2:
            last = sequence[-2]
            print("📍 Using second-to-last beat (placeholder detected)")
        else:
            last = sequence[-1]
            print("📍 Using last beat")

        start = last.get(END_POS)
        print(f"🎯 Searching for options with START_POS = '{start}'")

        if start:
            dataset_groups_checked = 0
            total_items_checked = 0
            matches_found = 0

            for group_key, group in self.pictograph_dataset.items():
                dataset_groups_checked += 1
                for item in group:
                    total_items_checked += 1
                    if item.get(START_POS) == start:
                        letter = item.get("letter", "Unknown")
                        end_pos = item.get(END_POS, "N/A")
                        matches_found += 1
                        next_opts.append(item)
                        print(
                            f"   ✅ Match {matches_found}: Letter {letter}, {start} → {end_pos}"
                        )

            print(f"📊 Dataset search complete:")
            print(f"   - Groups checked: {dataset_groups_checked}")
            print(f"   - Total items checked: {total_items_checked}")
            print(f"   - Matches found: {matches_found}")
        else:
            print("❌ No start position found in last beat")

        print(f"🔧 Applying orientation updates to {len(next_opts)} options...")
        for o in next_opts:
            for color in (BLUE, RED):
                o[f"{color}_attributes"][START_ORI] = last[f"{color}_attributes"][
                    END_ORI
                ]
            self.ori_validation_engine.validate_single_pictograph(o, last)

        print(f"✅ Returning {len(next_opts)} validated options")
        print("-" * 60)
        return next_opts

    def _determine_reversal_filter(
        self, sequence: list[dict[str, Any]], o: dict[str, Any]
    ) -> str:
        blue_cont, red_cont = self._check_continuity(sequence, o)
        if blue_cont and red_cont:
            return "continuous"
        elif blue_cont ^ red_cont:
            return "one_reversal"
        return "two_reversals"

    def _check_continuity(
        self, sequence: list[dict[str, Any]], o: dict[str, Any]
    ) -> tuple[bool, bool]:
        def get_last_rot(seq: list[dict[str, Any]], color: str) -> Optional[str]:
            for item in reversed(seq):
                rot = item.get(f"{color}_attributes", {}).get(PROP_ROT_DIR)
                if rot and rot != NO_ROT:
                    return rot
            return None

        last_blue = get_last_rot(sequence, BLUE)
        last_red = get_last_rot(sequence, RED)
        curr_blue = o.get(BLUE_ATTRS, {}).get(PROP_ROT_DIR, NO_ROT)
        curr_red = o.get(RED_ATTRS, {}).get(PROP_ROT_DIR, NO_ROT)
        if curr_blue == NO_ROT:
            curr_blue = last_blue
        if curr_red == NO_ROT:
            curr_red = last_red
        blue_cont = last_blue is None or curr_blue is None or curr_blue == last_blue
        red_cont = last_red is None or curr_red is None or curr_red == last_red
        return blue_cont, red_cont
