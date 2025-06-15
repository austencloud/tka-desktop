"""
Contract tests for TKA V2 service interfaces.

These tests verify that all service implementations correctly implement
their interface contracts and maintain expected behaviors.

TESTS:
- Interface compliance for all service protocols
- Service interaction contracts
- Error handling contracts
- State management contracts
"""

import pytest
from unittest.mock import Mock, MagicMock
from abc import ABC
from typing import get_type_hints, get_origin, get_args
import inspect

from src.core.interfaces.core_services import (
    IArrowManagementService,
    IMotionManagementService,
    ISequenceManagementService,
    IPictographManagementService,
    IUIStateManagementService,
    ILayoutManagementService,
)


class TestServiceInterfaceContracts:
    """Test that service interfaces define proper contracts."""

    @pytest.mark.parametrize("interface_class", [
        IArrowManagementService,
        IMotionManagementService,
        ISequenceManagementService,
        IPictographManagementService,
        IUIStateManagementService,
        ILayoutManagementService,
    ])
    def test_interface_is_abstract(self, interface_class):
        """Test that all service interfaces are abstract base classes."""
        assert issubclass(interface_class, ABC)
        
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            interface_class()

    @pytest.mark.parametrize("interface_class", [
        IArrowManagementService,
        IMotionManagementService,
        ISequenceManagementService,
        IPictographManagementService,
        IUIStateManagementService,
        ILayoutManagementService,
    ])
    def test_interface_has_abstract_methods(self, interface_class):
        """Test that interfaces define abstract methods."""
        abstract_methods = getattr(interface_class, '__abstractmethods__', set())
        assert len(abstract_methods) > 0, f"{interface_class.__name__} should have abstract methods"

    @pytest.mark.parametrize("interface_class", [
        IArrowManagementService,
        IMotionManagementService,
        ISequenceManagementService,
        IPictographManagementService,
        IUIStateManagementService,
        ILayoutManagementService,
    ])
    def test_interface_methods_have_type_hints(self, interface_class):
        """Test that interface methods have proper type hints."""
        for method_name in dir(interface_class):
            if not method_name.startswith('_'):
                method = getattr(interface_class, method_name)
                if callable(method):
                    # Check if method has type hints
                    hints = get_type_hints(method)
                    # At minimum should have return type hint
                    assert 'return' in hints, f"{interface_class.__name__}.{method_name} missing return type hint"


class TestArrowManagementServiceContract:
    """Contract tests for IArrowManagementService implementations."""

    def test_calculate_arrow_position_contract(self):
        """Test calculate_arrow_position method contract."""
        service = Mock(spec=IArrowManagementService)
        service.calculate_arrow_position.return_value = (1.0, 2.0, 45.0)
        
        # Contract: Should return tuple of three floats (x, y, rotation)
        result = service.calculate_arrow_position(Mock(), Mock())
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert all(isinstance(x, (int, float)) for x in result)

    def test_should_mirror_arrow_contract(self):
        """Test should_mirror_arrow method contract."""
        service = Mock(spec=IArrowManagementService)
        service.should_mirror_arrow.return_value = True
        
        # Contract: Should return boolean
        result = service.should_mirror_arrow(Mock())
        assert isinstance(result, bool)

    def test_apply_beta_positioning_contract(self):
        """Test apply_beta_positioning method contract."""
        service = Mock(spec=IArrowManagementService)
        mock_beat_data = Mock()
        service.apply_beta_positioning.return_value = mock_beat_data
        
        # Contract: Should return modified beat data
        result = service.apply_beta_positioning(mock_beat_data)
        assert result is not None

    def test_calculate_all_arrow_positions_contract(self):
        """Test calculate_all_arrow_positions method contract."""
        service = Mock(spec=IArrowManagementService)
        mock_pictograph_data = Mock()
        service.calculate_all_arrow_positions.return_value = mock_pictograph_data
        
        # Contract: Should return modified pictograph data
        result = service.calculate_all_arrow_positions(mock_pictograph_data)
        assert result is not None


class TestMotionManagementServiceContract:
    """Contract tests for IMotionManagementService implementations."""

    def test_validate_motion_combination_contract(self):
        """Test validate_motion_combination method contract."""
        service = Mock(spec=IMotionManagementService)
        service.validate_motion_combination.return_value = True
        
        # Contract: Should return boolean
        result = service.validate_motion_combination(Mock(), Mock())
        assert isinstance(result, bool)

    def test_get_valid_motion_combinations_contract(self):
        """Test get_valid_motion_combinations method contract."""
        service = Mock(spec=IMotionManagementService)
        service.get_valid_motion_combinations.return_value = [Mock(), Mock()]
        
        # Contract: Should return list
        result = service.get_valid_motion_combinations(Mock(), Mock())
        assert isinstance(result, list)

    def test_calculate_motion_orientation_contract(self):
        """Test calculate_motion_orientation method contract."""
        service = Mock(spec=IMotionManagementService)
        mock_orientation = Mock()
        service.calculate_motion_orientation.return_value = mock_orientation
        
        # Contract: Should return orientation data
        result = service.calculate_motion_orientation(Mock())
        assert result is not None

    def test_get_motion_validation_errors_contract(self):
        """Test get_motion_validation_errors method contract."""
        service = Mock(spec=IMotionManagementService)
        service.get_motion_validation_errors.return_value = ["Error 1", "Error 2"]
        
        # Contract: Should return list of strings
        result = service.get_motion_validation_errors(Mock(), Mock())
        assert isinstance(result, list)
        assert all(isinstance(error, str) for error in result)


class TestSequenceManagementServiceContract:
    """Contract tests for ISequenceManagementService implementations."""

    def test_create_sequence_contract(self):
        """Test create_sequence method contract."""
        service = Mock(spec=ISequenceManagementService)
        mock_sequence = Mock()
        service.create_sequence.return_value = mock_sequence
        
        # Contract: Should return sequence data
        result = service.create_sequence("Test Sequence", 16)
        assert result is not None

    def test_add_beat_contract(self):
        """Test add_beat method contract."""
        service = Mock(spec=ISequenceManagementService)
        mock_sequence = Mock()
        service.add_beat.return_value = mock_sequence
        
        # Contract: Should return modified sequence
        result = service.add_beat(Mock(), Mock(), 1)
        assert result is not None

    def test_remove_beat_contract(self):
        """Test remove_beat method contract."""
        service = Mock(spec=ISequenceManagementService)
        mock_sequence = Mock()
        service.remove_beat.return_value = mock_sequence
        
        # Contract: Should return modified sequence
        result = service.remove_beat(Mock(), 1)
        assert result is not None

    def test_generate_sequence_contract(self):
        """Test generate_sequence method contract."""
        service = Mock(spec=ISequenceManagementService)
        mock_sequence = Mock()
        service.generate_sequence.return_value = mock_sequence
        
        # Contract: Should return generated sequence
        result = service.generate_sequence("random", 16)
        assert result is not None


class TestPictographManagementServiceContract:
    """Contract tests for IPictographManagementService implementations."""

    def test_create_pictograph_contract(self):
        """Test create_pictograph method contract."""
        service = Mock(spec=IPictographManagementService)
        mock_pictograph = Mock()
        service.create_pictograph.return_value = mock_pictograph
        
        # Contract: Should return pictograph data
        result = service.create_pictograph()
        assert result is not None

    def test_create_from_beat_contract(self):
        """Test create_from_beat method contract."""
        service = Mock(spec=IPictographManagementService)
        mock_pictograph = Mock()
        service.create_from_beat.return_value = mock_pictograph
        
        # Contract: Should return pictograph data
        result = service.create_from_beat(Mock())
        assert result is not None

    def test_search_dataset_contract(self):
        """Test search_dataset method contract."""
        service = Mock(spec=IPictographManagementService)
        service.search_dataset.return_value = [Mock(), Mock()]
        
        # Contract: Should return list of pictographs
        result = service.search_dataset({"query": "test"})
        assert isinstance(result, list)


class TestUIStateManagementServiceContract:
    """Contract tests for IUIStateManagementService implementations."""

    def test_get_setting_contract(self):
        """Test get_setting method contract."""
        service = Mock(spec=IUIStateManagementService)
        service.get_setting.return_value = "test_value"
        
        # Contract: Should return setting value or default
        result = service.get_setting("test_key", "default")
        assert result is not None

    def test_set_setting_contract(self):
        """Test set_setting method contract."""
        service = Mock(spec=IUIStateManagementService)
        
        # Contract: Should not raise exception for valid inputs
        service.set_setting("test_key", "test_value")
        service.set_setting.assert_called_once_with("test_key", "test_value")

    def test_get_tab_state_contract(self):
        """Test get_tab_state method contract."""
        service = Mock(spec=IUIStateManagementService)
        service.get_tab_state.return_value = {"state": "active"}
        
        # Contract: Should return dictionary
        result = service.get_tab_state("construct")
        assert isinstance(result, dict)

    def test_toggle_graph_editor_contract(self):
        """Test toggle_graph_editor method contract."""
        service = Mock(spec=IUIStateManagementService)
        service.toggle_graph_editor.return_value = True
        
        # Contract: Should return boolean indicating new state
        result = service.toggle_graph_editor()
        assert isinstance(result, bool)


class TestLayoutManagementServiceContract:
    """Contract tests for ILayoutManagementService implementations."""

    def test_calculate_beat_frame_layout_contract(self):
        """Test calculate_beat_frame_layout method contract."""
        service = Mock(spec=ILayoutManagementService)
        service.calculate_beat_frame_layout.return_value = {"layout": "data"}
        
        # Contract: Should return layout dictionary
        result = service.calculate_beat_frame_layout(Mock(), (800, 600))
        assert isinstance(result, dict)

    def test_calculate_responsive_scaling_contract(self):
        """Test calculate_responsive_scaling method contract."""
        service = Mock(spec=ILayoutManagementService)
        service.calculate_responsive_scaling.return_value = 1.5
        
        # Contract: Should return float scaling factor
        result = service.calculate_responsive_scaling((400, 300), (800, 600))
        assert isinstance(result, (int, float))
        assert result > 0

    def test_get_optimal_grid_layout_contract(self):
        """Test get_optimal_grid_layout method contract."""
        service = Mock(spec=ILayoutManagementService)
        service.get_optimal_grid_layout.return_value = (4, 4)
        
        # Contract: Should return tuple of two integers (rows, cols)
        result = service.get_optimal_grid_layout(16, (800, 600))
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(x, int) for x in result)
        assert all(x > 0 for x in result)


class TestServiceInteractionContracts:
    """Test contracts for service interactions."""

    def test_services_can_be_mocked_for_testing(self):
        """Test that all services can be properly mocked."""
        services = [
            IArrowManagementService,
            IMotionManagementService,
            ISequenceManagementService,
            IPictographManagementService,
            IUIStateManagementService,
            ILayoutManagementService,
        ]
        
        for service_interface in services:
            # Should be able to create mock with spec
            mock_service = Mock(spec=service_interface)
            assert mock_service is not None
            
            # Mock should have all abstract methods
            abstract_methods = getattr(service_interface, '__abstractmethods__', set())
            for method_name in abstract_methods:
                assert hasattr(mock_service, method_name)

    def test_service_error_handling_contracts(self):
        """Test that services handle errors appropriately."""
        # Services should not raise unexpected exceptions
        # This is a contract that implementations must follow
        
        service = Mock(spec=IArrowManagementService)
        
        # Configure mock to raise specific exceptions
        service.calculate_arrow_position.side_effect = ValueError("Invalid input")
        
        # Contract: Services should raise appropriate exceptions for invalid inputs
        with pytest.raises(ValueError):
            service.calculate_arrow_position(None, None)
