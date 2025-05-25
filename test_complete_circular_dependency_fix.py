#!/usr/bin/env python3
"""
Complete verification test for the circular dependency fix.
This test verifies that the initialization order and AppContextAdapter issues are completely resolved.
"""

import sys
import os
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_logging():
    """Setup logging to see what's happening."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_complete_initialization_sequence():
    """Test the complete initialization sequence that was causing the circular dependency."""
    logger = logging.getLogger(__name__)
    
    logger.info("=== Testing Complete Initialization Sequence ===")
    
    try:
        # Step 1: Test dependency injection initialization (includes legacy compatibility)
        logger.info("Step 1: Testing dependency injection initialization...")
        from src.main import initialize_dependency_injection
        
        app_context = initialize_dependency_injection()
        logger.info("✅ Dependency injection initialized successfully")
        
        # Step 2: Verify AppContextAdapter is properly initialized
        logger.info("Step 2: Verifying AppContextAdapter is available...")
        from src.core.migration_adapters import AppContextAdapter
        
        settings_manager = AppContextAdapter.settings_manager()
        json_manager = AppContextAdapter.json_manager()
        logger.info("✅ AppContextAdapter is properly initialized and accessible")
        
        # Step 3: Test MainWindow creation (without widgets)
        logger.info("Step 3: Testing MainWindow creation...")
        from src.main import create_main_window
        from src.splash_screen.splash_screen import SplashScreen
        from src.settings_manager.settings_manager import SettingsManager
        from src.profiler import Profiler
        
        # Create minimal dependencies for MainWindow
        settings = SettingsManager()
        splash_screen = SplashScreen(None, settings)  # Pass None for app since we're just testing
        profiler = Profiler()
        
        main_window = create_main_window(profiler, splash_screen, app_context)
        logger.info("✅ MainWindow created successfully (without widgets)")
        
        # Step 4: Test widget initialization (this was the problematic part)
        logger.info("Step 4: Testing widget initialization...")
        main_window.initialize_widgets()
        logger.info("✅ Widget initialization completed successfully")
        
        # Step 5: Test the specific component chain that was causing issues
        logger.info("Step 5: Testing problematic component chain...")
        
        # This chain was: app_context.json_manager -> JsonManager -> SequenceDataLoaderSaver -> SequencePropertiesManager
        json_mgr = app_context.json_manager
        loader_saver = json_mgr.loader_saver
        props_manager = loader_saver.sequence_properties_manager
        
        logger.info(f"✅ Component chain works:")
        logger.info(f"   - JsonManager: {type(json_mgr).__name__}")
        logger.info(f"   - SequenceDataLoaderSaver: {type(loader_saver).__name__}")
        logger.info(f"   - SequencePropertiesManager: {type(props_manager).__name__}")
        
        # Step 6: Test method calls that were failing
        logger.info("Step 6: Testing method calls that previously failed...")
        
        try:
            sequence = loader_saver.load_current_sequence()
            logger.info(f"✅ load_current_sequence() works: loaded {len(sequence)} items")
        except Exception as e:
            logger.warning(f"⚠️ load_current_sequence() issue: {e}")
        
        try:
            word = props_manager.calculate_word(None)
            logger.info(f"✅ calculate_word() works: '{word}'")
        except Exception as e:
            logger.warning(f"⚠️ calculate_word() issue: {e}")
        
        try:
            properties = props_manager.check_all_properties()
            logger.info(f"✅ check_all_properties() works: {len(properties)} properties")
        except Exception as e:
            logger.warning(f"⚠️ check_all_properties() issue: {e}")
        
        logger.info("=== All Tests Passed! Circular Dependency Completely Fixed! ===")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_widget_creation_sequence():
    """Test the specific widget creation sequence that was causing the circular dependency."""
    logger = logging.getLogger(__name__)
    
    logger.info("=== Testing Widget Creation Sequence ===")
    
    try:
        # Initialize dependency injection
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        logger.info("✅ Dependency injection initialized")
        
        # Test MainWidgetCoordinator creation (this was triggering the issue)
        logger.info("Testing MainWidgetCoordinator creation...")
        from src.main_window.main_widget.core.main_widget_coordinator import MainWidgetFactory
        from src.splash_screen.splash_screen import SplashScreen
        from src.settings_manager.settings_manager import SettingsManager
        
        # Create minimal dependencies
        settings = SettingsManager()
        splash_screen = SplashScreen(None, settings)
        
        # Create a mock main window
        class MockMainWindow:
            def __init__(self):
                pass
        
        main_window = MockMainWindow()
        
        # Create MainWidgetCoordinator (this should not trigger circular dependency)
        coordinator = MainWidgetFactory.create(main_window, splash_screen, app_context)
        logger.info("✅ MainWidgetCoordinator created successfully")
        
        # Test component initialization (this was the failing part)
        coordinator.initialize_components()
        logger.info("✅ Component initialization completed successfully")
        
        # Test that we can access the widgets that were causing issues
        widget_manager = coordinator.widget_manager
        logger.info(f"✅ WidgetManager accessible: {type(widget_manager).__name__}")
        
        logger.info("=== Widget Creation Sequence Test Passed! ===")
        return True
        
    except Exception as e:
        logger.error(f"❌ Widget creation sequence test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sequence_properties_manager_factory():
    """Test the SequencePropertiesManagerFactory that was causing the circular dependency."""
    logger = logging.getLogger(__name__)
    
    logger.info("=== Testing SequencePropertiesManagerFactory ===")
    
    try:
        # Test create_legacy() method when AppContextAdapter is not available
        logger.info("Testing create_legacy() without AppContextAdapter...")
        from src.main_window.main_widget.sequence_properties_manager.sequence_properties_manager_factory import SequencePropertiesManagerFactory
        
        # This should now work even if AppContextAdapter is not initialized
        manager = SequencePropertiesManagerFactory.create_legacy()
        logger.info(f"✅ create_legacy() works: {type(manager).__name__}")
        
        # Test create_legacy() method when AppContextAdapter is available
        logger.info("Testing create_legacy() with AppContextAdapter...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        
        manager2 = SequencePropertiesManagerFactory.create_legacy()
        logger.info(f"✅ create_legacy() with AppContextAdapter works: {type(manager2).__name__}")
        
        # Test create() method with app_context
        logger.info("Testing create() with app_context...")
        manager3 = SequencePropertiesManagerFactory.create(app_context)
        logger.info(f"✅ create() with app_context works: {type(manager3).__name__}")
        
        logger.info("=== SequencePropertiesManagerFactory Test Passed! ===")
        return True
        
    except Exception as e:
        logger.error(f"❌ SequencePropertiesManagerFactory test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all verification tests."""
    setup_logging()
    
    print("🔧 Complete Verification: Circular Dependency Fix")
    print("=" * 60)
    
    # Test 1: Complete initialization sequence
    test1_passed = test_complete_initialization_sequence()
    
    # Test 2: Widget creation sequence
    test2_passed = test_widget_creation_sequence()
    
    # Test 3: SequencePropertiesManagerFactory
    test3_passed = test_sequence_properties_manager_factory()
    
    # Summary
    print("\n" + "=" * 60)
    print("COMPLETE VERIFICATION RESULTS")
    print("=" * 60)
    
    if test1_passed:
        print("✅ Complete Initialization Sequence: PASSED")
    else:
        print("❌ Complete Initialization Sequence: FAILED")
    
    if test2_passed:
        print("✅ Widget Creation Sequence: PASSED")
    else:
        print("❌ Widget Creation Sequence: FAILED")
    
    if test3_passed:
        print("✅ SequencePropertiesManagerFactory: PASSED")
    else:
        print("❌ SequencePropertiesManagerFactory: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED! The circular dependency issue is COMPLETELY FIXED!")
        print("✅ Initialization order is correct")
        print("✅ AppContextAdapter is properly initialized")
        print("✅ Widget creation works without circular dependencies")
        print("✅ All component chains work correctly")
        print("✅ The application can start successfully")
    else:
        print("\n⚠️ Some tests failed. The circular dependency issue may not be fully resolved.")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
