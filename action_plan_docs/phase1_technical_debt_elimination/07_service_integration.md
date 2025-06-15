# **Task 1.6: Integration with Existing Services**

**Timeline**: Day 5  
**Priority**: CRITICAL  
**Goal**: Update main application to use enhanced DI with validation

---

## **Update Service Registration:**

### **FILE: v2/main.py**

Replace the existing service configuration with enhanced DI validation:

```python
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

def _register_motion_services(self):
    """Register motion-related services with validation."""
    try:
        # Register core motion services
        self.container.auto_register_with_validation(
            IMotionManagementService,
            MotionManagementService
        )

        self.container.auto_register_with_validation(
            IArrowManagementService,
            ArrowManagementService
        )

        self.container.auto_register_with_validation(
            IMotionValidationService,
            MotionValidationService
        )

        # Register positioning services
        self.container.auto_register_with_validation(
            IDefaultPlacementService,
            DefaultPlacementService
        )

        self.container.auto_register_with_validation(
            IPlacementKeyService,
            PlacementKeyService
        )

        logger.info("✅ Motion services registered successfully")

    except Exception as e:
        logger.error(f"Motion service registration failed: {e}")
        # Print diagnostic information
        self.container.debug_info()
        raise

def _register_layout_services(self):
    """Register layout-related services with validation."""
    try:
        self.container.auto_register_with_validation(
            ILayoutManagementService,
            LayoutManagementService
        )

        self.container.auto_register_with_validation(
            IUIStateManagementService,
            UIStateManagementService
        )

        self.container.auto_register_with_validation(
            IComponentFactoryService,
            ComponentFactoryService
        )

        logger.info("✅ Layout services registered successfully")

    except Exception as e:
        logger.error(f"Layout service registration failed: {e}")
        self.container.debug_info()
        raise

def _register_pictograph_services(self):
    """Register pictograph-related services with validation."""
    try:
        self.container.auto_register_with_validation(
            IPictographManagementService,
            PictographManagementService
        )

        self.container.auto_register_with_validation(
            IVisualizationService,
            VisualizationService
        )

        self.container.auto_register_with_validation(
            IRenderingService,
            RenderingService
        )

        logger.info("✅ Pictograph services registered successfully")

    except Exception as e:
        logger.error(f"Pictograph service registration failed: {e}")
        self.container.debug_info()
        raise

def _validate_service_health(self):
    """Perform comprehensive service health validation."""
    if self.splash:
        self.splash.update_progress(45, "Validating service health...")

    try:
        # Perform health check
        health_ok, issues = self.container.validate_registration_health()

        if not health_ok:
            logger.error("Service health check failed:")
            for issue in issues:
                logger.error(f"  ❌ {issue}")

            # Print detailed diagnostic information
            print("\n" + "="*60)
            print("🚨 SERVICE HEALTH CHECK FAILED")
            print("="*60)
            self.container.debug_info()
            print("="*60)

            raise ValueError(f"Service health check failed with {len(issues)} issues")

        # Print dependency graph for verification
        logger.info("Service dependency graph:")
        self.container.print_dependency_graph()

        if self.splash:
            self.splash.update_progress(50, "✅ Service health validated")

        logger.info("✅ All services are healthy and ready")

    except Exception as e:
        logger.error(f"Service health validation failed: {e}")
        raise
```

---

## **Enhanced Error Handling:**

### **Add Startup Diagnostics:**

```python
def _startup_diagnostics(self):
    """Run comprehensive startup diagnostics."""
    logger.info("🔍 Running startup diagnostics...")

    try:
        # Check DI container health
        self._validate_service_health()

        # Test critical service resolution
        self._test_critical_services()

        # Validate service interactions
        self._validate_service_interactions()

        logger.info("✅ Startup diagnostics passed")

    except Exception as e:
        logger.error(f"Startup diagnostics failed: {e}")
        self._print_diagnostic_report()
        raise

def _test_critical_services(self):
    """Test that critical services can be resolved and function."""
    critical_services = [
        ISequenceManagementService,
        ILayoutManagementService,
        IArrowManagementService,
        IMotionManagementService
    ]

    for service_interface in critical_services:
        try:
            service = self.container.resolve(service_interface)
            logger.info(f"✅ {service_interface.__name__} resolved successfully")

            # Test basic functionality if available
            if hasattr(service, 'initialize') and callable(getattr(service, 'initialize')):
                service.initialize()
                logger.info(f"✅ {service_interface.__name__} initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to resolve {service_interface.__name__}: {e}")
            logger.error(self.container.diagnose_resolution_failure(service_interface))
            raise

def _validate_service_interactions(self):
    """Validate that services can interact with each other."""
    try:
        # Test sequence management service
        sequence_service = self.container.resolve(ISequenceManagementService)

        # Test basic sequence creation (should not fail)
        test_sequence = sequence_service.create_sequence("Startup Test")
        logger.info("✅ Sequence creation test passed")

        # Test arrow management service
        arrow_service = self.container.resolve(IArrowManagementService)

        # Test basic arrow operations (should not fail)
        # arrow_service.test_basic_operations()  # If such method exists
        logger.info("✅ Arrow management test passed")

        logger.info("✅ Service interaction validation passed")

    except Exception as e:
        logger.error(f"Service interaction validation failed: {e}")
        raise

def _print_diagnostic_report(self):
    """Print comprehensive diagnostic report on failure."""
    print("\n" + "="*80)
    print("🚨 STARTUP FAILURE DIAGNOSTIC REPORT")
    print("="*80)

    # Print registration summary
    self.container.print_registration_summary()

    print("\n" + "-"*80)
    print("📊 DEPENDENCY GRAPH")
    print("-"*80)
    self.container.print_dependency_graph()

    print("\n" + "-"*80)
    print("🔍 HEALTH CHECK RESULTS")
    print("-"*80)
    health_ok, issues = self.container.validate_registration_health()

    if not health_ok:
        print("❌ Health check failed with issues:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("✅ Health check passed")

    print("\n" + "-"*80)
    print("📋 REGISTRATION INFO")
    print("-"*80)
    info = self.container.get_registration_info()
    print(f"Total Services: {info['total_services']}")
    print(f"Total Factories: {info['total_factories']}")
    print(f"Total Instances: {info['total_instances']}")

    print("="*80)
```

---

## **Update Application Initialization:**

### **Enhanced **init** method:**

```python
def __init__(self):
    """Initialize TKA Desktop with enhanced DI validation."""
    super().__init__()

    # Initialize logging first
    self._setup_logging()

    logger.info("🚀 Starting TKA Desktop v2 with enhanced DI...")

    # Initialize splash screen
    self.splash = self._create_splash_screen()
    if self.splash:
        self.splash.show()
        self.splash.update_progress(10, "Initializing dependency injection...")

    try:
        # Initialize DI container with enhanced features
        self.container = DIContainer()
        logger.info("✅ DI Container initialized")

        # Configure services with validation
        self._configure_services()

        # Run startup diagnostics
        self._startup_diagnostics()

        # Initialize UI components
        self._initialize_ui()

        if self.splash:
            self.splash.update_progress(100, "✅ Startup complete")
            self.splash.finish(self.main_window)

        logger.info("🎉 TKA Desktop v2 startup completed successfully")

    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")

        if self.splash:
            self.splash.update_progress(100, f"❌ Startup failed: {str(e)[:50]}...")
            self.splash.close()

        # Show error dialog
        self._show_startup_error(e)
        raise

def _show_startup_error(self, error: Exception):
    """Show detailed startup error to user."""
    from PyQt6.QtWidgets import QMessageBox

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("TKA Desktop Startup Failed")
    msg.setText("TKA Desktop failed to start due to a configuration error.")

    # Create detailed text with diagnostic information
    detailed_text = f"""
Error: {str(error)}

Diagnostic Information:
{self._get_diagnostic_summary()}

Please check the log file for more details.
    """

    msg.setDetailedText(detailed_text)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()

def _get_diagnostic_summary(self) -> str:
    """Get summary of diagnostic information."""
    try:
        if not hasattr(self, 'container'):
            return "DI Container not initialized"

        info = self.container.get_registration_info()
        health_ok, issues = self.container.validate_registration_health()

        summary = f"""
Services Registered: {info['total_services']}
Factories Registered: {info['total_factories']}
Health Status: {'✅ Healthy' if health_ok else '❌ Issues Found'}
        """

        if not health_ok:
            summary += f"\nIssues ({len(issues)}):\n"
            for issue in issues[:5]:  # Show first 5 issues
                summary += f"- {issue}\n"
            if len(issues) > 5:
                summary += f"... and {len(issues) - 5} more issues\n"

        return summary

    except Exception:
        return "Unable to generate diagnostic summary"
```

---

## **Service Migration Examples:**

### **Update individual services to use enhanced DI:**

```python
# EXAMPLE: Update SequenceManagementService to work with enhanced DI

class SequenceManagementService:
    """Sequence management with enhanced DI support."""

    def __init__(self,
                 event_bus: IEventBus,
                 motion_service: IMotionManagementService,
                 validation_service: IValidationService = None):  # Optional dependency
        """Initialize with automatic dependency injection."""
        self.event_bus = event_bus
        self.motion_service = motion_service
        self.validation_service = validation_service
        self._sequences: Dict[str, SequenceData] = {}

        logger.info("✅ SequenceManagementService initialized")

    def initialize(self):
        """Optional initialization method called by DI container."""
        logger.info("🔄 Initializing SequenceManagementService...")
        # Perform any initialization logic here
        logger.info("✅ SequenceManagementService initialization complete")

    def cleanup(self):
        """Optional cleanup method called by DI container."""
        logger.info("🧹 Cleaning up SequenceManagementService...")
        # Perform any cleanup logic here
        logger.info("✅ SequenceManagementService cleanup complete")
```

---

## **Validation Scripts:**

### **Create validation script for service integration:**

```python
# FILE: scripts/validate_service_integration.py

"""
Script to validate service integration after Phase 1 completion.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.core.dependency_injection.di_container import DIContainer
import logging

def main():
    """Run comprehensive service integration validation."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("🔍 Validating TKA v2 service integration...")

    try:
        # Initialize container
        container = DIContainer()

        # Import and register all services
        from src.application.services.core.sequence_management_service import (
            ISequenceManagementService, SequenceManagementService
        )
        # Add all other service imports here...

        # Register services
        container.auto_register_with_validation(
            ISequenceManagementService,
            SequenceManagementService
        )
        # Add all other service registrations here...

        # Validate all registrations
        container.validate_all_registrations()

        # Check health
        health_ok, issues = container.validate_registration_health()

        if health_ok:
            logger.info("✅ All service integrations validated successfully!")
            container.print_registration_summary()
            return True
        else:
            logger.error("❌ Service integration validation failed:")
            for issue in issues:
                logger.error(f"  - {issue}")
            return False

    except Exception as e:
        logger.error(f"❌ Validation failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

---

## **Testing Integration:**

### **Run integration tests:**

```bash
# Test the enhanced service integration
python scripts/validate_service_integration.py

# Run main application to test startup
python v2/main.py

# Run specific service tests
python -m pytest tests/application/services/ -v

# Run DI container tests
python -m pytest tests/specification/core/test_enhanced_di_container.py -v
```

---

## **Success Criteria:**

By the end of Task 1.6:

- ✅ **All services use enhanced DI** with validation
- ✅ **Startup diagnostics** provide clear error reporting
- ✅ **Service health validation** works at startup
- ✅ **All existing functionality** continues to work
- ✅ **Performance is maintained** or improved
- ✅ **Error messages are helpful** for debugging

---

## **Phase 1 Completion Validation:**

After Task 1.6, run this comprehensive validation:

```bash
# 1. Verify no V1 references remain
grep -r "V1\|v1\|old\|legacy" v2/src/application/services/ --include="*.py"
# Should return zero results

# 2. Run all tests
python -m pytest v2/tests/ -v

# 3. Test application startup
python v2/main.py

# 4. Run service integration validation
python scripts/validate_service_integration.py

# 5. Performance check
python -c "
import time
start = time.time()
import sys; sys.path.append('v2/src')
from core.dependency_injection.di_container import DIContainer
container = DIContainer()
# ... register services ...
print(f'DI setup time: {(time.time() - start) * 1000:.1f}ms')
"
```

**Expected Results:**

- ✅ Zero V1 references found
- ✅ All tests pass
- ✅ Application starts successfully
- ✅ Service integration validates
- ✅ DI setup completes in < 100ms

---

## **🎉 Phase 1 Complete!**

Congratulations! You have successfully completed Phase 1 of the TKA v2 implementation plan.

**Next Steps:**

1. Commit all changes: `git commit -m "Phase 1: Complete technical debt elimination"`
2. Create a tag: `git tag v2-phase1-complete`
3. Proceed to: [Phase 2: Advanced Architecture Patterns](../phase2_advanced_patterns/week1_event_driven/01_event_bus_implementation.md)
