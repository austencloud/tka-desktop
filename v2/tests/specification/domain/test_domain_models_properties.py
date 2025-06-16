"""
Property-based tests for TKA Modern domain models.

These tests use Hypothesis to generate random valid inputs and verify
that domain model invariants hold across all possible inputs.

TESTS:
- MotionData invariants and serialization
- BeatData invariants and immutability
- SequenceData invariants and operations
- GlyphData serialization roundtrips
"""

import pytest
from hypothesis import given, strategies as st, assume
from src.domain.models.core_models import (
    MotionData,
    BeatData,
    SequenceData,
    GlyphData,
    MotionType,
    RotationDirection,
    Location,
    VTGMode,
    ElementalType,
    LetterType,
)


class TestMotionDataProperties:
    """Property-based tests for MotionData."""

    @given(
        motion_type=st.sampled_from(MotionType),
        prop_rot_dir=st.sampled_from(RotationDirection),
        start_loc=st.sampled_from(Location),
        end_loc=st.sampled_from(Location),
        turns=st.floats(
            min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False
        ),
        start_ori=st.sampled_from(["in", "out"]),
        end_ori=st.sampled_from(["in", "out"]),
    )
    def test_motion_data_creation_invariants(
        self, motion_type, prop_rot_dir, start_loc, end_loc, turns, start_ori, end_ori
    ):
        """Test that MotionData maintains invariants during creation."""
        motion = MotionData(
            motion_type=motion_type,
            prop_rot_dir=prop_rot_dir,
            start_loc=start_loc,
            end_loc=end_loc,
            turns=turns,
            start_ori=start_ori,
            end_ori=end_ori,
        )

        # Invariant: All fields should be preserved
        assert motion.motion_type == motion_type
        assert motion.prop_rot_dir == prop_rot_dir
        assert motion.start_loc == start_loc
        assert motion.end_loc == end_loc
        assert motion.turns == turns
        assert motion.start_ori == start_ori
        assert motion.end_ori == end_ori

    @given(
        motion_type=st.sampled_from(MotionType),
        prop_rot_dir=st.sampled_from(RotationDirection),
        start_loc=st.sampled_from(Location),
        end_loc=st.sampled_from(Location),
        turns=st.floats(
            min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False
        ),
        start_ori=st.sampled_from(["in", "out"]),
        end_ori=st.sampled_from(["in", "out"]),
    )
    def test_motion_data_serialization_roundtrip(
        self, motion_type, prop_rot_dir, start_loc, end_loc, turns, start_ori, end_ori
    ):
        """Test that MotionData serialization is lossless."""
        original = MotionData(
            motion_type=motion_type,
            prop_rot_dir=prop_rot_dir,
            start_loc=start_loc,
            end_loc=end_loc,
            turns=turns,
            start_ori=start_ori,
            end_ori=end_ori,
        )

        # Serialize to dict and back
        data_dict = original.to_dict()
        reconstructed = MotionData.from_dict(data_dict)

        # Invariant: Roundtrip should be lossless
        assert reconstructed == original
        assert reconstructed.to_dict() == data_dict

    @given(
        motion_type=st.sampled_from(MotionType),
        prop_rot_dir=st.sampled_from(RotationDirection),
        start_loc=st.sampled_from(Location),
        end_loc=st.sampled_from(Location),
        turns=st.floats(
            min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_motion_data_immutability(
        self, motion_type, prop_rot_dir, start_loc, end_loc, turns
    ):
        """Test that MotionData is truly immutable."""
        motion = MotionData(
            motion_type=motion_type,
            prop_rot_dir=prop_rot_dir,
            start_loc=start_loc,
            end_loc=end_loc,
            turns=turns,
        )

        # Invariant: Should not be able to modify fields
        with pytest.raises(AttributeError):
            motion.motion_type = MotionType.PRO
        with pytest.raises(AttributeError):
            motion.turns = 5.0


class TestBeatDataProperties:
    """Property-based tests for BeatData."""

    @given(
        beat_number=st.integers(min_value=1, max_value=64),
        duration=st.floats(
            min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False
        ),
        letter=st.one_of(
            st.none(),
            st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=1),
        ),
        is_blank=st.booleans(),
    )
    def test_beat_data_creation_invariants(
        self, beat_number, duration, letter, is_blank
    ):
        """Test that BeatData maintains invariants during creation."""
        beat = BeatData(
            beat_number=beat_number, duration=duration, letter=letter, is_blank=is_blank
        )

        # Invariant: Beat number must be positive
        assert beat.beat_number >= 1

        # Invariant: Duration must be positive
        assert beat.duration > 0

        # Invariant: ID should be generated
        assert beat.id is not None
        assert len(beat.id) > 0

    @given(
        beat_number=st.integers(min_value=1, max_value=64),
        duration=st.floats(
            min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_beat_data_update_immutability(self, beat_number, duration):
        """Test that BeatData.update() creates new instances."""
        original = BeatData(beat_number=beat_number, duration=duration)
        updated = original.update(letter="A")

        # Invariant: Update should create new instance
        assert original is not updated
        assert original.letter != updated.letter
        assert original.beat_number == updated.beat_number
        assert original.duration == updated.duration

    @given(st.data())
    def test_beat_data_serialization_roundtrip(self, data):
        """Test that BeatData serialization is lossless."""
        # Generate a valid BeatData
        beat_number = data.draw(st.integers(min_value=1, max_value=64))
        duration = data.draw(
            st.floats(
                min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False
            )
        )
        letter = data.draw(
            st.one_of(
                st.none(),
                st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=1),
            )
        )

        original = BeatData(beat_number=beat_number, duration=duration, letter=letter)

        # Serialize to dict and back
        data_dict = original.to_dict()
        reconstructed = BeatData.from_dict(data_dict)

        # Invariant: Roundtrip should be lossless
        assert reconstructed.beat_number == original.beat_number
        assert reconstructed.duration == original.duration
        assert reconstructed.letter == original.letter
        assert reconstructed.is_blank == original.is_blank


class TestSequenceDataProperties:
    """Property-based tests for SequenceData."""

    @given(
        name=st.text(min_size=0, max_size=100), word=st.text(min_size=0, max_size=50)
    )
    def test_sequence_data_creation_invariants(self, name, word):
        """Test that SequenceData maintains invariants during creation."""
        sequence = SequenceData(name=name, word=word)

        # Invariant: ID should be generated
        assert sequence.id is not None
        assert len(sequence.id) > 0

        # Invariant: Empty sequence properties
        assert sequence.length == 0
        assert sequence.total_duration == 0.0
        assert sequence.is_empty is True
        assert sequence.is_valid is False

    @given(beat_count=st.integers(min_value=1, max_value=16))
    def test_sequence_data_beat_operations(self, beat_count):
        """Test that sequence beat operations maintain invariants."""
        sequence = SequenceData.empty()

        # Add beats one by one
        for i in range(beat_count):
            beat = BeatData(
                beat_number=i + 1, duration=1.0, letter=chr(ord("A") + i % 26)
            )
            sequence = sequence.add_beat(beat)

            # Invariant: Length should increase
            assert sequence.length == i + 1

            # Invariant: Beat numbers should be sequential
            for j, beat in enumerate(sequence.beats):
                assert beat.beat_number == j + 1

    @given(
        initial_count=st.integers(min_value=2, max_value=8),
        remove_index=st.integers(min_value=1, max_value=8),
    )
    def test_sequence_data_remove_beat_invariants(self, initial_count, remove_index):
        """Test that removing beats maintains sequence invariants."""
        assume(remove_index <= initial_count)

        # Create sequence with beats
        sequence = SequenceData.empty()
        for i in range(initial_count):
            beat = BeatData(beat_number=i + 1, duration=1.0)
            sequence = sequence.add_beat(beat)

        # Remove a beat
        sequence = sequence.remove_beat(remove_index)

        # Invariant: Length should decrease
        assert sequence.length == initial_count - 1

        # Invariant: Beat numbers should still be sequential
        for i, beat in enumerate(sequence.beats):
            assert beat.beat_number == i + 1

    @given(st.data())
    def test_sequence_data_serialization_roundtrip(self, data):
        """Test that SequenceData serialization is lossless."""
        name = data.draw(st.text(min_size=0, max_size=50))
        word = data.draw(st.text(min_size=0, max_size=20))
        beat_count = data.draw(st.integers(min_value=0, max_value=5))

        # Create sequence with beats
        sequence = SequenceData(name=name, word=word)
        for i in range(beat_count):
            beat = BeatData(beat_number=i + 1, duration=1.0)
            sequence = sequence.add_beat(beat)

        # Serialize to dict and back
        data_dict = sequence.to_dict()
        reconstructed = SequenceData.from_dict(data_dict)

        # Invariant: Roundtrip should be lossless
        assert reconstructed.name == sequence.name
        assert reconstructed.word == sequence.word
        assert reconstructed.length == sequence.length
        assert len(reconstructed.beats) == len(sequence.beats)


class TestGlyphDataProperties:
    """Property-based tests for GlyphData."""

    @given(
        vtg_mode=st.one_of(st.none(), st.sampled_from(VTGMode)),
        elemental_type=st.one_of(st.none(), st.sampled_from(ElementalType)),
        letter_type=st.one_of(st.none(), st.sampled_from(LetterType)),
        has_dash=st.booleans(),
        show_elemental=st.booleans(),
        show_vtg=st.booleans(),
        show_tka=st.booleans(),
        show_positions=st.booleans(),
    )
    def test_glyph_data_serialization_roundtrip(
        self,
        vtg_mode,
        elemental_type,
        letter_type,
        has_dash,
        show_elemental,
        show_vtg,
        show_tka,
        show_positions,
    ):
        """Test that GlyphData serialization is lossless."""
        original = GlyphData(
            vtg_mode=vtg_mode,
            elemental_type=elemental_type,
            letter_type=letter_type,
            has_dash=has_dash,
            show_elemental=show_elemental,
            show_vtg=show_vtg,
            show_tka=show_tka,
            show_positions=show_positions,
        )

        # Serialize to dict and back
        data_dict = original.to_dict()
        reconstructed = GlyphData.from_dict(data_dict)

        # Invariant: Roundtrip should be lossless
        assert reconstructed.vtg_mode == original.vtg_mode
        assert reconstructed.elemental_type == original.elemental_type
        assert reconstructed.letter_type == original.letter_type
        assert reconstructed.has_dash == original.has_dash
        assert reconstructed.show_elemental == original.show_elemental
        assert reconstructed.show_vtg == original.show_vtg
        assert reconstructed.show_tka == original.show_tka
        assert reconstructed.show_positions == original.show_positions
