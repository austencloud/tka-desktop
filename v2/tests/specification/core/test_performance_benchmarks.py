"""
Performance benchmarks for TKA Modern core services.

These tests establish baseline performance metrics and detect regressions
in critical operations.

TESTS:
- Event bus performance under load
- DI container resolution speed
- Service operation benchmarks
- Memory usage validation
"""

import pytest
import time
import gc
import psutil
import os
from unittest.mock import Mock
from typing import List, Dict, Any

from src.core.events.event_bus import TypeSafeEventBus
from src.core.dependency_injection.di_container import DIContainer
from src.domain.models.core_models import (
    BeatData,
    SequenceData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)


class PerformanceTimer:
    """Context manager for measuring execution time."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.duration = None

    def __enter__(self):
        gc.collect()  # Clean up before measurement
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time


class MemoryProfiler:
    """Context manager for measuring memory usage."""

    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.start_memory = None
        self.end_memory = None
        self.memory_delta = None

    def __enter__(self):
        gc.collect()  # Clean up before measurement
        self.start_memory = self.process.memory_info().rss
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        gc.collect()  # Clean up after operation
        self.end_memory = self.process.memory_info().rss
        self.memory_delta = self.end_memory - self.start_memory


@pytest.mark.slow
class TestEventBusPerformance:
    """Performance tests for TypeSafeEventBus."""

    def test_event_publishing_performance(self):
        """Test event publishing performance under load."""
        event_bus = TypeSafeEventBus()

        # Setup event handler
        received_events = []

        def handler(event_data):
            received_events.append(event_data)

        event_bus.subscribe("test_event", handler)

        # Benchmark: Publish 1000 events
        event_count = 1000
        with PerformanceTimer() as timer:
            for i in range(event_count):
                event_bus.publish("test_event", {"index": i})

        # Performance assertion: Should handle 1000 events in under 100ms
        assert (
            timer.duration < 0.1
        ), f"Event publishing too slow: {timer.duration:.3f}s for {event_count} events"
        assert len(received_events) == event_count

    def test_event_subscription_performance(self):
        """Test event subscription/unsubscription performance."""
        event_bus = TypeSafeEventBus()

        # Benchmark: Subscribe/unsubscribe 100 handlers
        handler_count = 100
        handlers = []

        with PerformanceTimer() as timer:
            for i in range(handler_count):
                handler = lambda event_data, idx=i: None
                handlers.append(handler)
                event_bus.subscribe(f"event_{i}", handler)

        # Performance assertion: Should handle 100 subscriptions in under 10ms
        assert (
            timer.duration < 0.01
        ), f"Event subscription too slow: {timer.duration:.3f}s for {handler_count} handlers"

        # Benchmark unsubscription
        with PerformanceTimer() as timer:
            for i, handler in enumerate(handlers):
                event_bus.unsubscribe(f"event_{i}", handler)

        assert (
            timer.duration < 0.01
        ), f"Event unsubscription too slow: {timer.duration:.3f}s for {handler_count} handlers"

    def test_event_bus_memory_usage(self):
        """Test event bus memory usage under load."""
        event_bus = TypeSafeEventBus()

        # Setup handlers
        handlers = []
        for i in range(50):
            handler = lambda event_data, idx=i: None
            handlers.append(handler)
            event_bus.subscribe(f"event_{i}", handler)

        # Measure memory usage during event publishing
        with MemoryProfiler() as profiler:
            for i in range(1000):
                event_bus.publish(f"event_{i % 50}", {"data": f"test_{i}"})

        # Memory assertion: Should not leak significant memory
        # Allow up to 1MB memory increase for event processing
        assert (
            profiler.memory_delta < 1024 * 1024
        ), f"Event bus memory usage too high: {profiler.memory_delta} bytes"


@pytest.mark.slow
class TestDIContainerPerformance:
    """Performance tests for DIContainer."""

    def test_service_resolution_performance(self):
        """Test service resolution performance."""
        container = DIContainer()

        # Register a simple service
        class TestService:
            def __init__(self):
                self.value = "test"

        container.register_singleton(TestService, TestService)

        # Benchmark: Resolve service 1000 times
        resolution_count = 1000
        with PerformanceTimer() as timer:
            for _ in range(resolution_count):
                service = container.resolve(TestService)
                assert service is not None

        # Performance assertion: Should resolve 1000 services in under 50ms
        assert (
            timer.duration < 0.05
        ), f"Service resolution too slow: {timer.duration:.3f}s for {resolution_count} resolutions"

    def test_dependency_injection_performance(self):
        """Test dependency injection performance with complex dependencies."""
        container = DIContainer()

        # Setup complex dependency chain
        class ServiceA:
            def __init__(self):
                self.name = "ServiceA"

        class ServiceB:
            def __init__(self, service_a: ServiceA):
                self.service_a = service_a
                self.name = "ServiceB"

        class ServiceC:
            def __init__(self, service_a: ServiceA, service_b: ServiceB):
                self.service_a = service_a
                self.service_b = service_b
                self.name = "ServiceC"

        container.register_singleton(ServiceA, ServiceA)
        container.register_singleton(ServiceB, ServiceB)
        container.register_singleton(ServiceC, ServiceC)

        # Benchmark: Resolve complex service 100 times
        resolution_count = 100
        with PerformanceTimer() as timer:
            for _ in range(resolution_count):
                service = container.resolve(ServiceC)
                assert service.service_a is not None
                assert service.service_b is not None

        # Performance assertion: Should resolve complex dependencies in under 20ms
        assert (
            timer.duration < 0.02
        ), f"Complex DI too slow: {timer.duration:.3f}s for {resolution_count} resolutions"

    def test_container_memory_usage(self):
        """Test DI container memory usage."""
        container = DIContainer()

        # Register many services
        services = []
        with MemoryProfiler() as profiler:
            for i in range(100):
                class_name = f"TestService{i}"
                service_class = type(class_name, (), {"value": i})
                services.append(service_class)
                container.register_singleton(service_class, service_class)

        # Memory assertion: Should not use excessive memory for registration
        # Allow up to 500KB for 100 service registrations
        assert (
            profiler.memory_delta < 512 * 1024
        ), f"DI container memory usage too high: {profiler.memory_delta} bytes"


@pytest.mark.slow
class TestDomainModelPerformance:
    """Performance tests for domain models."""

    def test_beat_data_creation_performance(self):
        """Test BeatData creation performance."""
        motion_data = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

        # Benchmark: Create 1000 BeatData instances
        beat_count = 1000
        with PerformanceTimer() as timer:
            beats = []
            for i in range(beat_count):
                beat = BeatData(
                    beat_number=i + 1,
                    letter=chr(ord("A") + (i % 26)),
                    duration=1.0,
                    blue_motion=motion_data,
                    red_motion=motion_data,
                )
                beats.append(beat)

        # Performance assertion: Should create 1000 beats in under 100ms
        assert (
            timer.duration < 0.1
        ), f"BeatData creation too slow: {timer.duration:.3f}s for {beat_count} beats"
        assert len(beats) == beat_count

    def test_sequence_data_operations_performance(self):
        """Test SequenceData operations performance."""
        sequence = SequenceData.empty()

        # Benchmark: Add 64 beats to sequence
        beat_count = 64
        with PerformanceTimer() as timer:
            for i in range(beat_count):
                beat = BeatData(
                    beat_number=i + 1, letter=chr(ord("A") + (i % 26)), duration=1.0
                )
                sequence = sequence.add_beat(beat)

        # Performance assertion: Should add 64 beats in under 50ms
        assert (
            timer.duration < 0.05
        ), f"Sequence operations too slow: {timer.duration:.3f}s for {beat_count} beats"
        assert sequence.length == beat_count

    def test_serialization_performance(self):
        """Test domain model serialization performance."""
        # Create complex sequence
        sequence = SequenceData(name="Performance Test", word="PERFORMANCE")
        motion_data = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=2.5,
        )

        for i in range(16):
            beat = BeatData(
                beat_number=i + 1,
                letter=chr(ord("A") + (i % 26)),
                duration=1.0,
                blue_motion=motion_data,
                red_motion=motion_data,
            )
            sequence = sequence.add_beat(beat)

        # Benchmark: Serialize/deserialize 100 times
        iteration_count = 100
        with PerformanceTimer() as timer:
            for _ in range(iteration_count):
                data_dict = sequence.to_dict()
                reconstructed = SequenceData.from_dict(data_dict)
                assert reconstructed.length == sequence.length

        # Performance assertion: Should serialize/deserialize in under 200ms
        assert (
            timer.duration < 0.2
        ), f"Serialization too slow: {timer.duration:.3f}s for {iteration_count} iterations"


@pytest.mark.slow
class TestIntegratedPerformance:
    """Integrated performance tests across multiple components."""

    def test_full_workflow_performance(self):
        """Test performance of complete workflow operations."""
        # Setup components
        event_bus = TypeSafeEventBus()
        container = DIContainer()

        # Track events
        workflow_events = []

        def event_handler(event_data):
            workflow_events.append(event_data)

        event_bus.subscribe("workflow_step", event_handler)

        # Benchmark: Complete workflow with events and DI
        workflow_count = 50
        with PerformanceTimer() as timer:
            for i in range(workflow_count):
                # Create sequence
                sequence = SequenceData(name=f"Workflow {i}")

                # Add beats
                for j in range(8):
                    beat = BeatData(beat_number=j + 1, duration=1.0)
                    sequence = sequence.add_beat(beat)

                # Publish workflow event
                event_bus.publish(
                    "workflow_step",
                    {
                        "workflow_id": i,
                        "sequence_length": sequence.length,
                        "step": "complete",
                    },
                )

        # Performance assertion: Should complete 50 workflows in under 100ms
        assert (
            timer.duration < 0.1
        ), f"Integrated workflow too slow: {timer.duration:.3f}s for {workflow_count} workflows"
        assert len(workflow_events) == workflow_count

    def test_memory_stability_under_load(self):
        """Test memory stability under sustained load."""
        event_bus = TypeSafeEventBus()

        # Setup event handler
        processed_count = 0

        def handler(event_data):
            nonlocal processed_count
            processed_count += 1

        event_bus.subscribe("load_test", handler)

        # Sustained load test
        with MemoryProfiler() as profiler:
            for cycle in range(10):
                # Create and process data
                for i in range(100):
                    sequence = SequenceData(name=f"Load Test {cycle}-{i}")
                    for j in range(4):
                        beat = BeatData(beat_number=j + 1, duration=1.0)
                        sequence = sequence.add_beat(beat)

                    # Publish event
                    event_bus.publish(
                        "load_test",
                        {"cycle": cycle, "sequence": i, "length": sequence.length},
                    )

                # Force garbage collection between cycles
                gc.collect()

        # Memory assertion: Should not leak significant memory under sustained load
        # Allow up to 2MB memory increase for sustained operations
        assert (
            profiler.memory_delta < 2 * 1024 * 1024
        ), f"Memory leak detected: {profiler.memory_delta} bytes"
        assert processed_count == 1000
