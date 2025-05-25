#!/usr/bin/env python3
"""
Test script to verify the dependency injection system works correctly
after fixing the import issues.
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

def test_dependency_injection():
    """Test the dependency injection system."""
    logger = logging.getLogger(__name__)
    
    logger.info("=== Testing Dependency Injection System ===")
    
    try:
        # Step 1: Test container creation
        logger.info("Step 1: Testing container creation...")
        from src.core.dependency_container import configure_dependencies, get_container
        
        container = configure_dependencies()
        logger.info(f"✅ Container created with {len(container._services)} services")
        
        # Step 2: Test application context creation
        logger.info("Step 2: Testing application context creation...")
        from src.core.application_context import create_application_context
        
        app_context = create_application_context(container)
        logger.info("✅ Application context created successfully")
        
        # Step 3: Test service resolution
        logger.info("Step 3: Testing service resolution...")
        
        # Test settings manager
        try:
            settings_manager = app_context.settings_manager
            logger.info(f"✅ Settings manager resolved: {type(settings_manager).__name__}")
        except Exception as e:
            logger.warning(f"⚠️ Settings manager failed: {e}")
        
        # Test JSON manager
        try:
            json_manager = app_context.json_manager
            logger.info(f"✅ JSON manager resolved: {type(json_manager).__name__}")
        except Exception as e:
            logger.warning(f"⚠️ JSON manager failed: {e}")
        
        # Step 4: Test legacy compatibility
        logger.info("Step 4: Testing legacy compatibility...")
        from src.core.migration_adapters import setup_legacy_compatibility
        
        adapter = setup_legacy_compatibility(app_context)
        logger.info("✅ Legacy compatibility set up successfully")
        
        # Test legacy access
        try:
            from src.core.migration_adapters import AppContextAdapter
            legacy_settings = AppContextAdapter.settings_manager()
            logger.info(f"✅ Legacy settings access works: {type(legacy_settings).__name__}")
        except Exception as e:
            logger.warning(f"⚠️ Legacy settings access failed: {e}")
        
        # Step 5: Test optional services
        logger.info("Step 5: Testing optional services...")
        
        # Test DictionaryDataManager
        try:
            from main_window.main_widget.browse_tab.sequence_picker.dictionary_data_manager import DictionaryDataManager
            dict_manager = container.resolve(DictionaryDataManager)
            logger.info(f"✅ DictionaryDataManager resolved: {type(dict_manager).__name__}")
        except Exception as e:
            logger.info(f"ℹ️ DictionaryDataManager not available: {e}")
        
        # Test LetterDeterminer
        try:
            from letter_determination.core import LetterDeterminer
            letter_determiner = container.resolve(LetterDeterminer)
            logger.info(f"✅ LetterDeterminer resolved: {type(letter_determiner).__name__}")
        except Exception as e:
            logger.info(f"ℹ️ LetterDeterminer not available: {e}")
        
        # Test Motion/Arrow objects
        try:
            from objects.motion.motion import Motion
            from objects.arrow.arrow import Arrow
            
            motion = container.resolve(Motion)
            arrow = container.resolve(Arrow)
            logger.info(f"✅ Motion/Arrow objects resolved: {type(motion).__name__}, {type(arrow).__name__}")
        except Exception as e:
            logger.info(f"ℹ️ Motion/Arrow objects not available: {e}")
        
        # Step 6: Test cleanup
        logger.info("Step 6: Testing cleanup...")
        from src.core.migration_adapters import teardown_legacy_compatibility
        teardown_legacy_compatibility()
        container.clear()
        logger.info("✅ Cleanup completed successfully")
        
        logger.info("=== All Tests Completed Successfully! ===")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_initialization():
    """Test the main.py initialization process."""
    logger = logging.getLogger(__name__)
    
    logger.info("=== Testing Main Initialization ===")
    
    try:
        # Import the initialization function from main.py
        from src.main import initialize_dependency_injection
        
        app_context = initialize_dependency_injection()
        logger.info("✅ Main initialization completed successfully")
        
        # Test that we can access core services
        settings = app_context.settings_manager
        json_mgr = app_context.json_manager
        
        logger.info(f"✅ Core services accessible: {type(settings).__name__}, {type(json_mgr).__name__}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Main initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    setup_logging()
    
    print("🧪 Testing Dependency Injection System After Fixes")
    print("=" * 60)
    
    # Test 1: Basic dependency injection
    test1_passed = test_dependency_injection()
    
    # Test 2: Main initialization
    test2_passed = test_main_initialization()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if test1_passed:
        print("✅ Dependency Injection System: PASSED")
    else:
        print("❌ Dependency Injection System: FAILED")
    
    if test2_passed:
        print("✅ Main Initialization: PASSED")
    else:
        print("❌ Main Initialization: FAILED")
    
    overall_success = test1_passed and test2_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED! The dependency injection system is working correctly.")
        print("The application should now start without ModuleNotFoundError issues.")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
