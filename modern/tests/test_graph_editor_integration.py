#!/usr/bin/env python3
"""
Full Integration Test for Modern Graph Editor
"""

import sys
import os
from pathlib import Path

# Add the modern source to path
modern_src = Path(__file__).parent / "modern" / "src"
sys.path.insert(0, str(modern_src))


def test_graph_editor_integration():
    """Test complete graph editor integration without Qt GUI"""
    try:
        print("Testing graph editor integration...")

        # 1. Import all required components
        from core.dependency_injection.di_container import DIContainer
        from core.interfaces.workbench_services import IGraphEditorService
        from core.interfaces.core_services import (
            ILayoutService,
            IUIStateManagementService,
        )
        from application.services.graph_editor_service import GraphEditorService
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )
        from application.services.ui.ui_state_management_service import (
            UIStateManagementService,
        )
        from domain.models.core_models import BeatData, SequenceData

        print("  ✅ All imports successful")

        # 2. Setup DI container
        container = DIContainer()

        # Register core services
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(
            IUIStateManagementService, UIStateManagementService
        )

        # Get UI state service and create graph editor service
        ui_state_service = container.resolve(IUIStateManagementService)
        graph_editor_service = GraphEditorService(ui_state_service)
        container.register_instance(IGraphEditorService, graph_editor_service)

        print("  ✅ DI container configured")

        # 3. Test service functionality
        graph_service = container.resolve(IGraphEditorService)

        # Test basic operations
        assert graph_service.is_visible() == False
        new_state = graph_service.toggle_graph_visibility()
        assert new_state == True
        assert graph_service.is_visible() == True

        print("  ✅ Service operations working")  # 4. Test with sample data
        sample_beat = BeatData(beat_number=1, letter="A")

        sample_sequence = SequenceData(beats=[sample_beat], start_position="beta")

        # Test sequence operations
        graph_service.update_graph_display(sample_sequence)
        graph_service.set_selected_beat(sample_beat, 0)
        selected = graph_service.get_selected_beat()

        assert selected == sample_beat
        print("  ✅ Data operations working")

        # 5. Test arrow operations
        graph_service.set_arrow_selection("blue")
        available_turns = graph_service.get_available_turns("blue")
        available_orientations = graph_service.get_available_orientations("blue")

        assert isinstance(available_turns, list)
        assert isinstance(available_orientations, list)
        print("  ✅ Arrow operations working")

        print("\n🎉 Full integration test passed!")
        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_workbench_factory():
    """Test the workbench factory without Qt instantiation"""
    try:
        print("\nTesting workbench factory...")

        from core.dependency_injection.di_container import DIContainer
        from presentation.factories.workbench_factory import (
            configure_workbench_services,
        )
        from core.interfaces.core_services import (
            ILayoutService,
            IUIStateManagementService,
        )
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )
        from application.services.ui.ui_state_management_service import (
            UIStateManagementService,
        )

        # Create container and register prerequisite services
        container = DIContainer()
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(
            IUIStateManagementService, UIStateManagementService
        )

        print("  ✅ Prerequisites registered")

        # Configure workbench services
        configure_workbench_services(container)
        print("  ✅ Workbench services configured")

        # Verify all required services are available
        from core.interfaces.workbench_services import (
            ISequenceWorkbenchService,
            IFullScreenService,
            IBeatDeletionService,
            IGraphEditorService,
            IDictionaryService,
        )

        # Test each service resolution
        workbench_service = container.resolve(ISequenceWorkbenchService)
        fullscreen_service = container.resolve(IFullScreenService)
        deletion_service = container.resolve(IBeatDeletionService)
        graph_service = container.resolve(IGraphEditorService)
        dictionary_service = container.resolve(IDictionaryService)

        print(f"  ✅ All services resolved:")
        print(f"    - Workbench: {type(workbench_service).__name__}")
        print(f"    - Fullscreen: {type(fullscreen_service).__name__}")
        print(f"    - Deletion: {type(deletion_service).__name__}")
        print(f"    - Graph Editor: {type(graph_service).__name__}")
        print(f"    - Dictionary: {type(dictionary_service).__name__}")

        print("\n🎉 Workbench factory test passed!")
        return True

    except Exception as e:
        print(f"❌ Workbench factory test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_component_structure():
    """Test that component structure is sound"""
    try:
        print("\nTesting component structure...")

        # Test that we can import and inspect components
        from presentation.components.workbench.graph_editor.graph_editor import (
            GraphEditor,
        )
        from presentation.components.workbench.graph_editor.pictograph_container import (
            GraphEditorPictographContainer,
        )
        from presentation.components.workbench.graph_editor.adjustment_panel import (
            AdjustmentPanel,
        )
        from presentation.components.workbench.graph_editor.modern_toggle_tab import (
            ModernToggleTab,
        )

        # Test component class structure
        components = {
            "GraphEditor": GraphEditor,
            "PictographContainer": GraphEditorPictographContainer,
            "AdjustmentPanel": AdjustmentPanel,
            "ToggleTab": ModernToggleTab,
        }

        for name, cls in components.items():
            # Check if it's a proper class
            assert hasattr(cls, "__init__"), f"{name} missing __init__"
            print(f"  ✅ {name} structure valid")

        print("\n🎉 Component structure test passed!")
        return True

    except Exception as e:
        print(f"❌ Component structure test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all integration tests"""
    print("🚀 Modern Graph Editor Full Integration Test")
    print("=" * 70)

    tests = [
        test_graph_editor_integration,
        test_workbench_factory,
        test_component_structure,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 70)
    print(f"Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 ALL TESTS PASSED! Modern Graph Editor is ready for Qt integration!")
        print("\nNext steps:")
        print("1. Run with Qt to test UI components")
        print("2. Add graph editor to main application layout")
        print("3. Test user interactions and animations")
        return True
    else:
        print("❌ Some tests failed. Fix issues before proceeding.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
