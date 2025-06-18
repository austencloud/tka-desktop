"""
API data models with comprehensive validation and serialization.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# === Core API Models ===


class MotionTypeAPI(str, Enum):
    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"


class RotationDirectionAPI(str, Enum):
    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"
    NO_ROTATION = "no_rot"


class LocationAPI(str, Enum):
    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"
    NORTHEAST = "ne"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"
    NORTHWEST = "nw"


class MotionAPI(BaseModel):
    motion_type: MotionTypeAPI
    prop_rot_dir: RotationDirectionAPI
    start_loc: LocationAPI
    end_loc: LocationAPI
    turns: float = Field(default=0.0, ge=0.0, le=4.0)
    start_ori: str = Field(default="in", pattern="^(in|out)$")
    end_ori: str = Field(default="in", pattern="^(in|out)$")


class BeatAPI(BaseModel):
    id: str = Field(..., description="Unique beat identifier")
    beat_number: int = Field(..., ge=1, le=64)
    letter: Optional[str] = Field(None, pattern="^[A-Za-z]?$")
    duration: float = Field(default=1.0, gt=0.0, le=10.0)
    blue_motion: Optional[MotionAPI] = None
    red_motion: Optional[MotionAPI] = None
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SequenceAPI(BaseModel):
    id: str
    name: str = Field(..., min_length=1, max_length=100)
    word: str = ""
    beats: List[BeatAPI] = Field(default_factory=list)
    start_position: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @property
    def length(self) -> int:
        return len(self.beats)


# === Request/Response Models ===


class CreateSequenceRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    length: int = Field(default=16, ge=1, le=64)
    beats: Optional[List[BeatAPI]] = None


class APIResponse(BaseModel):
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class CommandResponse(APIResponse):
    command_id: str = ""
    can_undo: bool = False
    can_redo: bool = False
    undo_description: Optional[str] = None
