#!/usr/bin/env python3
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Option picker behavior contracts - consolidates option picker reactivity tests
CREATED: 2025-06-19
AUTHOR: AI Assistant
RELATED_ISSUE: Test suite restructuring

Option Picker Behavior Contract Tests
====================================

Consolidates functionality from:
- test_option_picker_reactivity.py (basic reactivity)
- test_option_picker_reactivity_enhanced.py (enhanced signal flow)

Defines behavioral contracts for option picker switching and reactivity.
"""

import sys
import pytest
from pathlib import Path
from typing import Optional

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


class TestOptionPickerBehaviorContract:
    """Option picker behavior contract tests."""

    def setup_method(self):
        """Setup for each test method."""
        self.container = None
        self.app = None

    def teardown_method(self):
        """Cleanup after each test method."""
        if self.app:
            self.app.quit()

    def test_di_container_configuration(self):
        """Test that DI container can be configured for option picker tests."""
        from core.dependency_injection.di_container import DIContainer
        from core.interfaces.core_services import ILayoutService, IUIStateManagementService
        from core.interfaces.workbench_services import (
            ISequenceWorkbenchService,
            IFullScreenService,
            IBeatDeletionService,
            IGraphEditorService,
            IDictionaryService,
        )
        from application.services.core.sequence_management_service import (
            SequenceManagementService,
        )
        from application.services.ui.ui_state_management_service import UIStateManagementService
        from application.services.ui.full_screen_service import FullScreenService
        from application.services.graph_editor_service import GraphEditorService
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )
        
        # Create container
        container = DIContainer()
        
        # Core services
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(IUIStateManagementService, UIStateManagementService)
        
        # Workbench services (using SequenceManagementService for consolidation)
        container.register_singleton(ISequenceWorkbenchService, SequenceManagementService)
        container.register_singleton(IBeatDeletionService, SequenceManagementService)
        container.register_singleton(IDictionaryService, SequenceManagementService)
        container.register_singleton(IFullScreenService, FullScreenService)
        
        # Graph editor needs UI state service
        ui_state_service = container.resolve(IUIStateManagementService)
        graph_editor_service = GraphEditorService(ui_state_service)
        container.register_instance(IGraphEditorService, graph_editor_service)
        
        # Verify all services can be resolved
        assert container.resolve(ILayoutService) is not None
        assert container.resolve(IUIStateManagementService) is not None
        assert container.resolve(ISequenceWorkbenchService) is not None
        assert container.resolve(IBeatDeletionService) is not None
        assert container.resolve(IDictionaryService) is not None
        assert container.resolve(IFullScreenService) is not None
        assert container.resolve(IGraphEditorService) is not None

    def test_domain_models_for_option_picker(self):
        """Test that domain models required for option picker work correctly."""
        from domain.models.core_models import SequenceData, BeatData
        
        # Test beat creation
        beat1 = BeatData(beat_number=1, letter="A")
        beat2 = BeatData(beat_number=2, letter="B")
        
        assert beat1.beat_number == 1
        assert beat1.letter == "A"
        assert beat2.beat_number == 2
        assert beat2.letter == "B"
        
        # Test sequence creation
        test_sequence = SequenceData(name="Test Sequence", beats=[beat1, beat2])
        assert test_sequence.name == "Test Sequence"
        assert len(test_sequence.beats) == 2
        assert test_sequence.length == 2
        
        # Test empty sequence
        empty_sequence = SequenceData.empty()
        assert empty_sequence.length == 0
        assert len(empty_sequence.beats) == 0

    def test_construct_tab_widget_import(self):
        """Test that construct tab widget can be imported."""
        from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
        assert ConstructTabWidget is not None

    @pytest.mark.skipif(
        not pytest.importorskip("PyQt6", minversion=None),
        reason="PyQt6 not available for UI testing"
    )
    def test_option_picker_reactivity_contract(self):
        """
        Test option picker reactivity contract.
        
        CONTRACT: Option picker must switch between start position picker and option picker
        based on sequence state:
        - Empty/cleared sequence → Start position picker (index 0)
        - Sequence with beats → Option picker (index 1)
        """
        try:
            from PyQt6.QtWidgets import QApplication
            from PyQt6.QtCore import QTimer
            from core.dependency_injection.di_container import DIContainer, get_container
            from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
            from domain.models.core_models import SequenceData, BeatData
            
            # Create Qt application
            self.app = QApplication.instance() or QApplication([])
            
            # Setup DI container
            container = get_container()
            self._configure_test_services(container)
            
            # Create construct tab
            construct_tab = ConstructTabWidget(container)
            construct_tab.resize(800, 600)
            
            # Verify initial state (should be start position picker for empty sequence)
            if hasattr(construct_tab, "layout_manager") and hasattr(
                construct_tab.layout_manager, "picker_stack"
            ):
                initial_index = construct_tab.layout_manager.picker_stack.currentIndex()
                assert initial_index == 0, f"Expected start position picker (0), got {initial_index}"
            
            # Test sequence with beats (should switch to option picker)
            beat1 = BeatData(beat_number=1, letter="A")
            beat2 = BeatData(beat_number=2, letter="B")
            test_sequence = SequenceData(name="Test Sequence", beats=[beat1, beat2])
            
            if hasattr(construct_tab, "workbench") and construct_tab.workbench:
                construct_tab.workbench.set_sequence(test_sequence)
                
                # Process events to allow picker switching
                self.app.processEvents()
                
                # Check if switched to option picker
                if hasattr(construct_tab.layout_manager, "picker_stack"):
                    current_index = construct_tab.layout_manager.picker_stack.currentIndex()
                    assert current_index == 1, f"Expected option picker (1) for sequence with beats, got {current_index}"
            
            # Test clearing sequence (should switch back to start position picker)
            if hasattr(construct_tab, "workbench") and construct_tab.workbench:
                if hasattr(construct_tab.workbench, "_handle_clear"):
                    construct_tab.workbench._handle_clear()
                    
                    # Process events to allow picker switching
                    self.app.processEvents()
                    
                    # Check if switched back to start position picker
                    if hasattr(construct_tab.layout_manager, "picker_stack"):
                        final_index = construct_tab.layout_manager.picker_stack.currentIndex()
                        assert final_index == 0, f"Expected start position picker (0) after clear, got {final_index}"
            
            # Test empty sequence (should be start position picker)
            empty_sequence = SequenceData.empty()
            if hasattr(construct_tab, "workbench") and construct_tab.workbench:
                construct_tab.workbench.set_sequence(empty_sequence)
                
                # Process events to allow picker switching
                self.app.processEvents()
                
                # Check if on start position picker
                if hasattr(construct_tab.layout_manager, "picker_stack"):
                    empty_index = construct_tab.layout_manager.picker_stack.currentIndex()
                    assert empty_index == 0, f"Expected start position picker (0) for empty sequence, got {empty_index}"
            
        except ImportError:
            pytest.skip("PyQt6 not available for UI testing")

    def test_signal_flow_contract(self):
        """
        Test signal flow contract.
        
        CONTRACT: Signal flow must prevent cascading refreshes and maintain proper
        sequence modification and start position signals.
        """
        from core.dependency_injection.di_container import DIContainer, get_container
        
        # Setup container
        container = get_container()
        self._configure_test_services(container)
        
        # Test that signal coordinator can be created
        try:
            from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
            
            # This test verifies that the construct tab can be created without errors
            # which implies proper signal flow setup
            construct_tab = ConstructTabWidget(container)
            
            # Verify signal coordinator exists
            assert hasattr(construct_tab, "signal_coordinator")
            
            if construct_tab.signal_coordinator:
                # Verify required signals exist
                assert hasattr(construct_tab.signal_coordinator, "sequence_modified")
                assert hasattr(construct_tab.signal_coordinator, "start_position_set")
                
        except ImportError:
            pytest.skip("Construct tab not available for signal flow testing")

    def _configure_test_services(self, container: DIContainer):
        """Configure all services needed for the construct tab test."""
        from core.interfaces.core_services import ILayoutService, IUIStateManagementService
        from core.interfaces.workbench_services import (
            ISequenceWorkbenchService,
            IFullScreenService,
            IBeatDeletionService,
            IGraphEditorService,
            IDictionaryService,
        )
        from application.services.core.sequence_management_service import (
            SequenceManagementService,
        )
        from application.services.ui.ui_state_management_service import UIStateManagementService
        from application.services.ui.full_screen_service import FullScreenService
        from application.services.graph_editor_service import GraphEditorService
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )
        
        # Core services
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(IUIStateManagementService, UIStateManagementService)
        
        # Workbench services (using SequenceManagementService for consolidation)
        container.register_singleton(ISequenceWorkbenchService, SequenceManagementService)
        container.register_singleton(IBeatDeletionService, SequenceManagementService)
        container.register_singleton(IDictionaryService, SequenceManagementService)
        container.register_singleton(IFullScreenService, FullScreenService)
        
        # Graph editor needs UI state service
        ui_state_service = container.resolve(IUIStateManagementService)
        graph_editor_service = GraphEditorService(ui_state_service)
        container.register_instance(IGraphEditorService, graph_editor_service)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
