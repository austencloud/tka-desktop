#!/usr/bin/env python3
"""
Test to verify that the import path configuration is working correctly for modern tests.
This test validates that domain models can be imported successfully from test files.
"""

import sys
from pathlib import Path

# Add modern src to path
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_domain_models_import():
    """Test that domain models can be imported successfully."""
    try:
        from domain.models.core_models import (
            BeatData,
            MotionData,
            MotionType,
            RotationDirection,
            Location,
        )

        print("✅ Domain models imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import domain models: {e}")
        return False


def test_presentation_components_import():
    """Test that presentation components can be imported successfully."""
    try:
        from presentation.components.pictograph.pictograph_component import (
            PictographComponent,
        )

        print("✅ Presentation components imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import presentation components: {e}")
        return False


def test_core_services_import():
    """Test that core services can be imported successfully."""
    try:
        from core.dependency_injection.di_container import DIContainer

        print("✅ Core services imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import core services: {e}")
        return False


def main():
    """Main test function."""
    print("🧪 Testing modern Import Path Configuration")
    print("=" * 50)

    tests = [
        test_domain_models_import,
        test_presentation_components_import,
        test_core_services_import,
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    print("\n📊 Test Results:")
    print(f"   Passed: {sum(results)}/{len(results)}")

    if all(results):
        print(
            "🎉 All import tests passed! modern import path configuration is working correctly."
        )
        return 0
    else:
        print("❌ Some import tests failed. Import path configuration needs fixing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
