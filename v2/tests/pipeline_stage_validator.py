"""
Pipeline Stage Validator for Legacy and V2 Pictograph Rendering.

This validator tests dimensions at each major stage of the pictograph rendering pipeline
to identify exactly where discrepancies are introduced.
"""

import sys
import os
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add paths for both Legacy and V2
current_dir = os.path.dirname(os.path.abspath(__file__))
legacy_src_path = os.path.join(current_dir, "..", "..", "legacy", "src")
v2_src_path = os.path.join(current_dir, "..", "src")

sys.path.insert(0, legacy_src_path)
sys.path.insert(0, v2_src_path)

print(f"Legacy path: {legacy_src_path}")
print(f"V2 path: {v2_src_path}")
print(f"Legacy exists: {os.path.exists(legacy_src_path)}")
print(f"V2 exists: {os.path.exists(v2_src_path)}")


@dataclass
class PipelineStageResult:
    """Results from a single pipeline stage validation."""

    stage_name: str
    legacy_dimensions: Dict[str, Any]
    v2_dimensions: Dict[str, Any]
    discrepancies: List[str]

    def has_discrepancies(self) -> bool:
        return len(self.discrepancies) > 0


class PipelineStageValidator:
    """Validates dimensions at each stage of the pictograph rendering pipeline."""

    def __init__(self):
        self.app = None
        self.legacy_pictograph = None
        self.v2_pictograph = None
        self.legacy_view = None
        self.results: List[PipelineStageResult] = []

    def setup_validation_environment(self) -> bool:
        """Setup the validation environment."""
        try:
            if not QApplication.instance():
                self.app = QApplication(sys.argv)

            # Import and create Legacy components
            from base_widgets.pictograph.pictograph import (
                Pictograph as LegacyPictograph,
            )
            from base_widgets.pictograph.elements.views.base_pictograph_view import (
                BasePictographView,
            )

            # Import V2 components
            from presentation.components.pictograph.pictograph_component import (
                PictographComponent,
            )

            self.legacy_pictograph = LegacyPictograph()
            self.legacy_view = BasePictographView(self.legacy_pictograph)
            self.legacy_view.setFixedSize(400, 400)

            self.v2_pictograph = PictographComponent()
            self.v2_pictograph.setFixedSize(400, 400)

            print("✅ Validation environment setup successful")
            return True

        except Exception as e:
            print(f"❌ Failed to setup validation environment: {e}")
            return False

    def validate_stage_1_initialization(self) -> PipelineStageResult:
        """Validate Stage 1: Initial component and scene setup."""
        stage_name = "Stage 1: Initialization"
        print(f"\n🔍 Validating {stage_name}")

        legacy_dims = {}
        v2_dims = {}
        discrepancies = []

        try:
            # Legacy dimensions after initialization
            legacy_dims["scene_rect"] = {
                "width": self.legacy_pictograph.sceneRect().width(),
                "height": self.legacy_pictograph.sceneRect().height(),
            }
            legacy_dims["component_size"] = {
                "width": self.legacy_view.size().width(),
                "height": self.legacy_view.size().height(),
            }

            # V2 dimensions after initialization
            v2_dims["scene_rect"] = {
                "width": self.v2_pictograph.scene.sceneRect().width(),
                "height": self.v2_pictograph.scene.sceneRect().height(),
            }
            v2_dims["component_size"] = {
                "width": self.v2_pictograph.size().width(),
                "height": self.v2_pictograph.size().height(),
            }

            # Check for discrepancies
            if legacy_dims["scene_rect"] != v2_dims["scene_rect"]:
                discrepancies.append(
                    f"Scene rect mismatch: Legacy={legacy_dims['scene_rect']}, V2={v2_dims['scene_rect']}"
                )

            if legacy_dims["component_size"] != v2_dims["component_size"]:
                discrepancies.append(
                    f"Component size mismatch: Legacy={legacy_dims['component_size']}, V2={v2_dims['component_size']}"
                )

        except Exception as e:
            discrepancies.append(f"Error during validation: {e}")

        result = PipelineStageResult(stage_name, legacy_dims, v2_dims, discrepancies)
        self.results.append(result)
        return result

    def validate_stage_2_content_update(self) -> PipelineStageResult:
        """Validate Stage 2: Content update with test data."""
        stage_name = "Stage 2: Content Update"
        print(f"\n🔍 Validating {stage_name}")

        legacy_dims = {}
        v2_dims = {}
        discrepancies = []

        try:
            # Create and apply test data
            beat_data = self._create_test_beat_data()
            if not beat_data:
                discrepancies.append("Failed to create test beat data")
                return PipelineStageResult(
                    stage_name, legacy_dims, v2_dims, discrepancies
                )

            # Update V2
            self.v2_pictograph.update_from_beat(beat_data)

            # Update Legacy
            legacy_data = self._convert_beat_data_to_legacy_format(beat_data)
            self.legacy_pictograph.managers.updater.update_pictograph(legacy_data)

            # Process events
            if self.app:
                self.app.processEvents()

            # Capture dimensions after content update
            legacy_dims["items_count"] = len(self.legacy_pictograph.items())
            legacy_dims["scene_rect"] = {
                "width": self.legacy_pictograph.sceneRect().width(),
                "height": self.legacy_pictograph.sceneRect().height(),
            }

            v2_dims["items_count"] = len(self.v2_pictograph.scene.items())
            v2_dims["scene_rect"] = {
                "width": self.v2_pictograph.scene.sceneRect().width(),
                "height": self.v2_pictograph.scene.sceneRect().height(),
            }

            # Check for discrepancies
            if (
                abs(legacy_dims["items_count"] - v2_dims["items_count"]) > 2
            ):  # Allow small difference
                discrepancies.append(
                    f"Item count significant difference: Legacy={legacy_dims['items_count']}, V2={v2_dims['items_count']}"
                )

        except Exception as e:
            discrepancies.append(f"Error during content update validation: {e}")

        result = PipelineStageResult(stage_name, legacy_dims, v2_dims, discrepancies)
        self.results.append(result)
        return result

    def validate_stage_3_view_scaling(self) -> PipelineStageResult:
        """Validate Stage 3: View scaling and transformation."""
        stage_name = "Stage 3: View Scaling"
        print(f"\n🔍 Validating {stage_name}")

        legacy_dims = {}
        v2_dims = {}
        discrepancies = []

        try:
            # Force view updates
            self.legacy_view.update()
            self.v2_pictograph.update()

            if self.app:
                self.app.processEvents()

            # Legacy scaling information
            legacy_transform = self.legacy_view.transform()
            legacy_dims["transform_scale"] = {
                "x": legacy_transform.m11(),
                "y": legacy_transform.m22(),
            }
            legacy_dims["view_rect"] = {
                "width": self.legacy_view.viewport().size().width(),
                "height": self.legacy_view.viewport().size().height(),
            }

            # V2 scaling information
            v2_transform = self.v2_pictograph.transform()
            v2_dims["transform_scale"] = {
                "x": v2_transform.m11(),
                "y": v2_transform.m22(),
            }
            v2_dims["view_rect"] = {
                "width": self.v2_pictograph.viewport().size().width(),
                "height": self.v2_pictograph.viewport().size().height(),
            }

            # Calculate effective sizes
            legacy_scene_rect = self.legacy_view.sceneRect()
            legacy_effective_width = (
                legacy_scene_rect.width() * legacy_dims["transform_scale"]["x"]
            )
            legacy_effective_height = (
                legacy_scene_rect.height() * legacy_dims["transform_scale"]["y"]
            )
            legacy_dims["effective_size"] = {
                "width": legacy_effective_width,
                "height": legacy_effective_height,
            }

            v2_scene_rect = self.v2_pictograph.scene.sceneRect()
            v2_effective_width = v2_scene_rect.width() * v2_dims["transform_scale"]["x"]
            v2_effective_height = (
                v2_scene_rect.height() * v2_dims["transform_scale"]["y"]
            )
            v2_dims["effective_size"] = {
                "width": v2_effective_width,
                "height": v2_effective_height,
            }

            # Check for scaling discrepancies
            scale_diff_x = abs(
                legacy_dims["transform_scale"]["x"] - v2_dims["transform_scale"]["x"]
            )
            scale_diff_y = abs(
                legacy_dims["transform_scale"]["y"] - v2_dims["transform_scale"]["y"]
            )

            if scale_diff_x > 0.01 or scale_diff_y > 0.01:  # 1% tolerance
                discrepancies.append(
                    f"Transform scale difference: Legacy={legacy_dims['transform_scale']}, V2={v2_dims['transform_scale']}"
                )

            # Check effective size difference
            size_diff_w = abs(legacy_effective_width - v2_effective_width)
            size_diff_h = abs(legacy_effective_height - v2_effective_height)

            if size_diff_w > 10 or size_diff_h > 10:  # 10px tolerance
                discrepancies.append(
                    f"Effective size difference: Legacy={legacy_dims['effective_size']}, V2={v2_dims['effective_size']}"
                )

        except Exception as e:
            discrepancies.append(f"Error during scaling validation: {e}")

        result = PipelineStageResult(stage_name, legacy_dims, v2_dims, discrepancies)
        self.results.append(result)
        return result

    def validate_stage_4_tka_glyph_rendering(self) -> PipelineStageResult:
        """Validate Stage 4: TKA glyph specific rendering and positioning."""
        stage_name = "Stage 4: TKA Glyph Rendering"
        print(f"\n🔍 Validating {stage_name}")

        legacy_dims = {}
        v2_dims = {}
        discrepancies = []

        try:
            # Legacy TKA glyph analysis
            if (
                hasattr(self.legacy_pictograph.elements, "tka_glyph")
                and self.legacy_pictograph.elements.tka_glyph
            ):
                tka_glyph = self.legacy_pictograph.elements.tka_glyph
                tka_rect = tka_glyph.boundingRect()
                tka_pos = tka_glyph.pos()
                scene_rect = tka_glyph.sceneBoundingRect()

                legacy_dims["tka_bounding_rect"] = {
                    "width": tka_rect.width(),
                    "height": tka_rect.height(),
                }
                legacy_dims["tka_position"] = {"x": tka_pos.x(), "y": tka_pos.y()}
                legacy_dims["tka_scene_rect"] = {
                    "width": scene_rect.width(),
                    "height": scene_rect.height(),
                    "x": scene_rect.x(),
                    "y": scene_rect.y(),
                }

                # Letter item analysis
                if hasattr(tka_glyph, "letter_item") and tka_glyph.letter_item:
                    letter_rect = tka_glyph.letter_item.boundingRect()
                    legacy_dims["letter_rect"] = {
                        "width": letter_rect.width(),
                        "height": letter_rect.height(),
                    }
            else:
                legacy_dims["tka_found"] = False
                discrepancies.append("Legacy TKA glyph not found")

            # V2 TKA glyph analysis
            v2_tka_found = False
            if self.v2_pictograph.scene:
                for item in self.v2_pictograph.scene.items():
                    if hasattr(item, "childItems") and item.childItems():
                        # Simple heuristic to identify TKA group
                        children = item.childItems()
                        if len(children) > 0:
                            first_child = children[0]
                            if hasattr(first_child, "boundingRect"):
                                v2_tka_found = True
                                item_rect = item.boundingRect()
                                item_pos = item.pos()
                                scene_rect = item.sceneBoundingRect()

                                v2_dims["tka_bounding_rect"] = {
                                    "width": item_rect.width(),
                                    "height": item_rect.height(),
                                }
                                v2_dims["tka_position"] = {
                                    "x": item_pos.x(),
                                    "y": item_pos.y(),
                                }
                                v2_dims["tka_scene_rect"] = {
                                    "width": scene_rect.width(),
                                    "height": scene_rect.height(),
                                    "x": scene_rect.x(),
                                    "y": scene_rect.y(),
                                }

                                # First child (letter) analysis
                                letter_rect = first_child.boundingRect()
                                v2_dims["letter_rect"] = {
                                    "width": letter_rect.width(),
                                    "height": letter_rect.height(),
                                }
                                break

            if not v2_tka_found:
                v2_dims["tka_found"] = False
                discrepancies.append("V2 TKA glyph not found")

            # Compare TKA dimensions if both found
            if legacy_dims.get("tka_bounding_rect") and v2_dims.get(
                "tka_bounding_rect"
            ):
                legacy_tka = legacy_dims["tka_bounding_rect"]
                v2_tka = v2_dims["tka_bounding_rect"]

                width_diff = abs(legacy_tka["width"] - v2_tka["width"])
                height_diff = abs(legacy_tka["height"] - v2_tka["height"])

                if width_diff > 5 or height_diff > 5:  # 5px tolerance
                    discrepancies.append(
                        f"TKA size difference: Legacy={legacy_tka}, V2={v2_tka}"
                    )

                # Compare positions
                legacy_pos = legacy_dims["tka_position"]
                v2_pos = v2_dims["tka_position"]
                pos_diff_x = abs(legacy_pos["x"] - v2_pos["x"])
                pos_diff_y = abs(legacy_pos["y"] - v2_pos["y"])

                if pos_diff_x > 10 or pos_diff_y > 10:  # 10px tolerance
                    discrepancies.append(
                        f"TKA position difference: Legacy={legacy_pos}, V2={v2_pos}"
                    )

        except Exception as e:
            discrepancies.append(f"Error during TKA validation: {e}")

        result = PipelineStageResult(stage_name, legacy_dims, v2_dims, discrepancies)
        self.results.append(result)
        return result

    def _create_test_beat_data(self):
        """Create test beat data."""
        try:
            from domain.models.core_models import (
                BeatData,
                MotionData,
                GlyphData,
                LetterType,
                Location,
                MotionType,
            )

            blue_motion = MotionData(
                motion_type=MotionType.PRO,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=1.0,
            )

            glyph_data = GlyphData(
                letter_type=LetterType.Type1,
                show_tka=True,
                show_vtg=False,
                show_elemental=False,
                show_positions=False,
            )

            return BeatData(letter="A", blue_motion=blue_motion, glyph_data=glyph_data)
        except:
            return None

    def _convert_beat_data_to_legacy_format(self, beat_data) -> Dict[str, Any]:
        """Convert V2 BeatData to Legacy format."""
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

    def run_full_pipeline_validation(self) -> bool:
        """Run validation for all pipeline stages."""
        print("🚀 Starting Full Pipeline Validation")

        if not self.setup_validation_environment():
            return False

        # Run all validation stages
        self.validate_stage_1_initialization()
        self.validate_stage_2_content_update()
        self.validate_stage_3_view_scaling()
        self.validate_stage_4_tka_glyph_rendering()

        # Print summary report
        self.print_validation_summary()

        return True

    def print_validation_summary(self) -> None:
        """Print summary of all validation results."""
        print("\n" + "=" * 80)
        print("📋 PIPELINE VALIDATION SUMMARY")
        print("=" * 80)

        total_discrepancies = 0
        for result in self.results:
            status = "❌ FAIL" if result.has_discrepancies() else "✅ PASS"
            print(f"\n{status} {result.stage_name}")

            if result.has_discrepancies():
                total_discrepancies += len(result.discrepancies)
                for discrepancy in result.discrepancies:
                    print(f"   ⚠️  {discrepancy}")

        print(f"\n📊 TOTAL DISCREPANCIES: {total_discrepancies}")

        if total_discrepancies == 0:
            print("🎉 All pipeline stages validated successfully!")
        else:
            print("🔧 Pipeline discrepancies found - investigation needed")

        print("=" * 80)
        print()


def run_pipeline_validation():
    """Run the pipeline stage validation."""
    validator = PipelineStageValidator()
    return validator.run_full_pipeline_validation()


if __name__ == "__main__":
    success = run_pipeline_validation()
    sys.exit(0 if success else 1)
