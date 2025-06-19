#!/usr/bin/env python3
"""
Debug script to isolate import issues causing Windows fatal exceptions.
"""

import sys
import traceback
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_import(module_name, description):
    """Test importing a module and report results."""
    print(f"\n🔍 Testing {description}...")
    try:
        exec(f"import {module_name}")
        print(f"✅ {description} imported successfully")
        return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Test imports step by step to isolate the issue."""
    print("🚀 Import Debug Test")
    print("=" * 50)
    
    # Test basic imports first
    test_import("domain.models.core_models", "Core Models")
    test_import("domain.models.pictograph_models", "Pictograph Models")
    test_import("core.events", "Event System")
    
    # Test service dependencies
    test_import("application.services.data.pictograph_analysis_service", "Pictograph Analysis Service")
    test_import("application.services.positioning.placement_key_service", "Placement Key Service")
    test_import("application.services.positioning.default_placement_service", "Default Placement Service")
    test_import("application.services.positioning.dash_location_service", "Dash Location Service")
    
    # Test the problematic service
    test_import("application.services.positioning.arrow_management_service", "Arrow Management Service")
    
    print("\n🎯 Import test complete!")

if __name__ == "__main__":
    main()
