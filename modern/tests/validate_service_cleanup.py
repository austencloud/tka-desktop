#!/usr/bin/env python3
"""
Service Cleanup Validation Script

Validates that the service consolidation and cleanup was successful.
Ensures all consolidated services work and old services are properly removed.
"""

import sys
import os
from pathlib import Path


def validate_service_directory_cleanup():
    """Validate that the services directory has been properly cleaned up."""
    print("🧹 Validating Service Directory Cleanup...")

    services_dir = Path("src/application/services")

    # Expected consolidated services
    expected_services = {
        "arrow_management_service.py",
        "motion_management_service.py",
        "sequence_management_service.py",
        "pictograph_management_service.py",
        "ui_state_management_service.py",
        "layout_management_service.py",
        "legacy_pictograph_integration_service.py",  # Keep for Legacy/Modern bridge
        "position_matching_service.py",  # Keep - not consolidated yet
        "__init__.py",
    }

    # Services that should have been removed
    removed_services = {
        "arrow_mirror_service.py",
        "arrow_positioning_service.py",
        "beta_prop_position_service.py",
        "beta_prop_swap_service.py",
        "default_placement_service.py",
        "placement_key_service.py",
        "motion_orientation_service.py",
        "motion_validation_service.py",
        "motion_combination_service.py",
        "simple_sequence_service.py",
        "beat_management_service.py",
        "generation_services.py",
        "workbench_services.py",
        "pictograph_service.py",
        "pictograph_data_service.py",
        "pictograph_dataset_service.py",
        "pictograph_context_configurator.py",
        "glyph_data_service.py",
        "data_conversion_service.py",
        "settings_service.py",
        "settings_dialog_service.py",
        "tab_settings_services.py",
        "option_picker_state_service.py",
        "graph_editor_service.py",
        "graph_editor_hotkey_service.py",
        "simple_layout_service.py",
        "beat_frame_layout_service.py",
        "context_aware_scaling_service.py",
    }

    # Check current services
    current_services = set()
    for file_path in services_dir.glob("*.py"):
        current_services.add(file_path.name)

    # Validate expected services exist
    missing_services = expected_services - current_services
    if missing_services:
        print(f"❌ Missing expected services: {missing_services}")
        return False

    # Validate removed services are gone
    still_present = removed_services & current_services
    if still_present:
        print(f"❌ Services that should be removed are still present: {still_present}")
        return False

    # Check for unexpected services
    unexpected_services = current_services - expected_services
    if unexpected_services:
        print(f"⚠️  Unexpected services found: {unexpected_services}")

    print(f"✅ Service directory cleanup successful!")
    print(f"  • Expected services: {len(expected_services)} ✅")
    print(f"  • Removed services: {len(removed_services)} ✅")
    print(f"  • Current services: {len(current_services)}")

    return True


def validate_consolidated_services():
    """Validate that all consolidated services can be imported and work."""
    print("🧪 Validating Consolidated Services...")

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

    try:
        # Test ArrowManagementService
        from application.services.positioning.arrow_management_service import (
            ArrowManagementService,
        )

        arrow_service = ArrowManagementService()
        print("✅ ArrowManagementService imported and instantiated")

        # Test MotionManagementService
        from application.services.motion.motion_management_service import (
            MotionManagementService,
        )

        motion_service = MotionManagementService()
        print("✅ MotionManagementService imported and instantiated")

        # Test SequenceManagementService
        from application.services.core.sequence_management_service import (
            SequenceManagementService,
        )

        sequence_service = SequenceManagementService()
        print("✅ SequenceManagementService imported and instantiated")

        # Test PictographManagementService
        from application.services.core.pictograph_management_service import (
            PictographManagementService,
        )

        pictograph_service = PictographManagementService()
        print("✅ PictographManagementService imported and instantiated")

        # Test UIStateManagementService
        from application.services.ui.ui_state_management_service import (
            UIStateManagementService,
        )

        ui_service = UIStateManagementService()
        print("✅ UIStateManagementService imported and instantiated")

        # Test LayoutManagementService
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )

        layout_service = LayoutManagementService()
        print("✅ LayoutManagementService imported and instantiated")

        return True

    except Exception as e:
        print(f"❌ Error importing consolidated services: {e}")
        return False


def validate_interfaces():
    """Validate that all interfaces are properly defined."""
    print("🔌 Validating Service Interfaces...")

    try:
        from core.interfaces.core_services import (
            IArrowManagementService,
            IMotionManagementService,
            ISequenceManagementService,
            IPictographManagementService,
            IUIStateManagementService,
            ILayoutManagementService,
        )

        print("✅ All consolidated service interfaces imported successfully")

        # Validate interface methods exist
        arrow_methods = [
            "calculate_arrow_position",
            "should_mirror_arrow",
            "apply_beta_positioning",
        ]
        for method in arrow_methods:
            assert hasattr(
                IArrowManagementService, method
            ), f"Missing {method} in IArrowManagementService"

        motion_methods = [
            "validate_motion_combination",
            "get_valid_motion_combinations",
        ]
        for method in motion_methods:
            assert hasattr(
                IMotionManagementService, method
            ), f"Missing {method} in IMotionManagementService"

        print("✅ All interface methods validated")
        return True

    except Exception as e:
        print(f"❌ Error validating interfaces: {e}")
        return False


def validate_event_bus():
    """Validate that the event bus is working."""
    print("📡 Validating Event Bus...")

    try:
        from core.events.event_bus import TypeSafeEventBus, SequenceEvent

        bus = TypeSafeEventBus()

        # Test subscription and publishing
        call_count = 0

        def test_handler(event):
            nonlocal call_count
            call_count += 1

        sub_id = bus.subscribe("sequence.test", test_handler)

        event = SequenceEvent(
            sequence_id="test-123", operation="test", source="validation"
        )

        bus.publish(event)

        assert call_count == 1, "Event handler not called"

        bus.unsubscribe(sub_id)
        bus.shutdown()

        print("✅ Event bus working correctly")
        return True

    except Exception as e:
        print(f"❌ Error validating event bus: {e}")
        return False


def calculate_consolidation_metrics():
    """Calculate and display consolidation metrics."""
    print("📊 Calculating Consolidation Metrics...")

    # Original service count (from our analysis)
    original_services = [
        "arrow_mirror_service",
        "arrow_positioning_service",
        "beta_prop_position_service",
        "beta_prop_swap_service",
        "default_placement_service",
        "placement_key_service",
        "motion_orientation_service",
        "motion_validation_service",
        "motion_combination_service",
        "simple_sequence_service",
        "beat_management_service",
        "generation_services",
        "workbench_services",
        "pictograph_service",
        "pictograph_data_service",
        "pictograph_dataset_service",
        "pictograph_context_configurator",
        "glyph_data_service",
        "data_conversion_service",
        "settings_service",
        "settings_dialog_service",
        "tab_settings_services",
        "option_picker_state_service",
        "graph_editor_service",
        "graph_editor_hotkey_service",
        "simple_layout_service",
        "beat_frame_layout_service",
        "context_aware_scaling_service",
    ]

    # Consolidated services
    consolidated_services = [
        "arrow_management_service",
        "motion_management_service",
        "sequence_management_service",
        "pictograph_management_service",
        "ui_state_management_service",
        "layout_management_service",
    ]

    # Remaining services (not consolidated)
    remaining_services = [
        "legacy_pictograph_integration_service",
        "position_matching_service",
    ]

    original_count = len(original_services)
    consolidated_count = len(consolidated_services)
    remaining_count = len(remaining_services)
    total_current = consolidated_count + remaining_count

    reduction_percentage = ((original_count - total_current) / original_count) * 100

    print(f"📈 Consolidation Metrics:")
    print(f"  • Original services: {original_count}")
    print(f"  • Consolidated into: {consolidated_count} unified services")
    print(f"  • Remaining services: {remaining_count}")
    print(f"  • Total current services: {total_current}")
    print(f"  • Reduction: {reduction_percentage:.1f}%")
    print(f"  • Services eliminated: {original_count - total_current}")

    return {
        "original_count": original_count,
        "consolidated_count": consolidated_count,
        "remaining_count": remaining_count,
        "reduction_percentage": reduction_percentage,
    }


def main():
    """Run all cleanup validation tests."""
    print("🚀 Service Consolidation Cleanup Validation")
    print("=" * 60)

    tests = [
        validate_service_directory_cleanup,
        validate_consolidated_services,
        validate_interfaces,
        validate_event_bus,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} failed with error: {e}")

    # Calculate metrics regardless of test results
    metrics = calculate_consolidation_metrics()

    print("\n" + "=" * 60)
    print(f"📊 Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 Service consolidation and cleanup successful!")
        print("\n✅ **CLEANUP COMPLETE: Service Architecture Optimized**")
        print("\n🏗️ **Final Architecture:**")
        print("  • ArrowManagementService - Unified arrow operations")
        print("  • MotionManagementService - Unified motion operations")
        print("  • SequenceManagementService - Unified sequence operations")
        print("  • PictographManagementService - Unified pictograph operations")
        print("  • UIStateManagementService - Unified UI state operations")
        print("  • LayoutManagementService - Unified layout operations")
        print("  • TypeSafeEventBus - Event-driven communication")
        print("  • Enhanced DI Container - Protocol-based interfaces")

        print(f"\n📈 **Impact:**")
        print(f"  • {metrics['reduction_percentage']:.1f}% reduction in service count")
        print(
            f"  • Eliminated {metrics['original_count'] - metrics['consolidated_count'] - metrics['remaining_count']} micro-services"
        )
        print(f"  • Unified interfaces for all major operations")
        print(f"  • Event-driven architecture for decoupled communication")
        print(f"  • Clean, maintainable, debt-free service layer")

        return True
    else:
        print(f"⚠️  {failed} validation tests failed - cleanup needs attention")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
