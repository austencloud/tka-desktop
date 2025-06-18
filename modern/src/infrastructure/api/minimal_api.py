"""
Minimal REST API for TKA Desktop.
Provides external access to core functionality with minimal overhead.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import asyncio
import threading
import logging

# Import API models
from .api_models import (
    BeatAPI, 
    SequenceAPI, 
    CreateSequenceRequest, 
    APIResponse, 
    CommandResponse,
    MotionAPI,
    MotionTypeAPI,
    RotationDirectionAPI,
    LocationAPI
)

logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="TKA Desktop API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for current sequence (will be replaced with proper service integration)
_current_sequence: Optional[SequenceAPI] = None
_sequence_counter = 0

def get_next_sequence_id() -> str:
    global _sequence_counter
    _sequence_counter += 1
    return f"seq_{_sequence_counter}"

# Dependency injection placeholder - will be replaced with actual DI integration
def get_sequence_service():
    """Placeholder for sequence service dependency injection."""
    # This will be replaced with actual service resolution from DI container
    return None

# Simple conversion functions
def domain_to_api_sequence(sequence) -> Optional[SequenceAPI]:
    """Convert domain SequenceData to API SequenceAPI."""
    if not sequence:
        return None
    
    api_beats = []
    for beat in sequence.beats:
        # Convert domain BeatData to API BeatAPI
        blue_motion = None
        if beat.blue_motion:
            blue_motion = MotionAPI(
                motion_type=MotionTypeAPI(beat.blue_motion.motion_type.value),
                prop_rot_dir=RotationDirectionAPI(beat.blue_motion.prop_rot_dir.value),
                start_loc=LocationAPI(beat.blue_motion.start_loc.value),
                end_loc=LocationAPI(beat.blue_motion.end_loc.value),
                turns=beat.blue_motion.turns,
                start_ori=beat.blue_motion.start_ori,
                end_ori=beat.blue_motion.end_ori
            )
        
        red_motion = None
        if beat.red_motion:
            red_motion = MotionAPI(
                motion_type=MotionTypeAPI(beat.red_motion.motion_type.value),
                prop_rot_dir=RotationDirectionAPI(beat.red_motion.prop_rot_dir.value),
                start_loc=LocationAPI(beat.red_motion.start_loc.value),
                end_loc=LocationAPI(beat.red_motion.end_loc.value),
                turns=beat.red_motion.turns,
                start_ori=beat.red_motion.start_ori,
                end_ori=beat.red_motion.end_ori
            )
        
        api_beat = BeatAPI(
            id=beat.id,
            beat_number=beat.beat_number,
            letter=beat.letter,
            duration=beat.duration,
            blue_motion=blue_motion,
            red_motion=red_motion,
            blue_reversal=beat.blue_reversal,
            red_reversal=beat.red_reversal,
            is_blank=beat.is_blank,
            metadata=beat.metadata
        )
        api_beats.append(api_beat)
    
    return SequenceAPI(
        id=sequence.id,
        name=sequence.name,
        word=sequence.word,
        beats=api_beats,
        start_position=sequence.start_position,
        metadata=sequence.metadata
    )

# API endpoints
@app.get("/api/status")
async def get_status():
    """Get application status."""
    return {
        "status": "running",
        "version": "2.0.0",
        "api_enabled": True
    }

@app.get("/api/current-sequence", response_model=Optional[SequenceAPI])
async def get_current_sequence():
    """Get the currently active sequence."""
    global _current_sequence
    return _current_sequence

@app.post("/api/sequences", response_model=SequenceAPI)
async def create_sequence(request: CreateSequenceRequest):
    """Create a new sequence."""
    try:
        global _current_sequence
        
        sequence_id = get_next_sequence_id()
        
        # Create beats for the sequence
        beats = []
        if request.beats:
            beats = request.beats
        else:
            # Create empty beats
            for i in range(request.length):
                beat = BeatAPI(
                    id=f"beat_{sequence_id}_{i+1}",
                    beat_number=i + 1,
                    letter=None,
                    duration=1.0,
                    is_blank=True
                )
                beats.append(beat)
        
        sequence = SequenceAPI(
            id=sequence_id,
            name=request.name,
            beats=beats
        )
        
        _current_sequence = sequence
        return sequence
        
    except Exception as e:
        logger.error(f"Failed to create sequence: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/undo")
async def undo_last_action():
    """Undo the last action."""
    # Mock implementation - will be replaced with actual service integration
    return {
        "success": False,
        "message": "Undo not yet implemented",
        "can_undo": False,
        "can_redo": False
    }

@app.post("/api/redo")
async def redo_last_action():
    """Redo the last undone action."""
    # Mock implementation - will be replaced with actual service integration
    return {
        "success": False,
        "message": "Redo not yet implemented",
        "can_undo": False,
        "can_redo": False
    }
