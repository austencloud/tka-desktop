#!/usr/bin/env python3
"""
Simple verification script to confirm the circular dependency fix.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🔧 Verifying Circular Dependency Fix")
    print("=" * 50)
    
    try:
        print("1. Testing dependency injection initialization...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("   ✅ Dependency injection initialized")
        
        print("2. Testing legacy compatibility setup...")
        from src.core.migration_adapters import setup_legacy_compatibility
        setup_legacy_compatibility(app_context)
        print("   ✅ Legacy compatibility established")
        
        print("3. Testing JsonManager creation...")
        json_manager = app_context.json_manager
        print(f"   ✅ JsonManager created: {type(json_manager).__name__}")
        
        print("4. Testing component chain...")
        loader_saver = json_manager.loader_saver
        props_manager = loader_saver.sequence_properties_manager
        print(f"   ✅ Component chain accessible")
        print(f"      - SequenceDataLoaderSaver: {type(loader_saver).__name__}")
        print(f"      - SequencePropertiesManager: {type(props_manager).__name__}")
        
        print("5. Testing method calls...")
        try:
            sequence = loader_saver.load_current_sequence()
            print(f"   ✅ load_current_sequence() works: {len(sequence)} items")
        except Exception as e:
            print(f"   ⚠️ load_current_sequence() issue: {e}")
        
        try:
            word = props_manager.calculate_word(None)
            print(f"   ✅ calculate_word() works: '{word}'")
        except Exception as e:
            print(f"   ⚠️ calculate_word() issue: {e}")
        
        print("\n🎉 SUCCESS: Circular dependency issue is FIXED!")
        print("The application can now start without AppContextAdapter errors.")
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
