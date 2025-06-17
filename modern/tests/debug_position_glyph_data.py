#!/usr/bin/env python3
"""
Debug script to investigate Modern position glyph data extraction issues.

This script will:
1. Load a sample beat from the position matching service
2. Trace how position data flows through the glyph generation pipeline
3. Identify why position glyphs are not being displayed in option picker cards
"""

import sys
import os

# Add the modern src directory to the Python path
modern_src_path = os.path.join(os.path.dirname(__file__), "..", "src")
sys.path.insert(0, os.path.abspath(modern_src_path))


def debug_position_glyph_data():
    """Debug position glyph data extraction and display."""
    print("🔍 DEBUGGING Modern POSITION GLYPH DATA EXTRACTION")
    print("=" * 60)

    try:
        # Import Modern services
        from application.services.positioning.position_matching_service import (
            PositionMatchingService,
        )
        from application.services.core.pictograph_management_service import (
            PictographManagementService,
        )

        # Initialize services
        position_service = PositionMatchingService()
        pictograph_service = PictographManagementService()

        print("✅ Services initialized successfully")

        # Get sample position-matched beats
        print("\n🎯 Getting sample beats from position matching service...")
        sample_beats = position_service.get_next_options("alpha1")

        # Find a cross-position example
        cross_position_beat = None
        for beat in sample_beats:
            start = beat.metadata.get("start_pos", "")
            end = beat.metadata.get("end_pos", "")
            if start.startswith("alpha") and end.startswith("beta"):
                cross_position_beat = beat
                break

        if cross_position_beat:
            print(f"\n🎯 Found cross-position example: {cross_position_beat.letter}")
            print(
                f"   {cross_position_beat.metadata.get('start_pos')} → {cross_position_beat.metadata.get('end_pos')}"
            )

            # Test this specific case
            glyph_data = cross_position_beat.glyph_data
            if glyph_data:
                print(f"   Glyph start_position: {glyph_data.start_position}")
                print(f"   Glyph end_position: {glyph_data.end_position}")

                # Extract alphabetic parts (what the renderer will use)
                start_symbol = "".join(
                    filter(str.isalpha, glyph_data.start_position or "")
                )
                end_symbol = "".join(filter(str.isalpha, glyph_data.end_position or ""))
                print(f"   Rendered as: {start_symbol} → {end_symbol}")

        # Reset to alpha1 for main test
        sample_beats = position_service.get_next_options("alpha1")

        if not sample_beats:
            print("❌ No beats found for alpha1")
            return

        print(f"✅ Found {len(sample_beats)} beats for alpha1")

        # Examine first few beats
        for i, beat_data in enumerate(sample_beats[:3]):
            print(f"\n📊 BEAT {i+1}: {beat_data.letter}")
            print("-" * 40)

            # Check metadata
            print(f"📋 Metadata: {beat_data.metadata}")

            # Check glyph data
            if beat_data.glyph_data:
                glyph = beat_data.glyph_data
                print(f"🎨 Glyph Data:")
                print(f"   start_position: {glyph.start_position}")
                print(f"   end_position: {glyph.end_position}")
                print(f"   show_positions: {glyph.show_positions}")
                print(f"   letter_type: {glyph.letter_type}")
            else:
                print("❌ No glyph data found")

            # Test glyph generation manually
            print(f"🔧 Testing manual glyph generation...")
            try:
                manual_glyph = pictograph_service._generate_glyph_data(beat_data)
                if manual_glyph:
                    print(f"   Manual start_position: {manual_glyph.start_position}")
                    print(f"   Manual end_position: {manual_glyph.end_position}")
                    print(f"   Manual show_positions: {manual_glyph.show_positions}")
                else:
                    print("   ❌ Manual glyph generation failed")
            except Exception as e:
                print(f"   ❌ Manual glyph generation error: {e}")

        # Test position extraction logic directly
        print(f"\n🔍 TESTING POSITION EXTRACTION LOGIC")
        print("-" * 50)

        sample_beat = sample_beats[0]
        print(f"Sample beat metadata: {sample_beat.metadata}")

        # Test the _determine_positions method
        start_pos, end_pos = pictograph_service._determine_positions(sample_beat)
        print(f"Extracted start_pos: {start_pos}")
        print(f"Extracted end_pos: {end_pos}")

        # Check if position data exists in different formats
        print(f"\n📋 CHECKING POSITION DATA FORMATS")
        print("-" * 40)

        # Check direct fields
        print(f"Direct start_pos in metadata: {sample_beat.metadata.get('start_pos')}")
        print(f"Direct end_pos in metadata: {sample_beat.metadata.get('end_pos')}")

        # Check motion-based calculation
        if sample_beat.blue_motion and sample_beat.red_motion:
            blue_start = sample_beat.blue_motion.start_loc
            blue_end = sample_beat.blue_motion.end_loc
            red_start = sample_beat.red_motion.start_loc
            red_end = sample_beat.red_motion.end_loc

            print(f"Blue motion: {blue_start} → {blue_end}")
            print(f"Red motion: {red_start} → {red_end}")

            # Test position mapping
            position_map = {
                ("n", "n"): "alpha1",
                ("n", "e"): "alpha2",
                ("n", "s"): "alpha3",
                ("n", "w"): "alpha4",
                ("e", "n"): "alpha5",
                ("e", "e"): "alpha6",
                ("e", "s"): "alpha7",
                ("e", "w"): "alpha8",
                ("s", "n"): "beta1",
                ("s", "e"): "beta2",
                ("s", "s"): "beta3",
                ("s", "w"): "beta4",
                ("w", "n"): "beta5",
                ("w", "e"): "beta6",
                ("w", "s"): "beta7",
                ("w", "w"): "beta8",
            }

            # Convert Location enums to strings for mapping
            blue_start_str = (
                blue_start.value.lower()
                if hasattr(blue_start, "value")
                else str(blue_start).lower()
            )
            blue_end_str = (
                blue_end.value.lower()
                if hasattr(blue_end, "value")
                else str(blue_end).lower()
            )
            red_start_str = (
                red_start.value.lower()
                if hasattr(red_start, "value")
                else str(red_start).lower()
            )
            red_end_str = (
                red_end.value.lower()
                if hasattr(red_end, "value")
                else str(red_end).lower()
            )

            start_key = (blue_start_str, red_start_str)
            end_key = (blue_end_str, red_end_str)

            calculated_start_pos = position_map.get(start_key)
            calculated_end_pos = position_map.get(end_key)

            print(f"Calculated start position: {start_key} → {calculated_start_pos}")
            print(f"Calculated end position: {end_key} → {calculated_end_pos}")

        print(f"\n✅ Position glyph data debugging complete!")

    except Exception as e:
        print(f"❌ Error during debugging: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    debug_position_glyph_data()
