#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path for imports
src_path = os.path.join(os.path.dirname(__file__), "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import and run the main application
if __name__ == "__main__":
    from src.main import main

    main()
