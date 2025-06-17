"""
Basic TKA Workflow Scenarios
============================

Fundamental user interaction patterns for TKA parallel testing.
Based on verified TKA domain model and workflow patterns.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Test core TKA workflows for Legacy/Modern functional equivalence
"""

from typing import List, Dict, Any
import logging

from ..actions import (
    UserAction,
    ActionSequence,
    ActionType,
    GridPosition,
    MotionTypeValue,
    ActionParameters,
    ExpectedOutcome,
)


logger = logging.getLogger(__name__)


class BasicWorkflowScenarios:
    """Core TKA workflow scenarios for parallel testing."""

    def __init__(self):
        self.scenarios = {}
        self._create_basic_scenarios()

    def _create_basic_scenarios(self):
        """Create all basic workflow scenarios."""
        self.scenarios = {
            "start_position_selection": self.create_start_position_selection_scenario(),
            "single_beat_creation": self.create_single_beat_creation_scenario(),
            "sequence_building": self.create_sequence_building_scenario(),
            "motion_modification": self.create_motion_modification_scenario(),
            "graph_editor_toggle": self.create_graph_editor_toggle_scenario(),
            "sequence_clear": self.create_sequence_clear_scenario(),
        }

    def get_scenario(self, name: str) -> ActionSequence:
        """Get a scenario by name."""
        return self.scenarios.get(name)

    def get_all_scenarios(self) -> Dict[str, ActionSequence]:
        """Get all basic scenarios."""
        return self.scenarios.copy()

    def create_start_position_selection_scenario(self) -> ActionSequence:
        """
        Test start position selection across all grid positions.

        This is the foundation of all TKA workflows - selecting alpha, beta, or gamma
        start positions and verifying that option picker updates correctly.
        """
        sequence = ActionSequence(
            name="Start Position Selection",
            description="Test start position selection for alpha, beta, gamma positions",
            category="core_workflow",
            priority=1,
            estimated_duration_ms=15000,
        )

        # Test each start position
        for position in [GridPosition.ALPHA, GridPosition.BETA, GridPosition.GAMMA]:
            # Clear any existing sequence first
            clear_action = UserAction(
                action_type=ActionType.CLEAR_SEQUENCE,
                description=f"Clear sequence before testing {position.value} position",
                parameters=ActionParameters(),
                expected_outcome=ExpectedOutcome(sequence_length=0, beat_count=0),
                is_critical=True,
                tags=["setup", "clear"],
            )
            sequence.add_action(clear_action)

            # Select start position
            select_action = UserAction(
                action_type=ActionType.SELECT_START_POSITION,
                description=f"Select {position.value} start position",
                parameters=ActionParameters(grid_position=position),
                expected_outcome=ExpectedOutcome(
                    expected_data={"start_position": position.value},
                    max_execution_time_ms=3000,
                ),
                is_critical=True,
                tags=["start_position", position.value],
            )
            sequence.add_action(select_action)

            # Verify option picker has options available
            verify_action = UserAction(
                action_type=ActionType.EXTRACT_DATA,
                description=f"Verify option picker updated for {position.value}",
                parameters=ActionParameters(context={"verify_option_picker": True}),
                expected_outcome=ExpectedOutcome(
                    expected_data={"has_options": True}, max_execution_time_ms=2000
                ),
                is_critical=True,
                tags=["verification", "option_picker"],
            )
            sequence.add_action(verify_action)

        return sequence

    def create_single_beat_creation_scenario(self) -> ActionSequence:
        """
        Test creating a single beat through pictograph option selection.

        Verifies the core sequence building workflow: start position → option selection → beat creation.
        """
        sequence = ActionSequence(
            name="Single Beat Creation",
            description="Test creating a single beat from start position through option selection",
            category="core_workflow",
            priority=2,
            estimated_duration_ms=20000,
        )

        # Clear sequence
        clear_action = UserAction(
            action_type=ActionType.CLEAR_SEQUENCE,
            description="Clear sequence for clean test",
            parameters=ActionParameters(),
            expected_outcome=ExpectedOutcome(sequence_length=0, beat_count=0),
            is_critical=True,
            tags=["setup"],
        )
        sequence.add_action(clear_action)

        # Select alpha start position
        start_action = UserAction(
            action_type=ActionType.SELECT_START_POSITION,
            description="Select alpha start position",
            parameters=ActionParameters(grid_position=GridPosition.ALPHA),
            expected_outcome=ExpectedOutcome(expected_data={"start_position": "alpha"}),
            is_critical=True,
            tags=["start_position"],
        )
        sequence.add_action(start_action)

        # Select first available pictograph option
        option_action = UserAction(
            action_type=ActionType.SELECT_PICTOGRAPH_OPTION,
            description="Select first available pictograph option",
            parameters=ActionParameters(
                context={"option_index": 0}  # Select first option
            ),
            expected_outcome=ExpectedOutcome(
                beat_count=1, expected_data={"beat_added": True}
            ),
            is_critical=True,
            tags=["option_selection", "beat_creation"],
        )
        sequence.add_action(option_action)

        # Verify beat was created with correct data
        verify_action = UserAction(
            action_type=ActionType.EXTRACT_DATA,
            description="Verify beat was created correctly",
            parameters=ActionParameters(),
            expected_outcome=ExpectedOutcome(
                beat_count=1, expected_data={"sequence_length": 1}
            ),
            is_critical=True,
            tags=["verification"],
        )
        sequence.add_action(verify_action)

        return sequence

    def create_sequence_building_scenario(self) -> ActionSequence:
        """
        Test building a multi-beat sequence.

        Tests the dynamic option picker updates as sequence builds.
        """
        sequence = ActionSequence(
            name="Sequence Building",
            description="Test building a 3-beat sequence with dynamic option updates",
            category="core_workflow",
            priority=3,
            estimated_duration_ms=45000,
        )

        # Clear and start
        sequence.add_action(
            UserAction(
                action_type=ActionType.CLEAR_SEQUENCE,
                description="Clear sequence",
                parameters=ActionParameters(),
                expected_outcome=ExpectedOutcome(sequence_length=0),
                is_critical=True,
                tags=["setup"],
            )
        )

        sequence.add_action(
            UserAction(
                action_type=ActionType.SELECT_START_POSITION,
                description="Select alpha start position",
                parameters=ActionParameters(grid_position=GridPosition.ALPHA),
                expected_outcome=ExpectedOutcome(
                    expected_data={"start_position": "alpha"}
                ),
                is_critical=True,
                tags=["start_position"],
            )
        )

        # Add 3 beats sequentially
        for beat_num in range(1, 4):
            # Select option to add beat
            add_beat_action = UserAction(
                action_type=ActionType.SELECT_PICTOGRAPH_OPTION,
                description=f"Add beat {beat_num}",
                parameters=ActionParameters(
                    context={"option_index": 0, "beat_number": beat_num}
                ),
                expected_outcome=ExpectedOutcome(
                    beat_count=beat_num, expected_data={"beat_added": True}
                ),
                is_critical=True,
                tags=["beat_addition", f"beat_{beat_num}"],
            )
            sequence.add_action(add_beat_action)

            # Verify option picker updated with new options
            verify_options_action = UserAction(
                action_type=ActionType.EXTRACT_DATA,
                description=f"Verify options updated after beat {beat_num}",
                parameters=ActionParameters(context={"verify_option_picker": True}),
                expected_outcome=ExpectedOutcome(expected_data={"has_options": True}),
                is_critical=True,
                tags=["verification", "option_picker"],
            )
            sequence.add_action(verify_options_action)

        return sequence

    def create_motion_modification_scenario(self) -> ActionSequence:
        """
        Test motion modification operations.

        Tests turn adjustments and motion type changes.
        """
        sequence = ActionSequence(
            name="Motion Modification",
            description="Test motion turn adjustments and type changes",
            category="motion_editing",
            priority=4,
            estimated_duration_ms=30000,
        )

        # Setup: Create a beat first
        sequence.add_action(
            UserAction(
                action_type=ActionType.CLEAR_SEQUENCE,
                description="Clear sequence",
                parameters=ActionParameters(),
                expected_outcome=ExpectedOutcome(sequence_length=0),
                is_critical=True,
                tags=["setup"],
            )
        )

        sequence.add_action(
            UserAction(
                action_type=ActionType.SELECT_START_POSITION,
                description="Select alpha start position",
                parameters=ActionParameters(grid_position=GridPosition.ALPHA),
                expected_outcome=ExpectedOutcome(
                    expected_data={"start_position": "alpha"}
                ),
                is_critical=True,
                tags=["setup"],
            )
        )

        sequence.add_action(
            UserAction(
                action_type=ActionType.SELECT_PICTOGRAPH_OPTION,
                description="Create beat for modification",
                parameters=ActionParameters(),
                expected_outcome=ExpectedOutcome(beat_count=1),
                is_critical=True,
                tags=["setup"],
            )
        )

        # Test turn adjustments
        turn_adjustments = [1.0, -0.5, 0.5, -1.0]
        for adjustment in turn_adjustments:
            adjust_action = UserAction(
                action_type=ActionType.ADJUST_TURNS,
                description=f"Adjust turns by {adjustment}",
                parameters=ActionParameters(
                    turns=adjustment, beat_index=0  # First beat
                ),
                expected_outcome=ExpectedOutcome(
                    expected_data={"turns_adjusted": adjustment}
                ),
                is_critical=True,
                tags=["turn_adjustment"],
            )
            sequence.add_action(adjust_action)

        return sequence

    def create_graph_editor_toggle_scenario(self) -> ActionSequence:
        """
        Test graph editor toggle functionality.

        Verifies graph editor opens/closes correctly and maintains layout.
        """
        sequence = ActionSequence(
            name="Graph Editor Toggle",
            description="Test graph editor toggle functionality and layout preservation",
            category="ui_interaction",
            priority=5,
            estimated_duration_ms=20000,
        )

        # Setup: Create a beat first so graph editor has content
        sequence.add_action(
            UserAction(
                action_type=ActionType.CLEAR_SEQUENCE,
                description="Clear sequence",
                parameters=ActionParameters(),
                expected_outcome=ExpectedOutcome(sequence_length=0),
                is_critical=True,
                tags=["setup"],
            )
        )

        sequence.add_action(
            UserAction(
                action_type=ActionType.SELECT_START_POSITION,
                description="Select alpha start position",
                parameters=ActionParameters(grid_position=GridPosition.ALPHA),
                expected_outcome=ExpectedOutcome(
                    expected_data={"start_position": "alpha"}
                ),
                is_critical=True,
                tags=["setup"],
            )
        )

        sequence.add_action(
            UserAction(
                action_type=ActionType.SELECT_PICTOGRAPH_OPTION,
                description="Create beat for graph editor",
                parameters=ActionParameters(),
                expected_outcome=ExpectedOutcome(beat_count=1),
                is_critical=True,
                tags=["setup"],
            )
        )

        # Test graph editor toggle
        for toggle_count in range(3):  # Toggle 3 times to test stability
            # Open graph editor
            open_action = UserAction(
                action_type=ActionType.TOGGLE_GRAPH_EDITOR,
                description=f"Open graph editor (toggle {toggle_count + 1})",
                parameters=ActionParameters(),
                expected_outcome=ExpectedOutcome(
                    expected_data={"graph_editor_open": True}
                ),
                is_critical=True,
                tags=["graph_editor", "open"],
            )
            sequence.add_action(open_action)

            # Close graph editor
            close_action = UserAction(
                action_type=ActionType.TOGGLE_GRAPH_EDITOR,
                description=f"Close graph editor (toggle {toggle_count + 1})",
                parameters=ActionParameters(),
                expected_outcome=ExpectedOutcome(
                    expected_data={"graph_editor_open": False}
                ),
                is_critical=True,
                tags=["graph_editor", "close"],
            )
            sequence.add_action(close_action)

        return sequence

    def create_sequence_clear_scenario(self) -> ActionSequence:
        """
        Test sequence clearing functionality.

        Verifies that clearing resets all state correctly.
        """
        sequence = ActionSequence(
            name="Sequence Clear",
            description="Test sequence clearing and state reset",
            category="sequence_management",
            priority=6,
            estimated_duration_ms=25000,
        )

        # Build up a sequence first
        sequence.add_action(
            UserAction(
                action_type=ActionType.SELECT_START_POSITION,
                description="Select alpha start position",
                parameters=ActionParameters(grid_position=GridPosition.ALPHA),
                expected_outcome=ExpectedOutcome(
                    expected_data={"start_position": "alpha"}
                ),
                is_critical=True,
                tags=["setup"],
            )
        )

        # Add multiple beats
        for beat_num in range(1, 4):
            sequence.add_action(
                UserAction(
                    action_type=ActionType.SELECT_PICTOGRAPH_OPTION,
                    description=f"Add beat {beat_num}",
                    parameters=ActionParameters(),
                    expected_outcome=ExpectedOutcome(beat_count=beat_num),
                    is_critical=True,
                    tags=["setup", f"beat_{beat_num}"],
                )
            )

        # Verify sequence has content
        verify_content_action = UserAction(
            action_type=ActionType.EXTRACT_DATA,
            description="Verify sequence has content before clearing",
            parameters=ActionParameters(),
            expected_outcome=ExpectedOutcome(
                beat_count=3, expected_data={"sequence_length": 3}
            ),
            is_critical=True,
            tags=["verification", "pre_clear"],
        )
        sequence.add_action(verify_content_action)

        # Clear sequence
        clear_action = UserAction(
            action_type=ActionType.CLEAR_SEQUENCE,
            description="Clear the sequence",
            parameters=ActionParameters(),
            expected_outcome=ExpectedOutcome(
                sequence_length=0,
                beat_count=0,
                expected_data={"sequence_cleared": True},
            ),
            is_critical=True,
            tags=["clear"],
        )
        sequence.add_action(clear_action)

        # Verify sequence is empty
        verify_empty_action = UserAction(
            action_type=ActionType.EXTRACT_DATA,
            description="Verify sequence is empty after clearing",
            parameters=ActionParameters(),
            expected_outcome=ExpectedOutcome(sequence_length=0, beat_count=0),
            is_critical=True,
            tags=["verification", "post_clear"],
        )
        sequence.add_action(verify_empty_action)

        return sequence
