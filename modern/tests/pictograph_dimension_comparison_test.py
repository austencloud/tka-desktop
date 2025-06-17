"""
Automated comparison testing for Legacy vs Modern pictograph dimensions.

This test creates side-by-side renderings of identical pictographs in both Legacy and Modern
and compares their dimensions to identify discrepancies.
"""

import sys
import os
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QPainter

# Add paths for both Legacy and Modern
current_dir = os.path.dirname(os.path.abspath(__file__))
legacy_src_path = os.path.join(current_dir, "..", "..", "legacy", "src")
modern_src_path = os.path.join(current_dir, "..", "src")

sys.path.insert(0, legacy_src_path)
sys.path.insert(0, modern_src_path)

print(f"Legacy path: {legacy_src_path}")
print(f"Modern path: {modern_src_path}")
print(f"Legacy exists: {os.path.exists(legacy_src_path)}")
print(f"Modern exists: {os.path.exists(modern_src_path)}")


@dataclass
class DimensionComparison:
    """Results of comparing Legacy and Modern pictograph dimensions."""

    legacy_component_size: Tuple[int, int]
    modern_component_size: Tuple[int, int]
    legacy_scene_size: Tuple[float, float]
    modern_scene_size: Tuple[float, float]
    legacy_scale: Tuple[float, float]
    modern_scale: Tuple[float, float]
    legacy_effective_size: Tuple[float, float]
    modern_effective_size: Tuple[float, float]
    legacy_tka_size: Optional[Tuple[float, float]]
    modern_tka_size: Optional[Tuple[float, float]]

    def size_difference_percentage(self) -> float:
        """Calculate percentage difference in effective pictograph size."""
        legacy_area = self.legacy_effective_size[0] * self.legacy_effective_size[1]
        modern_area = self.modern_effective_size[0] * self.modern_effective_size[1]
        if legacy_area == 0:
            return 0.0
        return ((modern_area - legacy_area) / legacy_area) * 100

    def tka_size_difference_percentage(self) -> Optional[float]:
        """Calculate percentage difference in TKA glyph size."""
        if not self.legacy_tka_size or not self.modern_tka_size:
            return None
        legacy_area = self.legacy_tka_size[0] * self.legacy_tka_size[1]
        modern_area = self.modern_tka_size[0] * self.modern_tka_size[1]
        if legacy_area == 0:
            return 0.0
        return ((modern_area - legacy_area) / legacy_area) * 100


class PictographComparisonTest:
    """Automated testing framework for comparing Legacy and Modern pictograph dimensions."""

    def __init__(self):
        self.app = None
        self.legacy_pictograph = None
        self.modern_pictograph = None
        self.comparison_widget = None

    def setup_test_environment(self) -> bool:
        """Setup the test environment with both Legacy and Modern components."""
        try:
            # Create QApplication if it doesn't exist
            if not QApplication.instance():
                self.app = QApplication(sys.argv)

            # Import Legacy components
            from base_widgets.pictograph.pictograph import (
                Pictograph as LegacyPictograph,
            )
            from base_widgets.pictograph.elements.views.base_pictograph_view import (
                BasePictographView,
            )

            # Import Modern components
            from presentation.components.pictograph.pictograph_component import (
                PictographComponent,
            )
            from domain.models.core_models import (
                BeatData,
                MotionData,
                GlyphData,
                LetterType,
            )

            # Create Legacy pictograph
            self.legacy_pictograph = LegacyPictograph()
            self.legacy_view = BasePictographView(self.legacy_pictograph)
            self.legacy_view.setFixedSize(400, 400)

            # Create Modern pictograph
            self.modern_pictograph = PictographComponent()
            self.modern_pictograph.setFixedSize(400, 400)

            print("✅ Test environment setup successful")
            return True

        except Exception as e:
            print(f"❌ Failed to setup test environment: {e}")
            return False

    def create_test_beat_data(self) -> Any:
        """Create test beat data for comparison."""
        try:
            from domain.models.core_models import (
                BeatData,
                MotionData,
                GlyphData,
                LetterType,
                Location,
                MotionType,
            )

            # Create simple test motion data
            blue_motion = MotionData(
                motion_type=MotionType.PRO,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=1.0,
            )

            # Create glyph data with TKA
            glyph_data = GlyphData(
                letter_type=LetterType.Type1,
                show_tka=True,
                show_vtg=False,
                show_elemental=False,
                show_positions=False,
            )

            # Create beat data
            beat_data = BeatData(
                letter="A", blue_motion=blue_motion, glyph_data=glyph_data
            )

            return beat_data

        except Exception as e:
            print(f"❌ Failed to create test beat data: {e}")
            return None

    def update_pictographs_with_test_data(self, beat_data: Any) -> bool:
        """Update both Legacy and Modern pictographs with the same test data."""
        try:
            # Update Modern pictograph
            self.modern_pictograph.update_from_beat(beat_data)

            # Update Legacy pictograph (convert beat_data to Legacy format)
            legacy_data = self._convert_beat_data_to_legacy_format(beat_data)
            self.legacy_pictograph.managers.updater.update_pictograph(legacy_data)

            print("✅ Both pictographs updated with test data")
            return True

        except Exception as e:
            print(f"❌ Failed to update pictographs: {e}")
            return False

    def _convert_beat_data_to_legacy_format(self, beat_data: Any) -> Dict[str, Any]:
        """Convert Modern BeatData to Legacy pictograph data format."""
        # This is a simplified conversion - in a real test, this would need
        # to be more comprehensive to match Legacy's exact data structure
        return {
            "letter": beat_data.letter,
            "start_pos": "alpha1",
            "end_pos": "alpha3",
            "timing": "1",
            "direction": "cw",
            "blue_attrs": {
                "motion_type": "pro",
                "start_loc": "n",
                "end_loc": "s",
                "prop_rot_dir": "cw",
                "turns": 1.0,
            },
            "red_attrs": {
                "motion_type": "static",
                "start_loc": "n",
                "end_loc": "n",
                "prop_rot_dir": "no_rot",
                "turns": 0.0,
            },
        }

    def capture_dimensions(self) -> Optional[DimensionComparison]:
        """Capture and compare dimensions from both pictographs."""
        try:
            # Force rendering and layout updates
            self.legacy_view.update()
            self.modern_pictograph.update()

            # Process events to ensure rendering is complete
            if self.app:
                self.app.processEvents()

            # Capture Legacy dimensions
            legacy_component_size = (
                self.legacy_view.size().width(),
                self.legacy_view.size().height(),
            )
            legacy_scene_rect = self.legacy_view.sceneRect()
            legacy_scene_size = (legacy_scene_rect.width(), legacy_scene_rect.height())
            legacy_transform = self.legacy_view.transform()
            legacy_scale = (legacy_transform.m11(), legacy_transform.m22())
            legacy_effective_size = (
                legacy_scene_size[0] * legacy_scale[0],
                legacy_scene_size[1] * legacy_scale[1],
            )

            # Capture Modern dimensions
            modern_component_size = (
                self.modern_pictograph.size().width(),
                self.modern_pictograph.size().height(),
            )
            modern_scene_rect = self.modern_pictograph.scene.sceneRect()
            modern_scene_size = (modern_scene_rect.width(), modern_scene_rect.height())
            modern_transform = self.modern_pictograph.transform()
            modern_scale = (modern_transform.m11(), modern_transform.m22())
            modern_effective_size = (
                modern_scene_size[0] * modern_scale[0],
                modern_scene_size[1] * modern_scale[1],
            )

            # Capture TKA glyph dimensions (simplified)
            legacy_tka_size = self._get_legacy_tka_dimensions()
            modern_tka_size = self._get_modern_tka_dimensions()

            comparison = DimensionComparison(
                legacy_component_size=legacy_component_size,
                modern_component_size=modern_component_size,
                legacy_scene_size=legacy_scene_size,
                modern_scene_size=modern_scene_size,
                legacy_scale=legacy_scale,
                modern_scale=modern_scale,
                legacy_effective_size=legacy_effective_size,
                modern_effective_size=modern_effective_size,
                legacy_tka_size=legacy_tka_size,
                modern_tka_size=modern_tka_size,
            )

            return comparison

        except Exception as e:
            print(f"❌ Failed to capture dimensions: {e}")
            return None

    def _get_legacy_tka_dimensions(self) -> Optional[Tuple[float, float]]:
        """Get Legacy TKA glyph dimensions."""
        try:
            if (
                hasattr(self.legacy_pictograph.elements, "tka_glyph")
                and self.legacy_pictograph.elements.tka_glyph
            ):
                tka_rect = self.legacy_pictograph.elements.tka_glyph.sceneBoundingRect()
                return (tka_rect.width(), tka_rect.height())
        except:
            pass
        return None

    def _get_modern_tka_dimensions(self) -> Optional[Tuple[float, float]]:
        """Get Modern TKA glyph dimensions."""
        try:
            if self.modern_pictograph.scene:
                for item in self.modern_pictograph.scene.items():
                    if hasattr(item, "childItems") and item.childItems():
                        # This is a simplified check - in reality would need better TKA detection
                        scene_rect = item.sceneBoundingRect()
                        return (scene_rect.width(), scene_rect.height())
        except:
            pass
        return None

    def print_comparison_report(self, comparison: DimensionComparison) -> None:
        """Print detailed comparison report."""
        print("\n" + "=" * 80)
        print("📊 PICTOGRAPH DIMENSION COMPARISON REPORT")
        print("=" * 80)

        print(f"\n📐 COMPONENT SIZES:")
        print(
            f"   Legacy: {comparison.legacy_component_size[0]}x{comparison.legacy_component_size[1]}"
        )
        print(
            f"   Modern: {comparison.modern_component_size[0]}x{comparison.modern_component_size[1]}"
        )

        print(f"\n📐 SCENE SIZES:")
        print(
            f"   Legacy: {comparison.legacy_scene_size[0]:.1f}x{comparison.legacy_scene_size[1]:.1f}"
        )
        print(
            f"   Modern: {comparison.modern_scene_size[0]:.1f}x{comparison.modern_scene_size[1]:.1f}"
        )

        print(f"\n📐 VIEW SCALES:")
        print(
            f"   Legacy: {comparison.legacy_scale[0]:.4f}x{comparison.legacy_scale[1]:.4f}"
        )
        print(
            f"   Modern: {comparison.modern_scale[0]:.4f}x{comparison.modern_scale[1]:.4f}"
        )

        print(f"\n📐 EFFECTIVE SIZES:")
        print(
            f"   Legacy: {comparison.legacy_effective_size[0]:.1f}x{comparison.legacy_effective_size[1]:.1f}"
        )
        print(
            f"   Modern: {comparison.modern_effective_size[0]:.1f}x{comparison.modern_effective_size[1]:.1f}"
        )

        size_diff = comparison.size_difference_percentage()
        print(f"\n📊 SIZE DIFFERENCE: {size_diff:+.1f}%")

        if comparison.legacy_tka_size and comparison.modern_tka_size:
            print(f"\n🔤 TKA GLYPH SIZES:")
            print(
                f"   Legacy: {comparison.legacy_tka_size[0]:.1f}x{comparison.legacy_tka_size[1]:.1f}"
            )
            print(
                f"   Modern: {comparison.modern_tka_size[0]:.1f}x{comparison.modern_tka_size[1]:.1f}"
            )

            tka_diff = comparison.tka_size_difference_percentage()
            if tka_diff is not None:
                print(f"   TKA Difference: {tka_diff:+.1f}%")

        print("=" * 80)
        print()


def run_comparison_test():
    """Run the automated comparison test."""
    print("🚀 Starting Pictograph Dimension Comparison Test")

    test = PictographComparisonTest()

    # Setup test environment
    if not test.setup_test_environment():
        return False

    # Create test data
    beat_data = test.create_test_beat_data()
    if not beat_data:
        return False

    # Update pictographs
    if not test.update_pictographs_with_test_data(beat_data):
        return False

    # Wait for rendering to complete
    QTimer.singleShot(500, lambda: None)
    if test.app:
        test.app.processEvents()

    # Capture and compare dimensions
    comparison = test.capture_dimensions()
    if not comparison:
        return False

    # Print report
    test.print_comparison_report(comparison)

    print("✅ Comparison test completed successfully")
    return True


if __name__ == "__main__":
    success = run_comparison_test()
    sys.exit(0 if success else 1)
