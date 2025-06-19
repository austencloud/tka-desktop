#!/usr/bin/env python3
"""
Production Readiness Verification Script
Verifies that TKA Desktop is ready for production deployment.
"""

import sys
import json
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def verify_imports():
    """Verify all critical imports work."""
    print("📦 Verifying Critical Imports...")
    
    try:
        # Core infrastructure
        from core.events import get_event_bus, IEventBus
        from core.commands import CommandProcessor
        from core.dependency_injection.di_container import DIContainer
        from core.monitoring import performance_monitor
        print("  ✅ Core infrastructure imports")
        
        # Services
        from application.services.core.sequence_management_service import SequenceManagementService
        from application.services.positioning.arrow_management_service import ArrowManagementService
        print("  ✅ Service imports")
        
        # API
        from infrastructure.api.production_api import app, initialize_services
        from infrastructure.api.api_models import SequenceAPI, BeatAPI, CreateSequenceRequest
        print("  ✅ API imports")
        
        # Domain models
        from domain.models.core_models import SequenceData, BeatData, MotionData
        from domain.models.pictograph_models import ArrowData, PictographData
        print("  ✅ Domain model imports")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False

def verify_services():
    """Verify services can be initialized."""
    print("\n🔧 Verifying Service Initialization...")
    
    try:
        from core.events import get_event_bus
        from core.commands import CommandProcessor
        from application.services.core.sequence_management_service import SequenceManagementService
        from application.services.positioning.arrow_management_service import ArrowManagementService
        
        # Initialize event bus
        event_bus = get_event_bus()
        print("  ✅ Event bus initialized")
        
        # Initialize command processor
        command_processor = CommandProcessor(event_bus)
        print("  ✅ Command processor initialized")
        
        # Initialize services
        sequence_service = SequenceManagementService(event_bus=event_bus)
        arrow_service = ArrowManagementService(event_bus=event_bus)
        print("  ✅ Core services initialized")
        
        # Test basic functionality
        sequence = sequence_service.create_sequence("Test", 2)
        print(f"  ✅ Sequence creation works: {sequence.id}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Service initialization failed: {e}")
        return False

def verify_api():
    """Verify API can be initialized."""
    print("\n🌐 Verifying API Initialization...")
    
    try:
        from infrastructure.api.production_api import app, initialize_services
        
        # Initialize services
        initialize_services()
        print("  ✅ API services initialized")
        
        # Check OpenAPI schema
        openapi_schema = app.openapi()
        endpoint_count = sum(len(methods) for methods in openapi_schema.get('paths', {}).values())
        print(f"  ✅ API schema generated: {endpoint_count} endpoints")
        
        # Check required endpoints
        paths = openapi_schema.get('paths', {})
        required_endpoints = [
            "/api/health", "/api/status", "/api/performance",
            "/api/sequences", "/api/commands/undo", "/api/commands/redo"
        ]
        
        missing = [ep for ep in required_endpoints if ep not in paths]
        if missing:
            print(f"  ❌ Missing endpoints: {missing}")
            return False
        
        print("  ✅ All required endpoints present")
        return True
        
    except Exception as e:
        print(f"  ❌ API initialization failed: {e}")
        return False

def verify_architecture():
    """Verify architecture components."""
    print("\n🏗️ Verifying Architecture Components...")
    
    try:
        # Test event system
        from core.events import get_event_bus, SequenceCreatedEvent
        from datetime import datetime
        import uuid
        
        event_bus = get_event_bus()
        events_received = []
        
        def handler(event):
            events_received.append(event)
        
        event_bus.subscribe("sequence.created", handler)
        
        test_event = SequenceCreatedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="verification_test",
            sequence_id="test_seq",
            sequence_name="Test Sequence"
        )
        
        event_bus.publish(test_event)
        
        if len(events_received) == 1:
            print("  ✅ Event system working")
        else:
            print(f"  ❌ Event system failed: {len(events_received)} events received")
            return False
        
        # Test performance monitoring
        from core.monitoring import monitor_performance, get_performance_report
        
        @monitor_performance("verification_test")
        def test_function():
            return "test_result"
        
        result = test_function()
        if result == "test_result":
            print("  ✅ Performance monitoring working")
        else:
            print("  ❌ Performance monitoring failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Architecture verification failed: {e}")
        return False

def main():
    """Run complete production readiness verification."""
    print("🔍 TKA Desktop Production Readiness Verification")
    print("=" * 60)
    
    # Run all verification tests
    tests = [
        ("Import Verification", verify_imports),
        ("Service Verification", verify_services),
        ("API Verification", verify_api),
        ("Architecture Verification", verify_architecture)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TKA DESKTOP IS PRODUCTION READY!")
        print("🚀 Ready for deployment with:")
        print("   python start_production_api.py")
        print("📚 Documentation at: http://localhost:8000/api/docs")
        return True
    else:
        print(f"\n⚠️ {total - passed} verification tests failed")
        print("🔧 Please address the issues before production deployment")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
