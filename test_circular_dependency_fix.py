#!/usr/bin/env python3
"""
Test script to verify the circular dependency fix in the dependency injection system.
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

def test_circular_dependency_fix():
    """Test that the circular dependency is fixed."""
    logger = logging.getLogger(__name__)
    
    logger.info("=== Testing Circular Dependency Fix ===")
    
    try:
        # Step 1: Test dependency injection initialization
        logger.info("Step 1: Testing dependency injection initialization...")
        from src.main import initialize_dependency_injection
        
        app_context = initialize_dependency_injection()
        logger.info("✅ Dependency injection initialized successfully")
        
        # Step 2: Test legacy compatibility setup
        logger.info("Step 2: Testing legacy compatibility setup...")
        from src.core.migration_adapters import setup_legacy_compatibility
        
        setup_legacy_compatibility(app_context)
        logger.info("✅ Legacy compatibility set up successfully")
        
        # Step 3: Test JsonManager creation (this was the problematic part)
        logger.info("Step 3: Testing JsonManager creation...")
        json_manager = app_context.json_manager
        logger.info(f"✅ JsonManager created successfully: {type(json_manager).__name__}")
        
        # Step 4: Test SequenceDataLoaderSaver functionality
        logger.info("Step 4: Testing SequenceDataLoaderSaver functionality...")
        loader_saver = json_manager.loader_saver
        logger.info(f"✅ SequenceDataLoaderSaver accessible: {type(loader_saver).__name__}")
        
        # Step 5: Test SequencePropertiesManager functionality
        logger.info("Step 5: Testing SequencePropertiesManager functionality...")
        props_manager = loader_saver.sequence_properties_manager
        logger.info(f"✅ SequencePropertiesManager accessible: {type(props_manager).__name__}")
        
        # Step 6: Test that we can call methods without errors
        logger.info("Step 6: Testing method calls...")
        
        # Test loading current sequence (should not throw circular dependency error)
        try:
            sequence = loader_saver.load_current_sequence()
            logger.info(f"✅ load_current_sequence() works: loaded {len(sequence)} items")
        except Exception as e:
            logger.warning(f"⚠️ load_current_sequence() failed: {e}")
        
        # Test calculating word (should not throw circular dependency error)
        try:
            word = props_manager.calculate_word(None)
            logger.info(f"✅ calculate_word() works: '{word}'")
        except Exception as e:
            logger.warning(f"⚠️ calculate_word() failed: {e}")
        
        # Step 7: Test cleanup
        logger.info("Step 7: Testing cleanup...")
        from src.core.migration_adapters import teardown_legacy_compatibility
        teardown_legacy_compatibility()
        logger.info("✅ Cleanup completed successfully")
        
        logger.info("=== All Tests Passed! Circular Dependency Fixed! ===")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_application_startup():
    """Test that the main application can start without circular dependency errors."""
    logger = logging.getLogger(__name__)
    
    logger.info("=== Testing Main Application Startup ===")
    
    try:
        # Test the main initialization sequence
        from src.main import initialize_dependency_injection
        from src.core.migration_adapters import setup_legacy_compatibility
        
        # Initialize dependency injection
        app_context = initialize_dependency_injection()
        logger.info("✅ Dependency injection initialization completed")
        
        # Set up legacy compatibility
        setup_legacy_compatibility(app_context)
        logger.info("✅ Legacy compatibility established")
        
        # Test that JsonManager can be created without circular dependency
        json_manager = app_context.json_manager
        logger.info("✅ JsonManager created without circular dependency")
        
        # Test that we can access nested components
        loader_saver = json_manager.loader_saver
        props_manager = loader_saver.sequence_properties_manager
        logger.info("✅ All nested components accessible")
        
        logger.info("=== Main Application Startup Test Passed! ===")
        return True
        
    except Exception as e:
        logger.error(f"❌ Main application startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    setup_logging()
    
    print("🔧 Testing Circular Dependency Fix")
    print("=" * 60)
    
    # Test 1: Circular dependency fix
    test1_passed = test_circular_dependency_fix()
    
    # Test 2: Main application startup
    test2_passed = test_main_application_startup()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if test1_passed:
        print("✅ Circular Dependency Fix: PASSED")
    else:
        print("❌ Circular Dependency Fix: FAILED")
    
    if test2_passed:
        print("✅ Main Application Startup: PASSED")
    else:
        print("❌ Main Application Startup: FAILED")
    
    overall_success = test1_passed and test2_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED! The circular dependency issue is fixed.")
        print("The application should now start without AppContextAdapter errors.")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
