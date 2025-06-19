#!/usr/bin/env python3
"""
Test graph editor import to verify the project_root fix
"""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

print("Testing graph editor import fix...")

try:
    print("1. Testing graph editor __init__ import...")
    from presentation.components.workbench.graph_editor import __init__
    print("   ✅ Graph editor __init__ imported successfully")
    
    print("2. Testing graph editor module import...")
    from presentation.components.workbench.graph_editor.graph_editor import GraphEditor
    print("   ✅ GraphEditor class imported successfully")
    
    print("3. Testing graph section import...")
    from presentation.components.workbench.graph_section import WorkbenchGraphSection
    print("   ✅ WorkbenchGraphSection imported successfully")
    
    print("\n🎉 Graph editor import test PASSED!")
    print("The project_root import issue has been fixed.")
    
except Exception as e:
    print(f"\n❌ Graph editor import test FAILED: {e}")
    import traceback
    traceback.print_exc()
