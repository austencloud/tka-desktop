# **Task 3.1: REST API Layer**

**Timeline**: Week 1 of Phase 3  
**Priority**: MEDIUM  
**Goal**: Create cross-language API layer for TKA functionality

---

## **Create API Infrastructure:**

### **FILE: src/infrastructure/api/rest_api.py**

```python
"""
REST API layer for cross-language access to TKA functionality.
Enables TypeScript, Rust, C++, or other language clients.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime

from src.core.dependency_injection.di_container import get_container
from src.domain.models.core_models import SequenceData, BeatData, MotionData
from src.application.services.core.sequence_management_service import SequenceManagementService

# API Models (Pydantic for validation and OpenAPI generation)
class MotionAPI(BaseModel):
    """API model for motion data."""
    motion_type: str
    prop_rot_dir: str
    start_loc: str
    end_loc: str
    turns: float = 0.0
    start_ori: str = "in"
    end_ori: str = "in"

    class Config:
        schema_extra = {
            "example": {
                "motion_type": "pro",
                "prop_rot_dir": "cw",
                "start_loc": "n",
                "end_loc": "e",
                "turns": 1.0,
                "start_ori": "in",
                "end_ori": "out"
            }
        }

class BeatAPI(BaseModel):
    """API model for beat data."""
    id: str
    beat_number: int
    letter: Optional[str] = None
    duration: float = 1.0
    blue_motion: Optional[MotionAPI] = None
    red_motion: Optional[MotionAPI] = None
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SequenceAPI(BaseModel):
    """API model for sequence data."""
    id: str
    name: str = ""
    word: str = ""
    beats: List[BeatAPI] = Field(default_factory=list)
    start_position: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        schema_extra = {
            "example": {
                "id": "seq_123",
                "name": "Example Sequence",
                "word": "HELLO",
                "beats": [],
                "start_position": "n",
                "metadata": {}
            }
        }

class CreateSequenceRequest(BaseModel):
    """Request model for creating sequences."""
    name: str = "New Sequence"
    beats: Optional[List[BeatAPI]] = None

class UpdateSequenceRequest(BaseModel):
    """Request model for updating sequences."""
    name: Optional[str] = None
    beats: Optional[List[BeatAPI]] = None
    metadata: Optional[Dict[str, Any]] = None

# FastAPI Application
app = FastAPI(
    title="TKA Desktop API",
    description="Cross-language API for Kinetic Alphabet Desktop",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
def get_sequence_service() -> SequenceManagementService:
    """Get sequence service from DI container."""
    container = get_container()
    return container.resolve(SequenceManagementService)

# Conversion utilities
def domain_to_api_motion(motion: MotionData) -> MotionAPI:
    """Convert domain motion to API model."""
    return MotionAPI(
        motion_type=motion.motion_type.value,
        prop_rot_dir=motion.prop_rot_dir.value,
        start_loc=motion.start_loc.value,
        end_loc=motion.end_loc.value,
        turns=motion.turns,
        start_ori=motion.start_ori,
        end_ori=motion.end_ori
    )

def api_to_domain_motion(motion: MotionAPI) -> MotionData:
    """Convert API motion to domain model."""
    return MotionData.from_dict(motion.dict())

def domain_to_api_beat(beat: BeatData) -> BeatAPI:
    """Convert domain beat to API model."""
    return BeatAPI(
        id=beat.id,
        beat_number=beat.beat_number,
        letter=beat.letter,
        duration=beat.duration,
        blue_motion=domain_to_api_motion(beat.blue_motion) if beat.blue_motion else None,
        red_motion=domain_to_api_motion(beat.red_motion) if beat.red_motion else None,
        blue_reversal=beat.blue_reversal,
        red_reversal=beat.red_reversal,
        is_blank=beat.is_blank,
        metadata=beat.metadata
    )

def domain_to_api_sequence(sequence: SequenceData) -> SequenceAPI:
    """Convert domain sequence to API model."""
    return SequenceAPI(
        id=sequence.id,
        name=sequence.name,
        word=sequence.word,
        beats=[domain_to_api_beat(beat) for beat in sequence.beats],
        start_position=sequence.start_position,
        metadata=sequence.metadata
    )

# API Endpoints
@app.get("/api/sequences/", response_model=List[SequenceAPI])
async def list_sequences(service: SequenceManagementService = Depends(get_sequence_service)):
    """List all sequences."""
    try:
        sequences = service.get_all_sequences()
        return [domain_to_api_sequence(seq) for seq in sequences]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sequences/", response_model=SequenceAPI)
async def create_sequence(
    request: CreateSequenceRequest,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Create a new sequence."""
    try:
        sequence = service.create_sequence(name=request.name)

        # Add beats if provided
        if request.beats:
            for beat_api in request.beats:
                beat_data = BeatData.from_dict(beat_api.dict())
                sequence = service.add_beat_with_undo(beat_data)

        return domain_to_api_sequence(sequence)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/sequences/{sequence_id}", response_model=SequenceAPI)
async def get_sequence(
    sequence_id: str,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Get a specific sequence."""
    try:
        sequence = service.get_sequence(sequence_id)
        if not sequence:
            raise HTTPException(status_code=404, detail="Sequence not found")
        return domain_to_api_sequence(sequence)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/sequences/{sequence_id}", response_model=SequenceAPI)
async def update_sequence(
    sequence_id: str,
    request: UpdateSequenceRequest,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Update a sequence."""
    try:
        sequence = service.get_sequence(sequence_id)
        if not sequence:
            raise HTTPException(status_code=404, detail="Sequence not found")

        updates = {}
        if request.name is not None:
            updates["name"] = request.name
        if request.metadata is not None:
            updates["metadata"] = request.metadata

        if updates:
            sequence = service.update_sequence(sequence.update(**updates))

        return domain_to_api_sequence(sequence)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/sequences/{sequence_id}")
async def delete_sequence(
    sequence_id: str,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Delete a sequence."""
    try:
        success = service.delete_sequence(sequence_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sequence not found")
        return {"message": "Sequence deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sequences/{sequence_id}/beats/", response_model=SequenceAPI)
async def add_beat(
    sequence_id: str,
    beat: BeatAPI,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Add a beat to a sequence."""
    try:
        beat_data = BeatData.from_dict(beat.dict())
        sequence = service.add_beat_with_undo(beat_data)
        return domain_to_api_sequence(sequence)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0"
    }

# API Server
class TKAAPIServer:
    """API server for TKA Desktop."""

    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self.server = None

    def start(self):
        """Start the API server."""
        uvicorn.run(app, host=self.host, port=self.port, log_level="info")

    async def start_async(self):
        """Start the API server asynchronously."""
        config = uvicorn.Config(app, host=self.host, port=self.port, log_level="info")
        self.server = uvicorn.Server(config)
        await self.server.serve()

    def stop(self):
        """Stop the API server."""
        if self.server:
            self.server.should_exit = True
```

---

## **Success Criteria:**

By the end of Task 3.1:

- ✅ **REST API layer** implemented with FastAPI
- ✅ **OpenAPI documentation** auto-generated
- ✅ **CORS support** for web clients
- ✅ **Type validation** with Pydantic models
- ✅ **Error handling** with proper HTTP status codes
- ✅ **Health check endpoint** for monitoring

---

## **Next Step**

After completing the REST API layer, proceed to: [Task 3.2: Schema-First Development](02_schema_first_development.md)
