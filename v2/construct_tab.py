#!/usr/bin/env python3
"""
Kinetic Constructor modern - Construct Tab

The foundational Construct tab for the new modular architecture.
Self-contained widget for sequence construction with start position selection
and option picking.

FEATURES:
- Start position selection with visual feedback
- Option picker for sequence building
- Sequence workbench for editing and modification
- Modern dependency injection architecture
- Zero global state access

USAGE:
    python construct_tab.py  # Run construct tab demo

INTEGRATION:
    from construct_tab import ConstructTabWidget
    construct = ConstructTabWidget(container)
    main_layout.addWidget(construct)
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

v2_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src_path))

from src.presentation.demos.construct_tab_demo import ConstructTabDemo


def main():
    print("🔧 Starting Kinetic Constructor modern - Construct Tab")
    print("=" * 50)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = ConstructTabDemo()
    window.show()

    print("✅ Construct tab demo started!")
    print("📋 Features:")
    print("   • Modern legacy construct tab layout")
    print("   • Sequence workbench on the left")
    print("   • Start position + option pickers on the right")
    print("   • Zero global state access")
    print("   • Clean component communication")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
