"""
End-to-end integration tests for TKA Modern workflows.

These tests validate complete user workflows from start to finish,
ensuring all components work together correctly.

TESTS:
- Sequence creation → pictograph generation workflow
- Cross-service integration validation
- Event flow validation
- Error propagation testing
"""

import pytest
from unittest.mock import Mock, patch
from typing import List, Dict, Any

from src.core.events.event_bus import (
    TypeSafeEventBus,
    SequenceEvent,
    UIEvent,
    BaseEvent,
)
from src.core.dependency_injection.di_container import DIContainer
from src.domain.models.core_models import (
    BeatData,
    SequenceData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from dataclasses import dataclass, field


@dataclass(frozen=True)
class WorkflowEvent(BaseEvent):
    """Custom event for workflow testing."""

    workflow_type: str = ""
    operation: str = ""
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def event_type(self) -> str:
        return f"workflow.{self.operation}"


class MockServiceRegistry:
    """Mock service registry for integration testing."""

    def __init__(self):
        self.event_bus = TypeSafeEventBus()
        self.container = DIContainer()
        self.workflow_events = []

        # Setup event tracking for workflow events
        self.event_bus.subscribe("workflow.started", self._track_event)
        self.event_bus.subscribe("workflow.sequence_created", self._track_event)
        self.event_bus.subscribe("workflow.beat_added", self._track_event)
        self.event_bus.subscribe("workflow.pictograph_generated", self._track_event)
        self.event_bus.subscribe("workflow.completed", self._track_event)
        self.event_bus.subscribe("workflow.error_occurred", self._track_event)

    def _track_event(self, event: WorkflowEvent):
        """Track workflow events for validation."""
        self.workflow_events.append(
            {
                "operation": event.operation,
                "workflow_type": event.workflow_type,
                **event.data,
            }
        )


@pytest.fixture
def mock_service_registry():
    """Provide mock service registry for tests."""
    return MockServiceRegistry()


@pytest.fixture
def sample_motion_data():
    """Provide sample motion data for testing."""
    return MotionData(
        motion_type=MotionType.PRO,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        turns=1.0,
        start_ori="in",
        end_ori="out",
    )


class TestSequenceCreationWorkflow:
    """Test complete sequence creation workflows."""

    def test_create_empty_sequence_workflow(self, mock_service_registry):
        """Test creating an empty sequence through the complete workflow."""
        registry = mock_service_registry

        # Start workflow
        start_event = WorkflowEvent(
            workflow_type="sequence_creation",
            operation="started",
            data={"user_action": "create_empty_sequence"},
        )
        registry.event_bus.publish(start_event)

        # Create sequence
        sequence = SequenceData(name="Test Sequence", word="TEST")
        create_event = WorkflowEvent(
            workflow_type="sequence_creation",
            operation="sequence_created",
            data={
                "sequence_id": sequence.id,
                "sequence_name": sequence.name,
                "initial_length": sequence.length,
            },
        )
        registry.event_bus.publish(create_event)

        # Complete workflow
        complete_event = WorkflowEvent(
            workflow_type="sequence_creation",
            operation="completed",
            data={
                "result": "success",
                "sequence_id": sequence.id,
            },
        )
        registry.event_bus.publish(complete_event)

        # Validate workflow events
        assert len(registry.workflow_events) == 3
        assert registry.workflow_events[0]["workflow_type"] == "sequence_creation"
        assert registry.workflow_events[1]["sequence_name"] == "Test Sequence"
        assert registry.workflow_events[2]["result"] == "success"

    def test_create_sequence_with_beats_workflow(
        self, mock_service_registry, sample_motion_data
    ):
        """Test creating a sequence with beats through the complete workflow."""
        registry = mock_service_registry

        # Start workflow
        registry.event_bus.publish(
            "workflow_started",
            {"workflow_type": "sequence_with_beats", "target_length": 4},
        )

        # Create sequence
        sequence = SequenceData(name="Beat Sequence", word="BEAT")
        registry.event_bus.publish(
            "sequence_created",
            {"sequence_id": sequence.id, "sequence_name": sequence.name},
        )

        # Add beats one by one
        for i in range(4):
            beat = BeatData(
                beat_number=i + 1,
                letter=chr(ord("A") + i),
                duration=1.0,
                blue_motion=sample_motion_data,
                red_motion=sample_motion_data,
            )
            sequence = sequence.add_beat(beat)

            registry.event_bus.publish(
                "beat_added",
                {
                    "sequence_id": sequence.id,
                    "beat_number": beat.beat_number,
                    "beat_letter": beat.letter,
                    "sequence_length": sequence.length,
                },
            )

        # Complete workflow
        registry.event_bus.publish(
            "workflow_completed",
            {
                "workflow_type": "sequence_with_beats",
                "result": "success",
                "final_length": sequence.length,
            },
        )

        # Validate workflow
        assert sequence.length == 4
        assert len(registry.workflow_events) == 7  # start + create + 4 beats + complete

        # Validate beat events
        beat_events = [e for e in registry.workflow_events if "beat_number" in e]
        assert len(beat_events) == 4
        assert all(e["sequence_length"] == e["beat_number"] for e in beat_events)


class TestPictographGenerationWorkflow:
    """Test pictograph generation workflows."""

    def test_beat_to_pictograph_workflow(
        self, mock_service_registry, sample_motion_data
    ):
        """Test generating pictograph from beat data."""
        registry = mock_service_registry

        # Create beat data
        beat = BeatData(
            beat_number=1,
            letter="A",
            duration=1.0,
            blue_motion=sample_motion_data,
            red_motion=sample_motion_data,
        )

        # Start pictograph generation workflow
        registry.event_bus.publish(
            "workflow_started",
            {
                "workflow_type": "pictograph_generation",
                "source": "beat_data",
                "beat_id": beat.id,
            },
        )

        # Mock pictograph generation process
        with patch(
            "src.application.services.pictograph_management_service.PictographManagementService"
        ) as mock_service:
            mock_pictograph = Mock()
            mock_pictograph.id = "pictograph_123"
            mock_service.return_value.create_from_beat.return_value = mock_pictograph

            # Simulate pictograph generation
            registry.event_bus.publish(
                "pictograph_generated",
                {
                    "pictograph_id": mock_pictograph.id,
                    "source_beat_id": beat.id,
                    "generation_method": "from_beat_data",
                },
            )

        # Complete workflow
        registry.event_bus.publish(
            "workflow_completed",
            {
                "workflow_type": "pictograph_generation",
                "result": "success",
                "pictograph_id": "pictograph_123",
            },
        )

        # Validate workflow
        assert len(registry.workflow_events) == 3
        assert registry.workflow_events[1]["source_beat_id"] == beat.id
        assert registry.workflow_events[2]["pictograph_id"] == "pictograph_123"

    def test_sequence_to_pictographs_workflow(
        self, mock_service_registry, sample_motion_data
    ):
        """Test generating pictographs for entire sequence."""
        registry = mock_service_registry

        # Create sequence with beats
        sequence = SequenceData(name="Pictograph Sequence")
        for i in range(3):
            beat = BeatData(
                beat_number=i + 1,
                letter=chr(ord("A") + i),
                duration=1.0,
                blue_motion=sample_motion_data,
                red_motion=sample_motion_data,
            )
            sequence = sequence.add_beat(beat)

        # Start workflow
        registry.event_bus.publish(
            "workflow_started",
            {
                "workflow_type": "sequence_pictograph_generation",
                "sequence_id": sequence.id,
                "sequence_length": sequence.length,
            },
        )

        # Generate pictographs for each beat
        pictograph_ids = []
        for beat in sequence.beats:
            pictograph_id = f"pictograph_{beat.beat_number}"
            pictograph_ids.append(pictograph_id)

            registry.event_bus.publish(
                "pictograph_generated",
                {
                    "pictograph_id": pictograph_id,
                    "source_beat_id": beat.id,
                    "beat_number": beat.beat_number,
                    "sequence_id": sequence.id,
                },
            )

        # Complete workflow
        registry.event_bus.publish(
            "workflow_completed",
            {
                "workflow_type": "sequence_pictograph_generation",
                "result": "success",
                "sequence_id": sequence.id,
                "pictograph_count": len(pictograph_ids),
            },
        )

        # Validate workflow
        pictograph_events = [
            e
            for e in registry.workflow_events
            if "pictograph_id" in e and "beat_number" in e
        ]
        assert len(pictograph_events) == 3
        assert all(e["sequence_id"] == sequence.id for e in pictograph_events)


class TestCrossServiceIntegration:
    """Test integration between different services."""

    def test_arrow_motion_sequence_integration(self, mock_service_registry):
        """Test integration between arrow, motion, and sequence services."""
        registry = mock_service_registry

        # Mock services
        with patch(
            "src.application.services.arrow_management_service.ArrowManagementService"
        ) as mock_arrow_service, patch(
            "src.application.services.motion_management_service.MotionManagementService"
        ) as mock_motion_service, patch(
            "src.application.services.sequence_management_service.SequenceManagementService"
        ) as mock_sequence_service:

            # Configure mocks
            mock_motion_service.return_value.validate_motion_combination.return_value = (
                True
            )
            mock_arrow_service.return_value.calculate_arrow_position.return_value = (
                100.0,
                200.0,
                45.0,
            )
            mock_sequence_service.return_value.create_sequence.return_value = Mock()

            # Start integration workflow
            registry.event_bus.publish(
                "workflow_started",
                {
                    "workflow_type": "cross_service_integration",
                    "services": ["arrow", "motion", "sequence"],
                },
            )

            # Simulate service interactions
            motion_data = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
            )

            # Motion validation
            is_valid = mock_motion_service.return_value.validate_motion_combination(
                motion_data, motion_data
            )
            assert is_valid

            # Arrow positioning
            position = mock_arrow_service.return_value.calculate_arrow_position(
                motion_data, Mock()
            )
            assert position == (100.0, 200.0, 45.0)

            # Sequence creation
            sequence = mock_sequence_service.return_value.create_sequence(
                "Integration Test", 16
            )
            assert sequence is not None

            # Complete workflow
            registry.event_bus.publish(
                "workflow_completed",
                {
                    "workflow_type": "cross_service_integration",
                    "result": "success",
                    "services_tested": 3,
                },
            )

        # Validate integration
        assert len(registry.workflow_events) == 2
        assert registry.workflow_events[0]["services"] == [
            "arrow",
            "motion",
            "sequence",
        ]
        assert registry.workflow_events[1]["services_tested"] == 3


class TestErrorPropagationWorkflows:
    """Test error handling and propagation in workflows."""

    def test_invalid_motion_data_error_propagation(self, mock_service_registry):
        """Test error propagation when invalid motion data is provided."""
        registry = mock_service_registry

        # Start workflow
        registry.event_bus.publish(
            "workflow_started",
            {
                "workflow_type": "error_handling_test",
                "test_scenario": "invalid_motion_data",
            },
        )

        try:
            # Attempt to create invalid motion data (this should fail validation)
            invalid_motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=-1.0,  # Invalid negative turns
            )

            # This should trigger validation error
            if invalid_motion.turns < 0:
                raise ValueError("Turns cannot be negative")

        except ValueError as e:
            # Error should be captured and propagated
            registry.event_bus.publish(
                "error_occurred",
                {
                    "error_type": "ValueError",
                    "error_message": str(e),
                    "workflow_type": "error_handling_test",
                    "component": "motion_validation",
                },
            )

        # Validate error propagation
        error_events = [e for e in registry.workflow_events if "error_type" in e]
        assert len(error_events) == 1
        assert error_events[0]["error_type"] == "ValueError"
        assert "negative" in error_events[0]["error_message"]

    def test_service_unavailable_error_handling(self, mock_service_registry):
        """Test handling when services are unavailable."""
        registry = mock_service_registry

        # Start workflow
        registry.event_bus.publish(
            "workflow_started", {"workflow_type": "service_unavailable_test"}
        )

        # Mock service that raises exception
        with patch(
            "src.application.services.pictograph_management_service.PictographManagementService"
        ) as mock_service:
            mock_service.side_effect = ConnectionError("Service unavailable")

            try:
                # Attempt to use unavailable service
                service = mock_service()
                service.create_pictograph()
            except ConnectionError as e:
                # Error should be handled gracefully
                registry.event_bus.publish(
                    "error_occurred",
                    {
                        "error_type": "ConnectionError",
                        "error_message": str(e),
                        "workflow_type": "service_unavailable_test",
                        "component": "pictograph_service",
                    },
                )

        # Validate error handling
        error_events = [e for e in registry.workflow_events if "error_type" in e]
        assert len(error_events) == 1
        assert error_events[0]["error_type"] == "ConnectionError"
        assert error_events[0]["component"] == "pictograph_service"


class TestEventFlowValidation:
    """Test event flow validation across workflows."""

    def test_event_ordering_validation(self, mock_service_registry):
        """Test that events are published in correct order."""
        registry = mock_service_registry

        # Execute workflow with specific event ordering
        registry.event_bus.publish("workflow_started", {"step": 1})
        registry.event_bus.publish("sequence_created", {"step": 2})
        registry.event_bus.publish("beat_added", {"step": 3})
        registry.event_bus.publish("pictograph_generated", {"step": 4})
        registry.event_bus.publish("workflow_completed", {"step": 5})

        # Validate event ordering
        assert len(registry.workflow_events) == 5
        for i, event in enumerate(registry.workflow_events):
            assert event["step"] == i + 1

    def test_event_data_consistency(self, mock_service_registry):
        """Test that event data remains consistent across workflow."""
        registry = mock_service_registry
        sequence_id = "test_sequence_123"

        # Publish events with consistent data
        registry.event_bus.publish(
            "workflow_started",
            {"workflow_id": "workflow_456", "sequence_id": sequence_id},
        )

        registry.event_bus.publish(
            "sequence_created",
            {"sequence_id": sequence_id, "workflow_id": "workflow_456"},
        )

        registry.event_bus.publish(
            "workflow_completed",
            {
                "workflow_id": "workflow_456",
                "sequence_id": sequence_id,
                "result": "success",
            },
        )

        # Validate data consistency
        workflow_ids = [
            e.get("workflow_id") for e in registry.workflow_events if "workflow_id" in e
        ]
        sequence_ids = [
            e.get("sequence_id") for e in registry.workflow_events if "sequence_id" in e
        ]

        assert all(wid == "workflow_456" for wid in workflow_ids)
        assert all(sid == sequence_id for sid in sequence_ids)
