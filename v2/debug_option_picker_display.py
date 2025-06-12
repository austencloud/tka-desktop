#!/usr/bin/env python3
"""
Debug Option Picker Display Issue

This script traces the exact issue in the option picker visual pipeline
to identify why motion combinations are generated but not visually rendered.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


class OptionPickerDebugWindow(QMainWindow):
    """Debug window for option picker display issues"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐛 Option Picker Display Debug")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Debug button
        debug_btn = QPushButton("🔍 Debug Option Picker Display")
        debug_btn.clicked.connect(self.debug_display_pipeline)
        layout.addWidget(debug_btn)
        
        # Create the construct tab widget
        self.construct_tab = ConstructTabWidget(self.container, parent=self)
        layout.addWidget(self.construct_tab)
        
        # Set up debugging after a short delay
        QTimer.singleShot(1000, self.start_debugging)
        
    def start_debugging(self):
        """Start the debugging process"""
        print("🐛 Option Picker Display Debug Started")
        print("=" * 60)
        
        # Trigger start position selection to populate option picker
        print("\n1️⃣ Triggering start position selection...")
        self.construct_tab._handle_start_position_selected("alpha1_alpha1")
        
        # Debug after a short delay to allow processing
        QTimer.singleShot(1000, self.debug_display_pipeline)
        
    def debug_display_pipeline(self):
        """Debug the display pipeline step by step"""
        print("\n🔍 DEBUGGING OPTION PICKER DISPLAY PIPELINE")
        print("-" * 60)
        
        option_picker = self.construct_tab.option_picker
        
        # Step 1: Check if option picker exists and has data
        print(f"\n1️⃣ Option Picker Data Check:")
        if option_picker:
            beat_options = getattr(option_picker, '_beat_options', [])
            print(f"   ✅ Option picker exists")
            print(f"   📊 Beat options count: {len(beat_options)}")
            
            if len(beat_options) > 0:
                print(f"   📝 Sample beat letters: {[beat.letter for beat in beat_options[:5]]}")
                
                # Check first beat data structure
                first_beat = beat_options[0]
                print(f"   🔍 First beat details:")
                print(f"      Letter: {first_beat.letter}")
                print(f"      Blue motion: {first_beat.blue_motion.motion_type if first_beat.blue_motion else 'None'}")
                print(f"      Red motion: {first_beat.red_motion.motion_type if first_beat.red_motion else 'None'}")
            else:
                print("   ❌ No beat options found")
                return
        else:
            print("   ❌ Option picker not found")
            return
            
        # Step 2: Check sections
        print(f"\n2️⃣ Section Structure Check:")
        sections = getattr(option_picker, '_sections', {})
        print(f"   📊 Sections count: {len(sections)}")
        print(f"   📝 Section types: {list(sections.keys())}")
        
        for section_type, section in sections.items():
            pictographs = getattr(section, 'pictographs', [])
            print(f"   📂 {section_type}: {len(pictographs)} pictographs")
            
            # Check if section is visible
            if hasattr(section, 'pictograph_container'):
                container = section.pictograph_container
                is_visible = container.isVisible()
                print(f"      👁️ Container visible: {is_visible}")
                print(f"      📏 Container size: {container.size().width()}x{container.size().height()}")
                
        # Step 3: Check letter type classification
        print(f"\n3️⃣ Letter Type Classification Check:")
        from src.presentation.components.option_picker.letter_types import LetterType
        
        for beat in beat_options[:5]:
            letter_type = LetterType.get_letter_type(beat.letter)
            print(f"   📝 Letter '{beat.letter}' → Type '{letter_type}'")
            
            if letter_type in sections:
                print(f"      ✅ Section exists for type '{letter_type}'")
            else:
                print(f"      ❌ No section for type '{letter_type}'")
                
        # Step 4: Check ClickablePictographFrame creation
        print(f"\n4️⃣ ClickablePictographFrame Creation Check:")
        
        # Manually create a frame to test
        if len(beat_options) > 0:
            test_beat = beat_options[0]
            try:
                from src.presentation.components.option_picker.clickable_pictograph_frame import ClickablePictographFrame
                
                print(f"   🔧 Creating test frame for beat '{test_beat.letter}'...")
                test_frame = ClickablePictographFrame(test_beat)
                
                print(f"   ✅ Frame created successfully")
                print(f"   📏 Frame size: {test_frame.size().width()}x{test_frame.size().height()}")
                print(f"   👁️ Frame visible: {test_frame.isVisible()}")
                
                # Check pictograph component
                if hasattr(test_frame, 'pictograph_component'):
                    comp = test_frame.pictograph_component
                    print(f"   🖼️ Pictograph component exists: {comp is not None}")
                    if comp:
                        print(f"   📏 Component size: {comp.size().width()}x{comp.size().height()}")
                        print(f"   👁️ Component visible: {comp.isVisible()}")
                        
                        # Check scene
                        if hasattr(comp, 'scene') and comp.scene:
                            scene = comp.scene
                            print(f"   🎬 Scene exists: {scene is not None}")
                            print(f"   📊 Scene items count: {len(scene.items())}")
                        else:
                            print(f"   ❌ No scene in pictograph component")
                else:
                    print(f"   ❌ No pictograph component in frame")
                    
            except Exception as e:
                print(f"   ❌ Error creating frame: {e}")
                
        # Step 5: Check widget hierarchy and layout
        print(f"\n5️⃣ Widget Hierarchy Check:")
        
        if hasattr(option_picker, 'widget') and option_picker.widget:
            widget = option_picker.widget
            print(f"   🏗️ Main widget exists: {widget is not None}")
            print(f"   👁️ Main widget visible: {widget.isVisible()}")
            print(f"   📏 Main widget size: {widget.size().width()}x{widget.size().height()}")
            
            # Check sections container
            if hasattr(option_picker, 'sections_container'):
                container = option_picker.sections_container
                print(f"   📦 Sections container exists: {container is not None}")
                if container:
                    print(f"   👁️ Sections container visible: {container.isVisible()}")
                    print(f"   📏 Sections container size: {container.size().width()}x{container.size().height()}")
                    print(f"   👶 Child count: {len(container.children())}")
        else:
            print(f"   ❌ No main widget found")
            
        print(f"\n🎯 Debug Complete!")


def main():
    """Run the option picker debug"""
    print("🐛 Starting Option Picker Display Debug...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Option Picker Display Debug")
    
    # Create and show debug window
    window = OptionPickerDebugWindow()
    window.show()
    
    print("🐛 Debug window created")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
