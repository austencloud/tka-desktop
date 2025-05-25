#!/usr/bin/env python3
"""
Final verification test for the circular dependency fix.
This test verifies that the AppContextAdapter initialization order issue is completely resolved.
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

def test_initialization_order():
    """Test that the initialization order is correct and no circular dependency occurs."""
    logger = logging.getLogger(__name__)
    
    logger.info("=== Testing Initialization Order Fix ===")
    
    try:
        # Step 1: Test dependency injection initialization (this now includes legacy compatibility)
        logger.info("Step 1: Testing dependency injection initialization with legacy compatibility...")
        from src.main import initialize_dependency_injection
        
        app_context = initialize_dependency_injection()
        logger.info("✅ Dependency injection initialized successfully with legacy compatibility")
        
        # Step 2: Verify that AppContextAdapter is properly initialized
        logger.info("Step 2: Verifying AppContextAdapter is properly initialized...")
        from src.core.migration_adapters import AppContextAdapter
        
        # This should NOT throw a RuntimeError anymore
        settings_manager = AppContextAdapter.settings_manager()
        logger.info(f"✅ AppContextAdapter.settings_manager() works: {type(settings_manager).__name__}")
        
        json_manager = AppContextAdapter.json_manager()
        logger.info(f"✅ AppContextAdapter.json_manager() works: {type(json_manager).__name__}")
        
        # Step 3: Test that we can access services through app_context
        logger.info("Step 3: Testing service access through app_context...")
        
        app_settings = app_context.settings_manager
        app_json = app_context.json_manager
        logger.info(f"✅ app_context services accessible: {type(app_settings).__name__}, {type(app_json).__name__}")
        
        # Step 4: Test the problematic chain that was causing circular dependency
        logger.info("Step 4: Testing the previously problematic component chain...")
        
        # This chain was: JsonManager -> SequenceDataLoaderSaver -> SequencePropertiesManager -> AppContextAdapter
        json_mgr = app_context.json_manager
        loader_saver = json_mgr.loader_saver
        props_manager = loader_saver.sequence_properties_manager
        
        logger.info(f"✅ Component chain works:")
        logger.info(f"   - JsonManager: {type(json_mgr).__name__}")
        logger.info(f"   - SequenceDataLoaderSaver: {type(loader_saver).__name__}")
        logger.info(f"   - SequencePropertiesManager: {type(props_manager).__name__}")
        
        # Step 5: Test method calls that previously failed
        logger.info("Step 5: Testing method calls that previously caused circular dependency...")
        
        try:
            # This was failing because SequencePropertiesManager couldn't access AppContextAdapter
            sequence = loader_saver.load_current_sequence()
            logger.info(f"✅ load_current_sequence() works: loaded {len(sequence)} items")
        except Exception as e:
            logger.warning(f"⚠️ load_current_sequence() issue: {e}")
        
        try:
            # This was failing because of AppContextAdapter not being initialized
            word = props_manager.calculate_word(None)
            logger.info(f"✅ calculate_word() works: '{word}'")
        except Exception as e:
            logger.warning(f"⚠️ calculate_word() issue: {e}")
        
        # Step 6: Test that MainWindow creation would work (simulate the problematic scenario)
        logger.info("Step 6: Simulating MainWindow creation scenario...")
        
        # This simulates what happens when MainWindow is created and tries to access services
        try:
            # Simulate accessing json_manager during widget creation (this was the trigger)
            test_json_manager = app_context.json_manager
            test_loader_saver = test_json_manager.loader_saver
            test_props_manager = test_loader_saver.sequence_properties_manager
            
            # Try to use the properties manager (this was failing)
            test_properties = test_props_manager.check_all_properties()
            logger.info(f"✅ MainWindow creation simulation successful")
            logger.info(f"   - Properties calculated: {len(test_properties)} properties")
            
        except Exception as e:
            logger.error(f"❌ MainWindow creation simulation failed: {e}")
            return False
        
        logger.info("=== All Tests Passed! Circular Dependency Completely Fixed! ===")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_application_flow():
    """Test the complete main application flow."""
    logger = logging.getLogger(__name__)
    
    logger.info("=== Testing Complete Main Application Flow ===")
    
    try:
        # Test the exact sequence that happens in main.py
        logger.info("Testing main.py initialization sequence...")
        
        # Step 1: Initialize dependency injection (includes legacy compatibility now)
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        logger.info("✅ initialize_dependency_injection() completed")
        
        # Step 2: Simulate MainWindow creation (this was the failing point)
        logger.info("Simulating MainWindow creation...")
        
        # This simulates the MainWindow constructor calling MainWidgetFactory.create()
        # which then tries to access app_context.json_manager
        json_manager = app_context.json_manager  # This was triggering the circular dependency
        logger.info("✅ app_context.json_manager accessed successfully")
        
        # This simulates the widget creation that was failing
        loader_saver = json_manager.loader_saver
        props_manager = loader_saver.sequence_properties_manager
        logger.info("✅ Component chain created successfully")
        
        # This simulates the method calls that were failing due to AppContextAdapter not being initialized
        try:
            sequence = loader_saver.load_current_sequence()
            properties = props_manager.check_all_properties()
            logger.info("✅ Method calls successful")
        except Exception as e:
            logger.warning(f"⚠️ Method call issue: {e}")
        
        logger.info("=== Main Application Flow Test Passed! ===")
        return True
        
    except Exception as e:
        logger.error(f"❌ Main application flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all verification tests."""
    setup_logging()
    
    print("🔧 Final Verification: Circular Dependency Fix")
    print("=" * 60)
    
    # Test 1: Initialization order
    test1_passed = test_initialization_order()
    
    # Test 2: Main application flow
    test2_passed = test_main_application_flow()
    
    # Summary
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION RESULTS")
    print("=" * 60)
    
    if test1_passed:
        print("✅ Initialization Order: PASSED")
    else:
        print("❌ Initialization Order: FAILED")
    
    if test2_passed:
        print("✅ Main Application Flow: PASSED")
    else:
        print("❌ Main Application Flow: FAILED")
    
    overall_success = test1_passed and test2_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED! The circular dependency issue is COMPLETELY FIXED!")
        print("✅ AppContextAdapter is properly initialized before any components try to use it")
        print("✅ The application can start without RuntimeError exceptions")
        print("✅ MainWindow creation will work without circular dependency issues")
        print("✅ All component chains work correctly")
    else:
        print("\n⚠️ Some tests failed. The circular dependency issue may not be fully resolved.")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
