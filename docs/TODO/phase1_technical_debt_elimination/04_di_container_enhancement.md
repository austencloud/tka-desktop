# **Task 1.3: Complete Auto-Injection Implementation**

**Timeline**: Day 3-4  
**Priority**: CRITICAL  
**Goal**: Implement comprehensive automatic constructor injection for the DI container

---

## **Current Gap Analysis:**

### **Current Implementation (Basic)**

```python
# CURRENT: Basic constructor injection
def _create_instance(self, implementation_class: Type) -> Any:
    # ❌ Skips complex dependencies
    # ❌ No validation of dependency chain
    # ❌ Limited error reporting
```

### **Required Implementation (Enhanced)**

```python
# REQUIRED: Comprehensive automatic constructor injection
def _create_instance(self, implementation_class: Type) -> Any:
    # ✅ Handles multi-level dependencies
    # ✅ Validates complete dependency chain
    # ✅ Provides detailed error reporting
    # ✅ Supports default parameters
    # ✅ Skips primitive types automatically
```

---

## **Implementation Required:**

### **FILE: src/core/dependency_injection/di_container.py**

```python
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

---

## **Helper Methods to Add:**

### **Primitive Type Detection**

```python
def _is_primitive_type(self, param_type: Type) -> bool:
    """Check if type is a primitive that should not be injected."""
    primitive_types = {
        str, int, float, bool, bytes,
        type(None), list, dict, tuple, set,
        # Add common standard library types
        Path, datetime, timedelta
    }

    # Handle Union types (e.g., Optional[str])
    if hasattr(param_type, '__origin__'):
        if param_type.__origin__ is Union:
            # Check if it's Optional[T] (Union[T, None])
            args = param_type.__args__
            if len(args) == 2 and type(None) in args:
                # It's Optional[T], check the non-None type
                non_none_type = next(arg for arg in args if arg is not type(None))
                return self._is_primitive_type(non_none_type)

    return param_type in primitive_types or param_type.__module__ == 'builtins'
```

### **Protocol Validation**

```python
def _validate_protocol_implementation(self, interface: Type, implementation: Type) -> None:
    """Validate that implementation satisfies the protocol interface."""
    if not hasattr(interface, '__protocols__') and not hasattr(interface, '_is_protocol'):
        # Not a protocol, skip validation
        return

    # Check if implementation has all required methods
    required_methods = []
    for attr_name in dir(interface):
        attr = getattr(interface, attr_name)
        if callable(attr) and not attr_name.startswith('_'):
            required_methods.append(attr_name)

    missing_methods = []
    for method_name in required_methods:
        if not hasattr(implementation, method_name):
            missing_methods.append(method_name)
        elif not callable(getattr(implementation, method_name)):
            missing_methods.append(f"{method_name} (not callable)")

    if missing_methods:
        raise ValueError(
            f"{implementation.__name__} does not implement {interface.__name__}. "
            f"Missing: {', '.join(missing_methods)}"
        )
```

### **Constructor Dependency Analysis**

```python
def _get_constructor_dependencies(self, implementation: Type) -> List[Type]:
    """Get list of constructor dependencies for a class."""
    try:
        signature = inspect.signature(implementation.__init__)
        type_hints = get_type_hints(implementation.__init__)
        dependencies = []

        for param_name, param in signature.parameters.items():
            if param_name == "self":
                continue

            # Skip if has default value
            if param.default != inspect.Parameter.empty:
                continue

            param_type = type_hints.get(param_name, param.annotation)

            # Skip if no type annotation
            if not param_type or param_type == inspect.Parameter.empty:
                continue

            # Skip primitive types
            if self._is_primitive_type(param_type):
                continue

            dependencies.append(param_type)

        return dependencies

    except Exception:
        return []
```

---

## **Enhanced Features to Add:**

### **1. Circular Dependency Detection**

```python
def _detect_circular_dependencies(self, start_type: Type, visited: Optional[Set[Type]] = None) -> None:
    """Detect circular dependencies in the service graph."""
    if visited is None:
        visited = set()

    if start_type in visited:
        cycle_path = " -> ".join(t.__name__ for t in visited) + f" -> {start_type.__name__}"
        raise ValueError(f"Circular dependency detected: {cycle_path}")

    visited.add(start_type)

    # Get implementation for this type
    implementation = self._services.get(start_type) or self._factories.get(start_type)
    if implementation:
        dependencies = self._get_constructor_dependencies(implementation)
        for dep in dependencies:
            self._detect_circular_dependencies(dep, visited.copy())
```

### **2. Dependency Graph Generation**

```python
def get_dependency_graph(self) -> Dict[str, List[str]]:
    """Generate dependency graph for debugging."""
    graph = {}

    for interface, implementation in self._services.items():
        deps = self._get_constructor_dependencies(implementation)
        graph[f"{interface.__name__} -> {implementation.__name__}"] = [
            dep.__name__ for dep in deps if not self._is_primitive_type(dep)
        ]

    return graph
```

### **3. Service Lifecycle Management**

```python
def _create_with_lifecycle(self, implementation_class: Type) -> Any:
    """Create instance with proper lifecycle management."""
    instance = self._create_instance(implementation_class)

    # Call initialization method if it exists
    if hasattr(instance, 'initialize') and callable(getattr(instance, 'initialize')):
        instance.initialize()

    # Register for cleanup if it has cleanup method
    if hasattr(instance, 'cleanup') and callable(getattr(instance, 'cleanup')):
        self._cleanup_handlers.append(instance.cleanup)

    return instance

def cleanup_all(self) -> None:
    """Cleanup all registered services."""
    for cleanup_handler in reversed(self._cleanup_handlers):
        try:
            cleanup_handler()
        except Exception as e:
            logger.error(f"Error during service cleanup: {e}")

    self._cleanup_handlers.clear()
```

---

## **Integration Points:**

### **Update Constructor**

```python
def __init__(self):
    self._services: Dict[Type, Type] = {}
    self._instances: Dict[Type, Any] = {}
    self._factories: Dict[Type, Callable] = {}
    self._cleanup_handlers: List[Callable] = []  # New for lifecycle management
    self._creation_stack: List[Type] = []  # New for circular dependency detection
```

---

## **Testing the Enhanced Implementation:**

### **Test Complex Dependencies**

```python
# Example of complex dependency chain that should work:
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

# This should work automatically:
container.auto_register_with_validation(IRepository, Repository)
container.auto_register_with_validation(IService, Service)
controller = container._create_instance(Controller)  # Should work!
```

---

## **Validation Steps:**

### **1. Dependency Chain Validation**

```python
# Test that complex dependency chains work
container = DIContainer()
container.auto_register_with_validation(IRepository, Repository)
container.auto_register_with_validation(IService, Service)

# This should validate the entire chain
container.validate_all_registrations()
```

### **2. Error Reporting Validation**

```python
# Test enhanced error messages
try:
    container.resolve(UnregisteredService)
except ValueError as e:
    assert "Available registrations:" in str(e)
    assert "Cannot resolve dependency" in str(e)
```

### **3. Circular Dependency Detection**

```python
class A:
    def __init__(self, b: 'B'): pass

class B:
    def __init__(self, a: A): pass

# This should detect the circular dependency
with pytest.raises(ValueError, match="Circular dependency detected"):
    container.auto_register_with_validation(A, A)
    container.auto_register_with_validation(B, B)
```

---

## **Success Criteria:**

By the end of Task 1.3:

- ✅ **Complex dependency chains** resolve automatically
- ✅ **Default parameters** are handled correctly
- ✅ **Primitive types** are skipped appropriately
- ✅ **Circular dependencies** are detected and prevented
- ✅ **Detailed error messages** help with debugging
- ✅ **All existing services** work with enhanced DI

---

## **Next Step**

After completing auto-injection enhancement, proceed to: [Task 1.4: Enhanced Error Reporting](05_enhanced_error_reporting.md)
