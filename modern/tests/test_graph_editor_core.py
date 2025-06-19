#!/usr/bin/env python3
"""
Quick test script to validate Modern Graph Editor functionality
"""

import sys
import os
from pathlib import Path

# Add the modern source to path
modern_src = Path(__file__).parent / "modern" / "src"
sys.path.insert(0, str(modern_src))


def test_imports():
    """Test that core imports work"""
    try:
        print("Testing core imports...")

        # Test basic domain models
        from domain.models.core_models import BeatData, SequenceData

        print("✅ Domain models import successful")

        # Test service interfaces
        from core.interfaces.workbench_services import IGraphEditorService

        print("✅ Service interfaces import successful")

        # Test service implementation
        from application.services.graph_editor_service import GraphEditorService

        print("✅ Service implementation import successful")

        # Test dependency injection
        from core.dependency_injection.di_container import DIContainer

        print("✅ DI container import successful")

        print("\n🎉 All core imports successful!")
        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_service_creation():
    """Test service creation and basic functionality"""
    try:
        print("\nTesting service creation...")

        from application.services.graph_editor_service import GraphEditorService

        # Create service
        service = GraphEditorService()
        print("✅ GraphEditorService created")

        # Test basic methods
        print(f"✅ Initial visibility: {service.is_visible()}")

        # Test toggle
        new_state = service.toggle_graph_visibility()
        print(f"✅ After toggle: {new_state}")

        print("\n🎉 Service functionality test passed!")
        return True

    except Exception as e:
        print(f"❌ Service test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_di_container():
    """Test dependency injection container"""
    try:
        print("\nTesting DI container...")

        from core.dependency_injection.di_container import DIContainer
        from core.interfaces.workbench_services import IGraphEditorService
        from application.services.graph_editor_service import GraphEditorService

        # Create container
        container = DIContainer()
        print("✅ DI container created")

        # Register service
        container.register_singleton(IGraphEditorService, GraphEditorService)
        print("✅ Service registered")

        # Resolve service
        service = container.resolve(IGraphEditorService)
        print("✅ Service resolved")

        print(f"✅ Service type: {type(service)}")

        print("\n🎉 DI container test passed!")
        return True

    except Exception as e:
        print(f"❌ DI container test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Modern Graph Editor Validation Test")
    print("=" * 50)

    tests = [
        test_imports,
        test_service_creation,
        test_di_container,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 All tests passed! Modern Graph Editor core is functional.")
        return True
    else:
        print("❌ Some tests failed. Check implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
