# **Task 1.4: Enhanced Error Reporting**

**Timeline**: Day 3-4  
**Priority**: HIGH  
**Goal**: Add comprehensive diagnostic methods to the DI container for debugging

---

## **Add Diagnostic Methods:**

### **FILE: src/core/dependency_injection/di_container.py**

Add these diagnostic methods to provide detailed failure analysis:

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

def get_registration_info(self) -> Dict[str, Any]:
    """Get comprehensive information about all registrations."""
    info = {
        "total_services": len(self._services),
        "total_factories": len(self._factories),
        "total_instances": len(self._instances),
        "services": {},
        "factories": {},
        "dependency_graph": self.get_dependency_graph()
    }

    # Service details
    for interface, implementation in self._services.items():
        deps = self._get_constructor_dependencies(implementation)
        info["services"][interface.__name__] = {
            "implementation": implementation.__name__,
            "dependencies": [dep.__name__ for dep in deps],
            "has_instance": interface in self._instances,
            "can_resolve": self._can_resolve_safely(interface)
        }

    # Factory details
    for interface, factory in self._factories.items():
        info["factories"][interface.__name__] = {
            "factory": str(factory),
            "can_resolve": self._can_resolve_safely(interface)
        }

    return info

def _can_resolve_safely(self, interface: Type) -> bool:
    """Check if interface can be resolved without side effects."""
    try:
        # Try to resolve without creating instance (dry run)
        if interface in self._services:
            implementation = self._services[interface]
            deps = self._get_constructor_dependencies(implementation)

            # Check if all dependencies can be resolved
            for dep in deps:
                if dep not in self._services and dep not in self._factories:
                    if not self._is_primitive_type(dep):
                        return False
            return True
        elif interface in self._factories:
            return True
        else:
            return False
    except Exception:
        return False

def print_dependency_graph(self) -> None:
    """Print a human-readable dependency graph."""
    graph = self.get_dependency_graph()

    print("🔍 Dependency Graph:")
    print("=" * 50)

    if not graph:
        print("No dependencies found.")
        return

    for service, deps in graph.items():
        print(f"\n📦 {service}")
        if deps:
            for dep in deps:
                print(f"  └── depends on: {dep}")
        else:
            print("  └── no dependencies")

def print_registration_summary(self) -> None:
    """Print a summary of all registrations."""
    info = self.get_registration_info()

    print("📋 Registration Summary:")
    print("=" * 50)
    print(f"Total Services: {info['total_services']}")
    print(f"Total Factories: {info['total_factories']}")
    print(f"Total Instances: {info['total_instances']}")

    print("\n🔧 Services:")
    for interface_name, service_info in info["services"].items():
        status = "✅" if service_info["can_resolve"] else "❌"
        instance_status = "💾" if service_info["has_instance"] else "🆕"
        print(f"  {status} {instance_status} {interface_name} -> {service_info['implementation']}")

        if service_info["dependencies"]:
            for dep in service_info["dependencies"]:
                print(f"    └── {dep}")

    print("\n🏭 Factories:")
    for interface_name, factory_info in info["factories"].items():
        status = "✅" if factory_info["can_resolve"] else "❌"
        print(f"  {status} {interface_name} -> {factory_info['factory']}")

def validate_registration_health(self) -> Tuple[bool, List[str]]:
    """Comprehensive health check of all registrations."""
    issues = []

    # Check for unresolvable services
    for interface, implementation in self._services.items():
        if not self._can_resolve_safely(interface):
            issues.append(f"Cannot resolve {interface.__name__} -> {implementation.__name__}")

    # Check for circular dependencies
    for interface in self._services.keys():
        try:
            self._detect_circular_dependencies(interface)
        except ValueError as e:
            issues.append(f"Circular dependency: {e}")

    # Check for missing dependencies
    for interface, implementation in self._services.items():
        deps = self._get_constructor_dependencies(implementation)
        for dep in deps:
            if not self._is_primitive_type(dep):
                if dep not in self._services and dep not in self._factories:
                    issues.append(f"{implementation.__name__} depends on unregistered {dep.__name__}")

    return len(issues) == 0, issues

def get_resolution_path(self, interface: Type) -> List[str]:
    """Get the resolution path for an interface (for debugging)."""
    path = []

    def trace_resolution(current_interface: Type, depth: int = 0):
        indent = "  " * depth

        if current_interface in self._services:
            implementation = self._services[current_interface]
            path.append(f"{indent}{current_interface.__name__} -> {implementation.__name__}")

            deps = self._get_constructor_dependencies(implementation)
            for dep in deps:
                if not self._is_primitive_type(dep):
                    trace_resolution(dep, depth + 1)
                else:
                    path.append(f"{indent}  {dep.__name__} (primitive)")

        elif current_interface in self._factories:
            factory = self._factories[current_interface]
            path.append(f"{indent}{current_interface.__name__} -> factory({factory})")

        else:
            path.append(f"{indent}{current_interface.__name__} -> NOT REGISTERED ❌")

    trace_resolution(interface)
    return path

def print_resolution_path(self, interface: Type) -> None:
    """Print the resolution path for debugging."""
    print(f"🛤️  Resolution Path for {interface.__name__}:")
    print("=" * 50)

    path = self.get_resolution_path(interface)
    for step in path:
        print(step)
```

---

## **Enhanced Error Handling in Core Methods:**

### **Update resolve() method with better error reporting:**

```python
def resolve(self, interface: Type[T]) -> T:
    """Resolve service with enhanced error reporting."""
    try:
        return self._resolve_internal(interface)
    except Exception as e:
        # Generate diagnostic information
        diagnosis = self.diagnose_resolution_failure(interface)

        logger.error(f"Resolution failed for {interface.__name__}")
        logger.error(diagnosis)

        # Re-raise with enhanced message
        raise ValueError(f"Cannot resolve {interface.__name__}: {e}\n\nDiagnosis:\n{diagnosis}")

def _resolve_internal(self, interface: Type[T]) -> T:
    """Internal resolution with original logic."""
    # ... existing resolve logic ...
    pass
```

### **Update auto_register_with_validation() with better error reporting:**

```python
def auto_register_with_validation(self, interface: Type[T], implementation: Type[T]) -> None:
    """Register service with comprehensive validation and error reporting."""
    try:
        # Step 1: Validate Protocol implementation
        self._validate_protocol_implementation(interface, implementation)
        logger.debug(f"✅ Protocol validation passed: {interface.__name__}")

        # Step 2: Validate dependency chain can be resolved
        self._validate_dependency_chain(implementation)
        logger.debug(f"✅ Dependency chain validation passed: {implementation.__name__}")

        # Step 3: Check for circular dependencies
        self._detect_circular_dependencies(interface)
        logger.debug(f"✅ Circular dependency check passed: {interface.__name__}")

        # Step 4: Register if validation passes
        self.register_singleton(interface, implementation)

        logger.info(f"✅ Successfully registered {interface.__name__} -> {implementation.__name__}")

    except ValueError as e:
        # Enhanced error reporting
        error_msg = f"Registration failed for {interface.__name__} -> {implementation.__name__}: {e}"
        logger.error(error_msg)

        # Provide additional context
        if "not registered" in str(e):
            logger.error("Available registrations:")
            for registered in self._services.keys():
                logger.error(f"  - {registered.__name__}")

        # Print dependency information
        deps = self._get_constructor_dependencies(implementation)
        if deps:
            logger.error(f"Constructor dependencies for {implementation.__name__}:")
            for dep in deps:
                status = "✅" if dep in self._services or self._is_primitive_type(dep) else "❌"
                logger.error(f"  {status} {dep.__name__}")

        raise ValueError(error_msg)
```

---

## **Debug CLI Commands:**

Add methods that can be called from CLI or debug console:

```python
def debug_info(self, interface_name: Optional[str] = None) -> None:
    """Print comprehensive debug information."""
    if interface_name:
        # Debug specific interface
        matching_interfaces = [
            interface for interface in self._services.keys()
            if interface.__name__ == interface_name
        ]

        if matching_interfaces:
            interface = matching_interfaces[0]
            print(f"🔍 Debug Info for {interface_name}:")
            print("=" * 50)
            self.print_resolution_path(interface)
            print()
            diagnosis = self.diagnose_resolution_failure(interface)
            print(diagnosis)
        else:
            print(f"❌ Interface '{interface_name}' not found")
            print("Available interfaces:")
            for interface in self._services.keys():
                print(f"  - {interface.__name__}")
    else:
        # Print overall summary
        self.print_registration_summary()
        print()
        self.print_dependency_graph()

        health_ok, issues = self.validate_registration_health()
        if not health_ok:
            print("\n⚠️  Health Issues Found:")
            for issue in issues:
                print(f"  ❌ {issue}")
        else:
            print("\n✅ All registrations are healthy!")

# CLI helper function
def debug_container(container: DIContainer, interface_name: Optional[str] = None):
    """Debug helper function for CLI usage."""
    container.debug_info(interface_name)
```

---

## **Example Usage:**

### **1. Debug resolution failures:**

```python
# When a resolution fails, you get detailed information:
try:
    service = container.resolve(IUnknownService)
except ValueError as e:
    print(e)  # Shows diagnosis and available services
```

### **2. Debug dependency graph:**

```python
# Print the complete dependency graph
container.print_dependency_graph()

# Or get it programmatically
graph = container.get_dependency_graph()
```

### **3. Health check before deployment:**

```python
# Validate all registrations
health_ok, issues = container.validate_registration_health()
if not health_ok:
    for issue in issues:
        logger.error(f"Registration issue: {issue}")
    raise ValueError("Container health check failed")
```

### **4. Debug specific service:**

```python
# Get detailed info about specific service
container.debug_info("ISequenceManagementService")

# Print resolution path
container.print_resolution_path(ISequenceManagementService)
```

---

## **Integration with Logging:**

### **Add structured logging configuration:**

```python
import logging

# Configure logging for DI container
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# In the container __init__:
def __init__(self):
    # ... existing init ...
    self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    self._logger.info("DI Container initialized")
```

---

## **Success Criteria:**

By the end of Task 1.4:

- ✅ **Detailed error messages** for resolution failures
- ✅ **Dependency graph visualization** available
- ✅ **Health check methods** for validation
- ✅ **Debug CLI commands** for troubleshooting
- ✅ **Structured logging** throughout DI operations
- ✅ **Resolution path tracing** for complex dependencies

---

## **Next Step**

After completing enhanced error reporting, proceed to: [Task 1.5: Comprehensive DI Testing](06_validation_and_testing.md)
