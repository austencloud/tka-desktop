# 🚀 TKA Desktop V2 - Complete Implementation Phase Plan

**Project**: Kinetic Alphabet Desktop V2 Architecture Completion  
**Date**: June 15, 2025  
**Current Status**: 85% Architecture Complete  
**Goal**: Eliminate remaining technical debt and achieve world-class architecture

---

## 📋 **Phase Overview**

Based on the comprehensive architecture audit, your V2 implementation is **85% complete** with excellent foundations. The remaining 15% consists of:

1. **Phase 1**: Immediate Technical Debt Elimination (1 week)
2. **Phase 2**: Advanced Architecture Patterns (2 weeks)  
3. **Phase 3**: Enterprise-Grade Features (2 weeks)

**Total Timeline**: 5 weeks to achieve world-class architecture

---

# 🔥 **PHASE 1: IMMEDIATE TECHNICAL DEBT ELIMINATION**

**Timeline**: 1 Week  
**Priority**: CRITICAL  
**Goal**: Clean up remaining V1 cruft and complete core DI infrastructure

## **Day 1-2: V1 Compatibility Code Removal**

### **Task 1.1: Systematic V1 Code Identification**

**What to do:**
```bash
# Step 1: Find all V1 references
cd TKA/tka-desktop/v2/src/application/services
grep -r "V1\|v1" . --include="*.py" > v1_references.txt
grep -r "# V1\|# v1" . --include="*.py" >> v1_references.txt
grep -r "old\|Old\|OLD" . --include="*.py" >> v1_references.txt
grep -r "legacy\|Legacy" . --include="*.py" >> v1_references.txt

# Step 2: Find V1-style comments
grep -r "V1-style\|v1-style" . --include="*.py" >> v1_references.txt
grep -r "V1 approach\|v1 approach" . --include="*.py" >> v1_references.txt
```

**Expected Issues Found:**
```python
# EXAMPLE 1: arrow_management_service.py
def create_sections(self) -> None:
    """V1-style: Create sections with single-row layout for sections 4,5,6"""
    # V1-style: Create transparent horizontal container for sections 4, 5, 6
    # V1 approach: no finalization needed, QVBoxLayout just works!

# EXAMPLE 2: Various services
# Using DIAMOND layer2 points from circle_coords.json (old working service)
# Hand point coordinates (for STATIC/DASH arrows) - inner grid positions where props are placed
```

### **Task 1.2: Clean V1 References**

**Action Plan:**
```python
# BEFORE (V1 cruft):
def create_sections(self) -> None:
    """V1-style: Create sections with single-row layout for sections 4,5,6"""
    # V1-style: Create transparent horizontal container for sections 4, 5, 6
    # V1 approach: no finalization needed, QVBoxLayout just works!
    
# AFTER (Clean V2):
def create_sections(self) -> None:
    """Create responsive section layout for option picker components."""
    # Implementation with modern responsive design patterns
```

**Files to Clean:**
1. `arrow_management_service.py` - Remove V1 positioning comments
2. `motion_management_service.py` - Remove V1 algorithm references  
3. `sequence_management_service.py` - Clean up V1 compatibility paths
4. All services in `positioning/`, `motion/`, `core/` directories

**Validation:**
```bash
# After cleanup, this should return zero results:
grep -r "V1\|v1\|old\|legacy" src/application/services/ --include="*.py"
```

## **Day 3-4: DI Container Enhancement**

### **Task 1.3: Complete Auto-Injection Implementation**

**Current Gap Analysis:**
```python
# CURRENT: Basic constructor injection
def _create_instance(self, implementation_class: Type) -> Any:
    # ❌ Skips complex dependencies
    # ❌ No validation of dependency chain
    # ❌ Limited error reporting
```

**Implementation Required:**
```python
# FILE: src/core/dependency_injection/di_container.py

def _create_instance(self, implementation_class: Type) -> Any:
    """Create instance with comprehensive automatic constructor injection."""
    try:
        signature = inspect.signature(implementation_class.__init__)
        type_hints = get_type_hints(implementation_class.__init__)
        dependencies = {}
        
        for param_name, param in signature.parameters.items():
            if param_name == "self":
                continue
                
            param_type = type_hints.get(param_name, param.annotation)
            
            # Enhanced dependency resolution
            if param.default != inspect.Parameter.empty:
                # Has default value - use it and skip dependency resolution
                dependencies[param_name] = param.default
                continue
                
            # Skip if no type annotation
            if not param_type or param_type == inspect.Parameter.empty:
                continue
                
            # Skip primitive types
            if self._is_primitive_type(param_type):
                continue
                
            # Enhanced error handling for dependency resolution
            try:
                dependencies[param_name] = self.resolve(param_type)
            except ValueError as e:
                raise ValueError(
                    f"Cannot resolve dependency {param_type.__name__} for parameter "
                    f"'{param_name}' in {implementation_class.__name__}. "
                    f"Original error: {e}. "
                    f"Available registrations: {list(self._services.keys())}"
                )
        
        return implementation_class(**dependencies)
        
    except Exception as e:
        logger.error(f"Failed to create instance of {implementation_class.__name__}: {e}")
        logger.error(f"Available services: {list(self._services.keys())}")
        logger.error(f"Available factories: {list(self._factories.keys())}")
        raise RuntimeError(f"Dependency injection failed for {implementation_class.__name__}: {e}")

def auto_register_with_validation(self, interface: Type[T], implementation: Type[T]) -> None:
    """Register service with comprehensive validation."""
    # Step 1: Validate Protocol implementation
    self._validate_protocol_implementation(interface, implementation)
    
    # Step 2: Validate dependency chain can be resolved
    self._validate_dependency_chain(implementation)
    
    # Step 3: Register if validation passes
    self.register_singleton(interface, implementation)
    
    logger.info(f"✅ Successfully registered {interface.__name__} -> {implementation.__name__}")

def _validate_dependency_chain(self, implementation: Type) -> None:
    """Validate that all constructor dependencies can be resolved."""
    signature = inspect.signature(implementation.__init__)
    type_hints = get_type_hints(implementation.__init__)
    
    for param_name, param in signature.parameters.items():
        if param_name == "self":
            continue
            
        # Skip if has default value
        if param.default != inspect.Parameter.empty:
            continue
            
        param_type = type_hints.get(param_name, param.annotation)
        
        # Skip primitives
        if self._is_primitive_type(param_type):
            continue
            
        # Check if dependency is registered
        if param_type not in self._services and param_type not in self._factories:
            raise ValueError(
                f"Dependency {param_type.__name__} for {implementation.__name__} "
                f"is not registered. Register it first or make parameter optional."
            )

def validate_all_registrations(self) -> None:
    """Validate that all registered services can be instantiated."""
    errors = []
    
    for interface, implementation in self._services.items():
        try:
            self.resolve(interface)
            logger.info(f"✅ {interface.__name__} -> {implementation.__name__}")
        except Exception as e:
            errors.append(f"❌ {interface.__name__}: {e}")
    
    if errors:
        logger.error("Registration validation failed:")
        for error in errors:
            logger.error(f"  {error}")
        raise ValueError(f"Service registration validation failed: {len(errors)} errors")
    
    logger.info(f"✅ All {len(self._services)} service registrations validated successfully")
```

### **Task 1.4: Enhanced Error Reporting**

**Add Diagnostic Methods:**
```python
# FILE: src/core/dependency_injection/di_container.py

def get_dependency_graph(self) -> Dict[str, List[str]]:
    """Generate dependency graph for debugging."""
    graph = {}
    
    for interface, implementation in self._services.items():
        deps = self._get_constructor_dependencies(implementation)
        graph[f"{interface.__name__} -> {implementation.__name__}"] = [
            dep.__name__ for dep in deps if not self._is_primitive_type(dep)
        ]
    
    return graph

def diagnose_resolution_failure(self, interface: Type) -> str:
    """Provide detailed diagnosis for resolution failures."""
    diagnosis = [f"Diagnosing resolution failure for {interface.__name__}:"]
    
    # Check if registered
    if interface not in self._services and interface not in self._factories:
        diagnosis.append(f"❌ {interface.__name__} is not registered")
        diagnosis.append("Available interfaces:")
        for registered in self._services.keys():
            diagnosis.append(f"  - {registered.__name__}")
        return "\n".join(diagnosis)
    
    # Check dependency chain
    implementation = self._services.get(interface) or self._factories.get(interface)
    if implementation:
        deps = self._get_constructor_dependencies(implementation)
        diagnosis.append(f"Dependencies for {implementation.__name__}:")
        
        for dep in deps:
            if self._is_primitive_type(dep):
                diagnosis.append(f"  ✅ {dep.__name__} (primitive)")
            elif dep in self._services or dep in self._factories:
                diagnosis.append(f"  ✅ {dep.__name__} (registered)")
            else:
                diagnosis.append(f"  ❌ {dep.__name__} (NOT REGISTERED)")
    
    return "\n".join(diagnosis)
```

## **Day 5: Validation and Testing**

### **Task 1.5: Comprehensive DI Testing**

**Create Test Suite:**
```python
# FILE: tests/specification/core/test_enhanced_di_container.py

"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce enhanced DI container behavioral contracts
PERMANENT: Core infrastructure must be bulletproof
AUTHOR: @developer
"""

import pytest
from typing import Protocol, runtime_checkable
from src.core.dependency_injection.di_container import DIContainer

class TestEnhancedDIContainer:
    
    def test_auto_injection_with_complex_dependencies(self):
        """Test automatic injection of multi-level dependencies."""
        container = DIContainer()
        
        @runtime_checkable
        class IRepository(Protocol):
            def save(self, data: str) -> None: ...
        
        @runtime_checkable  
        class IService(Protocol):
            def process(self, input: str) -> str: ...
        
        class Repository:
            def save(self, data: str) -> None:
                pass
        
        class Service:
            def __init__(self, repo: IRepository):
                self.repo = repo
                
            def process(self, input: str) -> str:
                return f"processed: {input}"
        
        class Controller:
            def __init__(self, service: IService, config: str = "default"):
                self.service = service
                self.config = config
        
        # Register services
        container.auto_register_with_validation(IRepository, Repository)
        container.auto_register_with_validation(IService, Service)
        
        # Test complex dependency resolution
        controller = container._create_instance(Controller)
        assert isinstance(controller.service, Service)
        assert controller.config == "default"
    
    def test_dependency_chain_validation(self):
        """Test validation of complete dependency chains."""
        container = DIContainer()
        
        class MissingDependency:
            pass
        
        class ServiceWithMissingDep:
            def __init__(self, missing: MissingDependency):
                self.missing = missing
        
        # Should raise error for missing dependency
        with pytest.raises(ValueError, match="is not registered"):
            container._validate_dependency_chain(ServiceWithMissingDep)
    
    def test_enhanced_error_reporting(self):
        """Test detailed error messages for resolution failures."""
        container = DIContainer()
        
        diagnosis = container.diagnose_resolution_failure(str)  # Unregistered type
        assert "is not registered" in diagnosis
        assert "Available interfaces:" in diagnosis
    
    def test_registration_validation(self):
        """Test comprehensive validation of all registrations."""
        container = DIContainer()
        
        class ValidService:
            pass
        
        container.register_singleton(str, ValidService)  # Valid registration
        
        # Should validate successfully
        container.validate_all_registrations()
```

### **Task 1.6: Integration with Existing Services**

**Update Service Registration:**
```python
# FILE: v2/main.py

def _configure_services(self):
    """Configure services with enhanced DI validation."""
    if self.splash:
        self.splash.update_progress(20, "Configuring services...")
    
    # Use enhanced registration with validation
    try:
        self.container.auto_register_with_validation(
            ILayoutManagementService, 
            LayoutManagementService
        )
        
        self.container.auto_register_with_validation(
            IUIStateManagementService, 
            UIStateManagementService
        )
        
        # Register all services with validation
        self._register_motion_services()
        self._register_layout_services()
        self._register_pictograph_services()
        
        # Validate all registrations at startup
        self.container.validate_all_registrations()
        
        if self.splash:
            self.splash.update_progress(40, "✅ All services validated")
            
    except Exception as e:
        logger.error(f"Service configuration failed: {e}")
        logger.error(self.container.diagnose_resolution_failure(ILayoutManagementService))
        raise
```

---

# ⚡ **PHASE 2: ADVANCED ARCHITECTURE PATTERNS**

**Timeline**: 2 Weeks  
**Priority**: HIGH  
**Goal**: Implement event-driven architecture and advanced patterns

## **Week 1: Event-Driven Architecture**

### **Task 2.1: Type-Safe Event Bus Implementation**

**Create Event Infrastructure:**
```python
# FILE: src/core/events/event_bus.py

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

### **Task 2.2: Domain Events Definition**

**Create Event Types:**
```python
# FILE: src/core/events/domain_events.py

"""
Domain events for TKA application.
These events represent significant business state changes.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid

from src.core.events.event_bus import BaseEvent
from src.domain.models.core_models import BeatData, SequenceData, MotionData
from src.domain.models.pictograph_models import PictographData

# === Sequence Events ===

@dataclass(frozen=True)
class SequenceCreatedEvent(BaseEvent):
    """Published when a new sequence is created."""
    sequence: SequenceData

@dataclass(frozen=True)
class SequenceUpdatedEvent(BaseEvent):
    """Published when sequence data changes."""
    sequence: SequenceData
    previous_sequence: Optional[SequenceData] = None
    change_type: str = "general"  # "beat_added", "beat_removed", "beat_updated", etc.

@dataclass(frozen=True)
class SequenceDeletedEvent(BaseEvent):
    """Published when a sequence is deleted."""
    sequence_id: str
    sequence_name: str

# === Beat Events ===

@dataclass(frozen=True)
class BeatSelectedEvent(BaseEvent):
    """Published when a beat is selected in the UI."""
    beat: BeatData
    beat_index: int
    sequence_id: str

@dataclass(frozen=True)
class BeatUpdatedEvent(BaseEvent):
    """Published when beat data changes."""
    beat: BeatData
    beat_index: int
    sequence_id: str
    field_changed: str  # "letter", "duration", "blue_motion", etc.
    previous_value: Optional[Any] = None

@dataclass(frozen=True)
class BeatCreatedEvent(BaseEvent):
    """Published when a new beat is added."""
    beat: BeatData
    beat_index: int
    sequence_id: str

# === Motion Events ===

@dataclass(frozen=True)
class MotionGeneratedEvent(BaseEvent):
    """Published when new motion is generated."""
    motion: MotionData
    beat_index: int
    color: str  # "blue" or "red"
    sequence_id: str
    generation_method: str  # "manual", "random", "smart_fill", etc.

@dataclass(frozen=True)
class MotionValidationEvent(BaseEvent):
    """Published when motion validation occurs."""
    motion: MotionData
    is_valid: bool
    validation_errors: List[str] = field(default_factory=list)

# === Pictograph Events ===

@dataclass(frozen=True)
class PictographUpdatedEvent(BaseEvent):
    """Published when pictograph visualization changes."""
    pictograph: PictographData
    beat_index: int
    sequence_id: str
    update_type: str  # "position", "visibility", "styling", etc.

@dataclass(frozen=True)
class PictographGeneratedEvent(BaseEvent):
    """Published when pictograph is generated from motion data."""
    pictograph: PictographData
    beat_index: int
    sequence_id: str
    generation_time_ms: float

# === UI State Events ===

@dataclass(frozen=True)
class UIStateChangedEvent(BaseEvent):
    """Published when UI state changes."""
    state_key: str
    new_value: Any
    previous_value: Optional[Any] = None

@dataclass(frozen=True)
class ComponentResizedEvent(BaseEvent):
    """Published when layout components are resized."""
    component_name: str
    new_size: Tuple[int, int]
    previous_size: Optional[Tuple[int, int]] = None

# === Application Events ===

@dataclass(frozen=True)
class ApplicationStartedEvent(BaseEvent):
    """Published when application completes initialization."""
    version: str
    startup_time_ms: float

@dataclass(frozen=True)
class ErrorOccurredEvent(BaseEvent):
    """Published when recoverable errors occur."""
    error_type: str
    error_message: str
    component: str
    stack_trace: Optional[str] = None
```

### **Task 2.3: Event-Driven Service Integration**

**Update Services to Use Events:**
```python
# FILE: src/application/services/core/sequence_management_service.py

class SequenceManagementService:
    """Enhanced with event publishing."""
    
    def __init__(self, event_bus: IEventBus):
        self.event_bus = event_bus
        self._current_sequence: Optional[SequenceData] = None
    
    def create_sequence(self, name: str = "New Sequence") -> SequenceData:
        """Create sequence and publish event."""
        sequence = SequenceData(name=name)
        self._current_sequence = sequence
        
        # Publish event instead of directly calling other components
        self.event_bus.publish(SequenceCreatedEvent(
            timestamp=time.time(),
            source_component="SequenceManagementService",
            sequence=sequence
        ))
        
        return sequence
    
    def update_sequence(self, sequence: SequenceData, change_type: str = "general") -> SequenceData:
        """Update sequence and publish event."""
        previous = self._current_sequence
        self._current_sequence = sequence
        
        self.event_bus.publish(SequenceUpdatedEvent(
            timestamp=time.time(),
            source_component="SequenceManagementService",
            sequence=sequence,
            previous_sequence=previous,
            change_type=change_type
        ))
        
        return sequence
    
    def add_beat(self, beat: BeatData) -> SequenceData:
        """Add beat and publish specific event."""
        if not self._current_sequence:
            raise ValueError("No active sequence")
        
        updated_sequence = self._current_sequence.add_beat(beat)
        self._current_sequence = updated_sequence
        
        # Publish both general update and specific beat event
        self.event_bus.publish(BeatCreatedEvent(
            timestamp=time.time(),
            source_component="SequenceManagementService",
            beat=beat,
            beat_index=len(updated_sequence.beats) - 1,
            sequence_id=updated_sequence.id
        ))
        
        self.event_bus.publish(SequenceUpdatedEvent(
            timestamp=time.time(),
            source_component="SequenceManagementService",
            sequence=updated_sequence,
            change_type="beat_added"
        ))
        
        return updated_sequence
```

### **Task 2.4: Component Event Subscriptions**

**Update Components to Subscribe to Events:**
```python
# FILE: src/presentation/components/workbench/graph_editor.py

class GraphEditor(QWidget):
    """Graph editor that responds to events instead of direct calls."""
    
    def __init__(self, container: DIContainer):
        super().__init__()
        self.container = container
        self.event_bus = container.resolve(IEventBus)
        self._subscription_ids: List[str] = []
        
        self._setup_event_subscriptions()
    
    def _setup_event_subscriptions(self):
        """Subscribe to relevant events."""
        
        # Subscribe to sequence events
        sub_id = self.event_bus.subscribe(
            SequenceUpdatedEvent,
            self._on_sequence_updated
        )
        self._subscription_ids.append(sub_id)
        
        # Subscribe to beat selection events
        sub_id = self.event_bus.subscribe(
            BeatSelectedEvent,
            self._on_beat_selected
        )
        self._subscription_ids.append(sub_id)
        
        # Subscribe to pictograph events
        sub_id = self.event_bus.subscribe(
            PictographUpdatedEvent,
            self._on_pictograph_updated
        )
        self._subscription_ids.append(sub_id)
    
    def _on_sequence_updated(self, event: SequenceUpdatedEvent):
        """Handle sequence updates."""
        logger.debug(f"Graph editor updating for sequence: {event.sequence.name}")
        
        # Update display based on sequence
        self._update_sequence_display(event.sequence)
        
        # If this was a beat addition, highlight the new beat
        if event.change_type == "beat_added":
            self._highlight_latest_beat()
    
    def _on_beat_selected(self, event: BeatSelectedEvent):
        """Handle beat selection."""
        logger.debug(f"Graph editor highlighting beat {event.beat_index}")
        self._highlight_beat(event.beat_index)
    
    def _on_pictograph_updated(self, event: PictographUpdatedEvent):
        """Handle pictograph updates."""
        logger.debug(f"Graph editor updating pictograph for beat {event.beat_index}")
        self._update_pictograph_display(event.pictograph, event.beat_index)
    
    def cleanup(self):
        """Unsubscribe from events when component is destroyed."""
        for sub_id in self._subscription_ids:
            self.event_bus.unsubscribe(sub_id)
        self._subscription_ids.clear()
```

## **Week 2: Command Pattern & Advanced Patterns**

### **Task 2.5: Command Pattern for Undo/Redo**

**Implement Command Infrastructure:**
```python
# FILE: src/core/commands/command_system.py

"""
Command pattern implementation for undo/redo functionality.
Provides type-safe, undoable operations.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any
from dataclasses import dataclass
import logging

T = TypeVar("T")

class ICommand(Generic[T], ABC):
    """Interface for undoable commands."""
    
    @abstractmethod
    def execute(self) -> T:
        """Execute the command and return result."""
        pass
    
    @abstractmethod
    def undo(self) -> T:
        """Undo the command and return previous state."""
        pass
    
    @abstractmethod
    def can_execute(self) -> bool:
        """Check if command can be executed."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get human-readable description of the command."""
        pass

@dataclass(frozen=True)
class AddBeatCommand(ICommand[SequenceData]):
    """Command to add a beat to a sequence."""
    sequence: SequenceData
    beat: BeatData
    position: int
    
    def execute(self) -> SequenceData:
        if not self.can_execute():
            raise ValueError("Cannot add beat at invalid position")
        return self.sequence.add_beat_at_position(self.beat, self.position)
    
    def undo(self) -> SequenceData:
        return self.sequence.remove_beat_at_position(self.position)
    
    def can_execute(self) -> bool:
        return 0 <= self.position <= len(self.sequence.beats)
    
    def get_description(self) -> str:
        return f"Add beat '{self.beat.letter}' at position {self.position + 1}"

@dataclass(frozen=True)
class UpdateBeatCommand(ICommand[SequenceData]):
    """Command to update a beat in a sequence."""
    sequence: SequenceData
    beat_index: int
    field_updates: Dict[str, Any]
    previous_values: Dict[str, Any]
    
    def execute(self) -> SequenceData:
        if not self.can_execute():
            raise ValueError("Cannot update beat at invalid index")
        return self.sequence.update_beat(self.beat_index, **self.field_updates)
    
    def undo(self) -> SequenceData:
        return self.sequence.update_beat(self.beat_index, **self.previous_values)
    
    def can_execute(self) -> bool:
        return 0 <= self.beat_index < len(self.sequence.beats)
    
    def get_description(self) -> str:
        changes = ", ".join(f"{k}={v}" for k, v in self.field_updates.items())
        return f"Update beat {self.beat_index + 1}: {changes}"

class CommandProcessor:
    """Processes commands with undo/redo support."""
    
    def __init__(self, event_bus: IEventBus, max_history: int = 100):
        self.event_bus = event_bus
        self.max_history = max_history
        self._history: List[ICommand] = []
        self._current_index = -1
        self._logger = logging.getLogger(__name__)
    
    def execute(self, command: ICommand[T]) -> T:
        """Execute command and add to history."""
        if not command.can_execute():
            raise ValueError(f"Command cannot be executed: {command.get_description()}")
        
        try:
            result = command.execute()
            
            # Clear redo history if we're not at the end
            self._history = self._history[:self._current_index + 1]
            
            # Add command to history
            self._history.append(command)
            self._current_index += 1
            
            # Limit history size
            if len(self._history) > self.max_history:
                self._history = self._history[-self.max_history:]
                self._current_index = len(self._history) - 1
            
            self._logger.debug(f"Executed: {command.get_description()}")
            
            # Publish command executed event
            self.event_bus.publish(CommandExecutedEvent(
                timestamp=time.time(),
                source_component="CommandProcessor",
                command_description=command.get_description(),
                can_undo=self.can_undo(),
                can_redo=self.can_redo()
            ))
            
            return result
            
        except Exception as e:
            self._logger.error(f"Command execution failed: {command.get_description()}: {e}")
            raise
    
    def undo(self) -> Optional[Any]:
        """Undo the last command."""
        if not self.can_undo():
            return None
        
        command = self._history[self._current_index]
        try:
            result = command.undo()
            self._current_index -= 1
            
            self._logger.debug(f"Undid: {command.get_description()}")
            
            # Publish undo event
            self.event_bus.publish(CommandUndoneEvent(
                timestamp=time.time(),
                source_component="CommandProcessor",
                command_description=command.get_description(),
                can_undo=self.can_undo(),
                can_redo=self.can_redo()
            ))
            
            return result
            
        except Exception as e:
            self._logger.error(f"Command undo failed: {command.get_description()}: {e}")
            raise
    
    def redo(self) -> Optional[Any]:
        """Redo the next command."""
        if not self.can_redo():
            return None
        
        self._current_index += 1
        command = self._history[self._current_index]
        
        try:
            result = command.execute()
            
            self._logger.debug(f"Redid: {command.get_description()}")
            
            # Publish redo event
            self.event_bus.publish(CommandRedoneEvent(
                timestamp=time.time(),
                source_component="CommandProcessor",
                command_description=command.get_description(),
                can_undo=self.can_undo(),
                can_redo=self.can_redo()
            ))
            
            return result
            
        except Exception as e:
            self._logger.error(f"Command redo failed: {command.get_description()}: {e}")
            self._current_index -= 1  # Revert index on failure
            raise
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self._current_index >= 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self._current_index < len(self._history) - 1
    
    def get_undo_description(self) -> Optional[str]:
        """Get description of command that would be undone."""
        if self.can_undo():
            return self._history[self._current_index].get_description()
        return None
    
    def get_redo_description(self) -> Optional[str]:
        """Get description of command that would be redone."""
        if self.can_redo():
            return self._history[self._current_index + 1].get_description()
        return None
    
    def clear_history(self):
        """Clear command history."""
        self._history.clear()
        self._current_index = -1

# Command Events
@dataclass(frozen=True)
class CommandExecutedEvent(BaseEvent):
    """Published when a command is executed."""
    command_description: str
    can_undo: bool
    can_redo: bool

@dataclass(frozen=True)
class CommandUndoneEvent(BaseEvent):
    """Published when a command is undone."""
    command_description: str
    can_undo: bool
    can_redo: bool

@dataclass(frozen=True)
class CommandRedoneEvent(BaseEvent):
    """Published when a command is redone."""
    command_description: str
    can_undo: bool
    can_redo: bool
```

### **Task 2.6: Service Integration with Commands**

**Update Services to Use Commands:**
```python
# FILE: src/application/services/core/sequence_management_service.py

class SequenceManagementService:
    """Enhanced with command pattern integration."""
    
    def __init__(self, event_bus: IEventBus, command_processor: CommandProcessor):
        self.event_bus = event_bus
        self.command_processor = command_processor
        self._current_sequence: Optional[SequenceData] = None
    
    def add_beat_with_undo(self, beat: BeatData, position: Optional[int] = None) -> SequenceData:
        """Add beat using command pattern for undo support."""
        if not self._current_sequence:
            raise ValueError("No active sequence")
        
        if position is None:
            position = len(self._current_sequence.beats)
        
        command = AddBeatCommand(
            sequence=self._current_sequence,
            beat=beat,
            position=position
        )
        
        # Execute through command processor for undo support
        result = self.command_processor.execute(command)
        self._current_sequence = result
        
        return result
    
    def update_beat_with_undo(self, beat_index: int, **updates) -> SequenceData:
        """Update beat using command pattern."""
        if not self._current_sequence:
            raise ValueError("No active sequence")
        
        current_beat = self._current_sequence.get_beat(beat_index + 1)  # beat_number is 1-indexed
        if not current_beat:
            raise ValueError(f"No beat at index {beat_index}")
        
        # Capture previous values for undo
        previous_values = {}
        for field, new_value in updates.items():
            previous_values[field] = getattr(current_beat, field)
        
        command = UpdateBeatCommand(
            sequence=self._current_sequence,
            beat_index=beat_index,
            field_updates=updates,
            previous_values=previous_values
        )
        
        result = self.command_processor.execute(command)
        self._current_sequence = result
        
        return result
    
    def undo_last_action(self) -> Optional[SequenceData]:
        """Undo the last action."""
        result = self.command_processor.undo()
        if result and isinstance(result, SequenceData):
            self._current_sequence = result
            return result
        return None
    
    def redo_last_action(self) -> Optional[SequenceData]:
        """Redo the last undone action."""
        result = self.command_processor.redo()
        if result and isinstance(result, SequenceData):
            self._current_sequence = result
            return result
        return None
```

---

# 🚀 **PHASE 3: ENTERPRISE-GRADE FEATURES**

**Timeline**: 2 Weeks  
**Priority**: MEDIUM  
**Goal**: Add cross-language compatibility and advanced monitoring

## **Week 1: Cross-Language API Layer**

### **Task 3.1: REST API Layer**

**Create API Infrastructure:**
```python
# FILE: src/infrastructure/api/rest_api.py

"""
REST API layer for cross-language access to TKA functionality.
Enables TypeScript, Rust, C++, or other language clients.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime

from src.core.dependency_injection.di_container import get_container
from src.domain.models.core_models import SequenceData, BeatData, MotionData
from src.application.services.core.sequence_management_service import SequenceManagementService

# API Models (Pydantic for validation and OpenAPI generation)
class MotionAPI(BaseModel):
    """API model for motion data."""
    motion_type: str
    prop_rot_dir: str
    start_loc: str
    end_loc: str
    turns: float = 0.0
    start_ori: str = "in"
    end_ori: str = "in"
    
    class Config:
        schema_extra = {
            "example": {
                "motion_type": "pro",
                "prop_rot_dir": "cw",
                "start_loc": "n",
                "end_loc": "e",
                "turns": 1.0,
                "start_ori": "in",
                "end_ori": "out"
            }
        }

class BeatAPI(BaseModel):
    """API model for beat data."""
    id: str
    beat_number: int
    letter: Optional[str] = None
    duration: float = 1.0
    blue_motion: Optional[MotionAPI] = None
    red_motion: Optional[MotionAPI] = None
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SequenceAPI(BaseModel):
    """API model for sequence data."""
    id: str
    name: str = ""
    word: str = ""
    beats: List[BeatAPI] = Field(default_factory=list)
    start_position: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "id": "seq_123",
                "name": "Example Sequence",
                "word": "HELLO",
                "beats": [],
                "start_position": "n",
                "metadata": {}
            }
        }

class CreateSequenceRequest(BaseModel):
    """Request model for creating sequences."""
    name: str = "New Sequence"
    beats: Optional[List[BeatAPI]] = None

class UpdateSequenceRequest(BaseModel):
    """Request model for updating sequences."""
    name: Optional[str] = None
    beats: Optional[List[BeatAPI]] = None
    metadata: Optional[Dict[str, Any]] = None

# FastAPI Application
app = FastAPI(
    title="TKA Desktop API",
    description="Cross-language API for Kinetic Alphabet Desktop",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
def get_sequence_service() -> SequenceManagementService:
    """Get sequence service from DI container."""
    container = get_container()
    return container.resolve(SequenceManagementService)

# Conversion utilities
def domain_to_api_motion(motion: MotionData) -> MotionAPI:
    """Convert domain motion to API model."""
    return MotionAPI(
        motion_type=motion.motion_type.value,
        prop_rot_dir=motion.prop_rot_dir.value,
        start_loc=motion.start_loc.value,
        end_loc=motion.end_loc.value,
        turns=motion.turns,
        start_ori=motion.start_ori,
        end_ori=motion.end_ori
    )

def api_to_domain_motion(motion: MotionAPI) -> MotionData:
    """Convert API motion to domain model."""
    return MotionData.from_dict(motion.dict())

def domain_to_api_beat(beat: BeatData) -> BeatAPI:
    """Convert domain beat to API model."""
    return BeatAPI(
        id=beat.id,
        beat_number=beat.beat_number,
        letter=beat.letter,
        duration=beat.duration,
        blue_motion=domain_to_api_motion(beat.blue_motion) if beat.blue_motion else None,
        red_motion=domain_to_api_motion(beat.red_motion) if beat.red_motion else None,
        blue_reversal=beat.blue_reversal,
        red_reversal=beat.red_reversal,
        is_blank=beat.is_blank,
        metadata=beat.metadata
    )

def domain_to_api_sequence(sequence: SequenceData) -> SequenceAPI:
    """Convert domain sequence to API model."""
    return SequenceAPI(
        id=sequence.id,
        name=sequence.name,
        word=sequence.word,
        beats=[domain_to_api_beat(beat) for beat in sequence.beats],
        start_position=sequence.start_position,
        metadata=sequence.metadata
    )

# API Endpoints
@app.get("/api/sequences/", response_model=List[SequenceAPI])
async def list_sequences(service: SequenceManagementService = Depends(get_sequence_service)):
    """List all sequences."""
    try:
        sequences = service.get_all_sequences()
        return [domain_to_api_sequence(seq) for seq in sequences]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sequences/", response_model=SequenceAPI)
async def create_sequence(
    request: CreateSequenceRequest,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Create a new sequence."""
    try:
        sequence = service.create_sequence(name=request.name)
        
        # Add beats if provided
        if request.beats:
            for beat_api in request.beats:
                beat_data = BeatData.from_dict(beat_api.dict())
                sequence = service.add_beat_with_undo(beat_data)
        
        return domain_to_api_sequence(sequence)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/sequences/{sequence_id}", response_model=SequenceAPI)
async def get_sequence(
    sequence_id: str,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Get a specific sequence."""
    try:
        sequence = service.get_sequence(sequence_id)
        if not sequence:
            raise HTTPException(status_code=404, detail="Sequence not found")
        return domain_to_api_sequence(sequence)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/sequences/{sequence_id}", response_model=SequenceAPI)
async def update_sequence(
    sequence_id: str,
    request: UpdateSequenceRequest,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Update a sequence."""
    try:
        sequence = service.get_sequence(sequence_id)
        if not sequence:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        updates = {}
        if request.name is not None:
            updates["name"] = request.name
        if request.metadata is not None:
            updates["metadata"] = request.metadata
        
        if updates:
            sequence = service.update_sequence(sequence.update(**updates))
        
        return domain_to_api_sequence(sequence)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/sequences/{sequence_id}")
async def delete_sequence(
    sequence_id: str,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Delete a sequence."""
    try:
        success = service.delete_sequence(sequence_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sequence not found")
        return {"message": "Sequence deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sequences/{sequence_id}/beats/", response_model=SequenceAPI)
async def add_beat(
    sequence_id: str,
    beat: BeatAPI,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Add a beat to a sequence."""
    try:
        beat_data = BeatData.from_dict(beat.dict())
        sequence = service.add_beat_with_undo(beat_data)
        return domain_to_api_sequence(sequence)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0"
    }

# API Server
class TKAAPIServer:
    """API server for TKA Desktop."""
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self.server = None
    
    def start(self):
        """Start the API server."""
        uvicorn.run(app, host=self.host, port=self.port, log_level="info")
    
    async def start_async(self):
        """Start the API server asynchronously."""
        config = uvicorn.Config(app, host=self.host, port=self.port, log_level="info")
        self.server = uvicorn.Server(config)
        await self.server.serve()
    
    def stop(self):
        """Stop the API server."""
        if self.server:
            self.server.should_exit = True
```

### **Task 3.2: Schema-First Development**

**Generate Language Bindings:**
```python
# FILE: src/infrastructure/codegen/schema_generator.py

"""
Schema-first development with automatic code generation.
Generates TypeScript, Rust, C++, and other language bindings.
"""

import json
from typing import Dict, Any, List
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class SchemaGenerator:
    """Generates schemas and language bindings."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja2 for templates
        template_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate_json_schema(self) -> Dict[str, Any]:
        """Generate JSON Schema for all API models."""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "TKA Desktop API Schema",
            "version": "2.0.0",
            "definitions": {
                "MotionData": {
                    "type": "object",
                    "required": ["motion_type", "prop_rot_dir", "start_loc", "end_loc"],
                    "properties": {
                        "motion_type": {
                            "type": "string",
                            "enum": ["pro", "anti", "float", "dash", "static"]
                        },
                        "prop_rot_dir": {
                            "type": "string", 
                            "enum": ["cw", "ccw", "no_rot"]
                        },
                        "start_loc": {
                            "type": "string",
                            "enum": ["n", "e", "s", "w", "ne", "se", "sw", "nw"]
                        },
                        "end_loc": {
                            "type": "string",
                            "enum": ["n", "e", "s", "w", "ne", "se", "sw", "nw"]
                        },
                        "turns": {"type": "number", "default": 0.0},
                        "start_ori": {"type": "string", "default": "in"},
                        "end_ori": {"type": "string", "default": "in"}
                    }
                },
                "BeatData": {
                    "type": "object",
                    "required": ["id", "beat_number"],
                    "properties": {
                        "id": {"type": "string"},
                        "beat_number": {"type": "integer", "minimum": 1},
                        "letter": {"type": "string", "nullable": True},
                        "duration": {"type": "number", "default": 1.0, "minimum": 0.1},
                        "blue_motion": {"$ref": "#/definitions/MotionData", "nullable": True},
                        "red_motion": {"$ref": "#/definitions/MotionData", "nullable": True},
                        "blue_reversal": {"type": "boolean", "default": False},
                        "red_reversal": {"type": "boolean", "default": False},
                        "is_blank": {"type": "boolean", "default": False},
                        "metadata": {"type": "object", "default": {}}
                    }
                },
                "SequenceData": {
                    "type": "object", 
                    "required": ["id"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string", "default": ""},
                        "word": {"type": "string", "default": ""},
                        "beats": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/BeatData"},
                            "default": []
                        },
                        "start_position": {"type": "string", "nullable": True},
                        "metadata": {"type": "object", "default": {}}
                    }
                }
            }
        }
        
        # Write schema file
        schema_file = self.output_dir / "tka_schema.json"
        with open(schema_file, 'w') as f:
            json.dump(schema, f, indent=2)
        
        return schema
    
    def generate_typescript_bindings(self, schema: Dict[str, Any]) -> None:
        """Generate TypeScript interfaces."""
        template = self.jinja_env.get_template("typescript.j2")
        
        ts_content = template.render(
            schema=schema,
            definitions=schema["definitions"]
        )
        
        ts_file = self.output_dir / "tka_types.ts"
        with open(ts_file, 'w') as f:
            f.write(ts_content)
    
    def generate_rust_bindings(self, schema: Dict[str, Any]) -> None:
        """Generate Rust structs."""
        template = self.jinja_env.get_template("rust.j2")
        
        rust_content = template.render(
            schema=schema,
            definitions=schema["definitions"]
        )
        
        rust_file = self.output_dir / "tka_types.rs"
        with open(rust_file, 'w') as f:
            f.write(rust_content)
    
    def generate_cpp_bindings(self, schema: Dict[str, Any]) -> None:
        """Generate C++ classes."""
        header_template = self.jinja_env.get_template("cpp_header.j2")
        impl_template = self.jinja_env.get_template("cpp_impl.j2")
        
        header_content = header_template.render(
            schema=schema,
            definitions=schema["definitions"]
        )
        
        impl_content = impl_template.render(
            schema=schema,
            definitions=schema["definitions"]
        )
        
        header_file = self.output_dir / "tka_types.h"
        impl_file = self.output_dir / "tka_types.cpp"
        
        with open(header_file, 'w') as f:
            f.write(header_content)
        
        with open(impl_file, 'w') as f:
            f.write(impl_content)
    
    def generate_all(self) -> None:
        """Generate all language bindings."""
        print("🔄 Generating TKA API schemas and bindings...")
        
        # Generate JSON schema
        schema = self.generate_json_schema()
        print("✅ JSON Schema generated")
        
        # Generate language bindings
        self.generate_typescript_bindings(schema)
        print("✅ TypeScript bindings generated")
        
        self.generate_rust_bindings(schema)
        print("✅ Rust bindings generated")
        
        self.generate_cpp_bindings(schema)
        print("✅ C++ bindings generated")
        
        print(f"🎉 All bindings generated in: {self.output_dir}")

# CLI for code generation
def main():
    """CLI entry point for schema generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate TKA API schemas and language bindings")
    parser.add_argument("--output", "-o", default="./generated", help="Output directory")
    parser.add_argument("--language", "-l", choices=["all", "typescript", "rust", "cpp"], 
                       default="all", help="Language to generate")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    generator = SchemaGenerator(output_dir)
    
    if args.language == "all":
        generator.generate_all()
    else:
        schema = generator.generate_json_schema()
        
        if args.language == "typescript":
            generator.generate_typescript_bindings(schema)
        elif args.language == "rust":
            generator.generate_rust_bindings(schema)
        elif args.language == "cpp":
            generator.generate_cpp_bindings(schema)

if __name__ == "__main__":
    main()
```

## **Week 2: Performance Monitoring & Quality Gates**

### **Task 3.3: Performance Monitoring System**

**Create Performance Infrastructure:**
```python
# FILE: src/infrastructure/monitoring/performance_monitor.py

"""
Comprehensive performance monitoring for TKA Desktop.
Tracks metrics, detects regressions, and provides insights.
"""

import time
import psutil
import threading
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from pathlib import Path
import logging

@dataclass
class PerformanceMetric:
    """Individual performance measurement."""
    operation: str
    duration_ms: float
    memory_usage_mb: float
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceBaseline:
    """Performance baseline for regression detection."""
    operation: str
    avg_duration_ms: float
    max_duration_ms: float
    avg_memory_mb: float
    max_memory_mb: float
    sample_count: int
    last_updated: datetime

class PerformanceMonitor:
    """High-precision performance monitoring system."""
    
    def __init__(self, baseline_file: Optional[Path] = None):
        self.baseline_file = baseline_file or Path("performance_baselines.json")
        self.metrics: List[PerformanceMetric] = []
        self.baselines: Dict[str, PerformanceBaseline] = {}
        self._lock = threading.Lock()
        self._logger = logging.getLogger(__name__)
        
        self._load_baselines()
    
    def measure_operation(self, operation_name: str, context: Optional[Dict[str, Any]] = None):
        """Context manager for measuring operation performance."""
        return PerformanceContext(self, operation_name, context or {})
    
    def record_metric(self, metric: PerformanceMetric) -> None:
        """Record a performance metric."""
        with self._lock:
            self.metrics.append(metric)
            
            # Check for regression
            if metric.operation in self.baselines:
                baseline = self.baselines[metric.operation]
                if self._is_regression(metric, baseline):
                    self._logger.warning(
                        f"Performance regression detected for {metric.operation}: "
                        f"{metric.duration_ms:.2f}ms vs baseline {baseline.avg_duration_ms:.2f}ms"
                    )
    
    def update_baseline(self, operation: str, force: bool = False) -> None:
        """Update performance baseline for an operation."""
        operation_metrics = [m for m in self.metrics if m.operation == operation]
        
        if len(operation_metrics) < 5 and not force:
            return  # Need at least 5 samples for meaningful baseline
        
        durations = [m.duration_ms for m in operation_metrics]
        memory_usage = [m.memory_usage_mb for m in operation_metrics]
        
        baseline = PerformanceBaseline(
            operation=operation,
            avg_duration_ms=sum(durations) / len(durations),
            max_duration_ms=max(durations),
            avg_memory_mb=sum(memory_usage) / len(memory_usage),
            max_memory_mb=max(memory_usage),
            sample_count=len(operation_metrics),
            last_updated=datetime.now()
        )
        
        self.baselines[operation] = baseline
        self._save_baselines()
        
        self._logger.info(f"Updated baseline for {operation}: {baseline.avg_duration_ms:.2f}ms avg")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        operations = set(m.operation for m in self.metrics)
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_metrics": len(self.metrics),
            "operations": {}
        }
        
        for operation in operations:
            op_metrics = [m for m in self.metrics if m.operation == operation]
            durations = [m.duration_ms for m in op_metrics]
            memory_usage = [m.memory_usage_mb for m in op_metrics]
            
            baseline = self.baselines.get(operation)
            
            op_report = {
                "sample_count": len(op_metrics),
                "avg_duration_ms": sum(durations) / len(durations),
                "min_duration_ms": min(durations),
                "max_duration_ms": max(durations),
                "avg_memory_mb": sum(memory_usage) / len(memory_usage),
                "baseline": baseline.__dict__ if baseline else None,
                "regression_detected": False
            }
            
            if baseline:
                current_avg = op_report["avg_duration_ms"]
                regression_threshold = baseline.avg_duration_ms * 1.2  # 20% slower
                op_report["regression_detected"] = current_avg > regression_threshold
            
            report["operations"][operation] = op_report
        
        return report
    
    def _is_regression(self, metric: PerformanceMetric, baseline: PerformanceBaseline) -> bool:
        """Check if metric indicates performance regression."""
        # Consider it a regression if 20% slower than baseline
        return metric.duration_ms > baseline.avg_duration_ms * 1.2
    
    def _load_baselines(self) -> None:
        """Load performance baselines from file."""
        if not self.baseline_file.exists():
            return
        
        try:
            with open(self.baseline_file, 'r') as f:
                data = json.load(f)
                
            for op_name, baseline_dict in data.items():
                baseline_dict['last_updated'] = datetime.fromisoformat(baseline_dict['last_updated'])
                self.baselines[op_name] = PerformanceBaseline(**baseline_dict)
                
        except Exception as e:
            self._logger.warning(f"Could not load performance baselines: {e}")
    
    def _save_baselines(self) -> None:
        """Save performance baselines to file."""
        try:
            data = {}
            for op_name, baseline in self.baselines.items():
                baseline_dict = baseline.__dict__.copy()
                baseline_dict['last_updated'] = baseline.last_updated.isoformat()
                data[op_name] = baseline_dict
            
            with open(self.baseline_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            self._logger.error(f"Could not save performance baselines: {e}")

class PerformanceContext:
    """Context manager for measuring operation performance."""
    
    def __init__(self, monitor: PerformanceMonitor, operation: str, context: Dict[str, Any]):
        self.monitor = monitor
        self.operation = operation
        self.context = context
        self.start_time: Optional[float] = None
        self.start_memory: Optional[float] = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        process = psutil.Process()
        self.start_memory = process.memory_info().rss / 1024 / 1024  # MB
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is None or self.start_memory is None:
            return
        
        end_time = time.perf_counter()
        process = psutil.Process()
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        duration_ms = (end_time - self.start_time) * 1000
        memory_usage_mb = max(end_memory, self.start_memory)  # Peak memory
        
        metric = PerformanceMetric(
            operation=self.operation,
            duration_ms=duration_ms,
            memory_usage_mb=memory_usage_mb,
            timestamp=datetime.now(),
            context=self.context
        )
        
        self.monitor.record_metric(metric)

# Global performance monitor instance
_performance_monitor: Optional[PerformanceMonitor] = None

def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor

# Decorator for automatic performance monitoring
def monitor_performance(operation_name: Optional[str] = None):
    """Decorator to automatically monitor function performance."""
    def decorator(func: Callable) -> Callable:
        nonlocal operation_name
        if operation_name is None:
            operation_name = f"{func.__module__}.{func.__qualname__}"
        
        def wrapper(*args, **kwargs):
            monitor = get_performance_monitor()
            with monitor.measure_operation(operation_name):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

### **Task 3.4: Quality Gates and CI Integration**

**Create Quality Gate System:**
```python
# FILE: src/infrastructure/quality/quality_gates.py

"""
Quality gates for CI/CD pipeline.
Enforces code quality, performance, and test coverage standards.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class QualityLevel(Enum):
    """Quality gate severity levels."""
    ERROR = "error"
    WARNING = "warning" 
    INFO = "info"

@dataclass
class QualityIssue:
    """Individual quality issue."""
    level: QualityLevel
    category: str
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    
class QualityGateRunner:
    """Runs quality checks and enforces standards."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues: List[QualityIssue] = []
    
    def run_all_checks(self) -> bool:
        """Run all quality checks. Returns True if all pass."""
        print("🔍 Running TKA v2 Quality Gates...")
        
        checks = [
            ("Type Safety", self._check_type_safety),
            ("Code Formatting", self._check_code_formatting),
            ("Test Coverage", self._check_test_coverage),
            ("Performance Baselines", self._check_performance_baselines),
            ("Documentation", self._check_documentation),
            ("Security", self._check_security),
            ("Architecture Compliance", self._check_architecture_compliance)
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            print(f"  🔄 {check_name}...")
            passed = check_func()
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"    {status}")
            
            if not passed:
                all_passed = False
        
        self._print_summary()
        return all_passed
    
    def _check_type_safety(self) -> bool:
        """Check type safety with mypy."""
        try:
            result = subprocess.run([
                "mypy", 
                str(self.project_root / "src"),
                "--config-file", str(self.project_root / "mypy.ini"),
                "--json-report", str(self.project_root / "mypy_report.json")
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                self.issues.append(QualityIssue(
                    level=QualityLevel.ERROR,
                    category="Type Safety",
                    message=f"MyPy type checking failed: {result.stdout}"
                ))
                return False
            
            return True
            
        except FileNotFoundError:
            self.issues.append(QualityIssue(
                level=QualityLevel.WARNING,
                category="Type Safety",
                message="MyPy not installed - type checking skipped"
            ))
            return True
    
    def _check_code_formatting(self) -> bool:
        """Check code formatting with black and isort."""
        try:
            # Check black formatting
            black_result = subprocess.run([
                "black", "--check", "--diff", str(self.project_root / "src")
            ], capture_output=True, text=True)
            
            # Check isort formatting
            isort_result = subprocess.run([
                "isort", "--check-only", "--diff", str(self.project_root / "src")
            ], capture_output=True, text=True)
            
            if black_result.returncode != 0:
                self.issues.append(QualityIssue(
                    level=QualityLevel.ERROR,
                    category="Code Formatting",
                    message=f"Black formatting issues found:\n{black_result.stdout}"
                ))
                return False
            
            if isort_result.returncode != 0:
                self.issues.append(QualityIssue(
                    level=QualityLevel.ERROR,
                    category="Code Formatting", 
                    message=f"Import sorting issues found:\n{isort_result.stdout}"
                ))
                return False
            
            return True
            
        except FileNotFoundError:
            self.issues.append(QualityIssue(
                level=QualityLevel.WARNING,
                category="Code Formatting",
                message="Black/isort not installed - formatting check skipped"
            ))
            return True
    
    def _check_test_coverage(self) -> bool:
        """Check test coverage meets minimum requirements."""
        try:
            result = subprocess.run([
                "pytest", 
                str(self.project_root / "tests"),
                "--cov=src",
                "--cov-report=json:coverage.json",
                "--cov-fail-under=80"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                self.issues.append(QualityIssue(
                    level=QualityLevel.ERROR,
                    category="Test Coverage",
                    message="Test coverage below 80% threshold"
                ))
                return False
            
            # Parse coverage report
            coverage_file = self.project_root / "coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    coverage_data = json.load(f)
                    total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
                    
                    if total_coverage < 85:
                        self.issues.append(QualityIssue(
                            level=QualityLevel.WARNING,
                            category="Test Coverage",
                            message=f"Test coverage {total_coverage:.1f}% - aim for 85%+"
                        ))
            
            return True
            
        except FileNotFoundError:
            self.issues.append(QualityIssue(
                level=QualityLevel.WARNING,
                category="Test Coverage",
                message="Pytest not installed - coverage check skipped"
            ))
            return True
    
    def _check_performance_baselines(self) -> bool:
        """Check performance against established baselines."""
        try:
            from src.infrastructure.monitoring.performance_monitor import get_performance_monitor
            
            monitor = get_performance_monitor()
            report = monitor.get_performance_report()
            
            regression_count = 0
            for operation, metrics in report["operations"].items():
                if metrics.get("regression_detected", False):
                    regression_count += 1
                    self.issues.append(QualityIssue(
                        level=QualityLevel.ERROR,
                        category="Performance",
                        message=f"Performance regression detected in {operation}"
                    ))
            
            if regression_count > 0:
                return False
            
            return True
            
        except Exception as e:
            self.issues.append(QualityIssue(
                level=QualityLevel.WARNING,
                category="Performance",
                message=f"Performance baseline check failed: {e}"
            ))
            return True
    
    def _check_documentation(self) -> bool:
        """Check documentation completeness."""
        required_docs = [
            "README.md",
            "ARCHITECTURE.md", 
            "API.md",
            "CONTRIBUTING.md"
        ]
        
        missing_docs = []
        for doc in required_docs:
            if not (self.project_root / doc).exists():
                missing_docs.append(doc)
        
        if missing_docs:
            self.issues.append(QualityIssue(
                level=QualityLevel.WARNING,
                category="Documentation",
                message=f"Missing documentation files: {', '.join(missing_docs)}"
            ))
        
        # Check for docstring coverage
        try:
            result = subprocess.run([
                "interrogate",
                str(self.project_root / "src"),
                "--quiet",
                "--fail-under=80"
            ], capture_output=True)
            
            if result.returncode != 0:
                self.issues.append(QualityIssue(
                    level=QualityLevel.WARNING,
                    category="Documentation",
                    message="Docstring coverage below 80%"
                ))
        except FileNotFoundError:
            pass  # interrogate not installed
        
        return True
    
    def _check_security(self) -> bool:
        """Check for security vulnerabilities."""
        try:
            # Check for known vulnerabilities in dependencies
            result = subprocess.run([
                "safety", "check", "--json"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                try:
                    vulnerabilities = json.loads(result.stdout)
                    if vulnerabilities:
                        self.issues.append(QualityIssue(
                            level=QualityLevel.ERROR,
                            category="Security",
                            message=f"Found {len(vulnerabilities)} security vulnerabilities"
                        ))
                        return False
                except json.JSONDecodeError:
                    pass
            
            # Check for hardcoded secrets
            result = subprocess.run([
                "bandit", "-r", str(self.project_root / "src"), "-f", "json"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                try:
                    bandit_report = json.loads(result.stdout)
                    high_severity = [r for r in bandit_report.get("results", []) 
                                   if r.get("issue_severity") == "HIGH"]
                    
                    if high_severity:
                        self.issues.append(QualityIssue(
                            level=QualityLevel.ERROR,
                            category="Security",
                            message=f"Found {len(high_severity)} high severity security issues"
                        ))
                        return False
                except json.JSONDecodeError:
                    pass
            
            return True
            
        except FileNotFoundError:
            self.issues.append(QualityIssue(
                level=QualityLevel.WARNING,
                category="Security",
                message="Security tools not installed - security check skipped"
            ))
            return True
    
    def _check_architecture_compliance(self) -> bool:
        """Check architecture compliance."""
        # Check for circular dependencies
        src_dir = self.project_root / "src"
        
        # Check domain layer has no dependencies on other layers
        domain_files = list((src_dir / "domain").rglob("*.py"))
        
        for file_path in domain_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Check for imports from application/infrastructure/presentation
                forbidden_imports = [
                    "from src.application",
                    "from application", 
                    "from src.infrastructure",
                    "from infrastructure",
                    "from src.presentation", 
                    "from presentation"
                ]
                
                for forbidden in forbidden_imports:
                    if forbidden in content:
                        self.issues.append(QualityIssue(
                            level=QualityLevel.ERROR,
                            category="Architecture",
                            message=f"Domain layer violation in {file_path}: {forbidden}",
                            file_path=str(file_path)
                        ))
                        return False
                        
            except Exception:
                continue
        
        # Check for V1 compatibility cruft
        v1_patterns = ["V1-style", "v1-style", "V1 approach", "old working service"]
        
        for file_path in src_dir.rglob("*.py"):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                for pattern in v1_patterns:
                    if pattern in content:
                        self.issues.append(QualityIssue(
                            level=QualityLevel.WARNING,
                            category="Architecture",
                            message=f"V1 compatibility cruft found in {file_path}: {pattern}",
                            file_path=str(file_path)
                        ))
                        
            except Exception:
                continue
        
        return True
    
    def _print_summary(self) -> None:
        """Print quality gate summary."""
        print("\n📊 Quality Gate Summary:")
        
        error_count = len([i for i in self.issues if i.level == QualityLevel.ERROR])
        warning_count = len([i for i in self.issues if i.level == QualityLevel.WARNING])
        
        print(f"  ❌ Errors: {error_count}")
        print(f"  ⚠️  Warnings: {warning_count}")
        
        if self.issues:
            print("\n📋 Issues Found:")
            for issue in self.issues:
                icon = "❌" if issue.level == QualityLevel.ERROR else "⚠️"
                print(f"  {icon} [{issue.category}] {issue.message}")
                if issue.file_path:
                    print(f"      File: {issue.file_path}")
                    if issue.line_number:
                        print(f"      Line: {issue.line_number}")
        
        if error_count == 0:
            print("\n🎉 All quality gates passed!")
        else:
            print(f"\n💥 Quality gates failed with {error_count} errors")

def main():
    """CLI entry point for quality gates."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run TKA v2 quality gates")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--fail-on-warning", action="store_true", 
                       help="Fail on warnings as well as errors")
    
    args = parser.parse_args()
    
    project_root = Path(args.project_root).absolute()
    runner = QualityGateRunner(project_root)
    
    success = runner.run_all_checks()
    
    if args.fail_on_warning:
        warning_count = len([i for i in runner.issues if i.level == QualityLevel.WARNING])
        if warning_count > 0:
            success = False
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

### **Task 3.5: Documentation Generation**

**Auto-generate Documentation:**
```python
# FILE: src/infrastructure/docs/doc_generator.py

"""
Automatic documentation generation for TKA v2.
Generates API docs, architecture diagrams, and user guides.
"""

import ast
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    docstring: Optional[str]
    methods: List[str]
    file_path: str
    is_interface: bool = False
    is_service: bool = False

@dataclass
class ServiceInfo:
    """Information about a service."""
    name: str
    interface: Optional[str]
    implementation: str
    dependencies: List[str]
    description: str

class DocumentationGenerator:
    """Generates comprehensive documentation."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = project_root / "src"
        self.docs_dir = project_root / "docs"
        self.docs_dir.mkdir(exist_ok=True)
    
    def generate_all(self) -> None:
        """Generate all documentation."""
        print("📚 Generating TKA v2 Documentation...")
        
        # Generate API documentation
        self._generate_api_docs()
        print("  ✅ API Documentation")
        
        # Generate architecture overview
        self._generate_architecture_docs()
        print("  ✅ Architecture Documentation")
        
        # Generate service documentation
        self._generate_service_docs() 
        print("  ✅ Service Documentation")
        
        # Generate user guide
        self._generate_user_guide()
        print("  ✅ User Guide")
        
        print(f"🎉 Documentation generated in: {self.docs_dir}")
    
    def _generate_api_docs(self) -> None:
        """Generate API documentation."""
        api_file = self.src_dir / "infrastructure" / "api" / "rest_api.py"
        
        if not api_file.exists():
            return
        
        # Parse API endpoints
        endpoints = self._parse_api_endpoints(api_file)
        
        # Generate markdown
        content = [
            "# TKA Desktop API Documentation",
            "",
            "This document describes the REST API for TKA Desktop v2.",
            "",
            "## Base URL",
            "```",
            "http://localhost:8000/api",
            "```",
            "",
            "## Endpoints",
            ""
        ]
        
        for endpoint in endpoints:
            content.extend([
                f"### {endpoint['method']} {endpoint['path']}",
                "",
                endpoint.get('description', 'No description available.'),
                "",
                "**Request:**",
                f"```http",
                f"{endpoint['method']} {endpoint['path']}",
                "```",
                "",
                "**Response:**",
                "```json",
                json.dumps(endpoint.get('response_example', {}), indent=2),
                "```",
                ""
            ])
        
        with open(self.docs_dir / "API.md", 'w') as f:
            f.write('\n'.join(content))
    
    def _generate_architecture_docs(self) -> None:
        """Generate architecture documentation."""
        content = [
            "# TKA Desktop v2 Architecture",
            "",
            "## Overview",
            "",
            "TKA Desktop v2 follows Clean Architecture principles with clear separation of concerns:",
            "",
            "```",
            "src/",
            "├── domain/          # Business logic and models",
            "├── application/     # Use cases and services",
            "├── infrastructure/  # External concerns (DB, APIs, etc.)",
            "└── presentation/    # UI components and controllers",
            "```",
            "",
            "## Layer Responsibilities",
            "",
            "### Domain Layer",
            "- Core business models (`BeatData`, `SequenceData`, `MotionData`)",
            "- Business rules and invariants",
            "- No dependencies on other layers",
            "",
            "### Application Layer", 
            "- Application services implementing use cases",
            "- Service interfaces (Protocols)",
            "- Cross-cutting concerns (events, commands)",
            "",
            "### Infrastructure Layer",
            "- Data persistence",
            "- External API integrations", 
            "- Configuration management",
            "",
            "### Presentation Layer",
            "- UI components and widgets",
            "- User interaction handling",
            "- View models and controllers",
            "",
            "## Key Patterns",
            "",
            "### Dependency Injection",
            "- Constructor injection with type resolution",
            "- Interface-based programming",
            "- Singleton and transient lifetimes",
            "",
            "### Event-Driven Architecture",
            "- Type-safe event bus",
            "- Decoupled component communication",
            "- Event sourcing for complex workflows",
            "",
            "### Command Pattern",
            "- Undoable operations",
            "- Command history and replay",
            "- Transactional business operations",
            "",
            "## Service Architecture",
            ""
        ]
        
        # Add service information
        services = self._analyze_services()
        for service in services:
            content.extend([
                f"### {service.name}",
                f"- **Interface**: `{service.interface}`",
                f"- **Implementation**: `{service.implementation}`",
                f"- **Dependencies**: {', '.join(service.dependencies) if service.dependencies else 'None'}",
                f"- **Description**: {service.description}",
                ""
            ])
        
        with open(self.docs_dir / "ARCHITECTURE.md", 'w') as f:
            f.write('\n'.join(content))
    
    def _generate_service_docs(self) -> None:
        """Generate detailed service documentation."""
        services = self._analyze_services()
        
        content = [
            "# Service Documentation",
            "",
            "This document provides detailed information about all services in TKA v2.",
            ""
        ]
        
        for service in services:
            content.extend([
                f"## {service.name}",
                "",
                f"**Interface**: `{service.interface}`",
                f"**Implementation**: `{service.implementation}`",
                "",
                f"### Description",
                service.description,
                "",
                f"### Dependencies",
                ""
            ])
            
            if service.dependencies:
                for dep in service.dependencies:
                    content.append(f"- `{dep}`")
            else:
                content.append("- None")
            
            content.extend(["", "---", ""])
        
        with open(self.docs_dir / "SERVICES.md", 'w') as f:
            f.write('\n'.join(content))
    
    def _generate_user_guide(self) -> None:
        """Generate user guide."""
        content = [
            "# TKA Desktop v2 User Guide",
            "",
            "## Getting Started",
            "",
            "### Installation", 
            "",
            "1. Clone the repository",
            "2. Install dependencies: `pip install -r requirements.txt`",
            "3. Run the application: `python v2/main.py`",
            "",
            "### Basic Usage",
            "",
            "1. **Create a Sequence**: Use the Construct tab to create new sequences",
            "2. **Add Beats**: Click the '+' button to add beats to your sequence",
            "3. **Edit Motions**: Select a beat and modify its blue/red motions",
            "4. **Preview**: Use the graph editor to preview your sequence",
            "",
            "## Advanced Features",
            "",
            "### Command Line Interface",
            "",
            "TKA v2 includes a powerful CLI for automation:",
            "",
            "```bash",
            "# Generate API bindings",
            "python src/infrastructure/codegen/schema_generator.py --language typescript",
            "",
            "# Run quality gates",
            "python src/infrastructure/quality/quality_gates.py",
            "",
            "# Start API server",
            "python src/infrastructure/api/rest_api.py",
            "```",
            "",
            "### API Integration",
            "",
            "TKA v2 provides a REST API for external integrations. See [API.md](API.md) for details.",
            "",
            "### Performance Monitoring",
            "",
            "Enable performance monitoring to track application performance:",
            "",
            "```python",
            "from src.infrastructure.monitoring.performance_monitor import monitor_performance",
            "",
            "@monitor_performance()",
            "def my_function():",
            "    # Function will be automatically monitored",
            "    pass",
            "```"
        ]
        
        with open(self.docs_dir / "USER_GUIDE.md", 'w') as f:
            f.write('\n'.join(content))
    
    def _parse_api_endpoints(self, api_file: Path) -> List[Dict[str, Any]]:
        """Parse API endpoints from FastAPI file."""
        # This is a simplified parser - in reality you'd want more sophisticated parsing
        endpoints = [
            {
                "method": "GET",
                "path": "/api/sequences/",
                "description": "List all sequences",
                "response_example": {"sequences": []}
            },
            {
                "method": "POST", 
                "path": "/api/sequences/",
                "description": "Create a new sequence",
                "response_example": {"id": "seq_123", "name": "New Sequence"}
            }
        ]
        return endpoints
    
    def _analyze_services(self) -> List[ServiceInfo]:
        """Analyze services in the application."""
        services = [
            ServiceInfo(
                name="Sequence Management",
                interface="ISequenceManagementService",
                implementation="SequenceManagementService", 
                dependencies=["IEventBus", "CommandProcessor"],
                description="Manages sequence creation, modification, and persistence"
            ),
            ServiceInfo(
                name="Motion Management",
                interface="IMotionManagementService",
                implementation="MotionManagementService",
                dependencies=["IMotionValidationService", "IMotionGenerationService"],
                description="Handles motion generation, validation, and transformation"
            ),
            ServiceInfo(
                name="Arrow Management",
                interface="IArrowManagementService", 
                implementation="ArrowManagementService",
                dependencies=["DefaultPlacementService", "PlacementKeyService"],
                description="Manages arrow positioning, rotation, and visualization"
            )
        ]
        return services

def main():
    """CLI entry point for documentation generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate TKA v2 documentation")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--type", choices=["all", "api", "architecture", "services", "user"], 
                       default="all", help="Documentation type to generate")
    
    args = parser.parse_args()
    
    project_root = Path(args.project_root).absolute()
    generator = DocumentationGenerator(project_root)
    
    if args.type == "all":
        generator.generate_all()
    elif args.type == "api":
        generator._generate_api_docs()
    elif args.type == "architecture":
        generator._generate_architecture_docs()
    elif args.type == "services":
        generator._generate_service_docs()
    elif args.type == "user":
        generator._generate_user_guide()

if __name__ == "__main__":
    main()
```

---

## 🎯 **Implementation Timeline Summary**

### **Phase 1: Immediate Technical Debt Elimination** (1 Week)
- **Days 1-2**: Remove all V1 compatibility code and comments
- **Days 3-4**: Complete DI container with full auto-injection
- **Day 5**: Validation testing and integration

### **Phase 2: Advanced Architecture Patterns** (2 Weeks)
- **Week 1**: Event-driven architecture with type-safe event bus
- **Week 2**: Command pattern for undo/redo functionality

### **Phase 3: Enterprise-Grade Features** (2 Weeks)
- **Week 1**: Cross-language API layer and schema generation
- **Week 2**: Performance monitoring and quality gates

## 🏆 **Success Criteria**

After completing all phases, you will have achieved:

- ✅ **Zero technical debt** from V1 compatibility
- ✅ **100% automatic dependency injection** 
- ✅ **Event-driven architecture** for complex state management
- ✅ **Comprehensive undo/redo** system
- ✅ **Cross-language API** compatibility
- ✅ **Enterprise-grade monitoring** and quality gates
- ✅ **Automatic documentation** generation

**Result**: World-class architecture ready for the next 5+ years of development.

---

## 🚀 **Getting Started**

To begin Phase 1 immediately:

```bash
# 1. Create a new branch for the cleanup
git checkout -b phase1-technical-debt-elimination

# 2. Find all V1 references
cd TKA/tka-desktop/v2/src/application/services
grep -r "V1\|v1\|old\|legacy" . --include="*.py" > v1_references.txt

# 3. Start with the most critical service
# Edit arrow_management_service.py first - remove all V1 comments

# 4. Run tests to ensure nothing breaks
python -m pytest tests/ -v

# 5. Continue with