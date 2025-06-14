"""
Automated comparison testing for V1 vs V2 pictograph dimensions.

This test creates side-by-side renderings of identical pictographs in both V1 and V2
and compares their dimensions to identify discrepancies.
"""

import sys
import os
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QPainter

# Add paths for both V1 and V2
current_dir = os.path.dirname(os.path.abspath(__file__))
v1_src_path = os.path.join(current_dir, "..", "..", "v1", "src")
v2_src_path = os.path.join(current_dir, "..", "src")

sys.path.insert(0, v1_src_path)
sys.path.insert(0, v2_src_path)

print(f"V1 path: {v1_src_path}")
print(f"V2 path: {v2_src_path}")
print(f"V1 exists: {os.path.exists(v1_src_path)}")
print(f"V2 exists: {os.path.exists(v2_src_path)}")


@dataclass
class DimensionComparison:
    """Results of comparing V1 and V2 pictograph dimensions."""

    v1_component_size: Tuple[int, int]
    v2_component_size: Tuple[int, int]
    v1_scene_size: Tuple[float, float]
    v2_scene_size: Tuple[float, float]
    v1_scale: Tuple[float, float]
    v2_scale: Tuple[float, float]
    v1_effective_size: Tuple[float, float]
    v2_effective_size: Tuple[float, float]
    v1_tka_size: Optional[Tuple[float, float]]
    v2_tka_size: Optional[Tuple[float, float]]

    def size_difference_percentage(self) -> float:
        """Calculate percentage difference in effective pictograph size."""
        v1_area = self.v1_effective_size[0] * self.v1_effective_size[1]
        v2_area = self.v2_effective_size[0] * self.v2_effective_size[1]
        if v1_area == 0:
            return 0.0
        return ((v2_area - v1_area) / v1_area) * 100

    def tka_size_difference_percentage(self) -> Optional[float]:
        """Calculate percentage difference in TKA glyph size."""
        if not self.v1_tka_size or not self.v2_tka_size:
            return None
        v1_area = self.v1_tka_size[0] * self.v1_tka_size[1]
        v2_area = self.v2_tka_size[0] * self.v2_tka_size[1]
        if v1_area == 0:
            return 0.0
        return ((v2_area - v1_area) / v1_area) * 100


class PictographComparisonTest:
    """Automated testing framework for comparing V1 and V2 pictograph dimensions."""

    def __init__(self):
        self.app = None
        self.v1_pictograph = None
        self.v2_pictograph = None
        self.comparison_widget = None

    def setup_test_environment(self) -> bool:
        """Setup the test environment with both V1 and V2 components."""
        try:
            # Create QApplication if it doesn't exist
            if not QApplication.instance():
                self.app = QApplication(sys.argv)

            # Import V1 components
            from base_widgets.pictograph.pictograph import Pictograph as V1Pictograph
            from base_widgets.pictograph.elements.views.base_pictograph_view import (
                BasePictographView,
            )

            # Import V2 components
            from presentation.components.pictograph.pictograph_component import (
                PictographComponent,
            )
            from domain.models.core_models import (
                BeatData,
                MotionData,
                GlyphData,
                LetterType,
            )

            # Create V1 pictograph
            self.v1_pictograph = V1Pictograph()
            self.v1_view = BasePictographView(self.v1_pictograph)
            self.v1_view.setFixedSize(400, 400)

            # Create V2 pictograph
            self.v2_pictograph = PictographComponent()
            self.v2_pictograph.setFixedSize(400, 400)

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
        """Update both V1 and V2 pictographs with the same test data."""
        try:
            # Update V2 pictograph
            self.v2_pictograph.update_from_beat(beat_data)

            # Update V1 pictograph (convert beat_data to V1 format)
            v1_data = self._convert_beat_data_to_v1_format(beat_data)
            self.v1_pictograph.managers.updater.update_pictograph(v1_data)

            print("✅ Both pictographs updated with test data")
            return True

        except Exception as e:
            print(f"❌ Failed to update pictographs: {e}")
            return False

    def _convert_beat_data_to_v1_format(self, beat_data: Any) -> Dict[str, Any]:
        """Convert V2 BeatData to V1 pictograph data format."""
        # This is a simplified conversion - in a real test, this would need
        # to be more comprehensive to match V1's exact data structure
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
            self.v1_view.update()
            self.v2_pictograph.update()

            # Process events to ensure rendering is complete
            if self.app:
                self.app.processEvents()

            # Capture V1 dimensions
            v1_component_size = (
                self.v1_view.size().width(),
                self.v1_view.size().height(),
            )
            v1_scene_rect = self.v1_view.sceneRect()
            v1_scene_size = (v1_scene_rect.width(), v1_scene_rect.height())
            v1_transform = self.v1_view.transform()
            v1_scale = (v1_transform.m11(), v1_transform.m22())
            v1_effective_size = (
                v1_scene_size[0] * v1_scale[0],
                v1_scene_size[1] * v1_scale[1],
            )

            # Capture V2 dimensions
            v2_component_size = (
                self.v2_pictograph.size().width(),
                self.v2_pictograph.size().height(),
            )
            v2_scene_rect = self.v2_pictograph.scene.sceneRect()
            v2_scene_size = (v2_scene_rect.width(), v2_scene_rect.height())
            v2_transform = self.v2_pictograph.transform()
            v2_scale = (v2_transform.m11(), v2_transform.m22())
            v2_effective_size = (
                v2_scene_size[0] * v2_scale[0],
                v2_scene_size[1] * v2_scale[1],
            )

            # Capture TKA glyph dimensions (simplified)
            v1_tka_size = self._get_v1_tka_dimensions()
            v2_tka_size = self._get_v2_tka_dimensions()

            comparison = DimensionComparison(
                v1_component_size=v1_component_size,
                v2_component_size=v2_component_size,
                v1_scene_size=v1_scene_size,
                v2_scene_size=v2_scene_size,
                v1_scale=v1_scale,
                v2_scale=v2_scale,
                v1_effective_size=v1_effective_size,
                v2_effective_size=v2_effective_size,
                v1_tka_size=v1_tka_size,
                v2_tka_size=v2_tka_size,
            )

            return comparison

        except Exception as e:
            print(f"❌ Failed to capture dimensions: {e}")
            return None

    def _get_v1_tka_dimensions(self) -> Optional[Tuple[float, float]]:
        """Get V1 TKA glyph dimensions."""
        try:
            if (
                hasattr(self.v1_pictograph.elements, "tka_glyph")
                and self.v1_pictograph.elements.tka_glyph
            ):
                tka_rect = self.v1_pictograph.elements.tka_glyph.sceneBoundingRect()
                return (tka_rect.width(), tka_rect.height())
        except:
            pass
        return None

    def _get_v2_tka_dimensions(self) -> Optional[Tuple[float, float]]:
        """Get V2 TKA glyph dimensions."""
        try:
            if self.v2_pictograph.scene:
                for item in self.v2_pictograph.scene.items():
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
            f"   V1: {comparison.v1_component_size[0]}x{comparison.v1_component_size[1]}"
        )
        print(
            f"   V2: {comparison.v2_component_size[0]}x{comparison.v2_component_size[1]}"
        )

        print(f"\n📐 SCENE SIZES:")
        print(
            f"   V1: {comparison.v1_scene_size[0]:.1f}x{comparison.v1_scene_size[1]:.1f}"
        )
        print(
            f"   V2: {comparison.v2_scene_size[0]:.1f}x{comparison.v2_scene_size[1]:.1f}"
        )

        print(f"\n📐 VIEW SCALES:")
        print(f"   V1: {comparison.v1_scale[0]:.4f}x{comparison.v1_scale[1]:.4f}")
        print(f"   V2: {comparison.v2_scale[0]:.4f}x{comparison.v2_scale[1]:.4f}")

        print(f"\n📐 EFFECTIVE SIZES:")
        print(
            f"   V1: {comparison.v1_effective_size[0]:.1f}x{comparison.v1_effective_size[1]:.1f}"
        )
        print(
            f"   V2: {comparison.v2_effective_size[0]:.1f}x{comparison.v2_effective_size[1]:.1f}"
        )

        size_diff = comparison.size_difference_percentage()
        print(f"\n📊 SIZE DIFFERENCE: {size_diff:+.1f}%")

        if comparison.v1_tka_size and comparison.v2_tka_size:
            print(f"\n🔤 TKA GLYPH SIZES:")
            print(
                f"   V1: {comparison.v1_tka_size[0]:.1f}x{comparison.v1_tka_size[1]:.1f}"
            )
            print(
                f"   V2: {comparison.v2_tka_size[0]:.1f}x{comparison.v2_tka_size[1]:.1f}"
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
