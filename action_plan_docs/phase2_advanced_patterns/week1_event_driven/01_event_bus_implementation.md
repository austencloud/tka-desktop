# **Task 2.1: Type-Safe Event Bus Implementation**

**Timeline**: Week 1 of Phase 2  
**Priority**: HIGH  
**Goal**: Implement event-driven architecture with type-safe event bus

---

## **Create Event Infrastructure:**

### **FILE: src/core/events/event_bus.py**

```python
"""
Type-safe event bus for decoupled component communication.
Replaces direct method calls with event-driven architecture.
"""

from typing import TypeVar, Type, Dict, List, Callable, Any, Generic
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging
import asyncio
from datetime import datetime

T = TypeVar("T")

@dataclass(frozen=True)
class BaseEvent(ABC):
    """Base class for all events in the system."""
    timestamp: float
    source_component: str
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

class IEventBus(ABC):
    """Interface for event bus implementations."""

    @abstractmethod
    def publish(self, event: BaseEvent) -> None:
        """Publish an event to all subscribers."""
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[T], handler: Callable[[T], None]) -> str:
        """Subscribe to events of a specific type. Returns subscription ID."""
        pass

    @abstractmethod
    def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from events."""
        pass

class TypeSafeEventBus(IEventBus):
    """
    High-performance, type-safe event bus with error isolation.
    """

    def __init__(self):
        self._handlers: Dict[Type, List[Tuple[str, Callable]]] = defaultdict(list)
        self._subscription_counter = 0
        self._logger = logging.getLogger(__name__)

    def publish(self, event: BaseEvent) -> None:
        """Publish event with error isolation."""
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])

        self._logger.debug(f"Publishing {event_type.__name__} to {len(handlers)} handlers")

        failed_handlers = []
        for subscription_id, handler in handlers:
            try:
                handler(event)
            except Exception as e:
                self._logger.error(
                    f"Event handler {subscription_id} failed for {event_type.__name__}: {e}"
                )
                failed_handlers.append(subscription_id)

        # Remove failed handlers to prevent repeated failures
        if failed_handlers:
            self._handlers[event_type] = [
                (sub_id, handler) for sub_id, handler in self._handlers[event_type]
                if sub_id not in failed_handlers
            ]

    def subscribe(self, event_type: Type[T], handler: Callable[[T], None]) -> str:
        """Subscribe with unique subscription ID."""
        self._subscription_counter += 1
        subscription_id = f"sub_{self._subscription_counter}"

        self._handlers[event_type].append((subscription_id, handler))

        self._logger.debug(f"Subscribed {subscription_id} to {event_type.__name__}")
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        """Remove subscription by ID."""
        for event_type, handlers in self._handlers.items():
            self._handlers[event_type] = [
                (sub_id, handler) for sub_id, handler in handlers
                if sub_id != subscription_id
            ]

    def get_subscription_count(self, event_type: Type) -> int:
        """Get number of subscribers for event type."""
        return len(self._handlers.get(event_type, []))
```

---

## **Enhanced Event Bus Features:**

### **Add Event Filtering and Middleware:**

```python
from typing import Optional, Union
from collections import defaultdict
import threading
import queue
import time

class EventFilter:
    """Filter for event subscriptions."""

    def __init__(self, predicate: Callable[[BaseEvent], bool]):
        self.predicate = predicate

    def matches(self, event: BaseEvent) -> bool:
        """Check if event matches filter."""
        try:
            return self.predicate(event)
        except Exception:
            return False

class EventMiddleware:
    """Middleware for event processing."""

    def process_before(self, event: BaseEvent) -> Optional[BaseEvent]:
        """Process event before publishing. Return None to cancel event."""
        return event

    def process_after(self, event: BaseEvent, handlers_called: int) -> None:
        """Process event after publishing."""
        pass

class AdvancedEventBus(TypeSafeEventBus):
    """Enhanced event bus with filtering, middleware, and async support."""

    def __init__(self, enable_async: bool = False):
        super().__init__()
        self._middleware: List[EventMiddleware] = []
        self._filtered_handlers: Dict[Type, List[Tuple[str, Callable, Optional[EventFilter]]]] = defaultdict(list)
        self._enable_async = enable_async
        self._event_queue: Optional[queue.Queue] = queue.Queue() if enable_async else None
        self._processing_thread: Optional[threading.Thread] = None
        self._stop_processing = threading.Event()

        if enable_async:
            self._start_async_processing()

    def add_middleware(self, middleware: EventMiddleware) -> None:
        """Add middleware to the event bus."""
        self._middleware.append(middleware)

    def subscribe_with_filter(self,
                             event_type: Type[T],
                             handler: Callable[[T], None],
                             event_filter: Optional[EventFilter] = None) -> str:
        """Subscribe with optional event filter."""
        self._subscription_counter += 1
        subscription_id = f"sub_{self._subscription_counter}"

        self._filtered_handlers[event_type].append((subscription_id, handler, event_filter))

        self._logger.debug(f"Subscribed {subscription_id} to {event_type.__name__} with filter")
        return subscription_id

    def publish(self, event: BaseEvent) -> None:
        """Publish event with middleware and filtering support."""
        if self._enable_async:
            self._event_queue.put(event)
        else:
            self._publish_sync(event)

    def _publish_sync(self, event: BaseEvent) -> None:
        """Synchronous event publishing."""
        # Process middleware before
        processed_event = event
        for middleware in self._middleware:
            processed_event = middleware.process_before(processed_event)
            if processed_event is None:
                return  # Event was cancelled by middleware

        event_type = type(processed_event)
        handlers_called = 0

        # Handle filtered subscribers
        filtered_handlers = self._filtered_handlers.get(event_type, [])
        for subscription_id, handler, event_filter in filtered_handlers:
            try:
                if event_filter is None or event_filter.matches(processed_event):
                    handler(processed_event)
                    handlers_called += 1
            except Exception as e:
                self._logger.error(
                    f"Filtered event handler {subscription_id} failed for {event_type.__name__}: {e}"
                )

        # Handle regular subscribers
        regular_handlers = self._handlers.get(event_type, [])
        for subscription_id, handler in regular_handlers:
            try:
                handler(processed_event)
                handlers_called += 1
            except Exception as e:
                self._logger.error(
                    f"Event handler {subscription_id} failed for {event_type.__name__}: {e}"
                )

        # Process middleware after
        for middleware in self._middleware:
            try:
                middleware.process_after(processed_event, handlers_called)
            except Exception as e:
                self._logger.error(f"Middleware post-processing failed: {e}")

        self._logger.debug(f"Published {event_type.__name__} to {handlers_called} handlers")

    def _start_async_processing(self) -> None:
        """Start async event processing thread."""
        self._processing_thread = threading.Thread(target=self._process_events_async, daemon=True)
        self._processing_thread.start()

    def _process_events_async(self) -> None:
        """Process events asynchronously."""
        while not self._stop_processing.is_set():
            try:
                event = self._event_queue.get(timeout=0.1)
                self._publish_sync(event)
                self._event_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                self._logger.error(f"Async event processing failed: {e}")

    def shutdown(self) -> None:
        """Shutdown async processing."""
        if self._enable_async:
            self._stop_processing.set()
            if self._processing_thread:
                self._processing_thread.join(timeout=1.0)

    def wait_for_all_events(self, timeout: Optional[float] = None) -> bool:
        """Wait for all queued events to be processed."""
        if not self._enable_async or not self._event_queue:
            return True

        try:
            if timeout:
                start_time = time.time()
                while not self._event_queue.empty():
                    if time.time() - start_time > timeout:
                        return False
                    time.sleep(0.01)
            else:
                self._event_queue.join()
            return True
        except Exception:
            return False

# Event Statistics and Monitoring
class EventBusStatistics:
    """Statistics and monitoring for event bus."""

    def __init__(self, event_bus: AdvancedEventBus):
        self.event_bus = event_bus
        self._event_counts: Dict[str, int] = defaultdict(int)
        self._handler_counts: Dict[str, int] = defaultdict(int)
        self._error_counts: Dict[str, int] = defaultdict(int)
        self._processing_times: Dict[str, List[float]] = defaultdict(list)

        # Add monitoring middleware
        self.event_bus.add_middleware(StatisticsMiddleware(self))

    def get_event_count(self, event_type_name: str) -> int:
        """Get count of published events by type."""
        return self._event_counts[event_type_name]

    def get_handler_count(self, event_type_name: str) -> int:
        """Get count of handlers called for event type."""
        return self._handler_counts[event_type_name]

    def get_error_count(self, event_type_name: str) -> int:
        """Get count of handler errors for event type."""
        return self._error_counts[event_type_name]

    def get_average_processing_time(self, event_type_name: str) -> float:
        """Get average processing time for event type."""
        times = self._processing_times[event_type_name]
        return sum(times) / len(times) if times else 0.0

    def get_statistics_report(self) -> Dict[str, Any]:
        """Get comprehensive statistics report."""
        report = {
            "total_events": sum(self._event_counts.values()),
            "total_handlers": sum(self._handler_counts.values()),
            "total_errors": sum(self._error_counts.values()),
            "event_types": {}
        }

        for event_type in set(self._event_counts.keys()):
            report["event_types"][event_type] = {
                "events_published": self._event_counts[event_type],
                "handlers_called": self._handler_counts[event_type],
                "errors": self._error_counts[event_type],
                "avg_processing_time_ms": self.get_average_processing_time(event_type) * 1000
            }

        return report

class StatisticsMiddleware(EventMiddleware):
    """Middleware for collecting event statistics."""

    def __init__(self, stats: EventBusStatistics):
        self.stats = stats
        self._start_time: Optional[float] = None

    def process_before(self, event: BaseEvent) -> Optional[BaseEvent]:
        """Record event start."""
        event_type_name = type(event).__name__
        self.stats._event_counts[event_type_name] += 1
        self._start_time = time.perf_counter()
        return event

    def process_after(self, event: BaseEvent, handlers_called: int) -> None:
        """Record event completion."""
        if self._start_time is not None:
            processing_time = time.perf_counter() - self._start_time
            event_type_name = type(event).__name__

            self.stats._handler_counts[event_type_name] += handlers_called
            self.stats._processing_times[event_type_name].append(processing_time)

            # Keep only last 100 measurements for memory efficiency
            if len(self.stats._processing_times[event_type_name]) > 100:
                self.stats._processing_times[event_type_name] = \
                    self.stats._processing_times[event_type_name][-100:]
```

---

## **Event Bus Factory and Registration:**

### **Create Event Bus Factory:**

```python
# FILE: src/core/events/event_bus_factory.py

"""
Factory for creating and configuring event bus instances.
"""

from typing import Optional, List
from .event_bus import IEventBus, TypeSafeEventBus, AdvancedEventBus, EventBusStatistics
from .middleware import LoggingMiddleware, PerformanceMiddleware, ValidationMiddleware

class EventBusFactory:
    """Factory for creating configured event bus instances."""

    @staticmethod
    def create_simple_event_bus() -> IEventBus:
        """Create simple synchronous event bus."""
        return TypeSafeEventBus()

    @staticmethod
    def create_advanced_event_bus(enable_async: bool = False,
                                 enable_statistics: bool = True,
                                 enable_logging: bool = True,
                                 enable_performance_monitoring: bool = True) -> IEventBus:
        """Create advanced event bus with optional features."""
        event_bus = AdvancedEventBus(enable_async=enable_async)

        # Add middleware based on configuration
        if enable_logging:
            event_bus.add_middleware(LoggingMiddleware())

        if enable_performance_monitoring:
            event_bus.add_middleware(PerformanceMiddleware())

        event_bus.add_middleware(ValidationMiddleware())

        # Add statistics if requested
        if enable_statistics:
            EventBusStatistics(event_bus)

        return event_bus

    @staticmethod
    def create_tka_event_bus() -> IEventBus:
        """Create event bus configured specifically for TKA application."""
        return EventBusFactory.create_advanced_event_bus(
            enable_async=True,  # TKA benefits from async event processing
            enable_statistics=True,  # Useful for performance monitoring
            enable_logging=True,  # Important for debugging
            enable_performance_monitoring=True  # Track performance regressions
        )

# Additional middleware implementations
class LoggingMiddleware(EventMiddleware):
    """Middleware for logging event publishing."""

    def __init__(self):
        self._logger = logging.getLogger("EventBus")

    def process_before(self, event: BaseEvent) -> Optional[BaseEvent]:
        """Log event before publishing."""
        self._logger.debug(f"Publishing event: {type(event).__name__} from {event.source_component}")
        return event

    def process_after(self, event: BaseEvent, handlers_called: int) -> None:
        """Log event after publishing."""
        self._logger.debug(f"Event {type(event).__name__} handled by {handlers_called} handlers")

class PerformanceMiddleware(EventMiddleware):
    """Middleware for performance monitoring."""

    def __init__(self, slow_threshold_ms: float = 10.0):
        self.slow_threshold_ms = slow_threshold_ms
        self._logger = logging.getLogger("EventBus.Performance")
        self._start_time: Optional[float] = None

    def process_before(self, event: BaseEvent) -> Optional[BaseEvent]:
        """Start performance timing."""
        self._start_time = time.perf_counter()
        return event

    def process_after(self, event: BaseEvent, handlers_called: int) -> None:
        """Check for slow event processing."""
        if self._start_time is not None:
            duration_ms = (time.perf_counter() - self._start_time) * 1000

            if duration_ms > self.slow_threshold_ms:
                self._logger.warning(
                    f"Slow event processing: {type(event).__name__} took {duration_ms:.2f}ms "
                    f"with {handlers_called} handlers"
                )

class ValidationMiddleware(EventMiddleware):
    """Middleware for event validation."""

    def __init__(self):
        self._logger = logging.getLogger("EventBus.Validation")

    def process_before(self, event: BaseEvent) -> Optional[BaseEvent]:
        """Validate event before publishing."""
        # Check required fields
        if not hasattr(event, 'timestamp') or event.timestamp <= 0:
            self._logger.error(f"Invalid timestamp in event {type(event).__name__}")
            return None

        if not hasattr(event, 'source_component') or not event.source_component:
            self._logger.error(f"Missing source_component in event {type(event).__name__}")
            return None

        return event
```

---

## **Testing the Event Bus:**

### **FILE: tests/specification/core/test_event_bus.py**

```python
"""
Tests for the event bus implementation.
"""

import pytest
import time
from typing import Any
from src.core.events.event_bus import (
    BaseEvent, IEventBus, TypeSafeEventBus, AdvancedEventBus,
    EventFilter, EventBusStatistics
)
from src.core.events.event_bus_factory import EventBusFactory

@dataclass(frozen=True)
class TestEvent(BaseEvent):
    """Test event for unit tests."""
    message: str

@dataclass(frozen=True)
class AnotherTestEvent(BaseEvent):
    """Another test event for unit tests."""
    value: int

class TestEventBus:

    def test_basic_publish_subscribe(self):
        """Test basic event publishing and subscription."""
        event_bus = TypeSafeEventBus()
        received_events = []

        def handler(event: TestEvent):
            received_events.append(event)

        # Subscribe to events
        sub_id = event_bus.subscribe(TestEvent, handler)

        # Publish event
        test_event = TestEvent(
            timestamp=time.time(),
            source_component="test",
            message="Hello World"
        )
        event_bus.publish(test_event)

        # Verify event was received
        assert len(received_events) == 1
        assert received_events[0].message == "Hello World"

    def test_multiple_subscribers(self):
        """Test multiple subscribers to the same event type."""
        event_bus = TypeSafeEventBus()
        received_count = {"count": 0}

        def handler1(event: TestEvent):
            received_count["count"] += 1

        def handler2(event: TestEvent):
            received_count["count"] += 10

        # Subscribe multiple handlers
        event_bus.subscribe(TestEvent, handler1)
        event_bus.subscribe(TestEvent, handler2)

        # Publish event
        test_event = TestEvent(
            timestamp=time.time(),
            source_component="test",
            message="Test"
        )
        event_bus.publish(test_event)

        # Both handlers should be called
        assert received_count["count"] == 11

    def test_type_safety(self):
        """Test that handlers only receive events of subscribed type."""
        event_bus = TypeSafeEventBus()
        test_events = []
        other_events = []

        def test_handler(event: TestEvent):
            test_events.append(event)

        def other_handler(event: AnotherTestEvent):
            other_events.append(event)

        # Subscribe to different event types
        event_bus.subscribe(TestEvent, test_handler)
        event_bus.subscribe(AnotherTestEvent, other_handler)

        # Publish both types
        test_event = TestEvent(timestamp=time.time(), source_component="test", message="Test")
        other_event = AnotherTestEvent(timestamp=time.time(), source_component="test", value=42)

        event_bus.publish(test_event)
        event_bus.publish(other_event)

        # Each handler should only receive its type
        assert len(test_events) == 1
        assert len(other_events) == 1
        assert test_events[0].message == "Test"
        assert other_events[0].value == 42

    def test_unsubscribe(self):
        """Test unsubscribing from events."""
        event_bus = TypeSafeEventBus()
        received_events = []

        def handler(event: TestEvent):
            received_events.append(event)

        # Subscribe and then unsubscribe
        sub_id = event_bus.subscribe(TestEvent, handler)
        event_bus.unsubscribe(sub_id)

        # Publish event after unsubscribing
        test_event = TestEvent(timestamp=time.time(), source_component="test", message="Test")
        event_bus.publish(test_event)

        # Should not receive any events
        assert len(received_events) == 0

    def test_error_isolation(self):
        """Test that handler errors don't affect other handlers."""
        event_bus = TypeSafeEventBus()
        successful_calls = []

        def failing_handler(event: TestEvent):
            raise ValueError("Handler failure")

        def successful_handler(event: TestEvent):
            successful_calls.append(event)

        # Subscribe both handlers
        event_bus.subscribe(TestEvent, failing_handler)
        event_bus.subscribe(TestEvent, successful_handler)

        # Publish event
        test_event = TestEvent(timestamp=time.time(), source_component="test", message="Test")
        event_bus.publish(test_event)

        # Successful handler should still be called
        assert len(successful_calls) == 1

class TestAdvancedEventBus:

    def test_event_filtering(self):
        """Test event filtering functionality."""
        event_bus = AdvancedEventBus()
        filtered_events = []
        all_events = []

        # Create filter for specific messages
        message_filter = EventFilter(lambda event: event.message.startswith("Important"))

        def filtered_handler(event: TestEvent):
            filtered_events.append(event)

        def all_handler(event: TestEvent):
            all_events.append(event)

        # Subscribe with and without filter
        event_bus.subscribe_with_filter(TestEvent, filtered_handler, message_filter)
        event_bus.subscribe(TestEvent, all_handler)

        # Publish various events
        important_event = TestEvent(timestamp=time.time(), source_component="test", message="Important message")
        normal_event = TestEvent(timestamp=time.time(), source_component="test", message="Normal message")

        event_bus.publish(important_event)
        event_bus.publish(normal_event)

        # Filtered handler should only receive important events
        assert len(filtered_events) == 1
        assert filtered_events[0].message == "Important message"

        # All handler should receive both
        assert len(all_events) == 2

    def test_statistics_collection(self):
        """Test event statistics collection."""
        event_bus = AdvancedEventBus()
        stats = EventBusStatistics(event_bus)

        def handler(event: TestEvent):
            pass

        event_bus.subscribe(TestEvent, handler)

        # Publish some events
        for i in range(5):
            test_event = TestEvent(timestamp=time.time(), source_component="test", message=f"Message {i}")
            event_bus.publish(test_event)

        # Check statistics
        assert stats.get_event_count("TestEvent") == 5
        assert stats.get_handler_count("TestEvent") == 5
        assert stats.get_error_count("TestEvent") == 0

    def test_async_processing(self):
        """Test asynchronous event processing."""
        event_bus = AdvancedEventBus(enable_async=True)
        received_events = []

        def handler(event: TestEvent):
            received_events.append(event)

        event_bus.subscribe(TestEvent, handler)

        # Publish events
        for i in range(3):
            test_event = TestEvent(timestamp=time.time(), source_component="test", message=f"Message {i}")
            event_bus.publish(test_event)

        # Wait for async processing
        success = event_bus.wait_for_all_events(timeout=1.0)
        assert success
        assert len(received_events) == 3

        # Cleanup
        event_bus.shutdown()

class TestEventBusFactory:

    def test_simple_event_bus_creation(self):
        """Test creation of simple event bus."""
        event_bus = EventBusFactory.create_simple_event_bus()
        assert isinstance(event_bus, TypeSafeEventBus)

    def test_advanced_event_bus_creation(self):
        """Test creation of advanced event bus."""
        event_bus = EventBusFactory.create_advanced_event_bus()
        assert isinstance(event_bus, AdvancedEventBus)

    def test_tka_event_bus_creation(self):
        """Test creation of TKA-specific event bus."""
        event_bus = EventBusFactory.create_tka_event_bus()
        assert isinstance(event_bus, AdvancedEventBus)
```

---

## **Integration with DI Container:**

### **Register Event Bus in DI Container:**

```python
# In your main application setup (v2/main.py):

def _register_core_services(self):
    """Register core services including event bus."""
    from src.core.events.event_bus import IEventBus
    from src.core.events.event_bus_factory import EventBusFactory

    # Create and register event bus
    event_bus = EventBusFactory.create_tka_event_bus()
    self.container.register_singleton(IEventBus, lambda: event_bus)

    logger.info("✅ Event bus registered successfully")
```

---

## **Success Criteria:**

By the end of Task 2.1:

- ✅ **Type-safe event bus** implemented and tested
- ✅ **Error isolation** prevents handler failures from affecting others
- ✅ **Event filtering** allows selective subscription
- ✅ **Statistics collection** for performance monitoring
- ✅ **Async processing** option for high-throughput scenarios
- ✅ **Integration with DI container** completed

---

## **Next Step**

After completing the event bus implementation, proceed to: [Task 2.2: Domain Events Definition](02_domain_events_definition.md)
