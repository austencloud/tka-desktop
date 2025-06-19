#!/usr/bin/env python3
"""
Service Integration Test - Verify all services work together correctly
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_event_driven_integration():
    """Test event-driven service integration"""
    print("🧪 Testing event-driven service integration...")
    
    try:
        from core.events import get_event_bus, reset_event_bus
        from application.services.core.sequence_management_service import SequenceManagementService
        from domain.models.core_models import BeatData
        
        # Reset event bus for clean test
        reset_event_bus()
        event_bus = get_event_bus()
        
        # Track events
        events_received = []
        def track_events(event):
            events_received.append(event.event_type)
        
        # Subscribe to events
        event_bus.subscribe("sequence.created", track_events)
        event_bus.subscribe("sequence.beat_added", track_events)
        
        # Create service
        service = SequenceManagementService(event_bus=event_bus)
        
        # Test sequence creation
        sequence = service.create_sequence("Test Sequence", 2)
        assert sequence.name == "Test Sequence"
        assert len(sequence.beats) == 2
        
        # Test beat addition
        new_beat = BeatData(beat_number=3, letter="A", duration=1.0)
        updated_sequence = service.add_beat(sequence, new_beat, 2)
        assert len(updated_sequence.beats) == 3
        
        # Verify events were published
        assert len(events_received) == 2
        assert "sequence.created" in events_received
        assert "sequence.beat_added" in events_received
        
        print("✅ Event-driven integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Event-driven integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_arrow_service_integration():
    """Test arrow management service integration"""
    print("🧪 Testing arrow management service integration...")
    
    try:
        from application.services.positioning.arrow_management_service import ArrowManagementService
        from domain.models.core_models import MotionData, MotionType, Location, RotationDirection
        from domain.models.pictograph_models import ArrowData, PictographData, GridData, GridMode
        
        # Create service
        service = ArrowManagementService()
        
        # Create test data
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0
        )
        
        arrow = ArrowData(color="blue", motion_data=motion, is_visible=True)
        
        grid_data = GridData(
            grid_mode=GridMode.DIAMOND,
            center_x=475.0,
            center_y=475.0,
            radius=100.0
        )
        
        pictograph = PictographData(
            grid_data=grid_data,
            arrows={"blue": arrow},
            is_blank=False
        )
        
        # Test arrow positioning
        x, y, rotation = service.calculate_arrow_position(arrow, pictograph)
        
        # Verify results are reasonable
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(rotation, (int, float))
        assert 0 <= x <= 950  # Within scene bounds
        assert 0 <= y <= 950  # Within scene bounds
        
        print("✅ Arrow service integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Arrow service integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_di_container_integration():
    """Test dependency injection container integration"""
    print("🧪 Testing DI container integration...")
    
    try:
        from core.dependency_injection.di_container import DIContainer, reset_container
        from application.services.core.sequence_management_service import SequenceManagementService
        
        # Reset container
        reset_container()
        container = DIContainer()
        
        # Test service creation through DI
        service = container._create_instance(SequenceManagementService)
        assert isinstance(service, SequenceManagementService)
        
        # Test that service works
        sequence = service.create_sequence("DI Test", 1)
        assert sequence.name == "DI Test"
        
        print("✅ DI container integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ DI container integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all integration tests"""
    print("🚀 Service Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_event_driven_integration,
        test_arrow_service_integration,
        test_di_container_integration,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("📊 Test Results")
    print("=" * 50)
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        print("✅ Service integration is stable and working correctly")
        return True
    else:
        print(f"❌ {total - passed} tests failed")
        print("⚠️ Service integration needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
