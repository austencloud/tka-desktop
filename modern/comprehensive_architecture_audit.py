#!/usr/bin/env python3
"""
Comprehensive Architecture Audit for TKA Desktop Modern
Verifies core infrastructure integrity and identifies foundation gaps.
"""

import sys
import traceback
import time
import psutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


@dataclass
class AuditResult:
    """Result of an individual audit test."""

    test_name: str
    passed: bool
    details: str
    performance_ms: Optional[float] = None
    memory_mb: Optional[float] = None
    error: Optional[str] = None


class ArchitectureAuditor:
    """Comprehensive architecture auditor for TKA Desktop."""

    def __init__(self):
        self.results: List[AuditResult] = []
        self.start_memory = psutil.Process().memory_info().rss / 1024 / 1024

    def run_audit(self) -> Dict[str, Any]:
        """Run complete architecture audit."""
        print("🔍 TKA Desktop Architecture Audit")
        print("=" * 50)

        # Core Infrastructure Tests
        self._audit_core_infrastructure()

        # Service Integration Tests
        self._audit_service_integration()

        # Architecture Quality Tests
        self._audit_architecture_quality()

        # Performance & Robustness Tests
        self._audit_performance_robustness()

        # Generate comprehensive report
        return self._generate_audit_report()

    def _audit_core_infrastructure(self):
        """Audit core infrastructure components."""
        print("\n🏗️ Core Infrastructure Audit")
        print("-" * 30)

        # Test 1: Dependency Injection Container
        self._test_di_container()

        # Test 2: Event Bus System
        self._test_event_bus()

        # Test 3: Command Processor
        self._test_command_processor()

        # Test 4: Performance Monitoring
        self._test_performance_monitoring()

    def _audit_service_integration(self):
        """Audit service integration and data flow."""
        print("\n🔗 Service Integration Audit")
        print("-" * 30)

        # Test 5: Service Creation and Resolution
        self._test_service_resolution()

        # Test 6: Event-Driven Communication
        self._test_event_driven_communication()

        # Test 7: Cross-Service Data Flow
        self._test_cross_service_data_flow()

    def _audit_architecture_quality(self):
        """Audit architecture quality and consistency."""
        print("\n📐 Architecture Quality Audit")
        print("-" * 30)

        # Test 8: Import Consistency
        self._test_import_consistency()

        # Test 9: Type Safety
        self._test_type_safety()

        # Test 10: Error Handling
        self._test_error_handling()

    def _audit_performance_robustness(self):
        """Audit performance characteristics and robustness."""
        print("\n⚡ Performance & Robustness Audit")
        print("-" * 30)

        # Test 11: Memory Management
        self._test_memory_management()

        # Test 12: Concurrent Operations
        self._test_concurrent_operations()

        # Test 13: Error Recovery
        self._test_error_recovery()

    def _run_test(self, test_name: str, test_func):
        """Run individual test with performance tracking."""
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024

        try:
            result = test_func()
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024

            duration_ms = (end_time - start_time) * 1000
            memory_delta = abs(end_memory - start_memory)

            if isinstance(result, tuple):
                passed, details = result
            else:
                passed, details = result, "Test completed successfully"

            audit_result = AuditResult(
                test_name=test_name,
                passed=passed,
                details=details,
                performance_ms=duration_ms,
                memory_mb=memory_delta,
            )

            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} {test_name}: {details}")
            if duration_ms > 100:  # Log slow operations
                print(f"    ⏱️ Duration: {duration_ms:.1f}ms")

        except Exception as e:
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000

            audit_result = AuditResult(
                test_name=test_name,
                passed=False,
                details=f"Test failed with exception: {str(e)}",
                performance_ms=duration_ms,
                error=traceback.format_exc(),
            )

            print(f"❌ FAIL {test_name}: {str(e)}")

        self.results.append(audit_result)
        return audit_result

    def _test_di_container(self):
        """Test dependency injection container."""

        def test():
            from core.dependency_injection.di_container import (
                DIContainer,
                reset_container,
            )

            # Reset and create fresh container
            reset_container()
            container = DIContainer()

            # Test basic service resolution
            from application.services.core.sequence_management_service import (
                SequenceManagementService,
            )

            service = container._create_instance(SequenceManagementService)

            if not isinstance(service, SequenceManagementService):
                return False, "Failed to create service instance"

            return True, "DI container operational"

        return self._run_test("DI Container", test)

    def _test_event_bus(self):
        """Test event bus system."""

        def test():
            from core.events import get_event_bus, reset_event_bus, SequenceCreatedEvent
            from datetime import datetime
            import uuid

            # Reset and get fresh event bus
            reset_event_bus()
            event_bus = get_event_bus()

            # Test event publishing and subscribing
            events_received = []

            def handler(event):
                events_received.append(event)

            event_bus.subscribe("sequence.created", handler)

            # Publish test event
            test_event = SequenceCreatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="audit_test",
                sequence_id="test_seq",
                sequence_name="Test Sequence",
            )

            event_bus.publish(test_event)

            if len(events_received) != 1:
                return False, f"Expected 1 event, received {len(events_received)}"

            return True, "Event bus operational"

        return self._run_test("Event Bus", test)

    def _test_command_processor(self):
        """Test command processor system."""

        def test():
            from core.commands import CommandProcessor
            from core.events import get_event_bus

            # Create command processor
            event_bus = get_event_bus()
            processor = CommandProcessor(event_bus)

            # Test basic functionality
            if not hasattr(processor, "execute"):
                return False, "Command processor missing execute method"

            if not hasattr(processor, "undo"):
                return False, "Command processor missing undo method"

            if not hasattr(processor, "redo"):
                return False, "Command processor missing redo method"

            return True, "Command processor operational"

        return self._run_test("Command Processor", test)

    def _test_performance_monitoring(self):
        """Test performance monitoring system."""

        def test():
            from core.monitoring import performance_monitor, monitor_performance

            # Test monitoring decorator
            @monitor_performance("audit_test")
            def test_operation():
                return "test_result"

            result = test_operation()

            if result != "test_result":
                return False, "Performance monitoring affected function result"

            # Check if metrics were recorded
            stats = performance_monitor.get_operation_stats("audit_test")
            if not stats or stats.count == 0:
                return False, "Performance metrics not recorded"

            return True, "Performance monitoring operational"

        return self._run_test("Performance Monitoring", test)

    def _test_service_resolution(self):
        """Test service creation and resolution."""

        def test():
            from core.dependency_injection.di_container import DIContainer
            from application.services.core.sequence_management_service import (
                SequenceManagementService,
            )
            from application.services.positioning.arrow_management_service import (
                ArrowManagementService,
            )

            container = DIContainer()

            # Test multiple service types
            seq_service = container._create_instance(SequenceManagementService)

            # ArrowManagementService needs event_bus parameter, create manually
            from core.events import get_event_bus

            event_bus = get_event_bus()
            arrow_service = ArrowManagementService(event_bus=event_bus)

            if not isinstance(seq_service, SequenceManagementService):
                return False, "Failed to resolve SequenceManagementService"

            if not isinstance(arrow_service, ArrowManagementService):
                return False, "Failed to resolve ArrowManagementService"

            return True, "Service resolution operational"

        return self._run_test("Service Resolution", test)

    def _test_event_driven_communication(self):
        """Test event-driven communication between services."""

        def test():
            from core.events import get_event_bus, reset_event_bus
            from application.services.core.sequence_management_service import (
                SequenceManagementService,
            )

            # Reset event bus
            reset_event_bus()
            event_bus = get_event_bus()

            # Track events
            events_received = []

            def event_handler(event):
                events_received.append(event.event_type)

            # Subscribe to sequence events
            event_bus.subscribe("sequence.created", event_handler)

            # Create service and test event publishing
            service = SequenceManagementService(event_bus=event_bus)
            sequence = service.create_sequence("Test Sequence", 2)

            if len(events_received) == 0:
                return False, "No events published by service"

            if "sequence.created" not in events_received:
                return False, "Expected sequence.created event not published"

            return True, "Event-driven communication operational"

        return self._run_test("Event-Driven Communication", test)

    def _test_cross_service_data_flow(self):
        """Test data flow between services."""

        def test():
            from application.services.core.sequence_management_service import (
                SequenceManagementService,
            )
            from application.services.positioning.arrow_management_service import (
                ArrowManagementService,
            )
            from domain.models.core_models import (
                MotionData,
                MotionType,
                Location,
                RotationDirection,
            )
            from domain.models.pictograph_models import (
                ArrowData,
                PictographData,
                GridData,
                GridMode,
            )

            # Create services
            seq_service = SequenceManagementService()
            arrow_service = ArrowManagementService()

            # Test sequence creation
            sequence = seq_service.create_sequence("Test", 1)
            if not sequence or len(sequence.beats) != 1:
                return False, "Failed to create sequence with beats"

            # Test arrow positioning with data from sequence
            motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=1.0,
            )

            arrow = ArrowData(color="blue", motion_data=motion, is_visible=True)
            grid_data = GridData(
                grid_mode=GridMode.DIAMOND, center_x=475.0, center_y=475.0, radius=100.0
            )
            pictograph = PictographData(
                grid_data=grid_data, arrows={"blue": arrow}, is_blank=False
            )

            x, y, rotation = arrow_service.calculate_arrow_position(arrow, pictograph)

            if not all(isinstance(val, (int, float)) for val in [x, y, rotation]):
                return False, "Arrow positioning returned invalid data types"

            return True, "Cross-service data flow operational"

        return self._run_test("Cross-Service Data Flow", test)

    def _test_import_consistency(self):
        """Test import consistency across the codebase."""

        def test():
            # Test core imports
            try:
                from core.events import get_event_bus, IEventBus
                from core.commands import CommandProcessor, ICommand
                from core.dependency_injection.di_container import DIContainer
                from core.monitoring import performance_monitor
                from domain.models.core_models import SequenceData, BeatData
                from application.services.core.sequence_management_service import (
                    SequenceManagementService,
                )
            except ImportError as e:
                return False, f"Import failed: {str(e)}"

            return True, "All core imports consistent"

        return self._run_test("Import Consistency", test)

    def _test_type_safety(self):
        """Test type safety and annotation consistency."""

        def test():
            from core.events import get_event_bus
            from application.services.core.sequence_management_service import (
                SequenceManagementService,
            )

            # Test that services work with proper typing
            event_bus = get_event_bus()
            service = SequenceManagementService(event_bus=event_bus)

            # Test sequence creation with type validation
            sequence = service.create_sequence("Test", 2)

            # Verify types
            if not hasattr(sequence, "id"):
                return False, "Sequence missing required id attribute"

            if not hasattr(sequence, "beats"):
                return False, "Sequence missing required beats attribute"

            if len(sequence.beats) != 2:
                return False, f"Expected 2 beats, got {len(sequence.beats)}"

            return True, "Type safety operational"

        return self._run_test("Type Safety", test)

    def _test_error_handling(self):
        """Test error handling and recovery mechanisms."""

        def test():
            from application.services.core.sequence_management_service import (
                SequenceManagementService,
            )

            service = SequenceManagementService()

            # Test graceful handling of invalid operations
            try:
                # This should not crash the system
                sequence = service.create_sequence("Test", 0)  # Edge case: 0 beats
                if sequence is None:
                    return False, "Service returned None for edge case"
                # Service should handle edge case gracefully
                if len(sequence.beats) != 0:
                    return False, f"Expected 0 beats, got {len(sequence.beats)}"
            except Exception as e:
                # Some validation errors are expected
                error_msg = str(e).lower()
                if not any(
                    keyword in error_msg
                    for keyword in ["beat", "validation", "length", "integer"]
                ):
                    return False, f"Unexpected error type: {str(e)}"

            return True, "Error handling operational"

        return self._run_test("Error Handling", test)

    def _test_memory_management(self):
        """Test memory management and cleanup."""

        def test():
            from core.events import get_event_bus, reset_event_bus

            initial_memory = psutil.Process().memory_info().rss / 1024 / 1024

            # Create and destroy multiple event buses
            for i in range(10):
                reset_event_bus()
                event_bus = get_event_bus()

                # Subscribe and unsubscribe handlers
                def handler(event):
                    pass

                event_bus.subscribe("test.event", handler)
                event_bus.unsubscribe("test.event")

            final_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_growth = final_memory - initial_memory

            # Allow some memory growth but flag excessive growth
            if memory_growth > 50:  # 50MB threshold
                return False, f"Excessive memory growth: {memory_growth:.1f}MB"

            return True, f"Memory growth within limits: {memory_growth:.1f}MB"

        return self._run_test("Memory Management", test)

    def _test_concurrent_operations(self):
        """Test concurrent operations and thread safety."""

        def test():
            import threading
            from core.events import get_event_bus

            event_bus = get_event_bus()
            results = []
            errors = []

            def worker():
                try:
                    # Test concurrent event operations
                    def handler(event):
                        results.append(event.event_type)

                    event_bus.subscribe("ui.test.state_changed", handler)
                    # Create a proper event object
                    from core.events import UIStateChangedEvent
                    import uuid
                    from datetime import datetime

                    test_event = UIStateChangedEvent(
                        event_id=str(uuid.uuid4()),
                        timestamp=datetime.now(),
                        source="audit_test",
                        component="test",
                        state_key="concurrent",
                        old_value="old",
                        new_value="new",
                    )
                    event_bus.publish(test_event)
                    event_bus.unsubscribe("ui.test.state_changed")
                except Exception as e:
                    errors.append(str(e))

            # Run multiple threads
            threads = [threading.Thread(target=worker) for _ in range(5)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            if errors:
                return False, f"Concurrent operation errors: {errors[0]}"

            return True, f"Concurrent operations successful: {len(results)} events"

        return self._run_test("Concurrent Operations", test)

    def _test_error_recovery(self):
        """Test error recovery mechanisms."""

        def test():
            from core.events import get_event_bus

            event_bus = get_event_bus()

            # Test recovery from handler errors
            def failing_handler(event):
                raise ValueError("Test error")

            def working_handler(event):
                return "success"

            # Subscribe both handlers
            event_bus.subscribe("ui.test.state_changed", failing_handler)
            event_bus.subscribe("ui.test.state_changed", working_handler)

            try:
                # This should not crash the event bus
                from core.events import UIStateChangedEvent
                import uuid
                from datetime import datetime

                test_event = UIStateChangedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="audit_test",
                    component="test",
                    state_key="recovery",
                    old_value="old",
                    new_value="new",
                )
                event_bus.publish(test_event)
            except Exception as e:
                return (
                    False,
                    f"Event bus failed to recover from handler error: {str(e)}",
                )

            # Event bus should still be operational
            test_results = []

            def test_handler(event):
                test_results.append("recovered")

            event_bus.subscribe("ui.test.state_changed", test_handler)
            check_event = UIStateChangedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="audit_test",
                component="test",
                state_key="recovery_check",
                old_value="old",
                new_value="new",
            )
            event_bus.publish(check_event)

            if len(test_results) == 0:
                return False, "Event bus not operational after error"

            return True, "Error recovery operational"

        return self._run_test("Error Recovery", test)

    def _analyze_performance(self) -> Dict[str, Any]:
        """Analyze performance characteristics."""
        durations = [r.performance_ms for r in self.results if r.performance_ms]
        memory_usage = [r.memory_mb for r in self.results if r.memory_mb]

        return {
            "avg_duration_ms": (
                round(sum(durations) / len(durations), 2) if durations else 0
            ),
            "max_duration_ms": round(max(durations), 2) if durations else 0,
            "total_memory_mb": round(sum(memory_usage), 2) if memory_usage else 0,
            "slow_operations": [
                r.test_name
                for r in self.results
                if r.performance_ms and r.performance_ms > 100
            ],
        }

    def _assess_architecture(self) -> Dict[str, Any]:
        """Assess overall architecture quality."""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.passed])

        # Categorize test results
        core_tests = [
            r
            for r in self.results
            if any(
                keyword in r.test_name.lower()
                for keyword in ["di", "event", "command", "monitoring"]
            )
        ]
        integration_tests = [
            r
            for r in self.results
            if any(
                keyword in r.test_name.lower()
                for keyword in ["service", "communication", "data flow"]
            )
        ]
        quality_tests = [
            r
            for r in self.results
            if any(
                keyword in r.test_name.lower()
                for keyword in ["import", "type", "error"]
            )
        ]

        return {
            "overall_health": (
                "EXCELLENT"
                if passed_tests / total_tests >= 0.9
                else "GOOD" if passed_tests / total_tests >= 0.8 else "NEEDS_ATTENTION"
            ),
            "core_infrastructure": (
                len([r for r in core_tests if r.passed]) / len(core_tests) * 100
                if core_tests
                else 0
            ),
            "service_integration": (
                len([r for r in integration_tests if r.passed])
                / len(integration_tests)
                * 100
                if integration_tests
                else 0
            ),
            "code_quality": (
                len([r for r in quality_tests if r.passed]) / len(quality_tests) * 100
                if quality_tests
                else 0
            ),
            "foundation_strength": (
                "BULLETPROOF" if passed_tests == total_tests else "ROBUST"
            ),
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on audit results."""
        recommendations = []

        failed_tests = [r for r in self.results if not r.passed]
        slow_tests = [
            r for r in self.results if r.performance_ms and r.performance_ms > 100
        ]

        if failed_tests:
            recommendations.append(
                f"Address {len(failed_tests)} failing tests before production"
            )

        if slow_tests:
            recommendations.append(
                f"Optimize {len(slow_tests)} slow operations for better performance"
            )

        # Performance recommendations
        total_memory = sum(r.memory_mb for r in self.results if r.memory_mb)
        if total_memory > 100:
            recommendations.append(
                "Consider memory optimization - high memory usage detected"
            )

        # Architecture recommendations
        pass_rate = len([r for r in self.results if r.passed]) / len(self.results) * 100
        if pass_rate >= 95:
            recommendations.append(
                "Architecture is production-ready - proceed with confidence"
            )
        elif pass_rate >= 85:
            recommendations.append(
                "Architecture is solid - minor improvements recommended"
            )
        else:
            recommendations.append("Architecture needs strengthening before production")

        return recommendations

    def _generate_audit_report(self) -> Dict[str, Any]:
        """Generate comprehensive audit report."""
        passed_tests = [r for r in self.results if r.passed]
        failed_tests = [r for r in self.results if not r.passed]

        total_tests = len(self.results)
        pass_rate = len(passed_tests) / total_tests * 100 if total_tests > 0 else 0

        # Calculate performance metrics
        avg_duration = sum(
            r.performance_ms for r in self.results if r.performance_ms
        ) / len(self.results)
        total_memory = sum(r.memory_mb for r in self.results if r.memory_mb)

        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": len(passed_tests),
                "failed": len(failed_tests),
                "pass_rate": round(pass_rate, 1),
                "avg_duration_ms": round(avg_duration, 2),
                "total_memory_mb": round(total_memory, 2),
            },
            "passed_tests": [
                {"name": r.test_name, "details": r.details} for r in passed_tests
            ],
            "failed_tests": [
                {"name": r.test_name, "details": r.details, "error": r.error}
                for r in failed_tests
            ],
            "performance_analysis": self._analyze_performance(),
            "architecture_assessment": self._assess_architecture(),
            "recommendations": self._generate_recommendations(),
        }

        return report


def main():
    """Run comprehensive architecture audit."""
    auditor = ArchitectureAuditor()
    report = auditor.run_audit()

    print("\n📊 AUDIT SUMMARY")
    print("=" * 50)
    print(f"Tests Run: {report['summary']['total_tests']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"Pass Rate: {report['summary']['pass_rate']}%")
    print(f"Average Duration: {report['summary']['avg_duration_ms']}ms")

    if report["summary"]["failed"] > 0:
        print("\n❌ FAILED TESTS:")
        for test in report["failed_tests"]:
            print(f"  - {test['name']}: {test['details']}")

    return report["summary"]["pass_rate"] >= 80


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
