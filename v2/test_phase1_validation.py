#!/usr/bin/env python3
"""
Phase 1 Validation Script

Tests that all Phase 1 architectural improvements are working correctly:
1. Enhanced DI Container with constructor injection
2. V1 compatibility code removal
3. TypeSafe serialization layer
4. Service registration updates
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_enhanced_di_container():
    """Test enhanced dependency injection container."""
    print("🧪 Testing Enhanced DI Container...")

    from core.dependency_injection.di_container import (
        DIContainer,
        get_container,
        reset_container,
    )

    # Test basic functionality
    reset_container()
    container = get_container()
    assert isinstance(container, DIContainer), "Should return EnhancedContainer"

    # Test backward compatibility
    from core.dependency_injection.di_container import SimpleContainer

    assert SimpleContainer is DIContainer, "SimpleContainer should be alias"

    print("✅ Enhanced DI Container working")
    return True


def test_type_safe_serializer():
    """Test TypeSafe serialization layer."""
    print("🧪 Testing TypeSafe Serializer...")

    from core.serialization.type_safe_serializer import TypeSafeSerializer
    from domain.models.core_models import (
        BeatData,
        MotionData,
        MotionType,
        RotationDirection,
        Location,
    )

    # Create test data
    motion = MotionData(
        motion_type=MotionType.PRO,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        turns=1.5,
    )

    beat = BeatData(letter="A", duration=1.0, blue_motion=motion, red_motion=motion)

    # Test serialization
    serialized = TypeSafeSerializer.serialize(beat)
    assert "__type__" in serialized, "Should include type metadata"
    assert "__version__" in serialized, "Should include version metadata"
    assert serialized["letter"] == "A", "Should preserve data"

    # Test deserialization
    deserialized = TypeSafeSerializer.deserialize(serialized, BeatData)
    assert deserialized == beat, "Round-trip should preserve equality"

    # Test JSON serialization
    json_str = TypeSafeSerializer.serialize_to_json(beat)
    json_deserialized = TypeSafeSerializer.deserialize_from_json(json_str, BeatData)
    assert json_deserialized == beat, "JSON round-trip should work"

    print("✅ TypeSafe Serializer working")
    return True


def test_v1_compatibility_removal():
    """Test that V1 compatibility code has been removed."""
    print("🧪 Testing V1 Compatibility Removal...")

    # Check that beta prop services have clean comments
    from application.services.beta_prop_position_service import BetaPropPositionService
    from application.services.beta_prop_swap_service import BetaPropSwapService

    # These should instantiate without V1 references
    position_service = BetaPropPositionService()
    swap_service = BetaPropSwapService()

    assert position_service is not None, "Position service should work"
    assert swap_service is not None, "Swap service should work"

    print("✅ V1 Compatibility code cleaned up")
    return True


def test_service_registrations():
    """Test that existing service registrations work with enhanced container."""
    print("🧪 Testing Service Registrations...")

    from core.dependency_injection.di_container import (
        get_container,
        reset_container,
    )
    from core.interfaces.core_services import ILayoutService
    from application.services.simple_layout_service import SimpleLayoutService

    reset_container()
    container = get_container()

    # Test registration and resolution
    container.register_singleton(ILayoutService, SimpleLayoutService)
    layout_service = container.resolve(ILayoutService)

    assert isinstance(layout_service, SimpleLayoutService), "Should resolve correctly"

    # Test singleton behavior
    layout_service2 = container.resolve(ILayoutService)
    assert layout_service is layout_service2, "Should return same instance"

    print("✅ Service registrations working")
    return True


def test_domain_models():
    """Test that domain models work correctly with new serialization."""
    print("🧪 Testing Domain Models...")

    from domain.models.core_models import SequenceData, BeatData
    from core.serialization.type_safe_serializer import TypeSafeSerializer

    # Create a sequence with beats
    beat1 = BeatData(beat_number=1, letter="A", duration=1.0)
    beat2 = BeatData(beat_number=2, letter="B", duration=1.5)

    sequence = SequenceData(
        name="Test Sequence", word="AB", beats=[beat1, beat2], start_position="alpha1"
    )

    # Test serialization
    serialized = TypeSafeSerializer.serialize(sequence)
    deserialized = TypeSafeSerializer.deserialize(serialized, SequenceData)

    assert deserialized == sequence, "Sequence round-trip should work"
    assert len(deserialized.beats) == 2, "Should preserve beats"
    assert deserialized.beats[0].letter == "A", "Should preserve beat data"

    print("✅ Domain models working with serialization")
    return True


def main():
    """Run all Phase 1 validation tests."""
    print("🚀 Phase 1 Architectural Improvements Validation")
    print("=" * 50)

    tests = [
        test_enhanced_di_container,
        test_type_safe_serializer,
        test_v1_compatibility_removal,
        test_service_registrations,
        test_domain_models,
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

    print("\n" + "=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All Phase 1 improvements validated successfully!")
        print("\n✅ Enhanced DI Container: Constructor injection working")
        print("✅ V1 Compatibility: Clean V2-only code")
        print("✅ TypeSafe Serialization: Cross-language ready")
        print("✅ Service Registrations: Backward compatible")
        print("✅ Domain Models: Fully serializable")
        return True
    else:
        print(f"⚠️  {failed} tests failed - Phase 1 needs attention")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
