#!/usr/bin/env python3
"""
Production API Startup Script for TKA Desktop
Starts the production-ready FastAPI server with proper configuration.
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Start the TKA Desktop Production API."""
    print("🚀 Starting TKA Desktop Production API")
    print("=" * 50)
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Add src to Python path
    src_path = script_dir / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    print(f"📁 Working directory: {script_dir}")
    print(f"📦 Python path includes: {src_path}")
    
    # Check if uvicorn is available
    try:
        import uvicorn
        print("✅ Uvicorn is available")
    except ImportError:
        print("❌ Uvicorn not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn[standard]"], check=True)
        print("✅ Uvicorn installed successfully")
    
    # Check if FastAPI is available
    try:
        import fastapi
        print("✅ FastAPI is available")
    except ImportError:
        print("❌ FastAPI not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi"], check=True)
        print("✅ FastAPI installed successfully")
    
    # Start the API server
    print("\n🌐 Starting Production API Server...")
    print("📋 Configuration:")
    print("  - Host: 0.0.0.0 (all interfaces)")
    print("  - Port: 8000")
    print("  - Reload: Enabled (development mode)")
    print("  - Workers: 1")
    
    print("\n📚 Documentation URLs:")
    print("  - Interactive Docs: http://localhost:8000/api/docs")
    print("  - ReDoc: http://localhost:8000/api/redoc")
    print("  - OpenAPI Schema: http://localhost:8000/api/openapi.json")
    
    print("\n🏥 Health Check URLs:")
    print("  - Health: http://localhost:8000/api/health")
    print("  - Status: http://localhost:8000/api/status")
    print("  - Performance: http://localhost:8000/api/performance")
    
    print("\n🎮 Starting server... (Press Ctrl+C to stop)")
    print("=" * 50)
    
    try:
        # Start uvicorn server
        uvicorn.run(
            "infrastructure.api.production_api:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")
        print("\n🔧 Troubleshooting:")
        print("  1. Make sure you're in the 'modern' directory")
        print("  2. Check that all dependencies are installed")
        print("  3. Verify the src/infrastructure/api/production_api.py file exists")
        return 1
    
    print("👋 TKA Desktop Production API shutdown complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
